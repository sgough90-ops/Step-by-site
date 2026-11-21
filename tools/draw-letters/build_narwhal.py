"""N is for narwhal (dx_narwhal_n), Animals A to Z, slot N. From Claude's round-3 sketch 'Narwhal (spouting water)',
drawn without the water, as he asked (21 Nov 2026). Idea from ART'S ROOM's narwhal from a capital N (aRKqkh8BjCI).

The N is in its chest: the first line and the slanting line are the edges of its pale tummy, the last line is its throat.
Sketch coordinates (200 x 200) are turned into the app's 100 x 100 paper by T().
"""
import re
from kit15 import *

OX, OY = -12.0, -0.5
def T(x, y):
    return P(x * 0.5 + OX, y * 0.5 + OY)

def chain(d):
    """Pieces from a sketch path made of M, C and L (absolute)."""
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

BLUE, YELLOW = FILL['blue'], FILL['yellow']

# ---- the N ----
TL, BL, BR, TR = T(80, 100), T(80, 146), T(116, 146), T(116, 100)
n_letter = [Seg(BL, TL), Seg(TL, BR), Seg(BR, TR)]

# ---- the outline ----
head = chain('M116,100 C117,95 119,92 124,89 C132,85 140,76 141,62 C142,46 128,30 108,27 C88,25 70,36 64,54 C60,66 59,84 59,104')
back = chain('M59,104 C58,134 66,160 86,176 C102,188 124,193 146,188 C152,187 156,186 160,185')
tail = chain('M160,185 C168,190 178,193 190,192 C184,186 179,181 177,176 C181,170 186,162 190,152 C180,155 170,161 163,168')
front = chain('M163,168 C156,170 150,170 146,168 C136,164 124,158 116,146')
assert head[0].a == TR and front[-1].b == BR and head[-1].b == back[0].a and back[-1].b == tail[0].a and tail[-1].b == front[0].a
J = front[0].b                       # where the tummy line meets the front, by the tail
belly = chain('M80,146 C84,168 104,182 128,180 C136,178 142,172 146,168')
assert belly[0].a == BL and belly[-1].b == J

# ---- the tusk: two straight edges from the head out to the tip ----
base = (128, 42); ang = math.radians(-38); ln = 58; wd = 16
ux, uy = math.cos(ang), math.sin(ang); px, py = -uy, ux
b1 = (base[0] + px * wd / 2, base[1] + py * wd / 2)        # lower edge
b2 = (base[0] - px * wd / 2, base[1] - py * wd / 2)        # upper edge
TIP = T(base[0] + ux * ln, base[1] + uy * ln)
B1, B2 = T(*b1), T(*b2)
FH = 2                                                     # the head piece the tusk meets: (141,62) -> (108,27)
h1 = [t for t, q in line_hits_seg(B1, TIP, head[FH])]
h2 = [t for t, q in line_hits_seg(B2, TIP, head[FH])]
assert len(h1) == 1 and len(h2) == 1, (h1, h2)
t1, t2 = h1[0], h2[0]
assert t1 < t2
pa, rest = head[FH].split(t1)
pb, pc = rest.split((t2 - t1) / (1 - t1))
head = head[:FH] + [pa, pb, pc] + head[FH + 1:]
H1, H2 = pa.b, pb.b                                        # where the lower and upper edges of the tusk meet the head
tusk = [Seg(H1, TIP), Seg(TIP, H2)]
grooves = []
for k in range(1, 6):
    f = k / 6.4
    e1 = tusk[0].at(f); e2 = tusk[1].at(1 - f - 0.05)
    q1 = P(*e1); q2 = P(*e2)
    mid = ((q1[0] + q2[0]) / 2 + ux * 1.2, (q1[1] + q2[1]) / 2 + uy * 1.2)
    grooves.append(Seg(q1, P(q1[0] + (mid[0] - q1[0]) * .9, q1[1] + (mid[1] - q1[1]) * .9),
                       P(q2[0] + (mid[0] - q2[0]) * .9, q2[1] + (mid[1] - q2[1]) * .9), q2))

# ---- face ----
def q2c(p0, q, p2):
    a, b, c = T(*p0), T(*q), T(*p2)
    return Seg(a, (a[0] + 2 / 3 * (b[0] - a[0]), a[1] + 2 / 3 * (b[1] - a[1])), (c[0] + 2 / 3 * (b[0] - c[0]), c[1] + 2 / 3 * (b[1] - c[1])), c)
smile = q2c((118, 70), (126, 78), (134, 69))
EYE = T(106, 56)

steps = [
    step('Start with an N', 'Draw a capital N: two tall straight lines, joined by a slanting line from the top of the first down to the bottom of the second.',
         [line(*n_letter)]),
    step('The big head', 'From the top of the last line, draw a little chin, then a big round head that comes down at the back.', [line(*head)]),
    step('The back', 'Carry on down its back and round underneath, to where its tail starts.', [line(*back)]),
    step('The tail', 'Draw a tail fin with two points.', [line(*tail)]),
    step('The front', 'From the tail, curve back up to the bottom of the last line of the N.', [line(*front)]),
    step('The tummy line', 'From the bottom of the first line of the N, draw a curve down to the tail.', [line(*belly)]),
    step('The tusk', 'Draw a long pointy tusk from the top of its head, with little lines across it.', [line(*tusk)] + [line(g) for g in grooves]),
    step('Eye and smile', 'Draw a dot for its eye and a happy smile.', [dot(*EYE, w=5.2), line(smile)]),
]
# blue: everything but the tummy (the tummy is left white)
body_fill = fill(BLUE, *(head + back + tail + front[:1] + rev(belly) + n_letter))
tusk_fill = fill(YELLOW, *(tusk + [pb.rev()]))
steps += [step('Colour blue', 'Colour the narwhal blue, but leave its tummy white.', [body_fill], use='blue'),
          step('Colour yellow', 'Colour the tusk yellow.', [tusk_fill], use='yellow')]

Pd = drawing('dx_narwhal_n', 'N is for narwhal', 2, 10, 'animals', ['Letters', 'Animals'],
             'A happy narwhal with a long spiral tusk. The capital N is hiding in its chest: the edges of its white tummy and the front of its throat.',
             steps, ['blue', 'yellow'])
save('narwhal', Pd, {'set': 'animals-AZ', 'slot': 'N', 'kind': 'swim', 'age_from': 4})
