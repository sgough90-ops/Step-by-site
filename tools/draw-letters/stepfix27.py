"""Fixes from the full step check of every set drawing (27 Nov 2026).

His ask (27 Nov, 20:01): go through all the drawings and instructions and make sure every step is correct: the first
step is the letter, it all develops from there, nothing is missed out or blurry, and it all works as expected.

All 183 set drawings were checked (1,948 steps). These are the drawings that needed a change. Each fix has a name, so
only the ones he says yes to are applied:

    python3 stepfix27.py ../../public/draw/index.html ../../public/mim-plans.js digger fireengine zebra ...
    python3 stepfix27.py --list

  digger      D is for Digger: steps 10 and 11 each used two pencils. Now four steps, one pencil each (11 -> 13 steps).
  fireengine  F is for Fire Engine: steps 10 and 11 each used three pencils. Now six steps (11 -> 15 steps).
  zebra       Z is for zebra: step 12 asked for 20 leg stripes at once (the app's own check allows 14).
              Now front legs, then back legs (14 -> 15 steps).
  beetledots  B is for Beetle: step 9 drew 20 dots that disappear once the beetle is coloured black. The step goes
              (12 -> 11 steps), and so do the dots in the finished picture.
  colours     A colour went on top of a different colour (pencils cannot do that) in five drawings: C caterpillar
              (eyes, head, feet), S seahorse (eye, crest, tummy), L llama (ears, blanket), a apple juice (stalk),
              O owl (tummy). The colour underneath now leaves a gap for the one on top. The finished pictures look
              the same; in the colour step a small white gap shows where the next colour goes.
  paths       B beetle, H heron, k kayak: their lines used short forms of path writing (H, relative l, a, c) that
              the app's own check and check.py cannot read. Written out in full. Nothing moves.
  texts       g giraffe step 1 and k kayak step 2: words over 160 characters (the app's limit), shortened.
              The words are not shown to children.

Card step counts follow (REALS.draw), and the Make it move plans of the digger, the fire engine and the beetle
(public/mim-plans.js) are kept in step: their step numbers follow the new steps.

It stops if a drawing is not as it expects, so it cannot be run twice by mistake. If build_zebra.py is run again,
run step1fix2.py and then this (zebra) before reapply.py. The other drawings here have no build script.
"""
import json, re, sys

FIXES = ['digger', 'fireengine', 'zebra', 'beetledots', 'colours', 'paths', 'texts']

# ---------------------------------------------------------------- splitting a step that used more than one pencil
# key -> [(old title, how many shapes, [(new title, new words, pencil, [shapes, counted from 0]), ...]), ...]
SPLITS = {
    'digger': ('dx_digger_d', [
        ('Window and dirt', 2, [
            ('The window', 'Colour the window light blue.', 'lblue', [0]),
            ('The dirt', 'Colour the dirt brown.', 'brown', [1])]),
        ('Tracks and wheels', 10, [
            ('The track', 'Colour the track and the short box dark grey.', 'dgrey', [0, 1]),
            ('Wheels and teeth', 'Colour the wheels, the teeth and the circle on the arm grey. Your digger is ready to dig!', 'grey', [2, 3, 4, 5, 6, 7, 8, 9])])]),
    'fireengine': ('dn_fireengine', [
        ('Yellow and blue', 4, [
            ('Yellow', 'Colour the stripe and the headlight yellow.', 'yellow', [0, 1]),
            ('The window', 'Colour the window light blue, but leave the white shine.', 'lblue', [2]),
            ('The lamp', 'Colour the lamp on the roof blue.', 'blue', [3])]),
        ('Wheels and ladder', 14, [
            ('The tyres', 'Colour the tyres black.', 'black', [2, 3]),
            ('Grey parts', 'Colour the lockers, the hubs, the ladder and the bumpers grey.', 'grey', [0, 1, 4, 5, 8, 9, 10, 11, 12, 13]),
            ('Wheel dots', 'Colour a dark grey dot in the middle of each wheel. Your fire engine is ready to zoom to the rescue!', 'dgrey', [6, 7])])]),
    'zebra': ('dx_zebra_z', [
        ('Leg stripes', 20, [
            ('Front leg stripes', 'Draw two stripes on each front leg, and a line across the bottom of each leg for its hoof.', 'pencil', list(range(0, 10))),
            ('Back leg stripes', 'Now the back legs: two stripes on each, and a line across the bottom for its hoof.', 'pencil', list(range(10, 20)))])]),
}

# ---------------------------------------------------------------- a step that goes
DROPS = {'beetledots': ('dx_bug_b', 'Dots', 20)}
DROP_PLAN_WORDS = {'dx_bug_b': {'seen': (' (each with a top bump and a bigger bottom bump) covered in little dots.', ' (each with a top bump and a bigger bottom bump).')}}

# ---------------------------------------------------------------- a colour that leaves a gap for the colour on top of it
# (drawing, the colour underneath, the colour on top) as step.shape counted from 1, as the app's check writes them.
# replace: the cut that was drawn by hand round the eye is swapped for the eye itself (it was a little smaller).
GAPS = [
    ('dx_caterpillar_c', '8.1', '9.1'), ('dx_caterpillar_c', '8.4', '10.5'), ('dx_caterpillar_c', '8.4', '10.6'),
    ('dx_caterpillar_c', '9.1', '11.1', 0), ('dx_caterpillar_c', '9.1', '11.2', 1),
    ('dx_seahorse_s', '9.1', '13.1', 0), ('dx_seahorse_s', '9.1', '11.1'), ('dx_seahorse_s', '9.1', '10.2'), ('dx_seahorse_s', '9.1', '10.3'),
    ('dx_llama_l', '11.1', '12.1'), ('dx_llama_l', '11.1', '12.2'), ('dx_llama_l', '11.1', '15.1'), ('dx_llama_l', '11.1', '15.2'), ('dx_llama_l', '11.1', '16.1'),
    ('dx_applejuice_a', '8.1', '9.1'),
    ('dx_owl_o', '9.1', '10.1'),
]

PATHS = ['dx_bug_b', 'dx_heron_h', 'dx_kayak_k']

TEXTS = [
    ('dx_giraffe_g', 1, 'Draw a small letter g: a round shape, then a stick down its right side that curls round to the left at the bottom. The round part is a spot, and the stick and curl are the giraffe\'s chest and front leg.',
     'Draw a small letter g: a round shape, then a stick down its right side that curls to the left at the bottom. It becomes a spot, the chest and a front leg.'),
    ('dx_kayak_k', 2, 'Draw a long pointy shape around the k. Start at the top of the stick, go out through the ends of the two short lines, down to a point at the bottom, then back up the other side.',
     'Draw a long pointy shape around the k: from the top of the stick, out through the ends of the two short lines, down to a point, then back up the other side.'),
]


# ---------------------------------------------------------------- path writing
NUM = r'[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?'
TOKS = re.compile(r'[MmLlHhVvCcQqAaZz]|' + NUM)
NEED = {'M': 2, 'L': 2, 'H': 1, 'V': 1, 'C': 6, 'Q': 4, 'A': 7, 'Z': 0}


def fmt(v):
    t = ('%.3f' % v).rstrip('0').rstrip('.')
    return '0' if t in ('-0', '', '-') else t


def absolute(d, close=False):
    """the same path written with M L C Q A Z only and every point in paper units (nothing moves).
    A path that already uses only those letters keeps its own text (a colour also gets its Z if it had none)."""
    left = TOKS.sub(' ', d)
    assert not left.replace(',', ' ').strip(), ('a path letter this does not know', d[:80])
    t = TOKS.findall(d)
    if all(c in 'MLCQAZ' for c in t if c.isalpha()):
        s = d
    else:
        i = 0; out = []; x = y = sx = sy = 0.0; cmd = None
        while i < len(t):
            if t[i].isalpha():
                cmd = t[i]; i += 1
                if cmd in 'Zz':
                    out.append('Z'); x, y = sx, sy; continue
            assert cmd, d[:80]
            U = cmd.upper(); rel = cmd != U; n = NEED[U]
            raw = t[i:i + n]; v = [float(a) for a in raw]; i += n
            assert len(v) == n, ('a path ends half way through a point', d[:80])
            if U == 'M':
                x, y = (x + v[0], y + v[1]) if rel else (v[0], v[1]); sx, sy = x, y
                out.append('M %s %s' % ((fmt(x), fmt(y)) if rel else tuple(raw))); cmd = 'l' if rel else 'L'
            elif U == 'L':
                x, y = (x + v[0], y + v[1]) if rel else (v[0], v[1])
                out.append('L %s %s' % ((fmt(x), fmt(y)) if rel else tuple(raw)))
            elif U == 'H':
                x = x + v[0] if rel else v[0]; out.append('L %s %s' % (fmt(x) if rel else raw[0], fmt(y)))
            elif U == 'V':
                y = y + v[0] if rel else v[0]; out.append('L %s %s' % (fmt(x), fmt(y) if rel else raw[0]))
            elif U == 'C':
                p = [(x + v[k], y + v[k + 1]) for k in (0, 2, 4)] if rel else [(v[k], v[k + 1]) for k in (0, 2, 4)]
                out.append('C ' + (' '.join('%s %s' % (fmt(a), fmt(b)) for a, b in p) if rel else ' '.join(raw))); x, y = p[2]
            elif U == 'Q':
                p = [(x + v[k], y + v[k + 1]) for k in (0, 2)] if rel else [(v[k], v[k + 1]) for k in (0, 2)]
                out.append('Q ' + (' '.join('%s %s' % (fmt(a), fmt(b)) for a, b in p) if rel else ' '.join(raw))); x, y = p[1]
            elif U == 'A':
                ex, ey = (x + v[5], y + v[6]) if rel else (v[5], v[6])
                out.append('A %s %s %s %s %s %s %s' % (tuple(raw[:5]) + ((fmt(ex), fmt(ey)) if rel else tuple(raw[5:])))); x, y = ex, ey
        s = ' '.join(out)
    if close and not s.rstrip().endswith(('Z', 'z')): s = s.rstrip() + ' Z'
    return s


# ---------------------------------------------------------------- reading and writing the page
def dumps(o, style):
    return json.dumps(o, separators=(',', ':'), ensure_ascii=False) if style == 'tight' else json.dumps(o, ensure_ascii=False)


def find(s, key):
    """(start, end, drawing, style) of the one drawing with this id in the page"""
    dec = json.JSONDecoder(); hits = []
    for m in re.finditer(r'\{"format":\s*"stepby/1"', s):
        o, end = dec.raw_decode(s, m.start())
        if o.get('id') == key: hits.append((m.start(), end, o))
    assert len(hits) == 1, (key, len(hits))
    a, b, o = hits[0]
    style = 'tight' if s[a:b] == dumps(o, 'tight') else 'loose' if s[a:b] == dumps(o, 'loose') else None
    assert style, (key, 'the page writes this drawing in a way this would not write it back')
    return a, b, o, style


def set_card(s, key, old_n, new_n):
    """the card's number of steps (drawings in NEWD count their own steps, so they have no number to change)"""
    pat = re.compile(r'(REALS\.draw\.push\(\{[^}]*?steps:)(\d+)(,key:"%s",)' % re.escape(key))
    found = pat.findall(s)
    if not found:
        assert key.startswith('dn_'), (key, 'no card found')
        return s
    assert len(found) == 1 and int(found[0][1]) == old_n, (key, found)
    return pat.sub(lambda m: m.group(1) + str(new_n) + m.group(3), s)


def plan_find(p, key):
    head = 'MIM.reg("%s",' % key
    if p.count(head) == 0: return None
    assert p.count(head) == 1, key
    i = p.index(head) + len(head); o, end = json.JSONDecoder().raw_decode(p, i)
    assert p[i:end] == dumps(o, 'tight'), (key, 'the plan is written in a way this would not write it back')
    return i, end, o


def plan_remap(plan, mp, steps_of):
    """every step.shape in a plan (counted from 0) follows mp; "n.*" becomes the new step(s) its shapes went to"""
    def fix(v):
        if isinstance(v, dict): return {k: fix(x) for k, x in v.items()}
        if isinstance(v, list):
            out = []
            for x in v:
                if isinstance(x, str) and re.fullmatch(r'\d+\.\*', x):
                    new = steps_of[int(x.split('.')[0])]
                    assert new, ('a part named a step that has gone', x)
                    out += ['%d.*' % n for n in new]
                elif isinstance(x, str) and re.fullmatch(r'\d+\.\d+', x):
                    assert mp[x] is not None, ('a part named a shape that has gone', x)
                    out.append(mp[x])
                else:
                    out.append(fix(x))
            return out
        if isinstance(v, str) and re.fullmatch(r'\d+\.(\d+|\*)', v):
            raise AssertionError(('a step.shape outside a list; not handled', v))
        return v
    return fix(plan)


# ---------------------------------------------------------------- the fixes
def split(D, edits):
    D = json.loads(json.dumps(D)); mp = {}; steps_of = {}; steps = []
    titles = [st['title'] for st in D['steps']]
    for t, n, parts in edits:
        assert titles.count(t) == 1, ('expected one step called', t, titles)
        st = D['steps'][titles.index(t)]
        assert len(st['add']) == n, (t, len(st['add']), n)
        assert sorted(i for p in parts for i in p[3]) == list(range(n)), (t, 'every shape must go to exactly one new step')
        assert sorted(st['use']) == sorted({p[2] for p in parts}), (t, st['use'], [p[2] for p in parts])
    by = {t: parts for t, n, parts in edits}
    for si, st in enumerate(D['steps']):
        if st['title'] not in by:
            for ii in range(len(st['add'])): mp['%d.%d' % (si, ii)] = '%d.%d' % (len(steps), ii)
            steps_of[si] = [len(steps)]; steps.append(st); continue
        steps_of[si] = []
        for title, text, pencil, idx in by[st['title']]:
            assert len(text) <= 160, (title, len(text))
            new = {'title': title, 'text': text, 'use': [pencil], 'add': [st['add'][i] for i in idx]}
            fills = {(a.get('fill') or '').lower() or None for a in new['add']}
            if pencil == 'pencil': assert fills == {None}, (title, 'a line step with colour in it', fills)
            else: assert None not in fills and len(fills) == 1, (title, 'a colour step needs one colour', fills)
            for k, i in enumerate(idx): mp['%d.%d' % (si, i)] = '%d.%d' % (len(steps), k)
            steps_of[si].append(len(steps)); steps.append(new)
    D['steps'] = steps
    return D, mp, steps_of


def drop(D, title, n):
    D = json.loads(json.dumps(D)); mp = {}; steps_of = {}; steps = []
    titles = [st['title'] for st in D['steps']]
    assert titles.count(title) == 1 and len(D['steps'][titles.index(title)]['add']) == n, (title, titles)
    for si, st in enumerate(D['steps']):
        if st['title'] == title:
            for ii in range(len(st['add'])): mp['%d.%d' % (si, ii)] = None
            steps_of[si] = []; continue
        for ii in range(len(st['add'])): mp['%d.%d' % (si, ii)] = '%d.%d' % (len(steps), ii)
        steps_of[si] = [len(steps)]; steps.append(st)
    D['steps'] = steps
    return D, mp, steps_of


def shape(D, ref):
    s, i = (int(x) for x in ref.split('.'))
    return D['steps'][s - 1]['add'][i - 1]


def gaps(D, key):
    for g in GAPS:
        if g[0] != key: continue
        under, top = shape(D, g[1]), shape(D, g[2])
        assert 'fill' in under and 'fill' in top and under['fill'].lower() != top['fill'].lower(), g
        cuts = under.setdefault('cut', [])
        assert top['d'] not in cuts, (g, 'already has this gap')
        if len(g) > 3:
            old = cuts[g[3]]
            assert old not in [a['d'] for st in D['steps'] for a in st['add'] if 'fill' in a], (g, 'the cut to swap is already filled by a colour')
            cuts[g[3]] = top['d']
        else:
            cuts.append(top['d'])
    return D


def paths(D):
    for st in D['steps']:
        for it in st['add']:
            f = 'fill' in it
            it['d'] = absolute(it['d'], close=f)
            if 'cut' in it: it['cut'] = [absolute(c, close=True) for c in it['cut']]
    return D


def texts(D, key):
    for k, n, old, new in TEXTS:
        if k != key: continue
        st = D['steps'][n - 1]
        assert st['text'] == old, (key, n, st['text'])
        assert len(new) <= 160, (key, n, len(new))
        st['text'] = new
    return D


def check_steps(D, fxs):
    """every step adds something; after a split or a drop, every step uses one pencil"""
    for i, st in enumerate(D['steps']):
        assert st['add'] and st['title'] and st['text'], (D['id'], i + 1, st['title'])
        if any(fx in SPLITS or fx in DROPS for fx in fxs): assert len(st['use']) == 1, (D['id'], i + 1, st['title'], st['use'])


def run(f_page, f_plans, chosen):
    s = open(f_page, encoding='utf-8').read(); p = open(f_plans, encoding='utf-8').read()
    keys = {}
    for fx in chosen:
        if fx in SPLITS: keys.setdefault(SPLITS[fx][0], []).append(fx)
        elif fx in DROPS: keys.setdefault(DROPS[fx][0], []).append(fx)
        elif fx == 'colours':
            for g in GAPS: keys.setdefault(g[0], []).append(fx) if fx not in keys.get(g[0], []) else None
        elif fx == 'paths':
            for k in PATHS: keys.setdefault(k, []).append(fx)
        elif fx == 'texts':
            for t in TEXTS: keys.setdefault(t[0], []).append(fx)
        else:
            raise SystemExit('not a fix name: %s (try --list)' % fx)
    for key, fxs in keys.items():
        a, b, D, style = find(s, key); n0 = len(D['steps']); N = D; maps = []
        for fx in fxs:
            if fx in SPLITS:
                N, mp, so = split(N, SPLITS[fx][1]); maps.append((mp, so))
            elif fx in DROPS:
                N, mp, so = drop(N, DROPS[fx][1], DROPS[fx][2]); maps.append((mp, so))
            elif fx == 'colours': N = gaps(json.loads(json.dumps(N)), key)
            elif fx == 'paths': N = paths(json.loads(json.dumps(N)))
            elif fx == 'texts': N = texts(json.loads(json.dumps(N)), key)
        check_steps(N, fxs)
        s = s[:a] + dumps(N, style) + s[b:]
        if len(N['steps']) != n0: s = set_card(s, key, n0, len(N['steps']))
        line = '%-18s %-22s %2d -> %2d steps' % (key, '+'.join(fxs), n0, len(N['steps']))
        if maps:
            pl = plan_find(p, key)
            if pl:
                i, end, P = pl; Q = P
                for mp, so in maps: Q = plan_remap(Q, mp, so)
                for k, (old, new) in DROP_PLAN_WORDS.get(key, {}).items():
                    if any(fx in DROPS for fx in fxs):
                        assert Q[k].count(old) == 1, (key, k); Q = dict(Q); Q[k] = Q[k].replace(old, new)
                p = p[:i] + dumps(Q, 'tight') + p[end:]
                line += ' | Make it move plan kept in step'
        print(line)
    open(f_page, 'w', encoding='utf-8').write(s); open(f_plans, 'w', encoding='utf-8').write(p)


if __name__ == '__main__':
    if sys.argv[1:] == ['--list']:
        print(__doc__); print('fixes:', ' '.join(FIXES))
    else:
        run(sys.argv[1], sys.argv[2], sys.argv[3:] or FIXES)
