"""Y is for Yellow banana (dx_banana_y), Food and drink A to Z, slot Y (21 Nov 2026).
Idea from his screenshot of MK Fine art's banana drawn from a Y (OmRNTcL9VsQ), drawn fresh in our style.

A banana with its top peeled. The two arms of the capital Y are the top edges of the two floppy pieces of peel,
where they fold away from the soft banana inside, and the line down the Y is the seam down the peel underneath.
Step 1 is a normal Y (the arms meet half-way down); step 3 carries the line on down to the bottom of the banana.
The banana inside stays white (the paper), the peel is yellow and the little stalk brown.

Version 1 (live 15:36) had a straight top and bottom. Version 2 bent the top only; he said it was not very good and
asked for the bottom to curve too, and for four variations of the final banana (16:03). So now the whole banana bends
to the right like a real banana: the soft top bends over to the right and the bottom curves round to the right, with
the Y kept straight and normal in the middle. Variations shown to him (VARIANTS below): 1 gentle curve, 2 big curve,
3 a bite out of the top, 4 hanging peel (droopy). Ripe brown spots were tried and left out (they looked like rivets).

The steps don't follow the video (which draws the Y, both peels, the bottom and stalk, then the top last, then the
peel lines, and colours everything yellow): ours draws the whole banana first (top, long line, bottom, stalk), then
each piece of peel with its line, and keeps the top white and the stalk brown.

    python3 build_banana.py [variant]      (no variant: the picked one, written as out/banana.json)
"""
import sys
from kit15 import *

YELLOW, BROWN = FILL['yellow'], FILL['brown']

# ---- 1: the Y (a normal capital Y: 24 wide, 30 tall, arms meeting half-way down) ----
AL, AR, J, S1 = P(38, 33.5), P(62, 33.5), P(50, 48.5), P(50, 63.5)


def hermite(fn, a, b, n):
    """n cubic pieces through fn from a to b, with the true slope at each joint (so the line is smooth)"""
    hs = (b - a) / n; e = 1e-5; out = []
    pts = [fn(a + i * hs) for i in range(n + 1)]
    der = [tuple((q - p) / (2 * e) for p, q in zip(fn(a + i * hs - e), fn(a + i * hs + e))) for i in range(n + 1)]
    for i in range(n):
        p0, p3 = pts[i], pts[i + 1]
        c1 = (p0[0] + der[i][0] * hs / 3, p0[1] + der[i][1] * hs / 3)
        c2 = (p3[0] - der[i + 1][0] * hs / 3, p3[1] - der[i + 1][1] * hs / 3)
        out.append(Seg(p0, c1, c2, p3))
    for s1, s2 in zip(out, out[1:]):
        s2.p[0] = s1.p[-1]
    return out


def tangent(fn, t):
    e = 1e-5; q0, q1 = fn(t - e), fn(t + e); L = math.dist(q0, q1)
    return ((q1[0] - q0[0]) / L, (q1[1] - q0[1]) / L)


def add(p, v, k=1.0):
    return (p[0] + v[0] * k, p[1] + v[1] * k)


VARIANTS = {
    # top: bend radius R and angle TH (degrees); bottom: bend radius RB and angle PH (degrees)
    'gentle': dict(R=50, TH=26, RB=60, PH=27),
    'big': dict(R=38, TH=34, RB=40, PH=38),
    'bite': dict(R=50, TH=26, RB=60, PH=27, bite=True),
    'spots': dict(R=44, TH=30, RB=48, PH=32, spots=True),
    'droopy': dict(R=44, TH=30, RB=48, PH=32, droopy=True),
}


def make(R, TH, RB, PH, bite=False, spots=False, droopy=False):
    TH, PH = math.radians(TH), math.radians(PH)
    arm_l, arm_r, stem = Seg(AL, J), Seg(AR, J), Seg(J, S1)

    # ---- 2: the soft banana top: both sides bend round the same centre, R to the right of the middle ----
    X0 = (50.0 + R, 33.5)
    R_IN, R_OUT0, R_OUT1 = R - 12.0, R + 12.0, R + 4.5

    def outer(th):
        r = R_OUT0 - (R_OUT0 - R_OUT1) * th / TH      # narrows evenly, so this side stays a smooth outward curve
        return (X0[0] - r * math.cos(th), X0[1] - r * math.sin(th))

    left_up = hermite(outer, 0.0, TH, 3)
    right_up = arc(X0[0], X0[1], R_IN, R_IN, 180, 180 + math.degrees(TH), start=AR)
    assert left_up[0].a == AL and right_up[0].a == AR, (left_up[0].a, right_up[0].a)
    H = (R_OUT1 - R_IN) / 2; RC = (R_IN + R_OUT1) / 2
    fwd = (math.sin(TH), -math.cos(TH)); across = (math.cos(TH), math.sin(TH))
    C = (X0[0] - RC * math.cos(TH), X0[1] - RC * math.sin(TH))
    O, I = left_up[-1].b, right_up[-1].b
    od = tangent(outer, TH)
    if not bite:
        T = P(*add(C, fwd, 1.3 * H))
        k1, k2 = 0.62 * 1.3 * H, 0.6 * H
        tip = [Seg(O, add(O, od, k1), add(T, across, -k2), T), Seg(T, add(T, across, k2), add(I, fwd, k1), I)]
    else:
        # a bite out of the top: the sides carry on a little, then three round bite marks across the top
        P1, P4 = P(*add(O, od, 3.2)), P(*add(I, fwd, 3.2))
        pts = [P1] + [P(P1[0] + (P4[0] - P1[0]) * f, P1[1] + (P4[1] - P1[1]) * f) for f in (1 / 3, 2 / 3)] + [P4]
        tip = [Seg(O, add(O, od, 1.1), add(P1, od, -1.1), P1)]
        for a, b in zip(pts, pts[1:]):
            dv = (b[0] - a[0], b[1] - a[1])
            tip.append(Seg(a, (a[0] + dv[0] * .15 - fwd[0] * 3.4, a[1] + dv[1] * .15 - fwd[1] * 3.4),
                           (a[0] + dv[0] * .85 - fwd[0] * 3.4, a[1] + dv[1] * .85 - fwd[1] * 3.4), b))
        tip.append(Seg(P4, add(P4, fwd, -1.1), add(I, fwd, 1.1), I))
    inside = left_up + tip + rev(right_up)
    chain_ok(inside)

    # ---- the peel's lower edge (needed now, because the bottom of the banana starts on it) ----
    TIP = P(27.6, 80) if droopy else P(24, 70.4)
    d = (-math.cos(math.radians(38 if droopy else 24)), math.sin(math.radians(38 if droopy else 24)))
    under = Seg(TIP, (31.5, 74) if droopy else (29, 65), (J[0] + 11 * d[0], J[1] + 11 * d[1]), J)
    BX = 38.6
    under_out, under_in = under.split(seg_x(under, BX))
    BL0 = under_out.b
    W0 = 50 - BX

    # ---- 3: the line down the Y carries on, curving round to the right at the bottom ----
    CB = (50.0 + RB, S1[1])
    E = P(CB[0] - RB * math.cos(PH), CB[1] + RB * math.sin(PH))
    seam = arc(CB[0], CB[1], RB, RB, 180, 180 - math.degrees(PH), start=S1, end=E)

    # ---- 4: the bottom of the banana, still in its peel: a long curved U round the line ----
    # Each side keeps an even gap from the middle line, narrowing smoothly all the way from under the peel to the
    # stalk, so the inside of the bend never bulges out.
    WE = 3.3
    S0 = S1[1] - BL0[1]; LT = S0 + RB * PH
    def mid(t):
        if t <= S0:
            return (50.0, BL0[1] + t), (0.0, 1.0)
        ph = (t - S0) / RB
        return (CB[0] - RB * math.cos(ph), CB[1] + RB * math.sin(ph)), (math.sin(ph), math.cos(ph))
    def half(t):
        return WE + (W0 - WE) * (1 - (t / LT) ** 2)
    def side(t, sg):
        (x, y), (dx, dy) = mid(t)
        h = half(t) * sg
        return (x - dy * h, y + dx * h)
    l_down = hermite(lambda t: side(t, 1), 0.0, LT, 5)
    r_down = hermite(lambda t: side(t, -1), 0.0, LT, 5)
    assert l_down[0].a == BL0, (l_down[0].a, BL0)
    SL, SR = l_down[-1].b, r_down[-1].b
    base = [Seg(SL, E), Seg(E, SR)]
    bottom = l_down + base + rev(r_down)

    # ---- 5: the little stalk, sticking out of the bottom ----
    dv = (math.sin(PH), math.cos(PH)); nv = (math.cos(PH), -math.sin(PH))   # along the stalk, and across it
    S2L, S2R = P(*add(add(SL, dv, 4.2), nv, 0.4)), P(*add(add(SR, dv, 4.2), nv, -0.4))
    STT = P(*add(E, dv, 5.0))
    stalk = [Seg(SL, add(SL, dv, 1.8), add(S2L, dv, -1.8), S2L), Seg(S2L, add(S2L, dv, 0.8), add(STT, nv, 1.2), STT),
             Seg(STT, add(STT, nv, -1.2), add(S2R, dv, 0.8), S2R), Seg(S2R, add(S2R, dv, -1.8), add(SR, dv, 1.8), SR)]

    # ---- 6 and 7: each floppy piece of peel, with a curved line on it ----
    if droopy:     # pieces of peel that hang down beside the banana, like a real peeled banana
        flap_top = [Seg(AL, (33.6, 31.4), (27.6, 32.2), (24.2, 36.4)),
                    Seg((24.2, 36.4), (20.6, 41), (19.6, 56), (21, 69)),
                    Seg((21, 69), (21.8, 76), (24.2, 80.4), TIP)]
    else:
        flap_top = [Seg(AL, (33.4, 31), (25.4, 31.4), (21, 36.4)),
                    Seg((21, 36.4), (16.6, 41.4), (15.8, 52), (17, 61)),
                    Seg((17, 61), (17.9, 67), (20.6, 70.6), TIP)]
    flap_l = flap_top + [under_out, under_in]
    flap_r = mirror(flap_l)
    assert flap_r[-1].a == r_down[0].a, (flap_r[-1].a, r_down[0].a)
    RIB0 = point_on_line(AL, J, 0.36)
    rib_l = Seg(RIB0, (36, 40.6), (28.6, 49), (26.6, 68)) if droopy else Seg(RIB0, (35.4, 40), (27, 46), (23.2, 60.5))
    rib_r = mirror([rib_l])[0]

    # ---- ripe spots (spots variant): little ovals on the peel, kept clear of every line ----
    spot_rings = []
    if spots:
        sp_lower = [side(LT * .5, .5), side(LT * .8, -.45)]
        spot_rings = [circle(*sp_lower[0], 1.9, ry=1.4), circle(*sp_lower[1], 1.6, ry=1.2),
                      circle(25.5, 41.5, 1.7, ry=1.3), circle(70.5, 53.5, 1.9, ry=1.4)]

    # ---- the colours ----
    peel_l = fill(YELLOW, *(flap_l + [Seg(J, AL)]))
    peel_r = fill(YELLOW, *(flap_r + [Seg(J, AR)]))
    lower = fill(YELLOW, *([under_in.rev()] + bottom + [flap_r[-1]]))
    stalk_fill = fill(BROWN, *(stalk + rev(base)))
    if spots:
        cuts = [d_fill(*r) for r in spot_rings]
        peel_l['cut'] = [cuts[2]]; peel_r['cut'] = [cuts[3]]; lower['cut'] = cuts[:2]

    steps = [
        step('Start with a Y', 'Draw a capital Y: two short slanting lines that meet in the middle, then a straight line down. This Y is hiding in the banana.',
             [line(arm_l), line(arm_r), line(stem)]),
        step('The banana', ('From the top of the left arm, draw up and over to the right. Make a bite at the top, then come back down to the right arm.' if bite else
                            'From the top of the left arm, draw up and over to the right, round the tip of the banana, then back down to the top of the right arm.'),
             [line(*inside)]),
        step('A longer line', 'Make the straight line of the Y much longer. At the bottom it curves round to the right.',
             [line(*seam)]),
        step('The bottom', 'Draw a long curved U round the line. Start a little lower than the middle of the Y, under the side of the banana, and end the same on the other side.',
             [line(*bottom)]),
        step('The stalk', 'Draw a little stalk at the end of the U.',
             [line(*stalk)]),
        step('Left peel', 'From the top of the left arm, draw a floppy piece of peel out and down to a tip, then back past the U to the middle. Add a curved line on it.',
             [line(*flap_l), line(rib_l)]),
        step('Right peel', 'Do the same on the right: a floppy piece of peel out, down to a tip and back to the middle, with a curved line on it.',
             [line(*flap_r), line(rib_r)]),
    ]
    if spots:
        steps.append(step('Ripe spots', 'Draw a few little spots on the peel, so it looks nice and ripe.', [ring(*r) for r in spot_rings]))
    steps.append(step('Colour yellow', 'Colour the peel yellow: both floppy pieces and the bottom. Leave the soft banana at the top white.'
                      + (' Leave the spots too.' if spots else ''), [peel_l, peel_r, lower], use='yellow'))
    steps.append(step('Colour brown', 'Colour the stalk brown.' if not spots else 'Colour the stalk and the spots brown.',
                      [stalk_fill] + ([fill(BROWN, *r) for r in spot_rings] if spots else []), use='brown'))

    desc = ('A yellow banana with its top peeled' + (' and a bite out of it' if bite else '') + (', nice and ripe' if spots else '')
            + '. The capital Y is hiding in it: the tops of the two pieces of peel are its arms, and the line down the peel is its tail.')
    return drawing('dx_banana_y', 'Y is for Yellow banana', 2, 10, 'things', ['Letters', 'Around the house'], desc, steps, ['yellow', 'brown'])


PICK = 'droopy'

if __name__ == '__main__':
    v = sys.argv[1] if len(sys.argv) > 1 else PICK
    save('banana' if len(sys.argv) == 1 else 'banana_' + v, make(**VARIANTS[v]),
         {'set': 'house-AZ', 'slot': 'Y', 'kind': 'key', 'age_from': 4})
