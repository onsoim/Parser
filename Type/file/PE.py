
import os, sys
sys.path.append(os.path.dirname(__file__) + "/../../")

from Utils.Converter import CONVERTER


class PE:
    def __init__(self, fname, raw):
        self.cvt = CONVERTER('little')

        # // DOS
        self._IMAGE_DOS_HEADER(raw[ : 0x40 ])
        # self._IMAGE_DOS_STUB        = raw[ 0x40 : self.e_lfanew ]
        base = self.e_lfanew

        # // PE Header
        sizeOfOptionalHeader   = self.cvt.bytes2int(raw[ base + 0x14 : base + 0x16 ])
        self._IMAGE_NT_HEADERS(raw[ base : base + sizeOfOptionalHeader + 0x18 ])
        base += sizeOfOptionalHeader + 0x18

        # // Section Header
        self._IMAGE_SECTION_HEADER  = raw[ base : base + 0x28 * self.numberOfSections ]

        # // Section

    def _IMAGE_DOS_HEADER(self, data):
        e_magic         = data[0x00:0x02]
        self.e_cblp     = data[0x02:0x04]
        self.e_cp       = data[0x04:0x06]
        self.e_crlc     = data[0x06:0x08]
        self.e_cparhdr  = data[0x08:0x0A]
        self.e_minalloc = data[0x0A:0x0C]
        self.e_maxalloc = data[0x0C:0x0E]
        self.e_ss       = data[0x0E:0x10]
        self.e_sp       = data[0x10:0x12]
        self.e_csum     = data[0x12:0x14]
        self.e_ip       = data[0x14:0x16]
        self.e_cs       = data[0x16:0x18]
        self.e_lfarlc   = data[0x18:0x1A]
        self.e_ovno     = data[0x1A:0x1C]
        self.e_res      = data[0x1C:0x24]
        self.e_oemid    = data[0x24:0x26]
        self.e_oeminfo  = data[0x26:0x28]
        self.e_res2     = data[0x28:0x3C]
        self.e_lfanew   = self.cvt.bytes2int(data[0x3C:0x40])

        if e_magic != b'MZ': exit(-1)

    def _IMAGE_NT_HEADERS(self, data):
        signature   = data[ 0x00 : 0x04 ]

        # fileHeader                = data[ 0x04 : 0x18 ]
        self.machine                = data[ 0x04 : 0x06 ]
        self.numberOfSections       = self.cvt.bytes2int(data[ 0x06 : 0x08 ])
        self.timeDateStemp          = data[ 0x08 : 0x0C ]
        self.pointerToSymbolTable   = data[ 0x0C : 0x10 ]
        self.numberOfSymbols        = data[ 0x10 : 0x14 ]
        self.sizeOfOptionalHeader   = self.cvt.bytes2int(data[ 0x14 : 0x16 ])
        self.characteristics        = data[ 0x16 : 0x18 ]

        optionalHeader  = data[ 0x18 : 0x18 + self.sizeOfOptionalHeader ]


if __name__ == "__main__":
    import os

    files = ['/data/test1.exe', '/data/test2.exe']
    for f in files:
        with open(f, 'rb') as r:
            PE(f, r.read())

# https://yum-history.tistory.com/266
# https://thejn.tistory.com/93
