"""s is for Sushi (dx_sushi_s), Food and drink a to z, slot s (23 Nov 2026).
From his pick, round 2 number 3 "Inside-out rolls" (Claude's sketches, claude/step-by-draw-food-small-round2-and-five-builds.md),
with his change: "also adding the chopsticks to the right like it's done in number one".

Two sushi rolls seen from above (rice on the outside, with seeds), on a wooden board with a dish of soy sauce,
ginger and wasabi, and two chopsticks beside the board on the right. The s is his own plan: the left edge of the
top roll, then the right edge of the roll under it. The two rolls touch at one point, where the s passes from one
to the other. The board starts a little way down so nothing sits under the step number.
Written in the sketch's numbers.

    python3 build_sushi.py
"""
import qcheck                                    # the quicker crossing test (the same 9 checks)
from bcommon import *

p = Pic(s=1.0, dx=1.5, dy=0.0)
CX, CY, R = 25.0, 57.0, 18.0                     # where the two rolls touch, and how big each roll is
RN, RF = 10.4, 7.6                               # the ring of seaweed in each roll: outside and inside
TOPC, BOTC = (CX, CY - R), (CX, CY + R)          # the middles of the two rolls
K = math.sqrt(0.5) * R
S0, S1, TOUCH = (CX + K, CY - R - K), (CX - K, CY + R + K), (CX, CY)   # the s: where it starts and ends, and where the rolls touch
DISH, GIN, WAS = (59.5, 32.0), (59.5, 56.0), (60.0, 80.0)
CHOP = (84.0, 91.0)


def wavy(cx, cy, rx, ry, k, amp, phase=0.0):
    """a round shape with a wavy edge (k bumps)"""
    pts = []
    for i in range(2 * k):
        a = math.radians(phase) + i * math.pi / k; r = 1.0 if i % 2 == 0 else 1.0 - amp
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return smooth(pts, closed=True)


# ---- the board and what is on it, the chopsticks beside it ----
p.shape('board', rrect(3, 17, 75, 97, 8), step=4)
p.shape('dish', circle(DISH[0], DISH[1], 10), step=5)
p.shape('sauce', circle(DISH[0], DISH[1], 7), step=5)
p.shape('ginger', wavy(GIN[0], GIN[1], 9, 6.5, 7, 0.16), step=5)
p.shape('wasabi', wavy(WAS[0], WAS[1], 8.5, 7.5, 6, 0.13, 20), step=5)
for i, x in enumerate(CHOP):
    p.shape('chop%d' % i, poly((x - 1.8, 12), (x + 1.8, 12), (x + 1.3, 97), (x - 1.3, 97), closed=True), step=6)

# ---- the two rolls: the rest of each one's edge, and its middle ----
p.stroke('restT', arc(TOPC[0], TOPC[1], R, R, 315, 450, start=P(*S0), end=P(*TOUCH)), step=2)
p.stroke('restB', arc(BOTC[0], BOTC[1], R, R, 135, 270, start=P(*S1), end=P(*TOUCH)), step=2)
for nm, (x, y) in (('T', TOPC), ('B', BOTC)):
    p.shape('nori' + nm, circle(x, y, RN), step=3)
    p.shape('fill' + nm, circle(x, y, RF), step=3)

# ---- the s, in front of everything ----
p.stroke('s_top', arc(TOPC[0], TOPC[1], R, R, 315, 90, start=P(*S0), end=P(*TOUCH)), step=1)
p.stroke('s_bot', arc(BOTC[0], BOTC[1], R, R, 270, 495, start=P(*TOUCH), end=P(*S1)), step=1)
p.build()

# ---- the seeds on the rice ----
seeds = []                                       # five on each roll: with the four circles that makes 14 new lines, the most the app's checker allows in a step
for (x, y), a0 in ((TOPC, 18), (BOTC, 54)):
    for i in range(5):
        a = math.radians(a0 + 72 * i)
        seeds.append(dot(*p.pt(x + 14.2 * math.cos(a), y + 14.2 * math.sin(a)), w=2.4))

# ---- the board's colour goes all round the things on it; the two rolls (the rice) stay white ----
net = p.net
roll_t = d_fill(*(net.all('s_top') + rev(net.all('restT'))))
roll_b = d_fill(*(net.all('s_bot') + net.all('restB')))
p.white += [roll_t, roll_b]
board = net.fill(FILL['lbrown'], p.pt(45, 22), names=[it['name'] for it in p.items if it['kind'] != 'region'],
                 cut=[roll_t, roll_b] + [d_fill(*net.all(h)) for h in ('dish', 'ginger', 'wasabi')])

steps = [
    step('Start with an s', 'Draw a small letter s: curl round to the left at the top, then round to the right at the bottom. Make both halves the same size.', p.step(1)),
    step('Two rolls', 'Each half of the s is one side of a round sushi roll. Draw the other side of each roll, so you have two circles.', p.step(2)),
    step('The middles', 'In the middle of each roll draw a ring: two circles, one just inside the other. Dot the rice with a few little seeds.', p.step(3) + seeds),
    step('The board', 'Draw a big board round the two rolls, with round corners. Leave lots of room on the right of the rolls.', p.step(4)),
    step('Sauce, ginger, wasabi', 'On the board draw a round dish of soy sauce (two circles), a wavy pile of ginger and a wavy blob of wasabi.', p.step(5)),
    step('Chopsticks', 'Next to the board, on the right, draw two long thin chopsticks.', p.step(6)),
    step('Colour black', 'Colour the thin ring in each roll black. That is the seaweed. Colour the edge of the little dish black too.',
         [p.ring('black', 'noriT', holes=('fillT',)), p.ring('black', 'noriB', holes=('fillB',)), p.ring('black', 'dish', holes=('sauce',))], use='black'),
    step('Colour orange', 'Colour the middle of the top roll orange, for salmon.', [p.ring('orange', 'fillT')], use='orange'),
    step('Colour green', 'Colour the middle of the bottom roll green, for avocado. Colour the wasabi green too.', [p.ring('green', 'fillB'), p.ring('green', 'wasabi')], use='green'),
    step('Colour pink', 'Colour the ginger pink.', [p.ring('pink', 'ginger')], use='pink'),
    step('Colour brown', 'Colour the soy sauce and the two chopsticks brown.', [p.ring('brown', 'sauce'), p.ring('brown', 'chop0'), p.ring('brown', 'chop1')], use='brown'),
    step('Colour the board', 'Colour the board light brown, all round the rolls and the food. Leave the rice white.', [board], use='lbrown'),
]
D = drawing('dx_sushi_s', 's is for Sushi', 3, 15, 'things', ['Letters', 'Around the house'],
            'Two sushi rolls on a board, with soy sauce, ginger, wasabi and chopsticks. The small letter s is hiding in the rolls: the left edge of the top one and the right edge of the bottom one.',
            steps, ['black', 'orange', 'green', 'pink', 'brown', 'lbrown'])
ok = finish('sushi', D, {'set': 'house-az', 'slot': 's', 'kind': 'key', 'age_from': 4}, p)
