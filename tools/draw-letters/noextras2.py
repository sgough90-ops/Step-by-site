"""Extras out, round 2 (26 Nov 2026). He asked: "on some of the drawings where they just have like little bubbles or stuff
like that off the page ... or off the main drawing ... could be something on the floor" -- yak, caterpillar, X-15,
submarine, xiao long bao, zipline car, fizzy drink, onion, udon, swan (2 is for Swan), stork, piranha and shark.
Each loses the bits that float off the main picture (bubbles, clouds, steam, grass, rocks, a ground line, splashes,
fizz lines, a bit of onion skin), and is moved to the middle of the paper again. Uses noextras.py's tools.

    python3 noextras2.py ../../public/draw/index.html ../../public/mim-plans.js
"""
import json, re, sys
import noextras as NX

T = lambda title, idx, n, text, new_title=None: (title, idx, n, text, new_title)
EDITS = {
    'dx_yak_y': dict(after=(0, 4.0), trim=[T('Hair and grass', list(range(3, 12)), 12, 'Draw a few lines of hair on its side.', 'More hair')],
                     desc=('A shaggy yak standing in the grass, with', 'A shaggy yak with')),
    'dx_caterpillar_c': dict(drop={'Grass and rocks': 5, 'Colour the grass': 3, 'Colour the rocks': 2}, out=['grass', 'grey']),
    'dx_x15_x': dict(drop={'Clouds': 2}, after=(-3.0, 1.0)),   # moved +3, -1 only: at +6, -2 the app's own checker sees two colours touch
    'dx_submarine_s': dict(drop={'Bubbles': 3}),
    'dx_xiaolongbao_x': dict(trim=[T('Steam and spring onion', [4, 5, 6], 7, 'Draw four small circles in the basket: bits of spring onion.', 'Spring onion')]),
    'dx_ziplinecar_z': dict(drop={'Clouds': 2}),
    'dx_fizzydrink_f': dict(trim=[T('Ice cubes', [2, 3, 4], 5, 'Draw two ice cubes in the drink.')]),
    'dx_onion_o': dict(trim=[T('The skin', [4], 5, 'Draw four curved lines down the onion, from near the top to near the bottom.'),
                             T('Colour the onion', [1], 2, 'Colour the onion light brown.')]),
    'dx_udon_u': dict(drop={'Steam': 3}),
    'dx_swan_2': dict(trim=[T('The eye and water', [1, 2, 3, 4], 5, 'Draw a dot for the eye.', 'The eye')],
                      desc=('A swan on the water, stretching', 'A swan stretching')),
    'dx_stork_4': dict(trim=[T('The beak', [2, 3], 4, 'Draw a long open beak: two pointy triangles.'),
                             T('The feet', [4], 5, 'Draw two little toes at the end of each leg.')],
                       desc=('with its head held high, clattering its long beak.', 'with its head held high and its long beak open.')),
    'dx_piranha_5': dict(drop={'Bubbles': 2}),
    'dx_shark_7': dict(trim=[T('The face', [3, 4], 5, 'Draw a dot for the eye and two curved lines for the gills.')], drop={'Colour light blue': 2}, out=['lblue']),
}
PLAN_WORDS = {'dx_caterpillar_c': {
    'seen': (' Around it on the ground: three small green grass tufts (bottom left, bottom right and one inside the C) and two grey rocks (one to the right under the head, a small pebble at the bottom right).', ' Nothing else is drawn.'),
    'silly': ('; the grass tufts sway and the rocks stay put.', '.'),
    'cool': (' glides in over the grass with', ' glides in with'),
}}
PLAN_GONE = {'dx_caterpillar_c': ['grassL', 'grassR', 'grassC', 'rock', 'pebble']}


def fix_plan(plan, mp, dx, dy, gone_ok, words):
    """noextras.fix_plan, also knowing the moves that never name a place: hide, step and sway"""
    real = NX.fix_plan.__globals__
    src = NX.fix_plan
    # the same steps as noextras.fix_plan; only the list of known moves is longer
    plan = json.loads(json.dumps(plan)); dx, dy = float(dx), float(dy)
    r2 = lambda v: int(round(v, 2)) if float(round(v, 2)).is_integer() else round(v, 2)
    parts = []; gone = []
    for pt in plan['parts']:
        if isinstance(pt.get('items'), list):
            new = [mp[r] for r in pt['items']]
            if pt['items'] and all(n is None for n in new): gone.append(pt['id']); continue
            assert all(n is not None for n in new), ('a part would keep some shapes and lose others', pt['id'])
            pt['items'] = new
        if pt.get('pivot'): pt['pivot'] = [r2(pt['pivot'][0] + dx), r2(pt['pivot'][1] + dy)]
        for m in pt.get('motion', []):
            assert m['type'] in ('bob', 'extend', 'wag', 'blink', 'show', 'lift', 'hide', 'step', 'sway'), m
        parts.append(pt)
    assert gone == gone_ok, (gone, gone_ok)
    assert not [pt['id'] for pt in parts if pt.get('parent') in gone]
    plan['parts'] = parts
    plan['points'] = {k: [r2(v[0] + dx), r2(v[1] + dy)] for k, v in plan.get('points', {}).items()}
    for pa in plan.get('patches', []):
        assert pa['part'] not in gone
        pa['d'] = NX.move_path(pa['d'], dx, dy)
        if pa.get('by') in gone: pa['by'] = 'paper'
    for k, (old, new) in words.items():
        assert plan[k].count(old) == 1, (k, old)
        plan[k] = plan[k].replace(old, new)
    return plan


def main(f_page, f_plans):
    s = open(f_page, encoding='utf-8').read(); plans = open(f_plans, encoding='utf-8').read()
    for key, E in EDITS.items():
        head = 'DX.reg("%s",' % key; assert s.count(head) == 1, key
        i = s.index(head) + len(head); D, end = json.JSONDecoder().raw_decode(s, i)
        assert s[i:end] == NX.dump(D), key
        trim = {t[0]: (t[2], t[1], t[3]) for t in E.get('trim', [])}
        N, mp = NX.without(D, E.get('drop', {}), trim, E.get('out', []), E.get('desc') and (D['description'], D['description'].replace(*E['desc'])))
        for t in E.get('trim', []):
            if t[4]:
                for st in N['steps']:
                    if st['title'] == t[0]: st['title'] = t[4]
        b, c = NX.middle(N); dx, dy = NX.half(50 - c[0]), NX.half(50 - c[1])
        N = NX.moved(N, str(dx), str(dy))
        if E.get('after'):                     # a second move, where the middle would put it under the step number
            N = NX.moved(N, str(E['after'][0]), str(E['after'][1])); dx += E['after'][0]; dy += E['after'][1]
        s = s[:i] + NX.dump(N) + s[end:]
        card = re.compile(r'(REALS\.draw\.push\(\{t:"[^"]*",lvl:\d+,time:\d+,theme:"[^"]*",eq:\["pencil","colour"\],steps:)(\d+)(,key:"%s",type:"draw",)' % re.escape(key))
        assert len(card.findall(s)) == 1, key
        s = card.sub(lambda m: m.group(1) + str(len(N['steps'])) + m.group(3), s)
        json.dump(N, open('out/ne2_%s.json' % key, 'w'), ensure_ascii=False)
        msg = ''
        ph = 'MIM.reg("%s",' % key
        if ph in plans:
            j = plans.index(ph) + len(ph); P, pend = json.JSONDecoder().raw_decode(plans, j)
            Q = fix_plan(P, mp, dx, dy, PLAN_GONE.get(key, []), PLAN_WORDS.get(key, {}))
            plans = plans[:j] + NX.dump(Q) + plans[pend:]; msg = '| plan %d parts -> %d' % (len(P['parts']), len(Q['parts']))
        print('%-18s %2d steps -> %2d | moved %+.1f, %+.1f %s' % (key, len(D['steps']), len(N['steps']), dx, dy, msg))
    open(f_page, 'w', encoding='utf-8').write(s); open(f_plans, 'w', encoding='utf-8').write(plans)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
