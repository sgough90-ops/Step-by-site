"""K is for Ketch (dx_ketch_k), Vehicles A to Z, slot K (22 Nov 2026).
From his pick "K1 Three sails" (Claude's sketches, claude/step-by-draw-vehicles-capitals-6x4-sketches.md).

A sailing boat with two masts, bow to the right. The K's tall line is the front edge of the back mast (a thin brown
band); its two arms are the two free edges of the middle sail, whose back corner touches that mast.
Written in the sketch's numbers; the Pic moves it onto the paper.

    python3 build_ketch.py
"""
from vkit import *

X, TOP, BOT, JY, XR, MW = 32, 22, 63, 45, 60, 3.2     # the K's tall line, its top and bottom, the joint, the front mast, how wide a mast is
MT = 13                                             # the top of the front mast
p = Pic(s=0.95, dx=1.99, dy=-1.35)

# ---- behind: the cabin, its windows, the sails and the flag ----
p.shape('cabin', one("M26.6,63 L67.4,63 Q70,63 70,65.6 L70,76 L24,76 L24,65.6 Q24,63 26.6,63 Z"), step=5)
for i, wx in enumerate((41, 47.5, 54)):
    p.shape('win%d' % i, ell(wx, 67.0, 2.0), step=5)
p.stroke('sail_back', poly((X - MW, 25), (8, 59), (X - MW, 59)), step=3)
p.stroke('sail_front', poly((XR + MW, 21), (92.5, 61.5), (XR + MW, 59.5)), step=4)
p.stroke('flag', poly((XR + MW, MT + 0.8), (71.2, MT + 3.2), (XR + MW, MT + 5.6)), step=4)
# ---- the masts and the K ----
p.stroke('mast_back', poly((X, TOP), (X - MW, TOP), (X - MW, BOT)), step=2)
p.stroke('mast_front', poly((XR, BOT), (XR, MT), (XR + MW, MT), (XR + MW, BOT)), step=2)
p.stroke('K1', Seg((X, TOP), (X, BOT)), step=1)
p.stroke('K2', poly((XR, TOP), (X, JY), (XR, BOT)), step=1)
# ---- in front: the boat, then the sea ----
p.shape('hull', one("M6,68 C28,73 62,73 96,64 C94,74 89,83 82,90 L16,90 C11,84 7,76 6,68 Z"), step=6)
p.shape('sea', blob(4, 97, 86.2, 8.2), step=7)
p.build()

WINS = ['win0', 'win1', 'win2']
steps = [
    step('Start with a K', 'Draw a capital K: a tall line down, then a slanted line in to its middle and a slanted line out again. This K is hiding in the boat.', p.step(1)),
    step('Two masts', "Draw a line down beside the K's tall line and join them at the top. Then draw a taller thin mast that touches the ends of the K's two arms.", p.step(2)),
    step('The back sail', 'On the left of the first mast, draw a sail: a long slanted line down to the left, then a straight line back to the mast.', p.step(3)),
    step('Front sail and flag', 'On the right of the tall mast, draw a big sail the same way. Add a little pointed flag at the top of the mast.', p.step(4)),
    step('Cabin and windows', 'Under the masts, draw a long low cabin with round top corners. Draw three round windows in it.', p.step(5)),
    step('The boat', 'Draw a long curved line under the cabin, a little past each end. Then curve down and in at both ends for the sides of the boat.', p.step(6)),
    step('The sea', 'Draw a long wavy line across the bottom of the boat. Carry it round underneath to make a puddle of sea.', p.step(7)),
    step('Colour brown', 'Colour the two thin masts brown.', [p.face('brown', (X - MW / 2, 40)), p.face('brown', (XR + MW / 2, 40))], use='brown'),
    step('Colour yellow', 'Colour the three sails yellow.', [p.face('yellow', (22, 50)), p.face('yellow', (50, 45)), p.face('yellow', (72, 48))], use='yellow'),
    step('Colour blue', 'Colour the boat blue.', [p.face('blue', (50, 79))], use='blue'),
    step('Colour red', 'Colour the little flag red.', [p.face('red', (65.5, MT + 3.2))], use='red'),
    step('Colour light blue', 'Colour the sea and the three round windows light blue.', [p.ring('lblue', 'sea')] + [p.ring('lblue', w) for w in WINS], use='lblue'),
]

D = drawing('dx_ketch_k', 'K is for Ketch', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'A ketch, a sailing boat with two masts and three sails. The capital K is hiding in it: its tall line is the front edge '
            'of the back mast, and its two arms are the edges of the middle sail.',
            steps, ['brown', 'yellow', 'blue', 'red', 'lblue'])
save('ketch', D, {'set': 'vehicles-AZ', 'slot': 'K', 'kind': 'sail', 'age_from': 5})
save_white('ketch', p.white)
if __name__ == '__main__':
    preview(D, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'ketch-look.png'))
