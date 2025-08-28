#!/usr/bin/env python3
import socket
import threading
import os
import time
import zlib
import struct
import datetime

from baudtest import baudtest_handler

from mudsocket import sendall
from menu import HELLO, OPTIONS, MENU

HOST = "0.0.0.0"
PORT = 5050

def handle_client(conn: socket.socket, addr):
    sendall(conn, HELLO)

    try:
        while True:
            sendall(conn, MENU)

            conn.settimeout(60)
            data = b""
            while b"\n" not in data and len(data) < 4096:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                data += chunk

            decoded = data.decode(errors="ignore").strip() if data else ""
            option = decoded.split()[0] if decoded.split() else ""
            optionhandler = OPTIONS.get(option)

            if not optionhandler:
                if option:  # Only show error if they actually typed something
                    sendall(conn, f"Unknown option: {option}\r\n".encode())
                continue  # Go back to menu instead of returning

            optionhandler(conn)

    finally:
        conn.close()

def main():
    print(f"Serving on {HOST}:{PORT} (Ctrl+C to stop)")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(5)
        while True:
            conn, addr = srv.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down.")
