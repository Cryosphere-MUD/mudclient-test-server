

ANSI_TEST = """
\033[1m bold \033[0m normal
\033[1m bold \033[m normal

\033[0;31mnormal red      \033[1;31mbold red
\033[0;32mnormal green    \033[1;32mbold green
\033[0;33mnormal yellow   \033[1;33mbold yellow
\033[0;34mnormal blue     \033[1;34mbold blue
\033[0;35mnormal magneta  \033[1;35mbold magenta
\033[0;36mnormal cyan     \033[1;36mbold cyan
\033[0;37mnormal white    \033[1;37mbold white

\033[m normal

\033[3m italics\033[m    \033[4munderlined\033[m
\033[5m blinking\033[m   \033[7minverse\033[m
\033[8m hidden\033[m     \033[9mstrikethrough\033[m
\033[20m fraktur\033[m   \033[21mdouble underline\033[m and \033[53moverline\033[m

""".encode()

try:
    UTF8_TEST = open("utf8-test.txt", "rb").read()
except FileNotFoundError:
    UTF8_TEST = b"UTF-8 test file not found"

# MCCP2 test data
MCCP2_TEST = (b"""1. Note that this test is a unilateral negotiation, i.e the server\r\n2. does not wait for the response before starting compression.\r\n""" + 
              bytes([IAC, WILL, TELOPT_MCCP2]) + bytes([IAC, SB, TELOPT_MCCP2]) + bytes([IAC, SE]) + 
              zlib.compress(b"3. This data's been compressed! Now we're going to finish the compression and carry on.\r\n4. The next line should be line 5.\r\n") +
              b"5. This is line five.\r\n")
