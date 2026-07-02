from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "database"


class QueryResult:
    def __init__(self, cursor):
        self.cursor = cursor
        self.lastrowid = cursor.lastrowid

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def __iter__(self):
        return iter(self.cursor.fetchall())


class MySQLConnection:
    def __init__(self):
        try:
            import pymysql
            from pymysql.cursors import DictCursor
        except ImportError as exc:
            raise RuntimeError(
                "Falta PyMySQL. Ejecuta: pip install -r requirements.txt"
            ) from exc

        self.pymysql = pymysql
        self.conn = pymysql.connect(
            host=os.getenv("MYSQL_HOST", "127.0.0.1"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "hospital_financiero"),
            charset="utf8mb4",
            cursorclass=DictCursor,
            autocommit=False,
        )

    def execute(self, sql, params=()):
        cursor = self.conn.cursor()
        cursor.execute(_mysql_sql(sql), tuple(params or ()))
        return QueryResult(cursor)

    def executescript(self, script):
        for statement in _split_sql(script):
            self.execute(statement)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.close()


def get_connection():
    return MySQLConnection()


def initialize_database():
    initialize_mysql_database()


def initialize_mysql_database():
    try:
        import pymysql
        from pymysql.cursors import DictCursor
    except ImportError as exc:
        raise RuntimeError("Falta PyMySQL. Ejecuta: pip install -r requirements.txt") from exc

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    config = mysql_config(include_database=False)
    with pymysql.connect(**config, cursorclass=DictCursor, autocommit=True) as conn:
        with conn.cursor() as cursor:
            schema = (DATA_DIR / "schema_mysql.sql").read_text(encoding="utf-8")
            for statement in _split_sql(schema):
                try:
                    cursor.execute(statement)
                except pymysql.err.OperationalError as exc:
                    if exc.args and exc.args[0] in {1050, 1061}:
                        continue
                    raise

    with MySQLConnection() as conn:
        migrate_mysql_schema(conn)
        total = conn.execute("SELECT COUNT(*) AS total FROM Usuario").fetchone()["total"]
        if int(total) == 0:
            seed = (DATA_DIR / "seed_mysql.sql").read_text(encoding="utf-8")
            conn.executescript(seed)


def migrate_mysql_schema(conn):
    conn.execute("""
      CREATE TABLE IF NOT EXISTS PagoReportado (
        id_reporte INT AUTO_INCREMENT PRIMARY KEY,
        id_factura INT NOT NULL,
        id_pago INT NOT NULL,
        monto DECIMAL(10,2) NOT NULL CHECK (monto >= 0),
        fecha_reporte DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        usuario_registro INT NOT NULL,
        observacion VARCHAR(255),
        estado VARCHAR(20) NOT NULL DEFAULT 'REPORTADO' CHECK (estado IN ('REPORTADO','VALIDADO','RECHAZADO')),
        CONSTRAINT FK_PagoReportado_Factura FOREIGN KEY(id_factura) REFERENCES Factura(id_factura),
        CONSTRAINT FK_PagoReportado_TipoPago FOREIGN KEY(id_pago) REFERENCES TipoPago(id_pago),
        CONSTRAINT FK_PagoReportado_Usuario FOREIGN KEY(usuario_registro) REFERENCES Usuario(id_usuario)
      )
    """)


def mysql_config(include_database=True):
    config = {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "charset": "utf8mb4",
    }
    if include_database:
        config["database"] = os.getenv("MYSQL_DATABASE", "hospital_financiero")
    return config


def mysql_connection_hint():
    return {
        "driver": "PyMySQL",
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": os.getenv("MYSQL_PORT", "3306"),
        "user": os.getenv("MYSQL_USER", "root"),
        "database": os.getenv("MYSQL_DATABASE", "hospital_financiero"),
        "schema": str(DATA_DIR / "schema_mysql.sql"),
    }


def current_database_label():
    cfg = mysql_connection_hint()
    return f"MySQL {cfg['user']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"


def _mysql_sql(sql):
    translated = sql
    translated = translated.replace("DATE('now')", "CURDATE()")
    translated = translated.replace("strftime('%Y-%m', fecha_factura)", "DATE_FORMAT(fecha_factura, '%%Y-%%m')")
    translated = translated.replace("strftime('%Y-%m','now')", "DATE_FORMAT(CURDATE(), '%%Y-%%m')")
    translated = translated.replace("strftime('%w', fecha_factura)", "DAYOFWEEK(fecha_factura) - 1")
    translated = _replace_full_name_concat(translated)
    translated = translated.replace("?", "%s")
    return translated


def _replace_full_name_concat(sql):
    import re

    pattern = re.compile(r"(\b(?:[A-Za-z_]\w*\.)?[A-Za-z_]\w*)\s*\|\|\s*' '\s*\|\|\s*(\b(?:[A-Za-z_]\w*\.)?[A-Za-z_]\w*)")
    return pattern.sub(r"CONCAT(\1, ' ', \2)", sql)


def _split_sql(script):
    statements = []
    current = []
    in_string = None
    escape = False

    for char in script:
        current.append(char)
        if char == "\\" and in_string:
            escape = not escape
            continue
        if char in {"'", '"'} and not escape:
            in_string = None if in_string == char else char if not in_string else in_string
        if char == ";" and not in_string:
            statement = "".join(current).strip().rstrip(";")
            if statement and not statement.startswith("--"):
                statements.append(statement)
            current = []
        escape = False

    tail = "".join(current).strip()
    if tail:
        statements.append(tail)
    return statements
