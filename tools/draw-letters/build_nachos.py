"""N is for Nachos (dx_nachos_n), Food and drink A to Z, slot N (23 Nov 2026).
From his pick "N4 Cinema tray" (Claude's second-go sketches, claude/step-by-draw-food-capitals-vehicles-small-14x4.md).

Nachos in a stripy paper tray with melted cheese and a pot of cheese sauce. The N is the edges of two chips: the left
edge and the slanting edge of the chip in front, and the left edge of the chip beside it.

    python3 build_nachos.py
"""
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=1.0)
X0, X1, TOP, BOT = 27, 57, 12, 52                              # the N
TY = 60                                                        # the top edge of the tray

# ---- at the back: a chip behind the left of the N, and a chip behind the pot ----
p.shape('chipL', poly((6, TY), (19, 22), (33, TY), closed=True), step=6)
p.shape('chipB', poly((73, TY), (84.5, 25), (91, TY), closed=True), step=6)
# ---- the two chips of the N (their other edges are the N itself) ----
p.region('chipFR', poly((X0, TOP), (X1, BOT), (X0, BOT + 6), closed=True))
chipR = one("M57,12 Q69.6,10.6 81,20") + [Seg((81, 20), (X1, BOT))]
p.region('chipRR', chipR, Seg((X1, BOT), (X1, TOP)))
p.stroke('chipR', chipR, step=2)
# ---- melted cheese over the bottoms of the chips ----
CH = smooth([(9, TY), (13, 55), (20, 56), (X0, BOT), (41, 55), (X1, BOT), (61, 56), (66, TY)])
p.region('cheeseR', CH, Seg((66, TY), (9, TY)))
p.stroke('cheese', CH, step=3)
# ---- the pot of cheese sauce, standing in the tray ----
p.region('potR', Seg((68, TY), (66, 46)), arc(80, 46, 14, 3.6, 180, 360, start=P(66, 46), end=P(94, 46)), Seg((94, 46), (92, TY)), Seg((92, TY), (68, TY)))
p.shape('rim', ell(80, 46, 14, 3.6, start=180), step=5)
p.shape('dip', ell(80, 46.3, 11.4, 2.2), step=5)
p.stroke('potL', Seg((66, 46), (68, TY)), step=5)
p.stroke('potR_', Seg((94, 46), (92, TY)), step=5)
# ---- the tray, with four lines for its stripes ----
p.shape('tray', poly((4, TY), (96, TY), (89, 92), (11, 92), closed=True), step=4)
for i, f in enumerate((0.2, 0.4, 0.6, 0.8)):
    p.stroke('str%d' % i, Seg((4 + 92 * f, TY), (11 + 78 * f, 92)), step=4)
# ---- the N ----
p.stroke('n', poly((X0, BOT), (X0, TOP), (X1, BOT), (X1, TOP)), step=1)
p.build()

steps = [
    step('Start with an N', 'Draw a capital N: a line up, a slanting line down, and a line up again.', p.step(1)),
    step('A second chip', 'From the top of the last line, draw a curve out to the right. Then draw a straight line back down to the bottom of the N.', p.step(2)),
    step('Melted cheese', 'Draw a wavy line from left to right. It goes through the two bottom points of the N.', p.step(3)),
    step('The tray', 'Under the cheese draw a long line across. Draw two slanting sides and the bottom. Add four lines down the tray for its stripes.', p.step(4)),
    step('A pot of cheese', 'On the right, draw a flat oval with a smaller oval inside it. Draw two sides down to the tray.', p.step(5)),
    step('More chips', 'Draw the point of a chip behind the left of the N, with its sides coming down. Draw another point behind the pot.', p.step(6)),
    step('Colour yellow', 'Colour the four chips yellow.',
         [p.face('yellow', (33, 40)), p.face('yellow', (64, 24)), p.face('yellow', (15, 44)), p.face('yellow', (84.6, 35))], use='yellow'),
    step('Colour orange', 'Colour the melted cheese orange. Colour the cheese in the pot orange too.', [p.face('orange', (40, 57.6)), p.ring('orange', 'dip')], use='orange'),
    step('Colour red', 'Colour three stripes on the tray red: the two at the ends and the one in the middle.',
         [p.face('red', (13, 76)), p.face('red', (50, 76)), p.face('red', (87, 76))], use='red'),
]
D = drawing('dx_nachos_n', 'N is for Nachos', 2, 12, 'things', ['Letters', 'Around the house'],
            'A tray of nachos with melted cheese. The capital N is hiding in the chips: the edges of the two chips at the front.',
            steps, ['yellow', 'orange', 'red'])
ok = finish('nachos', D, {'set': 'house-AZ', 'slot': 'N', 'kind': 'key', 'age_from': 4}, p)
