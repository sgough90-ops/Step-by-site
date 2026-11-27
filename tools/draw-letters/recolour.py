"""Colour changes from the colour review (27 Nov 2026): changes only colours (and the colour words) of live drawings in the
page, no lines. His picks from the before/after pictures: helicopter, kayak, snowmobile, wagon, lorry, quad bike, yoghurt
and insect. The yoghurt's blue step is split in two (yellow bowl, then blue blueberries), so it has one more step.

    python3 recolour.py ../../public/draw/index.html

Helicopter, snowmobile, wagon, quad bike and yoghurt have build scripts, changed the same way, which build exactly
what this puts in the page. Kayak, lorry and insect have no build script, so they are changed here only.
"""
import json, re, sys

PEN = {'red': ('Red pencil', '#fa5252'), 'yellow': ('Yellow pencil', '#ffd43b'), 'blue': ('Blue pencil', '#4dabf7'),
       'green': ('Green pencil', '#40c057'), 'lgreen': ('Light green pencil', '#a9e34b'), 'orange': ('Orange pencil', '#ff922b'),
       'purple': ('Purple pencil', '#9775fa')}


def mat(i): return {"id": i, "kind": "pencil", "name": PEN[i][0], "qty": "1", "color": PEN[i][1]}


# key: description change, pencil swaps in the materials, and colour steps (counted from 0) -> new title, text, pencil, fill
SPEC = {
    'dx_helicopter_h': (('A red helicopter', 'A purple helicopter'), {'red': 'purple'}, {
        7: ('Colour purple', 'Colour the tail purple. Colour the bottom of the cabin purple too, under the window.', 'purple', '#b197fc')}),
    'dx_kayak_k': (('A red kayak', 'A green kayak'), {'red': 'green'}, {
        8: ('Colour green', 'Colour the kayak green. Leave the seat.', 'green', '#8ad35a')}),
    'dx_snowmobile_s': (('A red snowmobile', 'An orange snowmobile'), {'red': 'orange'}, {
        7: ('Colour orange', 'Colour the back of the body orange, as far as the line down the middle. Leave the nose white.', 'orange', '#ffa94d')}),
    'dx_wagon_w': (('A red railway wagon', 'A blue railway wagon'), {'red': 'blue'}, {
        8: ('Colour blue', 'Colour the wagon blue.', 'blue', '#4dabf7')}),
    'dx_lorry_l': (None, {'red': 'blue'}, {
        8: ('Colour blue', 'Colour the cab blue, and the strip under the box. Go round the window and the headlight.', 'blue', '#4dabf7')}),
    'dx_quadbike_q': (('A red quad bike', 'A green quad bike'), {'red': 'green'}, {
        9: ('Colour green', 'Colour the body green. Go round the light.', 'green', '#8ad35a')}),
    'dx_insect_i': (('A little brown insect', 'A little green insect'), {'brown': 'green', 'lbrown': 'lgreen'}, {
        8: ('Colour the head', 'Colour the head green. Leave the two eyes for later.', 'green', '#5fb03e'),
        9: ('Colour the body', 'Colour the body light green, on both sides of the line down the middle.', 'lgreen', '#8ad35a')}),
}


def yoghurt(P):
    """Step 8 (blue bowl and blueberries) becomes two steps: the bowl yellow, then the two blueberries blue."""
    st = P['steps'][7]
    assert st['use'] == ['blue'] and len(st['add']) == 3, st
    bowl, berries = st['add'][:1], st['add'][1:]
    bowl[0]['fill'] = '#ffd43b'
    a = {'title': 'Colour yellow', 'text': 'Colour the bowl yellow, under the ovals.', 'use': ['yellow'], 'add': bowl}
    b = {'title': 'Colour blue', 'text': 'Colour the two blueberries blue.', 'use': ['blue'], 'add': berries}
    for k in st:
        if k not in a: a[k] = st[k]; b[k] = st[k]
    P['steps'][7:8] = [a, b]
    i = [m['id'] for m in P['materials']].index('blue')
    P['materials'].insert(i, mat('yellow'))
    return P


def change(key, P):
    if key == 'dx_yoghurt_y': return yoghurt(P)
    desc, pens, steps = SPEC[key]
    if desc:
        assert desc[0] in P['description'], (key, P['description'])
        P['description'] = P['description'].replace(desc[0], desc[1])
    for n, (title, text, pen, fill) in steps.items():
        st = P['steps'][n]
        assert len(st['use']) == 1 and st['use'][0] in pens, (key, n, st['use'])
        st['title'], st['text'], st['use'] = title, text, [pen]
        for it in st['add']:
            assert 'fill' in it, (key, n)
            it['fill'] = fill
    for old, new in pens.items():
        assert not any(old in st.get('use', []) for st in P['steps']), (key, old, 'still used')
        ids = [m['id'] for m in P['materials']]
        P['materials'][ids.index(old)] = mat(new)
    return P


if __name__ == '__main__':
    f = sys.argv[1]; s = open(f, encoding='utf-8').read()
    for key in list(SPEC) + ['dx_yoghurt_y']:
        head = 'DX.reg("%s",' % key
        assert s.count(head) == 1, key
        i = s.index(head) + len(head); P, end = json.JSONDecoder().raw_decode(s, i)
        P = change(key, P)
        s = s[:i] + json.dumps(P, separators=(',', ':'), ensure_ascii=False) + s[end:]
        card = re.compile(r'(REALS\.draw\.push\(\{t:"[^"]*",lvl:\d+,time:\d+,theme:"[^"]*",eq:\["pencil","colour"\],steps:)\d+(,key:"%s",)' % re.escape(key))
        assert len(card.findall(s)) == 1, key
        s = card.sub(lambda m: m.group(1) + str(len(P['steps'])) + m.group(2), s)
        print('changed', key, len(P['steps']), 'steps')
    open(f, 'w', encoding='utf-8').write(s)
