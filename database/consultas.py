import csv
import hashlib
import io
from datetime import date, timedelta

from database.conexion import get_connection


class Repository:
    def validar_usuario(self, username, password):
        sql = """
        SELECT u.id_usuario, u.username, u.nombres, u.apellidos, u.email, r.nombre AS rol,
               p.id_paciente
        FROM Usuario u
        JOIN Rol r ON r.id_rol = u.id_rol
        LEFT JOIN Paciente p ON LOWER(p.email) = LOWER(u.email)
        WHERE u.username = ? AND u.password_hash = ? AND u.estado_activo = 1 AND u.eliminado = 0
        """
        with get_connection() as conn:
            row = conn.execute(sql, (username.strip(), self._hash(password))).fetchone()
            return dict(row) if row else None

    def paciente_portal(self, user):
        paciente = self._paciente_de_usuario(user)
        if not paciente:
            return {"paciente": None, "facturas": [], "citas": [], "kpis": {}}
        with get_connection() as conn:
            facturas = conn.execute("""
              SELECT f.id_factura, f.numero_factura, f.id_paciente, f.id_reserva,
                     f.fecha_factura, f.subtotal, f.igv, f.total,
                     CASE WHEN pr.id_reporte IS NOT NULL AND f.estado_pago='PENDIENTE' THEN 'REPORTADO' ELSE f.estado_pago END AS estado_pago,
                     f.motivo_anulacion, f.eliminado,
                     r.titulo AS cita, r.id_pago AS metodo_pago_reserva,
                     pr.observacion AS pago_reportado
              FROM Factura f
              LEFT JOIN Reservacion r ON r.id_reserva=f.id_reserva
              LEFT JOIN PagoReportado pr ON pr.id_factura=f.id_factura AND pr.estado='REPORTADO'
              WHERE f.id_paciente=? AND f.eliminado=0
              ORDER BY f.fecha_factura DESC
            """, (paciente["id_paciente"],)).fetchall()
            citas = conn.execute("""
              SELECT r.fecha_cita, r.hora_cita, r.titulo, r.precio,
                     m.nombres || ' ' || m.apellidos AS medico,
                     e.nombre AS especialidad,
                     es.nombre AS estado
              FROM Reservacion r
              JOIN Medico m ON m.id_medico=r.id_medico
              JOIN Especialidad e ON e.id_especialidad=m.id_especialidad
              JOIN Estado es ON es.id_estado=r.id_estado
              WHERE r.id_paciente=? AND r.eliminado=0
              ORDER BY r.fecha_cita DESC, r.hora_cita DESC
            """, (paciente["id_paciente"],)).fetchall()
        factura_rows = [dict(r) for r in facturas]
        return {
            "paciente": paciente,
            "facturas": factura_rows,
            "citas": [dict(r) for r in citas],
            "kpis": {
                "pendiente": sum(float(f["total"] or 0) for f in factura_rows if f["estado_pago"] in {"PENDIENTE", "REPORTADO"}),
                "pagado": sum(float(f["total"] or 0) for f in factura_rows if f["estado_pago"] == "PAGADO"),
                "facturas": len(factura_rows),
                "citas": len(citas),
            },
        }

    def detalle_factura_paciente(self, id_factura, user):
        paciente = self._paciente_de_usuario(user)
        if not paciente:
            return None
        with get_connection() as conn:
            owner = conn.execute("""
              SELECT id_factura FROM Factura
              WHERE id_factura=? AND id_paciente=? AND eliminado=0
            """, (id_factura, paciente["id_paciente"])).fetchone()
        return self.detalle_factura(id_factura) if owner else None

    def registrar_pago_paciente(self, data, user):
        paciente = self._paciente_de_usuario(user)
        if not paciente:
            return False
        with get_connection() as conn:
            factura = conn.execute("""
              SELECT f.id_factura, f.numero_factura, f.total, f.estado_pago, tp.nombre AS tipo_pago
              FROM Factura f
              JOIN TipoPago tp ON tp.id_pago=?
              LEFT JOIN PagoReportado pr ON pr.id_factura=f.id_factura AND pr.estado='REPORTADO'
              WHERE f.id_factura=? AND f.id_paciente=? AND f.estado_pago='PENDIENTE' AND pr.id_reporte IS NULL
            """, (data.get("id_pago"), data.get("id_factura"), paciente["id_paciente"])).fetchone()
            if not factura:
                return False
            tipo_pago = str(factura["tipo_pago"] or "").upper()
            if tipo_pago == "EFECTIVO":
                return False
            observacion = self._observacion_pago_paciente(data, tipo_pago)
            if not observacion:
                return False
            conn.execute("""
              INSERT INTO PagoReportado(id_factura, id_pago, monto, usuario_registro, observacion)
              VALUES(?,?,?,?,?)
            """, (
                factura["id_factura"],
                data.get("id_pago"),
                factura["total"],
                user["id_usuario"],
                observacion,
            ))
            self._audit(conn, "PagoReportado", "REPORTAR_PAGO_PACIENTE", user, datos_nuevos=f"{factura['numero_factura']} {tipo_pago} total {factura['total']}")
            return True

    def dashboard(self):
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        with get_connection() as conn:
            kpis = conn.execute("""
              SELECT
                COALESCE(SUM(CASE WHEN DATE(fecha_factura)=DATE('now') THEN total END),0) AS facturado_hoy,
                COALESCE(SUM(CASE WHEN strftime('%Y-%m', fecha_factura)=strftime('%Y-%m','now') THEN total END),0) AS facturado_mes,
                COALESCE(SUM(CASE WHEN estado_pago='PAGADO' THEN total END),0) AS cobrado,
                COALESCE(SUM(CASE WHEN estado_pago IN ('PENDIENTE','REPORTADO') THEN total END),0) AS pendiente,
                COUNT(*) AS facturas
              FROM Factura
              WHERE eliminado = 0
            """).fetchone()
            citas = conn.execute("""
              SELECT
                SUM(CASE WHEN e.nombre='ATENDIDA' THEN 1 ELSE 0 END) AS cobradas,
                SUM(CASE WHEN f.estado_pago IN ('PENDIENTE','REPORTADO') THEN 1 ELSE 0 END) AS pendientes_pago
              FROM Reservacion r
              JOIN Estado e ON e.id_estado = r.id_estado
              LEFT JOIN Factura f ON f.id_reserva = r.id_reserva
            """).fetchone()
            por_dia = conn.execute("""
              SELECT DATE(fecha_pago) AS fecha, SUM(monto) AS total
              FROM Pago
              WHERE DATE(fecha_pago) BETWEEN ? AND ?
              GROUP BY DATE(fecha_pago)
              ORDER BY DATE(fecha_pago)
            """, (week_start.isoformat(), week_end.isoformat())).fetchall()
            por_pago = conn.execute("""
              SELECT tp.nombre, COALESCE(SUM(p.monto),0) AS total
              FROM TipoPago tp
              LEFT JOIN Pago p ON p.id_pago = tp.id_pago
              GROUP BY tp.id_pago, tp.nombre
              ORDER BY tp.id_pago
            """).fetchall()
            recientes = conn.execute("""
              SELECT f.id_factura, f.numero_factura, p.nombres || ' ' || p.apellidos AS paciente,
                     f.total, f.estado_pago, DATE(f.fecha_factura) AS fecha
              FROM Factura f
              JOIN Paciente p ON p.id_paciente = f.id_paciente
              ORDER BY f.fecha_factura DESC
              LIMIT 6
            """).fetchall()
        return {
            "kpis": dict(kpis),
            "citas": dict(citas),
            "por_dia": self._weekly_income_rows(por_dia),
            "inicio_semana": week_start.isoformat(),
            "fin_semana": week_end.isoformat(),
            "por_pago": [dict(r) for r in por_pago],
            "recientes": [dict(r) for r in recientes],
        }

    def listar_pacientes(self, q=""):
        params = []
        where = "WHERE eliminado=0"
        if q:
            like = f"%{q.strip()}%"
            where += " AND (dni LIKE ? OR nombres LIKE ? OR apellidos LIKE ? OR telefono LIKE ?)"
            params = [like, like, like, like]
        with get_connection() as conn:
            rows = conn.execute(f"""
              SELECT *, nombres || ' ' || apellidos AS nombre_completo
              FROM Paciente {where}
              ORDER BY fecha_creacion DESC
            """, params).fetchall()
            return [dict(r) for r in rows]

    def crear_paciente(self, data, user):
        with get_connection() as conn:
            conn.execute("""
              INSERT INTO Paciente(dni, nombres, apellidos, genero, fecha_nacimiento, email, telefono,
                direccion, grupo_sanguineo, contacto_emergencia, telefono_emergencia, alergias,
                enfermedades_cronicas, observaciones)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                data.get("dni"), data.get("nombres"), data.get("apellidos"), data.get("genero", "M"),
                data.get("fecha_nacimiento"), data.get("email") or None, data.get("telefono"),
                data.get("direccion"), data.get("grupo_sanguineo"), data.get("contacto_emergencia"),
                data.get("telefono_emergencia"), data.get("alergias"), data.get("enfermedades_cronicas"),
                data.get("observaciones"),
            ))
            self._audit(conn, "Paciente", "CREAR", user, datos_nuevos=data.get("dni", ""))

    def catalogos_cita(self):
        with get_connection() as conn:
            return {
                "pacientes": [dict(r) for r in conn.execute("""
                  SELECT id_paciente, dni, nombres || ' ' || apellidos AS nombre
                  FROM Paciente
                  WHERE eliminado=0
                  ORDER BY apellidos, nombres
                """)],
                "medicos": [dict(r) for r in conn.execute("""
                  SELECT m.id_medico, m.nombres || ' ' || m.apellidos AS nombre, e.nombre AS especialidad, e.precio_base
                  FROM Medico m JOIN Especialidad e ON e.id_especialidad=m.id_especialidad
                  WHERE m.eliminado=0 ORDER BY e.nombre, m.apellidos
                """)],
                "pagos": self.tipos_pago(),
                "estados": [dict(r) for r in conn.execute("SELECT id_estado, nombre FROM Estado ORDER BY id_estado")],
            }

    def crear_cita(self, data, user):
        with get_connection() as conn:
            medico = conn.execute("""
              SELECT e.nombre AS especialidad, e.precio_base
              FROM Medico m JOIN Especialidad e ON e.id_especialidad=m.id_especialidad
              WHERE m.id_medico=?
            """, (data.get("id_medico"),)).fetchone()
            precio = float(data.get("precio") or medico["precio_base"])
            titulo = data.get("titulo") or f"Consulta {medico['especialidad']}"
            cur = conn.execute("""
              INSERT INTO Reservacion(titulo, nota, mensaje, fecha_cita, hora_cita, sintomas, observaciones,
                precio, id_paciente, id_usuario, id_medico, id_pago, id_estado)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                titulo, data.get("nota"), data.get("mensaje"), data.get("fecha_cita"), data.get("hora_cita"),
                data.get("sintomas"), data.get("observaciones"), precio, data.get("id_paciente"),
                user["id_usuario"], data.get("id_medico"), data.get("id_pago"), data.get("id_estado"),
            ))
            self._audit(conn, "Reservacion", "CREAR", user, datos_nuevos=f"Cita #{cur.lastrowid}")
            if data.get("generar_factura") == "on":
                self._generar_factura(conn, cur.lastrowid, user)

    def listar_citas(self):
        with get_connection() as conn:
            rows = conn.execute("""
              SELECT r.id_reserva, r.titulo, r.fecha_cita, r.hora_cita, r.precio,
                     p.nombres || ' ' || p.apellidos AS paciente,
                     m.nombres || ' ' || m.apellidos AS medico,
                     e.nombre AS estado, tp.nombre AS tipo_pago,
                     f.numero_factura
              FROM Reservacion r
              JOIN Paciente p ON p.id_paciente=r.id_paciente
              JOIN Medico m ON m.id_medico=r.id_medico
              JOIN Estado e ON e.id_estado=r.id_estado
              JOIN TipoPago tp ON tp.id_pago=r.id_pago
              LEFT JOIN Factura f ON f.id_reserva=r.id_reserva
              WHERE r.eliminado=0
              ORDER BY r.fecha_cita DESC, r.hora_cita DESC
            """).fetchall()
            return [dict(r) for r in rows]

    def generar_factura_desde_cita(self, id_reserva, user):
        with get_connection() as conn:
            exists = conn.execute("SELECT id_factura FROM Factura WHERE id_reserva=?", (id_reserva,)).fetchone()
            if not exists:
                self._generar_factura(conn, id_reserva, user)

    def listar_facturas(self):
        with get_connection() as conn:
            rows = conn.execute("""
              SELECT f.*, p.nombres || ' ' || p.apellidos AS paciente, r.titulo AS cita
              FROM Factura f
              JOIN Paciente p ON p.id_paciente=f.id_paciente
              LEFT JOIN Reservacion r ON r.id_reserva=f.id_reserva
              WHERE f.eliminado=0
              ORDER BY f.fecha_factura DESC
            """).fetchall()
            return [dict(r) for r in rows]

    def detalle_factura(self, id_factura):
        with get_connection() as conn:
            cab = conn.execute("""
              SELECT f.*, p.dni, p.nombres || ' ' || p.apellidos AS paciente, p.email
              FROM Factura f JOIN Paciente p ON p.id_paciente=f.id_paciente
              WHERE f.id_factura=?
            """, (id_factura,)).fetchone()
            if not cab:
                return None
            det = conn.execute("SELECT * FROM DetalleFactura WHERE id_factura=?", (id_factura,)).fetchall()
            return {"cabecera": dict(cab), "detalle": [dict(r) for r in det]}

    def facturas_pendientes(self):
        with get_connection() as conn:
            rows = conn.execute("""
              SELECT f.id_factura, f.numero_factura, f.total, f.fecha_factura,
                     p.nombres || ' ' || p.apellidos AS paciente,
                     COALESCE(m.nombres || ' ' || m.apellidos, 'Sin medico') AS medico,
                     COALESCE(pr.id_pago, r.id_pago) AS id_pago_pactado,
                     COALESCE(tpr.nombre, tp.nombre, 'Sin metodo pactado') AS metodo_pago,
                     CASE WHEN pr.id_reporte IS NOT NULL THEN 'REPORTADO' ELSE f.estado_pago END AS estado_pago,
                     pr.observacion AS pago_reportado
              FROM Factura f
              JOIN Paciente p ON p.id_paciente=f.id_paciente
              LEFT JOIN Reservacion r ON r.id_reserva=f.id_reserva
              LEFT JOIN Medico m ON m.id_medico=r.id_medico
              LEFT JOIN TipoPago tp ON tp.id_pago=r.id_pago
              LEFT JOIN PagoReportado pr ON pr.id_factura=f.id_factura AND pr.estado='REPORTADO'
              LEFT JOIN TipoPago tpr ON tpr.id_pago=pr.id_pago
              WHERE f.estado_pago='PENDIENTE'
              ORDER BY f.fecha_factura DESC
            """).fetchall()
            return [dict(r) for r in rows]

    def anular_factura(self, data, user):
        with get_connection() as conn:
            factura = conn.execute("SELECT numero_factura, estado_pago FROM Factura WHERE id_factura=?", (data.get("id_factura"),)).fetchone()
            conn.execute("UPDATE Factura SET estado_pago='ANULADO', motivo_anulacion=? WHERE id_factura=?", (data.get("motivo"), data.get("id_factura")))
            self._audit(conn, "Factura", "ANULAR", user, datos_anteriores=factura["estado_pago"], datos_nuevos=data.get("motivo"))

    def tipos_pago(self):
        with get_connection() as conn:
            return [dict(r) for r in conn.execute("SELECT id_pago, nombre FROM TipoPago ORDER BY id_pago")]

    def facturas_para_pago(self):
        return self.facturas_pendientes()

    def registrar_pago(self, data, user):
        with get_connection() as conn:
            factura = conn.execute("""
              SELECT f.total, f.estado_pago, r.id_pago AS id_pago_pactado
              FROM Factura f
              LEFT JOIN Reservacion r ON r.id_reserva=f.id_reserva
              WHERE f.id_factura=? AND f.estado_pago='PENDIENTE'
            """, (data.get("id_factura"),)).fetchone()
            if not factura:
                return
            monto = float(data.get("monto") or factura["total"])
            id_pago = data.get("id_pago") or factura["id_pago_pactado"]
            conn.execute("""
              INSERT INTO Pago(id_factura, id_pago, monto, usuario_registro, observacion)
              VALUES(?,?,?,?,?)
            """, (data.get("id_factura"), id_pago, monto, user["id_usuario"], data.get("observacion")))
            conn.execute("UPDATE Factura SET estado_pago='PAGADO' WHERE id_factura=?", (data.get("id_factura"),))
            conn.execute("UPDATE PagoReportado SET estado='VALIDADO' WHERE id_factura=? AND estado='REPORTADO'", (data.get("id_factura"),))
            self._audit(conn, "Pago", "REGISTRAR", user, datos_nuevos=f"Factura {data.get('id_factura')} monto {monto}")

    def caja_diaria(self):
        with get_connection() as conn:
            rows = conn.execute("""
              SELECT tp.nombre, COALESCE(SUM(p.monto),0) AS total
              FROM TipoPago tp
              LEFT JOIN Pago p ON p.id_pago=tp.id_pago AND DATE(p.fecha_pago)=DATE('now')
              GROUP BY tp.id_pago, tp.nombre
            """).fetchall()
            movimientos = conn.execute("""
              SELECT p.fecha_pago, f.numero_factura, tp.nombre AS tipo_pago, p.monto, u.username
              FROM Pago p
              JOIN Factura f ON f.id_factura=p.id_factura
              JOIN TipoPago tp ON tp.id_pago=p.id_pago
              JOIN Usuario u ON u.id_usuario=p.usuario_registro
              WHERE DATE(p.fecha_pago)=DATE('now')
              ORDER BY p.fecha_pago DESC
            """).fetchall()
        totals = [dict(r) for r in rows]
        return {"totales": totals, "total": sum(float(r["total"]) for r in totals), "movimientos": [dict(r) for r in movimientos]}

    def reportes_financieros(self):
        with get_connection() as conn:
            diario = conn.execute("""
              SELECT DATE(fecha_factura) AS periodo, COUNT(*) AS facturas, SUM(total) AS total,
                     SUM(CASE WHEN estado_pago='PAGADO' THEN total ELSE 0 END) AS cobrado,
                     SUM(CASE WHEN estado_pago IN ('PENDIENTE','REPORTADO') THEN total ELSE 0 END) AS pendiente
              FROM Factura GROUP BY DATE(fecha_factura) ORDER BY periodo DESC
            """).fetchall()
            medico = conn.execute("""
              SELECT m.nombres || ' ' || m.apellidos AS medico, COUNT(f.id_factura) AS consultas, COALESCE(SUM(f.total),0) AS facturado
              FROM Medico m
              LEFT JOIN Reservacion r ON r.id_medico=m.id_medico
              LEFT JOIN Factura f ON f.id_reserva=r.id_reserva AND f.estado_pago <> 'ANULADO'
              GROUP BY m.id_medico ORDER BY facturado DESC
            """).fetchall()
            especialidad = conn.execute("""
              SELECT e.nombre AS especialidad, COALESCE(SUM(f.total),0) AS ingresos
              FROM Especialidad e
              LEFT JOIN Medico m ON m.id_especialidad=e.id_especialidad
              LEFT JOIN Reservacion r ON r.id_medico=m.id_medico
              LEFT JOIN Factura f ON f.id_reserva=r.id_reserva AND f.estado_pago <> 'ANULADO'
              GROUP BY e.id_especialidad ORDER BY ingresos DESC
            """).fetchall()
            pago = conn.execute("""
              SELECT tp.nombre AS tipo_pago, COALESCE(SUM(p.monto),0) AS ingresos
              FROM TipoPago tp LEFT JOIN Pago p ON p.id_pago=tp.id_pago
              GROUP BY tp.id_pago
            """).fetchall()
        return {
            "diario": [dict(r) for r in diario],
            "medico": [dict(r) for r in medico],
            "especialidad": [dict(r) for r in especialidad],
            "pago": [dict(r) for r in pago],
        }

    def exportar_reporte_csv(self):
        data = self.reportes_financieros()["diario"]
        out = io.StringIO()
        writer = csv.DictWriter(out, fieldnames=["periodo", "facturas", "total", "cobrado", "pendiente"])
        writer.writeheader()
        writer.writerows(data)
        return out.getvalue()

    def auditoria(self):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM Auditoria ORDER BY fecha DESC LIMIT 80").fetchall()
            return [dict(r) for r in rows]

    def usuarios(self, rol=""):
        params = []
        where = "WHERE u.eliminado=0 AND r.nombre IN ('ADMINISTRADOR', 'CAJA', 'RECEPCION')"
        if rol:
            where += " AND r.nombre=?"
            params.append(rol)
        with get_connection() as conn:
            rows = conn.execute(f"""
              SELECT u.username, u.nombres || ' ' || u.apellidos AS nombre, u.email, r.nombre AS rol, u.estado_activo
              FROM Usuario u JOIN Rol r ON r.id_rol=u.id_rol
              {where}
              ORDER BY r.nombre, u.username
            """, params).fetchall()
            return [dict(r) for r in rows]

    def pacientes_para_usuario(self):
        with get_connection() as conn:
            rows = conn.execute("""
              SELECT p.id_paciente, p.dni, p.nombres || ' ' || p.apellidos AS nombre,
                     p.email, u.username
              FROM Paciente p
              LEFT JOIN Usuario u ON LOWER(u.email)=LOWER(p.email) AND u.eliminado=0
              WHERE p.eliminado=0
              ORDER BY p.apellidos, p.nombres
            """).fetchall()
            return [dict(r) for r in rows]

    def crear_usuario(self, data, user):
        rol = data.get("rol")
        if rol not in {"CAJA", "RECEPCION"}:
            return
        with get_connection() as conn:
            rol_row = conn.execute("SELECT id_rol FROM Rol WHERE nombre=?", (rol,)).fetchone()
            if not rol_row:
                return
            exists = conn.execute("""
              SELECT id_usuario FROM Usuario
              WHERE LOWER(username)=LOWER(?) OR LOWER(email)=LOWER(?)
            """, (data.get("username", "").strip(), data.get("email", "").strip())).fetchone()
            if exists:
                return
            conn.execute("""
              INSERT INTO Usuario(username, nombres, apellidos, email, password_hash, telefono, direccion, id_rol)
              VALUES(?,?,?,?,?,?,?,?)
            """, (
                data.get("username", "").strip(),
                data.get("nombres", "").strip(),
                data.get("apellidos", "").strip(),
                data.get("email", "").strip(),
                self._hash(data.get("password", "")),
                data.get("telefono", "").strip(),
                data.get("direccion", "").strip(),
                rol_row["id_rol"],
            ))
            self._audit(conn, "Usuario", "CREAR", user, datos_nuevos=f"{data.get('username')} / {rol}")

    def crear_usuario_paciente(self, data, user):
        with get_connection() as conn:
            paciente = conn.execute("""
              SELECT id_paciente, dni, nombres, apellidos, email, telefono, direccion
              FROM Paciente
              WHERE id_paciente=? AND eliminado=0
            """, (data.get("id_paciente"),)).fetchone()
            if not paciente or not paciente["email"]:
                return
            rol = conn.execute("SELECT id_rol FROM Rol WHERE nombre='PACIENTE'").fetchone()
            if not rol:
                return
            username = (data.get("username") or paciente["dni"] or "").strip()
            password = (data.get("password") or paciente["dni"] or "Paciente123!").strip()
            exists = conn.execute("""
              SELECT id_usuario FROM Usuario
              WHERE LOWER(username)=LOWER(?) OR LOWER(email)=LOWER(?)
            """, (username, paciente["email"])).fetchone()
            if exists:
                return
            conn.execute("""
              INSERT INTO Usuario(username, nombres, apellidos, email, password_hash, telefono, direccion, id_rol)
              VALUES(?,?,?,?,?,?,?,?)
            """, (
                username,
                paciente["nombres"],
                paciente["apellidos"],
                paciente["email"],
                self._hash(password),
                paciente["telefono"],
                paciente["direccion"],
                rol["id_rol"],
            ))
            self._audit(conn, "Usuario", "CREAR_PACIENTE", user, datos_nuevos=f"{username} / PACIENTE")

    def _weekly_income_rows(self, rows):
        totals = {}
        for row in rows:
            raw_date = row["fecha"]
            parsed = raw_date if hasattr(raw_date, "weekday") else date.fromisoformat(str(raw_date)[:10])
            totals[str((parsed.weekday() + 1) % 7)] = float(row["total"] or 0)
        return [{"dia": day, "total": total} for day, total in totals.items()]

    def _paciente_de_usuario(self, user):
        if user.get("id_paciente"):
            sql = "SELECT *, nombres || ' ' || apellidos AS nombre_completo FROM Paciente WHERE id_paciente=? AND eliminado=0"
            params = (user["id_paciente"],)
        else:
            sql = "SELECT *, nombres || ' ' || apellidos AS nombre_completo FROM Paciente WHERE LOWER(email)=LOWER(?) AND eliminado=0"
            params = (user.get("email", ""),)
        with get_connection() as conn:
            row = conn.execute(sql, params).fetchone()
            return dict(row) if row else None

    def _generar_factura(self, conn, id_reserva, user):
        reserva = conn.execute("""
          SELECT r.*, p.id_paciente, m.nombres || ' ' || m.apellidos AS medico
          FROM Reservacion r
          JOIN Paciente p ON p.id_paciente=r.id_paciente
          JOIN Medico m ON m.id_medico=r.id_medico
          WHERE r.id_reserva=?
        """, (id_reserva,)).fetchone()
        if not reserva:
            return
        numero = self._next_invoice_number(conn)
        subtotal = float(reserva["precio"])
        igv = round(subtotal * 0.18, 2)
        total = round(subtotal + igv, 2)
        cur = conn.execute("""
          INSERT INTO Factura(numero_factura, id_paciente, id_reserva, subtotal, igv, total, estado_pago)
          VALUES(?,?,?,?,?,?, 'PENDIENTE')
        """, (numero, reserva["id_paciente"], id_reserva, subtotal, igv, total))
        conn.execute("""
          INSERT INTO DetalleFactura(id_factura, descripcion, cantidad, precio_unitario, subtotal)
          VALUES(?,?,?,?,?)
        """, (cur.lastrowid, reserva["titulo"], 1, subtotal, subtotal))
        self._audit(conn, "Factura", "CREAR", user, datos_nuevos=f"{numero} total {total}")

    def _next_invoice_number(self, conn):
        year = date.today().year
        prefix = f"FAC-{year}-"
        row = conn.execute("SELECT COUNT(*) AS total FROM Factura WHERE numero_factura LIKE ?", (prefix + "%",)).fetchone()
        return f"{prefix}{int(row['total']) + 1:06d}"

    def _audit(self, conn, table, action, user, datos_anteriores=None, datos_nuevos=None):
        conn.execute("""
          INSERT INTO Auditoria(tabla, accion, usuario_bd, datos_anteriores, datos_nuevos)
          VALUES(?,?,?,?,?)
        """, (table, action, user["username"], datos_anteriores, str(datos_nuevos or "")))

    def _hash(self, value):
        return hashlib.sha1(value.encode("utf-8")).hexdigest()

    def _observacion_pago_paciente(self, data, tipo_pago):
        if tipo_pago == "TARJETA":
            card_number = "".join(ch for ch in str(data.get("card_number", "")) if ch.isdigit())
            card_holder = str(data.get("card_holder", "")).strip()
            card_expiry = str(data.get("card_expiry", "")).strip()
            card_cvv = str(data.get("card_cvv", "")).strip()
            if len(card_number) < 12 or len(card_cvv) < 3 or not card_holder or not card_expiry:
                return ""
            return f"Pago simulado con tarjeta terminada en {card_number[-4:]}"
        if tipo_pago in {"YAPE", "PLIN", "TRANSFERENCIA"}:
            operation_code = str(data.get("operation_code", "")).strip()
            payer_phone = str(data.get("payer_phone", "")).strip()
            if len(operation_code) < 4:
                return ""
            phone_note = f" telefono {payer_phone}" if payer_phone else ""
            return f"Pago simulado {tipo_pago} operacion {operation_code}{phone_note}"
        return ""
