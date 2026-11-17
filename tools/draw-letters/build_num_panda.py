"""8 is for Panda (dx_panda_8), Animals 1 to 9, slot 8. Built from Claude's sketch "Panda 4" (picked 17 Nov 2026).
The 8 is the panda's round head and its bigger round body, one on top of the other."""
import json, os
from numkit import *

BK, PK, GR = FILL['black'], FILL['pink'], FILL['green']

# the 8: two circles, just touching
H = Ell(50, 28, 15)
B = Ell(50, 63, 20)
eight = [ring(*H.ring(90)), ring(*B.ring(-90))]

# ears: round, peeping over the top of the head
def ear(E):
    a, b = meet_ee(E, H)                       # where the ear crosses the head
    pts = sorted([a, b], key=lambda p: p[0])
    return pts, E.arc_pts(pts[0], pts[1], cw=True) if E.cx < H.cx else E.arc_pts(pts[0], pts[1], cw=True)
earL, earR = Ell(38, 16, 5.5), Ell(62, 16, 5.5)
eL_pts, eL_arc = ear(earL)
eR_pts, eR_arc = ear(earR)

# face
patchL, patchR = Ell(44, 27.4, 3.8, 4.8, 20), Ell(56, 27.4, 3.8, 4.8, -20)
eyeL, eyeR = Ell(44.6, 26.6, 1.8), Ell(55.4, 26.6, 1.8)
nose = Ell(50, 33.6, 2.6, 1.8)
NB = nose.P(90)
MC = P(50, 37.4)
mouth = [Seg(NB, MC)]
smile = [Seg((45.4, 37.6), (46.6, 38.9), (48.8, 38.9), MC), Seg(MC, (51.2, 38.9), (53.4, 38.9), (54.6, 37.6))]

# arms: big ovals behind the body, peeping out at the sides
armL, armR = Ell(31, 59, 6, 12, 18), Ell(69, 59, 6, 12, -18)
aL = sorted(meet_ee(armL, B), key=lambda p: p[1])     # top, bottom
aR = sorted(meet_ee(armR, B), key=lambda p: p[1])
armL_arc = armL.arc_pts(aL[1], aL[0], cw=True)         # round the outside, bottom to top
armR_arc = armR.arc_pts(aR[0], aR[1], cw=True)         # round the outside, top to bottom

# feet and legs
footL, footR = Ell(26, 82, 7, 5.5), Ell(74, 82, 7, 5.5)
LU0, LL0 = B.P(150), B.P(126)                          # leg roots on the body (left)
LU1, LL1 = footL.P(-70), footL.P(-5)
RU0, RL0 = B.P(30), B.P(54)                            # right
RU1, RL1 = footR.P(250), footR.P(185)
legL = [Seg(LU0, LU1), Seg(LL0, LL1)]
legR = [Seg(RU0, RU1), Seg(RL0, RL1)]
footL_ring = footL.ring_at([LU1, LL1], cw=True)
footR_ring = footR.ring_at([RL1, RU1], cw=True)
def pads(cx):
    return [Ell(cx, 83.5, 2.5), Ell(cx - 3.7, 79.6, 1.4), Ell(cx, 78.7, 1.4), Ell(cx + 3.7, 79.6, 1.4)]
padsL, padsR = pads(26), pads(74)

# bamboo
stalkL = rrect(9, 18, 13, 89, 2)
stalkR = rrect(88, 20, 92, 90, 2)
nodes = [Seg((9, 38), (13, 38)), Seg((9, 62), (13, 62)), Seg((88, 44), (92, 44)), Seg((88, 66), (92, 66))]
lfL0, lfL1 = P(13, 27), P(23.4, 21)
leafL = [Seg(lfL0, (15.2, 22.2), (19.6, 20.2), lfL1), Seg(lfL1, (19.6, 24.6), (16.2, 27.2), lfL0)]
lfR0, lfR1 = P(88, 30), P(77.2, 24.6)
leafR = [Seg(lfR0, (85.4, 25.6), (81, 24), lfR1), Seg(lfR1, (80.8, 28.2), (84.6, 30.4), lfR0)]

steps = [
    step('Start with an 8', 'Draw an 8 as two circles: a smaller one on top of a bigger one, just touching.', eight),
    step('The ears', 'Draw two round ears on top of the head.', [line(*eL_arc), line(*eR_arc)]),
    step('The eyes', 'Draw two tilted ovals for the eye patches, with a small circle and a dot in each.',
         [ring(*patchL.ring()), ring(*patchR.ring()), ring(*eyeL.ring()), ring(*eyeR.ring()), dot(44.6, 26.6, 2.0), dot(55.4, 26.6, 2.0)]),
    step('Nose and mouth', 'Draw an oval nose, a short line down from it, and a smile.', [ring(*nose.ring(90)), line(*mouth), line(*smile)]),
    step('The arms', 'Draw a big rounded arm peeping out on each side of the body.', [line(*armL_arc), line(*armR_arc)]),
    step('The feet', 'Draw two round feet at the bottom corners, and join each one to the body with two lines.',
         [ring(*footL_ring), ring(*footR_ring)] + [line(s) for s in legL + legR]),
    step('Paw pads', 'Draw a round pad and three little toes on each foot.', [ring(*e.ring()) for e in padsL + padsR]),
    step('The bamboo', 'Draw a tall bamboo stalk on each side, with lines across them and a leaf on each.',
         [ring(*stalkL), ring(*stalkR)] + [line(n) for n in nodes] + [ring(*leafL), ring(*leafR)]),
]
# colour outlines
ear_fill = [fill(BK, *eL_arc, *H.arc_pts(eL_pts[1], eL_pts[0], cw=False)), fill(BK, *eR_arc, *H.arc_pts(eR_pts[1], eR_pts[0], cw=False))]
patch_fill = [fill(BK, *patchL.ring(), cut=[d_fill(*eyeL.ring())]), fill(BK, *patchR.ring(), cut=[d_fill(*eyeR.ring())])]
arm_fill = [fill(BK, *armL_arc, *B.arc_pts(aL[0], aL[1], cw=False)), fill(BK, *armR_arc, *B.arc_pts(aR[1], aR[0], cw=False))]
leg_fill = [fill(BK, legL[0], *footL.arc_pts(LU1, LL1, cw=True), legL[1].rev(), *B.arc_pts(LL0, LU0, cw=True)),
            fill(BK, legR[1], *footR.arc_pts(RL1, RU1, cw=True), legR[0].rev(), *B.arc_pts(RU0, RL0, cw=True))]
foot_fill = [fill(BK, *footL_ring, cut=[d_fill(*e.ring()) for e in padsL]), fill(BK, *footR_ring, cut=[d_fill(*e.ring()) for e in padsR])]
steps += [
    step('Colour black', 'Colour the ears, eye patches, nose, arms, legs and feet black. Leave the eyes white.',
         ear_fill + patch_fill + [fill(BK, *nose.ring(90))] + arm_fill + leg_fill + foot_fill, use='black'),
    step('Colour pink', 'Colour the paw pads and toes pink.', [fill(PK, *e.ring()) for e in padsL + padsR], use='pink'),
    step('Colour green', 'Colour the bamboo and the leaves green.', [fill(GR, *stalkL), fill(GR, *stalkR), fill(GR, *leafL), fill(GR, *leafR)], use='green'),
]
P_ = drawing('dx_panda_8', '8 is for Panda', 3, 15, 'animals', ['Numbers', 'Animals'],
             'A chubby panda sitting with its feet out to the sides, in front of some bamboo. The 8 is hiding in it: '
             'it is the panda’s round head and its bigger round body, one on top of the other.',
             steps, ['black', 'pink', 'green'])
save('num8panda', P_, {'set': 'animals-09', 'slot': '8', 'kind': 'hop', 'age_from': 5})
here = os.path.dirname(os.path.abspath(__file__))
json.dump([d_fill(*eyeL.ring()), d_fill(*eyeR.ring())], open(os.path.join(here, 'out', 'num8panda.white.json'), 'w'))
