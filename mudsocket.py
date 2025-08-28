import socket
import time

def send(data, newline_replace=True):
    if newline_replace:
        data = data.replace(b"\n", b"\r\n")
    return lambda sock: sendall(sock, data, False)

def slowsend(data, newline_replace=True):
    if newline_replace:
        data = data.replace(b"\n", b"\r\n")
    def fn(sock):
        view = memoryview(data)
        while view:
            n = sock.send(view[0:15])
            view = view[n:]
            time.sleep(0.1)
    return fn

def send_slow_baud(sock, text, bps=1200):
    """Send text at specified bits per second (simulating old modem speeds)"""
    bytes_per_second = bps // 8  # Convert bits to bytes
    text = text.replace(b"\n", b"\r\n")
    
    for i in range(0, len(text), bytes_per_second):
        chunk = text[i:i + bytes_per_second]
        sock.send(chunk)
        if i + bytes_per_second < len(text):
            time.sleep(1.0)  # Wait 1 second between chunks

def sendall(sock: socket.socket, data, newline_replace = True):
    if isinstance(data, str):
        data = data.encode()
    if newline_replace:
        data = data.replace(b"\n", b"\r\n")
    view = memoryview(data)
    while view:
        n = sock.send(view)
        view = view[n:]
