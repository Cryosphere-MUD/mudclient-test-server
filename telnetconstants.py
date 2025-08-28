# Telnet protocol constants
IAC = 255  # Interpret As Command
WILL = 251
WONT = 252
DO = 253
DONT = 254
SB = 250   # Sub-negotiation begin
SE = 240   # Sub-negotiation end

# Telnet options (RFC + common MUD extensions)
BINARY = 0        # 8-bit data path
ECHO = 1          # Echo
RCP = 2           # Prepare to reconnect
SGA = 3           # Suppress Go Ahead
NAMS = 4          # Approximate message size
STATUS = 5        # Give status
TM = 6            # Timing mark
RCTE = 7          # Remote controlled transmission and echo
NAOL = 8          # Negotiate about output line width
NAOP = 9          # Negotiate about output page size
NAOCRD = 10       # Negotiate about CR disposition
NAOHTS = 11       # Negotiate about horizontal tabstops
NAOHTD = 12       # Negotiate about horizontal tab disposition
NAOFFD = 13       # Negotiate about formfeed disposition
NAOVTS = 14       # Negotiate about vertical tab stops
NAOVTD = 15       # Negotiate about vertical tab disposition
NAOLFD = 16       # Negotiate about output LF disposition
XASCII = 17       # Extended ASCII character set
LOGOUT = 18       # Force logout
BM = 19           # Byte macro
DET = 20          # Data entry terminal
SUPDUP = 21       # SUPDUP protocol
SUPDUPOUTPUT = 22 # SUPDUP output
SNDLOC = 23       # Send location
TTYPE = 24        # Terminal type
EOR = 25          # End of Record
TUID = 26         # TACACS user identification
OUTMRK = 27       # Output marking
TTYLOC = 28       # Terminal location number
REGIME_3270 = 29  # 3270 regime
X3PAD = 30        # X.3 PAD
NAWS = 31         # Window size
TSPEED = 32       # Terminal speed
LFLOW = 33        # Remote flow control
LINEMODE = 34     # Linemode option
XDISPLOC = 35     # X Display Location
OLD_ENVIRON = 36  # Old - Environment variables
AUTHENTICATION = 37  # Authenticate
ENCRYPT = 38      # Encryption option
NEW_ENVIRON = 39  # New - Environment variables
EXOPL = 255       # Extended-options-list

# Common MUD extensions
MSDP = 69            # Mud Server Data Protocol
MSSP = 70            # Mud Server Status Protocol
TELOPT_MCCP1 = 85    # Mud Client Compression Protocol (legacy)
TELOPT_MCCP2 = 86    # Mud Client Compression Protocol v2
TELOPT_MCCP3 = 87    # Mud Client Compression Protocol v3
TELOPT_MCCP4 = 88    # Mud Client Compression Protocol v4 (draft)
MSP = 90             # Mud Sound Protocol
MXP = 91             # Mud eXtension Protocol

SYNC = 96            # Cryosphere's SYNC protocol

GMCP = 201           # Generic MUD Communication Protocol

MPLEX = 112          # Cryosphere's MPLEX protocol

def option_name(option):
    names = {
        BINARY: "BINARY",
        ECHO: "ECHO",
        RCP: "RCP",
        SGA: "SGA",
        NAMS: "NAMS",
        STATUS: "STATUS",
        TM: "TM",
        RCTE: "RCTE",
        NAOL: "NAOL",
        NAOP: "NAOP",
        NAOCRD: "NAOCRD",
        NAOHTS: "NAOHTS",
        NAOHTD: "NAOHTD",
        NAOFFD: "NAOFFD",
        NAOVTS: "NAOVTS",
        NAOVTD: "NAOVTD",
        NAOLFD: "NAOLFD",
        XASCII: "XASCII",
        LOGOUT: "LOGOUT",
        BM: "BM",
        DET: "DET",
        SUPDUP: "SUPDUP",
        SUPDUPOUTPUT: "SUPDUPOUTPUT",
        SNDLOC: "SNDLOC",
        TTYPE: "TTYPE",
        EOR: "EOR",
        TUID: "TUID",
        OUTMRK: "OUTMRK",
        TTYLOC: "TTYLOC",
        REGIME_3270: "3270REGIME",
        X3PAD: "X3PAD",
        NAWS: "NAWS",
        TSPEED: "TSPEED",
        LFLOW: "LFLOW",
        LINEMODE: "LINEMODE",
        XDISPLOC: "XDISPLOC",
        OLD_ENVIRON: "OLD_ENVIRON",
        AUTHENTICATION: "AUTHENTICATION",
        ENCRYPT: "ENCRYPT",
        NEW_ENVIRON: "NEW_ENVIRON",
        EXOPL: "EXOPL",

        # MUD extensions
        MSSP: "MSSP",
        TELOPT_MCCP1: "MCCP1",
        TELOPT_MCCP2: "MCCP2",
        TELOPT_MCCP3: "MCCP3",
        TELOPT_MCCP4: "MCCP4",
        GMCP: "GMCP",
        MSDP: "MSDP",
        MSP: "MSP",
        MXP: "MXP",

        SYNC: "SYNC",
        MPLEX: "MPLEX",
    }
    return names.get(option, f"[{option}]")


def command_name(command):
        names = {
                IAC: "IAC",
                WILL: "WILL",
                WONT: "WONT",
                DO: "DO",
                DONT: "DONT",
                SB: "SB",
                SE: "SE",
        }
        return names.get(command, f"[{command}]")

