

def get_xterm256_handler_string():
    """Test xterm 256-color palette (foreground and background)"""
    
    content = "=== XTerm 256-Color Test ===\n\n"
    
    # Standard colors (0-15)
    content += "Standard Colors (0-15):\n"
    for i in range(16):
        if i == 8:
            content += "\n"
        content += f"\033[38;5;{i}m{i:3d}\033[0m "
    content += "\n\n"
    
    # 216 color cube (16-231)
    content += "216-Color Cube (16-231):\n"
    for r in range(6):
        for g in range(6):
            for b in range(6):
                color = 16 + (r * 36) + (g * 6) + b
                content += f"\033[38;5;{color}m\u2588\033[0m"
            content += " "
        content += "\n"
    content += "\n"
    
    # Grayscale ramp (232-255)
    content += "Grayscale Ramp (232-255):\n"
    for i in range(232, 256):
        content += f"\033[38;5;{i}m\u2588\033[0m"
    content += "\n\n"
    
    # Background color test
    content += "Background Colors Sample:\n"
    test_colors = [1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14]
    for color in test_colors:
        content += f"\033[48;5;{color}m\033[38;5;15m {color:3d} \033[0m "
    content += "\n\n"
    
    # Color gradient
    content += "Color Gradient:\n"
    for i in range(0, 256, 4):
        content += f"\033[48;5;{i}m \033[0m"
    content += "\n\n"
    
    # Gradient text examples
    content += "Gradient Text Examples:\n\n"
    
    # Fire gradient using xterm256 colors (red -> orange -> yellow)
    text1 = "XTerm256 fire gradient text"
    fire_colors = [52, 88, 124, 160, 196, 202, 208, 214, 220, 226]  # Dark red to bright yellow
    non_space_chars = [c for c in text1 if c != ' ']
    color_step = len(fire_colors) / len(non_space_chars)
    char_index = 0
    for char in text1:
        if char == ' ':
            content += " "
        else:
            color_index = min(int(char_index * color_step), len(fire_colors) - 1)
            color = fire_colors[color_index]
            content += f"\033[38;5;{color}m{char}\033[0m"
            char_index += 1
    content += "\n"
    
    # Ocean gradient using xterm256 colors (dark blue -> cyan -> light blue)
    text2 = "Deep ocean to sky gradient"  
    ocean_colors = [17, 18, 19, 20, 21, 27, 33, 39, 45, 51, 87, 123, 159, 195]  # Dark blue to cyan
    non_space_chars = [c for c in text2 if c != ' ']
    color_step = len(ocean_colors) / len(non_space_chars)
    char_index = 0
    for char in text2:
        if char == ' ':
            content += " "
        else:
            color_index = min(int(char_index * color_step), len(ocean_colors) - 1)
            color = ocean_colors[color_index]
            content += f"\033[38;5;{color}m{char}\033[0m"
            char_index += 1
    content += "\n"
    
    # Purple to pink gradient using xterm256 colors
    text3 = "Purple dreams to pink reality"
    purple_colors = [54, 55, 91, 127, 163, 199, 205, 211, 217, 223]  # Purple to pink
    non_space_chars = [c for c in text3 if c != ' ']
    color_step = len(purple_colors) / len(non_space_chars)
    char_index = 0
    for char in text3:
        if char == ' ':
            content += " "
        else:
            color_index = min(int(char_index * color_step), len(purple_colors) - 1)
            color = purple_colors[color_index]
            content += f"\033[38;5;{color}m{char}\033[0m"
            char_index += 1
    content += "\n\n"

    return content


XTERM256_TEST = get_xterm256_handler_string()