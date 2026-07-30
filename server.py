"""Inicializador para Windows, Linux e Railway."""

from __future__ import annotations

import os
import threading
import webbrowser

from waitress import serve

from app import app


def open_local_browser(port: int):
    webbrowser.open(f"http://127.0.0.1:{port}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    is_cloud = bool(os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("RENDER"))
    if not is_cloud:
        threading.Timer(1.2, open_local_browser, args=(port,)).start()
        print(f"\nGramática em Análise: http://127.0.0.1:{port}")
        print("Para encerrar, pressione Ctrl+C.\n")
    host = "0.0.0.0" if is_cloud else "127.0.0.1"
    serve(app, host=host, port=port, threads=6)
