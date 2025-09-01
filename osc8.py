
def get_link_tests():
    """Generate link support tests"""
    content = "\n"
    
    # Colors for link tests - same as UTF-8 section
    label_color = "\033[38;5;238m"  # Dark gray for labels
    content_color = "\033[38;5;220m"  # Golden yellow for content
    reset = "\033[0m"

    # Regular text URL (not a link)
    content += f"{label_color}NOT a link - {reset}https://www.mudvault.org\n"
    
    # OSC8 hyperlink - only the URL is clickable
    content += f"{label_color}Https link - {reset}\033]8;;https://www.mudvault.org\007https://www.mudvault.org\033]8;;\007\n"
    
    # Another OSC8 link with display text - only the display text is clickable
    content += f"{label_color}Https link - {reset}Check out the \033]8;;https://www.mudvault.org\007MUD Client Test Server!\033]8;;\007\n"
    
    # Send links (MUD command links) - only quoted text is gold and clickable
    content += f"{label_color}Send links - {reset}Want more? \033]8;;send:say please\007{content_color}'say please'{reset}\033]8;;\007 \033]8;;send:say no thanks\007{content_color}'say no thanks'{reset}\033]8;;\007.\n"
    
    # Prompt link - only quoted text is gold and clickable
    content += f"{label_color}Prompt link- {reset}How many do you want? \033]8;;send:buy \007{content_color}'buy <quantity>'{reset}\033]8;;\007\n\n"
    
    return content

OSC8_TEST = get_link_tests()