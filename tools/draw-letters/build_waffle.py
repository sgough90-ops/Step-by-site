"""w is for Waffle (dx_waffle_w), Food and drink a to z, slot w (23 Nov 2026).
From his pick, fourth go number 2 "Bigger holes" (Claude's sketches, claude/step-by-draw-nut-build-waffle-round4-23nov.py),
with his change (18:34): "I want the middle line drawn all the way up to the top".
His plan for the w (17:32): "make the W part of the outline and then make a thick line in the middle".

A waffle with twelve square holes full of chocolate, four across and three down.
The w is the waffle's outside edge (down the left side, round the corner, along the bottom, round the corner, up the right
side) and the line up the middle, between the two middle rows of holes.
  Step 1 draws a normal w: its three lines all stop at the same height (86 wide, 57 tall). Step 2 carries the middle line on
  up to the top edge, as he asked, and joins the two ends of the w across the top with round corners.
  The holes have thinner lines (1.2), so the outside edge and the middle line are the thick ones.
The middle line cuts the waffle in two, so its colour is two pieces, one each side.

    python3 build_waffle.py            (python3 build_waffle.py yellow makes out/waffle-yellow.json: a yellow waffle, not in the app)
"""
import sys
from bcommon import *

WAF = sys.argv[1] if len(sys.argv) > 1 else 'lbrown'
p = Pic(s=1.0, dx=0.0, dy=0.0)
X0, X1, Y0, Y1, R, CX = 7, 93, 17, 83, 9, 50                   # the waffle's edges, its round corners, the middle line
CELL, EDGE, GAP, HR = 20, 3, 3, 1.4                            # one square of the waffle; the border; half the bar between two holes; a hole's round corner
YW = Y0 + R                                                    # where the three lines of the w stop

W_U = ([Seg((X0, YW), (X0, Y1 - R))] + arc(X0 + R, Y1 - R, R, R, 180, 90, start=P(X0, Y1 - R), end=P(X0 + R, Y1)) +
       [Seg((X0 + R, Y1), (X1 - R, Y1))] + arc(X1 - R, Y1 - R, R, R, 90, 0, start=P(X1 - R, Y1), end=P(X1, Y1 - R)) + [Seg((X1, Y1 - R), (X1, YW))])
W_MID = Seg((CX, Y1), (CX, YW))
TOP = (arc(X1 - R, YW, R, R, 0, -90, start=P(X1, YW), end=P(X1 - R, Y0)) + [Seg((X1 - R, Y0), (X0 + R, Y0))] +
       arc(X0 + R, YW, R, R, 270, 180, start=P(X0 + R, Y0), end=P(X0, YW)))

HOLES = {}
for i in range(4):
    for j in range(3):
        hx, hy = X0 + EDGE + i * CELL, Y0 + EDGE + j * CELL
        HOLES['hole%d%d' % (i, j)] = (i, rrect(hx + GAP, hy + GAP, hx + CELL - GAP, hy + CELL - GAP, HR))
LEFT = [k for k, (i, _) in HOLES.items() if i < 2]
RIGHT = [k for k, (i, _) in HOLES.items() if i >= 2]

p.stroke('top', TOP, step=2)
p.stroke('mid_up', Seg((CX, YW), (CX, Y0)), step=2)
for k, (i, segs) in HOLES.items():
    p.shape(k, segs, step=3 if i < 2 else 4, w=1.2)
p.stroke('w_u', W_U, step=1)
p.stroke('w_mid', W_MID, step=1)
p.build()

NAME = {'lbrown': 'light brown', 'yellow': 'yellow', 'orange': 'orange'}[WAF]
steps = [
    step('Start with a w', 'Draw a small letter w with a flat bottom: down, round the corner, along, round the corner and up. Then draw a line up the middle from the bottom.', p.step(1)),
    step('The top', 'Carry the middle line on up a little. Then join the two ends of the w with a line across the top, with a round corner at each end.', p.step(2)),
    step('Six holes', 'On the left of the middle line draw six small squares: two across and three down.', p.step(3)),
    step('Six more holes', 'Draw six small squares on the right of the middle line too, to match.', p.step(4)),
    step('Colour brown', 'Colour all twelve squares brown. They are full of chocolate.', [p.ring('brown', k) for k in LEFT + RIGHT], use='brown'),
    step('Colour ' + NAME, 'Colour the rest of the waffle %s, all round the squares.' % NAME,
         [p.face(WAF, (X0 + EDGE, 50), holes=LEFT), p.face(WAF, (X1 - EDGE, 50), holes=RIGHT)], use=WAF),
]
D = drawing('dx_waffle_w', 'w is for Waffle', 2, 10, 'things', ['Letters', 'Around the house'],
            'A waffle with chocolate in its holes. The small letter w is hiding in it: the two sides, the bottom edge and the line up the middle.',
            steps, ['brown', WAF])
ok = finish('waffle' if WAF == 'lbrown' else 'waffle-' + WAF, D, {'set': 'house-az', 'slot': 'w', 'kind': 'key', 'age_from': 4}, p)
