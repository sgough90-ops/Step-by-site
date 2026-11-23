"""u is for Udon (dx_udon_u), Food and drink a to z, slot u (23 Nov 2026).
From his pick (18:37): "U2 but without the prawn" = the "With a crispy prawn" design on the u-udon sheet
(claude/step-by-draw-redo-u-y-E-X-school-bus-sketches.py, s_udon.py U2), with the prawn taken out.

A red bowl of noodles from the side, with a sheet of seaweed and steam. The u is the bowl: down the left side,
round the bottom and up the right side (no stick, like the live urchin). 60 wide and 46 tall.
The three noodle loops are solid (nothing shows through them), so the seaweed is one green shape.
The noodles stay white. Written in the sketch's numbers.

    python3 build_udon.py
"""
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=-4.0)
X0, X1, TOP, BOT, RY = 20, 80, 50, 96, 30
CY = BOT - RY
U = [Seg((X0, TOP), (X0, CY))] + arc(50, CY, 30, RY, 180, 0, start=P(X0, CY), end=P(X1, CY)) + [Seg((X1, CY), (X1, TOP))]


def wisp(x, y0, y1, amp=1.8):
    return smooth([(x + (0 if i in (0, 6) else (amp if i % 2 else -amp)), y0 + (y1 - y0) * i / 6) for i in range(7)])


def loop(name, cx, rx, ry, w):
    """one fat noodle: a round loop standing on the rim. Solid, so it hides what is behind it."""
    outer = arc(cx, TOP, rx, ry, 180, 360, start=P(cx - rx, TOP), end=P(cx + rx, TOP))
    inner = arc(cx, TOP, rx - w, ry - w, 180, 360, start=P(cx - rx + w, TOP), end=P(cx + rx - w, TOP))
    p.region(name + 'R', outer, Seg((cx + rx, TOP), (cx - rx, TOP)))
    p.stroke(name + '_o', outer, step=3); p.stroke(name + '_i', inner, step=3)


# ---- behind: steam, the sheet of seaweed, three loops of noodle (the front one last) ----
for i, (x, y0) in enumerate(((52, 15), (63, 10), (74, 15))):
    p.stroke('steam%d' % i, wisp(x, y0, y0 + 16), step=5, deco=True)
p.shape('nori', poly((23.68, 25.43), (37.46, 22.99), (42.67, 52.54), (28.89, 54.98), closed=True), step=4)
loop('la', 38, 13.5, 15.5, 5.2); loop('lb', 61.5, 13.5, 16.5, 5.2); loop('lc', 50, 18, 10.4, 5.0)

# ---- the foot, the bowl (hides the bottoms of everything), its rim and its stripe ----
p.shape('foot', rrect(40, 92, 60, 101, 2.5), step=2)
p.region('bowlR', U, Seg((X1, TOP), (X0, TOP)))
p.stroke('rim', Seg((X0, TOP), (X1, TOP)), step=2)
p.stroke('band', Seg((X0, 58), (X1, 58)), step=2)

# ---- the u, in front of everything ----
p.stroke('u', U, step=1)
p.build()

steps = [
    step('Start with a u', 'Draw a big letter u: straight down, round the bottom and straight back up.', p.step(1)),
    step('Make it a bowl', 'Draw a line across the top of the u. Draw another line a little way under it. Draw a small foot under the bowl.', p.step(2)),
    step('Noodles', 'On the bowl draw three fat loops of noodle. Each loop is two curved lines, like a little rainbow. The front loop hides part of the others.', p.step(3)),
    step('Seaweed', 'Behind the noodles draw a sheet of seaweed: a tall box that leans to the left.', p.step(4)),
    step('Steam', 'Draw three wavy lines above the noodles. The soup is hot!', p.step(5)),
    step('Colour red', 'Colour the bowl red, under the stripe. Colour its little foot red too.', [p.face('red', (50, 78)), p.face('red', (50, 99))], use='red'),
    step('Colour yellow', 'Colour the stripe round the top of the bowl yellow.', [p.face('yellow', (50, 54))], use='yellow'),
    step('Colour green', 'Colour the seaweed green. The noodles stay white.', [p.face('green', (30, 30))], use='green'),
]
D = drawing('dx_udon_u', 'u is for Udon', 2, 10, 'things', ['Letters', 'Around the house'],
            'A bowl of udon: fat, soft noodles in hot soup. The small letter u is hiding in it: the bowl itself.',
            steps, ['red', 'yellow', 'green'])
ok = finish('udon', D, {'set': 'house-az', 'slot': 'u', 'kind': 'key', 'age_from': 4}, p)
