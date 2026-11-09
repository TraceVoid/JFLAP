import struct, zipfile, io

def parse(data):
    """Parsea un .class: devuelve (entries, info) donde entries es la lista del constant pool."""
    pos = 8
    n = struct.unpack('>H', data[pos:pos+2])[0]; pos += 2
    entries = [None]*n
    i = 1
    while i < n:
        tag = data[pos]
        start = pos
        pos += 1
        if tag == 1:
            ln = struct.unpack('>H', data[pos:pos+2])[0]; pos += 2
            entries[i] = (1, start, pos, pos+ln)   # tag, start_of_entry, data_start, data_end
            pos += ln
        elif tag in (3, 4):
            pos += 4; entries[i] = (tag, start, pos)
        elif tag in (5, 6):
            pos += 8; entries[i] = (tag, start, pos); i += 1
        elif tag in (7, 8, 16, 19, 20):
            idx = struct.unpack('>H', data[pos:pos+2])[0]; pos += 2
            entries[i] = (tag, start, pos, idx)
        elif tag in (9, 10, 11, 12, 17, 18):
            a, b = struct.unpack('>HH', data[pos:pos+4]); pos += 4
            entries[i] = (tag, start, pos, a, b)
        elif tag == 15:
            pos += 3; entries[i] = (tag, start, pos)
        else:
            raise ValueError('tag %d' % tag)
        i += 1
    cp_end = pos
    return entries, cp_end

def decode_mutf8(b):
    try:
        return b.decode('utf-8')   # suficiente para nuestro caso (sin supplementary / NUL especial)
    except UnicodeDecodeError:
        return None

def name_indexes(data, entries, cp_end):
    """Indices de Utf8 usados como nombres/descriptores fuera del constant pool (miembros y atributos)."""
    used = set()
    pos = cp_end + 6
    ic = struct.unpack('>H', data[pos:pos+2])[0]; pos += 2 + 2*ic
    def attrs(pos):
        na = struct.unpack('>H', data[pos:pos+2])[0]; pos += 2
        for _ in range(na):
            name, ln = struct.unpack('>HI', data[pos:pos+6]); used.add(name)
            pos += 6 + ln
        return pos
    for _ in range(2):  # fields, methods
        cnt = struct.unpack('>H', data[pos:pos+2])[0]; pos += 2
        for _ in range(cnt):
            acc, nm, ds = struct.unpack('>HHH', data[pos:pos+6]); used.add(nm); used.add(ds)
            pos = attrs(pos+6)
    attrs(pos)
    return used
