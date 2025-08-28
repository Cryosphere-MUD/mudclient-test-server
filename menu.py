
from testdata import ANSI_TEST, UTF8_TEST, MCCP2_TEST
from mudsocket import send, slowsend

from nawstest import nawstest_handler

from optionscan import optionscan_handler

from baudtest import baudtest_handler

OPTIONS = {
    "ansi": send(ANSI_TEST),
    "ansi_slow": slowsend(ANSI_TEST),
    "utf": send(UTF8_TEST),
    "utf_slow": slowsend(UTF8_TEST),
    "mccp2": send(MCCP2_TEST, newline_replace=False),
    "mccp2_slow": slowsend(MCCP2_TEST, newline_replace=False),
    "naws": nawstest_handler,
    "optionscan": optionscan_handler,
    "baudtest": baudtest_handler,
}

HELLO = (
    "Welcome to The Mud Client Test Server\r\n"
    "How would you like to torture your mud client?\r\n").encode()

MENU = (
    "Options are: " + ", ".join(OPTIONS) + "\r\n"
    "\r\n"
    "Try 'baudtest' for a comprehensive capability test!\r\n"
).encode()
