#!/usr/bin/env python3
import socket
import threading
import os
import time
import zlib
import struct
import datetime

from baudtest import baudtest_handler

from menu import HELLO, OPTIONS, MENU

from telnet import TelnetState

HOST = "0.0.0.0"
PORT = 5050

def handle_client(conn: socket.socket, addr):
    telnet = TelnetState(conn)

    telnet.sendall(HELLO)

    try:
        while True:
            telnet.reset()
            telnet.sendall(MENU)

            decoded = telnet.readline()

            option = decoded.split()[0] if decoded.split() else ""
            
            # First check if it's a main category
            option_data = OPTIONS.get(option)
            
            if option_data:
                # It's a main category
                _, optionhandler = option_data
                optionhandler(telnet)
                continue
            
            # Check if it's a submenu option by importing handlers directly
            from testdata import ANSI_TEST, UTF8_TEST, MCCP2_TEST
            from mudsocket import send, slowsend
            from nawstest import nawstest_handler
            from optionscan import optionscan_handler
            from emptysubneg import emptysubneg_handler
            from echo import echo_handler
            from ttype import ttype_handler
            from xterm256 import xterm256_handler
            from truecolor import truecolor_handler
            from mccp4 import mccp4_handler_zstd, mccp4_handler_deflate
            
            # Define all submenu options with their handlers
            all_submenu_options = {
                # Compression options
                "mccp2": ("MCCP2 (zlib)", send(MCCP2_TEST, newline_replace=False)),
                "mccp2_slow": ("MCCP2 (slow)", slowsend(MCCP2_TEST, newline_replace=False)),
                "mccp4": ("MCCP4 (zstd)", mccp4_handler_zstd),
                "mccp4_deflate": ("MCCP4 (deflate)", mccp4_handler_deflate),
                # Telnet options
                "naws": ("NAWS (window size)", nawstest_handler),
                "optionscan": ("Option scanning", optionscan_handler),
                "emptysubneg": ("Empty subnegotiations", emptysubneg_handler),
                "echo": ("Echo option", echo_handler),
                "ttype": ("Terminal type", ttype_handler),
                # Display options
                "ansi": ("ANSI colors", send(ANSI_TEST)),
                "ansi_slow": ("ANSI colors (slow)", slowsend(ANSI_TEST)),
                "xterm256": ("xterm 256 colors", xterm256_handler),
                "truecolor": ("True color (24-bit)", truecolor_handler),
                # Encoding options
                "utf": ("UTF-8 text", send(UTF8_TEST)),
                "utf_slow": ("UTF-8 text (slow)", slowsend(UTF8_TEST)),
            }
            
            if option in all_submenu_options:
                _, handler = all_submenu_options[option]
                
                # Handle compression options with session state tracking
                if option in ["mccp2", "mccp2_slow", "mccp4", "mccp4_deflate"]:
                    # Track compression usage similar to submenu logic
                    COMPRESSION_GROUPS = {
                        "mccp2": ["mccp2", "mccp2_slow"],
                        "mccp4_zstd": ["mccp4"],
                        "mccp4_deflate": ["mccp4_deflate"]
                    }
                    
                    if not hasattr(telnet, '_compression_used'):
                        telnet._compression_used = None
                    
                    # Find which group this option belongs to
                    option_group = None
                    for group_name, group_options in COMPRESSION_GROUPS.items():
                        if option in group_options:
                            option_group = group_name
                            break
                    
                    # Check if we can run this test
                    if telnet._compression_used is None:
                        telnet._compression_used = option_group
                    elif telnet._compression_used == option_group:
                        pass  # Same group - allow it
                    else:
                        # Different group - require reconnection
                        telnet.sendall(f"\r\nCannot mix different compression protocols in the same session.\r\n".encode())
                        telnet.sendall(f"You've already used: {telnet._compression_used}\r\n".encode())
                        telnet.sendall(f"To test {option_group}, please reconnect and try again.\r\n".encode())
                        continue
                    
                    # Run the test
                    try:
                        handler(telnet)
                        telnet.sendall(b"\r\nTest completed. You can run other tests in the same group or try other categories.\r\n")
                    except Exception as e:
                        telnet.sendall(f"\r\nTest failed: {e}\r\n".encode())
                else:
                    # Non-compression options - run directly
                    handler(telnet)
                continue
            
            if option:  # Only show error if they actually typed something
                telnet.sendall(f"Unknown option: {option}\r\n".encode())

    finally:
        conn.close()

def main():
    print(f"Serving on {HOST}:{PORT} (Ctrl+C to stop)")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(5)
        while True:
            conn, addr = srv.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down.")
