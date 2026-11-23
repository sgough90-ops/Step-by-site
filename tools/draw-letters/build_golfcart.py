"""g is for golf cart (dx_golfcart_g), Vehicles a to z, slot g (23 Nov 2026).
From his pick "g1 Blue golf cart" (Claude's second-go sketches, claude/step-by-draw-food-capitals-vehicles-small-14x4.md).

A golf cart facing right. The g is at its nose: the round headlight (the round of the g), the front edge of the cart
(its stick) and the curl under the nose to the wheel arch (its tail). The headlight meets the front edge at two points
and is cut off flat by it, so the two lines do not run along each other. Written in the sketch's numbers.

    python3 build_golfcart.py
"""
from bcommon import *

p = Pic(s=1.0, dx=1.5, dy=5.0)
R, RA, WY = 10, 12.5, 78                                       # wheel, wheel arch, height of the middle of the wheels
YA, YB = WY - 4.25, WY + 2                                     # where the arches start, the bottom edge of the cart
NOSE, HW = 90, 10.5                                            # the g's stick, how wide its tail is
HR = HW / 2
XF, XR = NOSE - HW - RA, 24                                    # the front and the back wheel
BOT = YA + 2 + HR                                              # the bottom of the g's tail
RB = 6.5                                                       # the headlight
CYL = BOT - 13 - RB
TOP = CYL - RB                                                 # the top of the g
DECK, FLOOR, SX = TOP - 3, TOP + 11, XR + 22


def stick(a, b, w):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); r = w / 2; th = math.degrees(math.atan2(dy, dx))
    nx, ny = -dy / L * r, dx / L * r
    p1, p2, p3, p4 = P(a[0] + nx, a[1] + ny), P(b[0] + nx, b[1] + ny), P(b[0] - nx, b[1] - ny), P(a[0] - nx, a[1] - ny)
    return [Seg(p1, p2)] + arc(b[0], b[1], r, r, th + 90, th - 90, start=p2, end=p3) + [Seg(p3, p4)] + arc(a[0], a[1], r, r, th - 90, th - 270, start=p4, end=p1)


# ---- the g ----
G_STICK = [Seg((NOSE, TOP), (NOSE, BOT - HR)),
           Seg((NOSE, BOT - HR), (NOSE, BOT - HR * 0.45), (NOSE - HR * 0.45, BOT), (NOSE - HR, BOT)),
           Seg((NOSE - HR, BOT), (NOSE - HR * 1.55, BOT), (NOSE - HW, BOT - HR * 0.45), (NOSE - HW, BOT - HR)),
           Seg((NOSE - HW, BOT - HR), (NOSE - HW, YA))]
OFF = 5.8                                                      # how far the middle of the headlight is from the front edge
H = math.sqrt(RB * RB - OFF * OFF); ANG = math.degrees(math.atan2(H, OFF))
G_ROUND = arc(NOSE - OFF, CYL, RB, RB, -ANG, -360 + ANG, start=P(NOSE, CYL - H), end=P(NOSE, CYL + H))
# ---- the cart: everything but its front edge ----
BODY = (arc(XF, YA, RA, RA, 0, -180, start=P(NOSE - HW, YA), end=P(XF - RA, YA)) +
        [Seg((XF - RA, YA), (XF - RA, YB)), Seg((XF - RA, YB), (XR + RA, YB)), Seg((XR + RA, YB), (XR + RA, YA))] +
        arc(XR, YA, RA, RA, 0, -180, start=P(XR + RA, YA), end=P(XR - RA, YA)) +
        [Seg((XR - RA, YA), (XR - RA, YB)), Seg((XR - RA, YB), (8, YB)), Seg((8, YB), (8, DECK + 4))] +
        arc(12, DECK + 4, 4, 4, 180, 270, start=P(8, DECK + 4), end=P(12, DECK)) +
        [Seg((12, DECK), (SX, DECK)), Seg((SX, DECK), (SX + 2, FLOOR)), Seg((SX + 2, FLOOR), (XF - 10, FLOOR)),
         Seg((XF - 10, FLOOR), (XF - 4, TOP - 8)), Seg((XF - 4, TOP - 8), (NOSE, TOP))])

p.shape('roof', rrect(XR - 17, 11.5, XF + 13, 17.5, 2.8), step=5)
p.stroke('post0', Seg((XR - 11, 17.5), (XR - 11, DECK)), step=5)
p.stroke('post1', Seg((XF + 8, 17.5), (XF - 4, TOP - 8)), step=5)
p.shape('seatback', rrect(XR - 5, DECK - 22, XR + 2, DECK + 1, 3), step=4)
p.shape('seatbase', rrect(XR - 3, DECK - 6.5, SX + 1, DECK + 1, 3), step=4)
p.stroke('column', Seg((XF - 6, TOP + 1), (XF - 12.5, TOP - 12)), step=4)
p.shape('swheel', stick((XF - 16, TOP - 15), (XF - 9.4, TOP - 9.6), 3.2), step=4)
p.region('bodyR', BODY, G_STICK)
p.stroke('body', BODY, step=3)
for i, x in enumerate((XF, XR)):
    p.shape('tyre%d' % i, circle(x, WY, R), step=2)
    p.shape('hub%d' % i, circle(x, WY, 4.5), step=2)
p.stroke('g_round', G_ROUND, step=1)
p.stroke('g_stick', G_STICK, step=1)
p.build()

steps = [
    step('Start with a g', 'Draw a small letter g: a round shape, then a straight line down its right side that curls under to the left.', p.step(1)),
    step('Two wheels', 'Draw a big circle just to the left of the tail of the g, and another one further along. Draw a small circle inside each one.', p.step(2)),
    step('The cart', 'From the tail of the g go over the front wheel, along, over the back wheel and up the back. Go along the seat, down, along the floor and up to the top of the g.', p.step(3)),
    step('Seat and steering wheel', 'Draw a seat with a tall back. Draw a slanting line up from the front of the cart, with a little sausage shape on top for the steering wheel.', p.step(4)),
    step('The roof', 'Draw a line up from the back of the cart and a slanting line up from the front. Draw a long thin roof across the top of them.', p.step(5)),
    step('Colour blue', 'Colour the cart blue, all round the headlight.', [p.face('blue', (30, 62))], use='blue'),
    step('Colour yellow', 'Colour the headlight in the g yellow. Colour the roof yellow too.', [p.face('yellow', (83.4, 61.5)), p.ring('yellow', 'roof')], use='yellow'),
    step('Colour light brown', 'Colour the seat and its back light brown.', [p.face('lbrown', (22.5, 37)), p.face('lbrown', (36, 49))], use='lbrown'),
    step('Colour black', 'Colour the two tyres black, round the small circles. Colour the steering wheel black.',
         [p.ring('black', 'tyre0', holes=('hub0',)), p.ring('black', 'tyre1', holes=('hub1',)), p.ring('black', 'swheel')], use='black'),
    step('Colour grey', 'Colour the middle of each wheel grey.', [p.ring('grey', 'hub0'), p.ring('grey', 'hub1')], use='grey'),
]
D = drawing('dx_golfcart_g', 'g is for golf cart', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'A blue golf cart with a yellow roof. The small letter g is hiding at the front: the headlight, the front edge and the curl under it.',
            steps, ['blue', 'yellow', 'lbrown', 'black', 'grey'])
ok = finish('golfcart', D, {'set': 'vehicles-az', 'slot': 'g', 'kind': 'drive', 'age_from': 5}, p)
