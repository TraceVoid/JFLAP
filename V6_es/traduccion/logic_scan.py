import sys, zipfile, struct, json
sys.path.insert(0, '/home/claude/i18n')
from classlib import *
CMP = {'equals','equalsIgnoreCase','startsWith','endsWith','contains','indexOf','hashCode','compareTo','containsKey','getProperty','forName','getResource','getResourceAsStream','setActionCommand'}
def u16(d,p): return struct.unpack('>H',d[p:p+2])[0]
def methods_code(data, cp_end, entries):
    pos = cp_end + 6
    ic = u16(data,pos); pos += 2 + 2*ic
    def skipattrs(pos, collect=None):
        na = u16(data,pos); pos += 2
        for _ in range(na):
            nm = u16(data,pos); ln = struct.unpack('>I',data[pos+2:pos+6])[0]
            if collect is not None: collect.append((nm, pos+6, ln))
            pos += 6+ln
        return pos
    cnt = u16(data,pos); pos += 2
    for _ in range(cnt): pos = skipattrs(pos+6)
    cnt = u16(data,pos); pos += 2
    out=[]
    for _ in range(cnt):
        pos = skipattrs(pos+6, out)
    return out
def utf(data,entries,i):
    e=entries[i]; return data[e[2]:e[3]].decode('utf-8','replace')
flag = {}   # string -> set of (cls, method)
z = zipfile.ZipFile(sys.argv[1])
for name in z.namelist():
    if not name.endswith('.class') or name.startswith(('org/','META-INF/')): continue
    data = z.read(name); entries, cp_end = parse(data)
    # methodref idx -> method name
    mname = {}
    for i,e in enumerate(entries):
        if e and e[0] in (10,11):
            nt = entries[e[4]]; mname[i] = utf(data,entries,nt[3])
    strs = {i: utf(data,entries,e[3]) for i,e in enumerate(entries) if e and e[0]==8}
    for nm, p, ln in methods_code(data, cp_end, entries):
        if utf(data,entries,nm) != 'Code': continue
        clen = struct.unpack('>I', data[p+4:p+8])[0]
        code = data[p+8:p+8+clen]
        # linear scan for ldc(0x12)/ldc_w(0x13) and invoke (0xb6,0xb7,0xb8,0xb9) within next 12 bytes -- heuristic
        i=0
        while i < len(code)-2:
            op = code[i]; idx=None
            if op==0x12: idx=code[i+1]; L=2
            elif op==0x13: idx=u16(code,i+1); L=3
            else: i+=1; continue
            if idx in strs:
                for j in range(i+L, min(i+L+10, len(code)-2)):
                    if code[j] in (0xb6,0xb9,0xb8):
                        m = mname.get(u16(code,j+1))
                        if m in CMP: flag.setdefault(strs[idx], set()).add((name, m)); break
                        if m and m not in ('append','<init>'): break
            i += L
json.dump({k: sorted(set(c+':'+m for c,m in v)) for k,v in flag.items()}, open('logic.json','w'), ensure_ascii=False, indent=0)
print(len(flag))
