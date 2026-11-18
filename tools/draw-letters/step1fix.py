"""Step 1 fixes (18 Nov 2026): step 1 of 16 drawings now draws a natural-looking letter or number.

Each fix cuts the step-1 lines so their first part is a normal letter shape. The rest of each line is drawn in the step
that carries on from it (only T is for Tap gets one new step). The finished picture does not change at all.
They are live in the app already. Use this only if one of these drawings is rebuilt from its build script, so the
rebuilt drawing gets the same fix again (it finds the fix from the drawing's id and checks the old lines first):

    python3 step1fix.py out/tap.json [more.json ...]      # fixes each file in place
"""
import json, math, re, sys

TOK = re.compile(r'[MLCZ]|-?\d*\.?\d+(?:e-?\d+)?')


def r2(v):
    v = round(v + 0.0, 2)
    return 0.0 if v == 0 else v


def fmt(v):
    t = ('%.2f' % r2(v)).rstrip('0').rstrip('.')
    return '0' if t in ('-0', '') else t


def parse(d):
    """-> list of pieces [(kind, points)], kind 'L' (2 pts) or 'C' (4 pts); only single-subpath M/L/C paths."""
    t = TOK.findall(d); i = 0; cur = None; out = []; cmd = None
    assert t[0] == 'M', d
    while i < len(t):
        if t[i] in 'MLCZ':
            cmd = t[i]; i += 1
            if cmd == 'Z':
                raise ValueError('closed path: ' + d)
            continue
        if cmd == 'M':
            assert cur is None, 'one subpath only: ' + d
            cur = (float(t[i]), float(t[i + 1])); i += 2; cmd = 'L'
        elif cmd == 'L':
            p = (float(t[i]), float(t[i + 1])); i += 2
            out.append(('L', [cur, p])); cur = p
        elif cmd == 'C':
            c1 = (float(t[i]), float(t[i + 1])); c2 = (float(t[i + 2]), float(t[i + 3])); p = (float(t[i + 4]), float(t[i + 5])); i += 6
            out.append(('C', [cur, c1, c2, p])); cur = p
    return out


def write(pieces):
    s = 'M %s %s' % (fmt(pieces[0][1][0][0]), fmt(pieces[0][1][0][1]))
    for k, pts in pieces:
        s += ' ' + k + ' ' + ' '.join('%s %s' % (fmt(x), fmt(y)) for x, y in pts[1:])
    return s


def bez(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p; u = 1 - t
    return (u*u*u*x0 + 3*u*u*t*x1 + 3*u*t*t*x2 + t*t*t*x3, u*u*u*y0 + 3*u*u*t*y1 + 3*u*t*t*y2 + t*t*t*y3)


def split_c(p, t):
    a, b, c, d = p
    lerp = lambda P, Q: (P[0] + (Q[0] - P[0]) * t, P[1] + (Q[1] - P[1]) * t)
    ab, bc, cd = lerp(a, b), lerp(b, c), lerp(c, d)
    abc, bcd = lerp(ab, bc), lerp(bc, cd); m = lerp(abc, bcd)
    m = (r2(m[0]), r2(m[1]))
    rnd = lambda q: (r2(q[0]), r2(q[1]))
    return [a, rnd(ab), rnd(abc), m], [m, rnd(bcd), rnd(cd), d]


def cut(d, where):
    """Cut path d at points along it. where: list of (piece index, t) with t in (0,1], or a point (x, y) that is a
    vertex or lies on a straight piece. Returns the list of path texts between the cuts, in order."""
    pcs = parse(d)
    marks = []
    for w in where:
        if isinstance(w[0], int):
            marks.append(w)
        else:
            x, y = w; found = None
            for i, (k, pts) in enumerate(pcs):
                a, b = pts[0], pts[-1]
                if math.dist(b, (x, y)) < 1e-6: found = (i, 1.0); break
                if k == 'L':
                    L = math.dist(a, b); da = math.dist(a, (x, y)); db = math.dist((x, y), b)
                    if abs(da + db - L) < 1e-6 and 0 < da < L: found = (i, da / L); break
            assert found, ('point not on path', w, d)
            marks.append(found)
    marks.sort()
    out = []; curr = []; i = 0; rest = None
    for i, (k, pts) in enumerate(pcs):
        piece = (k, list(pts))
        mine = [t for (j, t) in marks if j == i]
        t0 = 0.0
        for t in mine:
            if t >= 1.0 - 1e-9:
                curr.append(piece); out.append(curr); curr = []; piece = None; break
            tt = (t - t0) / (1 - t0)
            if piece[0] == 'L':
                a, b = piece[1]; m = (r2(a[0] + (b[0] - a[0]) * tt), r2(a[1] + (b[1] - a[1]) * tt))
                curr.append(('L', [a, m])); out.append(curr); curr = []; piece = ('L', [m, b])
            else:
                p1, p2 = split_c(piece[1], tt)
                curr.append(('C', p1)); out.append(curr); curr = []; piece = ('C', p2)
            t0 = t
        if piece is not None: curr.append(piece)
    if curr: out.append(curr)
    return [write(p) for p in out]


def line_d(*pts):
    return 'M %s %s' % (fmt(pts[0][0]), fmt(pts[0][1])) + ''.join(' L %s %s' % (fmt(x), fmt(y)) for x, y in pts[1:])


def rev_d(d):
    pcs = parse(d)
    out = [(k, pts[::-1]) for k, pts in pcs[::-1]]
    return write(out)


def join_d(*ds):
    """Join paths end to start into one stroke."""
    pcs = []
    for d in ds:
        p = parse(d)
        if pcs: assert math.dist(pcs[-1][1][-1], p[0][1][0]) < 1e-6, ('not joined', ds)
        pcs += p
    return write(pcs)


def ln(d, w=1.8):
    return {'d': d, 'w': w}


def lines(st):
    return [a['d'] for a in st['add']]


FIXES = {}


def fix(key, why):
    def deco(f):
        FIXES[key] = (f, why)
        return f
    return deco


def set1(P, items, text):
    """Replace step 1's line items (keeps the title)."""
    P['steps'][0]['add'] = [ln(d) for d in items]
    P['steps'][0]['text'] = text


def insert2(P, title, text, items):
    P['steps'].insert(1, {'title': title, 'use': ['pencil'], 'text': text, 'add': [ln(d) for d in items]})


def set2(P, items, text, title=None):
    P['steps'][1]['add'] = [ln(d) for d in items]
    P['steps'][1]['text'] = text
    if title: P['steps'][1]['title'] = title


@fix('dx_fireplace_f', 'The bars of the F are as long as the F is tall, so it looks very wide.')
def _(P):
    s1 = lines(P['steps'][0]); s2 = lines(P['steps'][1])
    stem, top, mid = s1
    assert top == 'M 28.38 40.6 L 71.62 40.6' and mid == 'M 28.38 56.81 L 61.75 56.81'
    assert s2 == ['M 71.62 40.6 L 71.62 83.84', 'M 61.75 56.81 L 71.62 56.81']
    t1, t2 = cut(top, [(54.32, 40.6)]); m1, m2 = cut(mid, [(50.0, 56.81)])
    set1(P, [stem, t1, m1], 'Draw a capital F: a straight line down, a bar across the top and a slightly shorter bar under it. This F is hiding in the fireplace.')
    set2(P, [join_d(t2, s2[0]), join_d(m2, s2[1])],
         'Make the top bar longer. From its end, draw a straight line down, as far as the bottom of the F. Then make the shorter bar longer, so it touches that line.')


@fix('dx_electrictrain_e', 'The arms of the E are longer than the E is tall, so it looks stretched.')
def _(P):
    s1 = lines(P['steps'][0]); s2 = lines(P['steps'][1])
    assert s1 == ['M 62 31 L 14 31 L 14 71 L 62 71', 'M 14 51 L 59 51']
    a, b, c = cut(s1[0], [(38.0, 31.0), (38.0, 71.0)])     # top extension, the E's top+stem+bottom, bottom extension
    m1, m2 = cut(s1[1], [(36.0, 51.0)])
    set1(P, [b, m1], 'Draw a capital E: a straight line down, with three arms going right. Make the middle arm a little shorter.')
    set2(P, [join_d(rev_d(a), s2[0], rev_d(c)), m2],
         'Make the top arm longer, then curve down for the nose. Go straight down and back along the bottom to the E. Make the middle arm longer too.')


@fix('dx_heron_h', 'The H is very tall and thin, so it looks like two sticks.')
def _(P):
    s1 = lines(P['steps'][0])
    assert s1 == ['M 44 38 L 44 86', 'M 56 38 L 56 86', 'M 44 62 L 56 62']
    la, lb, lc = cut(s1[0], [(44.0, 53.5), (44.0, 70.5)])
    ra, rb, rc = cut(s1[1], [(56.0, 53.5), (56.0, 70.5)])
    s2 = lines(P['steps'][1])
    assert s2 == ['M 44 38 L 47 34 L 47 22.42', 'M 56 38 L 53 34 L 53 22.42'] and P['steps'][7]['title'] == 'The feet'
    set1(P, [lb, rb, s1[2]], 'Draw a small capital H: two short straight sticks with a line across the middle. This H is hiding in the heron.')
    set2(P, [join_d(rev_d(la), s2[0]), join_d(rev_d(ra), s2[1])],
         'Make each stick of the H taller. Then draw a short line leaning in, and go straight up. This is the long neck.')
    P['steps'][7]['add'] = [ln(lc), ln(rc)] + P['steps'][7]['add']
    P['steps'][7]['text'] = 'Make the two sticks of the H longer, down to the bottom. These are the legs. Then add three toes on each foot.'


@fix('dx_lorry_l', 'The foot of the L is longer than the L is tall.')
def _(P):
    s1 = lines(P['steps'][0]); s2 = lines(P['steps'][1])
    assert s1 == ['M 37 17.5 L 37 63.5', 'M 37 63.5 L 85 63.5'] and s2 == ['M 37 17.5 L 85 17.5 L 85 63.5']
    f1, f2 = cut(s1[1], [(62.0, 63.5)])
    set1(P, [s1[0], f1], 'Draw a capital L: a straight line down, then a shorter line going right from its foot. This L is hiding in the lorry.')
    set2(P, [join_d(s2[0], rev_d(f2))],
         'From the top of the L, draw a line across to the right and straight down. Then go back along the bottom to the end of the L. Now the L is a big box.')


@fix('dx_lunchbox_l', 'The foot of the L is much longer than the L is tall.')
def _(P):
    s1 = lines(P['steps'][0]); s2 = lines(P['steps'][1])
    assert s1 == ['M 28 15 L 28 63', 'M 28 63 L 86 63'] and s2[1] == 'M 18 63 L 28 63'
    f1, f2 = cut(s1[1], [(54.0, 63.0)])
    set1(P, [s1[0], f1], 'Draw a capital L: a straight line down, then a shorter line going right from its foot. This L is hiding in the lunchbox.')
    set2(P, [join_d(s2[0], rev_d(f2)), s2[1]],
         'From the top of the L, go left a little, down, along the bottom and up. Then go back along to the end of the L. Join the L’s corner to the left side.')


@fix('dx_tap_t', 'The top of the T is twice as wide as the T is tall.')
def _(P):
    s1 = lines(P['steps'][0])
    assert s1 == ['M 31.08 11.92 L 75.88 11.92', 'M 53.48 11.92 L 53.48 33.2']
    a, b, c = cut(s1[0], [(43.88, 11.92), (63.08, 11.92)])
    set1(P, [b, s1[1]], 'Draw a capital T near the top.')
    insert2(P, 'The water pipe', 'Make the top line of the T longer at both ends. It is the water pipe.', [rev_d(a), c])


@fix('dx_tiger_t', 'The top of the T is twice as wide as the T is tall.')
def _(P):
    s1 = lines(P['steps'][0])
    assert s1 == ['M 37.9 52.75 L 62.1 52.75', 'M 50 52.75 L 50 64.85']
    a, b, c = cut(s1[0], [(44.5, 52.75), (55.5, 52.75)])
    m = P['steps'][5]; assert m['title'] == 'The muzzle'
    mz = lines(m); assert mz[0].startswith('M 37.9 52.75 C') and mz[1].startswith('M 62.1 52.75 C')
    set1(P, [b, s1[1]], 'Draw a small capital T in the middle of your paper, a little low down.')
    m['add'] = [ln(join_d(rev_d(a), mz[0])), ln(join_d(c, mz[1]))]
    m['text'] = 'Make the T’s top line longer at each end. Then draw a curved line from each end down to the bottom of the circle.'


@fix('dx_train_t', 'The top of the T is a bit too long for its height.')
def _(P):
    s1 = lines(P['steps'][0]); s2 = lines(P['steps'][1])
    assert s1[0] == 'M 57.3 32.8 L 60.5 32.8 L 74.25 32.8 L 88 32.8 L 91.2 32.8'
    a, b, c = cut(s1[0], [(60.5, 32.8), (88.0, 32.8)])
    set1(P, [b, s1[1]], 'Draw a capital T near the top, on the right. This T is hiding in the train.')
    set2(P, [join_d(rev_d(a), s2[0], rev_d(c))],
         'Make the T’s top line a little longer at each end. Then draw a line over it, with a round end at each side. Now the roof is thick.')


@fix('dx_tank_t', 'The bar of the t is wider than the t is tall.')
def _(P):
    s1 = lines(P['steps'][0])
    assert s1[1] == 'M 37 26.5 L 39.5 26.5 L 50.5 26.5 L 54.5 26.5 L 78.5 26.5'
    a, b, c = cut(s1[1], [(47.5, 26.5), (63.5, 26.5)])
    s2 = lines(P['steps'][1]); g = P['steps'][6]; gl = lines(g)
    assert s2[0].startswith('M 37 26.5 C') and g['title'] == 'The gun' and gl == ['M 78.5 26.5 L 78.5 32.7 L 54.5 32.7']
    set1(P, [s1[0], b], 'Draw a small letter t: a tall stick with a short bar across near the top, and a curl at the bottom. This t is hiding in the tank.')
    set2(P, [join_d(rev_d(a), s2[0])], 'Make the bar longer to the left. Then curve round and draw a slanting line down. This is the back of the turret.')
    g['add'] = [ln(join_d(c, gl[0]))]
    g['text'] = 'Make the bar longer to the right. Then draw a short line down, and a line back to the stick. This is the gun.'


@fix('dx_toiletroll_t', 'The bar of the t is very long, and so is the curl.')
def _(P):
    s1 = lines(P['steps'][0])
    assert s1 == ['M 35.31 18.49 L 35.31 56.91 C 35.31 65.95 40.06 68.21 46.38 68.21 L 51.13 68.21', 'M 19.49 32.05 L 63.56 32.05']
    st1, st2 = cut(s1[0], [(46.38, 68.21)])
    a, b, c = cut(s1[1], [(24.31, 32.05), (48.31, 32.05)])
    sp = P['steps'][5]; assert sp['title'] == 'A spare roll'
    set1(P, [st1, b], 'Draw a small letter t: a tall stick with a bar across, and a curl to the right at the bottom.')
    P['steps'][1]['add'] = [ln(st2)] + P['steps'][1]['add']
    P['steps'][1]['text'] = 'Make the curl a little longer. At its end, draw a long box with a round end. It is the roll, sitting on the holder.'
    sp['add'] = [ln(rev_d(a)), ln(c)] + sp['add']
    sp['text'] = 'Make the bar of the t longer at both ends. Then stand a spare roll on it: two lines up from the bar and an oval on top.'


@fix('dx_jamjar_j', 'The hook of the j goes a long way left, so it looks like a hockey stick.')
def _(P):
    s1 = lines(P['steps'][0]); s2 = lines(P['steps'][1])
    hook = s1[0]
    assert hook.startswith('M 71 31.5 L 71 73.5 C 71 81.23 64.28 87.5 56 87.5 L 44 87.5') and s2[0].startswith('M 33.39 83.4')
    h1, h2 = cut(hook, [(56.0, 87.5)])
    set1(P, [h1, s1[1]], 'Draw a small letter j: a straight line down that curls round to the left at the bottom, and a dot above it. This j is hiding in the jam jar.')
    set2(P, [join_d(h2, s2[0])],
         'From the end of the curl, carry on along the bottom. Curve up, then draw a straight line up, as high as the top of the stick. Now you can see the jar.')


@fix('dx_dumper_d', 'The stick of the d is very tall, more than twice the height of the round part.')
def _(P):
    s1 = lines(P['steps'][0]); s2 = lines(P['steps'][1])
    assert s1[1] == 'M 67 18.5 L 67 84.5' and s2[0].startswith('M 67 18.5 L 90 18.5')
    a, b = cut(s1[1], [(67.0, 37.5)])
    set1(P, [s1[0], b], 'Draw a small letter d: a round shape with a straight stick on its right-hand side, touching it. This d is hiding in the dumper truck.')
    set2(P, [join_d(rev_d(a), s2[0])],
         'Make the stick taller. From its top, go across, down the far side and back along the bottom to the foot of the stick.')


@fix('dx_swan_2', 'The bottom line of the 2 is very long, so the 2 looks stretched.')
def _(P):
    s1 = lines(P['steps'][0])
    assert s1[0].endswith('L 20 75 L 85 75')
    a, b = cut(s1[0], [(54.0, 75.0)])
    st = P['steps'][2]; bk = lines(st); assert st['title'] == 'The back and tail' and bk[0].endswith('85 75')
    set1(P, [a], 'Draw a big 2: round over the top, a long straight line down to the left, then a line along the bottom.')
    st['add'] = [ln(join_d(bk[0], rev_d(b)))] + st['add'][1:]
    st['text'] = 'Draw the back along to a pointy tail. Then go down to the bottom, and along to the end of the 2.'


@fix('dx_shark_7', 'The top of the 7 is much longer than the 7 is tall.')
def _(P):
    s1 = lines(P['steps'][0]); s2 = lines(P['steps'][1])
    assert s1 == ['M 31.4 35 L 92.4 35 L 56.4 73'] and s2[0].endswith('L 31.4 35')
    a, b = cut(s1[0], [(60.4, 35.0)])
    set1(P, [b], 'Draw a big 7: a straight line across the top, then a long slanting line down to the left.')
    set2(P, [join_d(s2[0], a)] + s2[1:],
         'From the bottom of the 7, draw the tummy round to a big pointy tail. Then draw the back up and along to the top of the 7.')


@fix('dx_pig_6', 'The top of the 6 sweeps a long way to the right, so the 6 looks like it is falling over.')
def _(P):
    s1 = lines(P['steps'][0])
    assert s1[0].startswith('M 33.33 51 C 22 50 9 59 9 71')
    a, b = cut(s1[0], [(0, 0.3)])
    st = P['steps'][2]; assert st['title'] == 'The body' and lines(st)[0].count('33.33 51') == 1
    set1(P, [b], 'Draw a big 6: start at the top, curve down to the left and round into a closed loop at the bottom.')
    st['add'] = [ln(rev_d(a))] + st['add']
    st['text'] = 'Make the top of the 6 a little longer. Then draw a big round body from the top of the head, back past the end of the 6 and round under to the head.'


@fix('dx_llama_l', 'The foot of the L is a little long for its height.')
def _(P):
    s1 = lines(P['steps'][0])
    assert s1 == ['M 42 29.6 L 42 62 L 68 62']
    a, b = cut(s1[0], [(60.0, 62.0)])
    st = P['steps'][5]; d = st['add'][0]['d']; assert st['title'].startswith('Tummy') and d.endswith('C 77 65 74 62 68 62') and b == 'M 60 62 L 68 62'
    set1(P, [a], 'Draw a capital L: a long line down, then a shorter line across. This L is hiding in the llama.')
    st['add'][0]['d'] = d + ' L 60 62'
    st['text'] = 'Draw a wavy, fluffy tummy and two back legs. Then draw a fluffy bottom curving up, and go along the back to the end of the L.'


if __name__ == '__main__':
    for path in sys.argv[1:]:
        P = json.load(open(path))
        if P['id'] not in FIXES:
            print('no step 1 fix for', P['id']); continue
        before = len(P['steps']); FIXES[P['id']][0](P)
        json.dump(P, open(path, 'w'), ensure_ascii=False)
        print('fixed', P['id'], before, '->', len(P['steps']), 'steps')
