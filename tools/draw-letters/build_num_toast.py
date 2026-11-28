"""2 is for Toast (dx_toast_2), Food and drink 1 to 9, slot 2. Version 2, 28 Nov 2026 (version 1, toast and jam, was 23 Nov).

His asks on 28 Nov, in order: the cut should make two halves that look equal; a crust; the crust "naturally connected
on both slices"; butter "more spread" with no chunks. His picks: toast 1 of the crust sheet, butter 2 ("nearly to the
crust"), then "make live".

A slice of buttered toast, cut in two. The 2 is the round top of the slice, the cut and the bottom of the slice.
- Equal halves: the round top of the 2 stops TH degrees before the right-hand end of the dome, so the cut starts on top
  of the slice and each half gets a share of the dome. With TH = 40.89 the two halves have the same area (2046 each).
  The rest of the dome is not the 2: it is drawn in step 2 and carries the 2's round top on.
- The crust is one band of the same width all the way round the whole slice, then cut by the 2's slanted line. So its
  inside line is two lines (one for each half) that stop at the cut at the very same two spots: no line goes through
  the 2, but the crust does meet it from both sides at one spot, which is what he asked for. The bottom crust is just
  thick enough (TB) for the inside corner at the bottom left to sit on the cut.
- The butter is spread over the whole slice and cut with it, so its edge is two lines in the same way. Its edge is the
  wavy line of the sketch he picked (points read off the sketch, one list for each half).
- The butter is the yellow pencil pressed gently: the same pale yellow as V is for Vanilla cone.
Written in the sketch's numbers.

    python3 build_num_toast.py
"""
from ncommon import *

p = Pic(s=1.0, dx=0.0, dy=0.0)
CX, CY, R, XL, XR, BOT = 50, 41, 30, 22.5, 77.5, 89
TH = 40.89                                    # the round top of the 2 stops this many degrees before the dome's right end
LIP, SH = 5.0, 52.0                           # the dome sticks out over the sides: straight down LIP, then tucked in by SH
T = 3.6                                       # how thick the crust is
BUTTER = '#fff0b3'                            # pale yellow, as the vanilla cone's ice cream (yellow pencil, pressed gently)

S = P(CX - R, CY)
E = P(CX + R * math.cos(math.radians(-TH)), CY + R * math.sin(math.radians(-TH)))
V, B = P(XL, BOT), P(XR, BOT)
on_cut = lambda t: (E[0] + (V[0] - E[0]) * t, E[1] + (V[1] - E[1]) * t)        # a point on the cut (the slanted line of the 2)
TB = T * (BOT - E[1]) / (E[0] - XL)           # the bottom crust: its inside corner at the bottom left is then on the cut
RI = R - T


def cut_meets_circle(r):
    """how far along the cut it meets the circle of radius r round the middle of the dome"""
    lo, hi = 0.0, 0.5
    for _ in range(60):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if math.dist(on_cut(m), (CX, CY)) > r else (lo, m)
    return (lo + hi) / 2


C_TOP = P(*on_cut(cut_meets_circle(RI)))                                       # where the crust's inside line meets the cut, at the top
C_BOT = P(XL + T, BOT - TB)                                                    # and at the bottom left
A_TOP = math.degrees(math.atan2(C_TOP[1] - CY, C_TOP[0] - CX)) % 360

# ---- the rest of the slice: the dome carries on from the end of the 2's round top, then the two sides ----
p.stroke('side_r', arc(CX, CY, R, R, 360 - TH, 360, start=E, end=P(CX + R, CY)), Seg((CX + R, CY), (CX + R, CY + LIP)),
         Seg((CX + R, CY + LIP), (CX + R, CY + LIP + 2.8), (XR, SH - 3.4), (XR, SH)), Seg((XR, SH), B), step=2)
p.stroke('side_l', Seg(S, (CX - R, CY + LIP)), Seg((CX - R, CY + LIP), (CX - R, CY + LIP + 2.8), (XL, SH - 3.4), (XL, SH)), Seg((XL, SH), V), step=2)

# ---- the crust's inside line: one line for each half, both stopping at the same two spots on the cut ----
p.stroke('crust_a', arc(CX, CY, RI, RI, A_TOP, 180, start=C_TOP, end=P(CX - RI, CY)), Seg((CX - RI, CY), (CX - RI, CY + LIP)),
         Seg((CX - RI, CY + LIP), (CX - RI, CY + LIP + 2.8), (XL + T, SH - 3.4), (XL + T, SH)), Seg((XL + T, SH), C_BOT), step=3)
p.stroke('crust_b', Seg(C_BOT, (XR - T, BOT - TB)), Seg((XR - T, BOT - TB), (XR - T, SH)),
         Seg((XR - T, SH), (XR - T, SH - 3.4), (CX + RI, CY + LIP + 2.8), (CX + RI, CY + LIP)), Seg((CX + RI, CY + LIP), (CX + RI, CY)),
         arc(CX, CY, RI, RI, 360, A_TOP, start=P(CX + RI, CY), end=C_TOP), step=3)

# ---- the butter: its wavy edge, one line for each half, both stopping at the same two spots on the cut ----
UP = [(29.5, 75.44), (29.93, 72.22), (30.24, 68.99), (29.92, 65.76), (29.19, 62.59), (28.76, 59.37), (29.05, 56.13), (29.62, 52.93),
      (29.6, 49.69), (28.84, 46.53), (27.83, 43.44), (27.43, 40.23), (28.23, 37.1), (29.77, 34.24), (31.33, 31.38), (32.64, 28.4),
      (34.15, 25.53), (36.37, 23.18), (39.24, 21.68), (42.36, 20.74), (45.46, 19.76), (48.5, 18.62), (51.67, 17.91), (54.88, 18.26),
      (57.81, 19.65), (60.47, 21.52), (63.19, 23.3), (65.95, 25.02)]
LOW = [(69.88, 30.09), (70.48, 33.31), (70.77, 36.57), (71.29, 39.81), (71.67, 43.07), (71.54, 46.34), (70.71, 49.51), (69.63, 52.61),
       (69.26, 55.86), (69.79, 59.09), (70.63, 62.26), (71.05, 65.51), (70.75, 68.77), (70.2, 72.01), (70.06, 75.28), (69.86, 78.55),
       (68.21, 81.31), (65.2, 82.47), (61.97, 81.98), (58.78, 81.19), (55.52, 80.96), (52.26, 81.37), (49.01, 81.81), (45.74, 81.67),
       (42.53, 81.01), (39.29, 80.51), (36.02, 80.69), (32.76, 80.54)]
B_TOP = P(*on_cut((E[0] - 68.34) / (E[0] - V[0])))                             # where the butter's edge meets the cut
B_BOT = P(*on_cut((E[0] - 30.24) / (E[0] - V[0])))
p.stroke('butter_a', smooth([B_BOT] + UP + [B_TOP]), step=4)
p.stroke('butter_b', smooth([B_TOP] + LOW + [B_BOT]), step=4)

# ---- the 2, in front of everything: round top, the cut, the bottom ----
p.stroke('two', arc(CX, CY, R, R, 180, 360 - TH, start=S, end=E), Seg(E, V), Seg(V, B), step=1)
p.build()


def butter(seed):
    f = p.face('yellow', seed); f['fill'] = BUTTER
    return f


steps = [
    step('Start with a 2', 'Draw a big number 2: a round top, a straight slanted line down to the left, and a straight line along the bottom.', p.step(1)),
    step('The slice', 'Carry the round top on, round and down the right side. Tuck in a little on each side, then go straight down to the bottom.', p.step(2)),
    step('The crust', 'Draw a line just inside the edge, all the way round. Stop at the slanted line each time and carry on from its other side.', p.step(3)),
    step('The butter', 'Draw a big wobbly shape for the butter, nearly up to the crust. Stop at the slanted line and carry on from its other side.', p.step(4)),
    step('Colour brown', 'Colour the crust brown, all round the edge of both halves.', [p.face('brown', (24.3, 70)), p.face('brown', (50, 86.6))], use='brown'),
    step('Colour yellow', 'Colour the butter pale yellow, on both sides of the slanted line. Press gently.', [butter((40, 45)), butter((60, 65))], use='yellow'),
    step('Colour light brown', 'Colour the thin strip of toast between the crust and the butter light brown.',
         [p.face('lbrown', (27.9, 65.8)), p.face('lbrown', (49, 83.0))], use='lbrown'),
]
D = drawing('dx_toast_2', '2 is for Toast', 1, 10, 'things', TAGS,
            'A slice of buttered toast, cut into two equal halves. The number 2 is hiding in it: the round top, the cut and the bottom of the slice.',
            steps, ['brown', 'yellow', 'lbrown'])
ok = finish('num2toast', D, {'set': SET, 'slot': '2', 'kind': 'key', 'age_from': 4}, p)

if __name__ == '__main__':
    # the two halves, measured (each is closed by the cut)
    from fkit import chain_arr, poly_area
    names = ['two', 'side_l', 'side_r']
    up = abs(poly_area(chain_arr(p.net.face(p.pt(40, 45), names=names))))
    low = abs(poly_area(chain_arr(p.net.face(p.pt(60, 65), names=names))))
    print('    halves: top left %.1f, bottom right %.1f (%.2f%% bottom right)' % (up, low, 100 * low / (up + low)))
