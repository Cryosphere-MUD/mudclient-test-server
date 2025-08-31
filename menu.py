from submenu import MAIN_CATEGORIES, ALL_OPTIONS

def create_menu():
    menu_text = "\r\nMain Menu\r\n=========\r\n"
    menu_text += "Categories (Select to see more details about each test):\r\n"
    for key, (desc, _) in MAIN_CATEGORIES.items():
        menu_text += f"  {key:<15} - {desc}\r\n"
    
    # Show all direct options
    menu_text += "\r\nDirect access (or use category above):\r\n"
    menu_text += "  Compression:    mccp2, mccp2_slow, mccp4, mccp4_deflate\r\n"
    menu_text += "  Telnet:         naws, optionscan, emptysubneg, echo, ttype\r\n" 
    menu_text += "  Display:        ansi, ansi_slow, xterm256, truecolor\r\n"
    menu_text += "  Encoding:       utf, utf_slow\r\n"
    menu_text += "  Comprehensive:  baudtest\r\n"
    
    menu_text += "\r\nChoose a category or specific test: "
    return menu_text.encode()

HELLO = (
    "Welcome to The Mud Client Test Server\r\n"
    "How would you like to torture your mud client?\r\n").encode()

MENU = create_menu()

OPTIONS = ALL_OPTIONS