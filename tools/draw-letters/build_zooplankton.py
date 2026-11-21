"""z is for zooplankton (dx_zooplankton_z), Animals a to z, slot z (21 Nov 2026).
From Claude's sketch 'zooplankton (leading its babies)' (design 4 of the second round, from his "Krill (Zooplankton)"
picture), with the tail fan redrawn as two long paddles (he said the first fan did not look natural). A krill curled
up, facing left, with three babies above. The small z: its top line is the underside of its body, its slant is the
inside edge of its tail (facing the gap in the curl), and its bottom line is the underside of its tail. The tail narrows
to the z's bottom-left corner, where the fan is. Body and babies orange, fan yellow.
Sketch coordinates (200 x 200) go onto the paper by T().
"""
import math, re
from r5kit import *

PA = Paper(0.5, 0.75, 3.25)
T = PA.T
ORA, YEL = FILL['orange'], FILL['yellow']


def chain(d):
    toks = re.findall(r'[MCLQ]|-?\d+\.?\d*', d)
    out = []; cur = None; i = 0; cmd = None
    while i < len(toks):
        t = toks[i]
        if t in 'MCLQ':
            cmd = t; i += 1; continue
        if cmd == 'M':
            cur = T(float(toks[i]), float(toks[i + 1])); i += 2
        elif cmd == 'C':
            c1 = T(float(toks[i]), float(toks[i + 1])); c2 = T(float(toks[i + 2]), float(toks[i + 3])); p = T(float(toks[i + 4]), float(toks[i + 5]))
            out.append(Seg(cur, c1, c2, p)); cur = p; i += 6
        elif cmd == 'Q':
            q = T(float(toks[i]), float(toks[i + 1])); p = T(float(toks[i + 2]), float(toks[i + 3]))
            out.append(q2c(cur, q, p)); cur = p; i += 4
        elif cmd == 'L':
            p = T(float(toks[i]), float(toks[i + 1])); out.append(Seg(cur, p)); cur = p; i += 2
    return out


def at_x(ch, k, x, lo=0.0, hi=1.0):
    """a point on piece k of a chain at paper x (bisection)"""
    s = ch[k]; a, b = lo, hi
    fa = s.at(a)[0] - x
    for _ in range(60):
        m = (a + b) / 2; fm = s.at(m)[0] - x
        if (fa < 0) == (fm < 0): a, fa = m, fm
        else: b = m
    return P(*s.at((a + b) / 2))


# ---- 1: the z ----
TL, TR, BL, BR = T(90, 90), T(152, 90), T(90, 136), T(152, 136)
u = ((TR[0] - BL[0]), (TR[1] - BL[1])); L = math.hypot(*u); u = (u[0] / L, u[1] / L)
FA = P(BL[0] + u[0] * 3.5, BL[1] + u[1] * 3.5)          # the fan meets the slant here (7 sketch units from the corner)
FB = P(BL[0] + 3.5, BL[1])                               # and the bottom line here
z_top = Seg(TL, TR)
slant = [Seg(TR, FA), Seg(FA, BL)]
bottom = [Seg(BL, FB), Seg(FB, BR)]

# ---- the body: from the end of the bottom line, up round its back to its head, under its head and up to the z ----
OUT = chain('M30,98 C20,96 14,86 18,78 C22,70 28,68 36,68 C56,60 96,52 130,52 C162,52 186,70 190,96 '
            'C194,120 184,140 170,146 C160,150 154,146 152,136')
assert OUT[-1].b == BR
H1, S1 = OUT[0].a, T(84, 98)
# stripes start on its back, feelers start on its face: cut the outline there
st_pts = [at_x(OUT, 2, T(x, 0)[0]) for x in (104, 124)] + [at_x(OUT, 3, T(144, 0)[0])]
st_pts += [P(*OUT[3].at(0.62)), P(*OUT[4].at(0.1)), P(*OUT[4].at(0.45))]
an_pts = [P(*OUT[0].at(t)) for t in (0.62, 0.82)] + [P(*OUT[1].at(0.05))]
OUT, ex = cut_at_points(OUT, st_pts + an_pts)
ST = ex[:6]; AN = ex[6:]
BELLY = [Seg(H1, S1)]
leg_x = (36, 44, 52, 60, 70)
BELLY, LEGS = cut_at_points(BELLY, [T(x, 98) for x in leg_x])
step_up = Seg(S1, TL)
BODY_LINE = rev(OUT) + BELLY + [step_up]                 # drawn from the end of the bottom line round to the z's top
assert BODY_LINE[0].a == BR and BODY_LINE[-1].b == TL

# ---- the tail fan: two long paddles round the z's bottom corner ----
FAN = snap(chain('M95.6,131.8 C84,130 64,134 54,142 C48,147 52,153 60,152 C70,151 78,149 84,148 '
                 'C78,154 70,162 66,168 C63,173 68,177 73,174 C84,168 94,152 97,136'), FA, FB)
ribs = [Seg(T(86, 142), T(61, 147)), Seg(T(88, 151), T(71, 169))]

# ---- stripes on its back, legs, face ----
ends = [T(103, 83), T(123, 83), T(141, 83), T(164, 86), T(170, 106), T(166, 122)]
stripes = []
for a, b in zip(ST, ends):
    m = ((a[0] + b[0]) / 2 + 1.25, (a[1] + b[1]) / 2 + 0.5)
    stripes.append(q2c(a, P(*m), b))
legs = []
for p, (ln, dv) in zip(LEGS, [(20, (-0.3, 1)), (20, (-0.3, 1)), (19, (-0.25, 1)), (18, (-0.25, 1)), (16, (-0.2, 1))]):
    k = math.hypot(*dv); dv = (dv[0] / k, dv[1] / k); ln *= 0.5
    q = P(p[0] + dv[0] * ln, p[1] + dv[1] * ln); m = P(p[0] + dv[0] * ln * 0.55, p[1] + dv[1] * ln * 0.55)
    nx, ny = -dv[1], dv[0]
    legs.append(([Seg(p, m), Seg(m, q)], Seg(m, P(m[0] + (nx * 3.5 + dv[0] * 1.5) * 0.5, m[1] + (ny * 3.5 + dv[1] * 1.5) * 0.5))))
eyes = [dot(*T(34, 77), w=5.0), dot(*T(47, 73), w=5.0)]
smile = chain('M22,88 Q28,93 35,90')
f_ends = [('C14,96 14,110 18,124'), ('C10,82 6,92 6,106'), ('C10,70 6,62 8,52')]   # lowest feeler start goes furthest down
feelers = []
for p, tail in zip(AN, f_ends):
    nums = [float(v) for v in re.findall(r'-?\d+\.?\d*', tail)]
    feelers.append(Seg(p, T(nums[0], nums[1]), T(nums[2], nums[3]), T(nums[4], nums[5])))

# ---- three babies above it ----
def baby(x, y, k):
    pts = [(x - 7 * k, y - 2 * k), (x - 4 * k, y - 8 * k), (x + 6 * k, y - 8 * k), (x + 8 * k, y - 1 * k), (x + 9 * k, y + 4 * k), (x + 6 * k, y + 8 * k),
           (x + 2 * k, y + 8 * k), (x + 4 * k, y + 4 * k), (x + 2 * k, y + 1 * k), (x - 2 * k, y + 1 * k), (x - 5 * k, y + 1 * k), (x - 8 * k, y + 1 * k), (x - 7 * k, y - 2 * k)]
    q = [T(*p) for p in pts]
    ring_ = [Seg(q[0], q[1], q[2], q[3]), Seg(q[3], q[4], q[5], q[6]), Seg(q[6], q[7], q[8], q[9]), Seg(q[9], q[10], q[11], q[0])]
    tip = q[0]
    fl = [Seg(tip, T(x - 12 * k, y - 5 * k)), Seg(tip, T(x - 12.5 * k, y + 0.5 * k))]
    return ring_, fl, dot(*T(x - 3.5 * k, y - 3.5 * k), w=1.9)
babies = [baby(48, 36, 1.1), baby(74, 26, 1.0), baby(104, 34, 0.95)]
bubbles = [circle(*T(186, 26), 2.2), circle(*T(172, 16), 1.5), circle(*T(122, 182), 1.8)]

steps = [
    step('Start with a z', 'Draw a small letter z: a line across, a slanting line down to the left, and a line across the bottom. This z is hiding in the zooplankton.',
         [line(z_top, *slant, *bottom)]),
    step('Its body', 'From the end of the bottom line, draw a big curve up round its back to its head, then under its head and up to the start of the z.',
         [line(*BODY_LINE)]),
    step('The tail fan', 'At the bottom corner of the z, draw two long paddles for its tail fan, with a line down each one.',
         [line(*FAN)] + [line(r) for r in ribs]),
    step('Stripes', 'Draw six curved stripes on its back.', [line(s) for s in stripes]),
    step('Legs', 'Draw five little legs under its head, each with a tiny tick.', [line(*lg[0]) for lg in legs] + [line(lg[1]) for lg in legs]),
    step('Face and feelers', 'Draw two eyes, a smile and three long feelers.', eyes + [line(*smile)] + [line(f) for f in feelers]),
    step('The babies', 'Draw three little babies swimming above it, each with an eye.',
         [ring(*b[0]) for b in babies] + [b[2] for b in babies]),
    step('Feelers and bubbles', 'Give each baby two little feelers, and draw some bubbles.',
         [line(f) for b in babies for f in b[1]] + [ring(*c) for c in bubbles]),
]

# ---- colours ----
body = fill(ORA, *(OUT + [bottom[1].rev(), bottom[0].rev(), slant[1].rev(), slant[0].rev(), z_top.rev(), step_up.rev()] + rev(BELLY)))
fan = fill(YEL, *(FAN + [bottom[0].rev(), slant[1].rev()]))
steps += [
    step('Colour orange', 'Colour the zooplankton and its babies orange.', [body] + [fill(ORA, *b[0]) for b in babies], use='orange'),
    step('Colour yellow', 'Colour its tail fan yellow.', [fan], use='yellow'),
]

D = drawing('dx_zooplankton_z', 'z is for zooplankton', 2, 12, 'animals', ['Letters', 'Animals'],
            'A zooplankton (a krill) leading its babies. The small z is hiding in it: under its body, the inside of its tail and the underside of its tail.',
            steps, ['orange', 'yellow'])
save('zooplankton', D, {'set': 'animals-az', 'slot': 'z', 'kind': 'swim', 'age_from': 4})
