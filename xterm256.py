def xterm256_handler(telnet):
    """Test xterm 256-color palette (foreground and background)"""
    
    content = b"=== XTerm 256-Color Test ===\r\n\r\n"
    
    # Standard colors (0-15)
    content += b"Standard Colors (0-15):\r\n"
    for i in range(16):
        if i == 8:
            content += b"\r\n"
        content += f"\033[38;5;{i}m{i:3d}\033[0m ".encode()
    content += b"\r\n\r\n"
    
    # 216 color cube (16-231)
    content += b"216-Color Cube (16-231):\r\n"
    for r in range(6):
        for g in range(6):
            for b in range(6):
                color = 16 + (r * 36) + (g * 6) + b
                content += f"\033[38;5;{color}m\u2588\033[0m".encode()
            content += b" "
        content += b"\r\n"
    content += b"\r\n"
    
    # Grayscale ramp (232-255)
    content += b"Grayscale Ramp (232-255):\r\n"
    for i in range(232, 256):
        content += f"\033[38;5;{i}m\u2588\033[0m".encode()
    content += b"\r\n\r\n"
    
    # Background color test
    content += b"Background Colors Sample:\r\n"
    test_colors = [1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14]
    for color in test_colors:
        content += f"\033[48;5;{color}m\033[38;5;15m {color:3d} \033[0m ".encode()
    content += b"\r\n\r\n"
    
    # Color gradient
    content += b"Color Gradient:\r\n"
    for i in range(0, 256, 4):
        content += f"\033[48;5;{i}m \033[0m".encode()
    content += b"\r\n\r\n"
    
    # Gradient text examples
    content += b"Gradient Text Examples:\r\n\r\n"
    
    # Fire gradient using xterm256 colors (red -> orange -> yellow)
    text1 = "XTerm256 fire gradient text"
    fire_colors = [52, 88, 124, 160, 196, 202, 208, 214, 220, 226]  # Dark red to bright yellow
    non_space_chars = [c for c in text1 if c != ' ']
    color_step = len(fire_colors) / len(non_space_chars)
    char_index = 0
    for char in text1:
        if char == ' ':
            content += b" "
        else:
            color_index = min(int(char_index * color_step), len(fire_colors) - 1)
            color = fire_colors[color_index]
            content += f"\033[38;5;{color}m{char}\033[0m".encode()
            char_index += 1
    content += b"\r\n"
    
    # Ocean gradient using xterm256 colors (dark blue -> cyan -> light blue)
    text2 = "Deep ocean to sky gradient"  
    ocean_colors = [17, 18, 19, 20, 21, 27, 33, 39, 45, 51, 87, 123, 159, 195]  # Dark blue to cyan
    non_space_chars = [c for c in text2 if c != ' ']
    color_step = len(ocean_colors) / len(non_space_chars)
    char_index = 0
    for char in text2:
        if char == ' ':
            content += b" "
        else:
            color_index = min(int(char_index * color_step), len(ocean_colors) - 1)
            color = ocean_colors[color_index]
            content += f"\033[38;5;{color}m{char}\033[0m".encode()
            char_index += 1
    content += b"\r\n"
    
    # Purple to pink gradient using xterm256 colors
    text3 = "Purple dreams to pink reality"
    purple_colors = [54, 55, 91, 127, 163, 199, 205, 211, 217, 223]  # Purple to pink
    non_space_chars = [c for c in text3 if c != ' ']
    color_step = len(purple_colors) / len(non_space_chars)
    char_index = 0
    for char in text3:
        if char == ' ':
            content += b" "
        else:
            color_index = min(int(char_index * color_step), len(purple_colors) - 1)
            color = purple_colors[color_index]
            content += f"\033[38;5;{color}m{char}\033[0m".encode()
            char_index += 1
    content += b"\r\n\r\n"
    
    telnet.sendall(content)