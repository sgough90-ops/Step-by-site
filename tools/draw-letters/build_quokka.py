"""q is for quokka (dx_quokka_q), Animals a to z, slot q (21 Nov 2026).
From Claude's sketch 'quokka (sniffing a flower)' (design 3 of four, from his quokka picture): a quokka on all fours
sniffing a flower. The q's round is its head; the q's stick runs down the front of its chest and front leg, and the
little flick at the bottom is the heel of its front foot. Body, head, tail and paw brown; tummy patch light brown;
insides of the ears pink; flower yellow with a green leaf. Sketch coordinates (200 x 200) go onto the paper by T().
"""
import math, re
from r5kit import *

PA = Paper(0.47, 1.6, -7.9)
T = PA.T
BRN, LB, PNK, YEL, GRN = FILL['brown'], FILL['lbrown'], FILL['pink'], FILL['yellow'], FILL['green']


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


def bump(a, b, h, cen, side=0.12):
    """a round bump (an ear) from a to b, h high, bulging away from cen (all paper points).
    side > 0 lets it bulge out past its ends (the ear); side < 0 keeps it inside them (the inside of the ear)"""
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    if nx * (mx - cen[0]) + ny * (my - cen[1]) < 0: nx, ny = -nx, -ny
    c1 = P(a[0] + nx * h * 1.33 - dx * side, a[1] + ny * h * 1.33 - dy * side)
    c2 = P(b[0] + nx * h * 1.33 + dx * side, b[1] + ny * h * 1.33 + dy * side)
    return Seg(a, c1, c2, b)


# ---- 1: the q ----
ROUND = chain('M78,92 C64,84 40,88 36,108 C32,128 52,140 78,136')
ST, RB, SB, FE = T(78, 92), T(78, 136), T(78, 170), T(94, 180)
assert ROUND[0].a == ST and ROUND[-1].b == RB
FLICK = Seg(SB, T(78, 178), T(84, 182), FE)
f1, f2 = FLICK.split(0.3)
FT = f1.b
stick_a, stick_b = Seg(ST, RB), Seg(RB, SB)

# ears sit on the round: cut it there
CEN = T(56, 112)
e_pts = [P(*ROUND[0].at(t)) for t in (0.62, 0.44, 0.3, 0.1)]
ROUND, ex = cut_at_points(ROUND, e_pts)
E1a, E1b, E2a, E2b = ex
ear1, ear2 = bump(E1a, E1b, 5.0, CEN), bump(E2a, E2b, 5.0, CEN)
in1, in2 = bump(E1a, E1b, 3.0, CEN, -0.1), bump(E2a, E2b, 3.0, CEN, -0.1)

# ---- the body: from the top of the stick over its back, down the back leg to its foot, up the front of the back leg,
# along its tummy and down the back of its front leg to the end of the flick ----
BACK = chain('M78,92 C90,72 138,66 160,84 C172,94 174,114 168,130 C166,140 166,156 168,168 '
             'C170,174 166,178 160,178 L140,178 C136,178 134,174 138,172 C142,170 146,168 148,164')
UNDER = chain('M148,164 C150,154 152,146 148,140 C132,146 104,146 90,140 C90,152 92,166 94,180')
assert BACK[0].a == ST and BACK[-1].b == UNDER[0].a and UNDER[-1].b == FE
# the tail meets the rump, the tummy patch meets the tummy
TA, TB = P(*BACK[1].at(0.42)), P(*BACK[1].at(0.78))
BACK, ex = cut_at_points(BACK, [TA, TB]); TA, TB = ex
BP1, BP2 = P(*UNDER[1].at(0.25)), P(*UNDER[1].at(0.75))
UNDER, ex = cut_at_points(UNDER, [BP1, BP2]); BP1, BP2 = ex
HIP = UNDER[0].b                       # where the back leg meets the tummy
TAIL = snap(chain('M169.9,100.8 C184,112 192,146 194,178 C188,174 184,150 170.8,119'), TA, TB)
patch = [Seg(BP1, T(128, 133), T(109, 133), BP2)]
thigh = [Seg(HIP, T(140, 128), T(138, 116), T(146, 106))]

# ---- the front paw (from the bottom of the stick round to the flick) ----
PAW = snap(chain('M78,170 C70,170 64,174 64,178 C64,182 74,182 79.6,176.1'), SB, FT)

# ---- the face ----
eye = dot(*T(54, 106), w=3.1)
nose = dot(*T(43, 113), w=3.4)
smile = [q2c(T(43, 121), T(50.5, 129), T(60, 123))]
sniff = [q2c(T(27, 104), T(24, 104), T(22, 99)), Seg(T(28, 111), T(23, 110))]

# ---- the flower: a petal ring, a dot in the middle, a stem and a leaf ----
FC = (16, 122)
pts = []
for i in range(10):
    a = math.radians(90 + 36 * i); r = 7.5 if i % 2 == 0 else 4.6
    pts.append((FC[0] + r * math.cos(a), FC[1] + r * math.sin(a)))
pts.append(pts[0])
FLOWER = PA.smooth(pts)
FLOWER[-1] = Seg(FLOWER[-1].a, FLOWER[-1].p[1], FLOWER[-1].p[2], FLOWER[0].a)
chain_ok(FLOWER)
STEM = chain('M16,129.5 C17,150 14,166 16,180')
assert STEM[0].a == FLOWER[0].a
L0 = P(*STEM[0].at(0.55))
STEM, ex = cut_at_points(STEM, [L0]); L0 = ex[0]
LEAF = snap(chain('M15.5,159.7 C24,154 30,146 30,138 C22,140 17,148 15.5,159.7'), L0, L0)
centre = dot(*T(*FC), w=2.6)

steps = [
    step('Start with a q', 'Draw a small letter q: a round shape, a straight stick on its right, and a little flick at the bottom. This q is hiding in the quokka.',
         [line(*ROUND), line(stick_a, stick_b, f1, f2)]),
    step('The body', 'From the top of the stick, draw a big round back, down its back leg to a long foot, along its tummy and down to the end of the flick.',
         [line(*(BACK + UNDER))]),
    step('The front paw', 'At the bottom of the stick, draw its front paw.', [line(*PAW)]),
    step('The tail', 'From its bottom, draw a long thin tail down to the ground.', [line(*TAIL)]),
    step('The ears', 'Draw two little round ears on its head, with a smaller curve inside each one.',
         [line(ear1), line(ear2), line(in1), line(in2)]),
    step('The face', 'Draw an eye, a round nose and a smile.', [eye, nose, line(*smile)]),
    step('Leg and tummy', 'Draw a curve for the top of its back leg and a patch on its tummy.', [line(*thigh), line(*patch)]),
    step('The flower', 'Draw a flower with a dot in the middle, a stem and a leaf. Add two little sniff lines by its nose.',
         [ring(*FLOWER), centre, line(*STEM), ring(*LEAF), line(sniff[0]), line(sniff[1])]),
]

# ---- colours ----
i1 = next(k for k, sg in enumerate(UNDER) if sg.a == BP1); i2 = next(k for k, sg in enumerate(UNDER) if sg.b == BP2)
UNDER_P = UNDER[:i1] + patch + UNDER[i2 + 1:]       # the body's edge goes round the tummy patch
body = fill(BRN, *(BACK + UNDER_P + [f2.rev(), f1.rev(), stick_b.rev(), stick_a.rev()]))
head = fill(BRN, *(ROUND + [stick_a.rev()]))
tail = fill(BRN, *(TAIL + rev(piece(BACK, TA, TB))))
paw = fill(BRN, *(PAW + [f1.rev()]))
ear_out = [fill(BRN, ear1, in1.rev()), fill(BRN, ear2, in2.rev())]
ear_in = [fill(PNK, *([in1] + piece(ROUND, E1b, E1a))), fill(PNK, *([in2] + piece(ROUND, E2b, E2a)))]
steps += [
    step('Colour brown', 'Colour the quokka brown: its head, body, tail, paw and the edges of its ears.', [head, body, tail, paw] + ear_out, use='brown'),
    step('Colour light brown', 'Colour the patch on its tummy light brown.', [fill(LB, *(patch + rev(piece(UNDER, BP1, BP2))))], use='lbrown'),
    step('Colour pink', 'Colour the insides of its ears pink.', ear_in, use='pink'),
    step('Colour yellow', 'Colour the flower yellow.', [fill(YEL, *FLOWER)], use='yellow'),
    step('Colour green', 'Colour the leaf green.', [fill(GRN, *LEAF)], use='green'),
]

D = drawing('dx_quokka_q', 'q is for quokka', 2, 12, 'animals', ['Letters', 'Animals'],
            'A quokka sniffing a flower. The small q is hiding in it: its round head, and the line down its chest and front leg.',
            steps, ['brown', 'lbrown', 'pink', 'yellow', 'green'])
save('quokka', D, {'set': 'animals-az', 'slot': 'q', 'kind': 'hop', 'age_from': 4})
