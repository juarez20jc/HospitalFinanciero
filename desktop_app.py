import os
import traceback
import threading
import webbrowser


def main():
    from main import create_server, print_startup

    server, host, port = create_server()
    url = f"http://{host}:{port}"
    print_startup(host, port)

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        import webview
    except ImportError:
        print("Falta pywebview. Ejecuta: pip install -r requirements.txt")
        print(f"Abriendo temporalmente en el navegador: {url}")
        webbrowser.open(url)
        thread.join()
        return

    try:
        webview.create_window(
            "Clinica Ana San Gabriel",
            url,
            width=1366,
            height=820,
            min_size=(1100, 700),
        )
        webview.start(gui="edgechromium")
    except Exception:
        error = traceback.format_exc()
        log_path = os.path.join(os.path.dirname(__file__), "desktop_error.log")
        with open(log_path, "w", encoding="utf-8") as file:
            file.write(error)
        print("No se pudo abrir la ventana de escritorio.")
        print(f"Detalle guardado en: {log_path}")
        print(f"Abriendo temporalmente en el navegador: {url}")
        webbrowser.open(url)
        thread.join()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
