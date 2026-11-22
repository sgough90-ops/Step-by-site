"""O is for Oil tanker (dx_oiltanker_o), Vehicles A to Z, slot O (22 Nov 2026).
From his pick "O1 Three round tanks" (Claude's sketches, claude/step-by-draw-vehicles-capitals-6x4-sketches.md).

A tanker from the side, bow to the right: three round tanks on the deck, a yellow pipe over them, a white cabin with
a red funnel at the back. The O is the middle tank. A little simpler than the sketch so a pencil can do it: each tank
sits on one stand (not two legs), the pipe drops straight into the tanks (no caps), the funnel is all red, and there
is no white anchor. Written in the sketch's numbers; the Pic moves it onto the paper.

    python3 build_oiltanker.py
"""
from vkit import *

CXS, CY, RX, RY = (40.5, 60.0, 79.5), 50.6, 8.3, 9.0     # the three tanks (the middle one is the O)
DECK = 63.0
PY0, PY1 = 36.2, 39.4                                    # the pipe
p = Pic(s=0.94, dx=2.85, dy=-3.68)

# ---- at the back: funnel, mast, pipe, then the cabin in front of them ----
p.shape('funnel', poly((6.8, 46.5), (7.6, 28.5), (12.6, 28.5), (12.6, 46.5), closed=True), step=7)
p.stroke('bm_lo', Seg((20, 32.6), (20, 25.4)), step=8)
p.stroke('bm_hi', Seg((20, 25.4), (20, 22)), step=8)
p.stroke('bm_x', Seg((17, 25.4), (23, 25.4)), step=8)
tabs = []
for cx in reversed(CXS[:2]):
    tabs += [(cx + 1.5, PY1), (cx + 1.5, 44), (cx - 1.5, 44), (cx - 1.5, PY1)]
XE = CXS[2] + 1.5                                        # the pipe turns down into the last tank
pipe = [Seg((24, PY0), (XE - 1.6, PY0)), *arc(XE - 1.6, PY0 + 1.6, 1.6, 1.6, -90, 0, start=P(XE - 1.6, PY0), end=P(XE, PY0 + 1.6)),
        *poly((XE, PY0 + 1.6), (XE, 44), (XE - 3, 44), (XE - 3, PY1), *tabs, (24, PY1), (24, PY0))]
p.shape('pipe', pipe, step=4)
# the top box: its back wall is flush with the wall of the box below, so it is two side lines (not a box whose
# bottom would run along that wall); the region hides the funnel and the pipe behind it
p.region('cab_bR', box(12, 33, 26, 45.5))
p.stroke('cab_bl', Seg((12, 33), (12, 45.8)), step=7)
p.stroke('cab_br', Seg((26, 33), (26, 45)), step=7)
p.shape('slab', rrect(10.6, 31.4, 27.4, 34, 0.7), step=7)
p.shape('bwin', rrect(14, 37, 24, 41.6, 0.6), step=8)
for i, x in enumerate((17.33, 20.67)):
    p.stroke('bbar%d' % i, Seg((x, 37), (x, 41.6)), step=8, deco=True)
p.shape('cab_a', box(6, 45, 26, 60), step=7)
for i, x in enumerate((8.4, 14.2, 20.0)):
    p.shape('awin%d' % i, rrect(x, 48.4, x + 3.6, 53, 0.6), step=8)

# ---- on the deck: a stand under each tank, the tanks, an oil drop in each ----
for i, cx in enumerate(CXS):
    p.shape('stand%d' % i, poly((cx - 5.4, 64.2), (cx - 4.2, 56), (cx + 4.2, 56), (cx + 5.4, 64.2), closed=True), step=3)
for i, cx in enumerate(CXS):
    p.shape('O' if i == 1 else 'tank%d' % i, ell(cx, CY, RX, RY), step=1 if i == 1 else 2)
S = 2.6
for i, cx in enumerate(CXS):
    c2 = CY + 0.4
    drop = [Seg((cx, c2 - 1.55 * S), (cx + 0.95 * S, c2 - 0.3 * S), (cx + S, c2 + 0.3 * S), (cx + S, c2 + 0.5 * S)),
            *arc(cx, c2 + 0.5 * S, S, S, 0, 180, start=P(cx + S, c2 + 0.5 * S), end=P(cx - S, c2 + 0.5 * S)),
            Seg((cx - S, c2 + 0.5 * S), (cx - S, c2 + 0.3 * S), (cx - 0.95 * S, c2 - 0.3 * S), (cx, c2 - 1.55 * S))]
    p.shape('drop%d' % i, drop, step=9)

# ---- the front mast, the ship, the sea ----
p.stroke('fm_lo', Seg((93.6, 59), (93.6, 47.6)), step=8)
p.stroke('fm_hi', Seg((93.6, 47.6), (93.6, 44)), step=8)
p.stroke('fm_x', Seg((91, 47.6), (96.2, 47.6)), step=8)
p.shape('hull', one(f"M4,58 L26,58 C29,58 29,{DECK} 32,{DECK} L88,{DECK} C91,{DECK} 90,58 93,58 L98.5,58 L91,89 L8,89 Q4,89 4,85 Z"), step=5)
p.stroke('waterline', Seg((2, 76), (99.5, 76)), step=5)
p.shape('sea', blob(3, 97, 85.6, 8.5), step=6)

p.build(keep=[('waterline', 'sea')])
p.net.keep_in('waterline', 'hull')

TANKS = ['tank0', 'O', 'tank2']
steps = [
    step('Start with an O', 'Draw a capital O, a little taller than it is wide. This O is hiding on the ship: it is the middle tank.', p.step(1)),
    step('Two more tanks', 'Draw another O the same size on each side of it. Leave a small gap between them.', p.step(2)),
    step('The stands', 'Under each tank, draw two short lines going down that lean outwards, like little feet.', p.step(3)),
    step('The pipe', 'Above the tanks, draw a long thin pipe from the left. A short pipe drops into the top of each tank. At the last tank the pipe bends down.', p.step(4)),
    step('The ship', 'Draw a long line under the stands. Step up at both ends, go down at the back, and slant down and in at the front. Add a line along the side.', p.step(5)),
    step('The sea', 'Draw a long wavy line across the bottom of the ship. Carry it round underneath to make a puddle of sea.', p.step(6)),
    step('Cabin and funnel', 'At the back, draw a box for the cabin with a narrower box on top and a thin roof. Draw a tall funnel behind it, on the left.', p.step(7)),
    step('Windows and masts', 'Draw a long window with two bars in the top box and three small windows below. Draw a mast with a crossbar on the roof and one at the front.', p.step(8)),
    step('Oil drops', 'Draw a drop of oil in each tank: a point at the top and round at the bottom.', p.step(9)),
    step('Colour grey', 'Colour the three tanks and their stands grey. Leave the oil drops.',
         [p.ring('grey', t, holes=['drop%d' % i]) for i, t in enumerate(TANKS)] + [p.face('grey', (cx, 61.6)) for cx in CXS], use='grey'),
    step('Colour yellow', 'Colour the long pipe yellow, and the short pipes that drop into the tanks.', [p.face('yellow', (50, (PY0 + PY1) / 2))], use='yellow'),
    step('Colour red', 'Colour the funnel red. Colour the bottom of the ship red, under the line.', [p.face('red', (9.6, 38)), p.face('red', (50, 80))], use='red'),
    step('Colour black', 'Colour the top of the ship black, above the line. Colour the three oil drops black.',
         [p.face('black', (50, 69))] + [p.ring('black', 'drop%d' % i) for i in range(3)], use='black'),
    step('Colour blue', 'Colour the sea and all the windows blue. Leave the cabin white.',
         [p.ring('blue', 'sea'), p.ring('blue', 'bwin')] + [p.ring('blue', 'awin%d' % i) for i in range(3)], use='blue'),
]

D = drawing('dx_oiltanker_o', 'O is for Oil tanker', 4, 20, 'vehicles', ['Letters', 'Vehicles'],
            'An oil tanker with three round tanks, a yellow pipe and a red funnel. The capital O is hiding on its deck: '
            'it is the outline of the middle tank.',
            steps, ['grey', 'yellow', 'red', 'black', 'blue'])
save('oiltanker', D, {'set': 'vehicles-AZ', 'slot': 'O', 'kind': 'sail', 'age_from': 5})
save_white('oiltanker', p.white)
if __name__ == '__main__':
    preview(D, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'oiltanker-look.png'))
