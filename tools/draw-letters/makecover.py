"""Makes a home-tile picture from a drawing that is in the page.

    python3 makecover.py <public dir> <port> <key> <out .webp>

Paints the finished picture with the app's own paintFinal at 600 x 600, makes the paper see-through (only the paper
joined to the edge, so white bits inside the drawing stay white), and crops it with an 18 px margin, like the other
cov_d_ pictures. Then point the set at it in COVERS (sb-extras.js section 6) and bump sb-extras.js?v= in the page.
"""
import sys, threading, functools, http.server, socketserver, time, base64, io
from collections import deque
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

pub, port, key, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]


class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


def serve():
    h = functools.partial(Q, directory=pub)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('127.0.0.1', port), h) as s: s.serve_forever()


threading.Thread(target=serve, daemon=True).start(); time.sleep(0.5)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 800, 'height': 800}, device_scale_factor=1)
    pg.goto('http://127.0.0.1:%d/draw/' % port); pg.wait_for_timeout(2000)
    url = pg.evaluate('''(k) => { if (!DX.has(k)) return null; var cv = document.createElement('canvas');
          cv.style.cssText = 'position:fixed;left:0;top:0;width:600px;height:600px;z-index:99999'; document.body.appendChild(cv);
          paintFinal(cv, {type: 'draw', key: k}); return cv.toDataURL('image/png') }''', key)
    b.close()
if not url: sys.exit('no drawing with key ' + key)
im = np.asarray(Image.open(io.BytesIO(base64.b64decode(url.split(',', 1)[1]))).convert('RGBA')).copy()
H, W = im.shape[:2]
paper = im[2, 2, :3].astype(int)
near = np.all(np.abs(im[:, :, :3].astype(int) - paper) <= 24, axis=2)
seen = np.zeros((H, W), bool); dq = deque()
for x in range(W):
    for y in (0, H - 1):
        if near[y, x] and not seen[y, x]: seen[y, x] = True; dq.append((y, x))
for y in range(H):
    for x in (0, W - 1):
        if near[y, x] and not seen[y, x]: seen[y, x] = True; dq.append((y, x))
while dq:
    y, x = dq.popleft()
    for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
        if 0 <= yy < H and 0 <= xx < W and near[yy, xx] and not seen[yy, xx]:
            seen[yy, xx] = True; dq.append((yy, xx))
im[seen, 3] = 0
ys, xs = np.where(im[:, :, 3] > 0)
m = 18
crop = im[max(ys.min() - m, 0):min(ys.max() + m + 1, H), max(xs.min() - m, 0):min(xs.max() + m + 1, W)]
Image.fromarray(crop).save(out, 'WEBP', quality=88)
print(out, crop.shape[1], 'x', crop.shape[0])
