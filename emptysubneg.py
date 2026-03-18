import string
import struct
from telnet import TelnetState
from telnetconstants import IAC, SB, SE

def emptysubneg_handler(slow):
        def fn(telnetstate):
                scan = bytes()

                for byte in range(0, 0xff):
                        scan += bytes([IAC, SB, byte, IAC, SE])
                        
                if slow:
                        telnetstate.slow_send_bytes(scan)
                else:
                        telnetstate.send_bytes(scan)

                telnetstate.send_text("sent empty subnegotiations for every option to the client\n")

        return fn