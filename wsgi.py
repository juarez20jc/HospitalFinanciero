"""
WSGI entry point for PythonAnywhere.
Bridges WSGI requests to the existing HospitalHandler (BaseHTTPRequestHandler)
by constructing raw HTTP requests and capturing the response.
"""
import io
import os
import sys
from pathlib import Path
from wsgiref import util

_project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(_project_dir))

from main import HospitalHandler, initialize_database, BASE_DIR, SESSIONS

initialize_database()


def _build_raw_request(environ):
    method = environ["REQUEST_METHOD"]
    path = environ.get("PATH_INFO", "/")
    qs = environ.get("QUERY_STRING", "")
    full_path = f"{path}?{qs}" if qs else path
    host = environ.get("HTTP_HOST", environ.get("SERVER_NAME", "localhost"))
    scheme = environ.get("wsgi.url_scheme", "http")

    lines = [f"{method} {full_path} HTTP/1.1"]
    lines.append(f"Host: {host}")

    for key, value in environ.items():
        if key.startswith("HTTP_"):
            header = key[5:].replace("_", "-").title()
            lines.append(f"{header}: {value}")

    ct = environ.get("CONTENT_TYPE", "")
    if ct:
        lines.append(f"Content-Type: {ct}")

    cl = environ.get("CONTENT_LENGTH", "0")
    body = b""
    if cl and cl != "0":
        body = environ["wsgi.input"].read(int(cl))
        lines.append(f"Content-Length: {cl}")

    raw = "\r\n".join(lines).encode("utf-8") + b"\r\n\r\n" + body
    return raw


def _parse_wfile(wfile):
    data = wfile.getvalue()
    header_end = data.find(b"\r\n\r\n")
    if header_end == -1:
        return "500 Internal Server Error", [], [b"Internal server error"]

    header_section = data[:header_end].decode("utf-8", errors="replace")
    body = data[header_end + 4:]

    parts = header_section.split("\r\n")
    status_line = parts[0]
    status = status_line.split(" ", 1)[1] if " " in status_line else "200 OK"

    headers = []
    for line in parts[1:]:
        if ":" in line:
            name, value = line.split(":", 1)
            headers.append((name.strip(), value.strip()))

    return status, headers, [body]


class _MockSocket:
    def __init__(self, raw_request):
        if isinstance(raw_request, str):
            raw_request = raw_request.encode("utf-8")
        self._rfile = io.BytesIO(raw_request)
        self._wfile = io.BytesIO()

    def makefile(self, mode, *args, **kwargs):
        return self._rfile if "r" in mode else self._wfile

    def close(self):
        pass


class _WSGIApp:
    def __call__(self, environ, start_response):
        try:
            raw = _build_raw_request(environ)
            sock = _MockSocket(raw)
            HospitalHandler(sock, ("127.0.0.1", 8000), None)
            status, headers, body = _parse_wfile(sock._wfile)
            start_response(status, headers)
            return body
        except Exception as exc:
            start_response("500 Internal Server Error", [("Content-Type", "text/plain; charset=utf-8")])
            return [f"Error: {exc}".encode("utf-8")]


application = _WSGIApp()
