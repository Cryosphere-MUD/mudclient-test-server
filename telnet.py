from telnetconstants import IAC, WILL, DO, DONT, WONT, SE, SB

class TelnetState:
        def __init__(self, sock):
                self.sock = sock
                self.mode = self.handle_data
                self.subneg_option = None
                self.subneg_str = bytes()
                self.data_str = bytes()
                self.will = {}
                self.wont = {}
                self.do = {}
                self.dont = {}
                self.subneg_handlers = {}
                self.neg_handler = None             
                self.compression_used = None
                self.lineending = None
                self.dataline = None

        def reset(self):
                self.subneg_handlers = {}
                self.neg_handler = None

        def send_bytes(self, data):
                if isinstance(data, str):
                        data = data.encode()
                view = memoryview(data)
                while view:
                        n = self.sock.send(view)
                        view = view[n:]

        def send_text(self, data):
                if isinstance(data, str):
                        data = data.encode()
                view = memoryview(data)
                while view:
                        n = self.sock.send(view)
                        view = view[n:]

        def readline(self):
                while True:
                        data = self.sock.recv(1)
                        self.process(data)
                        if line := self.dataline:
                                self.dataline = None
                                return line.decode(errors="ignore")
                        

        def process(self, octet):
                if isinstance(octet, bytes):
                        for ch in octet:
                                self.mode(ch)
                else:
                        self.mode(octet)

        def handle_dataline(self, line):
                self.dataline = line

        def handle_databyte(self, octet):
                if self.subneg_option:
                        self.subneg_str += bytes([octet])
                else:
                        if self.lineending is None and octet in (10, 13):
                                self.lineending = octet

                        if octet == self.lineending:
                                self.handle_dataline(self.data_str)
                                self.data_str = bytes()
                        
                        if octet in (10, 13):
                                return

                        self.data_str += bytes([octet])

        def handle_data(self, octet):
                if octet == IAC:
                        self.mode = self.handle_iac
                else:
                        self.handle_databyte(octet)

        def handle_iac(self, octet):
                if octet == IAC:
                        handle_databyte(octet)
                        self.mode = self.handle_data
                elif octet == WILL:
                        self.mode = self.handle_will
                elif octet == WONT:
                        self.mode = self.handle_wont
                elif octet == DO:
                        self.mode = self.handle_do
                elif octet == DONT:
                        self.mode = self.handle_dont
                elif octet == SB:
                        self.mode = self.handle_sb
                elif octet == SE:
                        self.handle_subneg(self.subneg_option, self.subneg_str)
                        self.subneg_str = bytes()
                        self.subneg_option = None
                        self.mode = self.handle_data
                else: # unrecognised (for now), go back to data state
                        self.mode = self.handle_data

        def handle_subneg(self, option, data):
                if option in self.subneg_handlers:
                        self.subneg_handlers[option](data)

        def handle_sb(self, octet):
                self.subneg_str = bytes()
                self.subneg_option = octet
                self.mode = self.handle_data

        def handle_will(self, octet):
                if self.neg_handler:
                        self.neg_handler(WILL, octet)
                self.will[octet] = True
                if octet in self.wont: del self.wont[octet]
                self.mode = self.handle_data

        def handle_wont(self, octet):
                if self.neg_handler:
                        self.neg_handler(WONT, octet)
                self.wont[octet] = True
                if octet in self.will: del self.will[octet]
                self.mode = self.handle_data

        def handle_do(self, octet):
                if self.neg_handler:
                        self.neg_handler(DO, octet)
                self.do[octet] = True
                if octet in self.dont: del self.dont[octet]
                self.mode = self.handle_data

        def handle_dont(self, octet):
                if self.neg_handler:
                        self.neg_handler(DONT, octet)
                self.dont[octet] = True
                if octet in self.do: del self.do[octet]
                self.mode = self.handle_data
