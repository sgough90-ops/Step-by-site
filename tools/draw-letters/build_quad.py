"""Q is for Quad bike (dx_quadbike_q), Vehicles A to Z, slot Q. Version 2, 28 Nov 2026 (version 1 was 14 Nov, green since 27 Nov).

His asks on 28 Nov: none of the first sketches looked nice with the Q's line (it stuck out to a puff of dust), so "find
a clever way to incorporate that line, for example use it as a spoke on the wheel"; then "combine 1 and 2 for the
wheels so the q is embedded better" (spokes inside the rim, tread on the tyre); then, of the four-spoke version, "I want
the spokes from the inner circle and outer circle to be aligned ... as if it's one long line". His pick: 1 ("Four long
lines") of the lined-up sheet, then "make live".

Side view, facing left. Each wheel is a tyre (grey), a rim (yellow) and a little middle (black), with four long lines
from the middle out to the edge of the tyre, like a big X. The Q is the rim of the back wheel, and its tail is one of
that wheel's four long lines (the one at the bottom right).
The other three long lines are each two lines, a spoke and a groove, that stop at the rim from either side at the very
same spot. So no line goes through the Q, but lines do meet it from both sides at one spot: that is what he asked for
("as if it's one long line"), and he was told it goes against the old rule. No dust.
The body is green, his pick in the colour changes of 27 Nov. (The sketch he picked was purple and it went live purple
on 28 Nov at 16:15; he asked for that to be changed the same afternoon.) Written in the sketch's numbers with vkit; the
Pic moves it onto the paper.

    python3 build_quad.py
"""
from bcommon import *

p = Pic(s=1.05, dx=-2.30, dy=-6.80)
BC, BR = (68.0, 69.0), 14.5                  # back wheel (its rim is the Q)
FC, FR = (26.0, 71.0), 12.5                  # front wheel
RIM, HUB = 0.62, 0.19                        # the rim and the little middle, as parts of the wheel's size
ANG = (45, 135, 225, 315)                    # the four long lines; the one at 45 (bottom right) is the Q's tail
FG, RG = 16.0, 18.0                          # the mudguards: round the wheels with a gap
BODY = 'green'


def at(c, r, a):
    return P(c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a)))


def wheel(tag, c, R, step_circles, step_lines, letter=False):
    """tyre, grooves, rim, spokes, middle. With letter=True the rim and the long line at 45 are left for the Q."""
    r, h = R * RIM, R * HUB
    p.shape('tyre' + tag, circle(c[0], c[1], R), step=step_circles)
    for a in ANG:
        if not (letter and a == 45):
            p.stroke('groove%s%d' % (tag, a), Seg(at(c, r, a), at(c, R, a)), step=step_lines, deco=True)
    if not letter:
        p.shape('rim' + tag, circle(c[0], c[1], r), step=step_circles)
    for a in ANG:
        if not (letter and a == 45):
            p.stroke('spoke%s%d' % (tag, a), Seg(at(c, h, a), at(c, r, a)), step=step_lines, deco=True)
    p.shape('hub' + tag, circle(c[0], c[1], h), step=step_circles)
    return r, h


# ---- behind the body: the handlebars (a post and a bar) ----
p.stroke('post_l', Seg((32.0, 38.4), (32.0, 28.9)), step=8)
p.stroke('post_r', Seg((35.2, 38.4), (35.2, 28.9)), step=8)
p.shape('bar', rrect(24.1, 24.7, 43.1, 28.9, 2.1), step=8)

# ---- the body: mudguards over both wheels, the top line, the bump at the front ----
f0, f1 = at(FC, FG, 196), at(FC, FG, 336)
r0, r1 = at(BC, RG, 197), at(BC, RG, 346)
body = arc(FC[0], FC[1], FG, FG, 196, 336, start=f0, end=f1) + [Seg(f1, r0)] + arc(BC[0], BC[1], RG, RG, 197, 346, start=r0, end=r1) + \
       [Seg(r1, (88.6, 60.5), (89.6, 54.0), (89.6, 49.6)), Seg((89.6, 49.6), (89.6, 46.8), (88.27, 45.4), (85.6, 45.4)),
        Seg((85.6, 45.4), (47.0, 45.4)), Seg((47.0, 45.4), (43.5, 45.4), (42.0, 38.4), (37.0, 38.4)), Seg((37.0, 38.4), (30.5, 38.4)),
        Seg((30.5, 38.4), (24.5, 38.4), (16.5, 45.5), (12.5, 51.5)), Seg((12.5, 51.5), (10.0, 55.4), (9.4, 61.0), f0)]
p.shape('body', body, step=6)
p.shape('lamp', circle(20.6, 48.6, 2.8), step=9)

# ---- on the body's top line: the seat, and the rack with its two bars ----
p.stroke('seat', one("M50,45.4 C50,41.4 51.8,39.8 55.4,39.8 L69,39.8 C72.6,39.8 74.4,41.4 74.4,45.4"), step=7)
p.stroke('rack', poly((76.8, 45.4), (78.9, 38.2), (87.7, 38.2), (85.6, 45.4)), step=9)
for i, x in enumerate((79.7, 82.7)):
    p.stroke('slat%d' % i, Seg((x, 45.4), (x + 2.1, 38.2)), step=9, deco=True)

# ---- the wheels ----
wheel('F', FC, FR, 4, 5)
QR, QH = wheel('B', BC, BR, 2, 3, letter=True)

# ---- the Q, in front of everything: the back wheel's rim, and the long line at the bottom right ----
p.stroke('Q_ring', circle(BC[0], BC[1], QR), step=1)
p.stroke('Q_tail', Seg(at(BC, QH, 45), at(BC, BR, 45)), step=1)
p.build()

steps = [
    step('Start with a Q', 'Draw a capital Q: a round circle, then a straight line that starts inside it and pokes out at the bottom right.', p.step(1)),
    step('The back wheel', "Draw a little circle in the middle, at the start of the Q's line. Draw a big circle round the Q, at the end of its line.", p.step(2)),
    step('Three more lines', 'Draw three more lines from the little circle out to the big circle, so the wheel has a big X on it.', p.step(3)),
    step('The front wheel', 'Draw a smaller wheel on the left: a big circle, a circle inside it and a little circle in the middle.', p.step(4)),
    step('Its four lines', 'Draw four lines from the little circle out to the big circle, to make a big X like the back wheel.', p.step(5)),
    step('The body', 'Draw a curved mudguard over each wheel and join them. Go up the back, along the top, over a bump and down the front.', p.step(6)),
    step('The seat', 'Draw a long seat on the top of the body.', p.step(7)),
    step('The handlebars', 'Draw a short post up from the bump at the front. Put a long bar on top of it.', p.step(8)),
    step('Rack and light', 'Draw a rack on the back: a sloping box with two lines in it. Draw a round light on the front of the body.', p.step(9)),
    step('Colour ' + BODY, 'Colour the body %s. Go round the light.' % BODY, [p.ring(BODY, 'body', holes=('lamp',))], use=BODY),
    step('Colour grey', 'Colour both tyres grey, between the two big circles. Colour the rack and the post grey too.',
         [p.ring('grey', 'tyreF', holes=('rimF',)), p.ring('grey', 'tyreB', holes=('Q_ring',)), p.face('grey', (81.5, 42.0)), p.face('grey', (33.6, 33.5))], use='grey'),
    step('Colour yellow', 'Colour the inside of both wheels yellow, round the little circles. Colour the light yellow too.',
         [p.ring('yellow', 'rimF', holes=('hubF',)), p.ring('yellow', 'Q_ring', holes=('hubB',)), p.ring('yellow', 'lamp')], use='yellow'),
    step('Colour black', 'Colour the seat and the handlebars black. Colour the little circles in the wheels black too.',
         [p.face('black', (62.0, 43.0)), p.ring('black', 'bar'), p.ring('black', 'hubF'), p.ring('black', 'hubB')], use='black'),
]
D = drawing('dx_quadbike_q', 'Q is for Quad bike', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'A %s quad bike with big chunky wheels. The capital Q is hiding in the back wheel: the circle is the rim of the wheel '
            'and the tail is one of the four long lines across it.' % BODY,
            steps, [BODY, 'grey', 'yellow', 'black'])
ok = finish('quad', D, {'set': 'vehicles-AZ', 'slot': 'Q', 'kind': 'drive', 'age_from': 5}, p)

if __name__ == '__main__':
    pts = [q for st in D['steps'] for it in st['add'] for sub_, _ in CK.parse(it['d'], step=0.5) for q in sub_]
    xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
    print('    on the paper: x %.2f to %.2f, y %.2f to %.2f (middle %.2f, %.2f)' % (min(xs), max(xs), min(ys), max(ys), (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2))
    print('    longest step text %d, most lines in a step %d' % (max(len(st['text']) for st in D['steps']), max(sum(1 for a in st['add'] if 'fill' not in a) for st in D['steps'])))
