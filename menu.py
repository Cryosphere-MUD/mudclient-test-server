
from testdata import ANSI_TEST, UTF8_TEST, MCCP2_TEST
from mudsocket import send, slowsend

from nawstest import nawstest_handler

from optionscan import optionscan_handler
from emptysubneg import emptysubneg_handler
from echo import echo_handler
from ttype import ttype_handler

from baudtest import baudtest_handler
from xterm256 import xterm256_handler
from truecolor import truecolor_handler

OPTIONS = {
    "ansi": send(ANSI_TEST),
    "ansi_slow": slowsend(ANSI_TEST),
    "utf": send(UTF8_TEST),
    "utf_slow": slowsend(UTF8_TEST),
    "mccp2": send(MCCP2_TEST, newline_replace=False),
    "mccp2_slow": slowsend(MCCP2_TEST, newline_replace=False),
    "naws": nawstest_handler,
    "optionscan": optionscan_handler,
    "emptysubneg": emptysubneg_handler,
    "echo": echo_handler,
    "ttype": ttype_handler,
    "baudtest": baudtest_handler,
    "xterm256": xterm256_handler,
    "truecolor": truecolor_handler,
}

# Create word-wrapped options list
def create_menu():
    # Options with word wrapping at 80 chars
    options_text = "Options are: " + ", ".join(OPTIONS)
    wrapped_options = ""
    current_line = ""
    
    for word in options_text.split():
        if len(current_line + word + " ") <= 80:
            current_line += word + " "
        else:
            wrapped_options += current_line.rstrip() + "\r\n"
            current_line = word + " "
    wrapped_options += current_line.rstrip() + "\r\n"
    
    return (wrapped_options + "\r\n" + 
            "Try 'baudtest' for a comprehensive capability test!\r\n").encode()

HELLO = (
    "Welcome to The Mud Client Test Server\r\n"
    "How would you like to torture your mud client?\r\n").encode()

MENU = create_menu()
