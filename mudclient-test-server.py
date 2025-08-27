#!/usr/bin/env python3
import socket
import threading
import os
import time

HOST = "0.0.0.0"
PORT = 5050

ANSI_TEST = """
\033[1m bold \033[0m normal
\033[1m bold \033[m normal

\033[0;31mnormal red      \033[1;31mbold red
\033[0;32mnormal green    \033[1;32mbold green
\033[0;33mnormal yellow   \033[1;33mbold yellow
\033[0;34mnormal blue     \033[1;34mbold blue
\033[0;35mnormal magneta  \033[1;35mbold magenta
\033[0;36mnormal cyan     \033[1;36mbold cyan
\033[0;37mnormal white    \033[1;37mbold white

\033[m normal

\033[3m italics\033[m    \033[4munderlined\033[m
\033[5m blinking\033[m   \033[7minverse\033[m
\033[8m hidden\033[m     \033[9mstrikethrough\033[m
\033[20m fraktur\033[m   \033[21mdouble underline\033[m and \033[53moverline\033[m

""".encode()

UTF8_TEST = open("utf8-test.txt", "rb").read()

def send(data):
        data = data.replace(b"\n", b"\r\n")
        return lambda sock: sendall(sock, data)

def slowsend(data):
        data = data.replace(b"\n", b"\r\n")
        def fn(sock):
                view = memoryview(data)
                while view:
                        n = sock.send(view[0:12])
                        view = view[n:]
                        time.sleep(0.1)
        return fn


OPTIONS = {
    "ansi": send(ANSI_TEST),
    "ansi_slow": slowsend(ANSI_TEST),
    "utf": send(UTF8_TEST),
    "utf_slow": slowsend(UTF8_TEST),
}

MENU = (
    "Welcome to The Mud Client Test Server\n"
    "How would you like to torture your mud client?\n"
    "Options are: " + ", ".join(OPTIONS) + "\n"
).encode()


def sendall(sock: socket.socket, data: bytes):
    view = memoryview(data)
    while view:
        n = sock.send(view)
        view = view[n:]


def handle_client(conn: socket.socket, addr):
    try:
        sendall(conn, MENU)

        conn.settimeout(60)
        data = b""
        while b"\n" not in data and len(data) < 4096:
            chunk = conn.recv(1024)
            if not chunk:
                break
            data += chunk

        option = data.decode(errors="ignore").strip().split()[0] if data else ""
        optionhandler = OPTIONS.get(option)

        if not optionhandler:
            return

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
