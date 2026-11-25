"""j is for jet boat (dx_jetboat_j), Vehicles a to z, slot j. A new boat, 25 Nov 2026.

He sent step 1 from the live app and said "Do this better"; of Claude's sketch he said "I like the jet boat". The old
boat was a flat wedge with a straight keel, so it read as a paper dart. This one is a boat: a deep hull with a keel that
sweeps up to a pointed nose, a windscreen and two seats standing behind the top edge of the hull.

The j is as he asked on 12 Nov: its stick is the back of the boat, its hook is the round corner underneath (and the
start of the flat bottom), it is clear of the water, and its dot is a drop of water with other drops round it.
Written in the sketch's numbers (/home/claude/fix/boatheli.py); the Pic lifts it 6.5 to sit in the middle of the paper.

    python3 build_jetboat.py
"""
from bcommon import *
import ncommon

p = Pic(s=1.0, dx=0.0, dy=-6.5)
SX, GT, KB, HR = 76.0, 50.0, 71.0, 6.0          # the stick of the j, where it starts, the bottom of the boat, the hook
BOW = (7.0, 43.0)                               # the nose of the boat
HE = (SX - HR - 5.0, KB)                        # the end of the j's hook


def drop(cx, cy, s=1.0):
    """a drop of water, point up; (cx, cy) is the middle of its round part"""
    r = 2.0 * s; tip = (cx, cy - 4.6 * s)
    return ([Seg(tip, (cx + 0.8 * s, cy - 2.6 * s), (cx + r, cy - 1.2 * s), (cx + r, cy))] + arc(cx, cy, r, r, 0, 180, start=P(cx + r, cy), end=P(cx - r, cy))
            + [Seg((cx - r, cy), (cx - r, cy - 1.2 * s), (cx - 0.8 * s, cy - 2.6 * s), tip)])


J = [Seg((SX, GT), (SX, KB - HR))] + arc(SX - HR, KB - HR, HR, HR, 0, 90, start=P(SX, KB - HR), end=P(SX - HR, KB)) + [Seg((SX - HR, KB), HE)]
keel = Seg(HE, (45.0, KB), (22.0, 66.0), BOW)
gun = Seg((SX, GT), (56.0, 48.6), (30.0, 46.2), BOW)
stripe = Seg((SX, 57.4), (56.0, 56.0), (30.0, 52.4), BOW)

# ---- behind the hull: two seats and the windscreen (the hull hides their feet) ----
p.shape('seat1', rrect(51.0, 40.4, 57.6, 54.0, 2.2), step=6)
p.shape('seat2', rrect(61.4, 41.0, 68.0, 55.0, 2.2), step=6)
p.shape('screen', poly((28.6, 48.6), (41.0, 35.6), (45.4, 35.6), (47.95, 50.0), closed=True), step=5)

# ---- the hull, then its lines ----
p.region('hull', J + [keel] + [Seg(*reversed(gun.p))])
p.stroke('stripe', stripe, step=4)
p.stroke('gun', gun, step=3)
p.stroke('keel', keel, step=2)

# ---- drops of water in the air behind the boat, and the water ----
DROPS = [('d1', 85.5, 36.5, 1.25), ('d2', 92.0, 46.5, 1.0), ('d3', 86.5, 56.0, 0.85)]
for nm, x, y, s in DROPS: p.shape(nm, drop(x, y, s), step=7)
p.stroke('water', wavy(5.0, 95.0, 81.5, amp=1.2, wl=9.0), step=8)

# ---- the j, in front of everything: stick, hook, and its dot (a drop of water) ----
p.shape('dot', drop(SX, 42.2, 0.72), step=1)
p.stroke('j', J, step=1)
p.build()

steps = [
    step('Start with a j', 'Draw a small letter j: a straight stick that curls round to the left at the bottom, with a dot above it. Make the dot a drop of water.', p.step(1)),
    step('The bottom of the boat', 'Start at the tip of the hook. Draw a long curve to the left that sweeps up to a pointed nose.', p.step(2)),
    step('The top of the boat', 'Start at the top of the stick. Draw a long line to the left that slopes up a little to meet the nose.', p.step(3)),
    step('The stripe', 'Draw a line along the side of the boat, from the stick to the nose.', p.step(4)),
    step('The windscreen', 'Draw a window standing on the boat: a line leaning back, a short line along the top and a line back down.', p.step(5)),
    step('Two seats', 'Draw two seats behind the window: up, across and down, with round corners.', p.step(6)),
    step('More splashes', 'Draw three more drops of water in the air behind the boat.', p.step(7)),
    step('The water', 'Draw a long wavy line under the boat. Leave a gap, so the water does not touch the j.', p.step(8)),
    step('Colour the boat', 'Colour the top part of the boat blue, above the stripe.', [p.face('blue', (58.0, 53.0))], use='blue'),
    step('Colour light blue', 'Colour the window and all four drops of water light blue.',
         [p.face('lblue', (41.0, 42.0)), p.ring('lblue', 'dot')] + [p.ring('lblue', nm) for nm, _, _, _ in DROPS], use='lblue'),
    step('Colour the seats', 'Colour the two seats orange.', [p.face('orange', (54.3, 44.0)), p.face('orange', (64.7, 45.0))], use='orange'),
]

D = drawing('dx_jetboat_j', 'j is for jet boat', 2, 10, 'vehicles', ['Letters', 'Vehicles'],
            'A jet boat making a splash. The small letter j is hiding in it: its stick is the back of the boat, its hook is the round corner '
            'underneath and its dot is a drop of water.',
            steps, ['blue', 'lblue', 'orange'])
ok = finish('jetboat', D, {'set': 'vehicles-az', 'slot': 'j', 'kind': 'sail', 'age_from': 4}, p)
print('    on the paper: x %.1f to %.1f, y %.1f to %.1f' % ncommon.extent(D))
