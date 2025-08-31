from testdata import ANSI_TEST, UTF8_TEST, MCCP2_TEST
from mudsocket import bytes_sender, bytes_slow_sender, text_sender, text_slow_sender
from nawstest import nawstest_handler
from optionscan import optionscan_handler
from emptysubneg import emptysubneg_handler
from echo import echo_handler
from ttype import ttype_handler
from baudtest import baudtest_handler
from xterm256 import XTERM256_TEST
from truecolor import TRUECOLOR_TEST
from mccp4 import mccp4_handler_zstd
from base_submenu import BaseSubmenu, CompressionSubmenu


# Define options once per category
COMPRESSION_OPTIONS = {
    "mccp2": ("MCCP2 (zlib)", bytes_sender(MCCP2_TEST)),
    "mccp2_slow": ("MCCP2 (slow)", bytes_slow_sender(MCCP2_TEST)),
    "mccp4": ("MCCP4 (zstd)", mccp4_handler_zstd),
}

def compression_submenu(telnet):
    """Handle compression test submenu using CompressionSubmenu class."""
    submenu = CompressionSubmenu("Compression Tests", COMPRESSION_OPTIONS)
    submenu.run(telnet)


TELNET_OPTIONS = {
    "naws": ("NAWS (window size)", nawstest_handler),
    "optionscan": ("Option scanning", optionscan_handler),
    "emptysubneg": ("Empty subnegotiations", emptysubneg_handler),
    "echo": ("Echo option", echo_handler),
    "ttype": ("Terminal type", ttype_handler),
}

def telnet_submenu(telnet):
    """Handle telnet protocol test submenu using BaseSubmenu class."""
    submenu = BaseSubmenu("Telnet Protocol Tests", TELNET_OPTIONS)
    submenu.run(telnet)


DISPLAY_OPTIONS = {
    "ansi": ("ANSI colors", text_sender(ANSI_TEST)),
    "ansi_slow": ("ANSI colors (slow)", text_slow_sender(ANSI_TEST)),
    "xterm256": ("xterm 256 colors", text_sender(XTERM256_TEST)),
    "xterm256_slow": ("xterm 256 colors", text_slow_sender(XTERM256_TEST)),
    "truecolor": ("True color (24-bit)", text_sender(TRUECOLOR_TEST)),
    "truecolor_slow": ("True color (24-bit)", text_slow_sender(TRUECOLOR_TEST)),
}


def display_submenu(telnet):
    """Handle display/color test submenu using BaseSubmenu class."""
    submenu = BaseSubmenu("Display & Color Tests", DISPLAY_OPTIONS)
    submenu.run(telnet)


ENCODING_OPTIONS = {
    "utf": ("UTF-8 text", text_sender(UTF8_TEST)),
    "utf_slow": ("UTF-8 text (slow)", text_slow_sender(UTF8_TEST)),
}

def encoding_submenu(telnet):
    """Handle text encoding test submenu using BaseSubmenu class."""
    submenu = BaseSubmenu("Text Encoding Tests", ENCODING_OPTIONS)
    submenu.run(telnet)


# Main category handlers
MAIN_CATEGORIES = {
    "compression": ("Compression tests (MCCP2/4)", compression_submenu),
    "telnet": ("Telnet protocol tests", telnet_submenu),
    "display": ("Display & color tests", display_submenu),
    "encoding": ("Text encoding tests", encoding_submenu),
    "baudtest": ("Comprehensive capability test", baudtest_handler),
}

# Automatically build individual options from category definitions
INDIVIDUAL_OPTIONS = {
    **COMPRESSION_OPTIONS,
    **TELNET_OPTIONS, 
    **DISPLAY_OPTIONS,
    **ENCODING_OPTIONS,
}

# Combined options dictionary
ALL_OPTIONS = {**MAIN_CATEGORIES, **INDIVIDUAL_OPTIONS}