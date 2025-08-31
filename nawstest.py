import struct
from telnet import TelnetState
from telnetconstants import IAC, DO, NAWS

def nawstest_handler(telnetstate):
        telnetstate.send_bytes(bytes([IAC, DO, NAWS]))

        def handle_naws(data):
                width, height = struct.unpack('!HH', data)
                if len(data) != 4:
                        telnetstate.send_text("NAWS subnegotation was of malformed length!\n")
                else:
                        telnetstate.send_text(f"NAWS reports your screen size as {width} cols and {height} rows. Resize it!\n")

        telnetstate.subneg_handlers[NAWS] = handle_naws

        telnetstate.send_bytes("press enter to return to the menu\n")

        telnetstate.readline()
