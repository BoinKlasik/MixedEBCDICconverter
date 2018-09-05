# import ebcdic
import os
import struct


class RecordDataWord:
    def __init__(self, byte_input : bytes):
        if len(byte_input) is not 4:
            raise ValueError("RDW is only 4 bytes long")
        self.length = struct.unpack("<h")


def readRecord(byteinput) :
    rdw = RecordDataWord(byteinput[:4])
    print(rdw.length)
    return rdw.length

inputfiles = os.listdir('input')
print(inputfiles)
for fileName in inputfiles:
    with open('input/' + fileName, mode='br') as input_file:
        input_binary = input_file.read()
        ebcdic_decoded = input_binary.decode(encoding='cp1140')
        with open('output/' + fileName + ".output", mode='w', encoding='cp1140') as output_file:
            byte_encoded = bytes(ebcdic_decoded, encoding='utf-8')
            output_file.write(ebcdic_decoded)
    break
