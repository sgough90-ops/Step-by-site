"""h is for horse (dx_horse_h), Animals a to z, slot h (21 Nov 2026).
From Claude's round 4 sketch 'horse (a natural horse, no rug)': a bay horse standing with its head up, the thick neck he
liked from round 3 horse 1, no rug, and a more natural look than the earlier cartoon horses. The small h: its stick runs
from between its ears down the back of its neck, the back of its shoulder and the back of its front leg; the hump is its
back, over its rump and down the back of its back leg. Coat brown; mane, forelock, tail, eye and hooves black.
Sketch coordinates (200 x 200) go onto the paper by T().
"""
import math, re
from r5kit import *

PA = Paper(0.52, -5.4, 0.4)
T = PA.T
BRN, BLK = FILL['brown'], FILL['black']


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


def at_x(seg, x):
    a, b = 0.0, 1.0; fa = seg.at(a)[0] - x
    for _ in range(60):
        m = (a + b) / 2; fm = seg.at(m)[0] - x
        if (fa < 0) == (fm < 0): a, fa = m, fm
        else: b = m
    return P(*seg.at((a + b) / 2))


# ---- 1: the h ----
POLL, BASE = T(84, 26), T(84, 178)
W = T(84, 86)
ARCH = chain('M84,86 C100,74 138,74 158,78 C172,82 176,96 176,112 L176,178')
assert ARCH[0].a == W
TA, TB = P(*ARCH[1].at(0.3)), P(*ARCH[1].at(0.85))        # the tail meets the rump here
HC = T(176, 171)                                          # back hoof's top meets the back of its leg
ARCH, ex = cut_at_points(ARCH, [TA, TB, HC]); TA, TB, HC = ex
STICK_PTS = [T(84, 33), T(84, 64), W, T(84, 128), T(84, 171)]
stick = [Seg(a, b) for a, b in zip([POLL] + STICK_PTS, STICK_PTS + [BASE])]
FL, MN, _, BL, FC = STICK_PTS                              # forelock end, mane end, withers, tummy, front hoof top

# ---- head, neck, chest and front leg (left of the stick) ----
FRONT = chain('M84,26 C74,26 64,30 56,36 C46,44 34,56 26,64 C21,69 19,76 22,80 C25,85 31,87 37,85 '
              'C46,86 56,84 62,76 C64,72 64,69 63,66 C60,82 54,98 52,112 C50,124 56,134 64,138 '
              'C66,144 68,148 70,152 C71,156 73,160 73,164 C73,166 72,168 71,171')
E0 = P(*FRONT[0].at(0.28))                                 # the near ear's front foot
PF = P(*FRONT[0].at(0.66))                                 # the forelock's tip on the forehead
FRONT, ex = cut_at_points(FRONT, [E0, PF]); E0, PF = ex
FH = FRONT[-1].b                                           # front hoof's top, at the front
coronet_f = Seg(FH, FC)
hoof_f = [Seg(BASE, T(67, 178)), Seg(T(67, 178), FH)]
forelock = chain('M64,31 C66,36 70,38 73,41 C74,38 78,34 84,33')
forelock = snap(forelock, PF, FL)

# ---- the tummy and the front of the back leg ----
UNDER = chain('M84,128 C104,134 132,134 150,127 C152,129 154,132 158,136 C160,140 162,146 162,154 C162,160 163,166 163,171')
assert UNDER[0].a == BL
# the far legs meet the tummy here
LEGT = [at_x(UNDER[0], T(x, 0)[0]) for x in (93, 104, 134, 147)]
UNDER, ex = cut_at_points(UNDER, LEGT); F1a, F1b, F2a, F2b = ex
STIFLE = next(s.b for s in UNDER if math.dist(s.b, T(150, 127)) < 0.6)
HH = UNDER[-1].b
coronet_h = Seg(HH, HC)
hoof_h = [Seg(ARCH[-1].b, T(159, 178)), Seg(T(159, 178), HH)]

# ---- far legs, seen in the gap ----
farF = snap(chain('M93,131 C93,142 95,152 96,160 L97,170 L106,170 L106,160 C106,150 104,140 104,132'), F1a, F1b)
farH = snap(chain('M134,130 C136,140 140,148 142,154 L142,170 L151,170 L151,154 C150,146 148,138 147,131'), F2a, F2b)
def find(ch, p): return next(s.a for s in ch if math.dist(s.a, p) < 0.3)
fF1, fF2 = find(farF, T(97, 170)), find(farF, T(106, 170))
fH1, fH2 = find(farH, T(142, 170)), find(farH, T(151, 170))
hoof_fF = [Seg(fF1, T(95, 178)), Seg(T(95, 178), T(108, 178)), Seg(T(108, 178), fF2)]
hoof_fH = [Seg(fH1, T(140, 178)), Seg(T(140, 178), T(153, 178)), Seg(T(153, 178), fH2)]

# ---- mane, ears ----
MANE = chain('M84,26 C94,26 102,32 104,42 C110,46 110,54 104,58 C106,62 102,66 94,64 C90,64 87,64 84,64')
MANE = snap(MANE, POLL, MN)
G0, G1 = P(*MANE[0].at(0.22)), P(*MANE[0].at(0.5))         # the far ear stands on the mane
MANE, ex = cut_at_points(MANE, [G0, G1]); G0, G1 = ex
ear_n = snap(chain('M75.5,26.6 C74,20 75,14 78,10 C82,14 84,20 84,26'), E0, POLL)
ear_f = snap(chain('M87.4,26.2 C89,20 91,16 94,13 C96,18 95,23 92.6,27.2'), G0, G1)

# ---- the tail ----
TAIL = snap(chain('M168.6,80.6 C184,86 194,102 194,124 C194,140 192,154 188,166 C186,150 186,128 186,118 C186,110 182,106 175.8,104.6'), TA, TB)

# ---- face and leg lines ----
eye = chain('M52,47 C55,44 60,44 62,46 C60,49 55,50 52,47')
lid = chain('M51,42 C55,38 60,38 63,41')
nostril = chain('M29,68 C27,70 28,73 31,72')
M0 = next(sg.a for sg in FRONT if math.dist(sg.a, T(22, 80)) < 0.6)
mouth = [Seg(M0, T(26, 80), T(30, 80), T(34, 82))]
knee = [q2c(T(75, 147), T(77.5, 149.5), T(78, 154))]
shoulder = [q2c(T(58, 114), T(63, 120), T(62, 128))]
stifle = [Seg(STIFLE, T(156, 116), T(160, 104), T(158, 92))]

steps = [
    step('Start with an h', 'Draw a small letter h: a tall straight stick, then a hump that starts part way down and comes down to the bottom. This h is hiding in the horse.',
         [line(*stick), line(*ARCH)]),
    step('Head, neck and front leg', 'From the top of the stick, draw its long head, then its thick neck down to its chest, and down the front of its leg.',
         [line(*FRONT)]),
    step('Tummy and back leg', 'From the stick, draw its tummy across, then down the front of its back leg.', [line(*UNDER)]),
    step('Hooves', 'Draw a hoof at the bottom of each leg.', [line(coronet_f), line(*hoof_f), line(coronet_h), line(*hoof_h)]),
    step('The far legs', 'Draw its other two legs, behind, each with a hoof.', [line(*farF), line(*hoof_fF), line(*farH), line(*hoof_fH)]),
    step('Mane and forelock', 'Draw its mane along the top of its neck, and a forelock on its forehead.', [line(*MANE), line(*forelock)]),
    step('Ears and tail', 'Draw two pointed ears, and a long tail from the top of its bottom.', [line(*ear_n), line(*ear_f), line(*TAIL)]),
    step('The face', 'Draw an eye with a lid line above it, a nostril and its mouth.', [ring(*eye), line(*lid), line(*nostril), line(*mouth)]),
    step('Leg lines', 'Draw little curves for its knee, its shoulder and the top of its back leg.', [line(*knee), line(*shoulder), line(*stifle)]),
]

# ---- colours ----
def pc(ch, p, q): return piece(ch, p, q)
front = fill(BRN, *(piece(FRONT, PF, FH) + [coronet_f] + rev(stick[1:5]) + rev(forelock)), cut=[d_fill(*eye)])
# rev(stick[1:5]) runs from the front hoof top up to the forelock end
body = fill(BRN, *(piece(ARCH, W, HC) + [coronet_h.rev()] + rev(UNDER) + rev([stick[3]])))
far_f = fill(BRN, *(farF + rev(piece(UNDER, F1a, F1b))))
far_h = fill(BRN, *(farH + rev(piece(UNDER, F2a, F2b))))
ears = [fill(BRN, *(ear_n + piece(FRONT, POLL, E0))), fill(BRN, *(ear_f + rev(piece(MANE, G0, G1))))]
mane = fill(BLK, *(MANE + rev(stick[0:2])))
fore = fill(BLK, *(piece(FRONT, POLL, PF) + forelock + [stick[0].rev()]))
tail = fill(BLK, *(TAIL + rev(piece(ARCH, TA, TB))))
hooves = [fill(BLK, *([coronet_f, stick[5]] + hoof_f)), fill(BLK, *([coronet_h, ARCH[-1]] + hoof_h)),
          fill(BLK, *(hoof_fF + [Seg(fF2, fF1)])), fill(BLK, *(hoof_fH + [Seg(fH2, fH1)]))]
steps += [
    step('Colour brown', 'Colour the horse brown: its head, neck, body, legs and ears.', [front, body, far_f, far_h] + ears, use='brown'),
    step('Colour black', 'Colour its mane, forelock, tail, eye and hooves black.', [mane, fore, tail, fill(BLK, *eye)] + hooves, use='black'),
]

D = drawing('dx_horse_h', 'h is for horse', 2, 14, 'animals', ['Letters', 'Animals'],
            'A horse standing tall. The small h is hiding in it: the line down the back of its neck and front leg, and the hump of its back.',
            steps, ['brown', 'black'])
save('horse', D, {'set': 'animals-az', 'slot': 'h', 'kind': 'walk', 'age_from': 4})
