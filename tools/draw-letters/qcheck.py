"""The same checks as check.py, quicker: lines whose boxes are apart are not compared for crossings.
    python3 qcheck.py out/<name>.json [steps whose lines may cross] [number of letter steps]"""
import json, os, sys
import numpy as np
import check as C

_slow = C.crossings


def crossings(A, B, stepA=4, stepB=4):
    a, b = np.array(A), np.array(B)
    if a[:, 0].max() + 0.6 < b[:, 0].min() or b[:, 0].max() + 0.6 < a[:, 0].min() or a[:, 1].max() + 0.6 < b[:, 1].min() or b[:, 1].max() + 0.6 < a[:, 1].min():
        return []
    return _slow(A, B, stepA, stepB)


C.crossings = crossings
if __name__ == '__main__':
    P = json.load(open(sys.argv[1]))
    allow = tuple(a for a in sys.argv[2].split(',') if a) if len(sys.argv) > 2 else ()
    nlet = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    wf = sys.argv[1][:-5] + '.white.json'
    white = tuple(json.load(open(wf))) if os.path.exists(wf) else ()
    r, _ = C.check(P, allow_cross=allow, letter_steps=nlet, white=white)
    sys.exit(0 if all(g for _, g, _ in r) else 1)
