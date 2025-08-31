from submenu import MAIN_CATEGORIES, ALL_OPTIONS

def create_menu():
    menu_text = "\nMain Menu\n=========\n"
    menu_text += "Categories (Select to see more details about each test):\n"
    for key, (desc, _) in MAIN_CATEGORIES.items():
        menu_text += f"  {key:<15} - {desc}\n"
    
    # Show all direct options
    menu_text += "\nDirect access (or use category above):\n"
    menu_text += "  Compression:    mccp2, mccp2_slow, mccp4, mccp4_deflate\n"
    menu_text += "  Telnet:         naws, optionscan, emptysubneg, echo, ttype\n" 
    menu_text += "  Display:        ansi, ansi_slow, xterm256, truecolor\n"
    menu_text += "  Encoding:       utf, utf_slow\n"
    menu_text += "  Comprehensive:  baudtest\n"
    
    menu_text += "\nChoose a category or specific test: "
    return menu_text.encode()

HELLO = (
    "Welcome to The Mud Client Test Server\n"
    "How would you like to torture your mud client?\n").encode()

MENU = create_menu()

OPTIONS = ALL_OPTIONS