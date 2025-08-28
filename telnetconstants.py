# Telnet protocol constants
IAC = 255  # Interpret As Command
WILL = 251
WONT = 252
DO = 253
DONT = 254
SB = 250   # Sub-negotiation begin
SE = 240   # Sub-negotiation end

# Telnet options
TTYPE = 24    # Terminal type
NAWS = 31     # Negotiate About Window Size
ECHO = 1      # Echo
SGA = 3       # Suppress Go Ahead
EOR = 25      # End of Record
GMCP = 201    # Generic MUD Communication Protocol
TELOPT_MCCP2 = 86  # MCCP2 compression

