"""r is for rocket (dx_rocket_small_r), Vehicles a to z, slot r. Version 2 (27 Nov 2026).
From his pick "2 Boosters" of Claude's eight new rocket designs (step 1 review, round 2). The first rocket's r (the
left side and the curve up to the tip, from "r 1 Side and nose", 22 Nov) looked like a tall walking stick, because
the curve carried straight on from the side with no corner. The key dx_rocket_r is already used by the capital R
rocket, so this one has its own key.

A white rocket blasting off, with a booster on each side. The r is the rocket's right side and the low round top of
the right booster: the side is the r's stick (it starts a little above the booster's top, as a written r does), and
the round top leaves it at a clear angle, so it looks like the arm of an r. The round top is low on purpose: a taller
one would leave the side straight up and run along it. Step 1 is only the r: its stick stops level with the top of
the arm and a little way down, and its arm stops before the round top comes down again. Step 2 finishes that booster,
step 3 carries the stick on up into the rocket, step 4 is the other booster.

The body and the boosters stay white (plain paper), as on the first rocket. Written in the sketch's numbers; the
Pic lifts the picture 2 so its middle is the middle of the paper.

    python3 build_rocket.py
"""
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=-2.0)
L, R, TOP, BOT = 41, 59, 30, 80          # the rocket's body
BL, BR_, BBOT = 31, 69, 84                # the boosters' outer sides and their bottom
BY = 56                                    # where each booster's round top meets the rocket and its outer side
SAG = 2.6                                  # how high the round top rises
RAD = (5 ** 2 + SAG ** 2) / (2 * SAG)      # its radius (half a booster is 5 wide)
CY = BY - SAG + RAD                        # its centre (one each side, x 64 and x 36)
A_END = math.degrees(math.atan2(BY - CY, 5))           # -35.05: the angle of the outer end of the round top
A_ARM = -180 - A_END + 0.78 * (2 * A_END + 180)        # the r's arm stops 78% of the way over
STICK_TOP, STICK_BOT = BY - SAG, 73        # the r's stick: level with the top of the arm, down to 73
CAP = 59.5                                 # the line under each round top


def on_top(cx, deg):
    return P(cx + RAD * math.cos(math.radians(deg)), CY + RAD * math.sin(math.radians(deg)))


ARM_END = on_top(64, A_ARM)


def flame(x0, x1, y, depth):
    m, w = (x0 + x1) / 2, x1 - x0
    return Seg((x0, y), (x0 - w * .12, y + depth * .45), (m - w * .3, y + depth * .8), (m, y + depth)), \
        Seg((m, y + depth), (m + w * .3, y + depth * .8), (x1 + w * .12, y + depth * .45), (x1, y))


def flame_in(x0, x1, y, depth):
    m, w = (x0 + x1) / 2, x1 - x0
    a, b = m - w * .28, m + w * .28
    return Seg((a, y), (a - w * .05, y + depth * .35), (m - w * .14, y + depth * .55), (m, y + depth * .68)), \
        Seg((m, y + depth * .68), (m + w * .14, y + depth * .55), (b + w * .05, y + depth * .35), (b, y))


# ---- 7: the flames, under the rocket and the boosters ----
FL = ((44, 56, BOT, 14), (60.5, 67.5, BBOT, 9), (32.5, 39.5, BBOT, 9))
for i, (x0, x1, y, dp) in enumerate(FL):
    p.stroke('flame%d' % i, *flame(x0, x1, y, dp), step=7)
    p.stroke('flame_in%d' % i, *flame_in(x0, x1, y, dp), step=7)

# ---- 6: the windows ----
p.shape('port', circle(50, 42, 5.4), step=6)
p.shape('glass', circle(50, 42, 5.4 * 0.64), step=6)
p.shape('win2', circle(50, 62, 3.3), step=6)

# ---- 5: a line under the nose and under each round top ----
p.stroke('noseline', Seg((L, TOP), (R, TOP)), step=5)
p.stroke('cap_r', Seg((R, CAP), (BR_, CAP)), step=5)
p.stroke('cap_l', Seg((BL, CAP), (L, CAP)), step=5)

# ---- 4: the other booster, from the rocket's left side round its low top, down and back ----
p.stroke('booster_l', arc(36, CY, RAD, RAD, A_END, -180 - A_END, start=P(L, BY), end=P(BL, BY)),
         Seg((BL, BY), (BL, BBOT)), Seg((BL, BBOT), (L, BBOT)), Seg((L, BBOT), (L, BOT)), step=4)

# ---- 3: the rocket, from the top of the r's stick up, over the pointed nose, down and across the bottom ----
p.stroke('body', Seg((R, STICK_TOP), (R, TOP)), one("M59,30 C59,21 55,15 50,10 C45,15 41,21 41,30"),
         Seg((L, TOP), (L, BOT)), Seg((L, BOT), (R, BOT)), step=3)

# ---- 2: the right booster: the rest of its round top, down its outer side, along the bottom, up to the r ----
p.stroke('booster_r', arc(64, CY, RAD, RAD, A_ARM, A_END, start=ARM_END, end=P(BR_, BY)),
         Seg((BR_, BY), (BR_, BBOT)), Seg((BR_, BBOT), (R, BBOT)), Seg((R, BBOT), (R, STICK_BOT)), step=2)

# ---- 1: the r: the stick, and the arm that leaves it at the booster's top ----
p.stroke('r_stick', Seg((R, STICK_TOP), (R, STICK_BOT)), step=1)
p.stroke('r_arm', arc(64, CY, RAD, RAD, -180 - A_END, A_ARM, start=P(R, BY), end=ARM_END), step=1)
p.build()

steps = [
    step('Start with an r', 'Draw a small letter r: a short straight line down, and a little round arm that comes off it near the top and curves over to the right.', p.step(1)),
    step('A booster', "Finish the round top of the r's arm and go straight down. Go along the bottom, then up to the bottom of the r. This is a booster.", p.step(2)),
    step('The rocket', 'From the top of the r, draw a long line up. Make a pointed nose, come down the other side, and go across the bottom to the booster.', p.step(3)),
    step('The other booster', 'Draw the same booster on the other side of the rocket, with a low round top.', p.step(4)),
    step('Stripes', 'Draw a line across under the nose, and a line across each booster just under its round top.', p.step(5)),
    step('Windows', 'Draw a round window with a smaller circle inside it, and a little round window lower down.', p.step(6)),
    step('Flames', 'Draw a pointed flame under the rocket and a small one under each booster. Draw a smaller flame inside each one.', p.step(7)),
    step('Colour red', 'Colour the nose and the round tops of the boosters red.',
         [p.face('red', (50, 22)), p.face('red', (64, 58.2)), p.face('red', (36, 58.2))], use='red'),
    step('Colour grey', 'Colour the edge of the big window grey.', [p.ring('grey', 'port', holes=('glass',))], use='grey'),
    step('Colour light blue', 'Colour the middle of the big window and the little window light blue.',
         [p.ring('lblue', 'glass'), p.ring('lblue', 'win2')], use='lblue'),
    step('Colour orange', 'Colour the three big flames orange, round the small flames.',
         [p.face('orange', (44.6, 81.6)), p.face('orange', (61.3, 85.0)), p.face('orange', (33.3, 85.0))], use='orange'),
    step('Colour yellow', 'Colour the three small flames yellow.',
         [p.face('yellow', (50, 85)), p.face('yellow', (64, 86.5)), p.face('yellow', (36, 86.5))], use='yellow'),
]
D = drawing('dx_rocket_small_r', 'r is for rocket', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'A rocket blasting off, with a booster on each side. The small letter r is hiding in it: the side of the rocket and the round top of a booster.',
            steps, ['red', 'grey', 'lblue', 'orange', 'yellow'])
ok = finish('rocket', D, {'set': 'vehicles-az', 'slot': 'r', 'kind': 'fly', 'age_from': 5}, p)
