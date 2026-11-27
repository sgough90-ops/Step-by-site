"""w is for wagon (dx_wagon_w), Vehicles a to z, slot w. Rebuilt from his ChatGPT sheet (15 Nov 2026).
The w is the criss-cross planks on the side of a coal wagon."""
from kit15 import *
import math

BLUE, BLACK, GREY = FILL['blue'], FILL['black'], FILL['grey']

TY, BY = 30, 58
W1, b1, m, b2, W2 = P(22, TY), P(35, BY), P(50, TY), P(65, BY), P(78, TY)
wsegs = poly(W1, b1, m, b2, W2)
topL, topR = Seg(W1, m), Seg(m, W2)
sideL = [Seg(W1, (22, BY)), Seg((22, BY), b1)]
sideR = [Seg(W2, (78, BY)), Seg((78, BY), b2)]
midbot = Seg(b1, b2)

CY2 = 63.2
chassis = [Seg((22, BY), (17.6, BY)), *arc(17.6, (BY + CY2) / 2, 2.6, 2.6, 270, 90, start=P(17.6, BY), end=P(17.6, CY2)),
           Seg((17.6, CY2), (82.4, CY2)), *arc(82.4, (BY + CY2) / 2, 2.6, 2.6, 90, -90, start=P(82.4, CY2), end=P(82.4, BY)), Seg((82.4, BY), (78, BY))]

def wheel(cx, cy=68.2, r=7):
    dx = math.sqrt(r * r - (cy - CY2) ** 2)
    a0 = math.degrees(math.atan2(CY2 - cy, -dx)); a1 = math.degrees(math.atan2(CY2 - cy, dx))
    segs = arc(cx, cy, r, r, a0 % 360, a1, start=P(cx - dx, CY2), end=P(cx + dx, CY2))
    return segs, circle(cx, cy, 2.6)
wL, hubL = wheel(33)
wR, hubR = wheel(67)

bufL = [Seg((22, 47.6), (17.2, 47.6)), *arc(17.2, 49.8, 2.2, 2.2, 270, 90, start=P(17.2, 47.6), end=P(17.2, 52)), Seg((17.2, 52), (22, 52))]
bufR = [Seg((78, 47.6), (82.8, 47.6)), *arc(82.8, 49.8, 2.2, 2.2, -90, 90, start=P(82.8, 47.6), end=P(82.8, 52)), Seg((82.8, 52), (78, 52))]

# coal: a bumpy pile from one top corner to the other
cpts = [W1, P(30, 22.6), P(41, 19.4), P(52, 18.2), P(63, 19.8), P(72, 23.4), W2]
coal = [bump(a, b, 0.42) for a, b in zip(cpts, cpts[1:])]

track = Seg((8, 75.8), (92, 75.8))

steps = [
    step('Start with a w', 'Draw a wide small letter w. Make its three top points the same height.', [line(*wsegs)]),
    step('The top', 'Draw a line across the top of each V.', [line(topL), line(topR)]),
    step('The sides', 'From each top corner draw a line straight down, then along the bottom to the w. Join the two bottom points of the w too.',
         [line(*sideL), line(*sideR), line(midbot)]),
    step('The base', 'Draw a long flat bar under the wagon that sticks out a little at each end.', [line(*chassis)]),
    step('The wheels', 'Draw two wheels peeping out under the bar, with a small circle in each one.', [line(*wL), line(*wR), ring(hubL), ring(hubR)]),
    step('The buffers', 'Draw a little rounded bump sticking out of each side of the wagon.', [line(*bufL), line(*bufR)]),
    step('The coal', 'Draw a bumpy pile of coal on top, from one top corner to the other.', [line(*coal)]),
    step('The track', 'Draw a long line under the wheels for the railway track.', [line(track)]),
]
box = fill(BLUE, topL, topR, sideR[0], sideR[1], midbot.rev(), sideL[1].rev(), sideL[0].rev())
coal_f = fill(BLACK, *coal, topR.rev(), topL.rev())
wfl = fill(BLACK, *wL, Seg(wL[-1].b, wL[0].a), cut=[d_fill(*hubL)])
wfr = fill(BLACK, *wR, Seg(wR[-1].b, wR[0].a), cut=[d_fill(*hubR)])
ch_f = fill(GREY, *chassis, sideR[1], midbot.rev(), sideL[1].rev())
steps += [
    step('Colour blue', 'Colour the wagon blue.', [box], use='blue'),
    step('Colour black', 'Colour the coal and the wheels black.', [coal_f, wfl, wfr], use='black'),
    step('Colour grey', 'Colour the base, the buffers and the middles of the wheels grey.',
         [ch_f, fill(GREY, *bufL, Seg((22, 52), (22, 47.6))), fill(GREY, *bufR, Seg((78, 52), (78, 47.6))), fill(GREY, *hubL), fill(GREY, *hubR)], use='grey'),
]
P_ = drawing('dx_wagon_w', 'w is for wagon', 2, 10, 'vehicles', ['Letters', 'Vehicles'],
             'A blue railway wagon full of coal, on its track. The small letter w is hiding in it: it is the criss-cross planks on the side of the wagon.',
             steps, ['blue', 'black', 'grey'])
scale(P_, 1.1, 50, 47)
move(P_, 0, 4)
save('wagon', P_, {'set': 'vehicles-az', 'slot': 'w', 'kind': 'drive', 'age_from': 5})
