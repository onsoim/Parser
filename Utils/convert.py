def bytes2int(bytes, endian):
    return int.from_bytes(bytes, byteorder=endian)