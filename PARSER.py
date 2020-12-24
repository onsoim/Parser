from Extension.AR import *

class PARSER:
    def __init__(self, raw):
        self.raw = raw
        self.signature = self.checkSignature(raw[ : 0x8 ])
        self.handler = globals()[self.signature](self.raw)

    def checkSignature(self, sig):
        if (sig == b'!<arch>\n'):
            return 'AR'
