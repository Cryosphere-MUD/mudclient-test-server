from tests import CATEGORIES

def create_menu():
    menu_text = "\nMain Menu\n=========\n"
    menu_text += "Categories (Select to see more details about each test):\n"
    for key, tests in CATEGORIES.items():
        desc = ", ".join([item for item in tests])
        menu_text += f"  {key:<15} - {desc}\n"
    
    menu_text += "\nChoose a category or specific test: "
    return menu_text.encode()

HELLO = (
    "Welcome to The Mud Client Test Server\n"
    "How would you like to torture your mud client?\n").encode()

MENU = create_menu()
