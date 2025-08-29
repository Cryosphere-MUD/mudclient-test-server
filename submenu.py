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
from mccp4 import mccp4_handler_zstd, mccp4_handler_deflate


def create_submenu_text(title, options):
    """Create formatted submenu text"""
    menu_text = f"\r\n{title}\r\n" + "=" * len(title) + "\r\n"
    for key, desc in options:
        menu_text += f"  {key:<15} - {desc}\r\n"
    menu_text += "\r\nType 'back' to return to main menu, or choose an option: "
    return menu_text.encode()


def compression_submenu(telnet):
    """Handle compression test submenu"""
    COMPRESSION_OPTIONS = {
        "mccp2": ("MCCP2 (zlib)", send(MCCP2_TEST, newline_replace=False)),
        "mccp2_slow": ("MCCP2 (slow)", slowsend(MCCP2_TEST, newline_replace=False)),
        "mccp4": ("MCCP4 (zstd)", mccp4_handler_zstd),
        "mccp4_deflate": ("MCCP4 (deflate)", mccp4_handler_deflate),
    }
    
    # Group compatible tests
    COMPRESSION_GROUPS = {
        "mccp2": ["mccp2", "mccp2_slow"],  # MCCP2 variants are compatible
        "mccp4_zstd": ["mccp4"],           # MCCP4 zstd standalone
        "mccp4_deflate": ["mccp4_deflate"] # MCCP4 deflate (becomes MCCP2) standalone
    }
    
    # Track what compression type has been used in this session
    if not hasattr(telnet, '_compression_used'):
        telnet._compression_used = None
    
    menu_items = [(key, desc) for key, (desc, _) in COMPRESSION_OPTIONS.items()]
    
    while True:
        telnet.sendall(create_submenu_text("Compression Tests", menu_items))
        decoded = telnet.readline()
        option = decoded.split()[0] if decoded.split() else ""
        
        if option == "back":
            return
        elif option in COMPRESSION_OPTIONS:
            # Find which group this option belongs to
            option_group = None
            for group_name, group_options in COMPRESSION_GROUPS.items():
                if option in group_options:
                    option_group = group_name
                    break
            
            # Check if we can run this test
            if telnet._compression_used is None:
                # First compression test - allow it
                telnet._compression_used = option_group
            elif telnet._compression_used == option_group:
                # Same group - allow it
                pass
            else:
                # Different group - require reconnection
                telnet.sendall(f"\r\nCannot mix different compression protocols in the same session.\r\n".encode())
                telnet.sendall(f"You've already used: {telnet._compression_used}\r\n".encode())
                telnet.sendall(f"To test {option_group}, please reconnect and try again.\r\n".encode())
                continue
            
            # Run the test
            _, handler = COMPRESSION_OPTIONS[option]
            try:
                handler(telnet)
                if telnet._compression_used == option_group:
                    # Same group - can run more
                    telnet.sendall(b"\r\nTest completed. You can run other tests in the same group.\r\n")
                else:
                    # Different group - warn about reconnection
                    telnet.sendall(b"\r\nTest completed. Reconnect to test different compression protocols.\r\n")
            except Exception as e:
                telnet.sendall(f"\r\nTest failed: {e}\r\n".encode())
        elif option:
            telnet.sendall(f"Unknown option: {option}\r\n".encode())


def telnet_submenu(telnet):
    """Handle telnet protocol test submenu"""
    TELNET_OPTIONS = {
        "naws": ("NAWS (window size)", nawstest_handler),
        "optionscan": ("Option scanning", optionscan_handler),
        "emptysubneg": ("Empty subnegotiations", emptysubneg_handler),
        "echo": ("Echo option", echo_handler),
        "ttype": ("Terminal type", ttype_handler),
    }
    
    menu_items = [(key, desc) for key, (desc, _) in TELNET_OPTIONS.items()]
    
    while True:
        telnet.sendall(create_submenu_text("Telnet Protocol Tests", menu_items))
        decoded = telnet.readline()
        option = decoded.split()[0] if decoded.split() else ""
        
        if option == "back":
            return
        elif option in TELNET_OPTIONS:
            _, handler = TELNET_OPTIONS[option]
            handler(telnet)
            return
        elif option:
            telnet.sendall(f"Unknown option: {option}\r\n".encode())


def display_submenu(telnet):
    """Handle display/color test submenu"""
    DISPLAY_OPTIONS = {
        "ansi": ("ANSI colors", send(ANSI_TEST)),
        "ansi_slow": ("ANSI colors (slow)", slowsend(ANSI_TEST)),
        "xterm256": ("xterm 256 colors", xterm256_handler),
        "truecolor": ("True color (24-bit)", truecolor_handler),
    }
    
    menu_items = [(key, desc) for key, (desc, _) in DISPLAY_OPTIONS.items()]
    
    while True:
        telnet.sendall(create_submenu_text("Display & Color Tests", menu_items))
        decoded = telnet.readline()
        option = decoded.split()[0] if decoded.split() else ""
        
        if option == "back":
            return
        elif option in DISPLAY_OPTIONS:
            _, handler = DISPLAY_OPTIONS[option]
            handler(telnet)
            return
        elif option:
            telnet.sendall(f"Unknown option: {option}\r\n".encode())


def encoding_submenu(telnet):
    """Handle text encoding test submenu"""
    ENCODING_OPTIONS = {
        "utf": ("UTF-8 text", send(UTF8_TEST)),
        "utf_slow": ("UTF-8 text (slow)", slowsend(UTF8_TEST)),
    }
    
    menu_items = [(key, desc) for key, (desc, _) in ENCODING_OPTIONS.items()]
    
    while True:
        telnet.sendall(create_submenu_text("Text Encoding Tests", menu_items))
        decoded = telnet.readline()
        option = decoded.split()[0] if decoded.split() else ""
        
        if option == "back":
            return
        elif option in ENCODING_OPTIONS:
            _, handler = ENCODING_OPTIONS[option]
            handler(telnet)
            return
        elif option:
            telnet.sendall(f"Unknown option: {option}\r\n".encode())


MAIN_CATEGORIES = {
    "compression": ("Compression tests (MCCP2/4)", compression_submenu),
    "telnet": ("Telnet protocol tests", telnet_submenu),
    "display": ("Display & color tests", display_submenu),
    "encoding": ("Text encoding tests", encoding_submenu),
    "baudtest": ("Comprehensive capability test", baudtest_handler),
}