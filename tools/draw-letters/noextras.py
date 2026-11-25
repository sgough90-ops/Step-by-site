"""Takes the little extras out of drawings that are already in the app, and moves each picture to the middle of the paper.

25 Nov 2026, his words with seven screenshots: "For these instructions the final drawing has like little bit extras on
it so for example bubbles can you take these out and if you need to realign the pictures so the main picture [is in] the
centre so for example [the] seahorse".

Seven drawings were done. Four have a build script; those scripts were changed and the drawings put back with
reapply.py: build_rocket.py (four stars gone), build_zooplankton.py (three babies and three bubbles gone),
build_quokka.py (flower and sniff lines gone) and build_xrayfish.py (three bubbles gone). The other three have no build
script (the page holds the only copy), so this file changes them where they are:

    S is for Seahorse (dx_seahorse_s)     three bubbles gone, moved 11.5 to the right
    J is for Jellyfish (dx_jellyfish_j)   three bubbles gone, moved 5 to the right
    G is for Goldfish (dx_goldfish_g)     two bubbles gone, moved 7.5 to the right and 1 up

    python3 noextras.py ../../public/draw/index.html ../../public/mim-plans.js      # what was run on 25 Nov 2026
    python3 noextras.py --middle out/<name>.json [more.json ...]                    # where the middle of a picture is

Taking an extra out: a step that only drew or only coloured extras goes; a colour step that also coloured something else
loses just the extras' shapes; a pencil no step uses any more leaves the list of pencils; the card's number of steps
follows. Then every line and colour moves by one amount, so that the middle of what is left is the middle of the paper
(to the nearest half; less than three quarters of a unit is left alone).

The seahorse is the only one of the seven with a Make it move plan (public/mim-plans.js). The plan is kept in step with
the drawing: its three bubble parts go, the step numbers after the bubble steps move down, and its pivots, points and
patches move with the picture. The white shine on its eye used to be shown "by" the first bubble (a part that is always
moving); it is now shown by "paper", which is how the other plans say "always".

It stops if a drawing is not as it expects, so it cannot be run twice by mistake.
"""
import json, os, re, sys
from decimal import Decimal

TOK = re.compile(r'[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?')
NUMS = {'M': 2, 'L': 2, 'C': 6, 'Q': 4, 'A': 7, 'Z': 0}          # how many numbers each path letter takes

# drawing -> what goes. drop: a whole step by its title, with how many shapes it has (checked first).
# trim: a step that stays but loses some shapes: title -> (how many it has now, which ones go, its new words).
EDITS = {
    'dx_seahorse_s': dict(drop={'Bubbles': 3, 'Colour the bubbles': 3}, pencils_out=['blue'], move=('11.5', '0')),
    'dx_jellyfish_j': dict(drop={'The bubbles': 3, 'Colour light blue': 3}, pencils_out=['lblue'], move=('5', '0'),
                           desc=('A happy pink jellyfish with bubbles. The capital letter J is hiding in it five times: every tentacle is a J.',
                                 'A happy pink jellyfish. The capital letter J is hiding in it five times: every tentacle is a J.')),
    'dx_goldfish_g': dict(drop={'Bubbles': 2}, pencils_out=[], move=('7.5', '-1'),
                          desc=('A goldfish blowing bubbles. The capital G is hiding in it: its big curve is the body and its bar is the bottom of the open mouth.',
                                'A goldfish with its mouth open. The capital G is hiding in it: its big curve is the body and its bar is the bottom of the open mouth.')),
}
# the seahorse's Make it move plan: the parts that go with the bubbles, and the words that talked about them
PLAN_KEY = 'dx_seahorse_s'
PLAN_GONE = ['bub1', 'bub2', 'bub3']
PLAN_WORDS = {
    'seen': (' Three blue bubbles (small, middle, big) float up and away from the tip of its snout.', ' Nothing else is drawn.'),
    'silly': (', blows its three bubbles, then gets the hiccups', ', gets the hiccups'),
    'cool': ('; its three bubbles float up from its snout to the surface, it swims', '; it swims'),
}


def dump(o):
    return json.dumps(o, separators=(',', ':'), ensure_ascii=False)


def num(v):
    t = format(v.normalize(), 'f')
    return '0' if t in ('-0', '') else t


def move_path(d, dx, dy):
    """the same path, moved; only the numbers change, the rest of the text stays as it was written"""
    dx, dy = Decimal(str(dx)), Decimal(str(dy))
    assert not re.sub(r'[\s,]', '', TOK.sub('', d)), ('something in this path is not a letter or a number', d[:80])
    out = []; pos = 0; cmd = None; k = 0
    for m in TOK.finditer(d):
        t = m.group(); out.append(d[pos:m.start()]); pos = m.end()
        if t.isalpha():
            assert t in NUMS, ('path letter not known (only M L C Q A Z)', t, d[:80])
            cmd = t; k = 0; out.append(t); continue
        j = k % NUMS[cmd]; k += 1
        by = (dx if j == 5 else dy if j == 6 else None) if cmd == 'A' else (dx if j % 2 == 0 else dy)
        out.append(t if by is None or by == 0 else num(Decimal(t) + by))
    assert cmd is None or k % max(1, NUMS[cmd]) == 0, ('a path ends half way through a point', d[:80])
    return ''.join(out) + d[pos:]


def moved(D, dx, dy):
    """a copy of a drawing with every line and colour (and every hole cut in a colour) moved"""
    D = json.loads(json.dumps(D))
    for st in D['steps']:
        for it in st['add']:
            assert set(it) <= {'d', 'w', 'fill', 'cut'}, ('a shape has something this does not know how to move', sorted(it))
            it['d'] = move_path(it['d'], dx, dy)
            if 'cut' in it: it['cut'] = [move_path(c, dx, dy) for c in it['cut']]
    return D


def without(D, drop, trim=None, pencils_out=(), desc=None):
    """a copy of a drawing without its extras -> (the drawing, {'old step.shape': 'new step.shape' or None})"""
    D = json.loads(json.dumps(D)); trim = trim or {}
    titles = [st['title'] for st in D['steps']]
    for t, n in list(drop.items()) + [(t, v[0]) for t, v in trim.items()]:
        assert titles.count(t) == 1, ('expected one step called', t, titles)
        assert len(D['steps'][titles.index(t)]['add']) == n, ('step has a different number of shapes', t, len(D['steps'][titles.index(t)]['add']), n)
    steps = []; mp = {}
    for si, st in enumerate(D['steps']):
        if st['title'] in drop:
            for ii in range(len(st['add'])): mp['%d.%d' % (si, ii)] = None
            continue
        out = None
        if st['title'] in trim:
            out = set(trim[st['title']][1]); st['text'] = trim[st['title']][2]
        keep = []
        for ii, it in enumerate(st['add']):
            if out and ii in out: mp['%d.%d' % (si, ii)] = None
            else:
                mp['%d.%d' % (si, ii)] = '%d.%d' % (len(steps), len(keep)); keep.append(it)
        assert keep, ('a trimmed step would be left with nothing', st['title'])
        st['add'] = keep; steps.append(st)
    D['steps'] = steps
    used = {u for st in steps for u in st['use']}
    gone = [m['id'] for m in D['materials'] if m.get('kind') == 'pencil' and m['id'] not in used]
    assert sorted(gone) == sorted(pencils_out), ('pencils no step uses now', gone, 'expected', list(pencils_out))
    D['materials'] = [m for m in D['materials'] if m['id'] not in gone]
    for st in steps:
        assert len(st['use']) == 1 and st['text'] and len(st['text']) <= 160, st['title']
    if desc:
        assert D['description'] == desc[0], D['description']
        D['description'] = desc[1]
    return D, mp


def fix_plan(plan, mp, dx, dy, gone_ok, words):
    """a Make it move plan kept in step with its drawing: parts whose shapes have all gone go too"""
    plan = json.loads(json.dumps(plan)); dx, dy = float(dx), float(dy)
    r2 = lambda v: int(round(v, 2)) if float(round(v, 2)).is_integer() else round(v, 2)      # 50 stays 50, not 50.0
    parts = []; gone = []
    for pt in plan['parts']:
        if isinstance(pt.get('items'), list):
            assert all(re.fullmatch(r'\d+\.\d+', r) for r in pt['items']), ('only plain step.shape numbers are handled', pt['id'], pt['items'])
            new = [mp[r] for r in pt['items']]
            if all(n is None for n in new):
                gone.append(pt['id']); continue
            assert all(n is not None for n in new), ('a part would keep some shapes and lose others', pt['id'])
            pt['items'] = new
        else:
            assert pt.get('items') == 'rest', pt
        if pt.get('pivot'): pt['pivot'] = [r2(pt['pivot'][0] + dx), r2(pt['pivot'][1] + dy)]
        assert set(pt) <= {'id', 'role', 'parent', 'behind', 'items', 'pivot', 'under', 'motion'}, ('a part has something this does not know about', sorted(pt))
        for m in pt.get('motion', []):                     # every move here is "by so much", never "to a place"
            assert m['type'] in ('bob', 'extend', 'wag', 'blink', 'show', 'lift'), ('check whether this move names a place on the paper', m)
        parts.append(pt)
    assert gone == gone_ok, (gone, gone_ok)
    assert not [pt['id'] for pt in parts if pt.get('parent') in gone], 'a part hangs on a part that has gone'
    plan['parts'] = parts
    plan['points'] = {k: [r2(v[0] + dx), r2(v[1] + dy)] for k, v in plan.get('points', {}).items()}
    for pa in plan.get('patches', []):
        assert set(pa) <= {'part', 'by', 'd', 'fill'}, sorted(pa)
        assert pa['part'] not in gone
        pa['d'] = move_path(pa['d'], dx, dy)
        if pa.get('by') in gone: pa['by'] = 'paper'
    for k, (old, new) in words.items():
        assert plan[k].count(old) == 1, (k, old)
        plan[k] = plan[k].replace(old, new)
    assert set(plan) <= {'v', 'seen', 'kind', 'scene', 'opt', 'points', 'parts', 'patches', 'silly', 'cool', 'wish'}, sorted(plan)
    return plan


def middle(D):
    """(left, top, right, bottom) of everything in a drawing, lines with half their width, and its middle"""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import check as C
    xs = []; ys = []
    for st in D['steps']:
        for it in st['add']:
            h = 0 if 'fill' in it else it.get('w', 1.8) * 0.3
            for d in [it['d']] + it.get('cut', []):
                for pts, closed in C.parse(d, 0.2):
                    xs += [p[0] - h for p in pts] + [p[0] + h for p in pts]; ys += [p[1] - h for p in pts] + [p[1] + h for p in pts]
    b = (min(xs), min(ys), max(xs), max(ys))
    return b, ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)


def half(v):
    """how far to move one way: to the nearest half, and not at all for less than three quarters of a unit"""
    return 0.0 if abs(v) < 0.75 else round(v * 2) / 2


def page(f_page, f_plans):
    s = open(f_page, encoding='utf-8').read(); plans = open(f_plans, encoding='utf-8').read(); maps = {}
    for key, E in EDITS.items():
        head = 'DX.reg("%s",' % key
        assert s.count(head) == 1, (key, s.count(head))
        i = s.index(head) + len(head); D, end = json.JSONDecoder().raw_decode(s, i)
        assert s[i:end] == dump(D), (key, 'the page writes this drawing in a way this would not write it back')
        N, mp = without(D, E['drop'], E.get('trim'), E['pencils_out'], E.get('desc'))
        N = moved(N, *E['move']); maps[key] = mp
        s = s[:i] + dump(N) + s[end:]
        card = re.compile(r'(REALS\.draw\.push\(\{t:"[^"]*",lvl:\d+,time:\d+,theme:"[^"]*",eq:\["pencil","colour"\],steps:)(\d+)(,key:"%s",type:"draw",)' % re.escape(key))
        found = card.findall(s)
        assert len(found) == 1 and int(found[0][1]) == len(D['steps']), (key, found)
        s = card.sub(lambda m: m.group(1) + str(len(N['steps'])) + m.group(3), s)
        print('%-16s %2d steps -> %2d | moved %s, %s | pencils out: %s' % (key, len(D['steps']), len(N['steps']), E['move'][0], E['move'][1], ', '.join(E['pencils_out']) or 'none'))
    head = 'MIM.reg("%s",' % PLAN_KEY
    assert plans.count(head) == 1
    i = plans.index(head) + len(head); P, end = json.JSONDecoder().raw_decode(plans, i)
    assert plans[i:end] == dump(P), 'the plan is written in a way this would not write it back'
    Q = fix_plan(P, maps[PLAN_KEY], *EDITS[PLAN_KEY]['move'], PLAN_GONE, PLAN_WORDS)
    plans = plans[:i] + dump(Q) + plans[end:]
    print('%-16s Make it move plan: %d parts -> %d' % (PLAN_KEY, len(P['parts']), len(Q['parts'])))
    open(f_page, 'w', encoding='utf-8').write(s); open(f_plans, 'w', encoding='utf-8').write(plans)


if __name__ == '__main__':
    if sys.argv[1] == '--middle':
        for f in sys.argv[2:]:
            b, c = middle(json.load(open(f)))
            print('%-34s left %.1f top %.1f right %.1f bottom %.1f | middle (%.2f, %.2f) | to centre it, move by (%+.1f, %+.1f)' % (
                os.path.basename(f), b[0], b[1], b[2], b[3], c[0], c[1], half(50 - c[0]), half(50 - c[1])))
    else:
        page(sys.argv[1], sys.argv[2])
