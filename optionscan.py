import string
import struct
from telnet import TelnetState
from telnetconstants import IAC, DO, WILL, DONT, WONT, command_name, option_name

def optionscan_handler(telnetstate):
        scan = bytes()

        for byte in range(0, 0xff):
                scan += bytes([IAC, DO, byte])
                scan += bytes([IAC, WILL, byte])

        telnetstate.sendall(scan, False)

        def neg_handler(command, option):
                if command not in (DONT, WONT):
                        our_cmd = "DO" if command == WILL else "WILL"
                        opt_name = option_name(option)
                        server_cmd = our_cmd + " " + opt_name
                        telnetstate.sendall(f"server {server_cmd:20}: client: {command_name(command)} {opt_name}\n")

        def subneg_handler(option, data):
                telnetstate.sendall(f"client: SUBNEG {option_name(option)}\n  payload: {data}\n")

        telnetstate.neg_handler = neg_handler
        telnetstate.handle_subneg = subneg_handler

        telnetstate.sendall("press enter to return to the menu\n")

        telnetstate.readline()
