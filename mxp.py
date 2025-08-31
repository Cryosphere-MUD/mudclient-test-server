import string
import struct
from telnet import TelnetState
from telnetconstants import IAC, WILL, MXP

MXP_TEST = bytes([IAC, WILL, MXP]) + b"""\033[5z

Hello welcome to MXP! We are in OPEN Mode

&lt; that should be a less-than sign
<bold>This should be in bold</bold>
<italic>This should be in italic</italic>
<underline>This should be underlined</underline>
<color fore="f0f000">This should be yellow</color>
<send href="zap me">this should NOT be a link</a>

\033[6z

Now we are in SECURE Mode

&lt; that should be a less-than sign
<bold>This should be in bold</bold>
<send href="zap me">this should be a link</a>

\033[7z

Now we are in LOCKED Mode

&lt; that should be an HTML entity code
<bold>it should just be displaying the tag</bold>
<send href="zap me">this should definitely not be a link</a>

"""

