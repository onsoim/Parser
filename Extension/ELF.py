# http://www.skyfree.org/linux/references/ELF_Format.pdf
class ELF:
    def __init__(self, raw):
        self.raw        = raw
        self.elf_header = raw[ : 0x34 ]
        self.endian     = 'little'
        self.APIs       = []
        self.parse()

    def parse(self):
        self.parseElfHeader()

    def parseElfHeader(self):
        e_ident     = self.elf_header[ : 0x10 ]  
        ei_magic        = e_ident[ : 0x4 ]
        ei_class        = e_ident[ 0x4 : 0x5 ][0]
        ei_data         = e_ident[ 0x5 : 0x6 ][0]
        ei_version      = e_ident[ 0x6 : 0x7 ][0]
        ei_osabi        = e_ident[ 0x7 : 0x8 ][0]
        ei_abiversion   = e_ident[ 0x8 : 0x9 ][0]
        ei_pad          = e_ident[ 0x9 : ]
        
        e_type      = self.elf_header[ 0x10 : 0x12 ]
        e_machine   = self.elf_header[ 0x12 : 0x14 ]
        e_version   = self.elf_header[ 0x14 : 0x18 ]
        e_entry     = self.elf_header[ 0x18 : 0x1C ]
        e_phoff     = self.elf_header[ 0x1C : 0x20 ]
        e_shoff     = self.elf_header[ 0x20 : 0x24 ]
        e_flags     = self.elf_header[ 0x24 : 0x28 ]
        e_ehsize    = self.elf_header[ 0x28 : 0x2A ]
        e_phentsize = self.elf_header[ 0x2A : 0x2C ]
        e_phnum     = self.elf_header[ 0x2C : 0x2E ]
        e_shentsize = self.elf_header[ 0x2E : 0x30 ]
        e_shnum     = self.elf_header[ 0x30 : 0x32 ]
        e_shstrndx  = self.elf_header[ 0x32 : ]

        if ei_data == 2: self.endian = "big" # {"little endian": 1, "big endian": 2}
