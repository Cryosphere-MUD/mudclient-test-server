import string
import struct
from telnet import TelnetState
from telnetconstants import IAC, DO, TTYPE, WONT, TTYPE, SB, SE, command_name, option_name, TTYPE_SEND, TTYPE_IS


def ttype_handler(telnetstate):
        
        telnetstate.sendall(bytes([IAC, DO, TTYPE, IAC, SB, TTYPE, TTYPE_SEND, IAC, SE]), False)

        seen_ttypes = set()

        def handle_type(ttype):
                if ttype[0] == TTYPE_IS:
                        telnetstate.sendall(f"  terminal is {ttype[1:].decode()}\n")

                        if ttype not in seen_ttypes:
                                telnetstate.sendall(bytes([IAC, SB, TTYPE, TTYPE_SEND, IAC, SE]))
                        
                        seen_ttypes.add(ttype)
                else:
                        
                        telnetstate.sendall(f"  bad ttype response {ttype}\n")

        telnetstate.subneg_handlers[TTYPE] = handle_type

        telnetstate.sendall("press enter to go back to menu.\n")

        telnetstate.readline()


