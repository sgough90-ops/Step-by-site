"""X is for Xiao long bao (dx_xiaolongbao_x), Food and drink A to Z, slot X (23 Nov 2026).
His idea (19:31), on Claude's sketch "Like your photo" (four soup dumplings in a bamboo steamer, after his ChatGPT card):
he circled the front dumpling and said that if it moves slightly to the left, an X will form.
In that sketch the sloping edges of two dumplings behind run down to a point beside the front dumpling's top, and the
front dumpling's own two edges slope away below. Moved across, the four edges make an X.

So the X is real edges of the dumplings: one line is the left dumpling's right edge, carrying straight on as the front
dumpling's right edge; the other is the right dumpling's left edge, carrying on as the front dumpling's left edge.
They cross at the pinch of the front dumpling, whose little top stands in the notch above. The four dumplings sit in
a diamond (back, left, right, front), as in his picture, so both lines are straight and the X has a normal shape.
The dumplings stay white. The back one stands up in front of the rim, so the brown inside is not a ring round them.

    python3 build_xiaolongbao.py
"""
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=0.0)
K = math.sqrt(0.5)
O = (50.0, 40.0)                               # where the X crosses: the pinch of the front dumpling
UP, DOWN = 13.0, 16.7                          # the X's arms above and below the crossing
NK, NH, OVX, OVY = 2.6, 2.4, 3.2, 1.3          # a dumpling's top: half its base, how tall its neck is, its oval
TALL = 27.0                                    # a dumpling, from its pinch to its bottom
BACK = 19.0                                    # how far above the crossing the back dumpling's top starts

UL = (O[0] - UP * K, O[1] - UP * K); UR = (O[0] + UP * K, O[1] - UP * K)       # the X's four ends
LL = (O[0] - DOWN * K, O[1] + DOWN * K); LR = (O[0] + DOWN * K, O[1] + DOWN * K)


def parts(ax, ay, nk):
    """a dumpling whose pinch is at (ax, ay): where its two edges start, its two hips, and its round bottom (two pieces)"""
    h = nk + (UP if nk else DOWN) * K
    sl, sr = (ax - nk, ay + nk), (ax + nk, ay + nk); hl, hr = (ax - h, ay + h), (ax + h, ay + h); yb = ay + TALL
    b1 = Seg(hl, (hl[0] - 5.66, hl[1] + 5.66), (ax - 11, yb), (ax, yb))
    b2 = Seg((ax, yb), (ax + 11, yb), (hr[0] + 5.66, hr[1] + 5.66), hr)
    return sl, sr, hl, hr, b1, b2


def top(name, sl, sr, step):
    """the little twisted top: two short lines and an oval. sl and sr are where it stands"""
    cx, y = (sl[0] + sr[0]) / 2, min(sl[1], sr[1]) - NH
    tl, tr = (cx - OVX, y), (cx + OVX, y)
    p.region(name + 'kR', poly(sl, tl, tr, sr, closed=True))
    p.stroke(name + '_nl', Seg(sl, tl), step=step); p.stroke(name + '_nr', Seg(sr, tr), step=step)
    p.shape(name + '_ov', ell(cx, y, OVX, OVY), step=step)


def folds(name, ax, ay, step, which=(-1, 0, 1), y0=6.6, y1=15.2, out=8.2):
    """the folds in the dough: thinner lines that follow the dumpling's own shape; the middle one is straight"""
    for k in which:
        if k == 0:
            p.stroke(name + '_f1', Seg((ax, ay + y0 + 0.6), (ax, ay + y1 + 0.6)), step=step, deco=True, w=1.2)
            continue
        a = (ax + k * 2.9, ay + y0); b = (ax + k * out, ay + y1)
        p.stroke('%s_f%d' % (name, k + 1), Seg(a, (a[0] + k * 2.6, a[1] + 2.4), (b[0], b[1] - 3.6), b), step=step, deco=True, w=1.2)


# ---- the steamer (behind the dumplings) ----
YB = O[1] - BACK                                # the back dumpling's top stands here
OT, IT = YB + 1.75, YB + 7.3                    # the back of the rim: its outside and inside edges, in the middle
FI = O[1] + TALL + 2.7; FO = FI + 2.5           # the front of the rim: inside and outside edges
CO, RO = (OT + FO) / 2, (FO - OT) / 2           # the outside oval
CI, RI = (IT + FI) / 2, (FI - IT) / 2           # the inside oval
WALL, LEAN = 21.5, 0.6
p.shape('rim_o', ell(50, CO, 46, RO), step=6)
side = lambda t: 4 - LEAN * t                   # the wall leans out a touch, so it does not run along the oval
p.stroke('wall', Seg((4, CO), (side(1), CO + WALL)), arc(50, CO + WALL, 50 - side(1), RO, 180, 0, start=P(side(1), CO + WALL), end=P(100 - side(1), CO + WALL)),
         Seg((100 - side(1), CO + WALL), (96, CO)), step=7)
TURN = 4.0                                                                        # each band meets the wall at a slant: it stops this many degrees short of the end
for i, yc in enumerate((CO + 4.6, CO + WALL - 6.2)):
    ye = yc + RO * math.sin(math.radians(TURN)); x = side((ye - CO) / WALL); rx = (50 - x) / math.cos(math.radians(TURN))
    p.stroke('hoop%d' % i, arc(50, yc, rx, RO, 180 - TURN, TURN, start=P(x, ye), end=P(100 - x, ye)), step=7)
p.shape('rim_i', ell(50, CI, 42, RI), step=6)
ONIONS = [(17.5, 44.5), (82.5, 42.0), (22.5, 60.5), (78.0, 61.5)]
for i, (x, y) in enumerate(ONIONS):
    p.shape('on%d' % i, circle(x, y, 2.2), step=8)

# ---- the four dumplings: back, left, right, front ----
sl, sr, hl, hr, b1, b2 = parts(50, YB - NK, NK)
p.region('bbR', Seg(sl, hl), b1, b2, Seg(hr, sr), Seg(sr, sl))
p.stroke('bb_l', Seg(sl, hl), step=4); p.stroke('bb_r', Seg(sr, hr), step=4)
top('bb', sl, sr, 4)
folds('bb', 50, YB - NK, 5, which=(-1, 1), y0=7.6, y1=12.6, out=5.2)

sl, sr, hl, hr, b1, b2 = parts(UL[0] - NK, UL[1] - NK, NK)                      # left: its right edge is the X's top left arm
p.region('blR', Seg(sl, hl), b1, b2, Seg(hr, sr), Seg(sr, sl))
p.stroke('bl_s', Seg(sl, hl), step=3); p.stroke('bl_b', b1, step=3)
top('bl', sl, sr, 3)
folds('bl', UL[0] - NK, UL[1] - NK, 5, which=(-1, 0)); folds('blx', UL[0] - NK, UL[1] - NK, 5, which=(1,), y1=12.0, out=6.0)

sl, sr, hl, hr, b1, b2 = parts(UR[0] + NK, UR[1] - NK, NK)                      # right: its left edge is the X's top right arm
p.region('bcR', Seg(sl, hl), b1, b2, Seg(hr, sr), Seg(sr, sl))
p.stroke('bc_s', Seg(sr, hr), step=3); p.stroke('bc_b', rev([b2]), step=3)
top('bc', sl, sr, 3)
folds('bc', UR[0] + NK, UR[1] - NK, 5, which=(0, 1)); folds('bcx', UR[0] + NK, UR[1] - NK, 5, which=(-1,), y1=12.0, out=6.0)

sl, sr, hl, hr, b1, b2 = parts(O[0], O[1], 0)                                   # front: its two edges are the X's bottom arms
p.region('fR', Seg(O, hl), b1, b2, Seg(hr, O))
p.stroke('f_b', b1, b2, step=2)
top('f', (O[0] - NK, O[1] - NK), (O[0] + NK, O[1] - NK), 2)
p.region('fpR', poly(O, (O[0] - NK, O[1] - NK), (O[0] + NK, O[1] - NK), closed=True))
folds('f', O[0], O[1], 5, which=(-1, 1), y0=7.6, y1=16.4, out=8.6)

for i, (x, y0) in enumerate(((28, 7.5), (50, 3.6), (72, 7.5))):
    pts = [(x + (0 if k in (0, 6) else (1.8 if k % 2 else -1.8)), y0 + 12.5 * k / 6) for k in range(7)]
    p.stroke('steam%d' % i, smooth(pts), step=8, deco=True)

# ---- the X, in front of everything ----
p.stroke('x1', Seg(UL, LR), step=1)
p.stroke('x2', Seg(UR, LL), step=1)
p.build()

steps = [
    step('Start with an X', 'Draw a capital X: a line sloping down to the right, then a line sloping down to the left across it.', p.step(1)),
    step('The front dumpling', 'Join the two bottom ends of the X with a big round curve underneath. Just above the middle of the X draw a tiny top: two short lines and a little oval.', p.step(2)),
    step('Two more dumplings', 'At each top end of the X draw a little top. From it, slope down and curve round until you reach the front dumpling.', p.step(3)),
    step('The one at the back', 'Higher up, between them, draw one more little top. Draw a line sloping down from each side of it.', p.step(4)),
    step('Folds', 'Draw two or three curved lines down each dumpling. These are the folds in the dough.', p.step(5)),
    step('The basket', 'Draw a big oval round all the dumplings. It goes behind the back one. Draw another oval just inside it.', p.step(6)),
    step('The side of the basket', 'Draw a line down from each end of the big oval. Join them with a curve. Draw two curved bands across.', p.step(7)),
    step('Steam and spring onion', 'Draw three wavy lines of steam at the top. Draw four small circles in the basket: bits of spring onion.', p.step(8)),
    step('Colour light brown', 'Colour the rim of the basket light brown. Colour the middle of its side light brown too.',
         [p.face('lbrown', (50, (FI + FO) / 2)), p.face('lbrown', (50, CO + RO + WALL / 2))], use='lbrown'),
    step('Colour brown', 'Colour the inside of the basket brown, all round the dumplings. Colour the two bands brown.',
         [p.face('brown', (14, CI), holes=['on%d' % i for i in range(4)]), p.face('brown', (50, CO + RO + 2.3)), p.face('brown', (50, CO + RO + WALL - 3.1))], use='brown'),
    step('Colour green', 'Colour the four bits of spring onion green. The dumplings stay white.', [p.ring('green', 'on%d' % i) for i in range(4)], use='green'),
]
D = drawing('dx_xiaolongbao_x', 'X is for Xiao long bao', 3, 15, 'things', ['Letters', 'Around the house'],
            'Soup dumplings in a bamboo basket. The capital letter X is hiding in them: it is the sloping edges where the dumplings meet.',
            steps, ['lbrown', 'brown', 'green'])
ok = finish('xiaolongbao', D, {'set': 'house-AZ', 'slot': 'X', 'kind': 'key', 'age_from': 5}, p)
