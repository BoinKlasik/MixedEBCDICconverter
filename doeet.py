import csv
import os
from enum import Enum, auto
from byte_read_util import *
from typing import Dict, List, Any

records = {}


class Format(Enum):
    EBCDIC = auto()
    BINARY = auto()


class Type(Enum):
    INT = 4
    SHORT = 2
    LONG = 8
    PADDING = 999
    STRING = 1000


class Field:
    def __init__(self, name: str, size: int, in_format: Format):
        if type == Format.BINARY and size > 4:
            print("Warning: '{}' has size >4 ({})  but is binary,"
                  " this is probably incorrect and is probably EBCDIC. Will treat as padding.".format(name, size))
        self.name = name
        self.format = in_format
        self.size = size
        if self.format is Format.EBCDIC:
            self.type = Type.STRING
        else:
            try:
                self.type = Type(size)
            except ValueError:
                self.type = Type.PADDING

    def __len__(self):
        return self.size

    def read(self, byte_input: io.BytesIO):
        if self.type is Type.INT:
            return read_int(byte_input)
        elif self.type is Type.SHORT:
            return read_short(byte_input)
        elif self.type is Type.LONG:
            return read_long(byte_input)
        elif self.type is Type.PADDING:
            read_padding(byte_input, self.size)
            return 0
        elif self.type is Type.STRING:
            return read_string(byte_input, self.size)


class BlockDataWord:
    def __init__(self, byte_input : io.BytesIO):
        self.block_length = read_short(byte_input)
        read_padding(byte_input, 2)

    def __len__(self):
        return 4


class RecordDataWord:
    def __init__(self, byte_input : io.BytesIO):
        self.record_length = read_short(byte_input)
        read_padding(byte_input, 2)

    def __len__(self):
        return 4


class GenericRecord:
    fields: [Field]
    name: str
    _length: int
    _read_values: Dict[str, Any]

    def __init__(self, name: str, fields: [Field]):
        self.name = name
        self.fields = fields
        self._length = sum([x.size for x in fields])
        self._read_values = {}

    def __len__(self):
        return self._length

    @property
    def real_length(self):
        return len(self) + 4


class ReadRecord:
    def __init__(self, record_type : GenericRecord, byte_stream: io.BytesIO):
        self.record_type = record_type
        self.read_values = {}
        for field in self.record_type.fields:
            self.read_values[field.name] = field.read(byte_stream)

    def __str__(self):
        result = ""

        for field in self.record_type.fields:
            value = self.read_values[field.name]
            result += "{}: {}\n".format(field.name, value)

        return result

    def fields(self) -> List[str]:
        return [x.name for x in self.record_type.fields]


def read_file(byte_stream, len_stream) -> Dict[str, ReadRecord]:
    read_records = {}
    read_bytes = 0
    while read_bytes < len_stream:
        bdw = BlockDataWord(byte_stream)
        read_bytes += len(bdw)
        block_read = 4
        while block_read < bdw.block_length:
            rdw = RecordDataWord(byte_stream)
            record = byte_stream.read(rdw.record_length - 4)

            block_read += rdw.record_length
            record_io = io.BytesIO(record)
            read_record = ReadRecord(records[rdw.record_length], record_io)
            read_records.setdefault(read_record.record_type.name, []).append(read_record)
        read_bytes += block_read

    return read_records


record_files = os.listdir('formats')
print(record_files)
for fileName in record_files:
    if not fileName.endswith('.csv'):
        continue
    with open('formats/' + fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        fields = []
        for row in reader:
            field = Field(row["Data element"], int(row["size"]), Format[row["data standard"].upper()])
            fields.append(field)
        record = GenericRecord(fileName, fields)
        print("Parsed record with name {}, {} fields and total length {}".format(record.name, len(record.fields), len(record)))
        if record.real_length in records:
            print("Two records with same recorded length, determining which record to use not yet implemented")
        records[record.real_length] = record


input_files = os.listdir('input')
print(input_files)
for fileName in input_files:
    full_name = 'input/' + fileName
    with open(full_name, mode='br') as input_file:
        file_size = os.stat(full_name).st_size
        results = read_file(input_file, file_size)
    print(fileName + ":")
    for key in results:
        print("{}: {}".format(key, len(results[key])))
    for key in results:
        with open('output/' + fileName + key, 'w', errors='backslashreplace') as output:
            value = results[key]
            field_names = value[0].fields()
            output_csv = csv.DictWriter(output, fieldnames=field_names)
            output_csv.writeheader()
            for x in value:
                output_csv.writerow(x.read_values)
