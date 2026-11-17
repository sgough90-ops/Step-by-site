"""9 is for Poodle (dx_poodle_9), Animals 1 to 9, slot 9. Built from Claude's sketch "Poodle 3" with the head of
"Poodle 1" (no bow) and no cushion, standing on the ground (picked 17 Nov 2026).
The 9 is the fluffy ball on the end of the poodle's tail (the loop) and its straight tail (the line down)."""
from numkit import *

LB = FILL['lbrown']

# the 9
TB = Ell(66, 24, 8)
S0, S1 = TB.P(0), P(74, 58)
nine = [ring(*TB.ring(0)), line(Seg(S0, S1))]

# head: topknot, muzzle and the round head behind them
TK, HD, MZ = Ell(25, 24, 6.5), Ell(26, 35, 9.5), Ell(16.5, 38, 6.5, 4.25)
tR, tL = meet_ee(TK, HD)                   # topknot meets head: right, left
mU, mL = sorted(meet_ee(MZ, HD), key=lambda p: p[1])   # muzzle meets head: upper, lower
EAR = Ell(33, 41, 4, 8.5)
eR, eL = sorted(meet_ee(EAR, HD), key=lambda p: p[1])  # ear meets head: upper right, lower left
headA = HD.arc_pts(tR, eR, cw=True) + HD.arc_pts(eR, eL, cw=True) + HD.arc_pts(eL, mL, cw=True)
headB = HD.arc_pts(mU, tL, cw=True)

# ear (in front of the chest)
CH = Ell(37, 57, 12.5)
cR, cL = sorted(meet_ee(EAR, CH), key=lambda p: -p[0])   # ear meets chest: right, left
ear_line = EAR.arc_pts(eR, cR, cw=True) + EAR.arc_pts(cR, cL, cw=True) + EAR.arc_pts(cL, eL, cw=True)

# body: a long box with round corners, behind the chest; its top right corner ends at the bottom of the 9
CT = P(37 + math.sqrt(12.5 ** 2 - 6 ** 2), 51)
corner_bl = Ell(44, 61, 7)
CB = [p for p in meet_ee(corner_bl, CH) if p[1] > 60][0]
LG = [P(39, 57 + math.sqrt(12.5 ** 2 - 4)), P(47, 68), P(62, 68), P(70, 61 + math.sqrt(49 - 9))]
top = [Seg(CT, (67, 51))] + Ell(67, 58, 7).arc(-90, 0, start=P(67, 51), end=S1)
rest = ([Seg(S1, (74, 61))] + Ell(67, 61, 7).arc(0, 90, start=P(74, 61), end=P(67, 68)))
rest = chain_split_at(rest, LG[3])
rest = rest[0] + rest[1]
bottom = [Seg(P(67, 68), LG[2]), Seg(LG[2], LG[1]), Seg(LG[1], (44, 68))] + corner_bl.arc_pts(P(44, 68), CB, cw=True)
chest_line = []
cpts = [cR, CT, CB, LG[0], cL]
for a, b in zip(cpts, cpts[1:]):
    chest_line += CH.arc_pts(a, b, cw=True)

# legs, fluffy feet and the ground
GYL = 89.15
feet = [Ell(p[0], 85.7, 3.3) for p in LG]
legs = [Seg(p, P(p[0], 82.4)) for p in LG]
ground = Seg((12, GYL), (86, GYL))

steps = [
    step('Start with a 9', 'Draw a 9: a small circle, then a long straight line down from its right side.', nine),
    step('The head', 'Draw a fluffy ball, an oval nose at the front, and a round head joining them. Add dots for the eye and nose.',
         [ring(*TK.ring(-90)), ring(*MZ.ring(-90)), line(*headA), line(*headB), dot(22.6, 34, 3.0), dot(12.6, 37.4, 3.0)]),
    step('The ear', 'Draw a long floppy ear hanging down from the side of the head.', [line(*ear_line)]),
    step('The chest', 'Draw a big round chest under the head, behind the ear.', [line(*chest_line)]),
    step('The body', 'Draw the body: a long shape with round corners, from the chest to the bottom of the 9.', [line(*top), line(*rest, *bottom)]),
    step('The legs', 'Draw four thin legs with a fluffy ball at the bottom of each, and a line for the ground.',
         [line(l) for l in legs] + [ring(*f.ring(-90)) for f in feet] + [line(ground)]),
]
# colour outlines
head_fill = fill(LB, *headA, *MZ.arc_pts(mL, mU, cw=False), *headB, *TK.arc_pts(tL, tR, cw=False))
ear_fill = fill(LB, *ear_line, *HD.arc_pts(eL, eR, cw=False))
chest_fill = fill(LB, *chest_line, *EAR.arc_pts(cL, cR, cw=False))
body_fill = fill(LB, *top, *rest, *bottom, *CH.arc_pts(CB, CT, cw=False))
steps += [
    step('Colour light brown', 'Colour the poodle light brown: its fluffy balls, head, ear, chest and body.',
         [fill(LB, *TB.ring(0)), fill(LB, *TK.ring(-90)), fill(LB, *MZ.ring(-90)), head_fill, ear_fill, chest_fill, body_fill]
         + [fill(LB, *f.ring(-90)) for f in feet], use='lbrown'),
]
P_ = drawing('dx_poodle_9', '9 is for Poodle', 2, 10, 'animals', ['Numbers', 'Animals'],
             'A fluffy poodle standing tall. The 9 is hiding in it: the fluffy ball on the end of its tail is the loop, '
             'and the straight tail under it is the line down.',
             steps, ['lbrown'])
P_ = move(P_, 8, 0)                               # centre it on the paper
save('num9poodle', P_, {'set': 'animals-09', 'slot': '9', 'kind': 'hop', 'age_from': 5})
