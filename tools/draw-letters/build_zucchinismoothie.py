"""z is for Zucchini smoothie (dx_zucchinismoothie_z), Food and drink a to z, slot z (24 Nov 2026).
From his pick, number 2 "Flat-top lid" of Claude's four alternatives to ChatGPT's number 8
(sheet z-zucchini-smoothie-like-8.png). His words: "Four alternatives to this", then "Create steps for number 2 and make live".

A cup of zucchini smoothie with a see-through dome lid and a yellow straw, two slices of zucchini in front and a whole
zucchini behind. The z is in the lid: its top line is the flat top of the lid (from its left end to the straw), its
slanting line is the left edge of the straw seen through the lid, and its bottom line is part of the rim of the lid
(21.3 wide, 24 tall). The straw carries the slanting line on up out of the lid; the rim carries the bottom line on both ways.
The lid's flat top is only as long as the z's top line plus the straw, so the straw hides the rest of it and no line
runs on past the z's top right corner but the straw's own edge.
The slices come before the cup in the steps, because the front slice hides a corner of the cup; the zucchini comes
after it, because the cup hides its end. The lid stays white (it is see-through): it is not shut inside a colour.
Written in the sketch's numbers.

    python3 build_zucchinismoothie.py
"""
from bcommon import *

p = Pic(s=1.0, dx=-1.4, dy=-1.5)
X0, TOP, BOT = 36.5, 20.0, 44.0                  # the z: its left, its top line (the flat top of the lid), its bottom line (the rim)
XH1, SW = 64.5, 5.0                              # the right end of the lid's flat top; how wide the straw is
W = 21.0                                         # the z's width: the straw must just fit between its top right corner and XH1
for _ in range(60):
    W = (XH1 - X0) - SW * math.hypot(W, BOT - TOP) / (BOT - TOP)
X1 = r2(X0 + W)                                  # 57.81
HW = r2(XH1 - X1)                                # 6.69: how wide the straw is along a level line
LEN = math.hypot(X1 - X0, BOT - TOP)
UX, UY = (X1 - X0) / LEN, (TOP - BOT) / LEN      # up the straw
UP = 18.0                                        # how far the straw stands out above the lid
TL = P(X1 + UX * UP, TOP + UY * UP)              # the straw's top end: its left corner, and its right corner
TR = P(TL[0] - UY * SW, TL[1] + UX * SW)
RIM = (23.0, BOT, 77.0, 50.5, 2.4)               # the rim of the lid: a long thin box with round ends
CUP = one("M27,47 L31,90 Q31.4,94 35.4,94 L64.6,94 Q68.6,94 69,90 L73,47")   # its top runs on behind the rim and is trimmed
ZA, ZLEN, ZR, ZDEG = (60.0, 88.0), 31.06, 5.5, -33.18   # the zucchini: where its hidden end is, how long, how fat, how it leans
S1, S2 = (15.0, 87.0, 8.5, 6.2), (27.0, 90.0, 7.5, 5.4)  # the two slices: middle, size, size of the ring inside

Z = poly((X0, TOP), (X1, TOP), (X0, BOT), (X1, BOT))


def turned(segs, deg=ZDEG, c=ZA):
    """pieces turned about the zucchini's hidden end (a minus number turns anticlockwise on screen)"""
    co, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [Seg(*[(c[0] + (x - c[0]) * co - (y - c[1]) * si, c[1] + (x - c[0]) * si + (y - c[1]) * co) for x, y in s.p]) for s in segs]


def along(d, off=0.0):
    """a point d along the zucchini from its hidden end, off to one side (minus = the upper side)"""
    return turned([Seg((ZA[0] + d, ZA[1] + off), (ZA[0] + d + 1, ZA[1] + off))])[0].a


# ---- behind the cup: the zucchini (its stalk first), and two lines along it ----
p.shape('stalk', turned(rrect(ZA[0] + ZLEN + 2.4, ZA[1] - 2.2, ZA[0] + ZLEN + 11.8, ZA[1] + 2.2, 2.2)), step=7)
p.shape('zuc', turned(rrect(ZA[0] - ZR, ZA[1] - ZR, ZA[0] + ZLEN + ZR, ZA[1] + ZR, ZR)), step=7)
for i, off in enumerate((-1.9, 1.9)):
    p.stroke('zline%d' % i, Seg(along(17.0, off), along(28.5, off)), step=7, deco=True, w=1.2)

# ---- the cup (hides the end of the zucchini), then the rim of the lid (hides the top of the cup) ----
p.region('cupR', CUP, Seg(CUP[-1].b, CUP[0].a))
p.stroke('cup', CUP, step=6)
R = rrect(*RIM)
p.region('rimR', R)
p.stroke('rim', Seg((X1, BOT), R[0].b), R[1:], Seg(R[0].a, (X0, BOT)), step=3)     # all of the rim but the z's bottom line

# ---- in front of the cup: two slices, the right-hand one in front ----
for nm, (cx, cy, r, ri) in (('s1', S1), ('s2', S2)):
    p.shape(nm, circle(cx, cy, r), step=5)
    p.stroke(nm + 'in', circle(cx, cy, ri), step=5, w=1.2)

# ---- the lid: a curve each side, from the rim up to the flat top ----
p.stroke('lidL', Seg((28, BOT), (28, 33), (31.5, 24), (X0, TOP)), step=4)
p.stroke('lidR', Seg((XH1, TOP), (68.5, 24), (72, 33), (72, BOT)), step=4)

# ---- the straw: up from the z's top right corner, across its end, and back down its other edge to the z's bottom line ----
p.stroke('straw', Seg((X1, TOP), TL), Seg(TL, TR), Seg(TR, (XH1, TOP)), Seg((XH1, TOP), (X0 + HW, BOT)), step=2)

# ---- the z, in front of everything ----
p.stroke('z', Z, step=1)
p.build()
# four seeds in each slice, set out like a diamond (three dots read as a face)
seeds = [dot(*p.pt(cx + dx * k, cy + dy * k), w=1.5) for (cx, cy, r, ri), k in ((S1, 3.0), (S2, 2.6)) for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0))]

steps = [
    step('Start with a z', 'Draw a small letter z: a line across, a slanting line down to the left, and another line across.', p.step(1)),
    step('The straw', 'From the top right corner of the z, carry the slanting line on up. Draw a short line across its end, then a long line back down to the bottom of the z.', p.step(2)),
    step('The rim of the lid', 'Carry the bottom line of the z on both ways. Join the two ends underneath to make a long thin box with round ends.', p.step(3)),
    step('The lid', 'Draw a curve from the start of the z down to the rim. Draw another curve from the straw down to the rim on the other side.', p.step(4)),
    step('Two slices', 'Bottom left, draw two slices of zucchini: two circles, one in front of the other. Draw a ring inside each, and four little seeds.', p.step(5) + seeds),
    step('The cup', 'From the rim draw the two sides of the cup, sloping in a little. Join them with a round bottom. The front slice hides one corner.', p.step(6)),
    step('The zucchini', 'Behind the cup draw a zucchini: a long round shape pointing up to the right. Add a little stalk on its end and two lines along it.', p.step(7)),
    step('Colour the smoothie', 'Colour the smoothie in the cup green.', [p.face('green', (50, 72))], use='green'),
    step('Colour the zucchini', 'Colour the zucchini and its stalk green. Colour the outside ring of each slice green too.',
         [p.face('green', along(24.0)), p.face('green', along(ZLEN + 9.0)), p.face('green', (S1[0], S1[1] - 7.4)), p.ring('green', 's2', holes=('s2in',))], use='green'),
    step('Colour yellow', 'Colour the straw yellow, all the way up. Colour the middle of each slice yellow.',
         [p.face('yellow', (52.2, 30)), p.face('yellow', (S1[0] - 3.5, S1[1])), p.ring('yellow', 's2in')], use='yellow'),
    step('Colour light blue', 'Colour the rim of the lid light blue. The lid itself stays white: you can see through it.', [p.face('lblue', (50, 47.2))], use='lblue'),
]
D = drawing('dx_zucchinismoothie_z', 'z is for Zucchini smoothie', 2, 12, 'things', ['Letters', 'Around the house'],
            'A cup of zucchini smoothie with a see-through lid and a straw. The small letter z is hiding in the lid: its flat top, the edge of the straw and the rim.',
            steps, ['green', 'yellow', 'lblue'])
ok = finish('zucchinismoothie', D, {'set': 'house-az', 'slot': 'z', 'kind': 'key', 'age_from': 4}, p)
