"""Puts built drawings into the Step by Draw app page.

    python3 apply.py <public/draw/index.html> name1 name2 ...

Each name reads out/<name>.json and out/<name>.place.json ({set, slot, kind, age_from}).
Each drawing goes in four places: the data + its card, its level, its Make it move kind, and its set slot.
Stops if anything is not found exactly once, or if a key or slot is already taken.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
f = sys.argv[1]; names = sys.argv[2:]
s = open(f, encoding='utf-8').read()
before = len(s.encode())


def set_head(setid):
    global s
    pat = r"\{id:'%s',n:'[^']*',cv:'[^']*',set:'[^']*',has:\{" % re.escape(setid)
    m = re.findall(pat, s)
    if not m:   # a set with no drawings yet (17 Nov 2026: the number sets) gets an empty list first
        bare = re.findall(r"\{id:'%s',n:'[^']*',cv:'[^']*',set:'[^']*'\}" % re.escape(setid), s)
        assert len(bare) == 1, (setid, bare)
        s = s.replace(bare[0], bare[0][:-1] + ',has:{}}')
        print('  (gave', setid, 'its first list of drawings)')
        m = re.findall(pat, s)
    assert len(m) == 1, (setid, m)
    return m[0]


def one(old, new):
    global s
    assert s.count(old) == 1, ('expected exactly one', old[:80], s.count(old))
    s = s.replace(old, new)


def real(P, age_from):
    return 'REALS.draw.push({t:"%s",lvl:%d,time:%d,theme:"%s",eq:["pencil","colour"],steps:%d,key:"%s",type:"draw",pop:98,age:0,ageFrom:%d});' % (
        P['title'], P['level'], int(P['time'].split()[0]), P['theme'], len(P['steps']), P['id'], age_from)


for name in names:
    P = json.load(open(os.path.join(OUT, name + '.json'))); w = json.load(open(os.path.join(OUT, name + '.place.json')))
    key = P['id']
    assert key not in s, key + ' is already in the page'
    assert re.fullmatch(r'[a-z_0-9]+', key)
    head = set_head(w['set'])
    i = s.index(head) + len(head); has = s[i:s.index('}', i)]
    assert not re.search(r"(^|,)%s:'" % re.escape(w['slot']), has), ('slot taken', w['set'], w['slot'], has)
    one('REALS.fold=[', 'DX.reg("%s",' % key + json.dumps(P, separators=(',', ':'), ensure_ascii=False) + ');' + real(P, w['age_from']) + 'REALS.fold=[')
    b = 'L10["dx_bug_b"]=3;REG["dx_bug_b"]={type:"draw"};'
    one(b, b + 'L10["%s"]=%d;REG["%s"]={type:"draw"};' % (key, P['level'], key))
    k = 'dx_ladybird:"fly",dx_bug_b:"fly",'
    one(k, k + '%s:"%s",' % (key, w['kind']))
    one(head, head + "%s:'%s'," % (w['slot'], key))
    print('added', key, '->', w['set'], w['slot'], '| level', P['level'], '| steps', len(P['steps']), '| kind', w['kind'])

open(f, 'w', encoding='utf-8').write(s)
print('done; page bytes %d -> %d (+%d)' % (before, len(s.encode()), len(s.encode()) - before))
