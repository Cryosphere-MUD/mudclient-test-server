from testdata import ANSI_TEST, UTF8_TEST, MCCP2_TEST
from mudsocket import bytes_sender, bytes_slow_sender, text_sender, text_slow_sender
from nawstest import nawstest_handler
from optionscan import optionscan_handler
from emptysubneg import emptysubneg_handler
from echo import echo_handler
from ttype import ttype_handler
from osc8 import OSC8_TEST
from mxp import MXP_TEST
from xterm256 import XTERM256_TEST
from truecolor import TRUECOLOR_TEST
from mccp4 import mccp4_handler_zstd
from combined import combined_handler, combined_handler_slow
from emoji import EMOJI_TEST

CATEGORIES = {
    "compression": {
        "mccp2": ("MCCP2 (zlib)", bytes_sender(MCCP2_TEST)),
        "mccp2_slow": ("MCCP2 (slow)", bytes_slow_sender(MCCP2_TEST)),
        "mccp4": ("MCCP4 (zstd)", mccp4_handler_zstd),
    },
    "telnet": {
        "naws": ("NAWS (window size)", nawstest_handler),
        "optionscan": ("Option scanning", optionscan_handler),
        "emptysubneg": ("Empty subnegotiations", emptysubneg_handler),
        "echo": ("Echo option", echo_handler),
        "ttype": ("Terminal type", ttype_handler),
    },
    "display": {
        "ansi": ("ANSI colors", text_sender(ANSI_TEST)),
        "ansi_slow": ("ANSI colors (slow)", text_slow_sender(ANSI_TEST)),
        "xterm256": ("xterm 256 colors", text_sender(XTERM256_TEST)),
        "xterm256_slow": ("xterm 256 colors", text_slow_sender(XTERM256_TEST)),
        "truecolor": ("True color (24-bit)", text_sender(TRUECOLOR_TEST)),
        "truecolor_slow": ("True color (24-bit)", text_slow_sender(TRUECOLOR_TEST)),
        "mxp": ("MXP", bytes_sender(MXP_TEST)),
        "mxp_slow": ("MXP", bytes_slow_sender(MXP_TEST)),
        "link": ("MXP", bytes_sender(OSC8_TEST)),
        "link_slow": ("MXP", bytes_slow_sender(OSC8_TEST)),
    },
    "encoding": {
        "utf": ("UTF-8 text", text_sender(UTF8_TEST)),
        "utf_slow": ("UTF-8 text (slow)", text_slow_sender(UTF8_TEST)),
        "emoji": ("Animal emoji", text_sender(EMOJI_TEST)),
        "emoji_slow": ("Animal emoji (slow)", text_slow_sender(EMOJI_TEST)),
    },
    "general": {
        "combined": ("combined misc test", combined_handler),
        "combined_slow": ("combined misc test (slow)", combined_handler_slow),
    }
}

OPTIONS = {}

for category in CATEGORIES.values():
    for test_id, test in category.items():
        OPTIONS[test_id] = test

    