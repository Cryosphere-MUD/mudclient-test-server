import datetime
from mudsocket import send_slow_baud
from telnetconstants import IAC, WONT, DONT, ECHO

def get_baudtest_intro():
    """Generate the introductory text for baudtest"""
    return b"""Hello, fellow network agent!

   Just between us 'bots, I want you to know that I am speaking to you slowly,
at about 1200 bits per second, so that you can check if your stream reassembly
routines are working correctly.
   
   If you speak UTF-8 and ANSI basic color, you shouldn't see any question
marks or weird characters due to my annoyingly slow send rate. If you offer
trigger support to your user, you should also be able to match on the text in
this paragraph without a problem too!



"""

def get_color_tests():
    """Generate comprehensive color tests"""
    content = b"""                     This is a nice test of some basic ANSI colors.\n\n"""
    
    # Beautiful gradient welcome text with underline
    welcome_text = "Welcome to the MUD Client Test Server!"
    welcome_colors = [220, 215, 209, 204, 205, 200, 201, 165, 99, 69, 51, 50, 84, 190, 226, 220, 209, 204, 205, 200, 201, 165, 69, 45, 51, 50, 119, 190, 226, 220, 215, 209, 204]
    
    # Center the welcome text (72 chars wide, so center at 36)
    content += b"                         "  # 25 spaces to center roughly
    
    for i, char in enumerate(welcome_text):
        color = welcome_colors[i % len(welcome_colors)]
        content += f"\033[4;38;5;{color}m{char}\033[0m".encode()  # underlined and colored
    
    # Explicit reset to ensure underline is completely cleared
    content += b"\033[24m\033[0m\n\n"
    
    # Basic ANSI colors
    content += b"          ANSI Normal: "
    colors = [(33, "Yellow"), (32, "Green"), (36, "Cyan"), (34, "Blue"), (35, "Purple"), (31, "Red"), (37, "White"), (30, "Black")]
    for code, name in colors:
        content += f"\033[{code}m{name} \033[0m".encode()
    
    content += b"\n          ANSI Bolded: "
    for code, name in colors:
        content += f"\033[1;{code}m{name} \033[0m".encode()
    
    content += b"\n          ANSI Bright: "
    for code, name in colors:
        bright_code = code + 60 if code < 38 else code
        content += f"\033[{bright_code}m{name} \033[0m".encode()
    
    # Common ANSI attributes
    content += b"\n\n                            Common ANSI Attributes:\n"
    content += b"                               \033[1mBold\033[0m \033[2mFaint\033[0m \033[3mItalic\033[0m\n"
    content += b"                           \033[4mUnderline\033[0m \033[5mBlink\033[0m \033[6mFastblink\033[0m\n"
    content += b"                          \033[9mCrossedout\033[0m \033[21mDoubleul\033[0m \033[7mReverse\033[0m\n\n"
    
    # 256-color palette with actual colored output, 72 characters wide
    content += b"Indexed Palette\n"
    # First 16 colors with proper spacing and actual colors
    for i in range(16):
        if i < 10:
            content += f"\033[38;5;{i}m{i}\033[0m ".encode()
        else:
            content += f"\033[38;5;{i}m{i}\033[0m ".encode()  # Added space after double digits too
    content += b"\n"
    
    # Colors 16-255 in compact hex grid - fit 36 colors per line (72 chars)
    for row in range(7):  # 7 rows to fit 240 colors (16-255 = 240 colors)
        for col in range(36):
            color_num = 16 + row * 36 + col
            if color_num <= 255:
                content += f"\033[38;5;{color_num}m{color_num:02X}\033[0m".encode()
        content += b"\n"
    
    # Grayscale ramp 232-255 with actual colors, fit on one line
    content += b" "
    for i in range(232, 256):
        content += f"\033[38;5;{i}m{i:03d}\033[0m".encode()  # 3 digits for 232-255
        if i < 255:
            content += b" "
    content += b"\n"
    
    # Comprehensive background color tests
    content += b"\n\nBackground Color Tests:\n"
    
    # Create rainbow background gradient using truecolor
    import math
    
    content += b"Rainbow Gradient (Truecolor backgrounds):\n"
    # Generate rainbow gradient across 72 characters, just 2 lines
    for line in range(2):  # Reduced from 3 to 2 lines
        for i in range(72):
            # Create hue from 0 to 360 degrees
            hue = (i / 72.0) * 360
            
            # Convert HSV to RGB (saturation=1, value=1 for bright colors)
            h = hue / 60.0
            c = 1.0  # saturation * value
            x = c * (1 - abs((h % 2) - 1))
            
            if 0 <= h < 1:
                r, g, b = c, x, 0
            elif 1 <= h < 2:
                r, g, b = x, c, 0
            elif 2 <= h < 3:
                r, g, b = 0, c, x
            elif 3 <= h < 4:
                r, g, b = 0, x, c
            elif 4 <= h < 5:
                r, g, b = x, 0, c
            else:
                r, g, b = c, 0, x
            
            # Convert to 0-255 range
            r, g, b = int(r * 255), int(g * 255), int(b * 255)
            
            # Use truecolor background
            content += f"\033[48;2;{r};{g};{b}m \033[0m".encode()
        content += b"\n"
    
    # Mixed foreground and background color tests
    content += b"\nMixed Foreground/Background Tests:\n"
    
    # Test various combinations
    test_combinations = [
        (15, 1, "White on Red"),    # white fg, red bg
        (0, 11, "Black on Cyan"),   # black fg, cyan bg
        (226, 21, "Yellow on Blue"), # bright yellow fg, blue bg
        (196, 46, "Red on Green"),   # red fg, green bg
        (129, 53, "Purple on Magenta"), # purple fg, magenta bg
    ]
    
    for fg, bg, desc in test_combinations:
        content += f"\033[38;5;{fg}m\033[48;5;{bg}m {desc} \033[0m ".encode()
    content += b"\n"
    
    # Gradient with text - single line test
    content += b"Background gradient with white text:\n"
    for i in range(72):  # Just one line of 72 characters
        content += f"\033[38;5;15m\033[48;5;{i}m▓\033[0m".encode()
    content += b"\n"
    
    return content

def get_utf8_tests():
    """Generate comprehensive UTF-8 tests"""
    current_time = datetime.datetime.now().strftime("%I:%M %p EST")
    
    content = f" ⠕ ⠖ ⠌ ⠓ ⡡ Server time is {current_time}.≋≋╰⠝⠥😽 ⠕ ⠖ ⠌ ⠓ ⡡ \n\n".encode()
    
    # UTF-8 test with xterm colors: 238 for borders, 220 for text
    border_color = "\033[38;5;238m"  # Dark gray
    text_color = "\033[38;5;220m"    # Golden yellow
    reset = "\033[0m"
    
    # Build the UTF-8 table with proper formatting
    content += f"UTF-8 Test:\n".encode()
    content += f"          {border_color}╭────────────────────────────────────────────────────────────╮{reset}\n".encode()
    
    # Language tests with proper alignment - match exact spacing from original
    languages = [
        ("English  ", "The quick brown fox jumps over the lazy dog.              "),
        ("German   ", "Falsches Üben von Xylophonmusik quält jeden größeren Zwerg"),
        ("Spanish  ", "¿¡Puedo comer vidrio, no me hace daño!?                   "),
        ("Québécois", "J'peux manger d'la vitre, ça m'fa pas mal.                "),
        ("Russian  ", "Я могу есть стекло, оно мне не вредит.                    "),
        ("Romanian ", "Pot să mănânc sticlă și ea nu mă rănește.                 "),
        ("Runic    ", "ᛁᚳ᛫ᛗᚨᚷ᛫ᚷᛚᚨᛋ᛫ᛖᚩᛏᚪᚾ᛫ᚩᚾᛞ᛫ᚻᛁᛏ᛫ᚾᛖ᛫ᚻᛖᚪᚱᛗᛁᚪᚧ᛫ᛗᛖ᛬                 "),
        ("Obfuscate", "Ï çåῃ ēąԷ ǧĺǟṡš, ἱʈ ďὃęș ᾐȭե ĥǔɼẗ ḿѐ.                     "),
        ("Symbols  ", "¢ € ¥ £ ☆ ☏ ☼ © … ☠ ☻ ☺ ☹ ★ ☮ ♠ ♣ ♥ ♦ ⚒ ·                 "),
    ]
    
    for lang, text in languages:
        # Use exact spacing to match the box
        line = f"{lang} {border_color}│{reset} {text_color}{text}{reset} {border_color}│{reset}\n"
        content += line.encode('utf-8')
    
    content += f"          {border_color}╰────────────────────────────────────────────────────────────╯{reset}\n\n".encode()
    
    return content

def get_emoji_tests():
    """Generate comprehensive emoji tests"""
    content = b"""   What follows next is a veritable Noah's ark of animal emoji, for your\nviewing pleasure, courtesy of Rahjiii's imagination. There should be a space between each glyph.\n\nPage U+1f400\n"""
    
    # Properly aligned header and border
    content += "    0 1 2 3 4 5 6 7 8 9 a b c d e f\n".encode('utf-8')
    content += "  ╭────────────────────────────────\n".encode('utf-8')
    
    # Generate emoji grid (Unicode page U+1F400 to U+1F4FF)
    for row in range(16):
        content += f"{row:x} │ ".encode('utf-8')
        for col in range(16):
            emoji_code = 0x1F400 + row * 16 + col
            if emoji_code <= 0x1F4FF:
                try:
                    emoji_char = chr(emoji_code)
                    content += f"{emoji_char} ".encode('utf-8')
                except (ValueError, UnicodeEncodeError):
                    content += "  ".encode()
            else:
                content += "  ".encode()
        content += b"\n"
    
    return content

def get_link_tests():
    """Generate link support tests"""
    content = b"\n"
    
    # Colors for link tests - same as UTF-8 section
    label_color = "\033[38;5;238m"  # Dark gray for labels
    content_color = "\033[38;5;220m"  # Golden yellow for content
    reset = "\033[0m"
    
    # Regular text URL (not a link)
    content += f"{label_color}NOT a link - {reset}https://www.mudvault.org\n".encode()
    
    # OSC8 hyperlink - only the URL is clickable
    content += f"{label_color}Https link - {reset}\033]8;;https://www.mudvault.org\007https://www.mudvault.org\033]8;;\007\n".encode()
    
    # Another OSC8 link with display text - only the display text is clickable
    content += f"{label_color}Https link - {reset}Check out the \033]8;;https://www.mudvault.org\007MUD Client Test Server!\033]8;;\007\n".encode()
    
    # Send links (MUD command links) - only quoted text is gold and clickable
    content += f"{label_color}Send links - {reset}Want more? \033]8;;send:say please\007{content_color}'say please'{reset}\033]8;;\007 \033]8;;send:say no thanks\007{content_color}'say no thanks'{reset}\033]8;;\007.\n".encode()
    
    # Prompt link - only quoted text is gold and clickable
    content += f"{label_color}Prompt link- {reset}How many do you want? \033]8;;send:buy \007{content_color}'buy <quantity>'{reset}\033]8;;\007\n\n".encode()
    
    return content

def baudtest_handler(telnet):
    """Comprehensive client capability test"""
    
    # Send introduction slowly (1200 bps simulation)
    intro_text = get_baudtest_intro()
    send_slow_baud(telnet, intro_text)
    
    # Send color tests slowly too
    color_tests = get_color_tests()
    send_slow_baud(telnet, color_tests, bps=2400)  # Slightly faster but still slow
    
    # Send UTF-8 tests at normal speed
    utf8_tests = get_utf8_tests()
    telnet.send_text(utf8_tests)
    
    # Send emoji tests at normal speed
    emoji_tests = get_emoji_tests()
    telnet.send_text(emoji_tests)
    
    # Send link tests at normal speed
    link_tests = get_link_tests()
    telnet.send_text(link_tests)
    
    # Final message
    telnet.send_text("\n   And that's that. Hope it all worked out for you!\n\n")
    

def misc_handler(telnet):
    """Comprehensive client capability test"""
    
    telnet.send_text(get_color_tests())
    telnet.send_text(get_utf8_tests())    
    telnet.send_text(get_emoji_tests())
    telnet.send_text(get_link_tests())
    
