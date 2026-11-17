"""Replaces the data of drawings already in the app page with freshly built ones (same key), and their card line.

    python3 reapply.py <public/draw/index.html> name1 name2 ...
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
f = sys.argv[1]; s = open(f, encoding='utf-8').read()
for name in sys.argv[2:]:
    P = json.load(open(os.path.join(OUT, name + '.json'))); w = json.load(open(os.path.join(OUT, name + '.place.json'))); key = P['id']
    head = 'DX.reg("%s",' % key
    assert s.count(head) == 1, (key, s.count(head))
    i = s.index(head) + len(head); obj, end = json.JSONDecoder().raw_decode(s, i)
    s = s[:i] + json.dumps(P, separators=(',', ':'), ensure_ascii=False) + s[end:]
    card = re.compile(r'REALS\.draw\.push\(\{t:"[^"]*",lvl:\d+,time:\d+,theme:"[^"]*",eq:\["pencil","colour"\],steps:\d+,key:"%s",type:"draw",pop:98,age:0,ageFrom:\d+\}\);' % re.escape(key))
    assert len(card.findall(s)) == 1, key
    s = card.sub('REALS.draw.push({t:"%s",lvl:%d,time:%d,theme:"%s",eq:["pencil","colour"],steps:%d,key:"%s",type:"draw",pop:98,age:0,ageFrom:%d});' % (
        P['title'], P['level'], int(P['time'].split()[0]), P['theme'], len(P['steps']), key, w['age_from']), s)
    s = re.sub(r'L10\["%s"\]=\d+;' % re.escape(key), 'L10["%s"]=%d;' % (key, P['level']), s)
    print('updated', key, len(P['steps']), 'steps')
open(f, 'w', encoding='utf-8').write(s)
