"""Opens the Step by Draw app in headless Chrome and tests drawings.

    python3 apptest.py <public dir> <port> <out prefix> key1 key2 ...

For every key: (phone and Chromebook size) home -> set -> slot -> start -> every step -> finish -> Make it move button,
with screenshots and page errors. Also writes the app's own checker results for every drawing, for a before/after compare,
and every set's filled slots and every card's step count.
"""
import sys, json, threading, functools, http.server, socketserver, time
from playwright.sync_api import sync_playwright

pub, port, pre = sys.argv[1], int(sys.argv[2]), sys.argv[3]
keys = sys.argv[4:]


class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


def serve():
    h = functools.partial(Q, directory=pub)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('127.0.0.1', port), h) as s: s.serve_forever()


threading.Thread(target=serve, daemon=True).start(); time.sleep(0.5)
URL = 'http://127.0.0.1:%d/draw/' % port
report = {'errors': [], 'all': {}, 'runs': []}

with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    for vp, touch, tag in [((390, 844), True, 'phone'), ((1366, 768), False, 'book')]:
        ctx = b.new_context(viewport={'width': vp[0], 'height': vp[1]}, has_touch=touch, is_mobile=touch, device_scale_factor=2 if touch else 1)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text + ' ' + str(m.location.get('url', ''))[:90]) if m.type == 'error' else None)
        pg.goto(URL); pg.wait_for_timeout(1500)
        if tag == 'phone':
            report['all'] = pg.evaluate('''() => { var out = {}; (REALS.draw||[]).forEach(function(r){ if(!r.key||!DX.has(r.key)) return;
                 try { var R = SBE.validate(Object.assign({kind:'draw'}, DX.get(r.key))); out[r.key] = R.map(function(x){ return [x.rule, !!x.pass, x.msg] }); } catch(e) { out[r.key] = 'ERR ' + e } }); return out; }''')
            report['slots'] = pg.evaluate('''() => { var o = {}; (window.SBSETS||[]).forEach(function(c){ c.cols.forEach(function(col){ o[col.id] = Object.keys(col.has||{}).length }) }); return o }''')
            report['cards'] = pg.evaluate('''() => (REALS.draw||[]).filter(function(r){ return r.key && DX.has(r.key) }).map(function(r){ return [r.key, r.t, r.lvl, r.steps, DX.n(r.key)] })''')
        for key in keys:
            run = {'key': key, 'size': tag}
            pg.goto(URL); pg.wait_for_timeout(1200)
            setid = pg.evaluate("""(k) => { var r = null; (window.SBSETS||[]).forEach(function(c){ c.cols.forEach(function(col){ var h = col.has||{}; Object.keys(h).forEach(function(s){ if (h[s] === k) r = [col.id, s] }) }) }); return r }""", key)
            run['slot'] = setid
            if not setid:
                run['problem'] = 'slot not found'; report['runs'].append(run); continue
            pg.locator('[data-set="%s"]' % setid[0]).first.click(); pg.wait_for_timeout(700)
            if tag == 'phone': pg.screenshot(path='%s-%s-%s-set.png' % (pre, key, tag))
            pg.locator('.sbslot.sbm[data-k="%s"]' % key).first.click(); pg.wait_for_timeout(600)
            if pg.locator('#pvgo').is_visible():
                pg.locator('#pvgo').click(); pg.wait_for_timeout(600)
            if pg.locator('#mtgo').is_visible():
                pg.locator('#mtgo').click(); pg.wait_for_timeout(600)
            n = pg.evaluate('(k)=>DX.n(k)', key); run['steps'] = n
            scroll = []; i = 0
            for i in range(n + 3):
                if pg.locator('#dn').is_visible(): break
                sh = pg.evaluate('()=>[document.scrollingElement.scrollHeight, innerHeight]')
                if sh[0] > sh[1] + 1: scroll.append((i, sh))
                if tag == 'phone' and i in (0, 1, n - 1):
                    pg.wait_for_timeout(700); pg.screenshot(path='%s-%s-%s-step%d.png' % (pre, key, tag, i + 1))
                pg.locator('#vnext').click(); pg.wait_for_timeout(300)
            pg.wait_for_timeout(800)
            run['finish'] = pg.locator('#dn').is_visible(); run['clicks'] = i; run['scroll'] = scroll
            if tag == 'phone': pg.screenshot(path='%s-%s-%s-finish.png' % (pre, key, tag))
            if pg.locator('#funbtn').is_visible():
                pg.locator('#funbtn').click(); pg.wait_for_timeout(600)
                run['mim'] = pg.locator('#mim').is_visible()
            report['runs'].append(run)
        report['errors'].append([tag, errs]); ctx.close()
    b.close()
json.dump(report, open(pre + '-report.json', 'w'), indent=1)
for r in report['runs']: print(r)
for t, e in report['errors']: print(t, 'errors:', len(e), e[:8])
