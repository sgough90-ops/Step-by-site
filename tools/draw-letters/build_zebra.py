"""Z is for zebra (dx_zebra_z), Animals A to Z, slot Z. From Claude's round-3 sketch 'Zebra (galloping)' (21 Nov 2026).
Idea from Art for Kids Hub's zebra from a capital Z (-_6dvQhJDLE).

The top line of the Z is the top of its head, the slanting line is the back of its neck (its mane sits just behind it)
and the bottom line is its back. Every stripe is its own shape whose ends sit on an outline, so it can be coloured,
and the stripes stop just short of the Z so nothing crosses it.
Sketch coordinates (200 x 200) are turned into the app's 100 x 100 paper by T().
"""
import re
from kit15 import *

OX, OY = 0.0, 3.0
def T(x, y):
    return P(x * 0.5 + OX, y * 0.5 + OY)

def chain(d):
    toks = re.findall(r'[MCL]|-?\d+\.?\d*', d)
    out = []; cur = None; i = 0; cmd = None
    while i < len(toks):
        t = toks[i]
        if t in 'MCL':
            cmd = t; i += 1; continue
        if cmd == 'M':
            cur = T(float(toks[i]), float(toks[i + 1])); i += 2
        elif cmd == 'C':
            c1 = T(float(toks[i]), float(toks[i + 1])); c2 = T(float(toks[i + 2]), float(toks[i + 3])); p = T(float(toks[i + 4]), float(toks[i + 5]))
            out.append(Seg(cur, c1, c2, p)); cur = p; i += 6
        elif cmd == 'L':
            p = T(float(toks[i]), float(toks[i + 1])); out.append(Seg(cur, p)); cur = p; i += 2
    return out

def refine(ch, cuts):
    """Cut a chain at several (piece, t) places. Returns the new chain and, for each cut name, the index of the piece that starts there."""
    by = {}
    for name, (i, t) in cuts.items():
        by.setdefault(i, []).append((t, name))
    new, node = [], {}
    for i, s in enumerate(ch):
        if i in by:
            lst = sorted(by[i]); pieces = split_many(s, [t for t, _ in lst])
            for k, (t, name) in enumerate(lst):
                new.append(pieces[k]); node[name] = len(new)
            new.append(pieces[-1])
        else:
            new.append(s)
    chain_ok(new)
    return new, node

def at_y(ch, y, lo=0):
    """(piece, t) where a chain first crosses height y, starting from piece lo."""
    for i in range(lo, len(ch)):
        ys = [ch[i].at(k / 200)[1] for k in range(201)]
        for k in range(200):
            if (ys[k] - y) * (ys[k + 1] - y) <= 0 and ys[k] != ys[k + 1]:
                return i, seg_y(ch[i], y, k / 200, (k + 1) / 200)
    raise ValueError(y)

def at_x(ch, x, lo=0):
    for i in range(lo, len(ch)):
        xs = [ch[i].at(k / 200)[0] for k in range(201)]
        for k in range(200):
            if (xs[k] - x) * (xs[k + 1] - x) <= 0 and xs[k] != xs[k + 1]:
                return i, seg_x(ch[i], x, k / 200, (k + 1) / 200)
    raise ValueError(x)

def hit(ch, p, q, near):
    """(piece, t) where the straight line p->q meets the chain, the meeting place nearest to the point near."""
    best = None
    for i, s in enumerate(ch):
        for t, pt in line_hits_seg(p, q, s):
            d = math.dist(pt, near)
            if best is None or d < best[0]:
                best = (d, i, t)
    assert best is not None and best[0] < 12, best
    return best[1], best[2]

BLACK, GREY = FILL['black'], FILL['grey']

# ---- the Z (sketch coordinates) ----
ZTL, ZTR, ZBL, ZBR = (36, 42), (98, 42), (60, 100), (132, 100)
z_letter = [Seg(T(*ZTL), T(*ZTR)), Seg(T(*ZTR), T(*ZBL)), Seg(T(*ZBL), T(*ZBR))]
_dl = math.hypot(ZBL[0] - ZTR[0], ZBL[1] - ZTR[1])
ZD = ((ZBL[0] - ZTR[0]) / _dl, (ZBL[1] - ZTR[1]) / _dl)
ZN = (-ZD[1], ZD[0]) if -ZD[1] > 0 else (ZD[1], -ZD[0])        # across the slanting line, towards the mane side
def zpt(t, off):
    return (ZTR[0] + (ZBL[0] - ZTR[0]) * t + ZN[0] * off, ZTR[1] + (ZBL[1] - ZTR[1]) * t + ZN[1] * off)
def zx(y, inset=3.8):
    """x of the point inset sketch units in front of the slanting line, at height y (the line carried on below its end)"""
    t = (y - ZTR[1] + ZN[1] * inset) / (ZBL[1] - ZTR[1])
    return ZTR[0] + (ZBL[0] - ZTR[0]) * t - ZN[0] * inset

# ---- outline: face (Z corner to chin), then neck, tummy and bottom (chin to the end of the Z) ----
face = chain('M36,42 C28,42 22,48 21,56 C20,66 20,76 26,82 C30,86 34,88 40,88')
body = chain('M40,88 C34,98 28,108 26,118 C24,126 24,132 28,137 C56,142 104,142 128,138 C142,136 150,126 150,116 C150,106 144,100 132,100')
assert face[0].a == T(*ZTL) and body[-1].b == T(*ZBR) and face[-1].b == body[0].a
NOSE_TOP, CHIN = face[0].b, face[-1].b                   # (21,56) and (40,88)
muzzle = chain('M40,88 C40,80 36,66 30,59 C27,56 23,55 21,56')
assert muzzle[0].a == CHIN and muzzle[-1].b == NOSE_TOP

# ---- legs: bent, from the body outline to the hoof ----
LEGS = {   # name: (top, knee, hoof, width, band on the upper part, band on the lower part)
    'near front': ((38, 130), (18, 142), (16, 162), 12.5, (.72, .86), (.36, .5)),
    'far front': ((56, 136), (50, 154), (58, 170), 11, (.5, .66), (.36, .5)),
    'far back': ((112, 138), (120, 156), (108, 170), 11, (.5, .66), (.36, .5)),
    'near back': ((128, 134), (150, 148), (166, 160), 12.5, (.72, .86), (.36, .5)),
}
HOOF = .8

def xline(p, q, r, s):
    """where line p-q meets line r-s"""
    d = (q[0] - p[0]) * (s[1] - r[1]) - (q[1] - p[1]) * (s[0] - r[0])
    u = ((r[0] - p[0]) * (s[1] - r[1]) - (r[1] - p[1]) * (s[0] - r[0])) / d
    return (p[0] + u * (q[0] - p[0]), p[1] + u * (q[1] - p[1]))

legcuts = {}; legplan = {}
for nm, (p0, kn, hf, w, b1, b2) in LEGS.items():
    sides = {}
    for sg in (1, -1):
        d1 = (kn[0] - p0[0], kn[1] - p0[1]); l1 = math.hypot(*d1); n1 = (-d1[1] / l1 * sg * w / 2, d1[0] / l1 * sg * w / 2)
        d2 = (hf[0] - kn[0], hf[1] - kn[1]); l2 = math.hypot(*d2); n2 = (-d2[1] / l2 * sg * w / 2, d2[0] / l2 * sg * w / 2)
        a0, a1 = (p0[0] + n1[0], p0[1] + n1[1]), (kn[0] + n1[0], kn[1] + n1[1])
        c0, c1 = (kn[0] + n2[0], kn[1] + n2[1]), (hf[0] + n2[0], hf[1] + n2[1])
        corner = xline(a0, a1, c0, c1)
        up = lambda f: (p0[0] + d1[0] * f + n1[0], p0[1] + d1[1] * f + n1[1])
        dn = lambda f: (kn[0] + d2[0] * f + n2[0], kn[1] + d2[1] * f + n2[1])
        top = hit(body, T(*corner), T(*a0), T(*up(.3)))
        tp = body[top[0]].at(top[1]); seg1 = (T(*a0), T(*a1))
        f_top = ((tp[0] - seg1[0][0]) * (seg1[1][0] - seg1[0][0]) + (tp[1] - seg1[0][1]) * (seg1[1][1] - seg1[0][1])) / math.dist(*seg1) ** 2
        print(f'  {nm} side {sg}: leaves the body {f_top:.2f} of the way to the knee; first stripe starts at {b1[0]}')
        assert f_top < b1[0] - .05, (nm, sg, f_top)
        sides[sg] = dict(top=top, pts=[up(b1[0]), up(b1[1]), corner, dn(b2[0]), dn(b2[1]), dn(HOOF), c1])
        legcuts[(nm, sg)] = top
    legplan[nm] = sides

# ---- where things meet the body outline ----
NECK = [(90, 97), (102, 109), (113, 119)]
cuts = {}
for k, (y0, y1) in enumerate(NECK):
    cuts[('neck', k, 0)] = at_y(body, T(0, y0)[1])
    cuts[('neck', k, 1)] = at_y(body, T(0, y1)[1])
BODYSTRIPES = [(70, 103.8), (84, 103.8), (98, 103.8)]   # top-left corner of each band, just under the back
belly_i = 2                                              # the tummy piece of the body outline
for k, (x, y) in enumerate(BODYSTRIPES):
    cuts[('band', k, 0)] = at_x(body, T(x - 1.5, 0)[0], belly_i)
    cuts[('band', k, 1)] = at_x(body, T(x + 3, 0)[0], belly_i)
tail_at = at_y(body, T(0, 108)[1], 4)
cuts['tail'] = tail_at
for key, v in legcuts.items():
    cuts[('leg',) + key] = v
body, node = refine(body, cuts)
ON = lambda name: body[node[name]].a
def between(a, b):
    i, j = node[a], node[b]
    assert i < j, (a, b)
    return body[i:j]

# ---- neck stripes: from the front of its neck to just short of the slanting line ----
neck_lines, neck_fills = [], []
for k, (y0, y1) in enumerate(NECK):
    A, B = ON(('neck', k, 0)), ON(('neck', k, 1))
    if k < 2:
        e0, e1 = T(zx(y0), y0), T(zx(y1), y1)
    else:
        e0, e1 = T(46, y0), T(46, y1)
    ln = [Seg(A, P(e0[0], A[1])), Seg(P(e0[0], A[1]), P(e1[0], B[1])), Seg(P(e1[0], B[1]), B)]
    neck_lines.append(line(*ln))
    neck_fills.append(fill(BLACK, *(ln + rev(between(('neck', k, 0), ('neck', k, 1))))))

# ---- body stripes: from just under its back down to its tummy ----
band_lines, band_fills = [], []
for k, (x, y) in enumerate(BODYSTRIPES):
    L0, R0 = ON(('band', k, 0)), ON(('band', k, 1))
    tl, tr = T(x, y), T(x + 7, y)
    left = Seg(L0, P(L0[0] + .6, L0[1] - 10), P(tl[0] - .2, tl[1] + 8), tl)
    right = Seg(tr, P(tr[0] + .4, tr[1] + 8), P(R0[0] + .6, R0[1] - 10), R0)
    ln = [left, Seg(tl, tr), right]
    band_lines.append(line(*ln))
    band_fills.append(fill(BLACK, *(ln + rev(between(('band', k, 0), ('band', k, 1))))))
rump = curve(T(122, 106), T(126, 104), T(130, 104), T(134, 106), T(134, 112), T(133, 120), T(131, 126),
             T(128, 127.5), T(125, 127.5), T(123, 126), T(124, 120), T(123, 112), T(122, 106))
band_lines.append(ring(*rump)); band_fills.append(fill(BLACK, *rump))

# ---- head stripes: two on its forehead and one on its cheek, all closed shapes ----
fore1 = curve(T(70, 48), T(69, 51), T(70, 54), T(72, 56)) + [Seg(T(72, 56), T(76, 55))] + curve(T(76, 55), T(74, 53), T(74, 51), T(75, 48)) + [Seg(T(75, 48), T(70, 48))]
fore2 = curve(T(80, 48), T(80, 51), T(81, 54), T(83, 56)) + [Seg(T(83, 56), T(87, 54))] + curve(T(87, 54), T(85, 52), T(85, 50), T(85.5, 48)) + [Seg(T(85.5, 48), T(80, 48))]
cheek = curve(T(62, 76), T(65, 73), T(69, 72), T(72, 73)) + [Seg(T(72, 73), T(71, 79))] + curve(T(71, 79), T(68, 78), T(65, 79), T(63, 81)) + [Seg(T(63, 81), T(62, 76))]
head_rings = [fore1, fore2, cheek]

# ---- legs: outline, two stripes and a hoof each ----
leg_lines, leg_marks, leg_fills = [], [], []
for nm, sides in legplan.items():
    A = [ON(('leg', nm, 1))] + [T(*q) for q in sides[1]['pts']]
    B = [ON(('leg', nm, -1))] + [T(*q) for q in sides[-1]['pts']]
    sa = [Seg(a, b) for a, b in zip(A, A[1:])]; sb = [Seg(a, b) for a, b in zip(B, B[1:])]
    leg_lines.append(line(*(sa + [Seg(A[-1], B[-1])] + rev(sb))))
    for i0, i1 in ((1, 2), (4, 5)):          # the two stripes: between points 1-2 (upper) and 4-5 (lower)
        leg_marks += [line(Seg(A[i0], B[i0])), line(Seg(A[i1], B[i1]))]
        leg_fills.append(fill(BLACK, *(sa[i0:i1] + [Seg(A[i1], B[i1])] + rev(sb[i0:i1]) + [Seg(B[i0], A[i0])])))
    leg_marks.append(line(Seg(A[6], B[6])))  # top of the hoof
    leg_fills.append(fill(BLACK, *(sa[6:] + [Seg(A[-1], B[-1])] + rev(sb[6:]) + [Seg(B[6], A[6])])))
front_legs = [leg_lines[0], leg_lines[1]]
back_legs = [leg_lines[2], leg_lines[3]]

# ---- ear, mane, tail ----
ear = chain('M91.5,42 C89.5,32 91.5,24 96,18 C100,25 100,35 97,42')
mp = [zpt(.06, 0)] + [zpt(t, 11 if i % 2 == 0 else 6.5) for i, t in enumerate([.12, .2, .28, .36, .44, .52, .6, .68, .76])] + [zpt(.84, 0)]
mane = [Seg(T(*a), T(*b)) for a, b in zip(mp, mp[1:])]
mane_fill = fill(BLACK, *(mane + [Seg(T(*mp[-1]), T(*mp[0]))]))
TS = ON('tail'); TT = T(178, 88)
tail = Seg(TS, T(160, 104), T(170, 98), TT)
tuft = curve(TT, T(182, 80), T(188, 76), T(192, 76), T(192, 84), T(186, 90), TT)

# ---- face ----
smile = Seg(T(27, 78), T(29.5, 81), T(32.5, 81.5), T(35, 79))
lashes = [Seg(T(50.5, 52.5), T(48, 50)), Seg(T(54, 51), T(53, 48.2)), Seg(T(58.5, 51), T(59.3, 48.2))]

steps = [
    step('Start with a Z', 'Draw a capital Z: a line across the top, a long slanting line down to the left, and a line across the bottom.', [line(*z_letter)]),
    step('The face', 'From the top left corner of the Z, draw the front of its face, round its nose and back to its chin.', [line(*face)]),
    step('Neck and tummy', 'From its chin, draw the front of its neck, under its tummy and round its bottom, up to the end of the Z.', [line(*body)]),
    step('The ear', 'Draw a pointy ear on top of its head, by the corner of the Z.', [line(*ear)]),
    step('The mane', 'Draw a spiky mane along the back of its neck, just behind the slanting line.', [line(*mane)]),
    step('Front legs', 'Draw two bent front legs, one stretched out in front, as if it is galloping.', front_legs),
    step('Back legs', 'Draw two bent back legs, one kicking out behind.', back_legs),
    step('The tail', 'Draw a tail flying out behind, with a pointy tuft at the end.', [line(tail), ring(*tuft)]),
    step('Nose and eye', 'Draw a line round its nose, a dot for its nostril, a little smile, and a big eye with three eyelashes.',
         [line(*muzzle), dot(*T(26, 68), w=2.4), line(smile), dot(*T(56, 58), w=5.6)] + [line(l) for l in lashes]),
    step('Head and neck stripes', 'Draw two stripes on its forehead, one on its cheek, and three across its neck.', [ring(*r) for r in head_rings] + neck_lines),
    step('Body stripes', 'Draw stripes hanging down from its back, and one on its bottom.', band_lines),
    step('Leg stripes', 'Draw two stripes on each leg, and a line across the bottom of each leg for its hoof.', leg_marks),
]
steps += [step('Colour black', 'Colour the mane, all the stripes, the hooves and the tuft on its tail black.',
               [mane_fill] + neck_fills + [fill(BLACK, *r) for r in head_rings] + band_fills + leg_fills + [fill(BLACK, *tuft)], use='black'),
          step('Colour grey', 'Colour its nose grey.', [fill(GREY, *(face[1:] + muzzle))], use='grey')]

Pd = drawing('dx_zebra_z', 'Z is for zebra', 3, 15, 'animals', ['Letters', 'Animals'],
             'A happy zebra galloping along. The capital Z is hiding in it: the top of its head, the back of its neck and its back.',
             steps, ['black', 'grey'])
save('zebra', Pd, {'set': 'animals-AZ', 'slot': 'Z', 'kind': 'hop', 'age_from': 5})
