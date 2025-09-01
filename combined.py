import datetime
from mudsocket import send_slow_baud
from telnetconstants import IAC, WONT, DONT, ECHO

from testdata import ANSI_TEST, UTF8_TEST
from xterm256 import XTERM256_TEST
from truecolor import TRUECOLOR_TEST
from osc8 import OSC8_TEST
from emoji import EMOJI_TEST


GENERAL_TESTS = (ANSI_TEST, XTERM256_TEST, TRUECOLOR_TEST, UTF8_TEST, EMOJI_TEST, OSC8_TEST)


def combined_handler_slow(telnet):
    """Comprehensive client capability test"""

    for test in GENERAL_TESTS:
        send_slow_baud(telnet, test.encode(), bps=2400)
    

def combined_handler(telnet):
    """Comprehensive client capability test"""
    
    for test in GENERAL_TESTS:
        telnet.send_text(test)
    
