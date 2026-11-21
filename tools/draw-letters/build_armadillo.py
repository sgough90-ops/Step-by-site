"""a is for armadillo (dx_armadillo_a), Animals a to z, slot a (21 Nov 2026).
From Claude's sketch 'armadillo (out for a walk)' (round 2 of his armadillo pictures), which follows his picture of an
armadillo with a small a in it: the a's round is its head, and the a's stick is the line behind its head where the shell
starts. A later step carries the stick on down as the front of its front leg. Shell brown; head, legs, paws and tail light
brown; ears and nose pink. Sketch coordinates (200 x 200) go onto the app's paper by T() (0.48 scale).
"""
import json, os, re
from r5kit import *

PA = Paper(0.48, 1.6, 0.4)
T = PA.T
LB, BRN, PNK = FILL['lbrown'], FILL['brown'], FILL['pink']


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


def sk(seg_list, k, t):
    """a point on piece k of a sketch chain, as a paper point"""
    return P(*seg_list[k].at(t))


def lowest_at_x(ch, x):
    """the lowest point of a chain at a given paper x (for points on the underside)"""
    best = None
    for s in ch:
        pts = [s.at(j / 400) for j in range(401)]
        for p, q in zip(pts, pts[1:]):
            if (p[0] - x) * (q[0] - x) <= 0 and p[0] != q[0]:
                u = (x - p[0]) / (q[0] - p[0]); y = p[1] + u * (q[1] - p[1])
                if best is None or y > best[1]: best = (x, y)
    return best


# ---- 1: the a ----
ROUND = chain('M64,88 C52,80 32,84 27,100 C22,116 40,128 64,124')
ST, RB, SB = T(64, 88), T(64, 124), T(64, 138)
assert ROUND[0].a == ST and ROUND[-1].b == RB
stick = Seg(ST, RB)
stick_more = Seg(RB, SB)

# ---- the shell (from the top of the stick, over its back and underneath, back to the bottom of the a) ----
SHELL = chain('M64,88 C70,66 100,56 124,58 C146,60 160,78 158,102 C157,114 150,122 140,124 C116,126 88,128 64,124')
assert SHELL[0].a == ST and SHELL[-1].b == RB
# band ends: tops on the top edge, bottoms on the underside
band_top = [P(*SHELL[0].at(t)) for t in (0.58, 0.72, 0.86)] + [P(*SHELL[1].at(t)) for t in (0.0, 0.14)]
band_bot = [lowest_at_x(SHELL[2:], T(x, 0)[0]) for x in (100, 108, 116, 124, 132)]
LEGX = {k: lowest_at_x(SHELL[2:], T(x, 0)[0]) for k, x in (('f2', 78), ('b1', 104), ('b2', 116), ('n1', 128), ('n2', 142))}
tail_o, tail_i = P(*SHELL[2].at(0.08)), P(*SHELL[2].at(0.38))
cuts = band_top + band_bot + [LEGX[k] for k in ('f2', 'b1', 'b2', 'n1', 'n2')] + [tail_o, tail_i]
SHELL, ex = cut_at_points(SHELL, cuts)
BT, BB = ex[0:5], ex[5:10]
F2, B1, B2, N1, N2 = ex[10:15]
TO, TI = ex[15:17]
bands = [Seg(a, P(a[0] + (b[0] - a[0]) / 3 + 1.2, a[1] + (b[1] - a[1]) / 3), P(a[0] + 2 * (b[0] - a[0]) / 3 + 1.2, a[1] + 2 * (b[1] - a[1]) / 3), b) for a, b in zip(BT, BB)]
scales = [dot(*T(x, y), w=1.5) for x, y in [(76, 82), (84, 96), (80, 112), (90, 84), (146, 86), (150, 104), (142, 112)]]

# ---- ears and the far front leg meet the round: cut it there ----
e_pts = [P(*ROUND[0].at(t)) for t in (0.55, 0.4, 0.25, 0.1)]
fl_pts = [P(*ROUND[1].at(t)) for t in (0.6, 0.8)]
ROUND, ex = cut_at_points(ROUND, e_pts + fl_pts)
E1a, E1b, E2a, E2b, FL1, FL2 = ex
ear1 = snap(chain('M40.7,85.6 C34,76 32,64 36,58 C44,60 48,72 47.2,84.2'), E1a, E1b)
ear2 = snap(chain('M53.9,84.3 C50,74 52,62 58,56 C64,62 63,76 60.2,86'), E2a, E2b)

# ---- paws (rounded boxes) and legs ----
def paw(x0, x1, y0, y1, tops):
    ring_ = rrect(*T(x0, y0), *T(x1, y1), 2.4 * 0.48)
    ring_, ex_ = cut_at_points(ring_, [T(x, y0) for x in tops])
    return ring_, ex_
paw_ff, (PF1, PF2) = paw(25, 47, 140, 149, (37, 46))
paw_nf, (PN1, PN2) = paw(56, 86, 138, 147, (64, 78))
paw_fb, (PB1, PB2) = paw(98, 120, 138, 147, (104, 116))
paw_nb, (PQ1, PQ2) = paw(124, 148, 138, 147, (128, 142))
assert PN1 == SB, (PN1, SB)
far_front = [Seg(FL1, PF1), Seg(FL2, PF2)]
near_front_back = Seg(F2, PN2)
far_back = [Seg(B1, PB1), Seg(B2, PB2)]
near_back = [Seg(N1, PQ1), Seg(N2, PQ2)]

def claws(paw_ring, x0, y0):
    out = []
    for dy in (3.0, 4.5, 6.0):
        p = T(x0, y0 + dy)
        out.append(line(Seg(p, P(p[0] - 2.4, p[1] + (dy - 4.5) * 0.35)), w=1.3))
    return out

# ---- the tail, with three rings ----
TAIL = snap(chain('M157.6,104.8 C172,112 184,128 188,144 C189,148 193,149 196,147 C191,152 184,152 181,147 C176,134 166,122 154.4,113.8'), TO, TI)
ring_o = [P(*TAIL[0].at(t)) for t in (0.3, 0.5, 0.7)]
ring_i = [P(*TAIL[3].at(t)) for t in (0.7, 0.5, 0.3)]
TAIL, ex = cut_at_points(TAIL, ring_o + ring_i)
rings = [Seg(a, b) for a, b in zip(ex[0:3], ex[3:6])]

# ---- the face ----
eye = [q2c(T(43, 100), T(48, 93), T(53, 100))]
nose = circle(*T(35.6, 104), 3.1 * 0.48)
smile = [q2c(T(38, 113), T(46, 119), T(55, 113))]
freckles = [dot(*T(x, y), w=1.2) for x, y in [(48, 108), (51.5, 110.5), (45.5, 111)]]

steps = [
    step('Start with an a', 'Draw a small letter a: a round shape with a straight stick on its right. This a is hiding in the armadillo.',
         [line(*ROUND), line(stick)]),
    step('The shell', 'From the top of the stick, draw a big round shell over its back and underneath, back to the bottom of the a.',
         [line(*SHELL)]),
    step('Stripes', 'Draw five curved stripes across the middle of the shell, and some little dots at each end.',
         [line(b) for b in bands] + scales),
    step('The front leg', 'Carry the stick on down for the front of its leg. Draw the back of the leg and a paw with three claws.',
         [line(stick_more), line(near_front_back), ring(*paw_nf)] + claws(paw_nf, 56, 138)),
    step('The other front leg', 'Under its chin, draw two short lines down to another paw with claws.',
         [line(*[far_front[0]]), line(*[far_front[1]]), ring(*paw_ff)] + claws(paw_ff, 25, 140)),
    step('The back legs', 'Under the back of the shell, draw two more legs, each with a paw.',
         [line(s) for s in far_back + near_back] + [ring(*paw_fb), ring(*paw_nb)]),
    step('The tail', 'From the back of the shell, draw a long tail that sweeps down to the ground. Add three rings.',
         [line(*TAIL)] + [line(r) for r in rings]),
    step('The ears', 'Draw two tall ears on top of its head.', [line(*ear1), line(*ear2)]),
    step('The face', 'Draw a happy closed eye, a round nose, a big smile and three freckles.',
         [line(*eye), ring(*nose), line(*smile)] + freckles),
]

# ---- colours ----
nose_hole = d_fill(*nose)
shell_fill = fill(BRN, *(SHELL + [stick.rev()]))
head = fill(LB, *(ROUND + [stick.rev()]), cut=[nose_hole])
def between(ch, p, q):
    return piece(ch, p, q)
def leg_fill(e1, e2, paw_ring, top1, top2, base):
    """a leg: down edge e1, along the paw top, up edge e2 (reversed), then back along base"""
    return fill(LB, *([e1] + piece(paw_ring, top1, top2) + [e2.rev()] + base))
ff = fill(LB, *([far_front[0]] + piece(paw_ff, PF1, PF2) + [far_front[1].rev()] + rev(piece(ROUND, FL1, FL2))))
nf = fill(LB, *([stick_more] + piece(paw_nf, PN1, PN2) + [near_front_back.rev()] + piece(SHELL, F2, RB)))
fb = fill(LB, *([far_back[0]] + piece(paw_fb, PB1, PB2) + [far_back[1].rev()] + piece(SHELL, B2, B1)))
nb = fill(LB, *([near_back[0]] + piece(paw_nb, PQ1, PQ2) + [near_back[1].rev()] + piece(SHELL, N2, N1)))
paws = [fill(LB, *r) for r in (paw_ff, paw_nf, paw_fb, paw_nb)]
tail_fill = fill(LB, *(TAIL + rev(piece(SHELL, TO, TI))))
ears = [fill(PNK, *(ear1 + piece(ROUND, E1b, E1a))), fill(PNK, *(ear2 + piece(ROUND, E2b, E2a)))]
steps += [
    step('Colour brown', 'Colour the shell brown.', [shell_fill], use='brown'),
    step('Colour light brown', 'Colour its head, legs, paws and tail light brown. Leave the nose.', [head, ff, nf, fb, nb] + paws + [tail_fill], use='lbrown'),
    step('Colour pink', 'Colour its ears and its nose pink.', ears + [fill(PNK, *nose)], use='pink'),
]

D = drawing('dx_armadillo_a', 'a is for armadillo', 2, 12, 'animals', ['Letters', 'Animals'],
            'An armadillo out for a walk. The small a is hiding in it: its round head, and the line where its shell starts.',
            steps, ['brown', 'lbrown', 'pink'])
save('armadillo', D, {'set': 'animals-az', 'slot': 'a', 'kind': 'hop', 'age_from': 4})
