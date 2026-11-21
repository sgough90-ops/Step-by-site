"""m is for mouse (dx_mouse_m), Animals a to z, slot m. From Claude's round-4 sketch 'Mouse (standing tall)' (21 Nov 2026),
drawn from the mouse picture he sent (Art Carnival With Subrata's mouse from a capital M, 8sNNrMQRi1s), with a small m where the M was.

The small m is its face: the outside lines are the sides of its face, the two humps are the top of its head (an eye under each),
and the middle line runs down to its nose. Its big round ears are tucked behind the humps.
Sketch coordinates (200 x 200) are turned into the app's 100 x 100 paper by T().
"""
import re, json, os
from kit15 import *

S, OX, OY = 0.48, 1.0, 1.0
def T(x, y):
    return P(x * S + OX, y * S + OY)

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

def nearest_t(seg, pt, n=2000):
    best = min(range(n + 1), key=lambda k: math.dist(seg.at(k / n), pt))
    lo, hi = max(0, best - 1) / n, min(n, best + 1) / n
    for _ in range(60):
        a, b = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if math.dist(seg.at(a), pt) < math.dist(seg.at(b), pt): hi = b
        else: lo = a
    return (lo + hi) / 2

def cut_chain_at(ch, pts):
    """Cut a chain at the points nearest to pts (in order along the chain). Returns the new chain and the exact cut points."""
    places = []
    for p in pts:
        i = min(range(len(ch)), key=lambda k: min(math.dist(ch[k].at(j / 400), p) for j in range(401)))
        places.append((i, nearest_t(ch[i], p)))
    by = {}
    for i, t in places:
        by.setdefault(i, []).append(t)
    new = []
    for i, s in enumerate(ch):
        new += split_many(s, sorted(by[i])) if i in by else [s]
    chain_ok(new)
    exact = [P(*ch[i].at(t)) for i, t in places]
    exact = [min((q.a for q in new[1:]), key=lambda q: math.dist(q, e)) for e in exact]
    return new, exact

GREY, PINK = FILL['grey'], FILL['pink']
SC = S                                       # radii scale

# ---- the m: lines at x 62, 100, 138; humps spring at y 70 (16 high); bottoms at y 106 ----
A0, A1, A2 = T(62, 106), T(62, 70), T(100, 70)
B1, B2 = T(100, 106), T(138, 70)
C1 = T(138, 106)
hump1 = arc(81 * S + OX, 70 * S + OY, 19 * S, 16 * S, 180, 360, start=A1, end=A2)
hump2 = arc(119 * S + OX, 70 * S + OY, 19 * S, 16 * S, 180, 360, start=A2, end=B2)
m_first = [Seg(A0, A1)] + hump1 + [Seg(A2, B1)]
m_second = hump2 + [Seg(B2, C1)]

# ---- ears: the part of a big circle outside the head, ending on a hump ----
EL1, EL2 = T(62.83, 65.31), T(72.34, 55.76)          # where the left ear meets the first hump (lower end, upper end)
ER1, ER2 = T(137.17, 65.31), T(127.66, 55.76)
hump1c, (EL1, EL2) = cut_chain_at(hump1, [EL1, EL2])
hump2c, (ER2, ER1) = cut_chain_at(hump2, [ER2, ER1])
def piece_between(ch, p, q):
    i = next(k for k, s in enumerate(ch) if s.a == p); j = next(k for k, s in enumerate(ch) if s.b == q)
    return ch[i:j + 1]
left_hump_bit = piece_between(hump1c, EL1, EL2)        # from the lower end up to the upper end, along the hump
right_hump_bit = piece_between(hump2c, ER2, ER1)
ELC, ERC, ER = T(55, 48), T(145, 48), 19 * S
a_l1 = math.degrees(math.atan2(EL1[1] - ELC[1], EL1[0] - ELC[0])); a_l2 = math.degrees(math.atan2(EL2[1] - ELC[1], EL2[0] - ELC[0]))
ear_l = arc(ELC[0], ELC[1], ER, ER, a_l1, a_l2 + 360, start=EL1, end=EL2)          # round the outside, clockwise
a_r1 = math.degrees(math.atan2(ER1[1] - ERC[1], ER1[0] - ERC[0])); a_r2 = math.degrees(math.atan2(ER2[1] - ERC[1], ER2[0] - ERC[0]))
ear_r = arc(ERC[0], ERC[1], ER, ER, a_r1, a_r2 - 360, start=ER1, end=ER2)          # anticlockwise
inner_l = circle(*T(53, 46), 11 * S); inner_r = circle(*T(147, 46), 11 * S)

# ---- body: from the bottom of the first line round to the bottom of the last line ----
body = chain('M62,106 C60,114 58,120 55,126 C44,142 40,160 46,174 C49,181 53,186 55,191 C57,197 69,197 71,191 C73,185 77,181 84,181 '
             'C91,181 95,185 97,191 C99,197 111,197 113,191 C115,185 121,180 128,176 C140,168 156,152 148,126 C145,120 141,114 138,106')
assert body[0].a == A0 and body[-1].b == C1
TAIL_LO_T, TAIL_HI_T = .2, .34                        # where the tail leaves the body, on the piece (128,176) -> (148,126)
tp = body[8]
TA, TB = P(*tp.at(TAIL_LO_T)), P(*tp.at(TAIL_HI_T))
ARM = {}
for side, (pi_top, pi_bot) in (('l', (0, 1)), ('r', (9, 8))):
    top_t = seg_y(body[pi_top], T(0, 123)[1]); bot_t = seg_y(body[pi_bot], T(0, 135.5)[1])
    ARM[side] = (P(*body[pi_top].at(top_t)), P(*body[pi_bot].at(bot_t)))
body, (TA, TB, ALT, ALB, ART, ARB) = cut_chain_at(body, [TA, TB, ARM['l'][0], ARM['l'][1], ARM['r'][0], ARM['r'][1]])
tail_base = piece_between(body, TA, TB)
tail = [Seg(TA, T(158, 176), T(172, 164), T(178, 148)), Seg(T(178, 148), T(182, 138), T(186, 130), T(194, 126)),
        Seg(T(194, 126), T(186, 128), T(181, 134), T(177, 144)), Seg(T(177, 144), T(171, 158), T(160, 166), TB)]

# ---- arms: little loops in front, both ends on the body's side ----
arm_l = [Seg(ALT, T(62, 129), T(72, 134), T(80, 134)), Seg(T(80, 134), T(88, 134), T(90, 142), T(82, 144)),
         Seg(T(82, 144), T(70, 146), T(58, 141), ALB)]
arm_r = [Seg(ART, T(138, 129), T(128, 134), T(120, 134)), Seg(T(120, 134), T(112, 134), T(110, 142), T(118, 144)),
         Seg(T(118, 144), T(130, 146), T(142, 141), ARB)]

# ---- face ----
eye_l = circle(*T(81, 77), 7.4 * S); eye_r = circle(*T(119, 77), 7.4 * S)
PUP_L, PUP_R = T(84, 76), T(122, 76)
NR = 4.6 * S
nose = circle(B1[0], B1[1] + NR, NR, start_deg=-90)                    # hangs from the bottom of the middle line
assert nose[0].a == B1
whiskers = []
for sgn in (-1, 1):
    for (x0, y0), (cx1, cy1), (cx2, cy2), (x1, y1) in [((8, -5), (14, -8), (20, -10), (28, -10)), ((8, 0), (14, -1), (21, -1), (30, 0)),
                                                         ((8, 5), (14, 7), (20, 10), (27, 13))]:
        whiskers.append(Seg(T(100 + sgn * x0, 106 + y0), T(100 + sgn * cx1, 106 + cy1), T(100 + sgn * cx2, 106 + cy2), T(100 + sgn * x1, 106 + y1)))
tummy = circle(*T(96, 160), 19 * S)

steps = [
    step('Start with an m', 'Draw a small letter m: a short straight line, then two humps side by side, each coming straight down.',
         [line(*m_first), line(*m_second)]),
    step('The ears', 'Draw a big round ear on each side, tucked behind the humps.', [line(*ear_l), line(*ear_r)]),
    step('Inside the ears', 'Draw a circle inside each ear.', [ring(*inner_l), ring(*inner_r)]),
    step('The body', 'From the bottom of the first line, draw its body round its tummy, with two little feet, up to the bottom of the last line.', [line(*body)]),
    step('Arms', 'Draw two little arms bent in front of it.', [line(*arm_l), line(*arm_r)]),
    step('The tail', 'Draw a long thin tail curling out from its side.', [line(*tail)]),
    step('The tummy', 'Draw a big circle for its tummy.', [ring(*tummy)]),
    step('The eyes', 'Draw two circles with a dot in each for its eyes.', [ring(*eye_l), ring(*eye_r), dot(*PUP_L, w=2.6), dot(*PUP_R, w=2.6)]),
    step('Nose and whiskers', 'Draw a little round nose at the bottom of the middle line, and three whiskers on each side.',
         [ring(*nose)] + [line(w) for w in whiskers]),
]
hole = lambda segs: d_fill(*segs)
grey_head = fill(GREY, *([Seg(A0, A1)] + hump1c + hump2c + [Seg(B2, C1)] + rev(body)),
                 cut=[hole(eye_l), hole(eye_r), hole(tummy), hole(nose)])
grey_ear_l = fill(GREY, *(ear_l + rev(left_hump_bit)), cut=[hole(inner_l)])
grey_ear_r = fill(GREY, *(ear_r + right_hump_bit), cut=[hole(inner_r)])
steps += [step('Colour grey', 'Colour the mouse grey, but leave its eyes and its tummy white.', [grey_head, grey_ear_l, grey_ear_r], use='grey'),
          step('Colour pink', 'Colour the insides of its ears, its nose and its tail pink.',
               [fill(PINK, *inner_l), fill(PINK, *inner_r), fill(PINK, *nose), fill(PINK, *(tail + rev(tail_base)))], use='pink')]

Pd = drawing('dx_mouse_m', 'm is for mouse', 2, 12, 'animals', ['Letters', 'Animals'],
             'A little mouse standing up. The small m is its face: the sides of its face, the top of its head and a line down to its nose.',
             steps, ['grey', 'pink'])
save('mouse', Pd, {'set': 'animals-az', 'slot': 'm', 'kind': 'hop', 'age_from': 4})
here = os.path.dirname(os.path.abspath(__file__))
json.dump([hole(eye_l), hole(eye_r), hole(tummy)], open(os.path.join(here, 'out', 'mouse.white.json'), 'w'))
