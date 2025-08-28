import string
import struct
from telnet import TelnetState
from telnetconstants import IAC, DO, WILL, DONT, WONT, command_name, option_name
from mudsocket import sendall

def pretty_bytes(data: bytes) -> str:
    result = []
    for b in data:
        if b >= 0x20 and b <= 0x7e:
            result.append(chr(b))
        else:
            result.append(f"\\x{b:02x}")  # hex escape
    return "".join(result)

def optionscan_handler(sock):
        scan = bytes()

        for byte in range(0, 0xff):
                scan += bytes([IAC, DO, byte])
                scan += bytes([IAC, WILL, byte])

        sendall(sock, scan, False)

        telnetstate = TelnetState()

        def neg_handler(command, option):
                if command not in (DONT, WONT):
                        our_cmd = "DO" if command == WILL else "WILL"
                        opt_name = option_name(option)
                        sendall(sock, f"server {our_cmd} {opt_name:15}: client: {command_name(command)} {opt_name}\n")

        def subneg_handler(option, data):
                sendall(sock, f"client: SUBNEG {option_name(option)}\n"
                "  payload: " + pretty_bytes(data) + "\n  or:     " + repr(data) + "\n")

        telnetstate.neg_handler = neg_handler
        telnetstate.handle_subneg = subneg_handler

        while True:
                data = sock.recv(1)

                telnetstate.process(data)

