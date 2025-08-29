#!/usr/bin/env python3
import socket
import threading
import os
import time
import zlib
import struct
import datetime

from baudtest import baudtest_handler

from menu import HELLO, OPTIONS, MENU

from telnet import TelnetState

HOST = "0.0.0.0"
PORT = 5050

def handle_client(conn: socket.socket, addr):
    telnet = TelnetState(conn)

    telnet.sendall(HELLO)

    try:
        while True:
            telnet.reset()
            telnet.sendall(MENU)

            decoded = telnet.readline()

            option = decoded.split()[0] if decoded.split() else ""
            optionhandler = OPTIONS.get(option)

            if not optionhandler:
                if option:  # Only show error if they actually typed something
                    telnet.sendall(f"Unknown option: {option}\r\n".encode())
                    continue

            optionhandler(telnet)

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
