from http.server import HTTPServer, BaseHTTPRequestHandler
from http import cookies
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import json
import mimetypes
import secrets
import socket

from controllers.dashboard_controller import DashboardController
from controllers.factura_controller import FacturaController
from controllers.paciente_controller import PacienteController
from controllers.pago_controller import PagoController
from controllers.reporte_controller import ReporteController
from database.conexion import current_database_label, initialize_database
from database.consultas import Repository
from views.templates import (
    admin_login_view,
    caja_view,
    citas_view,
    cuentas_view,
    dashboard_view,
    facturas_view,
    login_view,
    paciente_citas_view,
    paciente_dashboard_view,
    paciente_facturas_view,
    paciente_perfil_view,
    pacientes_view,
    pagos_view,
    reportes_view,
    auditoria_view,
    usuarios_paciente_view,
    usuarios_view,
)


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "assets"
SESSIONS = {}


def portal_payment_notice(code):
    messages = {
        "ok": "Pago reportado correctamente. Caja debe validarlo antes de marcar la factura como pagada.",
        "error": "No se registro el pago. Revisa el metodo y los datos; efectivo solo se confirma en caja.",
    }
    return messages.get(code, "")


class HospitalHandler(BaseHTTPRequestHandler):
    repo = Repository()
    dashboard = DashboardController(repo)
    pacientes = PacienteController(repo)
    facturas = FacturaController(repo)
    pagos = PagoController(repo)
    reportes = ReporteController(repo)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path.startswith("/assets/"):
            self.serve_static(path)
            return

        if path == "/":
            self.html(login_view(error=query.get("error", [""])[0]))
            return
        if path == "/admin":
            self.html(admin_login_view(error=query.get("error", [""])[0]))
            return
        if path == "/logout":
            self.logout()
            return

        user = self.current_user()
        if not user:
            self.redirect("/")
            return

        if path == "/dashboard":
            if user["rol"] == "PACIENTE":
                self.html(paciente_dashboard_view(user, self.repo.paciente_portal(user), self.repo.tipos_pago()))
            else:
                self.html(dashboard_view(user, self.dashboard.summary()))
        elif path == "/portal/facturas":
            self.require_any(user, {"PACIENTE"})
            notice = portal_payment_notice(query.get("pago", [""])[0])
            self.html(paciente_facturas_view(user, self.repo.paciente_portal(user), self.repo.tipos_pago(), notice=notice))
        elif path == "/portal/factura":
            self.require_any(user, {"PACIENTE"})
            invoice_id = int(query.get("id", ["0"])[0] or "0")
            invoice = self.repo.detalle_factura_paciente(invoice_id, user)
            notice = portal_payment_notice(query.get("pago", [""])[0])
            self.html(paciente_facturas_view(user, self.repo.paciente_portal(user), self.repo.tipos_pago(), detalle=invoice, notice=notice))
        elif path == "/portal/citas":
            self.require_any(user, {"PACIENTE"})
            self.html(paciente_citas_view(user, self.repo.paciente_portal(user)))
        elif path == "/portal/perfil":
            self.require_any(user, {"PACIENTE"})
            self.html(paciente_perfil_view(user, self.repo.paciente_portal(user)))
        elif path == "/pacientes/nuevo":
            self.redirect("/pacientes")
            return
        elif path == "/pacientes":
            self.require_any(user, {"ADMINISTRADOR", "RECEPCION", "CAJA"})
            self.html(pacientes_view(user, self.pacientes.listar(query.get("q", [""])[0]), path))
        elif path == "/citas":
            self.require_any(user, {"ADMINISTRADOR", "RECEPCION"})
            self.html(citas_view(user, self.repo.catalogos_cita(), self.repo.listar_citas()))
        elif path == "/facturas":
            self.require_any(user, {"ADMINISTRADOR", "RECEPCION", "CAJA"})
            self.html(facturas_view(user, self.facturas.listar()))
        elif path == "/factura":
            self.require_any(user, {"ADMINISTRADOR", "RECEPCION", "CAJA"})
            invoice_id = int(query.get("id", ["0"])[0] or "0")
            invoice = self.facturas.detalle(invoice_id)
            if not invoice:
                self.redirect("/facturas")
                return
            self.html(facturas_view(user, self.facturas.listar(), detalle=invoice))
        elif path == "/pagos":
            self.require_any(user, {"ADMINISTRADOR", "CAJA"})
            self.html(pagos_view(user, self.pagos.listar_pendientes(), self.repo.tipos_pago()))
        elif path == "/caja":
            self.require_any(user, {"ADMINISTRADOR", "CAJA"})
            self.html(caja_view(user, self.pagos.caja_diaria()))
        elif path == "/cuentas":
            self.require_any(user, {"ADMINISTRADOR", "CAJA", "RECEPCION"})
            self.html(cuentas_view(user, self.facturas.pendientes()))
        elif path == "/reportes":
            self.require_any(user, {"ADMINISTRADOR", "CAJA"})
            self.html(reportes_view(user, self.reportes.financieros()))
        elif path == "/reportes/exportar":
            self.require_any(user, {"ADMINISTRADOR", "CAJA"})
            self.csv("reporte_financiero.csv", self.reportes.exportar_csv())
        elif path == "/auditoria":
            self.require_any(user, {"ADMINISTRADOR"})
            self.html(auditoria_view(user, self.repo.auditoria()))
        elif path == "/usuarios":
            self.require_any(user, {"ADMINISTRADOR"})
            rol = query.get("rol", [""])[0]
            roles_validos = {"ADMINISTRADOR", "CAJA", "RECEPCION"}
            rol = rol if rol in roles_validos else ""
            self.html(usuarios_view(user, self.repo.usuarios(rol), rol))
        elif path == "/usuarios/paciente":
            self.require_any(user, {"ADMINISTRADOR", "RECEPCION"})
            self.html(usuarios_paciente_view(user, self.repo.pacientes_para_usuario()))
        elif path == "/configuracion":
            self.require_any(user, {"ADMINISTRADOR"})
            self.redirect("/dashboard")
        else:
            self.send_error(404)

    def do_POST(self):
        parsed = urlparse(self.path)
        form = self.form_data()

        if parsed.path in {"/login", "/login/admin"}:
            self.login(form, admin_mode=parsed.path.endswith("/admin"))
            return

        user = self.current_user()
        if not user:
            self.redirect("/")
            return

        if parsed.path == "/pacientes/crear":
            self.require_any(user, {"ADMINISTRADOR", "RECEPCION"})
            self.pacientes.crear(form, user)
            self.redirect("/pacientes")
        elif parsed.path == "/usuarios/crear":
            self.require_any(user, {"ADMINISTRADOR"})
            self.repo.crear_usuario(form, user)
            self.redirect("/usuarios")
        elif parsed.path == "/usuarios/paciente/crear":
            self.require_any(user, {"ADMINISTRADOR", "RECEPCION"})
            self.repo.crear_usuario_paciente(form, user)
            self.redirect("/usuarios/paciente")
        elif parsed.path == "/citas/crear":
            self.require_any(user, {"ADMINISTRADOR", "RECEPCION"})
            self.repo.crear_cita(form, user)
            self.redirect("/citas")
        elif parsed.path == "/facturas/generar":
            self.require_any(user, {"ADMINISTRADOR", "RECEPCION", "CAJA"})
            self.facturas.generar_desde_cita(int(form.get("id_reserva", "0")), user)
            self.redirect("/facturas")
        elif parsed.path == "/pagos/registrar":
            self.require_any(user, {"ADMINISTRADOR", "CAJA"})
            self.pagos.registrar(form, user)
            self.redirect("/pagos")
        elif parsed.path == "/facturas/anular":
            self.require_any(user, {"ADMINISTRADOR", "CAJA"})
            self.facturas.anular(form, user)
            self.redirect("/facturas")
        elif parsed.path == "/portal/pagar":
            self.require_any(user, {"PACIENTE"})
            status = "ok" if self.repo.registrar_pago_paciente(form, user) else "error"
            self.redirect(f"/portal/facturas?pago={status}")
        else:
            self.send_error(404)

    def form_data(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8")
        return {k: v[0] for k, v in parse_qs(raw).items()}

    def login(self, form, admin_mode=False):
        user = self.repo.validar_usuario(form.get("username", ""), form.get("password", ""))
        if not user:
            self.redirect(("/admin" if admin_mode else "/") + "?error=Credenciales incorrectas")
            return
        if admin_mode and user["rol"] != "ADMINISTRADOR":
            self.redirect("/admin?error=Este ingreso es solo para administradores")
            return
        token = secrets.token_urlsafe(32)
        SESSIONS[token] = user
        self.send_response(302)
        cookie = cookies.SimpleCookie()
        cookie["hospital_session"] = token
        cookie["hospital_session"]["path"] = "/"
        cookie["hospital_session"]["httponly"] = True
        self.send_header("Set-Cookie", cookie.output(header="", sep=""))
        self.send_header("Location", "/dashboard")
        self.end_headers()

    def logout(self):
        token = self.session_token()
        if token in SESSIONS:
            del SESSIONS[token]
        self.send_response(302)
        self.send_header("Set-Cookie", "hospital_session=; Path=/; Max-Age=0; HttpOnly")
        self.send_header("Location", "/")
        self.end_headers()

    def current_user(self):
        token = self.session_token()
        return SESSIONS.get(token)

    def session_token(self):
        if "Cookie" not in self.headers:
            return None
        jar = cookies.SimpleCookie(self.headers.get("Cookie"))
        morsel = jar.get("hospital_session")
        return morsel.value if morsel else None

    def require_any(self, user, roles):
        if user["rol"] not in roles:
            self.send_error(403, "No tienes permisos para este modulo")
            raise PermissionError

    def html(self, body, status=200):
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def csv(self, filename, content):
        payload = content.encode("utf-8-sig")
        self.send_response(200)
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def redirect(self, location):
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def serve_static(self, request_path):
        rel = request_path.removeprefix("/assets/").replace("/", "\\")
        target = (STATIC_DIR / rel).resolve()
        if not str(target).startswith(str(STATIC_DIR.resolve())) or not target.exists():
            self.send_error(404)
            return
        data = target.read_bytes()
        mime = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        return


def main():
    server, host, port = create_server()
    print_startup(host, port)
    server.serve_forever()


def create_server():
    initialize_database()
    host = "127.0.0.1"
    port = available_port(host, 8000)
    server = HTTPServer((host, port), HospitalHandler)
    return server, host, port


def print_startup(host, port):
    print(json.dumps({
        "app": "Clinica Ana San Gabriel",
        "url": f"http://{host}:{port}",
        "database": current_database_label(),
        "usuario_demo": "recepcion / Recepcion123!",
        "admin_demo": "admin / Admin123!"
    }, ensure_ascii=False, indent=2))


def available_port(host, start):
    for port in range(start, start + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((host, port)) != 0:
                return port
    return start


if __name__ == "__main__":
    main()
