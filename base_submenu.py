"""Base submenu system to eliminate code duplication in submenu implementations."""

class BaseSubmenu:
    """Base class for all submenu handlers to eliminate code duplication."""
    
    def __init__(self, title, options, special_handling=None):
        """
        Initialize submenu with title and options.
        
        Args:
            title: The submenu title to display
            options: Dict of {option_key: (description, handler)}
            special_handling: Optional dict of {option_key: special_handler_func}
        """
        self.title = title
        self.options = options
        self.special_handling = special_handling or {}
        
    def create_submenu_text(self):
        """Create formatted submenu text."""
        menu_text = f"\n{self.title}\n" + "=" * len(self.title) + "\n"
        for key, (desc, _) in self.options.items():
            menu_text += f"  {key:<15} - {desc}\n"
        menu_text += "\nType 'back' to return to main menu, or choose an option: "
        return menu_text.encode()
    
    def handle_option(self, option, telnet):
        """Handle a selected option. Returns True if should continue loop."""
        if option == "back":
            return False
        
        if option in self.options:
            # Check for special handling first
            if option in self.special_handling:
                self.special_handling[option](option, telnet)
                return True
            
            # Normal handling
            _, handler = self.options[option]
            handler(telnet)
            return False  # Exit submenu after normal test
        
        if option:  # Only show error if they actually typed something
            telnet.send_text(f"Unknown option: {option}\n".encode())
        
        return True  # Continue loop
    
    def run(self, telnet):
        """Main submenu loop."""
        while True:
            telnet.send_text(self.create_submenu_text())
            decoded = telnet.readline()
            option = decoded.split()[0] if decoded.split() else ""
            
            if not self.handle_option(option, telnet):
                break


class CompressionSubmenu(BaseSubmenu):
    """Specialized submenu for compression tests with session tracking."""
    
    def __init__(self, title, options):
        # Compression groups - tests within same group are compatible
        self.compression_groups = {
            "mccp2": ["mccp2", "mccp2_slow"],  
            "mccp4_zstd": ["mccp4"],           
            "mccp4_deflate": ["mccp4_deflate"] 
        }
        super().__init__(title, options)
    
    def init_compression_state(self, telnet):
        """Compression state is now initialized in TelnetState constructor."""
        pass
    
    def handle_option(self, option, telnet):
        """Handle compression option with compatibility checking."""
        if option == "back":
            return False
        
        if option in self.options:
            self.init_compression_state(telnet)
            
            # Find which group this option belongs to
            option_group = None
            for group_name, group_options in self.compression_groups.items():
                if option in group_options:
                    option_group = group_name
                    break
            
            # Check if we can run this test
            if telnet.compression_used is None:
                # First compression test - allow it
                telnet.compression_used = option_group
            elif telnet.compression_used == option_group:
                # Same group - allow it
                pass
            else:
                # Different group - require reconnection
                telnet.send_text(f"\nCannot mix different compression protocols in the same session.\n".encode())
                telnet.send_text(f"You've already used: {telnet.compression_used}\n".encode())
                telnet.send_text(f"To test {option_group}, please reconnect and try again.\n".encode())
                return True
            
            # Run the test
            _, handler = self.options[option]
            try:
                handler(telnet)
                if telnet.compression_used == option_group:
                    # Same group - can run more
                    telnet.send_text(b"\nTest completed. You can run other tests in the same group.\n")
                else:
                    # Different group - warn about reconnection
                    telnet.send_text(b"\nTest completed. Reconnect to test different compression protocols.\n")
            except Exception as e:
                telnet.send_text(f"\nTest failed: {e}\n".encode())
            
            return True  # Stay in compression submenu
        
        if option:
            telnet.send_text(f"Unknown option: {option}\n".encode())
        
        return True