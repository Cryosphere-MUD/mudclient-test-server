import string
import struct
from telnet import TelnetState
from telnetconstants import IAC, WILL, WONT, ECHO, command_name, option_name


def echo_handler(telnetstate):
        
        telnetstate.send_bytes(bytes([IAC, WILL, ECHO]))

        def neg_handler(command, option):
                opt_name = option_name(option)
                telnetstate.send_text(f"from client: {command_name(command)} {opt_name}\n")

        telnetstate.neg_handler = neg_handler

        telnetstate.send_text("Now please enter in a password.\n")
        
        telnetstate.readline()

        telnetstate.send_bytes(bytes([IAC, WONT, ECHO]))

