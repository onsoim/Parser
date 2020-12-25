import Utils.convert as converter

class ELF:
    def __init__(self, raw):
        self.raw        = raw
        self.endian     = 'little'
        self.symtab     = b''
        self.APIs       = []

        self.parse()


    def parse(self):
        self.parseElfHeader()
        self.parseSectionHeader()


    def parseElfHeader(self):
        elf_header = self.raw[ : 0x34 ]

        e_ident         = elf_header[ : 0x10 ]  
        ei_magic        = e_ident[ : 0x4 ]
        ei_class        = e_ident[ 0x4 : 0x5 ][0]
        ei_data         = e_ident[ 0x5 : 0x6 ][0]
        ei_version      = e_ident[ 0x6 : 0x7 ][0]
        ei_osabi        = e_ident[ 0x7 : 0x8 ][0]
        ei_abiversion   = e_ident[ 0x8 : 0x9 ][0]
        ei_pad          = e_ident[ 0x9 : ]

        if ei_data == 2: self.endian = "big" # {"little endian": 1, "big endian": 2}
        self.e_type      = converter.bytes2int(elf_header[ 0x10 : 0x12 ], self.endian)
        self.e_machine   = converter.bytes2int(elf_header[ 0x12 : 0x14 ], self.endian)
        self.e_version   = converter.bytes2int(elf_header[ 0x14 : 0x18 ], self.endian)
        self.e_entry     = converter.bytes2int(elf_header[ 0x18 : 0x1C ], self.endian)
        self.e_phoff     = converter.bytes2int(elf_header[ 0x1C : 0x20 ], self.endian)
        self.e_shoff     = converter.bytes2int(elf_header[ 0x20 : 0x24 ], self.endian)
        self.e_flags     = converter.bytes2int(elf_header[ 0x24 : 0x28 ], self.endian)
        self.e_ehsize    = converter.bytes2int(elf_header[ 0x28 : 0x2A ], self.endian)
        self.e_phentsize = converter.bytes2int(elf_header[ 0x2A : 0x2C ], self.endian)
        self.e_phnum     = converter.bytes2int(elf_header[ 0x2C : 0x2E ], self.endian)
        self.e_shentsize = converter.bytes2int(elf_header[ 0x2E : 0x30 ], self.endian)
        self.e_shnum     = converter.bytes2int(elf_header[ 0x30 : 0x32 ], self.endian)
        self.e_shstrndx  = converter.bytes2int(elf_header[ 0x32 : ], self.endian)


    def parseSectionHeader(self):
        start = self.e_shoff
        for i in range(self.e_shnum):
            section_header = self.raw[ start : start + 0x28 ]
            sh_name      = converter.bytes2int(section_header[ 0x00 : 0x04 ], self.endian)
            sh_type      = converter.bytes2int(section_header[ 0x04 : 0x08 ], self.endian)
            sh_flags     = converter.bytes2int(section_header[ 0x08 : 0x0C ], self.endian)
            sh_addr      = converter.bytes2int(section_header[ 0x0C : 0x10 ], self.endian)
            sh_offset    = converter.bytes2int(section_header[ 0x10 : 0x14 ], self.endian)
            sh_size      = converter.bytes2int(section_header[ 0x14 : 0x18 ], self.endian)
            sh_link      = converter.bytes2int(section_header[ 0x18 : 0x1C ], self.endian)
            sh_info      = converter.bytes2int(section_header[ 0x1C : 0x20 ], self.endian)
            sh_addralign = converter.bytes2int(section_header[ 0x20 : 0x24 ], self.endian)
            sh_entsize   = converter.bytes2int(section_header[ 0x24 : 0x28 ], self.endian)

            if sh_type == 2: self.symtab = self.raw[ sh_offset : sh_offset + sh_size ]
            start += 0x28


# http://www.skyfree.org/linux/references/ELF_Format.pdf