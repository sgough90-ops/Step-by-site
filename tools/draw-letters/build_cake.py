"""u is for Upside-down cake (dx_upsidedowncake_u), Food and drink a to z, slot u (23 Nov 2026).
From his pick (18:37): "cake 4" = "With custard" on the u-upside-down-cake sheet
(claude/step-by-draw-redo-u-y-E-X-school-bus-sketches.py, s_cake.py C4).

A slice of cake from the side, a pineapple ring and a cherry on top, and custard poured over it from a jug.
The u is the custard running down the front of the slice: down its left side, round the bottom and up its right
side (no stick, like the live urchin). 26 wide and 31 tall.
One line (the custard's edge) runs from one end of the u, over the top of the cake, to the other end of the u.
Written in the sketch's numbers.

    python3 build_cake.py
"""
from bcommon import *

p = Pic(s=0.96, dx=2.6, dy=2.2)
UX0, UX1, UT, UB, URY = 47, 73, 53, 84, 13
UCY = UB - URY
U = [Seg((UX0, UT), (UX0, UCY))] + arc(60, UCY, 13, URY, 180, 0, start=P(UX0, UCY), end=P(UX1, UCY)) + [Seg((UX1, UCY), (UX1, UT))]
# the custard's edge, from the left end of the u, up over the cake, down over the right corner, to the right end of the u
CUST = smooth([(UX0, UT), (44.9, 50.6), (44.6, 46), (47, 40.6), (54, 37.4), (64, 36.8), (72, 38), (79, 39.4), (82.4, 43.6),
               (82.6, 48.6), (80.8, 52.8), (77.4, 55.4), (UX1, UT)])
J = lambda x, y: (84 + 0.669 * x + 0.743 * y, 13 - 0.743 * x + 0.669 * y)       # the jug: tipped over, pouring to the left
JUG = poly(J(-6, -7.6), J(-10.5, -8.2), J(-6.3, -3.4), J(-7.6, 7.6), J(7.6, 7.6), J(6, -7.6), closed=True)
edge = lambda t: (J(6, -7.6)[0] + (J(7.6, 7.6)[0] - J(6, -7.6)[0]) * t, J(6, -7.6)[1] + (J(7.6, 7.6)[1] - J(6, -7.6)[1]) * t)
lip = lambda t: (J(-10.5, -8.2)[0] + (J(-6.3, -3.4)[0] - J(-10.5, -8.2)[0]) * t, J(-10.5, -8.2)[1] + (J(-6.3, -3.4)[1] - J(-10.5, -8.2)[1]) * t)
ST_L = smooth([lip(0.0), (66.6, 23), (63.8, 31), (63.2, 39)])
ST_R = smooth([lip(0.6), (70.4, 24), (68, 31.5), (67.4, 39)])

# ---- behind: the plate ----
p.shape('plate', ell(48, 90.5, 46, 6.5), step=6)

# ---- the slice: its front, its top, the pineapple ring and the cherry ----
p.shape('front', one("M12,46 L80,46 L80,85.5 Q80,88 77.5,88 L14.5,88 Q12,88 12,85.5 Z"), step=3)
p.region('topR', poly((12, 46), (19, 35), (73, 35), (80, 46), closed=True))
p.stroke('top', poly((12, 46), (19, 35), (73, 35), (80, 46)), step=3)
p.shape('ring', ell(31.5, 40.4, 14, 3.9), step=4)
p.stroke('stalk', one("M31.9,31.4 C33,26.9 36.1,24.2 39.6,23"), step=4)
p.shape('cherry', circle(31.5, 36.6, 5.4), step=4)

# ---- the custard falling (in front of the cake's top edge), the jug it falls from (in front of the stream's top),
#      then the custard on the cake (hides what is under it) ----
p.region('streamR', ST_L, Seg(ST_L[-1].b, ST_R[-1].b), rev(ST_R), Seg(ST_R[0].a, ST_L[0].a))
p.stroke('stream_l', ST_L, step=5); p.stroke('stream_r', ST_R, step=5)
p.stroke('handle_o', smooth([edge(0.24), (90.1, 2.4), (95.4, 7.2), edge(0.82)]), step=5)
p.stroke('handle_i', smooth([edge(0.4), (90.3, 5.0), (92.9, 7.4), edge(0.66)]), step=5)
p.shape('jug', JUG, step=5)
p.region('custR', CUST, rev(U))
p.stroke('cust', CUST, step=2)

# ---- the u, in front of everything ----
p.stroke('u', U, step=1)
p.build()

steps = [
    step('Start with a U', 'Draw a capital U: straight down, round the bottom and straight back up.', p.step(1)),
    step('Custard', 'From the top left of the U, go up, over in a long wobbly curve and down again to the top right of the U. This is custard.', p.step(2)),
    step('A slice of cake', 'Draw a big box behind the U for the slice of cake. On top of it draw a thin slanting top, going behind the custard.', p.step(3)),
    step('Pineapple and cherry', 'On the top of the cake draw a long flat oval, a ring of pineapple. Draw a round cherry in the middle of it, with a little stalk.', p.step(4)),
    step('The jug', 'Up above, draw a jug tipping over, with a handle at the back. Draw two lines falling from its spout down to the custard.', p.step(5)),
    step('The plate', 'Draw a long flat plate under the slice of cake.', p.step(6)),
    step('Colour yellow', 'Colour the custard yellow: on the cake, down the U and falling from the jug. Colour the pineapple yellow too.',
         [p.face('yellow', (60, 62)), p.face('yellow', (66.5, 28)), p.face('yellow', (21, 41))], use='yellow'),
    step('Colour light brown', 'Colour the front of the cake light brown, all round the custard.', [p.face('lbrown', (26, 70))], use='lbrown'),
    step('Colour brown', 'Colour the top of the cake brown, round the pineapple and behind the custard.', [p.face('brown', (22, 45.2))], use='brown'),
    step('Colour red', 'Colour the cherry red.', [p.ring('red', 'cherry')], use='red'),
    step('Colour light blue', 'Colour the jug and its handle light blue. Colour the plate light blue too.',
         [p.face('lblue', (84, 13)), p.face('lblue', (91.6, 4.4)), p.face('lblue', (48, 93.4))], use='lblue'),
]
D = drawing('dx_upsidedowncake_u', 'U is for Upside-down cake', 3, 15, 'things', ['Letters', 'Around the house'],
            'A slice of pineapple upside-down cake with custard poured over it. The capital letter U is hiding in it: the custard running down the front.',
            steps, ['yellow', 'lbrown', 'brown', 'red', 'lblue'])
ok = finish('cake', D, {'set': 'house-AZ', 'slot': 'U', 'kind': 'key', 'age_from': 5}, p)
