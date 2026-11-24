"""Z is for Zander (dx_zander_z), Food and drink A to Z, slot Z (24 Nov 2026).
From his pick, "a whole fish" number 4 "With tomatoes" (Claude's sketches, claude/step-by-draw-zander-whole-fish-sketches.py).
His words: "Create me four variations of a meal containing zander fish", then "4 more like 1" (the whole fish), then
"Do steps for number 4".

A whole grilled zander (a fish) on a long dish, head on the right, cut in two on the slant, with three little tomatoes,
two slices of lemon and two bits of parsley. The Z is three real edges of the fish: its back, the cut and its belly
(30 wide, 32 tall). The head is drawn from the Z's top right corner round to its end; the tail part from its start round to
its bottom left corner. The cut splits the fish in two, so its colour is two pieces, one each side.
Different from the sketch: the dish starts lower and is a little taller, so nothing is under the step number; the fish is a
little shorter (79 long, not 83) so it sits clear inside the dish; the lemon slices sit inside the dish, not on its rim
(a line hidden for a tiny way behind a slice is a fiddly thing to draw); each tomato's green star is a drawn star.
The eye and the middle of the dish stay white (holes meant to stay white: out/zander.white.json), so the app's own checker
lists them as gaps, as it does for the sushi and the fried eggs.

    python3 build_zander.py            (python3 build_zander.py brown makes out/zander-brown.json: a brown tail fin, not in the app)
"""
import sys
from bcommon import *

TAILC = next((a for a in sys.argv[1:] if a in ('orange', 'brown')), 'orange')
p = Pic(s=1.0, dx=0.0, dy=0.0)
T, B = 38, 70                                                  # the fish's back and its belly: the top and bottom lines of the Z
ZA, ZC = 34, 64                                                # the Z's left and right
MID = (T + B) / 2
XF, XS = 70.5, 89.5                                            # where the head starts, the tip of the nose
XB, XP, XT = 30.5, 21.5, 11                                    # where the body starts to narrow, the narrow part, the tips of the tail fin
PH = 11.6                                                      # how far the body narrows at the tail, top and bottom
DISH, WELL = (2.5, 16.5, 97.5, 91, 15), (8, 22, 92, 85.5, 9.5)  # the long dish, and the line inside its rim
TOMS, TR, SR = ((19.5, 30.4), (31, 29.6), (42.5, 30.4)), 4.6, 2.5   # three little tomatoes; a tomato's size; its star's size
LEMS, LR = ((69, 78), (80, 77.2)), 4.4                         # two slices of lemon
PARS = ((80, 30.6), (27, 78.4))                                # two bits of parsley

Z = poly((ZA, T), (ZC, T), (ZA, B), (ZC, B))
NOSE = P(XS, MID + 2)
HEAD = [Seg((ZC, T), (XF, T)), Seg((XF, T), (XF + 9.5, T), (XS - 1.9, T + 9), NOSE),
        Seg(NOSE, (XS - 2.85, B - 8), (XF + 8.55, B), (XF, B)), Seg((XF, B), (ZC, B))]
TAIL = [Seg((ZA, T), (XB, T)), Seg((XB, T), (XB - 4.6, T + 0.6), (XP + 2.4, T + 7), (XP, T + PH)), Seg((XP, T + PH), (XP, B - PH)),
        Seg((XP, B - PH), (XP + 2.4, B - 7), (XB - 4.6, B - 0.6), (XB, B)), Seg((XB, B), (ZA, B))]
FIN = poly((XP, T + PH), (XT, T + 1), (XT + 4.6, MID), (XT, B - 1), (XP, B - PH))
EYE = (XS - 8.4, MID - 3.6)
GILL = Seg((XF + 0.6, T + 3), (XF - 3.4, T + 11), (XF - 3.4, B - 11), (XF + 0.6, B - 3))
M0 = P(*HEAD[2].at(seg_y(HEAD[2], MID + 3.6)))                 # the mouth starts on the edge of the head, just under the nose
MOUTH = Seg(M0, (XS - 5.4, MID + 5.4))
MARKS = [Seg((x - 1.5, T + 9.4), (x + 1.5, B - 9.4)) for x in (XP + 9.4, XP + 5.6)]   # two marks from the grill, just before the tail


def sprig(cx, cy, rx=4.3, ry=3.7, k=7, amp=0.26, phase=20):
    """a bit of parsley: a round shape with a wavy edge (k bumps)"""
    pts = []
    for i in range(2 * k):
        a = math.radians(phase) + i * math.pi / k
        r = 1.0 if i % 2 == 0 else 1.0 - amp
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return smooth(pts, closed=True)


# ---- the dish, and the food round the fish (nothing sits on top of anything else) ----
p.shape('dish', rrect(*DISH), step=5)
p.shape('well', rrect(*WELL), step=5)
for i, (x, y) in enumerate(TOMS):
    p.shape('tom%d' % i, circle(x, y, TR), step=6)
    p.shape('star%d' % i, star5(x, y, SR), step=6, w=1.2)
for i, (x, y) in enumerate(PARS):
    p.shape('pars%d' % i, sprig(x, y), step=6)
for i, (x, y) in enumerate(LEMS):
    p.shape('lem%d' % i, circle(x, y, LR), step=7)
    for k in range(6):
        a = math.radians(30 + 60 * k)
        p.stroke('sp%d%d' % (i, k), Seg((x + 1.0 * math.cos(a), y + 1.0 * math.sin(a)), (x + 2.9 * math.cos(a), y + 2.9 * math.sin(a))), step=7, deco=True, w=1.2)

# ---- the fish ----
p.stroke('fin', FIN, step=3)
p.stroke('tail', TAIL, step=3)
for i, m in enumerate(MARKS):
    p.stroke('mark%d' % i, m, step=3, deco=True, w=1.2)
p.stroke('head', HEAD, step=2)
p.shape('eye', circle(EYE[0], EYE[1], 2.7), step=4)
p.stroke('gill', GILL, step=4, deco=True)
p.stroke('mouth', MOUTH, step=4, deco=True)
p.stroke('z', Z, step=1)
p.build()
p.stay_white('eye', 'well')
pupil = dot(*p.pt(EYE[0] + 0.3, EYE[1]), w=3.4)

TN = {'orange': 'orange', 'brown': 'brown'}[TAILC]
steps = [
    step('Start with a Z', 'Draw a capital Z: a line across, a slanting line down to the left, and another line across.', p.step(1)),
    step('The head', 'From the top right corner of the Z draw the head: along a little, round a pointed nose and back to the end of the Z.', p.step(2)),
    step('The tail', 'From the start of the Z draw the body getting thin, then round to the bottom corner of the Z. Add a tail fin with two points, and two slanting lines.', p.step(3)),
    step('The face', 'Draw an eye with a dot in it. Draw a curved line behind the head, and a little line for the mouth.', p.step(4) + [pupil]),
    step('The dish', 'Draw a long dish round the fish: a big box with round corners. Draw another box just inside it.', p.step(5)),
    step('Tomatoes and parsley', 'Above the tail draw three little tomatoes, each with a tiny star. Draw two curly bits of parsley: one top right, one bottom left.', p.step(6)),
    step('Slices of lemon', 'Under the head draw two slices of lemon: two circles, each with six little lines like spokes.', p.step(7)),
    step('Colour light brown', 'Colour the fish light brown, both sides of the cut. Leave its eye white.',
         [p.face('lbrown', (ZC - 4, B - 8), holes=('eye',)), p.face('lbrown', (ZA + 6, T + 8))], use='lbrown'),
    step('Colour ' + TN, 'Colour the tail fin %s.' % TN, [p.face(TAILC, (XP - 3.5, MID))], use=TAILC),
    step('Colour red', 'Colour the three tomatoes red, all round their little stars.', [p.ring('red', 'tom%d' % i, holes=('star%d' % i,)) for i in range(3)], use='red'),
    step('Colour yellow', 'Colour the two slices of lemon yellow.', [p.ring('yellow', 'lem%d' % i) for i in range(2)], use='yellow'),
    step('Colour green', 'Colour the two bits of parsley green. Colour the tiny star on each tomato green too.',
         [p.ring('green', 'pars%d' % i) for i in range(2)] + [p.ring('green', 'star%d' % i) for i in range(3)], use='green'),
    step('Colour light blue', 'Colour the rim of the dish light blue: the strip between its two lines. The middle of the dish stays white.',
         [p.ring('lblue', 'dish', holes=('well',))], use='lblue'),
]
D = drawing('dx_zander_z', 'Z is for Zander', 3, 15, 'things', ['Letters', 'Around the house'],
            'A zander is a fish. This one is grilled whole and cut in two, on a dish with tomatoes and lemon. The capital letter Z is hiding in it: its back, the cut and its belly.',
            steps, ['lbrown', TAILC, 'red', 'yellow', 'green', 'lblue'])
ok = finish('zander' if TAILC == 'orange' else 'zander-' + TAILC, D, {'set': 'house-AZ', 'slot': 'Z', 'kind': 'key', 'age_from': 5}, p)
