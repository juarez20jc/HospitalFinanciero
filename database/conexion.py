from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "database"
DB_PATH = DATA_DIR / "hospital_financiero.db"


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


class SQLiteConnection:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=ON")

    def execute(self, sql, params=()):
        cursor = self.conn.cursor()
        cursor.execute(sql, tuple(params or ()))
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
    return SQLiteConnection()


def initialize_database():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")

    schema = (DATA_DIR / "schema_sqlite.sql").read_text(encoding="utf-8")
    db.executescript(schema)

    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) AS total FROM Usuario")
    row = cursor.fetchone()
    total = int(row["total"]) if row else 0
    if total == 0:
        seed = (DATA_DIR / "seed_sqlite.sql").read_text(encoding="utf-8")
        db.executescript(seed)

    db.commit()
    db.close()


def current_database_label():
    return f"SQLite {DB_PATH}"


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
