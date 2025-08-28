import struct
from telnet import TelnetState
from telnetconstants import IAC, DO, NAWS
from mudsocket import sendall

def nawstest_handler(sock):
        sendall(sock, bytes([IAC, DO, NAWS]))

        telnetstate = TelnetState()

        def handle_naws(data):
                width, height = struct.unpack('!HH', data)
                if len(data) != 4:
                        sendall(sock, "NAWS subnegotation was of malformed length!\n")
                else:
                        sendall(sock, f"NAWS reports your screen size as {width} cols and {height} rows. Resize it!\n")

        telnetstate.subneg_handlers[NAWS] = handle_naws

        while True:
                data = sock.recv(1)
                telnetstate.process(data)
