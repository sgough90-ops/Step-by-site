"""Step 1 fixes, round 2 (27 Nov 2026): drawings added after the 18 Nov review whose step 1 did not draw a
natural-looking letter or number. Same method as step1fix.py: the step-1 lines are cut so that step 1 is the natural
letter; the rest of each line goes into the step that carries on from it. The finished picture does not change.
Live from 27 Nov 2026: Z is for zebra and 6 is for Racer. Re-run this after rebuilding either of them
(build_zebra.py, build_racecars.py), before reapply.py.

    python3 step1fix2.py out/<name>.json [more.json ...]      # fixes each file in place
"""
import json, sys
from step1fix import cut, rev_d, join_d, ln, lines, fix, FIXES, set1, set2

def text_ok(P):
    for st in P['steps']:
        assert len(st['text']) <= 160, (P['id'], st['title'], len(st['text']))

FIXES.clear()

@fix('dx_zebra_z', 'The Z is 48 wide and 29 tall, and its top line runs on to the left, so it looks stretched flat.')
def _(P):
    s1 = lines(P['steps'][0]); s2 = lines(P['steps'][1]); s3 = lines(P['steps'][2])
    assert s1 == ['M 18 24 L 49 24 L 30 53 L 66 53']
    assert s2[0].startswith('M 18 24 C 14 24') and s3[0].endswith('C 72.88 54.44 70.16 53 66 53') and len(s2) == len(s3) == 1
    a, z, c = cut(s1[0], [(28.0, 24.0), (52.0, 53.0)])          # top extension, the Z, bottom extension
    set1(P, [z], 'Draw a capital Z: a line across the top, a slanting line down to the left, and a line across the bottom.')
    set2(P, [join_d(rev_d(a), s2[0])], 'Make the top line of the Z longer to the left. Then draw the front of its face, round its nose and back to its chin.')
    P['steps'][2]['add'] = [ln(join_d(s3[0], rev_d(c)))]
    P['steps'][2]['text'] = 'From its chin, draw the front of its neck, under its tummy and round its bottom. Then go along its back to the end of the Z.'

@fix('dx_racer_6', 'The top of the 6 runs on past its loop and goes flat, so the 6 looks stretched to the right.')
def _(P):
    s1 = lines(P['steps'][0]); s2 = lines(P['steps'][1])
    assert s1[0].startswith('M 42.64 47.72 C 31.6 46.8 13.2 53.24 12.74 65.2 ') and len(s1) == 1
    assert s2 == ['M 42.64 47.72 C 44.48 44.65 46.63 43.12 49.08 43.12 L 51.84 56.92']
    a, b = cut(s1[0], [(0, 0.196)])                                # the 6 now starts above the right of its loop
    set1(P, [b], 'Draw a number 6: a curvy line coming down, then a big round loop at the bottom. The loop is the back wheel.')
    set2(P, [join_d(rev_d(a), s2[0])],
         'Make the top of the 6 longer. Then draw a little hump going up and over, and come down in a straight line.')

def apply(path):
    P = json.load(open(path)); f, why = FIXES[P['id']]
    f(P); text_ok(P)
    json.dump(P, open(path, 'w'), ensure_ascii=False)
    print('fixed', P['id'], '-', why)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        apply(p)
