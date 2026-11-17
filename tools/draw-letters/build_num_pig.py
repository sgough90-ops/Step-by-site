"""6 is for Pig (dx_pig_6), Animals 1 to 9, slot 6. Built from Claude's sketch "Pig 4" (picked 17 Nov 2026).
The 6 is the pig's curly tail: it comes down from its bottom and curls into a closed loop."""
from numkit import *

PK, RD = FILL['pink'], FILL['red']

body = Ell(58, 54, 26, 19)
head = Ell(82, 49, 13)
GY = 82                                            # the ground

# the 6: the tail
TS = body.P(180 + math.degrees(math.asin(6 / 19)))
loop = Ell(18, 68, 9)
stem = Seg(TS, (22, 47), (9, 56), loop.P(180))
loop_segs = loop.arc(180, -180, start=loop.P(180), end=loop.P(180))

# head and body cross at the top (Q1) and bottom (Q2) of the head's left side
Q = meet_ee(head, body)
Q2, Q1 = sorted(Q, key=lambda p: -p[1])            # Q2 lower, Q1 upper

# legs: two lines down from the tummy to the ground for each
def tummy(x):
    return P(x, body.cy + body.ry * math.sqrt(1 - ((x - body.cx) / body.rx) ** 2))
XS = [37, 44, 48, 55, 62, 69, 73, 80]
LT = [tummy(x) for x in XS]
legs = [Seg(t, P(t[0], GY)) for t in LT]
ground = Seg((20, GY), (96, GY))

# body line: from the top of the head round the back (past the end of the 6), under the tummy, to the bottom of the head
bpts = [Q1, TS] + LT + [Q2]
body_line = []
for a, b in zip(bpts, bpts[1:]):
    body_line += body.arc_pts(a, b, cw=False)

# ears: each is two lines from the head up to a point
EL1, EL2, ER1, ER2 = head.P(-121), head.P(-99), head.P(-81), head.P(-59)
ear_l = [Seg(EL1, (71.4, 29.4)), Seg((71.4, 29.4), EL2)]
ear_r = [Seg(ER1, (92.6, 29.4)), Seg((92.6, 29.4), ER2)]
head_ring = head.ring_at([Q1, EL1, EL2, ER1, ER2, Q2], cw=True)

snout = Ell(82, 55, 5.6, 4)
spots = [Ell(49.5, 47.5, 4.5, 3), Ell(60.5, 62, 5, 3), Ell(62.8, 45.4, 3.4, 2.4)]

steps = [
    step('Start with a 6', 'Draw a big 6: start at the top, curve down to the left and round into a closed loop at the bottom.', [line(stem, *loop_segs)]),
    step('The head', 'Draw a big circle for the head over on the right, a little higher than the top of the 6.', [ring(*head_ring)]),
    step('The body', 'Draw a big round body from the top of the head, back past the top of the 6 and round under to the head again.', [line(*body_line)]),
    step('The ears', 'Draw two pointy ears on top of the head.', [line(*ear_l), line(*ear_r)]),
    step('The face', 'Draw two dots for the eyes, and an oval snout with two dots in it.',
         [dot(77.4, 45.6, 2.8), dot(86.6, 45.6, 2.8), ring(*snout.ring()), dot(80, 55, 2.4), dot(84, 55, 2.4)]),
    step('The legs', 'Draw a line for the ground. Then draw four legs: two straight lines down from the tummy to the ground for each.',
         [line(ground)] + [line(l) for l in legs]),
    step('The spots', 'Draw three oval spots on the pig’s back.', [ring(*s.ring()) for s in spots]),
]
# colour outlines
left_of_head = head.arc_pts(Q2, Q1, cw=True)       # the head's left side, inside the body
body_fill = fill(PK, *body_line, *left_of_head, cut=[d_fill(*s.ring()) for s in spots])
head_fill = fill(PK, *head_ring, cut=[d_fill(*snout.ring())])
ear_fills = [fill(PK, *ear_l, *head.arc_pts(EL2, EL1, cw=False)), fill(PK, *ear_r, *head.arc_pts(ER2, ER1, cw=False))]
leg_fills = []
for i in range(0, 8, 2):
    a, b = LT[i], LT[i + 1]
    leg_fills.append(fill(PK, legs[i], Seg(P(a[0], GY), P(b[0], GY)), legs[i + 1].rev(), *body.arc_pts(b, a, cw=True)))
steps += [
    step('Colour pink', 'Colour the pig pink: its body, head, ears and legs.', [body_fill, head_fill] + ear_fills + leg_fills, use='pink'),
    step('Colour red', 'Colour the snout and the spots red.', [fill(RD, *snout.ring())] + [fill(RD, *s.ring()) for s in spots], use='red'),
]
P_ = drawing('dx_pig_6', '6 is for Pig', 2, 10, 'animals', ['Numbers', 'Animals'],
             'A spotty pig turning to look at you. The 6 is hiding in it: it is the pig’s curly tail, coming down '
             'and curling into a closed loop.',
             steps, ['pink', 'red'])
P_ = move(P_, 0, 3)                                # sit it a little lower on the paper
save('num6pig', P_, {'set': 'animals-09', 'slot': '6', 'kind': 'hop', 'age_from': 5})
