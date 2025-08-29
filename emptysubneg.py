import string
import struct
from telnet import TelnetState
from telnetconstants import IAC, SB, SE

def emptysubneg_handler(telnetstate):
        scan = bytes()

        for byte in range(0, 0xff):
                scan += bytes([IAC, SB, byte, IAC, SE])

        telnetstate.sendall(scan, False)

        telnetstate.sendall("sent empty subnegotiations for every option to the client\n")
