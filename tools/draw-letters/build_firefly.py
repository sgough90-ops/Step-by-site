"""f is for firefly (dx_firefly_f), Animals, slot f. A new firefly, 25 Nov 2026.

He sent step 1 from the live app: "Give me four fly variations that's a better". He liked number 2 (flying, side on)
and said "replace the red and yellow with black", then "do the steps for number one" of the four black versions:
the body is black all over (no yellow light), the wings are light blue. Then at 19:06: "do you not colour the fly's
face cream ... And can you make the start an f a bit more natural looking?" So the head is cream (a new pencil, 'cream'),
and the f is written the way it is in school: the curl goes over the top and a little way down, and its line across is
short, a little each side of the stick and higher up (it used to run right across the body, long on one side).

The f: its stick is the front of the body, its hook is the top of the head, its bar is a line across the middle of
the body that carries on into the wings. Sketch: /home/claude/fix/r2.py fly(1).

    python3 build_firefly.py
"""
from bcommon import *
import math
import ncommon

p = Pic(s=1.0, dx=5.5, dy=5.0)          # moved to the middle of the paper
SX, TOPY, BOTY, BARY, HR = 46.0, 31.0, 76.0, 47.0, 11.0
BARL, BARR = 37.5, 57.0                 # the f's line across: a little each side of the stick, as it is written
A1 = 300.0                              # the curl goes over the top and a little way down, like a written f


def smooth(pts):
    """a smooth line through the points (Catmull-Rom as curves)"""
    out = []
    q = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(q) - 2):
        a, b, c, d = q[i - 1], q[i], q[i + 1], q[i + 2]
        out.append(Seg(b, (b[0] + (c[0] - a[0]) / 6, b[1] + (c[1] - a[1]) / 6), (c[0] - (d[0] - b[0]) / 6, c[1] - (d[1] - b[1]) / 6), c))
    return out


def on_back(y, segs):
    """the point on the back line at height y (the curve that passes it)"""
    for s in segs:
        ys = [s.at(t / 400)[1] for t in range(401)]
        for t in range(400):
            if (ys[t] - y) * (ys[t + 1] - y) <= 0:
                return s.at(t / 400)
    raise ValueError(y)


def on_hook(a):
    return (SX + HR + HR * math.cos(math.radians(a)), TOPY + HR * math.sin(math.radians(a)))


E = on_hook(A1)
letter = [Seg((SX, BOTY), (SX, TOPY))] + arc(SX + HR, TOPY, HR, HR, 180, A1, start=P(SX, TOPY), end=P(*E))
bar = Seg((BARL, BARY), (BARR, BARY))
tx, ty = -math.sin(math.radians(A1)), math.cos(math.radians(A1))      # which way the curl is going at its end
back = [Seg(E, (E[0] + 4.0 * tx, E[1] + 4.0 * ty), (70.0, 26.6), (70.0, 32.0)), Seg((70.0, 32.0), (70.0, 37.0), (67.4, 40.6), (63.6, 42.4)),
        Seg((63.6, 42.4), (66.0, 46.0), (67.0, 50.0), (67.0, 52.0)), Seg((67.0, 52.0), (67.0, 62.0), (64.6, 70.0), (61.0, BOTY)),
        Seg((61.0, BOTY), (59.0, 81.6), (48.0, 81.6), (SX, BOTY))]
neck = Seg((SX, 41.0), (52.0, 42.6), (58.0, 43.4), (63.6, 42.4))
stripe = Seg((SX, 66.0), on_back(66.0, back[3:4]))

# wings, behind the body: the top one goes from the stick to the line across, the bottom one from the line across to the stick
p.stroke('wing1', smooth([(SX, 43.0), (37.0, 34.0), (25.0, 28.0), (16.6, 31.0), (17.0, 39.0), (25.0, 42.2), (33.0, 43.2), (40.0, BARY)]), step=5)
p.stroke('wing2', smooth([(41.5, BARY), (34.0, 51.2), (22.0, 55.2), (16.0, 59.6), (19.0, 64.4), (29.0, 62.6), (38.6, 57.4), (SX, 53.0)]), step=5)
# feelers come off the top of the head, legs off the back
f1, f2 = on_hook(265.0), on_back(22.8, back[0:1])
p.stroke('feel1', Seg(f1, (f1[0] - 0.4, 14.0), (f1[0] + 2.0, 10.0), (f1[0] + 6.6, 9.6)), step=6)
p.stroke('feel2', Seg(f2, (f2[0] + 1.2, 18.4), (f2[0] + 3.8, 15.6), (f2[0] + 8.0, 16.0)), step=6)
for k, y in enumerate((48.0, 57.0, 63.5)):
    b = on_back(y, back[2:4])
    p.stroke('leg%d' % k, Seg(b, (b[0] + 4.0, y - 0.6), (b[0] + 6.6, y + 1.6), (b[0] + 7.6, y + 5.0)), step=6)
p.stroke('back', back, step=2)
p.stroke('neck', neck, step=3)
p.shape('eye', circle(61.6, 30.4, 3.0), step=3)
p.shape('pupil', circle(62.4, 30.6, 1.3), step=3)
p.stroke('mouth', Seg((58.6, 36.4), (61.0, 38.8), (64.6, 38.6), (66.6, 36.2)), step=6, deco=True)
p.stroke('stripe', stripe, step=4)
p.stroke('fbar', bar, step=1)
p.stroke('f', letter, step=1)
p.build()

body = [p.face('black', (56.0, 55.0), skip=['fbar']), p.face('black', (54.0, 72.0))]
p.stay_white('eye')                     # the white of the eye stays white
head = p.face('cream', (51.0, 35.0), holes=['eye'])
steps = [
    step('Start with an f', 'Draw a small letter f: a straight stick that curls over at the top, and a short line across it. This f is hiding in the firefly.', p.step(1)),
    step('Its back', 'From the end of the curl, draw the back of the firefly: round the head, in at the neck, down a long body and round to the bottom of the stick.', p.step(2)),
    step('Head and eye', 'Draw a curved line across, under the head. Draw a big round eye with a dot inside it.', p.step(3)),
    step('A stripe', 'Draw a short line across the bottom of the body.', p.step(4)),
    step('Two wings', 'Draw a big wing from the stick out to the end of the short line. Draw a smaller wing below it.', p.step(5)),
    step('Feelers and legs', 'Draw two curly feelers on top of the head, three legs on its back, and a smile.', p.step(6)),
    step('Colour black', 'Colour the body black, below the head. Colour the dot in its eye black too.', body + [p.ring('black', 'pupil')], use='black'),
    step('Colour the face', 'Colour the head cream. Go round the eye.', [head], use='cream'),
    step('Colour the wings', 'Colour the two wings light blue.', [p.face('lblue', (24.0, 36.0)), p.face('lblue', (22.0, 60.0))], use='lblue'),
]
D = drawing('dx_firefly_f', 'f is for firefly', 2, 10, 'animals', ['Letters', 'Animals'],
            'A black firefly flying. The small letter f is hiding in it: its stick is the front of the body, its curl is the top '
            'of the head and its short line across is where the wings meet the body.',
            steps, ['black', 'cream', 'lblue'])
ok = finish('firefly', D, {'set': 'animals-az', 'slot': 'f', 'kind': 'fly', 'age_from': 5}, p)
print('    on the paper: x %.1f to %.1f, y %.1f to %.1f' % tuple(ncommon.extent(D)[i] for i in (0, 2, 1, 3)))
