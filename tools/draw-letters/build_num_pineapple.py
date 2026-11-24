"""4 is for Pineapple (dx_pineapple_4), Food and drink 1 to 9, slot 4 (24 Nov 2026).
From his pick "The third ones works best" (15:34) on the sheet number-4-pineapple-four-ways (design 3, "Leafy top"), with
his note "make sure the three bottom leaves [that] are dropped down are the same size". Notes:
claude/step-by-draw-number-4-pineapple-build.py. The layered leaves are his idea, from a picture of a 4 as a bamboo shoot.

A pineapple with a crown of pointed leaves that sit in front of each other. The 4 is the pointed-top kind (as on the
Jet car): its slanting line and the top half of its straight line are the front leaf, its flat line is the top of the
fruit, and the bottom of its straight line is the edge of a little leaf hanging over the fruit. The three hanging leaves
are the same shape and size and evenly spaced. Every leaf stands on the flat line, so no leaf draws its own bottom edge
(a region() and one stroke() each). The diamond lines are placed so that none of them ends on the 4: each one runs from
the fruit's edge to the fruit's edge or to the first little leaf it reaches, and is not carried on past that leaf (the
script stops if one would touch the 4). All leaves are one green; in the sketch they were three greens. The tall leaf
was made a little narrower than in the sketch, so it does not show again on the right of the 4's straight line.
Written in the sketch's numbers.

    python3 build_num_pineapple.py
"""
from ncommon import *

p = Pic(s=0.71, dx=16.6, dy=8.0)
XM, TOP, XA, YB, XC, Y1 = 58, 8, 28, 52, 72, 65            # the 4: straight line's x, its top, left end, flat line's y, right end, bottom
HANG_W, HANG_STEP = 10, 13                                # the three hanging leaves: how wide, how far apart
HANG = (XM - 2 * HANG_STEP, XM - HANG_STEP, XM)            # where each one's upright edge is
UP = (89.5, 108.5, 127.5, 146.5, 165.5)                    # the diamond lines going up to the right: x + y
DOWN = (-8, 11, 30, 49, 68)                                # ... and going down to the right: y - x

FRUIT = one("M28,52 C12,60 12,108 34,121 L66,121 C88,108 88,60 72,52")
FLAT = Seg((XA, YB), (XC, YB))
EDGES = {'the fruit': FRUIT, 'the flat line of the 4': [FLAT], 'the bottom of the 4': [Seg((XM, YB), (XM, Y1))]}
for i, x0 in enumerate(HANG):
    EDGES['little leaf %d' % (i + 1)] = ([] if x0 == XM else [Seg((x0, YB), (x0, Y1))]) + [Seg((x0, Y1), (x0 + HANG_W, YB))]
FRUIT_POLY = chain_arr(FRUIT + [Seg(FRUIT[-1].b, FRUIT[0].a)])
HANG_POLY = [np.array([(x0, YB), (x0 + HANG_W, YB), (x0, Y1)], float) for x0 in HANG]


def diamond_line(a, b):
    """the part of the slanted line through a and b that shows on the fruit, and what each end stops on"""
    hits = []
    for what, segs in EDGES.items():
        for s in segs:
            for t, q in line_hits_seg(a, b, s):
                if all(math.dist(q, h[0]) > 0.05 for h in hits): hits.append((q, what))
    hits.sort(key=lambda h: h[0][0])
    shows = []
    for (q0, w0), (q1, w1) in zip(hits, hits[1:]):
        m = ((q0[0] + q1[0]) / 2, (q0[1] + q1[1]) / 2)
        if in_poly(m, FRUIT_POLY) and not any(in_poly(m, h) for h in HANG_POLY): shows.append((q0, q1, w0, w1))
    # a line that reaches a little leaf stops there (the child is told to), so only its long part is drawn
    q0, q1, w0, w1 = max(shows, key=lambda v: math.dist(v[0], v[1]))
    assert '4' not in w0 + w1, ('a diamond line ends on the 4', a, b, w0, w1)
    assert math.dist(q0, q1) > 12, ('a very short diamond line', a, b)
    return Seg(q0, q1), (w0, w1)


# ---- the fruit, its diamond lines and the two little leaves beside the 4's own one (all below the flat line) ----
p.stroke('fruit', FRUIT, step=2)
STOPS = []
for i, c in enumerate(UP):
    s_, ends = diamond_line((0, c), (c, 0)); STOPS.append(('up %s' % c,) + ends)
    p.stroke('up%d' % i, s_, step=6, deco=True, w=1.2)
for i, e in enumerate(DOWN):
    s_, ends = diamond_line((0, e), (100, 100 + e)); STOPS.append(('down %s' % e,) + ends)
    p.stroke('down%d' % i, s_, step=7, deco=True, w=1.2)
for i, x0 in enumerate(HANG):
    if x0 == XM: p.stroke('hang%d' % i, Seg((x0, Y1), (x0 + HANG_W, YB)), step=5)        # its upright edge is the bottom of the 4
    else: p.stroke('hang%d' % i, poly((x0, YB), (x0, Y1), (x0 + HANG_W, YB)), step=5)


# ---- the crown, back to front. Each leaf: up one side to its point and down the other; its bottom is the flat line ----
def crown(name, d, step):
    segs = one(d)
    p.region(name + 'R', segs, Seg(segs[-1].b, segs[0].a))
    p.stroke(name, segs, step=step)


crown('tall', "M38,52 Q33,22 45,-3 Q58,20 56,52", 4)          # behind the top of the 4
crown('right', "M54,52 Q60,27 86,12 Q88,38 72,52", 4)
crown('big', "M28,52 Q11,32 13,6 Q40,23 52,52", 3)
crown('low', "M28,52 Q9,47 6,29 Q29,32 46,52", 3)

# ---- the 4, in front of everything: its own leaf hides what is behind it ----
p.region('fourR', poly((XM, TOP), (XA, YB), (XM, YB), closed=True))
p.stroke('four_a', poly((XM, TOP), (XA, YB), (XC, YB)), step=1)
p.stroke('four_b', Seg((XM, TOP), (XM, Y1)), step=1)
p.build()

GREEN = [(15, 40), (22, 22), (45, 10), (75, 30), (50, 40)] + [(x0 + 2.5, YB + 4) for x0 in HANG]
steps = [
    step('Start with a 4', 'Draw a number 4: a slanted line down, a flat line across, then a straight line down from the top. This 4 is hiding in a pineapple.', p.step(1)),
    step('The pineapple', 'From the left end of the flat line, draw a big round shape: down, flat along the bottom, and back up to the right end of the line.', p.step(2)),
    step('Two leaves', 'From the left corner of the 4 draw a pointed leaf, out to the left and back to the slanted line. Draw a bigger leaf above it.', p.step(3)),
    step('Two more leaves', 'Draw a tall leaf pointing up behind the 4. Then a leaf on the right: from the straight line, out to a point and down to the end of the flat line.', p.step(4)),
    step('Three little leaves', 'Three little leaves hang down. Draw two: a short line down and a slanted line back up. Then a slanted line up from the bottom of the 4.', p.step(5)),
    step('Slanted lines', 'Draw slanted lines across the pineapple, all going the same way. Stop when you reach a little leaf.', p.step(6)),
    step('Diamonds', 'Now draw slanted lines the other way to make diamonds. Stop when you reach a little leaf.', p.step(7)),
    step('Colour green', 'Colour all the leaves green: the big ones on top and the three little ones.', [p.face('green', s) for s in GREEN], use='green'),
    step('Colour yellow', 'Colour the pineapple yellow, all round the little leaves.', [p.face('yellow', (50, 100))], use='yellow'),
]
D = drawing('dx_pineapple_4', '4 is for Pineapple', 2, 10, 'things', TAGS,
            'A pineapple with pointed leaves. The number 4 is hiding in it: the front leaf, the top of the pineapple and a little leaf hanging down.',
            steps, ['green', 'yellow'])
if __name__ == '__main__':
    for s_ in STOPS: print('    diamond line %-11s from %s to %s' % s_)
    ok = finish('num4pineapple', D, {'set': SET, 'slot': '4', 'kind': 'key', 'age_from': 4}, p, allow=('7',))
