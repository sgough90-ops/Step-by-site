"""v is for vulture (dx_vulture_v), Animals a to z, slot v. From Claude's sketch 'Vulture (landing)' on the private page
'Step by Draw Animals from online ideas' (21 Nov 2026), idea from Art for Kids Hub's letter-V vulture.
The v: the inside edges of its two raised wings, meeting on its back."""
from kit15 import *


def on(cx, cy, rx, ry, a):
    return P(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))


def arc_to(cx, cy, rx, ry, p0, p1, clockwise=True):
    a0 = math.degrees(math.atan2((p0[1] - cy) / ry, (p0[0] - cx) / rx)) % 360
    a1 = math.degrees(math.atan2((p1[1] - cy) / ry, (p1[0] - cx) / rx)) % 360
    if clockwise:
        while a1 <= a0 + 1e-9: a1 += 360
    else:
        while a1 >= a0 - 1e-9: a1 -= 360
    return arc(cx, cy, rx, ry, a0, a1, start=P(*p0), end=P(*p1))


def q2c(p0, q, p2):
    return Seg(p0, (p0[0] + 2 / 3 * (q[0] - p0[0]), p0[1] + 2 / 3 * (q[1] - p0[1])),
               (p2[0] + 2 / 3 * (q[0] - p2[0]), p2[1] + 2 / 3 * (q[1] - p2[1])), p2)


BROWN, BLACK, PINK, GREY = FILL['brown'], FILL['black'], FILL['pink'], FILL['grey']

# ---- the v ----
L_, V_, R_ = P(30, 10), P(50, 50), P(70, 9)
vee = [Seg(L_, V_), Seg(V_, R_)]

# ---- the fluffy collar: a ring of bumps, clockwise from its left side ----
RP = [P(*q) for q in [(59, 61), (62, 57), (67, 56), (71, 59), (71.5, 64), (68, 67.5), (63, 68), (59.5, 65)]]
ruff = [bump(a, b, 0.34) for a, b in zip(RP, RP[1:] + RP[:1])]      # piece i goes from RP[i] to RP[i+1]

# ---- the left wing: bumpy long feathers from the top of the v down to the tummy ----
LW = [L_, (25, 11), (21, 15.5), (18, 22), (16.5, 29.5), (17, 37.5), (20, 45.5), (25, 52), (31, 57)]
lwing = [bump(P(*a), P(*b), -0.32) for a, b in zip(LW, LW[1:])]

# ---- the tummy: from the bottom of the left wing round to the bottom of the collar (RP[6]) ----
body1 = Seg((31, 57), (32, 66), (38, 73), (47, 74))
body2 = Seg((47, 74), (55, 75), (60, 72.5), RP[6])

# ---- the right wing: from the top right of the collar (RP[3]) up to the top of the v ----
RW = [RP[3], (75, 53), (80, 46), (83, 38), (83.5, 29.5), (81.5, 22), (77, 15), R_]
rwing = [Seg(RP[3], (73.2, 57.8), (74.4, 55.4), P(75, 53))] + [bump(P(*a), P(*b), -0.32) for a, b in zip(RW[1:], RW[2:])]

# ---- long feathers ----
feathers = [q2c(P(25, 11), (27, 21), (31, 27)), q2c(P(21, 15.5), (24, 26), (28, 33)), q2c(P(18, 22), (22, 32), (26, 39)),
            q2c(P(77, 15), (74, 24), (70, 29)), q2c(P(81.5, 22), (78, 31), (73, 36)), q2c(P(83.5, 29.5), (80, 38), (75, 43)),
            q2c((33, 26), (37, 38), (44, 45)), q2c((69, 26), (66, 38), (59, 47))]

# ---- neck and head ----
HC, HR = (81, 74), 4.5
E_, F_ = on(HC[0], HC[1], HR, HR, 210), on(HC[0], HC[1], HR, HR, 150)
neck_top = Seg(RP[4], (74, 65.5), (76, 68.5), E_)
neck_bot = Seg(RP[5], (71.5, 71), (74.5, 75.5), F_)
head = circle(HC[0], HC[1], HR, start_deg=210)
EYE = (82.4, 72.4)

# ---- hooked beak ----
bb1, bb2 = on(HC[0], HC[1], HR, HR, -28), on(HC[0], HC[1], HR, HR, 22)
BT = P(91.2, 78)
beak = [Seg(bb1, (88.6, 70.4), (91.6, 73.4), BT), Seg(BT, (89.6, 76.6), (87.6, 75.8), bb2)]
hook = Seg((88.2, 75.2), (89.6, 75.4), (90.6, 76.4), (91, 77.4))

# ---- tail: two edges from the tummy, a pointed end between them ----
tA, tB = 0.36, 0.74
b1a, b1b, b1c = split_many(body1, [tA, tB])
T1, T2 = b1a.b, b1b.b
tail = poly(T1, (22, 78), (27, 83), (32, 81), (33, 86), T2)

# ---- legs and toes, ready to land ----
b2a, b2b = body2.split(0.3)
G1, G2 = P(47, 74), b2a.b
F1, F2 = P(46, 84), P(54.5, 85)
legs = [Seg(G1, F1), Seg(G2, F2)]
toes = [Seg(F1, (42.5, 88)), Seg(F1, (46.5, 89)), Seg(F1, (50, 88)), Seg(F2, (51, 89)), Seg(F2, (55, 90)), Seg(F2, (58.5, 88.5))]

# ---- the rock ----
rock = rrect(33, 91, 85, 97, 3)
cracks = [Seg((42, 93.6), (46.5, 92.8)), Seg((70, 95.2), (75, 93.8))]

steps = [
    step('Start with a v', 'Draw a big letter v: two long straight lines that meet in a sharp point at the bottom.', [line(*vee)]),
    step('The left wing', 'From the top of the v on the left, draw a bumpy line down the outside. Add three feather lines and one long line inside.',
         [line(*lwing)] + [line(f) for f in feathers[0:3]] + [line(feathers[6])]),
    step('The tummy', 'From the bottom of the wing, draw a round tummy under the v, curving up a little on the right.', [line(body1, body2)]),
    step('The fluffy collar', 'Draw a fluffy collar at the end of the tummy: a bumpy ring.', [ring(*ruff)]),
    step('The right wing', 'From the top of the collar, draw a bumpy line up to the top of the v. Add the feather lines.',
         [line(*rwing)] + [line(f) for f in feathers[3:6]] + [line(feathers[7])]),
    step('Neck and head', 'Draw a long neck curving down from the collar, with a round head at the end and a dot for the eye.',
         [line(neck_top), line(neck_bot), ring(*head), dot(*EYE, w=2.6)]),
    step('The hooked beak', 'Draw a hooked beak on the front of the head.', [line(*beak), line(hook)]),
    step('The tail', 'Draw a pointed tail under the tummy on the left.', [line(*tail)]),
    step('Legs and toes', 'Draw two legs down from the tummy, each with three toes, ready to land.', [line(l) for l in legs] + [line(t) for t in toes]),
    step('The rock', 'Draw a long rock under the toes, with two little cracks.', [ring(*rock)] + [line(c) for c in cracks]),
]
# brown: left wing, tummy, collar's left side (RP6 -> RP7 -> RP0 -> RP1 -> RP2 -> RP3), right wing, then back down the v
wings_fill = fill(BROWN, *(lwing + [body1, body2] + ruff[6:8] + ruff[0:3] + rwing + rev(vee)))
tail_fill = fill(BLACK, *(tail + [b1b.rev()]))
neck_fill = fill(PINK, *([neck_top] + arc_to(HC[0], HC[1], HR, HR, E_, F_, clockwise=False) + [neck_bot.rev(), ruff[4].rev()]))
head_fill = fill(PINK, *head)
beak_fill = fill(GREY, *(beak + arc_to(HC[0], HC[1], HR, HR, bb2, bb1, clockwise=False)))
rock_fill = fill(GREY, *rock)
steps += [
    step('Colour brown', 'Colour the wings and the tummy brown. Leave the fluffy collar white.', [wings_fill], use='brown'),
    step('Colour black', 'Colour the tail black.', [tail_fill], use='black'),
    step('Colour pink', 'Colour the bare neck and head pink.', [neck_fill, head_fill], use='pink'),
    step('Colour grey', 'Colour the hooked beak and the rock grey.', [beak_fill, rock_fill], use='grey'),
]
Pd = drawing('dx_vulture_v', 'v is for vulture', 3, 15, 'animals', ['Letters', 'Animals'],
             'A vulture coming in to land on a rock, with its big brown wings held up. The small letter v is hiding in it: '
             'the inside edges of its two wings make the v.',
             steps, ['brown', 'black', 'pink', 'grey'])
save('vulture', Pd, {'set': 'animals-az', 'slot': 'v', 'kind': 'fly', 'age_from': 5})
