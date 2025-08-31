import string
import struct
from telnet import TelnetState
from telnetconstants import IAC, DO, TTYPE, WONT, TTYPE, SB, SE, command_name, option_name, TTYPE_SEND, TTYPE_IS


def ttype_handler(telnetstate):
        
        telnetstate.send_bytes(bytes([IAC, DO, TTYPE, IAC, SB, TTYPE, TTYPE_SEND, IAC, SE]))

        seen_ttypes = set()

        counter = 0

        def handle_type(ttype):
                if ttype[0] == TTYPE_IS:
                        telnetstate.send_text(f"  terminal is {ttype[1:].decode()}\n")

                        if ttype not in seen_ttypes:
                                telnetstate.send_text(bytes([IAC, SB, TTYPE, TTYPE_SEND, IAC, SE]))
                        
                        seen_ttypes.add(ttype)
                else:
                        
                        telnetstate.send_text(f"  bad ttype response {ttype}\n")

        telnetstate.subneg_handlers[TTYPE] = handle_type

        telnetstate.send_text("press enter to go back to menu.\n")

        telnetstate.readline()


