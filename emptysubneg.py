import string
import struct
from telnet import TelnetState
from telnetconstants import IAC, SB, SE

def emptysubneg_handler(telnetstate):
        scan = bytes()

        for byte in range(0, 0xff):
                scan += bytes([IAC, SB, byte, IAC, SE])

        telnetstate.send_bytes(scan, False)

        telnetstate.send_text("sent empty subnegotiations for every option to the client\n")
