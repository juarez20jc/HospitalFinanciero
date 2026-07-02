import threading
import webbrowser

from main import create_server, print_startup


def main():
    server, host, port = create_server()
    url = f"http://{host}:{port}"
    print_startup(host, port)
    print(f"Abriendo en el navegador: {url}")

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    webbrowser.open(url)

    try:
        thread.join()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
