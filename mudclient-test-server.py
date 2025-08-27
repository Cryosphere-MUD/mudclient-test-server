#!/usr/bin/env python3
import socket
import threading
import os
import time
import zlib

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

IAC = bytes([255])
WILL = bytes([251])
TELOPT_MCCP2 = bytes([86])
SE = bytes([240])
SB = bytes([250])

MCCP2_TEST = (b"""1. Note that this test is a unilateral negotiation, i.e the server\r\n2. does not wait for the response before starting encryption.\r\n""" + IAC + WILL + TELOPT_MCCP2 + IAC + SB + TELOPT_MCCP2 + IAC + SE + 
  zlib.compress(b"3. This data's been compressed! Now we're going to finish the compression and carry on.\r\n4. The next line should be line 5.\r\n") +
b"5. This is line five.\r\n")

def send(data, newline_replace = False):
    if newline_replace:
        data = data.replace(b"\n", b"\r\n")
    return lambda sock: sendall(sock, data)

def slowsend(data, newline_replace = False):
    if newline_replace:
        data = data.replace(b"\n", b"\r\n")
    def fn(sock):
            view = memoryview(data)
            while view:
                    n = sock.send(view[0:15])
                    view = view[n:]
                    time.sleep(0.1)
    return fn


OPTIONS = {
    "ansi": send(ANSI_TEST),
    "ansi_slow": slowsend(ANSI_TEST),
    "utf": send(UTF8_TEST),
    "utf_slow": slowsend(UTF8_TEST),
    "mccp2": send(MCCP2_TEST, newline_replace=False),
    "mccp2_slow": slowsend(MCCP2_TEST, newline_replace=False)
}

HELLO = (
    "Welcome to The Mud Client Test Server\r\n"
    "How would you like to torture your mud client?\r\n").encode()


MENU = (
    "Options are: " + ", ".join(OPTIONS) + "\r\n"
).encode()


def sendall(sock: socket.socket, data: bytes):
    view = memoryview(data)
    while view:
        n = sock.send(view)
        view = view[n:]


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
