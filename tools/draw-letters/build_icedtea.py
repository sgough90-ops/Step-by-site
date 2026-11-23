"""i is for Iced tea (dx_icedtea_i), Food and drink a to z, slot i (23 Nov 2026).
From his pick "i4" (the cup with a lid and a stripy straw; Claude's sketches,
claude/step-by-draw-food-small-12-ideas-4-versions.md), with his change: no bubble. "Where the dot is for the i,
can't it just be an extended line for the straw? Start with the i, then just draw a mini line in between the two
to connect them, and then do the rest from there."

A paper cup of iced tea with a lid, a label with a slice of lemon on it, and a tall stripy straw. The i is the
left edge of the straw: its line is the lower part of that edge, and its dot is the top corner of the straw.
Step 2 is the short line that joins the dot to the line. Written in the sketch's numbers.

    python3 build_icedtea.py
"""
import qcheck                                    # the quicker crossing test (the same 9 checks)
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=2.5)
X, XR = 46.0, 51.0                               # the straw: its left edge (the i) and its right edge
DOT, ITOP, LID = 0.0, 8.0, 30.0                  # the dot, the top of the i's line, the top of the lid (the i's line ends on it)
SLOPE = 4.4 / 50                                 # how much the cup's sides slope in


def side(y, sg):
    return 50 + sg * (20 - (y - 40) * SLOPE)


# ---- the cup (its top runs on behind the lid and is trimmed), the label and the lemon ----
p.stroke('cup', one("M%.3f,38 L34.4,90 Q34.8,94 38.8,94 L61.2,94 Q65.2,94 65.6,90 L%.3f,38" % (side(38, -1), side(38, 1))), step=6)
for nm, y in (('lab1', 54.0), ('lab2', 78.0)):
    p.stroke(nm, Seg((side(y, -1), y), (side(y, 1), y)), step=7)
p.shape('lemon', circle(50, 66, 7.4), step=7)
p.stroke('lemring', circle(50, 66, 5.2), step=7, deco=True, w=1.2)
for k in range(6):
    a = math.radians(30 + 60 * k)
    p.stroke('spoke%d' % k, Seg((50 + 1.2 * math.cos(a), 66 + 1.2 * math.sin(a)), (50 + 4.1 * math.cos(a), 66 + 4.1 * math.sin(a))), step=7, deco=True, w=1.2)

# ---- the lid: a flat box, and the longer box under it (in front) ----
p.shape('lidtop', rrect(33, LID, 67, 36, 1.6), step=5)
p.shape('rim', rrect(26.5, 34, 73.5, 40.5, 2.2), step=5)

# ---- the straw: the rest of its outline, its stripes, the short line that joins the dot to the i ----
p.stroke('straw', Seg((X, DOT), (XR, DOT)), Seg((XR, DOT), (XR, LID)), step=3)
STRIPES = (27.0, 22.5, 18.0, 13.5, 9.0, 4.5)
for k, y in enumerate(STRIPES):
    p.stroke('s%d' % k, Seg((X, y), (XR, y - 2.4)), step=4)
p.stroke('join', Seg((X, DOT), (X, ITOP)), step=2)

# ---- the i, in front of everything ----
p.stroke('i_stick', Seg((X, ITOP), (X, LID)), step=1)
p.build()
idot = dot(*p.pt(X, DOT), w=3.0)

steps = [
    step('Start with an i', 'Draw a small letter i: a short line down, with a dot above it. The dot does not touch the line.', p.step(1) + [idot]),
    step('Join the dot', 'Draw a short line from the dot down to the top of the i. Now it is one long line: the side of a straw.', p.step(2)),
    step('The straw', 'From the dot, draw a short line across. Then draw a long line down, next to the first one.', p.step(3)),
    step('The stripes', 'Draw six little slanting lines across the straw.', p.step(4)),
    step('The lid', 'Under the straw, draw a flat box. Under that, draw a longer flat box with round corners.', p.step(5)),
    step('The cup', 'From the lid, draw the two sides of the cup, sloping in a little. Join them with a round bottom.', p.step(6)),
    step('The label', 'Draw two lines across the cup. Between them draw a slice of lemon: a circle, a ring inside it, and six little lines like spokes.', p.step(7)),
    step('Colour the stripes', 'Colour every other stripe on the straw purple.',
         [p.face('purple', ((X + XR) / 2, (a + b) / 2 - 1.2)) for a, b in zip(STRIPES[0::2], STRIPES[1::2])], use='purple'),
    step('Colour the label', 'Colour the label orange, like tea, all round the lemon.', [p.face('orange', (38, 66), holes=('lemon',))], use='orange'),
    step('Colour the lemon', 'Colour the slice of lemon yellow.', [p.ring('yellow', 'lemon')], use='yellow'),
    step('Colour the lid', 'Colour the lid grey: both boxes.', [p.face('grey', (40, 32)), p.ring('grey', 'rim')], use='grey'),
]
D = drawing('dx_icedtea_i', 'i is for Iced tea', 2, 12, 'things', ['Letters', 'Around the house'],
            'A cup of iced tea with a lid and a stripy straw. The small letter i is hiding in it: it is the side of the straw, and its dot is the top corner.',
            steps, ['purple', 'orange', 'yellow', 'grey'])
ok = finish('icedtea', D, {'set': 'house-az', 'slot': 'i', 'kind': 'key', 'age_from': 4}, p)
