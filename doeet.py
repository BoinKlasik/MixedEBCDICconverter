# import ebcdic
import os
import io
import struct


def read_int(byte_input : io.BytesIO) -> int:
    return struct.unpack(">i", byte_input.read(4))[0]


def read_short(byte_input : io.BytesIO) -> int:
    return struct.unpack(">h", byte_input.read(2))[0]


def read_long(byte_input) -> int:
    return struct.unpack(">q", byte_input.read(8))[0]


def read_padding(byte_input : io.BytesIO, count : int) -> None:
    byte_input.read(count)


def read_string(byte_input : io.BytesIO, length : int) -> str:
    return byte_input.read(length).decode(encoding="cp1140")


class RecordDataWord:
    def __init__(self, byte_input : bytes):
        self.length = struct.unpack(">h", byte_input[:2])[0]


class BlockDataWord:
    def __init__(self, byte_input : io.BytesIO):
        self.length = read_short(byte_input)
        read_padding(byte_input, 2)


class DistrictDataRecord:
    def __init__(self, byte_input : io.BytesIO):
        self.record_type = 1
        self.school_system_code = read_int(byte_input)
        read_padding(byte_input, 4)
        self.system_name = read_string(byte_input, 32)
        self.address = read_string(byte_input, 32)
        self.city = read_string(byte_input, 16)
        self.county = read_string(byte_input, 16)
        self.state = read_string(byte_input, 16)
        self.zip = read_string(byte_input, 8)
        self.administrator = 0


def read_record(byte_stream) :
    rdw_bytes = byte_stream.read(4)
    if not len(rdw_bytes):
        return None
    rdw = RecordDataWord(rdw_bytes)
    bdw = BlockDataWord(byte_stream)
    block = byte_stream.read(bdw.length)
    block_io = io.BytesIO(block)
    record_type = read_int(block_io)
    if record_type is 1:
        ddr = DistrictDataRecord(block_io)
    print(rdw.length)
    return rdw.length


input_files = os.listdir('input')
print(input_files)
for fileName in input_files:
    with open('input/' + fileName, mode='br') as input_file:
        read_record(input_file)
    break
