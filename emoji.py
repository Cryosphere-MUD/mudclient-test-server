def get_emoji_tests():
    """Generate comprehensive emoji tests"""
    
    # God knows what alignment these are supposed to be. Despite their
    # origin, emoji don't have a definitive integral cjkwidth.  This
    # grid is aligned as if they had a cjkwidth of 1, which is probably
    # wrong but every other option would also be wrong.  The lesson here
    # is don't use emojis where alignment matters.
    content = "    0 1 2 3 4 5 6 7 8 9 a b c d e f\n"
    content += "  ╭────────────────────────────────\n"
    
    # Generate emoji grid (Unicode page U+1F400 to U+1F4FF)
    for row in range(16):
        content += f"{row:x} │ "
        for col in range(16):
            emoji_code = 0x1F400 + row * 16 + col
            if emoji_code <= 0x1F4FF:
                try:
                    emoji_char = chr(emoji_code)
                    content += f"{emoji_char} "
                except (ValueError, UnicodeEncodeError):
                    content += "  "
            else:
                content += "  "
        content += "\n"
    
    return content


EMOJI_TEST = get_emoji_tests()