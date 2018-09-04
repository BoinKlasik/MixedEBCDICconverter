# import ebcdic
import os
import struct

def read_int(byte_input, offset):
    return struct.unpack(">i", byte_input[offset:4]), offset + 4

class RecordDataWord:
    def __init__(self, byte_input : bytes):
        if len(byte_input) is not 4:
            raise ValueError("RDW is only 4 bytes long")
        self.length = struct.unpack(">h", byte_input[:2])[0]


class DistrictDataRecord:
    def __init__(self, byte_input : bytes):
        offset = 0
        self.school_system_code, offset = read_int(byte_input, offset)
        self.system_name = byte_input[8:31].decode(encoding="cp1140")
        self.address = ""


def read_record(byte_stream) :
    rdw_bytes = byte_stream.read(4)
    if not len(rdw_bytes):
        return None
    rdw = RecordDataWord(rdw_bytes)
    record_type = struct.unpack(">B", byte_stream.read(1))[0]
    if record_type is 1:
        ddr = DistrictDataRecord(byte_stream.read(rdw.length - 5))
    print(rdw.length)
    return rdw.length

inputfiles = os.listdir('input')
print(inputfiles)
for fileName in inputfiles:
    with open('input/' + fileName, mode='br') as input_file:
        read_record(input_file)
    break
