import io
import struct


def read_int(byte_input: io.BytesIO) -> int:
    return struct.unpack(">i", byte_input.read(4))[0]


def read_short(byte_input: io.BytesIO) -> int:
    return struct.unpack(">h", byte_input.read(2))[0]


def read_long(byte_input) -> int:
    return struct.unpack(">q", byte_input.read(8))[0]


def read_padding(byte_input: io.BytesIO, count: int) -> None:
    byte_input.read(count)


def read_string(byte_input: io.BytesIO, length: int) -> str:
    return byte_input.read(length).decode(encoding="cp1140")
