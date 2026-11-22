"""J is for Jasmine tea (dx_jasminetea_j), Food and drink A to Z, slot J (22 Nov 2026).
From his pick "J3 String over the side" (Claude's sketches, claude/step-by-draw-food-11-ideas-4-versions.md).

A cup of tea on a saucer. The string of the tea bag comes over the side of the cup and hangs down, with the tag on its
end. The string is the J: straight down, then a hook to the left. A little jasmine flower floats on the tea.

    python3 build_jasminetea.py
"""
import json, math, os
from fkit import *

YELLOW, LBLUE = FILL['yellow'], FILL['lblue']
CX, TOP, RX, RY, H = 58.0, 34.0, 28.0, 6.8, 36.0     # the cup: middle, top, half-width of the top, how tall
XL, XR = CX - RX, CX + RX
JB, HOOK = 66.5, 15.5                                # the bottom of the J, how wide its hook is
R = HOOK / 2
TAG = 5.5                                            # half the tag
TAGY = JB - R - 5.0                                  # the J ends here, on the bottom edge of the tag

net = Net()
# 1: the J (the string), in one go
net.add('J', Seg((XL, TOP), (XL, JB - R)), Seg((XL, JB - R), (XL, JB - R * 0.1), (XL - R * 0.45, JB), (XL - R, JB)),
        Seg((XL - R, JB), (XL - R * 1.55, JB), (XL - HOOK, JB - R * 0.45), (XL - HOOK, JB - R)), Seg((XL - HOOK, JB - R), (XL - HOOK, TAGY)))
# 2: the tag, starting and ending where the string joins it
TX = XL - HOOK
net.add('tag', poly((TX, TAGY), (TX + TAG, TAGY), (TX + TAG, TAGY - 2 * TAG), (TX - TAG, TAGY - 2 * TAG), (TX - TAG, TAGY), (TX, TAGY)))
# 3: the top of the cup, from the top of the J
net.add('rim', ell(CX, TOP, RX, RY, start=180))
# 4: the sides and bottom of the cup
A0 = math.radians(20)                                 # the sides start a little way in from the two ends of the oval
L0, R0 = P(CX - RX * math.cos(A0), TOP + RY * math.sin(A0)), P(CX + RX * math.cos(A0), TOP + RY * math.sin(A0))
net.add('cup', Seg(L0, (L0[0] + 3.2, L0[1] + 5), (XL + 4.6, TOP + 15.5), (XL + 9.5, TOP + 23)), Seg((XL + 9.5, TOP + 23), (XL + 13, TOP + 28.5), (CX - 13, TOP + H), (CX - 8, TOP + H)),
        Seg((CX - 8, TOP + H), (CX + 8, TOP + H)),
        Seg((CX + 8, TOP + H), (CX + 13, TOP + H), (XR - 13, TOP + 28.5), (XR - 9.5, TOP + 23)), Seg((XR - 9.5, TOP + 23), (XR - 4.6, TOP + 15.5), (R0[0] - 3.2, R0[1] + 5), R0))
net.region('cupR', net.all('cup'), Seg(R0, L0))
# 5: the handle (its ends run on behind the cup and are trimmed)
net.add('hout', Seg((XR - 9, TOP + 5.5), (XR + 12, TOP + 2), (XR + 11, TOP + 28), (XR - 14, TOP + 25.5)))
net.add('hin', Seg((XR - 9, TOP + 10.5), (XR + 5.6, TOP + 8.5), (XR + 4.6, TOP + 21.5), (XR - 13, TOP + 20)))
# 6: the saucer, behind the cup
net.add('saucer', ell(CX, TOP + H + 4.5, 38, 7.5))
# 7: the tea, a flower floating on it, and the steam
net.add('tea', ell(CX, TOP + 0.6, RX - 3.8, RY - 2.2))


def flower(cx, cy, r, k=5, rot=90):
    pts = []
    for i in range(k * 4):
        a = math.radians(rot + i * 360 / (k * 4))
        rr = r * (1.0 if i % 4 == 0 else 0.86 if i % 4 in (1, 3) else 0.5)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return smooth(pts, closed=True)


FL = flower(CX - 4, TOP + 0.7, 3.5)
net.add('flower', FL)
net.node()
net.hide('hout', 'cupR'); net.hide('hin', 'cupR'); net.hide('saucer', 'cupR')

steam = [smooth([(x, 23.5 + dy), (x - 2, 20.5 + dy), (x + 2, 16.5 + dy), (x - 2, 12.5 + dy), (x, 9 + dy)]) for x, dy in ((51, 0), (65, 1.5))]
white = [d_fill(*net.all('flower'))]
steps = [
    step('Start with a J', 'Draw a capital J: a straight line down, with a hook to the left at the bottom. This J is hiding in the cup of tea.',
         net.lines('J')),
    step('The tag', 'Draw a small square on the end of the hook. The J is the string of the tea bag, and this is its tag.', net.lines('tag')),
    step('The top of the cup', 'From the top of the J, draw a long flat oval to the right.', net.lines('rim')),
    step('The cup', 'Start on the oval, near the top of the J. Curve down and in, go along the flat bottom, and curve up to the other side of the oval.',
         net.lines('cup')),
    step('The handle', 'On the right of the cup, draw a handle like an ear: one big curve, and a smaller curve inside it.', net.lines('hout', 'hin')),
    step('The saucer', 'Draw a big flat oval under the cup. It goes behind the cup, so leave a gap there.', net.lines('saucer')),
    step('Tea and steam', 'Inside the top of the cup, draw a flat oval for the tea, with a tiny flower floating on it. Draw two wiggly lines above.',
         net.lines('tea', 'flower') + [dot(CX - 4, TOP + 0.7, w=1.6)] + [line(*s) for s in steam]),
    step('Colour yellow', 'Colour the tea yellow, round the flower. Colour the tag yellow too.',
         [fill(YELLOW, *net.all('tea'), cut=white), net.fill(YELLOW, (TX, TAGY - TAG), names=['tag'])], use='yellow'),
    step('Colour light blue', 'Colour the cup, the handle and the saucer light blue. Leave the flower and the inside rim of the cup white.',
         [net.fill(LBLUE, (CX, TOP + 22), names=['cup', 'rim']), net.fill(LBLUE, (XR + 2.2, TOP + 15), names=['hout', 'hin', 'cup']),
          net.fill(LBLUE, (CX - 26, TOP + H + 5.5), names=['saucer', 'cup'])], use='lblue'),
]

D = drawing('dx_jasminetea_j', 'J is for Jasmine tea', 2, 12, 'things', ['Letters', 'Around the house'],
            'A cup of jasmine tea on a saucer, with a flower floating on top. The capital J is hiding in it: it is the string of the tea bag.',
            steps, ['yellow', 'lblue'])
save('jasminetea', D, {'set': 'house-AZ', 'slot': 'J', 'kind': 'key', 'age_from': 4})
json.dump(white, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'jasminetea.white.json'), 'w'))
