"""t is for Teapot (dx_teapot_t), Food and drink a to z, slot t (23 Nov 2026).
From his pick "t3 A glass teapot" (Claude's sketches, claude/step-by-draw-food-small-12-ideas-4-versions.md):
"Create the steps for teapot number three".

A round glass teapot, spout on the left, with the tea and a tea bag showing inside. The t is the string of the
tea bag (its tall line, curling to the bag at the bottom) and the edge of the lid (its bar). The string comes out
from under the little ball on the lid. Written in the sketch's numbers.

    python3 build_teapot.py
"""
import qcheck                                    # the quicker crossing test (the same 9 checks)
from bcommon import *

p = Pic(s=1.0, dx=1.5, dy=-3.0)
BX, BY, RX, RY, RIM = 50, 62, 30, 26, 38.5       # the pot: middle, half-width, half-height; the edge of the lid
HX = RX * math.sqrt(1 - ((RIM - BY) / RY) ** 2)  # half the width of the lid (half the bar of the t)
KY, KR = 23.4, 4.6                               # the ball on the lid
TOP = KY + KR                                    # the top of the t
LEV = 45.0                                       # the top of the tea
LX = RX * math.sqrt(1 - ((LEV - BY) / RY) ** 2)
BAG = [(59.89, 64.79), (70.78, 66.32), (69.11, 78.21), (58.22, 76.68)]   # the tea bag, from the corner the string ends on
A0 = math.degrees(math.atan2((RIM - BY) / RY, -HX / RX)) % 360            # where the pot's outline starts (top left)

# ---- behind the pot: the handle and the spout (their ends run on behind it and are trimmed) ----
# (the curves' guide points stay on the paper too: the app's own checker reads every number in a line)
p.stroke('hout', one("M72,46.5 C97.6,41 98.6,82 70,80"), step=5)
p.stroke('hin', one("M72,51.5 C90.5,48.5 91.5,74.5 70,75"), step=5)
p.stroke('spout', one("M24,60 C15,58 12,49 8,41 L2.6,44 C6,56 11,68 24,72"), step=5)

# ---- the pot: its outline runs from one end of the lid's edge round to the other ----
body = arc(BX, BY, RX, RY, A0, A0 - (2 * A0 - 180), start=P(BX - HX, RIM), end=P(BX + HX, RIM))
p.region('bodyR', body, Seg((BX + HX, RIM), (BX - HX, RIM)))
p.stroke('body', body, step=4)

# ---- the lid and its ball ----
p.stroke('lidL', Seg((BX - HX, RIM), (BX - HX + 2, 30), (BX - 6, 27.6), (BX, 27.6)), step=3)
p.stroke('lidR', Seg((BX, 27.6), (BX + 6, 27.6), (BX + HX - 2, 30), (BX + HX, RIM)), step=3)
p.shape('knob', circle(BX, KY, KR), step=3)

# ---- inside: the top of the tea (a line each side of the string), the tea bag; outside: the steam ----
p.stroke('levL', Seg((BX - LX, LEV), (BX, LEV)), step=6)
p.stroke('levR', Seg((BX, LEV), (BX + LX, LEV)), step=6)
p.shape('bag', poly(*BAG, closed=True), step=2)
for i, (x, y1) in enumerate(((3, 38), (9, 35))):
    p.stroke('steam%d' % i, smooth([(x, y1), (x - 1.8, y1 - 3.5), (x + 1.8, y1 - 7), (x - 1.8, y1 - 10.5), (x, y1 - 14)]), step=6, deco=True)

# ---- the t, in front of everything: the string, then the bar ----
p.stroke('tstick', Seg((BX, TOP), (BX, 60)), Seg((BX, 60), (BX, 63.6), (53.2, 65.4), BAG[0]), step=1)
p.stroke('tbar', Seg((BX - HX, RIM), (BX + HX, RIM)), step=1)
p.build()

steps = [
    step('Start with a t', 'Draw a small letter t: a tall line that curls round to the right at the bottom, and a long bar across it, near the top.', p.step(1)),
    step('The tea bag', 'The t is the string of a tea bag. Draw a little square on the end of its curl.', p.step(2)),
    step('The lid', 'Draw a little ball on top of the t. Then draw a curved line from each end of the bar up to the ball. That is the lid.', p.step(3)),
    step('The pot', 'From one end of the bar, draw a big round pot, all the way round to the other end.', p.step(4)),
    step('Spout and handle', 'On the left draw a spout that points up. On the right draw a handle like an ear: a big curve with a smaller curve inside it.', p.step(5)),
    step('The tea', 'Draw a line across the pot on each side of the string. That is the top of the tea. Add two wiggly lines of steam by the spout.', p.step(6)),
    step('Colour the tea', 'Colour the tea orange, under the line and all round the tea bag.', [p.face('orange', (38, 72))], use='orange'),
    step('Colour brown', 'Colour the tea bag and the little ball on the lid brown.', [p.ring('brown', 'bag'), p.ring('brown', 'knob')], use='brown'),
    step('Colour the glass', 'Colour the lid, the spout, the handle and the top of the pot light blue.',
         [p.face('lblue', (44, 34)), p.face('lblue', (56, 34)), p.face('lblue', (40, 42)), p.face('lblue', (60, 42)),
          p.face('lblue', (11, 52)), p.face('lblue', (88.6, 62))], use='lblue'),
]
D = drawing('dx_teapot_t', 't is for Teapot', 2, 12, 'things', ['Letters', 'Around the house'],
            'A glass teapot full of tea, with a tea bag inside. The small letter t is hiding in it: the string of the tea bag and the edge of the lid.',
            steps, ['orange', 'brown', 'lblue'])
ok = finish('teapot', D, {'set': 'house-az', 'slot': 't', 'kind': 'key', 'age_from': 4}, p)
