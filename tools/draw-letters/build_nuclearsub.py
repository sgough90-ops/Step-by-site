"""N is for Nuclear submarine (dx_nuclearsub_n), Vehicles A to Z, slot N (22 Nov 2026).
From his pick "N1 Under the tail" (Claude's sketches, claude/step-by-draw-vehicles-capitals-6x4-sketches.md).

A yellow and grey submarine, nose to the right. The N is under its tail: the front edge of the bottom fin, the slope
under the tail, and the back edge of the yellow tummy. Written in the sketch's numbers; the Pic moves it onto the paper.

    python3 build_nuclearsub.py
"""
import math
from vkit import *

X1, X2, T, B = 16, 34, 48, 70                       # the N: left line, right line, top, bottom
p = Pic(s=1.0, dx=0.4, dy=11.7)

# ---- behind the body: propeller, fins, periscope, tower ----
for nm, cy in (('blade_a', 40.3), ('blade_b', 49.7)):
    p.shape(nm, ell(4.8, cy, 1.7, 4.0), step=5)
p.shape('hub', ell(5.2, 45, 1.7), step=5)
p.shape('fin_top', poly((14.6, 43), (14.6, 27), (9.6, 27), (8.2, 43), closed=True), step=5)
p.stroke('fin_bot', poly((X1, B), (10.4, B), (8.0, 47)), step=2)
p.shape('scope', poly((59.2, 20), (59.2, 6.6), (66, 6.6), (66, 9.6), (62, 9.6), (62, 20), closed=True), step=6)
p.shape('tower', one("M52,36 L52,22 Q52,18 56,18 L66,18 Q68.8,18 69.5,21 L72.6,36 Z"), step=6)
for nm, wx in (('win_a', 57.6), ('win_b', 64.0)):
    p.shape(nm, ell(wx, 26.2, 2.0), step=7)

# ---- the body: one long line from the top left of the N, round the tail, the top and the nose, to the bottom right of the N ----
hull = one(f"M{X1},{T} L7.6,{T} Q5.4,45 7.6,42 L14,42 C22,41 27,34 36,34 L76,34 C89,34 96,43 96,52 C96,61 89,70 76,70 L{X2},{B}")
p.region('hullR', hull, Seg((X2, B), (X1, T)))
p.stroke('hull', hull, step=3)
p.stroke('N', poly((X1, B), (X1, T), (X2, B), (X2, T)), step=1)
p.stroke('belly', Seg((X2, T), (98, T)), step=4)

# ---- the sign on the tummy ----
CX, CY, R, R1, R2 = 62, 59, 7.2, 2.0, 5.6
p.stroke('sign', ell(CX, CY, R), step=8)
for i, a in enumerate((90, 210, 330)):
    q = lambda r, ang: (CX + r * math.cos(math.radians(ang)), CY + r * math.sin(math.radians(ang)))
    blade = [*arc(CX, CY, R2, R2, a - 30, a + 30), Seg(q(R2, a + 30), q(R1, a + 30)), *arc(CX, CY, R1, R1, a + 30, a - 30), Seg(q(R1, a - 30), q(R2, a - 30))]
    blade[0] = Seg(q(R2, a - 30), *blade[0].p[1:])
    p.shape('wedge%d' % i, blade, step=8)

p.build()
p.net.keep_in('belly', 'hullR')
WED = ['wedge0', 'wedge1', 'wedge2']

steps = [
    step('Start with an N', 'Draw a capital N: a line up, a slanted line down, and a line up. This N is hiding under the tail of the submarine.', p.step(1)),
    step('The bottom fin', "From the bottom of the N's first line, draw a short line to the left. Then draw a long line up, leaning a little to the left.", p.step(2)),
    step('The body', "From the top left of the N, go left, round the end and along the top. Go round the big nose and back along the bottom to the N.", p.step(3)),
    step('The tummy line', "From the top of the N's last line, draw a straight line across to the nose.", p.step(4)),
    step('Top fin and propeller', 'Draw a tall fin on top of the tail. At the very back, draw a small circle with a thin oval above it and one below.', p.step(5)),
    step('Tower and periscope', 'On top, draw a tower with a round front corner. Draw a thin pipe up from it that bends forward at the top.', p.step(6)),
    step('Windows', 'Draw two round windows in the tower.', p.step(7)),
    step('The sign', 'On the tummy, draw a circle. Inside it, draw a dot with three fat wedges round it, like a fan with three blades.',
         p.step(8) + [dot(*p.pt(CX, CY), w=2.2)]),
    step('Colour yellow', 'Colour the tummy and the two fins yellow. Leave the three wedges for the black pencil.',
         [p.face('yellow', (45, 60), holes=WED), p.face('yellow', (11.5, 35)), p.face('yellow', (12.5, 60))], use='yellow'),
    step('Colour grey', 'Colour the top of the body, the tower, the periscope and the propeller grey. Leave the windows.',
         [p.face('grey', (50, 40)), p.face('grey', (60, 31), holes=['win_a', 'win_b']), p.face('grey', (60.6, 12)),
          p.face('grey', (4.8, 38.5)), p.face('grey', (4.8, 51.5)), p.face('grey', (4.4, 45))], use='grey'),
    step('Colour light blue', 'Colour the two round windows light blue.', [p.ring('lblue', 'win_a'), p.ring('lblue', 'win_b')], use='lblue'),
    step('Colour black', 'Colour the three wedges of the sign black.', [p.ring('black', w) for w in WED], use='black'),
]

D = drawing('dx_nuclearsub_n', 'N is for Nuclear submarine', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'A yellow and grey nuclear submarine with a tower, a periscope and a propeller. The capital N is hiding under its tail: '
            'the front of the bottom fin, the slope under the tail and the back edge of the yellow tummy.',
            steps, ['yellow', 'grey', 'lblue', 'black'])
save('nuclearsub', D, {'set': 'vehicles-AZ', 'slot': 'N', 'kind': 'swim', 'age_from': 5})
save_white('nuclearsub', p.white)
if __name__ == '__main__':
    preview(D, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'nuclearsub-look.png'))
