"""K is for King prawn (dx_kingprawn_k), Food and drink A to Z, slot K (23 Nov 2026).
From his pick "K1 Curled up" (Claude's second-go sketches, claude/step-by-draw-food-capitals-vehicles-small-14x4.md).

A big curled prawn. The K is its tail: the flat end of its body (the straight line) and the inside edges of its two
tail fins (the two slanting lines). Written in the sketch's numbers.

    python3 build_kingprawn.py
"""
from bcommon import *

p = Pic(s=1.0, dx=0.6, dy=5.0)
CX, CY, RO, RI = 40, 44, 35, 13                                # the curl: its middle, the outside and the inside of the body
KX, KT, KB, KW = 60, 57, 79, 18                                # the K: its line, top and bottom, how far the fins reach
KM = (KT + KB) / 2
HA = 300                                                       # where the body ends and the head starts (degrees round the curl)


def on(r, a):
    return (CX + r * math.cos(math.radians(a)), CY + r * math.sin(math.radians(a)))


# ---- behind the head: two long feelers ----
p.stroke('feel0', Seg((68, 22), (76, 8), (88, 6), (95, 16)), step=5, deco=True)
p.stroke('feel1', Seg((71, 31), (81, 28), (90, 33), (93, 44)), step=5, deco=True)
# ---- the body: two lines from the K, curling round to the head ----
p.stroke('outer', Seg((KX, KB), (CX, KB)), arc(CX, CY, RO, RO, 90, HA + 6, start=P(CX, KB)), step=3)
p.stroke('inner', Seg((KX, KT), (CX, KT)), arc(CX, CY, RI, RI, 90, HA + 6, start=P(CX, KT)), step=3)
for i, a in enumerate((266, 232, 198, 164, 128)):
    p.stroke('ring%d' % i, Seg(on(RI, a), on(RO, a)), step=6, deco=True)
p.stroke('ring5', Seg((50, KT), (50, KB)), step=6, deco=True)
for i, a in enumerate((246, 212, 178, 144)):
    p.stroke('leg%d' % i, Seg(on(RI, a), on(RI - 5.6, a - 16)), step=5, deco=True)
# ---- the head, in front of the end of the body ----
A, B = on(RO + 1.5, HA), on(RI - 1.5, HA)
NOSE = (74.5, 36.2)
p.shape('head', Seg(B, A), Seg(A, (68.4, 14.8), (73.5, 24.2), NOSE), Seg(NOSE, (66, 38.6), (54, 38), B), step=4)
# ---- the tail fins and the K ----
p.stroke('fin0', Seg((KX + KW, KT), (KX + KW * 0.72, KT - 4.6), (KX + KW * 0.3, KT - 2.2), (KX, KT)), step=2)
p.stroke('fin1', Seg((KX + KW, KB), (KX + KW * 0.72, KB + 4.6), (KX + KW * 0.3, KB + 2.2), (KX, KB)), step=2)
p.stroke('k_stick', Seg((KX, KT), (KX, KB)), step=1)
p.stroke('k_arms', poly((KX + KW, KT), (KX, KM), (KX + KW, KB)), step=1)
p.build()

eye = dot(*p.pt(61.6, 24.2), w=3.2)
steps = [
    step('Start with a K', 'Draw a capital K: a straight line down, then two slanting lines that meet at its middle.', p.step(1)),
    step('The tail', 'From the end of each slanting line, draw a curve back to the end of the straight line. Now the K is a tail with two fins.', p.step(2)),
    step('The body', 'From the top of the K draw a line left, then curl it round in a small circle. From the bottom draw a line left and a big curl round the outside.', p.step(3)),
    step('The head', 'Join the two curls with a line. Then draw a head with a pointed nose, and a dot for the eye.', p.step(4) + [eye]),
    step('Feelers and legs', 'Draw two long curved feelers from the head. Draw four little legs inside the curl.', p.step(5)),
    step('The shell', 'Draw six lines across the body, to make its shell.', p.step(6)),
    step('Colour orange', 'Colour the body and the head orange.', [p.face('orange', (16, 44)), p.ring('orange', 'head')], use='orange'),
    step('Colour red', 'Colour the two fins of the tail red.', [p.face('red', (65, 60.5)), p.face('red', (65, 75.5))], use='red'),
]
D = drawing('dx_kingprawn_k', 'K is for King prawn', 2, 12, 'things', ['Letters', 'Around the house'],
            'A big curled king prawn. The capital K is hiding in its tail: the end of its body and the edges of its two tail fins.',
            steps, ['orange', 'red'])
ok = finish('kingprawn', D, {'set': 'house-AZ', 'slot': 'K', 'kind': 'key', 'age_from': 4}, p)
