"""Y is for yak (dx_yak_y), Animals A to Z, slot Y. From Claude's sketch 'Yak (standing in the grass)' (21 Nov 2026), which
he picked, with a smaller hump at his word ("no need for such a big hump").
Idea from Art for Kids Hub's yak from a capital Y (EFp7yy1zBNE): the yak's head is seen from the front and the Y is in its face.

The Y's two short lines are the bottom edges of the dark shaggy fringe on its forehead, and its line down is the line of its nose,
down to the top of its pale muzzle. The body is seen from the side behind the head: a small hump, long hair hanging nearly to
the ground, four short legs and a bushy tail.
Sketch coordinates (200 x 200) are turned into the app's 100 x 100 paper by T().
"""
import re, math
from kit15 import *

OX, OY = 0.0, -1.0
def T(x, y):
    return P(x * 0.5 + OX, y * 0.5 + OY)

def chain(d):
    """pieces from sketch path text (absolute M, C, L only)"""
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

def at_y(ch, y, lo=0, hi=None):
    """(piece, t) where a chain first crosses height y (sketch units), looking from piece lo."""
    y = T(0, y)[1]
    for i in range(lo, len(ch) if hi is None else hi):
        ys = [ch[i].at(k / 200)[1] for k in range(201)]
        for k in range(200):
            if (ys[k] - y) * (ys[k + 1] - y) <= 0 and ys[k] != ys[k + 1]:
                return i, seg_y(ch[i], y, k / 200, (k + 1) / 200)
    raise ValueError(y)

def at_x(ch, x, lo=0):
    x = T(x, 0)[0]
    for i in range(lo, len(ch)):
        xs = [ch[i].at(k / 200)[0] for k in range(201)]
        for k in range(200):
            if (xs[k] - x) * (xs[k + 1] - x) <= 0 and xs[k] != xs[k + 1]:
                return i, seg_x(ch[i], x, k / 200, (k + 1) / 200)
    raise ValueError(x)

BROWN, LBROWN, PINK, BLACK = FILL['brown'], FILL['lbrown'], FILL['pink'], FILL['black']

# ---- the Y ----
TL, TR, FK, BT = T(34, 74), T(90, 74), T(62, 106), T(62, 134)
armL, armR, stem = Seg(TL, FK), Seg(TR, FK), Seg(FK, BT)

# ---- the face: a U from the top of the left arm, round the chin, up to the top of the right arm ----
head = chain('M34,74 C30,92 27,110 30,126 C33,142 42,158 62,158 C82,158 91,142 94,126 C97,110 94,92 90,74')
assert head[0].a == TL and head[-1].b == TR
cuts = {'earL0': (0, .16), 'earL1': (0, .42), 'earR0': (3, .58), 'earR1': (3, .84),
        'ML': at_y(head, 141, 1, 2), 'MR': at_y(head, 141, 2, 3), 'HQ': at_y(head, 150, 1, 2)}
head, hn = refine(head, cuts)
ON = lambda n: head[hn[n]].a
def hb(a, b):
    i, j = hn[a] if a else 0, hn[b] if b else len(head)
    assert i < j, (a, b)
    return head[i:j]
ML, MR, HQ = ON('ML'), ON('MR'), ON('HQ')

# ---- the shaggy fringe on top, from one arm of the Y to the other ----
tufts = chain('M34,74 C33,67 37,61 44,62 C45,55 52,52 57,56 C59,51 65,51 67,56 C72,52 79,55 80,62 C87,61 91,67 90,74')
assert tufts[0].a == TL and tufts[-1].b == TR

# ---- horns: a short line out from each top corner, and a horn curving up on it ----
extL = [Seg(TL, T(28, 74)), Seg(T(28, 74), T(16, 74))]          # from the corner out to the left
hornL = chain('M16,74 C5,70 4,52 15,38') + chain('M15,38 C13,52 18,66 28,74')
extR = [Seg(TR, T(96, 74)), Seg(T(96, 74), T(108, 74))]
hornR_out = chain('M108,74 C119,70 120,52 109,38')
HPT = .36                                                         # the back starts here, on the right horn's outer edge
hr_a, hr_b = hornR_out[0].split(HPT)
HP = hr_a.b
hornR = [hr_a, hr_b] + chain('M109,38 C111,52 106,66 96,74')

# ---- ears ----
def ear_l():
    a, b = ON('earL0'), ON('earL1')
    return [Seg(a, T(22, 80), T(12, 82), T(7, 90)), Seg(T(7, 90), T(13, 97), T(22, 100), b)]
def ear_r():
    a, b = ON('earR1'), ON('earR0')                              # from the upper point out to the tip and back to the lower point
    return [Seg(a, T(102, 80), T(112, 82), T(117, 90)), Seg(T(117, 90), T(111, 97), T(102, 100), b)]
earL, earR = ear_l(), ear_r()

# ---- muzzle: a curve across the bottom of the face that touches the bottom of the Y ----
mx, my = ML[0] * 2, (ML[1] - OY) * 2                              # back to sketch units for the control points
nx, ny = MR[0] * 2, (MR[1] - OY) * 2
muzzle = [Seg(ML, T(mx + 9, my - 6), T(51, 134), BT), Seg(BT, T(73, 134), T(nx - 9, ny - 6), MR)]

# ---- body: from the right horn, a small hump, the back, round its bottom and down; then its long hair ----
back = [Seg(HP, T(121, 54), T(128, 46), T(140, 45)), Seg(T(140, 45), T(153, 44), T(163, 48), T(169, 55)),
        Seg(T(169, 55), T(174, 61), T(176, 70), T(175, 80))]
tail_cuts = {'t0': at_y(back, 64, 2), 't1': at_y(back, 74, 2)}
back, bn = refine(back, tail_cuts)
U0, L0 = back[bn['t0']].a, back[bn['t1']].a
rear = Seg(T(175, 80), T(174, 166))

def locks(x0, x1, y, depth=10, w=10):
    """long hanging hair from x0 to x1 (x0 > x1), sketch units: a row of pointed locks"""
    out, x, k = [], x0, 0
    while x - w >= x1 - .1:
        dd = depth * (1 if k % 3 else .7)
        tip = x - w * .5
        out.append(Seg(T(x, y), T(x - w * .2, y + dd * .6), T(tip + w * .1, y + dd * .9), T(tip, y + dd)))
        out.append(Seg(T(tip, y + dd), T(tip - w * .1, y + dd * .8), T(x - w * .8, y + dd * .5), T(x - w, y)))
        x -= w; k += 1
    return out, x
hair, xe = locks(174, 54, 166)
chest = Seg(T(xe, 166), T(xe - 4, 163), T(44, 158), HQ)          # the front of its chest, up to the face

# ---- legs: four short legs under the hair, each with a hoof ----
LEGS = [(84, 97), (100, 115), (140, 153), (156, 171)]
leg_cuts = {}
for k, (x0, x1) in enumerate(LEGS):
    leg_cuts[('leg', k, 1)] = at_x(hair, x1)
    leg_cuts[('leg', k, 0)] = at_x(hair, x0)
hair, ln = refine(hair, leg_cuts)
HOOF_Y, FOOT_Y = 180, 188
legs, hooves, leg_fills, hoof_fills = [], [], [], []
for k, (x0, x1) in enumerate(LEGS):
    A, B = hair[ln[('leg', k, 0)]].a, hair[ln[('leg', k, 1)]].a     # tops of the left and right sides, on the hair
    a1, a2 = T(x0, HOOF_Y), T(x0, FOOT_Y)
    b1, b2 = T(x1, HOOF_Y), T(x1, FOOT_Y)
    sideL = [Seg(A, a1), Seg(a1, a2)]
    sideR = [Seg(b2, b1), Seg(b1, B)]
    legs.append(line(*(sideL + [Seg(a2, b2)] + sideR)))
    hooves.append(line(Seg(a1, b1)))
    i, j = ln[('leg', k, 1)], ln[('leg', k, 0)]                       # along the hair (going left) the right side comes first
    leg_fills.append(fill(BROWN, Seg(A, a1), Seg(a1, b1), Seg(b1, B), *hair[i:j]))
    hoof_fills.append(fill(BLACK, Seg(a1, a2), Seg(a2, b2), Seg(b2, b1), Seg(b1, a1)))

# ---- tail: hanging from its bottom, with a bushy end ----
tail = [Seg(U0, T(182, 64), T(187, 70), T(188, 80)), Seg(T(188, 80), T(189, 88), T(189, 96), T(189, 102)),
        Seg(T(189, 102), T(194, 110), T(195, 122), T(191, 132)), Seg(T(191, 132), T(188, 126)), Seg(T(188, 126), T(185, 134)),
        Seg(T(185, 134), T(182, 126)), Seg(T(182, 126), T(181, 116), T(182, 108), T(184, 102)),
        Seg(T(184, 102), T(184, 92), T(183, 84), L0)]

# ---- face details ----
smile = Seg(T(56, 150.5), T(60, 153.5), T(64, 153.5), T(68, 150.5))
strands = [chain('M156,128 C158,138 158,148 157,156'), chain('M140,132 C141,140 141,150 139,157'), chain('M124,134 C125,142 124,150 122,157')]
def grass(x, y=194):
    return [line(Seg(T(x, y), T(x - 3, y - 8))), line(Seg(T(x + 5, y), T(x + 5, y - 10))), line(Seg(T(x + 10, y), T(x + 13, y - 8)))]

steps = [
    step('Start with a Y', 'Draw a capital Y: two short lines that slant in and meet in the middle, then a line straight down.',
         [line(armL), line(armR), line(stem)]),
    step('The face', 'From the top of one arm of the Y, draw a big U shape for its face, round the bottom and up to the other arm.', [line(*head)]),
    step('Its hair', 'Draw a bumpy line of hair across the top, from one arm of the Y to the other.', [line(*tufts)]),
    step('The horns', 'Draw a short line out from each top corner, then a horn curving up on each one.',
         [line(*extL), line(*hornL), line(*extR), line(*hornR)]),
    step('The ears', 'Draw an ear sticking out under each horn.', [line(*earL), line(*earR)]),
    step('The muzzle', 'Draw a curved line across the bottom of the face, so it touches the bottom of the Y.', [line(*muzzle)]),
    step('Eyes and nose', 'Draw two big dots for its eyes, two dots for its nose and a little smile.',
         [dot(*T(45, 114), w=5.6), dot(*T(79, 114), w=5.6), dot(*T(52, 143), w=3.6), dot(*T(72, 143), w=3.6), line(smile)]),
    step('The back', 'From the back of the right horn, draw a little hump and its back, round its bottom and down.', [line(*(back + [rear]))]),
    step('Long hair', 'Draw its long shaggy hair along the bottom, from the back all the way to under its chin.', [line(*(hair + [chest]))]),
    step('Legs', 'Draw four short legs under its hair, with a line across the bottom of each one for the hoof.', legs + hooves),
    step('The tail', 'Draw a long tail hanging down from its bottom, with a bushy end.', [line(*tail)]),
    step('Hair and grass', 'Draw a few lines of hair on its side, and some grass.', [line(*s) for s in strands] + grass(10) + grass(120) + grass(176)),
]
fringe = fill(BROWN, *tufts, Seg(TR, FK), Seg(FK, TL))
body = fill(BROWN, *back, rear, *hair, chest, *hb('HQ', 'earR0'), *rev(earR), *hb('earR1', None), *extR, hr_a)
tail_fill = fill(BROWN, *tail, *rev(back[bn['t0']:bn['t1']]))
faceL = fill(LBROWN, *hb(None, 'ML'), muzzle[0], stem.rev(), armL.rev())
faceR = fill(LBROWN, armR, stem, muzzle[1], *hb('MR', None))
ear_fills = [fill(LBROWN, *earL, *rev(hb('earL0', 'earL1'))), fill(LBROWN, *earR, *hb('earR0', 'earR1'))]
muzzle_fill = fill(PINK, *muzzle, *rev(hb('ML', 'MR')))
steps += [
    step('Colour brown', 'Colour its hair, body, legs and tail brown. Leave the horns white.', [fringe, body] + leg_fills + [tail_fill], use='brown'),
    step('Colour light brown', 'Colour its face and ears light brown.', [faceL, faceR] + ear_fills, use='lbrown'),
    step('Colour pink', 'Colour its muzzle pink.', [muzzle_fill], use='pink'),
    step('Colour black', 'Colour the four hooves black.', hoof_fills, use='black'),
]
Pd = drawing('dx_yak_y', 'Y is for yak', 3, 15, 'animals', ['Letters', 'Animals'],
             'A shaggy yak standing in the grass, with curved horns and long hair. The capital Y is hiding in its face: '
             'the bottom of its fringe and the line of its nose.',
             steps, ['brown', 'lbrown', 'pink', 'black'])
save('yak', Pd, {'set': 'animals-AZ', 'slot': 'Y', 'kind': 'walk', 'age_from': 5})
