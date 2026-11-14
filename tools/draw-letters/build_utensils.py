"""U is for Utensils (Around the house A to Z, slot U). A pot of kitchen utensils.
The U: the sides and bottom of the pot. The front of the rim joins the two tops of the U.
The three handles stand on the front of the rim and the back of the rim is drawn in pieces between them,
so no line crosses another line and nothing crosses the U."""
import json, math, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

X0, X1, TOP, BOT, CR = 30.0, 70.0, 52.0, 90.0, 8.0
RC = (50.0, TOP); RX, RY = 20.0, 4.6        # the rim (an oval)

# ---- 1: the U ----
U_ = [Seg((X0, TOP), (X0, BOT - CR))] + arc(X0 + CR, BOT - CR, CR, CR, 180, 90, start=P(X0, BOT - CR), end=P(X0 + CR, BOT)) + \
     [Seg((X0 + CR, BOT), (X1 - CR, BOT))] + arc(X1 - CR, BOT - CR, CR, CR, 90, 0, start=P(X1 - CR, BOT), end=P(X1, BOT - CR)) + \
     [Seg((X1, BOT - CR), (X1, TOP))]


def place(segs, deg, px, py):
    return shift(rot(segs, deg), px, py)


def rim_hits(E, F):
    """Where a handle line (from its top E towards F) meets the front and the back of the rim."""
    hits = line_oval(E, F, RC[0], RC[1], RX, RY)
    front = max(hits, key=lambda h: h[1][1])[1]; back = min(hits, key=lambda h: h[1][1])[1]
    return front, back

HW = 1.6                                     # half the width of a handle

# ---- the slotted spoon (leans left) ----
SP = (-17.0, 41.0, 53.0); SL, SR_ = 33.0, 7.5
jy = -SL + math.sqrt(SR_ * SR_ - HW * HW)
aL = math.degrees(math.atan2(jy + SL, -HW)); aR = math.degrees(math.atan2(jy + SL, HW))     # about 102 and 78
sp_big = place(arc(0, -SL, SR_, SR_, aL, aR + 360, start=P(-HW, jy), end=P(HW, jy)), *SP)   # round the head
sp_small = place(arc(0, -SL, SR_, SR_, aR, aL, start=P(HW, jy), end=P(-HW, jy)), *SP)       # the bit between the handle lines
spEL, spER = sp_small[-1].b, sp_small[0].a
spFL = place([Seg((-HW, 8), (-HW, 9))], *SP)[0].a; spFR = place([Seg((HW, 8), (HW, 9))], *SP)[0].a
spBL, spKL = rim_hits(spEL, spFL); spBR, spKR = rim_hits(spER, spFR)
sp_dots = [place([Seg((x, y), (x, y + 1))], *SP)[0].a for x, y in ((-2.6, -35.6), (2.6, -35.6), (-2.6, -30.4), (2.6, -30.4))]

# ---- the whisk (upright) ----
WT = 36.0
whEL, whER = P(50 - HW, WT), P(50 + HW, WT)
whBL, whKL = rim_hits(whEL, (50 - HW, 70)); whBR, whKR = rim_hits(whER, (50 + HW, 70))
wh_top = Seg(whEL, whER)
outL = [Seg(whEL, (46.6, 30.0), (43.4, 25.0), (43.4, 18.0)), Seg((43.4, 18.0), (43.4, 11.6), (46.4, 7.0), (50.0, 7.0))]
outer = outL + rev(mirror(outL))
innL = [Seg((49.2, WT), (48.4, 30.0), (46.8, 25.0), (46.8, 19.0)), Seg((46.8, 19.0), (46.8, 13.5), (47.6, 9.6), (50.0, 7.0))]
innR = mirror(innL)
mid = Seg((50.0, WT), (50.0, 7.0))

# ---- the spatula (leans right) ----
ST_ = (15.0, 59.5, 53.0)
hd = rrect(-6.0, -39.0, 6.0, -24.0, 2.0)
assert hd[4].a == P(4.0, -24.0) and hd[4].b == P(-4.0, -24.0)
hd = hd[:4] + [Seg((4.0, -24.0), (HW, -24.0)), Seg((HW, -24.0), (-HW, -24.0)), Seg((-HW, -24.0), (-4.0, -24.0))] + hd[5:]
st_head = place(hd, *ST_)
st_mid = st_head[5]                           # the bit of the head's bottom edge between the handle lines (right to left)
stER, stEL = st_mid.a, st_mid.b
stFL = place([Seg((-HW, 8), (-HW, 9))], *ST_)[0].a; stFR = place([Seg((HW, 8), (HW, 9))], *ST_)[0].a
stBL, stKL = rim_hits(stEL, stFL); stBR, stKR = rim_hits(stER, stFR)
st_slots = place([Seg((x, -36.0), (x, -28.0)) for x in (-3.0, 0.0, 3.0)], *ST_)

# ---- 2: the front of the rim (in pieces, so the colours can use the same pieces) ----
LEFT, RIGHT = P(X0, TOP), P(X1, TOP)
fpts = [LEFT, spBL, spBR, whBL, whBR, stBL, stBR, RIGHT]
front = [arc_to(RC[0], RC[1], RX, RY, fpts[i], fpts[i + 1], False) for i in range(7)]
front_all = [s for piece in front for s in piece]

# ---- 6: the back of the rim, in four pieces between the handles ----
back = [arc_to(RC[0], RC[1], RX, RY, LEFT, spKL, True), arc_to(RC[0], RC[1], RX, RY, spKR, whKL, True),
        arc_to(RC[0], RC[1], RX, RY, whKR, stKL, True), arc_to(RC[0], RC[1], RX, RY, stKR, RIGHT, True)]

# colour areas
inside = [back[0] + [Seg(spKL, spBL)] + rev(front[0]),
          back[1] + [Seg(whKL, whBL)] + rev(front[2]) + [Seg(spBR, spKR)],
          back[2] + [Seg(stKL, stBL)] + rev(front[4]) + [Seg(whBR, whKR)],
          back[3] + rev(front[6]) + [Seg(stBR, stKR)]]
sp_handle = [Seg(spBL, spEL)] + rev(sp_small) + [Seg(spER, spBR)] + rev(front[1])
wh_handle = [Seg(whBL, whEL), wh_top, Seg(whER, whBR)] + rev(front[3])
st_handle = [Seg(stBL, stEL), st_mid.rev(), Seg(stER, stBR)] + rev(front[5])

steps = [
    step('Start with a U', 'Draw a big capital U: straight down, round the bottom and straight back up. This U is hiding in the pot.',
         [line(*U_)]),
    step('The front of the rim', 'Join the two tops of the U with a curved line that dips down a little in the middle.',
         [line(*front_all)]),
    step('A spoon', 'Draw a handle standing on the curved line and leaning to the left. Put a round head on top, with four dots for holes.',
         [line(Seg(spBL, spEL)), line(Seg(spBR, spER)), ring(*(sp_big + sp_small))] + [dot(x, y) for x, y in sp_dots]),
    step('A whisk', 'Draw a straight handle in the middle. On top draw a tall balloon shape, with a line down the middle and a curved line each side.',
         [line(Seg(whBL, whEL)), line(Seg(whBR, whER)), line(wh_top), line(*outer), line(mid), line(*innL), line(*innR)]),
    step('A spatula', 'Draw a handle leaning to the right. Put a box with round corners on top. Draw three lines inside the box.',
         [line(Seg(stBL, stEL)), line(Seg(stBR, stER)), ring(*st_head)] + [line(s) for s in st_slots]),
    step('The back of the rim', 'Draw little curved lines between the handles, from one top of the U to the other. They make the back of the rim.',
         [line(*b) for b in back]),
    step('Colour the pot', 'Colour the pot light blue, up to the front of the rim.',
         [fill(FILL['lblue'], *(U_ + rev(front_all)))], use='lblue'),
    step('Colour inside', 'Colour the inside of the pot blue: the little spaces between the handles.',
         [fill(FILL['blue'], *r) for r in inside], use='blue'),
    step('Colour the spoon', 'Colour the spoon light brown, the head and the handle.',
         [fill(FILL['lbrown'], *(sp_big + sp_small)), fill(FILL['lbrown'], *sp_handle)], use='lbrown'),
    step('Colour grey', 'Colour the handle of the whisk grey. Colour the top of the spatula grey too.',
         [fill(FILL['grey'], *wh_handle), fill(FILL['grey'], *st_head)], use='grey'),
    step('Colour red', 'Colour the handle of the spatula red.',
         [fill(FILL['red'], *st_handle)], use='red'),
]

D = drawing('dx_utensils_u', 'U is for Utensils', 4, 20, 'things', ['Letters', 'Around the house'],
            'A pot of kitchen utensils: a spoon with holes, a whisk and a spatula. The capital U is hiding in it: the U is the sides and bottom of the pot.',
            steps, ['lblue', 'blue', 'lbrown', 'grey', 'red'])
json.dump(D, open(os.path.join(OUT, 'utensils.json'), 'w'))
json.dump({'set': 'house-AZ', 'slot': 'U', 'kind': 'key', 'age_from': 6}, open(os.path.join(OUT, 'utensils.place.json'), 'w'))
print('utensils: %d steps' % len(steps))
