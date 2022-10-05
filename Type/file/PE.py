
import os, sys
sys.path.append(os.path.dirname(__file__) + "/../../")

from Utils.Converter import CONVERTER


class PE:
    def __init__(self, fname, raw):
        self.cvt    = CONVERTER('little')
        self.fSize  = len(raw)

        # // DOS
        self._IMAGE_DOS_HEADER(raw[ : 0x40 ])
        # self._IMAGE_DOS_STUB        = raw[ 0x40 : self.e_lfanew ]
        base = self.e_lfanew

        # // PE Header
        sizeOfOptionalHeader   = self.cvt.bytes2int(raw[ base + 0x14 : base + 0x16 ])
        self._IMAGE_NT_HEADERS(raw[ base : base + sizeOfOptionalHeader + 0x18 ])
        base += sizeOfOptionalHeader + 0x18

        # // Section Header
        self._IMAGE_SECTION_HEADER(raw[ base : base + 0x28 * self.numberOfSections ])

        # // Section

    def _IMAGE_DOS_HEADER(self, data):
        e_magic         = data[0x00:0x02]
        self.e_cblp     = self.cvt.bytes2int(data[0x02:0x04])
        self.e_cp       = self.cvt.bytes2int(data[0x04:0x06])
        self.e_crlc     = self.cvt.bytes2int(data[0x06:0x08])
        self.e_cparhdr  = self.cvt.bytes2int(data[0x08:0x0A])
        self.e_minalloc = self.cvt.bytes2int(data[0x0A:0x0C])
        self.e_maxalloc = self.cvt.bytes2int(data[0x0C:0x0E])
        self.e_ss       = self.cvt.bytes2int(data[0x0E:0x10])
        self.e_sp       = self.cvt.bytes2int(data[0x10:0x12])
        self.e_csum     = self.cvt.bytes2int(data[0x12:0x14])
        self.e_ip       = self.cvt.bytes2int(data[0x14:0x16])
        self.e_cs       = self.cvt.bytes2int(data[0x16:0x18])
        self.e_lfarlc   = self.cvt.bytes2int(data[0x18:0x1A])
        self.e_ovno     = self.cvt.bytes2int(data[0x1A:0x1C])
        self.e_res      = self.cvt.bytes2int(data[0x1C:0x24])
        self.e_oemid    = self.cvt.bytes2int(data[0x24:0x26])
        self.e_oeminfo  = self.cvt.bytes2int(data[0x26:0x28])
        self.e_res2     = self.cvt.bytes2int(data[0x28:0x3C])
        self.e_lfanew   = self.cvt.bytes2int(data[0x3C:0x40])

        if e_magic != b'MZ': exit(-1)

    def _IMAGE_NT_HEADERS(self, data):
        signature   = data[ 0x00 : 0x04 ]

        # fileHeader                = data[ 0x04 : 0x18 ]
        self.machine                = self.cvt.bytes2int(data[ 0x04 : 0x06 ])
        self.numberOfSections       = self.cvt.bytes2int(data[ 0x06 : 0x08 ])
        self.timeDateStemp          = self.cvt.bytes2int(data[ 0x08 : 0x0C ])
        self.pointerToSymbolTable   = self.cvt.bytes2int(data[ 0x0C : 0x10 ])
        self.numberOfSymbols        = self.cvt.bytes2int(data[ 0x10 : 0x14 ])
        self.sizeOfOptionalHeader   = self.cvt.bytes2int(data[ 0x14 : 0x16 ])
        self.characteristics        = self.cvt.bytes2int(data[ 0x16 : 0x18 ])

        optionalHeader  = data[ 0x18 : 0x18 + self.sizeOfOptionalHeader ]

    def _IMAGE_SECTION_HEADER(self, data):
        # headerNames = [ str(data[i * 0x28: i * 0x28 + 0x8], 'utf-8').rstrip('\x00') for i in range(self.numberOfSections) ]
        self.headerNames = [ data[i * 0x28: i * 0x28 + 0x8] for i in range(self.numberOfSections) ]

        if   [ s for s in self.headerNames if b'UPX' in s ]:
            self.packer = 'UPX'
        elif [ s for s in self.headerNames if b'MEW' in s ]:
            self.packer = 'MEW'
        # elif [ s for s in self.headerNames if b'.adata' in s ]:
        #     self.packer = 'Aspack/Armadillo'
        else:
            self.packer = b"Undetected"
            filteredHeaderNames = [ item.rstrip(b'\x00') for item in self.headerNames if item not in [
                b'.text\x00\x00\x00',

                b'.data\x00\x00\x00',
                b'.bdata\x00\x00',
                b'.cdata\x00\x00',
                b'.fdata\x00\x00',
                b'.kdata\x00\x00',
                b'.rdata\x00\x00',
                b'.xdata\x00\x00',

                b'.rsrc\x00\x00\x00'
            ]]

            if filteredHeaderNames:
                self.packer += b'/' + b' | '.join(filteredHeaderNames)                


if __name__ == "__main__":
    import os

    files = ['/data/test1.exe', '/data/test2.exe']
    for f in files:
        with open(f, 'rb') as r:
            PE(f, r.read())

# https://yum-history.tistory.com/266
# https://thejn.tistory.com/93
# https://www.hexacorn.com/blog/2016/12/15/pe-section-names-re-visited/
