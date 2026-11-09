import sys, zipfile, struct, json, importlib.util, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classlib import *
src, dst, dictfile = sys.argv[1:4]
D = {}
for df in dictfile.split(','):
    spec = importlib.util.spec_from_file_location('d', df); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    D.update(m.D)
D = {k: v for k, v in D.items() if k != v}
import re
SPLIT = re.compile('(\n|\x01)')
def translate(s):
    if s in D: return D[s]
    parts = SPLIT.split(s)
    if len(parts) == 1: return None
    out = []; hit = False
    for p in parts:
        if p in D: out.append(D[p]); used.add(p); hit = True
        else: out.append(p)
    return ''.join(out) if hit else None
logic = set(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logic.json'))))
used = set(); changed = 0
zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename.endswith('.class') and not item.filename.startswith(('org/', 'META-INF/')):
        entries, cp_end = parse(data)
        other = name_indexes(data, entries, cp_end)
        ref_other = set(); ref_str = set()
        for e in entries:
            if not e: continue
            if e[0] == 8: ref_str.add(e[3])
            elif e[0] in (7, 16, 19, 20): ref_other.add(e[3])
            elif e[0] in (9, 10, 11, 12, 17, 18): ref_other.update(e[3:5])
        repl = {}
        for idx in ref_str:
            if idx in ref_other or idx in other: continue
            e = entries[idx]; s = decode_mutf8(data[e[2]:e[3]])
            if s is None or s in logic: continue
            t = translate(s)
            if t is None: continue
            used.add(s)
            nb = t.encode('utf-8')
            assert len(nb) < 65535
            repl[idx] = nb
        if repl:
            out = bytearray(data[:10]); pos = 10
            for i in range(1, len(entries)):
                e = entries[i]
                if e is None: continue   # segunda ranura de long/double
                end = e[2] + 0
                # limite de la entrada: la siguiente entrada comienza donde termina esta
            # reconstruccion simple: copiar tramo a tramo
            starts = sorted((e[1], i) for i, e in enumerate(entries) if e)
            out = bytearray(data[:10])
            for k, (st, i) in enumerate(starts):
                en = starts[k+1][0] if k+1 < len(starts) else cp_end
                if i in repl:
                    out += b'\x01' + struct.pack('>H', len(repl[i])) + repl[i]
                else:
                    out += data[st:en]
            out += data[cp_end:]
            data = bytes(out); changed += 1
    zout.writestr(item, data)
zout.close()
print('clases modificadas:', changed, ' cadenas usadas:', len(used), 'de', len(D))
json.dump(sorted(set(D) - used), open('unused_keys.json', 'w'), ensure_ascii=False, indent=0)
