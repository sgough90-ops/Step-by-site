"""2 is for Toast (dx_toast_2), Food and drink 1 to 9, slot 2. Version 3, 28 Nov 2026.
(Version 1, toast and jam, was 23 Nov. Version 2 went live on 28 Nov at 16:15: buttered toast cut into two equal halves.)

His asks on 28 Nov, in order: the cut should make two halves that look equal; a crust; the crust "naturally connected
on both slices"; butter "more spread" with no chunks. His picks: toast 1 of the crust sheet, butter 2 ("nearly to the
crust"), then "make live" (version 2).
Then (16:24): "make the number two look more natural as the first step". From the sheet of four ways he took number 2,
where the 2 moves to the butter and its round top curls into the cut, "but the butter doesn't have to change ... the
line they should just be connected naturally", then "create steps and put live" (16:59). That is version 3.

A slice of buttered toast, cut in two. The picture is the same as version 2 but for one short curved line. What changed
is which lines are the 2, so that step 1 is a 2 as it is written:
- The 2 is the round top of the BUTTER, a curl, the cut from the curl down to the bottom-left corner, and the bottom of
  the slice. In version 2 its round top was the top of the slice, and it had to stop at a sharp corner part-way round,
  because for two equal halves the cut starts on top of the slice (see TH).
- The curl is a round corner, RHO big, that leaves the butter's round top and lands on the cut, touching both. So the
  2's round top runs into its slanted line with no corner. It is the one new line in the finished picture; it is drawn
  on the butter, which is yellow on both sides of it.
- The butter keeps its shape. Its edge still carries on across the cut at one spot (B_TOP), as he asked for the crust.
  Where the edge is the 2's round top, and for a little way either side, it is a clean part of a circle (it was wavy
  there); the wavy edge runs into it without a corner. The new points were read off Claude's sketch of 28 Nov.
- Step 1 draws the 2 with a bottom line that stops just past the curl, so the 2 is not too wide at the bottom. Step 2
  carries that line on to the corner, and carries the cut on from the curl up to the edge of the slice.
- Equal halves, the crust and the colours are as in version 2: the cut starts TH degrees before the right-hand end of
  the dome (TH = 40.89 gives two halves of 2046 each); the crust is one even band, cut by the slanted line; the butter
  is the yellow pencil pressed gently (the pale yellow of V is for Vanilla cone).
Written in the sketch's numbers.

    python3 build_num_toast.py
"""
from ncommon import *

p = Pic(s=1.0, dx=0.0, dy=0.0)
CX, CY, R, XL, XR, BOT = 50, 41, 30, 22.5, 77.5, 89
TH = 40.89                                    # the cut starts this many degrees before the dome's right end (equal halves)
LIP, SH = 5.0, 52.0                           # the dome sticks out over the sides: straight down LIP, then tucked in by SH
T = 3.6                                       # how thick the crust is
RB = 22.17                                    # the butter's round top: part of a circle round the middle of the dome. The 2's round top
RHO = 8.5                                     # how big the curl is that joins the 2's round top to the cut (9 on the sheet he
                                              # picked from; at 9 the curl and the butter's edge part too slowly for check 6)
HOOK_FROM = 225.0                             # the 2's round top starts here (about half past ten on a clock)
BUTTER = '#fff0b3'                            # pale yellow, as the vanilla cone's ice cream (yellow pencil, pressed gently)

S = P(CX - R, CY)
E = P(CX + R * math.cos(math.radians(-TH)), CY + R * math.sin(math.radians(-TH)))
V, B = P(XL, BOT), P(XR, BOT)
on_cut = lambda t: (E[0] + (V[0] - E[0]) * t, E[1] + (V[1] - E[1]) * t)        # a point on the cut
TB = T * (BOT - E[1]) / (E[0] - XL)           # the bottom crust: its inside corner at the bottom left is then on the cut
RI = R - T


def circ(r, a, c=(CX, CY)):
    """the point at angle a (degrees, 0 = right, 90 = down) on the circle r round c"""
    return (c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a)))


def cut_meets_circle(r):
    """how far along the cut it meets the circle of radius r round the middle of the dome"""
    lo, hi = 0.0, 0.5
    for _ in range(60):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if math.dist(on_cut(m), (CX, CY)) > r else (lo, m)
    return (lo + hi) / 2


angle = lambda q: math.degrees(math.atan2(q[1] - CY, q[0] - CX)) % 360
C_TOP = P(*on_cut(cut_meets_circle(RI)))                                       # where the crust's inside line meets the cut, at the top
C_BOT = P(XL + T, BOT - TB)                                                    # and at the bottom left
A_TOP = angle(C_TOP)

# ---- the curl: a circle RHO big that touches the butter's round top from inside and touches the cut ----
CUT = math.dist(E, V)
UX, UY = (V[0] - E[0]) / CUT, (V[1] - E[1]) / CUT                              # down the cut
NX, NY = -UY, UX                                                               # square to the cut, towards the top-left half
D0 = (CX - E[0]) * NX + (CY - E[1]) * NY                                       # how far the middle of the dome is from the cut
A_N = math.degrees(math.atan2(NY, NX)) % 360
A_PM = A_N + math.degrees(math.acos((RHO - D0) / (RB - RHO)))                  # where the curl leaves the round top (angle on it)
CC = circ(RB - RHO, A_PM)                                                      # the middle of the curl
H0 = P(*circ(RB, HOOK_FROM))                                                   # the start of the 2
PM = P(*circ(RB, A_PM))                                                        # the curl leaves the round top here
Q = P(CC[0] - RHO * NX, CC[1] - RHO * NY)                                      # and lands on the cut here
BX = P(CC[0] + RHO + 1.5, BOT)                                                 # step 1's bottom line stops here, just past the curl
B_TOP = P(*on_cut(cut_meets_circle(RB)))                                       # where the butter's edge meets the cut, at the top
A_BT = angle(B_TOP)
B_BOT = P(*on_cut((E[0] - 30.24) / (E[0] - V[0])))                             # and at the bottom left

# ---- the slice (step 2): up the left side and over the top to where the cut starts, then down the right side ----
TOP = arc(CX, CY, R, R, 180, 360 - TH, start=S, end=E)
SIDE_L = [Seg(S, (CX - R, CY + LIP)), Seg((CX - R, CY + LIP), (CX - R, CY + LIP + 2.8), (XL, SH - 3.4), (XL, SH)), Seg((XL, SH), V)]
SIDE_R = arc(CX, CY, R, R, 360 - TH, 360, start=E, end=P(CX + R, CY)) + [
    Seg((CX + R, CY), (CX + R, CY + LIP)), Seg((CX + R, CY + LIP), (CX + R, CY + LIP + 2.8), (XR, SH - 3.4), (XR, SH)), Seg((XR, SH), B)]
p.stroke('slice_l', rev(SIDE_L), TOP, step=2)
p.stroke('slice_r', SIDE_R, step=2)
p.stroke('cut_top', Seg(Q, E), step=2)                                         # the cut carries on from the curl up to the edge
p.stroke('base_rest', Seg(BX, B), step=2)                                      # the bottom line carries on to the corner

# ---- the crust's inside line: one line for each half, both stopping at the same two spots on the cut ----
p.stroke('crust_a', arc(CX, CY, RI, RI, A_TOP, 180, start=C_TOP, end=P(CX - RI, CY)), Seg((CX - RI, CY), (CX - RI, CY + LIP)),
         Seg((CX - RI, CY + LIP), (CX - RI, CY + LIP + 2.8), (XL + T, SH - 3.4), (XL + T, SH)), Seg((XL + T, SH), C_BOT), step=3)
p.stroke('crust_b', Seg(C_BOT, (XR - T, BOT - TB)), Seg((XR - T, BOT - TB), (XR - T, SH)),
         Seg((XR - T, SH), (XR - T, SH - 3.4), (CX + RI, CY + LIP + 2.8), (CX + RI, CY + LIP)), Seg((CX + RI, CY + LIP), (CX + RI, CY)),
         arc(CX, CY, RI, RI, 360, A_TOP, start=P(CX + RI, CY), end=C_TOP), step=3)

# ---- the rest of the butter's edge (step 4) ----
# up the left side to the start of the 2: version 2's points, then four new ones that settle onto the circle
UP = [(29.5, 75.44), (29.93, 72.22), (30.24, 68.99), (29.92, 65.76), (29.19, 62.59), (28.76, 59.37), (29.05, 56.13), (29.62, 52.93),
      (29.6, 49.69), (28.84, 46.53), (27.83, 43.44), (27.43, 40.23),
      (28.46, 36.56), (29.73, 33.63), (30.84, 30.63), (32.27, 27.77)]
# from the cut round the bottom-right half: four new points that leave the circle, then version 2's points
LOW = [(69.6, 30.54), (70.75, 33.52), (71.16, 36.69), (71.4, 39.88),
       (71.67, 43.07), (71.54, 46.34), (70.71, 49.51), (69.63, 52.61),
       (69.26, 55.86), (69.79, 59.09), (70.63, 62.26), (71.05, 65.51), (70.75, 68.77), (70.2, 72.01), (70.06, 75.28), (69.86, 78.55),
       (68.21, 81.31), (65.2, 82.47), (61.97, 81.98), (58.78, 81.19), (55.52, 80.96), (52.26, 81.37), (49.01, 81.81), (45.74, 81.67),
       (42.53, 81.01), (39.29, 80.51), (36.02, 80.69), (32.76, 80.54)]
STEP = math.degrees(3.2 / RB)                 # the points are about 3.2 apart; one more on the circle each side gives the right slope
p.stroke('butter_a', smooth([B_BOT] + UP + [H0, circ(RB, HOOK_FROM + STEP)])[:-1], step=4)        # ends at the start of the 2
p.stroke('butter_c', arc(CX, CY, RB, RB, A_PM, A_BT, start=PM, end=B_TOP), step=4)                # the round top carries on to the cut
p.stroke('butter_b', smooth([circ(RB, A_BT - STEP), B_TOP] + LOW + [B_BOT])[1:], step=4)          # and on from its other side

# ---- the 2, in front of everything: round top, curl, the cut, the bottom ----
p.stroke('two', arc(CX, CY, RB, RB, HOOK_FROM, A_PM, start=H0, end=PM), arc(CC[0], CC[1], RHO, RHO, A_PM, A_N + 180, start=PM, end=Q),
         Seg(Q, V), Seg(V, BX), step=1)
p.build()


def butter(seed):
    f = p.face('yellow', seed); f['fill'] = BUTTER
    return f


steps = [
    step('Start with a 2', 'Draw a number 2: a round top that curls round, a straight slanted line down to the left, and a straight line along the bottom.', p.step(1)),
    step('The slice', 'Draw the slice round your 2: up, over the top and down each side. Carry the slanted line on up to the edge, and the bottom line on to the corner.', p.step(2)),
    step('The crust', 'Draw a line just inside the edge, all the way round. Stop at the slanted line each time and carry on from its other side.', p.step(3)),
    step('The butter', 'Carry the top of your 2 on both ways to make a big wobbly shape for the butter. Stop at the slanted line and carry on from its other side.', p.step(4)),
    step('Colour brown', 'Colour the crust brown, all round the edge of both halves.', [p.face('brown', (24.3, 70)), p.face('brown', (50, 86.6))], use='brown'),
    step('Colour yellow', 'Colour the butter pale yellow, on both sides of the slanted line and on both sides of the curl. Press gently.',
         [butter((40, 45)), butter((65.5, 27.5)), butter((60, 65))], use='yellow'),
    step('Colour light brown', 'Colour the thin strip of toast between the crust and the butter light brown.',
         [p.face('lbrown', (27.9, 65.8)), p.face('lbrown', (49, 83.0))], use='lbrown'),
]
D = drawing('dx_toast_2', '2 is for Toast', 1, 10, 'things', TAGS,
            'A slice of buttered toast, cut into two equal halves. The number 2 is hiding in it: the round top of the butter, the cut and the bottom of the slice.',
            steps, ['brown', 'yellow', 'lbrown'])
ok = finish('num2toast', D, {'set': SET, 'slot': '2', 'kind': 'key', 'age_from': 4}, p)

if __name__ == '__main__':
    # the two halves, measured (each is closed by the cut)
    from fkit import chain_arr, poly_area
    up = abs(poly_area(chain_arr(TOP + [Seg(E, V)] + rev(SIDE_L))))
    low = abs(poly_area(chain_arr(SIDE_R + [Seg(B, V), Seg(V, E)])))
    print('    halves: top left %.1f, bottom right %.1f (%.2f%% bottom right)' % (up, low, 100 * low / (up + low)))
    print('    the 2: starts at %s, curl leaves the round top at %s (%.1f degrees), lands on the cut at %s; bottom line to x %.2f in step 1'
          % (H0, PM, A_PM, Q, BX[0]))
    print('    butter meets the cut at %s (version 2: (68.34, 27.21)) and %s' % (B_TOP, B_BOT))
