import string
import struct
from telnet import TelnetState
from telnetconstants import IAC, WILL, WONT, ECHO, command_name, option_name


def echo_handler(telnetstate):
        
        telnetstate.sendall(bytes([IAC, WILL, ECHO]), False)

        def neg_handler(command, option):
                opt_name = option_name(option)
                telnetstate.sendall(f"from client: {command_name(command)} {opt_name}\n")

        telnetstate.neg_handler = neg_handler

        telnetstate.sendall("Now please enter in a password.\n")
        
        telnetstate.readline()

        telnetstate.sendall(bytes([IAC, WONT, ECHO]), False)

