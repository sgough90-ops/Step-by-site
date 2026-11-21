"""E is for elephant (dx_elephant_e), Animals A to Z, slot E. From Claude's round-4 sketch 'Elephant (saying hello)' (21 Nov 2026),
drawn like the elephant picture he sent (Art Carnival With Subrata's elephant from a capital E, gJB1q8g5ENA).

The E is its side: the line down is the back of its head and body, where its big frilly ear joins; the top arm is the top of
its head; the middle arm is its jaw; the bottom arm runs under its back foot.
21 Nov 2026, 15:41: he asked to get rid of the far ear, so the round bump on top of its head is gone.
Sketch coordinates (200 x 200) are turned into the app's 100 x 100 paper by T().
"""
import re, json, os
from kit15 import *

OX, OY = -1.0, 1.5
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

GREY, PINK = FILL['grey'], FILL['pink']

# ---- the E ----
TL, TR, BL, BR, ML, MR = T(62, 54), T(116, 54), T(62, 176), T(124, 176), T(62, 114), T(108, 114)
e_main = [Seg(TR, TL), Seg(TL, BL), Seg(BL, BR)]
e_mid = [Seg(ML, MR)]

# ---- outlines from the sketch ----
dome = chain('M62,54 C56,40 60,24 76,22 C84,21 89,25 91,30 C95,20 110,16 117,28 C121,36 120,47 116,54')
trunk = chain('M116,54 C127,54 133,59 135,69 C137,80 143,85 150,80 C157,74 160,56 162,44 C160,36 166,30 172,34 '
              'C175,28 184,30 183,38 C182,44 176,47 171,47 C168,62 163,80 154,90 C145,99 131,104 118,100 C118,104 112,108 108,114')
ear = chain('M62,58 C50,49 31,50 19,60 C8,70 7,88 13,99 C17,105 24,104 27,99 C29,106 37,108 41,102 '
            'C43,109 52,112 56,106 C57,110 59,112 62,111')
ear_in = chain('M58,64 C49,58 34,58 25,66 C17,73 16,86 20,93 C24,96 28,93 30,90 C33,95 38,96 41,92 C44,96 50,98 53,94 C56,92 58,84 58,64')
legs = chain('M108,114 C116,114 121,117 125,122 C134,121 140,126 140,132 C140,139 134,143 126,142 L102,142 '
             'L102,154 L126,154 C134,154 140,159 140,166 C140,173 134,177 126,177 C125,176.5 124.5,176 124,176')
assert dome[0].a == TL and dome[-1].b == TR and trunk[0].a == TR and trunk[-1].b == MR
assert ear[0].a == T(62, 58) and ear[-1].b == T(62, 111) and legs[0].a == MR and legs[-1].b == BR

# ---- toenails: three little half-moons along the front of each foot, their ends on the foot's outline ----
def foot(front, spots=((.24, .6), (.82, 1.18), (1.4, 1.76)), k=1.5):
    """front = the two pieces of one foot's front (top to bottom). Positions g run 0..2 along them.
    Returns (outline pieces with the toenail ends as nodes, colour pieces with each toenail's bit of outline swapped for the toenail, toenails)."""
    gs = sorted(g for ab in spots for g in ab)
    subs = []
    for kk in (0, 1):
        ts = [g - kk for g in gs if kk < g < kk + 1]
        pieces = split_many(front[kk], ts) if ts else [front[kk]]
        bounds = [0.0] + ts + [1.0]
        subs += [(p, kk + t0, kk + t1) for p, (t0, t1) in zip(pieces, zip(bounds, bounds[1:]))]
    outline = [p for p, _, _ in subs]
    colour, nails = [], []
    i = 0
    while i < len(subs):
        p, g0, g1 = subs[i]
        nail = next(((a, b) for a, b in spots if abs(g0 - a) < 1e-9), None)
        if nail is None:
            colour.append(p); i += 1; continue
        j = i
        while abs(subs[j][2] - nail[1]) > 1e-9:
            j += 1
        pa, pb = subs[i][0].a, subs[j][0].b
        dx, dy = pb[0] - pa[0], pb[1] - pa[1]; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L   # left of travel = into the foot
        nl = Seg(pa, P(pa[0] + dx * .15 + nx * k, pa[1] + dy * .15 + ny * k), P(pb[0] - dx * .15 + nx * k, pb[1] - dy * .15 + ny * k), pb)
        nails.append(nl); colour.append(nl)
        i = j + 1
    chain_ok(outline); chain_ok(colour)
    return outline, colour, nails

up_o, up_c, nails_up = foot(legs[1:3])
lo_o, lo_c, nails_lo = foot(legs[6:8])
legs_colour = legs[:1] + up_c + legs[3:6] + lo_c + legs[8:]
legs = legs[:1] + up_o + legs[3:6] + lo_o + legs[8:]
chain_ok(legs); chain_ok(legs_colour)
assert legs_colour[0].a == MR and legs_colour[-1].b == BR

# ---- face ----
EYE_C, EYE_R = T(106, 73), 3.6
eye_ring = circle(EYE_C[0], EYE_C[1], EYE_R)
PUPIL = T(107.4, 74)
smile = Seg(T(95, 93), T(97, 100), T(106, 101), T(112, 96))
waves = [Seg(T(178, 22), T(183, 17)), Seg(T(185, 29.5), T(192, 27.5)), Seg(T(186.5, 38), T(193.5, 39))]

steps = [
    step('Start with an E', 'Draw a capital E: a tall straight line, with a line going right at the top, one in the middle and one at the bottom.',
         [line(*e_main), line(*e_mid)]),
    step('The trunk', 'From the end of the top line, draw a long trunk curling up, then come back down to the end of the middle line.', [line(*trunk)]),
    step('The ear', 'From near the top of the tall line, draw a big ear with a frilly bottom, ending just above the middle line.', [line(*ear)]),
    step('Inside the ear', 'Draw a smaller shape inside the ear.', [ring(*ear_in)]),
    step('The feet', 'From the end of the middle line, draw a foot sticking out, a step in, then a second foot, ending at the end of the bottom line.', [line(*legs)]),
    step('Toenails', 'Draw three little toenails on the front of each foot.', [line(n) for n in nails_up + nails_lo]),
    step('Eye, smile and a wave', 'Draw a circle with a dot in it for its eye, a big smile, and three little lines by its trunk to show it waving hello.',
         [ring(*eye_ring), dot(*PUPIL, w=3.2), line(smile)] + [line(w) for w in waves]),
]
assert ear_in[-1].b == ear_in[0].a
ear_in_closed = ear_in
eye_d = d_fill(*eye_ring); earin_d = d_fill(*ear_in_closed)
fills_grey = [
    fill(GREY, *([Seg(TL, TR)] + trunk + [Seg(MR, ML), Seg(ML, TL)]), cut=[eye_d]),
    fill(GREY, *(ear + [Seg(T(62, 111), T(62, 58))]), cut=[earin_d]),
    fill(GREY, *([Seg(ML, MR)] + legs_colour + [Seg(BR, BL), Seg(BL, ML)])),
]
steps += [step('Colour grey', 'Colour the elephant grey, but leave its eye, its toenails and the inside of its ear.', fills_grey, use='grey'),
          step('Colour pink', 'Colour the inside of its ear pink.', [fill(PINK, *ear_in_closed)], use='pink')]

Pd = drawing('dx_elephant_e', 'E is for elephant', 2, 12, 'animals', ['Letters', 'Animals'],
             'A happy elephant waving hello with its trunk. The capital E is its side: the back of its head and body, the top of its head, its jaw and the bottom of its foot.',
             steps, ['grey', 'pink'])
save('elephant', Pd, {'set': 'animals-AZ', 'slot': 'E', 'kind': 'hop', 'age_from': 4})
here = os.path.dirname(os.path.abspath(__file__))
json.dump([eye_d], open(os.path.join(here, 'out', 'elephant.white.json'), 'w'))
