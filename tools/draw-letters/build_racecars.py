"""The race car numbers for Vehicles 1 to 9 (19 Nov 2026): 1, 2, 3, 4, 5, 6, 7 and 9 so far (3 added 23 Nov 2026).

    python3 build_racecars.py        (writes out/<name>.json and out/<name>.place.json)

Each is built from Claude's sketch that he picked (Race car numbers, rounds 2 and 3), moved onto the app's paper
with carkit.T. Step 1 is always the whole number, written the normal way.
"""
import json, os, math
from kit import *
from carkit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
os.makedirs(OUT, exist_ok=True)
TAGS = ['Numbers', 'Vehicles']


def save(name, D, slot, white=None):
    json.dump(D, open(os.path.join(OUT, name + '.json'), 'w'))
    json.dump({'set': 'vehicles-09', 'slot': slot, 'kind': 'drive', 'age_from': 5}, open(os.path.join(OUT, name + '.place.json'), 'w'))
    if white: json.dump(white, open(os.path.join(OUT, name + '.white.json'), 'w'))
    print('%s: %d steps, %d bytes' % (name, len(D['steps']), len(json.dumps(D, separators=(',', ':')))))


# ------------------------------------------------------------------ 1 is for Race car (the hump)
def car1():
    one = Lp((88, 78), (98, 62), (98, 114))                       # flick, then the straight line down
    rear, front = Wheel(42, 154, 26), Wheel(160, 158, 22)
    rL, rR = rear.at_y(140); fL, fR = front.at_y(140)
    dome = Dome(114, 105, 11, 114)
    a = pts_line(T(98, 114), dome.pL, dome.pR, T(126, 114), T(132, 106), T(186, 128)) + \
        [C((186, 128), (194, 131), (196, 138), (188, 140)), Seg(T(188, 140), fR)]
    b = [Seg(fL, rR)]
    c = [Seg(rL, T(14, 140))] + Lp((14, 140), (12, 124), (14, 108), (88, 78))
    wing = rrect(tx(4), ty(70), tx(38), ty(80), 3 * S)
    post = Seg(T(22, 80), T(22, 104.757))
    stripe = rrect(tx(72), ty(121), tx(132), ty(129), 3 * S)
    body = one + a + front.over_top(fR, fL) + b + rear.over_top(rR, rL) + c
    steps = [
        step('Start with a 1', 'Draw a number 1: a short slanting line going up, then a long straight line down. No line along the bottom. This 1 is hiding in the race car.',
             [line(*one)]),
        step('Two wheels', 'Draw a big wheel under the left of the 1 and a smaller one on the right. Draw a small circle in the middle of each.',
             rear.lines() + front.lines()),
        step('The car', 'From the bottom of the 1, go along, over the nose and under to the front wheel. Join the wheels. Go round the back to the top of the 1.',
             [line(*a), line(*b), line(*c)]),
        step('The wing', 'Draw a wing at the back: a long thin box with round corners, on a stick that stands on the car.',
             [ring(*wing), line(post)]),
        step('The driver', 'Draw the round top of a helmet sitting on the car, in front of the 1. Draw the visor inside it.',
             dome.lines()),
        step('A stripe', 'Draw a long thin stripe with round ends along the side of the car.',
             [ring(*stripe)]),
        step('The road', 'Draw a long line under the wheels for the road.', [road()]),
        step('Colour red', 'Colour the car red, round the stripe. Colour the wing red too.',
             [fill(FILL['red'], *body, cut=[d_fill(*stripe)]), fill(FILL['red'], *wing)], use='red'),
        step('Colour yellow', 'Colour the stripe yellow. Colour the helmet yellow too, round the visor.',
             [fill(FILL['yellow'], *stripe), dome.yellow()], use='yellow'),
        step('Colour the visor', 'Colour the visor light blue.', [dome.blue()], use='lblue'),
        step('Colour the tyres', 'Colour the two tyres black, round their middles.', [rear.black(), front.black()], use='black'),
        step('Colour grey', 'Colour the middles of the wheels grey.', [rear.grey(), front.grey()], use='grey'),
    ]
    D = drawing('dx_racecar_1', '1 is for Race car', 2, 12, 'vehicles', TAGS,
                'A red race car with a wing at the back. The number 1 is hiding in it: it is the hump behind the driver, and its little flick is the top of the hump.',
                steps, ['red', 'yellow', 'lblue', 'black', 'grey'])
    save('car1', D, '1')


# ------------------------------------------------------------------ 2 is for Racing car (2a, the curved wing)
def car2():
    hook = [C((8, 62), (8, 46), (20, 40), (30, 40)), C((30, 40), (42, 40), (50, 50), (44, 60))]
    slope_a, slope_b = Seg(T(44, 60), T(14, 112)).split(0.11538)     # the slope, cut where the wing joins it
    base = Seg(T(14, 112), T(60, 112))
    two = hook + [slope_a, slope_b, base]
    under = q2c((40.538, 66), (24, 60), (8, 62))                      # the underside of the wing
    under = Seg(slope_a.b, under.p[1], under.p[2], two[0].a)          # ends exactly on the 2
    rear, front = Wheel(44, 154, 26), Wheel(160, 158, 22)
    rL, rR = rear.at_y(140); fL, fR = front.at_y(140)
    dome = Dome(117, 103, 11, 112)
    a = pts_line(T(60, 112), T(100, 100), T(104, 112), dome.pL, dome.pR, T(130, 112), T(136, 104), T(190, 128)) + \
        [C((190, 128), (196, 131), (197, 138), (190, 140)), Seg(T(190, 140), fR)]
    b = [Seg(fL, rR)]
    c = [Seg(rL, T(14, 140))] + Lp((14, 140), (12, 128), (14, 112))
    stripe = rrect(tx(70), ty(124), tx(132), ty(131), 3 * S)
    body = [base] + a + front.over_top(fR, fL) + b + rear.over_top(rR, rL) + c
    wing = hook + [slope_a, under]
    steps = [
        step('Start with a 2', 'Draw a number 2: a curve over the top, a long slanting line down and a straight line along the bottom. This 2 is hiding in the car.',
             [line(*two)]),
        step('The wing', 'Draw a curved line under the top of the 2, from its slanting line back to where the 2 began. Now the top of the 2 is a curved wing.',
             [line(under)]),
        step('Two wheels', 'Draw a big wheel under the bottom of the 2 and a smaller one further along. Draw a small circle in the middle of each.',
             rear.lines() + front.lines()),
        step('The car', 'From the end of the 2, go up and along, over the nose and under to the front wheel. Join the wheels. Go round the back to the 2.',
             [line(*a), line(*b), line(*c)]),
        step('The driver', 'Draw the round top of a helmet sitting in the car. Draw the visor inside it.', dome.lines()),
        step('A stripe', 'Draw a long thin stripe with round ends along the side of the car.', [ring(*stripe)]),
        step('The road', 'Draw a long line under the wheels for the road.', [road()]),
        step('Colour red', 'Colour the car red, round the stripe.', [fill(FILL['red'], *body, cut=[d_fill(*stripe)])], use='red'),
        step('Colour yellow', 'Colour the wing and the stripe yellow. Colour the helmet yellow too, round the visor.',
             [fill(FILL['yellow'], *wing), fill(FILL['yellow'], *stripe), dome.yellow()], use='yellow'),
        step('Colour the visor', 'Colour the visor light blue.', [dome.blue()], use='lblue'),
        step('Colour the tyres', 'Colour the two tyres black, round their middles.', [rear.black(), front.black()], use='black'),
        step('Colour grey', 'Colour the middles of the wheels grey.', [rear.grey(), front.grey()], use='grey'),
    ]
    D = drawing('dx_racingcar_2', '2 is for Racing car', 2, 12, 'vehicles', TAGS,
                'A red racing car with a big curved wing. The number 2 is hiding in it: its curve is the wing, its slanting line holds the wing up, and its bottom line is the top of the back of the car.',
                steps, ['red', 'yellow', 'lblue', 'black', 'grey'])
    save('car2', D, '2')


# ------------------------------------------------------------------ 5 is for Dragster (5b, the burnout)
def car5():
    cx, cy, R = tx(44), ty(148), r2(32 * S)
    P11 = on_circle(cx, cy, R, -120); P7 = on_circle(cx, cy, R, 120)
    hatR = T(70, 100.287); hatL = P(P11[0], hatR[1])
    stem_top, stem_bot = Seg(hatL, P(P11[0], ty(106))), Seg(P(P11[0], ty(106)), P11)
    belly = arc(cx, cy, R, R, -120, 120, start=P11, end=P7)
    five = [Seg(hatR, hatL), stem_top, stem_bot] + belly
    under = Seg(stem_top.b, T(40, 106.5), T(58, 104), hatR)            # the underside of the wing
    # smoke: a puffy cloud from one end of the curve, round the back of the wheel, to the other end
    def bump(p, q, h):
        """A round bump from p to q, bulging h to the left of the way it goes."""
        dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy); nx, ny = dy / L, -dx / L
        return Seg(p, (p[0] + dx * .1 + nx * h * 1.33, p[1] + dy * .1 + ny * h * 1.33),
                   (p[0] + dx * .9 + nx * h * 1.33, p[1] + dy * .9 + ny * h * 1.33), q)
    V = [P11, T(13, 127), T(6, 146), T(11, 164), P7]
    hs = [-3.4, -3.6, -3.6, -3.2]          # negative: bulge outwards, away from the wheel
    puff = [bump(V[i], V[i + 1], hs[i]) for i in range(4)]
    inner = Seg(P7, T(31.5, 161), T(31.5, 135), P11)                    # the cloud's edge on the wheel
    smoke = puff + [inner]
    hub = circle(cx, cy, r2(10 * S))
    tyre_out = belly + [inner]
    small = Wheel(182, 168, 12)
    dome = Dome(88, 115, 11, 124)
    top_front, bot_back = circle_at_y(cx, cy, R, ty(124))[1], circle_at_y(cx, cy, R, ty(142))[1]
    body_l = [Seg(top_front, dome.pL), Seg(dome.pL, dome.pR), Seg(dome.pR, T(100, 124)), Seg(T(100, 124), T(190, 134)),
              C((190, 134), (196, 135.5), (198, 139), (192, 142)), Seg(T(192, 142), bot_back)]
    strut = Seg(T(182, 142), P(tx(182), small.c[1] - small.r))
    stripe = rrect(tx(104), ty(133), tx(148), ty(138), 2.5 * S)
    body = body_l + arc_between(cx, cy, R, bot_back, top_front, cw=False)
    wing = [Seg(hatR, hatL), stem_top, under]
    steps = [
        step('Start with a 5', 'Draw a number 5: a flat line at the top, a short line down, then a big round curve. The curve goes nearly all the way round.',
             [line(*five)]),
        step('The wing', 'Draw a line under the flat top of the 5, from the short line to the front tip. Now the flat top is a wing.',
             [line(under)]),
        step('Smoke', 'Draw a puffy cloud of smoke behind the wheel. It goes from one end of the round curve to the other.',
             [ring(*smoke)]),
        step('The wheel', 'The round curve is a giant back wheel. Draw a circle in the middle of it.', [ring(*hub)]),
        step('The dragster', 'From the front of the wheel, draw a long thin body with a pointy nose. Come back along the bottom to the wheel.',
             [line(*body_l)]),
        step('The driver', 'Draw the round top of a helmet sitting on the dragster. Draw the visor inside it.', dome.lines()),
        step('The front wheel', 'Draw a short line down from the nose and a small wheel on the end of it. Draw a small circle in its middle.',
             [line(strut)] + small.lines()),
        step('A stripe', 'Draw a long thin stripe with round ends along the side.', [ring(*stripe)]),
        step('The road', 'Draw a long line under the wheels for the road.', [road()]),
        step('Colour orange', 'Colour the dragster orange, round the stripe.', [fill(FILL['orange'], *body, cut=[d_fill(*stripe)])], use='orange'),
        step('Colour yellow', 'Colour the wing and the stripe yellow. Colour the helmet yellow too, round the visor.',
             [fill(FILL['yellow'], *wing), fill(FILL['yellow'], *stripe), dome.yellow()], use='yellow'),
        step('Colour the visor', 'Colour the visor light blue.', [dome.blue()], use='lblue'),
        step('Colour the tyres', 'Colour the giant tyre black, up to the smoke and round its middle. Colour the small tyre black too.',
             [fill(FILL['black'], *tyre_out, cut=[d_fill(*hub)]), small.black()], use='black'),
        step('Colour grey', 'Colour the middles of the wheels grey. Leave the smoke white.',
             [fill(FILL['grey'], *hub), small.grey()], use='grey'),
    ]
    D = drawing('dx_dragster_5', '5 is for Dragster', 3, 15, 'vehicles', TAGS,
                'A dragster with a giant back wheel, doing a burnout in a puff of smoke. The number 5 is hiding in it: its flat top is the wing, its short line is the wing post and its curve is the giant wheel.',
                steps, ['orange', 'yellow', 'lblue', 'black', 'grey'])
    save('car5', D, '5')


# ------------------------------------------------------------------ 6 is for Racer (6a, the back wheel)
def car6():
    rear, front = Wheel(44, 154, 26), Wheel(160, 158, 22)
    left = P(rear.c[0] - rear.r, rear.c[1])
    stem = [C((84, 92), (60, 90), (20, 104), (19, 130)), Seg(T(19, 130), T(18, 142), T(18, 150), left)]
    loop = arc(rear.c[0], rear.c[1], rear.r, rear.r, 180, -180, start=left, end=left)
    six = stem + loop
    hump = [q2c((84, 92), (90, 82), (98, 82)), Seg(T(98, 82), T(104, 112))]
    rL, rR = rear.at_y(140); fL, fR = front.at_y(140)
    dome = Dome(117, 103, 11, 112)
    a = pts_line(T(104, 112), dome.pL, dome.pR, T(130, 112), T(136, 104), T(190, 128)) + \
        [C((190, 128), (196, 131), (197, 138), (190, 140)), Seg(T(190, 140), fR)]
    b = [Seg(fL, rR)]
    stripe = rrect(tx(76), ty(124), tx(140), ty(131), 3 * S)
    body = stem + arc_between(rear.c[0], rear.c[1], rear.r, left, rR, cw=True) + rev(b) + \
        arc_between(front.c[0], front.c[1], front.r, fL, fR, cw=True) + rev(a) + rev(hump)
    steps = [
        step('Start with a 6', 'Draw a number 6: a long curvy line coming down, then a big round loop at the bottom. The loop is the back wheel.',
             [line(*six)]),
        step('The hump', 'From the top of the 6, draw a little hump going up and over. Then come down in a straight line.',
             [line(*hump)]),
        step('The wheels', 'Draw a smaller wheel further along. Then draw a small circle in the middle of each wheel.',
             [ring(*front.tyre), ring(*rear.hub), ring(*front.hub)]),
        step('The car', 'From the bottom of the hump, go along, over the nose and under to the front wheel. Then join the front wheel to the back wheel.',
             [line(*a), line(*b)]),
        step('The driver', 'Draw the round top of a helmet sitting in the car, in front of the hump. Draw the visor inside it.', dome.lines()),
        step('A stripe', 'Draw a long thin stripe with round ends along the side of the car.', [ring(*stripe)]),
        step('The road', 'Draw a long line under the wheels for the road.', [road()]),
        step('Colour red', 'Colour the car red, round the stripe.', [fill(FILL['red'], *body, cut=[d_fill(*stripe)])], use='red'),
        step('Colour yellow', 'Colour the stripe yellow. Colour the helmet yellow too, round the visor.',
             [fill(FILL['yellow'], *stripe), dome.yellow()], use='yellow'),
        step('Colour the visor', 'Colour the visor light blue.', [dome.blue()], use='lblue'),
        step('Colour the tyres', 'Colour the two tyres black, round their middles.', [rear.black(), front.black()], use='black'),
        step('Colour grey', 'Colour the middles of the wheels grey.', [rear.grey(), front.grey()], use='grey'),
    ]
    D = drawing('dx_racer_6', '6 is for Racer', 2, 12, 'vehicles', TAGS,
                'A red racer with a hump behind the driver. The number 6 is hiding in it: its curvy line is the back of the car and its loop is the back wheel.',
                steps, ['red', 'yellow', 'lblue', 'black', 'grey'])
    save('car6', D, '6')


# ------------------------------------------------------------------ 7 is for Speedster (7b, long and low)
def car7():
    top_at = lambda x: 118 - (x - 12) * 18 / 88                         # the top of the car, back part
    end7 = T(26, top_at(26))
    seven = [Seg(T(6, 74), T(46, 74)), Seg(T(46, 74), end7)]
    rear, front = Wheel(42, 158, 22), Wheel(168, 160, 20)
    rL, rR = rear.at_y(150); fL, fR = front.at_y(150)
    dome = Dome(122, 107, 10, 116)
    a = [Seg(end7, T(100, 100))] + pts_line(T(100, 100), T(104, 116), dome.pL, dome.pR, T(140, 116), T(194, 136)) + \
        [C((194, 136), (199, 138.5), (200, 146), (192, 150)), Seg(T(192, 150), fR)]
    b = [Seg(fL, rR)]
    c = [Seg(end7, T(12, 118))] + Lp((12, 118), (10, 132), (12, 150)) + [Seg(T(12, 150), rL)]
    back = Seg(T(6, 74), T(12, 118))
    slot1 = circle(tx(20.4), ty(84.25), 9.6 * S, ry=3 * S, start_deg=180)
    slot2 = circle(tx(20.3), ty(95.3), 8 * S, ry=2.5 * S, start_deg=180)
    stripe = rrect(tx(70), ty(129), tx(130), ty(136), 3 * S)
    body = a + arc_between(front.c[0], front.c[1], front.r, fR, fL, cw=False) + b + \
        arc_between(rear.c[0], rear.c[1], rear.r, rR, rL, cw=False) + rev(c)
    plate = seven + [c[0], back.rev()]
    steps = [
        step('Start with a 7', 'Draw a number 7: a flat line along the top, then a long slanting line going down. This 7 is hiding in the car.',
             [line(*seven)]),
        step('Two wheels', 'Draw a wheel under the bottom of the 7 and another far along. Draw a small circle in the middle of each.',
             rear.lines() + front.lines()),
        step('The car', 'From the bottom of the 7, go along the long low car, over the nose and under to the front wheel. Join the wheels. Go round the back to the 7.',
             [line(*a), line(*b), line(*c)]),
        step('The wing', 'Draw a sloping line from the start of the 7 down to the back of the car. Then draw two flat ovals inside.',
             [line(back), ring(*slot1), ring(*slot2)]),
        step('The driver', 'Draw the round top of a helmet sitting in the car. Draw the visor inside it.', dome.lines()),
        step('A stripe', 'Draw a long thin stripe with round ends along the side of the car.', [ring(*stripe)]),
        step('The road', 'Draw a long line under the wheels for the road.', [road()]),
        step('Colour blue', 'Colour the car blue, round the stripe.', [fill(FILL['blue'], *body, cut=[d_fill(*stripe)])], use='blue'),
        step('Colour yellow', 'Colour the wing yellow, round the two ovals. Colour the stripe and the helmet yellow too.',
             [fill(FILL['yellow'], *plate, cut=[d_fill(*slot1), d_fill(*slot2)]), fill(FILL['yellow'], *stripe), dome.yellow()], use='yellow'),
        step('Colour black', 'Colour the two ovals black. Colour the two tyres black too, round their middles.',
             [fill(FILL['black'], *slot1), fill(FILL['black'], *slot2), rear.black(), front.black()], use='black'),
        step('Colour the visor', 'Colour the visor light blue.', [dome.blue()], use='lblue'),
        step('Colour grey', 'Colour the middles of the wheels grey.', [rear.grey(), front.grey()], use='grey'),
    ]
    D = drawing('dx_speedster_7', '7 is for Speedster', 2, 12, 'vehicles', TAGS,
                'A long, low blue speedster with a big wing at the back. The number 7 is hiding in it: its flat line is the top of the wing and its slanting line is the front of the wing.',
                steps, ['blue', 'yellow', 'black', 'lblue', 'grey'])
    save('car7', D, '7')


# ------------------------------------------------------------------ 9 is for Old racer (9c, facing left, the door)
def car9():
    hx, hy, hr = 86, 99.5, 10
    H = (tx(hx), ty(hy)); R9 = r2(hr * S)
    loop = circle(H[0], H[1], R9, start_deg=0)
    top9 = loop[0].a
    stick_a = Seg(top9, P(top9[0], ty(112))); stick_b = Seg(stick_a.b, P(top9[0], ty(140)))
    nine = loop + [stick_a, stick_b]
    rear, front = Wheel(156, 156, 24, hub=0.3), Wheel(40, 156, 24, hub=0.3)   # rear on the right: the car faces left
    fL, fR = front.at_y(140); rL, rR = rear.at_y(140)
    two = on_circle(H[0], H[1], R9, -30)                                # where the back of the car meets the helmet
    a = [Seg(stick_a.b, T(70, 112)), Seg(T(70, 112), T(64, 104)), Seg(T(64, 104), T(24, 108)),
         C((24, 108), (10, 110), (4, 120), (6, 130)), C((6, 130), (8, 138), (10, 140), (12, 140)), Seg(T(12, 140), fL)]
    b = [Seg(fR, rL)]
    c = [Seg(rR, T(184, 140)), q2c((184, 140), (196, 128), (184, 114)), Seg(T(184, 114), two)]
    door = Seg(T(74, 112), T(74, 140))
    handle = dot(tx(84), ty(121))
    bonnet = [Seg(T(x, 113), T(x, 130)) for x in (34, 42, 50)]
    vis = visor(hx, hy, hr, left=True, k=0.82)
    body = [stick_a] + a + arc_between(front.c[0], front.c[1], front.r, fL, fR, cw=True) + b + \
        arc_between(rear.c[0], rear.c[1], rear.r, rL, rR, cw=True) + c + arc_between(H[0], H[1], R9, two, top9, cw=True)
    steps = [
        step('Start with a 9', 'Draw a number 9: a round circle, then a long straight line down from its right side. This 9 is hiding in the car.',
             [line(*nine)]),
        step('Two wheels', 'Draw a big wheel on each side of the 9\'s line, lower down. Draw a small circle in the middle of each.',
             front.lines() + rear.lines()),
        step('The car', 'The car faces this way. From the 9\'s line, go along, over the bonnet and the nose, and under to the wheel. Join the wheels. Go round the back to the circle.',
             [line(*a), line(*b), line(*c)]),
        step('The door', 'The 9\'s straight line is the back of the door. Draw the front of the door: a line down from the top of the car to the bottom. Add a dot for the handle.',
             [line(door), handle]),
        step('The bonnet', 'Draw three short lines on the bonnet, in front of the door.', [line(s) for s in bonnet]),
        step('The visor', 'The circle of the 9 is the driver\'s helmet. Draw the visor inside it, on the side the car is facing.', [ring(*vis)]),
        step('The road', 'Draw a long line under the wheels for the road.', [road()]),
        step('Colour orange', 'Colour the car orange, door and all.', [fill(FILL['orange'], *body)], use='orange'),
        step('Colour the helmet', 'Colour the helmet yellow, round the visor.', [fill(FILL['yellow'], *loop, cut=[d_fill(*vis)])], use='yellow'),
        step('Colour the visor', 'Colour the visor light blue.', [fill(FILL['lblue'], *vis)], use='lblue'),
        step('Colour the tyres', 'Colour the two tyres black, round their middles.', [front.black(), rear.black()], use='black'),
        step('Colour grey', 'Colour the middles of the wheels grey.', [front.grey(), rear.grey()], use='grey'),
    ]
    D = drawing('dx_oldracer_9', '9 is for Old racer', 2, 12, 'vehicles', TAGS,
                'An old-style orange racing car with a door. The number 9 is hiding in it: its circle is the driver\'s helmet and its straight line is the back edge of the door.',
                steps, ['orange', 'yellow', 'lblue', 'black', 'grey'])
    save('car9', D, '9')


# ------------------------------------------------------------------ 4 is for Jet car (4b Long and low, facing left, the canopy roof)
def car4():
    # the 4 is the closed kind: slanting line from the top down to the left, flat line across, then the straight line down.
    # Step 1 keeps its flat line a natural length; the roof step carries it on to the back of the roof.
    top4, low4, bar_end, roof_end = T(100, 82), T(76, 116), T(110, 116), T(128, 116)
    slant, bar, stick = Seg(top4, low4), Seg(low4, bar_end), Seg(top4, T(100, 136))
    bar_more = Seg(bar_end, roof_end)
    roof = C((100, 82), (115.4, 82), (128, 97.3), (128, 116))          # the curved see-through roof, like a fighter jet's
    rear, front = Wheel(158, 158, 22), Wheel(32, 160, 20)              # rear on the right: the car faces left
    rL, rR = rear.at_y(150); fL, fR = front.at_y(150)
    a = Lp((128, 116), (150, 106), (188, 116), (190, 132), (188, 150)) + [Seg(T(188, 150), rR)]
    b = [Seg(rL, fR)]
    c = [Seg(fL, T(6, 150)), q2c((6, 150), (0, 145), (4, 138)), Seg(T(4, 138), low4)]
    wing = rrect(tx(158), ty(90), tx(194), ty(98), 3 * S)
    post = Seg(T(176, 98), T(176, 106 + (176 - 150) * 10 / 38))      # down to the top of the car
    dome = Dome(115, 108.5, 8.5, 116)                                   # the helmet top sits on the 4's flat line, under the roof
    dome.vis = visor(115, 108.5, 8.5, left=True, k=0.9)                 # visor on the side the car faces
    assert dome.pL[0] > bar_end[0] + 0.3
    bm1, bm2, bm3 = Seg(bar_end, dome.pL), Seg(dome.pL, dome.pR), Seg(dome.pR, roof_end)   # the flat line carried on, split at the helmet
    stripe = rrect(tx(106), ty(128), tx(146), ty(135), 3 * S)
    body = [bar, bm1, bm2, bm3] + a + rear.over_top(rR, rL) + b + front.over_top(fR, fL) + c
    glass = [slant, bar, bm1] + dome.arc + [bm3, roof.rev()]
    steps = [
        step('Start with a 4', 'Draw a number 4: a slanting line down, a flat line across, then a straight line down from the top. This 4 is hiding in the car.',
             [line(slant, bar), line(stick)]),
        step('The roof', 'From the top of the 4, draw a curved roof going down at the back. Then draw a flat line from its end back to the 4.',
             [line(roof, bm3.rev(), bm2.rev(), bm1.rev())]),
        step('Two wheels', 'Draw a wheel low down on each side of the 4, the back one a bit bigger. Draw a small circle in the middle of each.',
             front.lines() + rear.lines()),
        step('The car', 'The car faces this way. From the end of the roof, go over the back of the car and down to the wheel. Join the wheels. Go round the nose and up to the 4.',
             [line(*a), line(*b), line(*c)]),
        step('The wing', 'Draw a long flat wing with round ends above the back of the car. Join it to the car with a short straight line.',
             [ring(*wing), line(post)]),
        step('The driver', 'Under the roof, draw the round top of a helmet sitting on the flat line. Draw the visor inside it, on the side the car is facing.',
             dome.lines()),
        step('A stripe', 'Draw a long thin stripe with round ends along the side of the car.', [ring(*stripe)]),
        step('The road', 'Draw a long line under the wheels for the road.', [road()]),
        step('Colour blue', 'Colour the car and the wing blue, round the stripe. The stripe stays white.',
             [fill(FILL['blue'], *body, cut=[d_fill(*stripe)]), fill(FILL['blue'], *wing)], use='blue'),
        step('Colour the helmet', 'Colour the helmet yellow, round the visor.', [dome.yellow()], use='yellow'),
        step('Colour the glass', 'Colour the roof light blue on both sides of the 4\'s straight line, round the helmet. Colour the visor light blue too.',
             [fill(FILL['lblue'], *glass), dome.blue()], use='lblue'),
        step('Colour the tyres', 'Colour the two tyres black, round their middles.', [front.black(), rear.black()], use='black'),
        step('Colour grey', 'Colour the middles of the wheels grey.', [front.grey(), rear.grey()], use='grey'),
    ]
    D = drawing('dx_jetcar_4', '4 is for Jet car', 2, 13, 'vehicles', TAGS,
                'A long, low blue jet car with a curved see-through roof, like a fighter jet. The number 4 is hiding in it: its slanting line is the front of the windscreen, its straight line is the roof frame and its flat line is the top of the car.',
                steps, ['blue', 'yellow', 'lblue', 'black', 'grey'])
    save('car4', D, '4', white=[d_fill(*stripe)])


# ------------------------------------------------------------------ 3 is for Rocket car (23 Nov 2026, facing left)
def car3():
    # From his own picture (a white race car with two jets on its flat back, and a 3 he drew over them) and his pick,
    # sketch 1 "Like your drawing". The 3 is the two rockets and their fire: along the top of the top rocket, round its
    # fire, back to a point between the two, round the bottom fire and under the bottom rocket.
    XB, DECK, FLOOR = 143, 123.4, 173                                   # the flat back of the car, the top of the boot, the floor
    top = C((XB, 127.4), (XB + 30, 127.4), (XB + 30, 140), (XB + 5, 148))          # top bump, down to the point
    bot = C((XB + 5, 148), (XB + 33, 156), (XB + 33, 170), (XB, 170))              # bottom bump
    rim_x = tx(XB + 13.5)                                               # where the rockets stop and the fire starts

    def cut(seg, ts):
        """Cut one piece at several places (ts going up); the pieces share their cut points exactly."""
        out, rest, done = [], seg, 0.0
        for t in ts:
            a, rest = rest.split((t - done) / (1 - done)); out.append(a); done = t
        return out + [rest]

    def quad(p0, c, p1):
        """A quadratic curve (points already on the paper) as one cubic piece."""
        p0, p1 = P(*p0), P(*p1)
        return Seg(p0, (p0[0] + 2 / 3 * (c[0] - p0[0]), p0[1] + 2 / 3 * (c[1] - p0[1])), (p1[0] + 2 / 3 * (c[0] - p1[0]), p1[1] + 2 / 3 * (c[1] - p1[1])), p1)

    # each bump is cut where other lines meet it: the rocket's end line (twice) and the two ends of the flames
    T5 = cut(top, [seg_line_cross_x(top, rim_x, 0, .45), 0.3, 0.7, seg_line_cross_x(top, rim_x, .55, 1)])
    B5 = cut(bot, [seg_line_cross_x(bot, rim_x, 0, .45), 0.3, 0.7, seg_line_cross_x(bot, rim_x, .55, 1)])
    three = T5 + B5
    s3, e3 = three[0].a, three[-1].b                                    # its two ends, on the back of the car
    rim_t, rim_b = Seg(T5[0].b, T5[3].b), Seg(B5[0].b, B5[3].b)

    def flames(bump, pieces, h, L=23 * S):
        """Three pointed flames behind the round end of a bump, from one cut on the bump to the other."""
        xe, c = max((bump.at(i / 400) for i in range(401)), key=lambda q: q[0])
        a, b = pieces[1].b, pieces[2].b
        pts = [a, (xe + .1 * L, c - .5 * h), (xe + .5 * L, c - .4 * h), (xe + .24 * L, c - .22 * h), (xe + .22 * L, c - .14 * h),
               (xe + .6 * L, c - .17 * h), (xe + L, c), (xe + .6 * L, c + .17 * h), (xe + .22 * L, c + .14 * h),
               (xe + .24 * L, c + .22 * h), (xe + .5 * L, c + .4 * h), (xe + .1 * L, c + .5 * h), b]
        return [quad(pts[i], pts[i + 1], pts[i + 2]) for i in range(0, 12, 2)]

    fl_t, fl_b = flames(top, T5, (148 - 127.4) * S), flames(bot, B5, (170 - 148) * S)
    front, rear = Wheel(38, 164, 16, hub=0.52), Wheel(XB - 27, 164, 16, hub=0.52)   # rear on the right: the car faces left
    fL, fR = front.at_y(FLOOR); rL, rR = rear.at_y(FLOOR)
    post1, post2 = (138.5, DECK), (122.4, 121.53)                       # where the wing's two posts stand on the car
    corner = quad(T(3, 168), (tx(3), ty(FLOOR)), T(8.5, FLOOR))
    # the car: from the back wheel, up the flat back (through both ends of the 3), over the roof, round the nose to the front wheel
    body = [Seg(rR, T(XB, FLOOR)), Seg(T(XB, FLOOR), e3), Seg(e3, s3), Seg(s3, T(XB, DECK))] + \
        Lp((XB, DECK), post1, (128, DECK), post2, (113, 118.4)) + \
        [C((113, 118.4), (103, 113.4), (81, 114.4), (73.5, 119.6))] + Lp((73.5, 119.6), (56, 135.4), (24, 139.5)) + \
        [C((24, 139.5), (12, 143.5), (4, 156), (3, 164)), Seg(T(3, 164), T(3, 168)), corner, Seg(corner.b, fL)]
    under = Seg(fR, rL)
    back = body[2]                                                      # the bit of the back between the ends of the 3
    shut = lambda *pts: poly(*[T(*q) for q in pts], closed=True)
    win1 = shut((66.3, 132), (77.6, 122.2), (96.6, 121.2), (96.6, 132))
    win2 = shut((101.6, 121.6), (120, 132), (101.6, 132))
    wing = shut((116, 107.4), (170, 99.8), (170.6, 104), (149, 116.8), (143, 116.16), (124, 114.14), (117, 113.4))
    wpost1, wpost2 = Seg(T(143, 116.16), T(*post1)), Seg(T(124, 114.14), T(*post2))
    stripe = shut((50, 143.6), (137, 136.4), (135, 143.6))              # a long thin triangle, clear of the tyres and the windows
    light = [C((10.6, 154.4), (12.4, 150.4), (16.4, 147), (21.4, 145.2)), C((21.4, 145.2), (24, 146.8), (24.2, 148.8), (23, 150.4)),
             C((23, 150.4), (19.4, 151.2), (15, 153.4), (12.2, 155.8)), Seg(T(12.2, 155.8), T(10.6, 154.4))]
    rockets = [T5[0], rim_t, T5[4], B5[0], rim_b, B5[4], back]
    fire_t, fire_b = T5[1:4] + [rim_t.rev()], B5[1:4] + [rim_b.rev()]
    flame_t, flame_b = fl_t + [T5[2].rev()], fl_b + [B5[2].rev()]
    steps = [
        step('Start with a 3', 'Draw a number 3: two round bumps, one on top of the other, meeting in a point in the middle. This 3 is hiding in the car.',
             [line(*three)]),
        step('Two wheels', 'Draw a wheel to the left of the 3, low down. Draw another wheel far along to the left. Draw a small circle in the middle of each.',
             rear.lines() + front.lines()),
        step('The car', 'Draw a line down the open side of the 3. From its top go along, up over the roof and down to the nose. Come back along the bottom, wheel to wheel.',
             [line(*body), line(under)]),
        step('Two windows', 'Draw two windows under the roof: a big one with a sloping front, and a small pointed one behind it.',
             [ring(*win1), ring(*win2)]),
        step('The wing', 'Above the back of the car draw a long wing that points up at the back. Draw two short posts to hold it up.',
             [ring(*wing), line(wpost1), line(wpost2)]),
        step('Rockets and fire', 'Draw a line down across each bump of the 3: these are the ends of the two rockets. Behind each bump draw three pointed flames.',
             [line(rim_t), line(rim_b), line(*fl_t), line(*fl_b)]),
        step('Stripe and light', 'Draw a long pointed stripe along the side: thin at the front, wide at the back. Draw a light on the nose, shaped like a leaf.',
             [ring(*stripe), ring(*light)]),
        step('The road', 'Draw a long line under the wheels for the road.', [road()]),
        step('Colour grey', 'Colour the two rockets grey, from the back of the car to the lines across the 3. Colour the middles of the wheels grey too.',
             [fill(FILL['grey'], *rockets), rear.grey(), front.grey()], use='grey'),
        step('Colour yellow', 'Colour the fire in the round end of each bump yellow. Colour the light on the nose yellow too.',
             [fill(FILL['yellow'], *fire_t), fill(FILL['yellow'], *fire_b), fill(FILL['yellow'], *light)], use='yellow'),
        step('Colour orange', 'Colour the pointed flames orange.', [fill(FILL['orange'], *flame_t), fill(FILL['orange'], *flame_b)], use='orange'),
        step('Colour blue', 'Colour the long stripe blue. The rest of the car stays white.', [fill(FILL['blue'], *stripe)], use='blue'),
        step('Colour the windows', 'Colour the two windows light blue.', [fill(FILL['lblue'], *win1), fill(FILL['lblue'], *win2)], use='lblue'),
        step('Colour the tyres', 'Colour the two tyres black, round their middles.', [rear.black(), front.black()], use='black'),
    ]
    D = drawing('dx_rocketcar_3', '3 is for Rocket car', 3, 15, 'vehicles', TAGS,
                'A white race car with two rockets at the back, shooting out fire. The number 3 is hiding there: its two bumps are the rockets and their fire.',
                steps, ['grey', 'yellow', 'orange', 'blue', 'lblue', 'black'])
    save('car3', D, '3')


if __name__ == '__main__':
    for f in (car1, car2, car3, car4, car5, car6, car7, car9):
        f()
