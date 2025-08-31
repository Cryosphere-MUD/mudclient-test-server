import socket
import time

def bytes_sender(data):
    return lambda telnet: telnet.send_bytes(data)

def bytes_slow_sender(data):
    def fn(telnet):
        view = memoryview(data)
        while view:
            n = telnet.sock.send(view[0:15])
            view = view[n:]
            time.sleep(0.1)
    return fn

def text_sender(text):
    data = text.encode().replace(b"\n", b"\r\n")
    return lambda telnet: telnet.send_bytes(data)

def text_slow_sender(text):
    data = text.encode().replace(b"\n", b"\r\n")
    return bytes_slow_sender(data)

def send_slow_baud(telnet, text, bps=1200):
    """Send text at specified bits per second (simulating old modem speeds)"""
    bytes_per_second = bps // 8  # Convert bits to bytes
    text = text.replace(b"\n", b"\r\n")
    
    for i in range(0, len(text), bytes_per_second):
        chunk = text[i:i + bytes_per_second]
        telnet.sock.send(chunk)
        if i + bytes_per_second < len(text):
            time.sleep(1.0)  # Wait 1 second between chunks

