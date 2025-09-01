#!/usr/bin/env python3
import socket
import threading
import os
import time
import zlib
import struct
import datetime

from tests import OPTIONS, CATEGORIES

from menu import HELLO, MENU

from telnet import TelnetState

HOST = "0.0.0.0"
PORT = 5050

def handle_client(conn: socket.socket, addr):
    telnet = TelnetState(conn)

    telnet.send_text(HELLO)

    category = None

    try:
        while True:
            telnet.reset()
            
            if category is None:            
                telnet.send_text(MENU)
            else:
                for key, item in category.items():
                    telnet.send_text(f"  {key:15} - {item[0]}\n")

            decoded = telnet.readline()

            option = decoded.split()[0] if decoded.split() else ""
            
            if new_cat := CATEGORIES.get(option):
                telnet.send_text("Choose a specific test, or another category.\n")
                category = new_cat
                continue
            
            optionhandler = OPTIONS.get(option)

            if not optionhandler:
                if option:  # Only show error if they actually typed something
                    telnet.send_text(f"Unknown option: {option}\n".encode())
                    continue

            optionhandler[1](telnet)

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
