def truecolor_handler(telnet):
    """Test 24-bit truecolor (RGB) support"""
    
    content = b"=== TrueColor (24-bit RGB) Test ===\n\n"
    
    # RGB spectrum test
    content += b"RGB Spectrum:\n"
    for r in range(0, 256, 32):
        for g in range(0, 256, 32):
            for b in range(0, 256, 64):
                content += f"\033[38;2;{r};{g};{b}m\u2588\033[0m".encode()
            content += b" "
        content += b"\n"
    content += b"\n"
    
    # Red gradient
    content += b"Red Gradient:\n"
    for i in range(0, 256, 4):
        content += f"\033[38;2;{i};0;0m\u2588\033[0m".encode()
    content += b"\n"
    
    # Green gradient
    content += b"Green Gradient:\n"
    for i in range(0, 256, 4):
        content += f"\033[38;2;0;{i};0m\u2588\033[0m".encode()
    content += b"\n"
    
    # Blue gradient
    content += b"Blue Gradient:\n"
    for i in range(0, 256, 4):
        content += f"\033[38;2;0;0;{i}m\u2588\033[0m".encode()
    content += b"\n\n"
    
    # Background truecolor test
    content += b"Background TrueColor:\n"
    colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255)]
    for r, g, b in colors:
        content += f"\033[48;2;{r};{g};{b}m\033[38;2;0;0;0m RGB({r},{g},{b}) \033[0m ".encode()
    content += b"\n\n"
    
    # Rainbow gradient
    content += b"Rainbow Gradient:\n"
    for i in range(60):
        # Create a rainbow using HSV to RGB conversion
        hue = i * 6  # 0-360 degrees
        if hue < 60:
            r, g, b = 255, int(hue * 255 / 60), 0
        elif hue < 120:
            r, g, b = int((120 - hue) * 255 / 60), 255, 0
        elif hue < 180:
            r, g, b = 0, 255, int((hue - 120) * 255 / 60)
        elif hue < 240:
            r, g, b = 0, int((240 - hue) * 255 / 60), 255
        elif hue < 300:
            r, g, b = int((hue - 240) * 255 / 60), 0, 255
        else:
            r, g, b = 255, 0, int((360 - hue) * 255 / 60)
        
        content += f"\033[38;2;{r};{g};{b}m\u2588\033[0m".encode()
    content += b"\n\n"
    
    # Gray gradients with different step sizes (limited to 70 chars)
    content += b"TrueColor Gray Gradients:\n"
    for step in [1, 2, 4, 8]:
        content += f"Step {step}: ".encode()
        char_count = 8  # "Step X: " is 8 chars
        for i in range(0, 256, step):
            if char_count >= 70:  # Stop at 70 chars to stay under 80
                break
            content += f"\033[38;2;{i};{i};{i}m\u2588\033[0m".encode()
            char_count += 1
        content += b"\n"
    content += b"\n"
    
    # TrueColor gradient text examples
    content += b"TrueColor Gradient Text:\n\n"
    
    # Fire gradient text
    text1 = "TrueColor fire gradient text"
    for i, char in enumerate(text1):
        if char == ' ':
            content += b" "
        else:
            # Fire gradient: red -> orange -> yellow
            progress = i / (len(text1) - 1)
            if progress < 0.5:
                # Red to orange
                r = 255
                g = int(progress * 2 * 165)  # 0 to 165
                b = 0
            else:
                # Orange to yellow
                r = 255
                g = int(165 + (progress - 0.5) * 2 * 90)  # 165 to 255
                b = 0
            content += f"\033[38;2;{r};{g};{b}m{char}\033[0m".encode()
    content += b"\n"
    
    # Ocean gradient text
    text2 = "Deep ocean to sky gradient"
    for i, char in enumerate(text2):
        if char == ' ':
            content += b" "
        else:
            # Ocean gradient: dark blue -> cyan -> light blue
            progress = i / (len(text2) - 1)
            if progress < 0.33:
                # Dark blue to blue
                r = int(progress * 3 * 30)  # 0 to 30
                g = int(progress * 3 * 100)  # 0 to 100
                b = int(139 + progress * 3 * 75)  # 139 to 214
            elif progress < 0.66:
                # Blue to cyan
                p = (progress - 0.33) * 3
                r = int(30 + p * 30)  # 30 to 60
                g = int(100 + p * 155)  # 100 to 255
                b = int(214 + p * 41)  # 214 to 255
            else:
                # Cyan to light blue
                p = (progress - 0.66) * 3
                r = int(60 + p * 75)  # 60 to 135
                g = int(255 - p * 49)  # 255 to 206
                b = 255
            content += f"\033[38;2;{r};{g};{b}m{char}\033[0m".encode()
    content += b"\n"
    
    # Purple to pink gradient
    text3 = "Purple dreams to pink reality"
    for i, char in enumerate(text3):
        if char == ' ':
            content += b" "
        else:
            progress = i / (len(text3) - 1)
            # Purple to pink gradient
            r = int(128 + progress * 127)  # 128 to 255
            g = int(0 + progress * 192)    # 0 to 192
            b = int(128 + progress * 75)   # 128 to 203
            content += f"\033[38;2;{r};{g};{b}m{char}\033[0m".encode()
    content += b"\n\n"
    
    telnet.send_text(content)