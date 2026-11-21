"""b is for bird (dx_bird_b), Animals a to z, slot b. From Claude's sketch 'Bird (flying)' on the private page
'Step by Draw Animals from online ideas' (21 Nov 2026), idea from ART'S ROOM's small-b bird.
The b: the stick is the front edge of the raised wing, carrying on down the back of the head; the round part is the head."""
from kit15 import *


def on(cx, cy, rx, ry, a):
    """The point at angle a (degrees; 0 = right, 90 = down) on a circle or oval."""
    return P(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))


def arc_to(cx, cy, rx, ry, p0, p1, clockwise=True):
    """The arc of an oval from p0 to p1 (both on it), clockwise on screen or the other way."""
    a0 = math.degrees(math.atan2((p0[1] - cy) / ry, (p0[0] - cx) / rx)) % 360
    a1 = math.degrees(math.atan2((p1[1] - cy) / ry, (p1[0] - cx) / rx)) % 360
    if clockwise:
        while a1 <= a0 + 1e-9: a1 += 360
    else:
        while a1 >= a0 - 1e-9: a1 -= 360
    return arc(cx, cy, rx, ry, a0, a1, start=P(*p0), end=P(*p1))

ORANGE, YELLOW = FILL['orange'], FILL['yellow']

# ---- the b ----
X, TOP, YJ, YB, RX = 46, 19, 48, 73, 17
RY = (YB - YJ) / 2; CY = YJ + RY
stem = Seg((X, TOP), (X, YB))
bowl = arc(X, CY, RX, RY, -90, 90, start=P(X, YJ), end=P(X, YB))

# ---- the wing: bumpy feathers from the top of the stick round to the left ----
WP = [(X, TOP), (40, 18), (34.5, 21), (30, 26), (26, 32), (23, 39.5), (21, 47.5), (20.5, 55.5), (22, 63)]
wing = [bump(P(*a), P(*b), -0.3 if i == 0 else (-0.15 if i == len(WP) - 2 else -0.46)) for i, (a, b) in enumerate(zip(WP, WP[1:]))]
WE = wing[-1].b

# ---- tail, tummy and the bottom of the wing ----
tail = poly(WE, (13, 62), (5, 64.5), (12, 67.5), (5.5, 72.5), (17, 74), (20, 75))
J = P(39, 77.5)
tum1 = Seg((20, 75), (26, 78), (33, 79), J)
tum2 = Seg(J, (42, 76.5), (44.5, 75), (X, YB))
wingbot = Seg(WE, (28, 69), (34, 74), J)

# ---- long feathers inside the wing (from the sketch's three curves) ----
def q2c(p0, q, p2):
    return Seg(p0, (p0[0] + 2 / 3 * (q[0] - p0[0]), p0[1] + 2 / 3 * (q[1] - p0[1])),
               (p2[0] + 2 / 3 * (q[0] - p2[0]), p2[1] + 2 / 3 * (q[1] - p2[1])), p2)
fe1 = q2c((38, 26), (33, 37), (31.5, 49))
fe2 = q2c((42.5, 31), (38.5, 43), (37.5, 56))
fe3 = q2c((30, 33), (26.5, 42), (27, 52))

# ---- beak and eye ----
b1, b2 = on(X, CY, RX, RY, -16), on(X, CY, RX, RY, 12)
TIP = P(72.5, 59.5)
beak = [Seg(b1, TIP), Seg(TIP, b2)]
EYE = (54.2, 57.2)

steps = [
    step('Start with a b', 'Draw a small letter b: a tall straight stick, with a round shape at the bottom on the right.',
         [line(stem), line(*bowl)]),
    step('The big wing', 'From the top of the stick, draw a bumpy line round to the left and down. These are the wing feathers.',
         [line(*wing)]),
    step('The tail', 'From the bottom of the feathers, draw a pointed tail that zigzags out to the left and back.',
         [line(*tail)]),
    step('The tummy', 'From the end of the tail, draw a curved tummy under the wing, back to the bottom of the b.',
         [line(tum1, tum2)]),
    step('Bottom of the wing', 'Draw a curved line from the bottom of the feathers down to the tummy.',
         [line(wingbot)]),
    step('Long feathers', 'Draw three long curved lines inside the wing.',
         [line(fe1), line(fe2), line(fe3)]),
    step('Beak and eye', 'Draw a pointed beak on the round head, and a dot for the eye.',
         [line(*beak), dot(*EYE, w=3.6)]),
]
wing_fill = fill(ORANGE, *(wing + [wingbot, tum2, Seg((X, YB), (X, TOP))]))
beak_fill = fill(ORANGE, *(beak + arc_to(X, CY, RX, RY, b2, b1, clockwise=False)))
head_fill = fill(YELLOW, *(bowl + [Seg((X, YB), (X, YJ))]))
tail_fill = fill(YELLOW, *(tail + [tum1, wingbot.rev()]))
steps += [
    step('Colour orange', 'Colour the big wing and the beak orange.', [wing_fill, beak_fill], use='orange'),
    step('Colour yellow', 'Colour the head, the tail and the tummy yellow.', [head_fill, tail_fill], use='yellow'),
]
Pd = drawing('dx_bird_b', 'b is for bird', 2, 10, 'animals', ['Letters', 'Animals'],
             'A little bird flying with its wings up. The small letter b is hiding in it: '
             'the front edge of its wing is the stick and its round head is the round part.',
             steps, ['orange', 'yellow'])
move(Pd, 10, 3)
save('bird', Pd, {'set': 'animals-az', 'slot': 'b', 'kind': 'fly', 'age_from': 4})
