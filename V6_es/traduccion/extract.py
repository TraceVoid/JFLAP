import sys, zipfile, struct, json, re
from classlib import *
jar = sys.argv[1]
z = zipfile.ZipFile(jar)
skip = ('org/', 'META-INF/')
found = {}   # string -> list of classes
for name in z.namelist():
    if not name.endswith('.class') or name.startswith(skip): continue
    data = z.read(name)
    entries, cp_end = parse(data)
    other = name_indexes(data, entries, cp_end)
    # indices de Utf8 referenciados por entradas que NO son String(8)
    ref_other = set(); ref_str = set()
    for e in entries:
        if not e: continue
        t = e[0]
        if t == 8: ref_str.add(e[3])
        elif t in (7, 16, 19, 20): ref_other.add(e[3])
        elif t in (9,10,11,12,17,18): ref_other.update(e[3:5])
    for idx in ref_str:
        if idx in ref_other or idx in other: continue
        e = entries[idx]
        s = decode_mutf8(data[e[2]:e[3]])
        if s is None: continue
        found.setdefault(s, []).append(name)
json.dump({k: sorted(set(v)) for k, v in found.items()}, open('strings_all.json', 'w'), ensure_ascii=False, indent=0)
print(len(found), 'cadenas')
