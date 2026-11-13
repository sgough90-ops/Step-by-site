/* 12 Nov 2026: Make it move films.
   A drawing that has ready-made films (D is for Digger, T is for Tiger, a is for ambulance for now) gets a film picker when its
   Make it move button is tapped: Silly, Wonky and Starring role, plus the camera button for the existing
   Make it move with a photo of your own drawing. Icons only, no words on screen.
   Drawings without films keep the Make it move button exactly as before.
   Films live in /mim-films/<drawing key>/ as silly.mp4, wonky.mp4, star.mp4 and poster.jpg.
   12 Nov 2026 (later): every film ends on the Step by Draw end page (logo, step-by.com, bouncing stars), which is
   part of the film, so shared films carry it. The end page stays on screen with a replay button and a big green
   share button. Share asks the grown-ups times question first (the same gate as the shopping links), then opens
   the phone's share sheet with the film (Instagram, Messages, Save Video). Computers download the film instead. */
(function () {
  "use strict";
  var FILMS = {
    dx_digger_d: { dir: "mim-films/dx_digger_d/", v: "2", name: "digger" },   /* v2: ends on the Step by Draw end page */
    /* 13 Nov 2026: T is for Tiger, remade: a real tigress body (ChatGPT photos, cut out of green) wearing the
       4-year-old's drawn face, with drawn props (butterfly, flower, rock, sun). Silly = sneezes a flower bald and
       hiccups into the sky; Wonky = the lame chase (pounces an inch, tiny "rawr", the butterfly roars back);
       Starring role = the dawn roar that wakes the jungle. Founder's voices (incl. his tiger sounds); Claude's
       stand-in tunes on sampled instruments (TimGM6mb, GPL-2) until licensed music is chosen.
       v3 replaces the felt-tiger films (v2). */
    dx_tiger_t: { dir: "mim-films/dx_tiger_t/", v: "3", name: "tiger" },
    /* 13 Nov 2026: a is for ambulance, drawn as a child would colour it, on the founder's street. Silly slot = Icy rush
       (a call on a snowy night, it slips on the ice), Wonky slot = Rainy day (sad, soggy, through puddles),
       Starring role = the teddy rescue. Founder's voices; Claude's stand-in tunes (TimGM6mb, GPL-2) */
    dx_ambulance_a: { dir: "mim-films/dx_ambulance_a/", v: "1", name: "ambulance" }
  };
  var TYPES = [["silly", "Silly film"], ["wonky", "Wonky film"], ["star", "Starring role film"]];
  var NAVY = "#081130";
  var ICON = {
    silly: '<svg viewBox="0 0 60 60" aria-hidden="true"><circle cx="30" cy="30" r="26" fill="#ffc531" stroke="' + NAVY + '" stroke-width="3"/><circle cx="21" cy="24" r="6" fill="#fff" stroke="' + NAVY + '" stroke-width="2.5"/><circle cx="39" cy="22" r="4" fill="#fff" stroke="' + NAVY + '" stroke-width="2.5"/><circle cx="22" cy="25" r="2.5" fill="' + NAVY + '"/><circle cx="39" cy="22" r="2" fill="' + NAVY + '"/><path d="M16 36q14 16 28 0z" fill="' + NAVY + '"/><path d="M27 44q4 6 8 0" fill="#e5484d"/></svg>',
    wonky: '<svg viewBox="0 0 60 60" aria-hidden="true"><g transform="rotate(-14 30 30)"><circle cx="30" cy="30" r="26" fill="#ffc531" stroke="' + NAVY + '" stroke-width="3"/><path d="M17 25q13-13 26 0" stroke="' + NAVY + '" stroke-width="3.4" fill="none" stroke-linecap="round"/><ellipse cx="22" cy="38" rx="3.2" ry="4.2" fill="' + NAVY + '"/><ellipse cx="38" cy="38" rx="3.2" ry="4.2" fill="' + NAVY + '"/></g></svg>',
    star: '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M8 54h48" stroke="' + NAVY + '" stroke-width="4" stroke-linecap="round"/><path d="M14 54l6-16h24l6 16" fill="#e5484d" stroke="' + NAVY + '" stroke-width="3" stroke-linejoin="round"/><path d="M32 6l6.2 12.6 13.8 2-10 9.8 2.4 13.8L32 37.7l-12.4 6.5 2.4-13.8-10-9.8 13.8-2z" fill="#ffc531" stroke="' + NAVY + '" stroke-width="3" stroke-linejoin="round"/></svg>',
    cam: '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M10 22a5 5 0 0 1 5-5h7l4-6h12l4 6h7a5 5 0 0 1 5 5v24a5 5 0 0 1-5 5H15a5 5 0 0 1-5-5z" fill="#fff" stroke="' + NAVY + '" stroke-width="3.2" stroke-linejoin="round"/><circle cx="32" cy="33" r="10" fill="#d6ebff" stroke="' + NAVY + '" stroke-width="3.2"/></svg>',
    back: '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>',
    close: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    replay: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12a8 8 0 1 0 3-6.2"/><path d="M4 4v5h5"/></svg>',
    share: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 14.5V3M7.5 7.5L12 3l4.5 4.5"/><path d="M8.5 10.5H7a2 2 0 0 0-2 2V19a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6.5a2 2 0 0 0-2-2h-1.5"/></svg>',
    tick: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4.5 12.5l5 5 10-11"/></svg>',
    lock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/></svg>'
  };
  function G(id) { return document.getElementById(id); }
  function curKey() { try { return (typeof V !== "undefined" && V.p && V.p.key) || null; } catch (e) { return null; } }

  var css = document.createElement("style");
  css.textContent =
    "#mfpick{position:fixed;inset:0;z-index:900;background:#e3f1ff;display:flex;flex-direction:column;" +
    "padding:max(14px,env(safe-area-inset-top)) max(16px,env(safe-area-inset-right)) max(18px,env(safe-area-inset-bottom)) max(16px,env(safe-area-inset-left))}" +
    "#mfpick.off,#mfplay.off,#mfgate.off,#mfplay .mfend.off{display:none}" +
    "#mfpick .mftop{display:flex}" +
    "#mfpick .mfbody{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px;min-height:0}" +
    "#mfpick .mfprev{height:min(46vh,420px);aspect-ratio:9/16;border-radius:24px;overflow:hidden;background:" + NAVY + ";border:5px solid #fff;box-shadow:0 8px 0 rgba(8,17,48,.22);padding:0;cursor:pointer}" +
    "#mfpick .mfprev img{width:100%;height:100%;object-fit:cover;display:block}" +
    "#mfpick .mfrow{display:flex;gap:16px;justify-content:center}" +
    "#mfpick .mff{width:84px;height:84px;border-radius:26px;padding:8px;border:0;background:#fff;box-shadow:0 6px 0 rgba(8,17,48,.3);cursor:pointer}" +
    "#mfpick .mff svg{width:100%;height:100%;display:block}" +
    "#mfpick .mff.seen{box-shadow:0 0 0 4px #ffc531,0 6px 0 rgba(8,17,48,.3)}" +
    "#mfpick .mff:active,#mfpick .mfcam:active,#mfplay .shc:active,#mfgate .shc:active{transform:translateY(4px)}" +
    "#mfpick .mfcam{width:64px;height:64px;border-radius:50%;border:0;background:#fff;box-shadow:0 5px 0 rgba(8,17,48,.3);display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0}" +
    "#mfpick .mfcam svg{width:42px;height:42px}" +
    "#mfplay{position:fixed;inset:0;z-index:1000;background:#000;display:flex;align-items:center;justify-content:center}" +
    "#mfplay video{width:100%;height:100%;object-fit:contain;background:#000}" +
    /* the film ends on the cream Step by Draw end page, so the screen around it turns cream too */
    "#mfplay.done,#mfplay.done video{background:#fff6e0}" +
    "#mfplay .mfx{position:absolute;left:max(14px,env(safe-area-inset-left));top:max(14px,env(safe-area-inset-top))}" +
    "#mfplay .mfend{position:absolute;left:0;right:0;bottom:0;display:flex;align-items:center;justify-content:center;gap:30px;" +
    "padding:0 max(16px,env(safe-area-inset-right)) max(26px,calc(env(safe-area-inset-bottom) + 12px)) max(16px,env(safe-area-inset-left))}" +
    /* the app's .big class stretches buttons (flex:1); keep these round */
    "#mfplay .mfend .shc,#mfgate .shc{flex:none}" +
    "#mfplay .mfend .shc.big,#mfgate .shc.big{width:92px;height:92px;border-radius:50%}" +
    "#mfplay .shc.done,#mfgate .shc.done{color:#2fb344}" +
    "#mfgate{position:fixed;inset:0;z-index:1100;background:#fff6e0;display:flex;flex-direction:column;" +
    "padding:max(14px,env(safe-area-inset-top)) max(16px,env(safe-area-inset-right)) max(18px,env(safe-area-inset-bottom)) max(16px,env(safe-area-inset-left))}" +
    "#mfgate .mftop{display:flex}" +
    "#mfgate .mfgin{flex:1;min-height:0;width:100%;max-width:380px;margin:0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center}" +
    "#mfgate .gate{flex:none;padding-top:0}" +
    "@media (max-height:700px){#mfpick .mfprev{height:40vh}#mfpick .mff{width:70px;height:70px;border-radius:22px}#mfpick .mfcam{width:56px;height:56px}}";
  document.head.appendChild(css);

  var KEY = null, KIND = null, FILE = {}, FILEP = {};
  function build() {
    if (G("mfpick")) return;
    var s = document.createElement("section");
    s.id = "mfpick"; s.className = "off";
    s.setAttribute("aria-label", "Make it move films");
    var faces = TYPES.map(function (t) {
      return '<button type="button" class="mff" data-t="' + t[0] + '" aria-label="' + t[1] + '">' + ICON[t[0]] + "</button>";
    }).join("");
    s.innerHTML =
      '<div class="mftop"><button type="button" class="round" id="mfback" aria-label="Back">' + ICON.back + "</button></div>" +
      '<div class="mfbody">' +
      '<button type="button" class="mfprev" id="mfprev" aria-label="Silly film"><img id="mfposter" alt=""></button>' +
      '<div class="mfrow">' + faces + "</div>" +
      '<button type="button" class="mfcam" id="mfcam" aria-label="Make your own drawing move">' + ICON.cam + "</button>" +
      "</div>";
    document.body.appendChild(s);
    G("mfback").onclick = close;
    G("mfprev").onclick = function () { play("silly"); };
    G("mfcam").onclick = own;
    [].forEach.call(s.querySelectorAll(".mff"), function (b) {
      b.onclick = function () { play(b.getAttribute("data-t")); };
    });
    var w = document.createElement("div");
    w.id = "mfplay"; w.className = "off";
    w.innerHTML = '<video playsinline webkit-playsinline preload="auto"></video>' +
      '<button type="button" class="round mfx" aria-label="Close">' + ICON.close + "</button>" +
      '<div class="mfend off" id="mfend">' +
      '<button type="button" class="shc" id="mfagain" aria-label="Watch again">' + ICON.replay + "</button>" +
      '<button type="button" class="shc big keep" id="mfshare" aria-label="Share my film">' + ICON.share + "</button>" +
      "</div>";
    document.body.appendChild(w);
    w.querySelector(".mfx").onclick = stop;
    w.querySelector("video").addEventListener("ended", endUI);
    G("mfagain").onclick = replay;
    G("mfshare").onclick = shareTap;
    var g = document.createElement("section");
    g.id = "mfgate"; g.className = "off";
    g.setAttribute("aria-label", "Grown-ups only");
    g.innerHTML = '<div class="mftop"><button type="button" class="round" id="mfgback" aria-label="Back">' + ICON.back + "</button></div>" +
      '<div class="mfgin" id="mfgin"></div>';
    document.body.appendChild(g);
    G("mfgback").onclick = gateClose;
  }
  function open(k) {
    build(); KEY = k;
    var f = FILMS[k];
    G("mfposter").src = f.dir + "poster.jpg?v=" + f.v;
    G("mfpick").classList.remove("off");
  }
  function close() { stop(); var s = G("mfpick"); if (s) s.classList.add("off"); }
  function play(t) {
    var f = FILMS[KEY]; if (!f) return;
    KIND = t; hideEnd(); setShare(false);
    var w = G("mfplay"), v = w.querySelector("video");
    v.poster = f.dir + "poster.jpg?v=" + f.v;
    v.src = f.dir + t + ".mp4?v=" + f.v;
    w.classList.remove("off");
    var b = document.querySelector('#mfpick .mff[data-t="' + t + '"]'); if (b) b.classList.add("seen");
    go(v);
  }
  function go(v) { try { var p = v.play(); if (p && p.catch) p.catch(function () { v.controls = true; }); } catch (e) { v.controls = true; } }
  function stop() {
    gateClose(); hideEnd();
    var w = G("mfplay"); if (!w) return;
    var v = w.querySelector("video");
    try { v.pause(); } catch (e) {}
    v.removeAttribute("src"); try { v.load(); } catch (e) {}
    v.controls = false;
    w.classList.add("off");
  }
  /* the film has ended on its Step by Draw end page: keep it on screen with replay and share */
  function endUI() {
    var w = G("mfplay"); if (!w || w.classList.contains("off")) return;
    w.querySelector("video").controls = false;
    w.classList.add("done");
    G("mfend").classList.remove("off");
  }
  function hideEnd() {
    var w = G("mfplay"); if (w) w.classList.remove("done");
    var e = G("mfend"); if (e) e.classList.add("off");
  }
  function replay() { var v = G("mfplay").querySelector("video"); hideEnd(); try { v.currentTime = 0; } catch (e) {} go(v); }
  function setShare(done) {
    var b = G("mfshare"); if (!b) return;
    b.className = done ? "shc big done" : "shc big keep";
    b.innerHTML = done ? ICON.tick : ICON.share;
    b.setAttribute("aria-label", done ? "Shared" : "Share my film");
  }

  /* ---- sharing: the grown-ups question first, then the phone's share sheet with the film ---- */
  function fid(k, t) { var f = FILMS[k]; return f ? k + "/" + t + "/" + f.v : ""; }
  function fileName(k, t) { return "step-by-draw-" + ((FILMS[k] && FILMS[k].name) || "film") + "-" + t + ".mp4"; }
  function getFile(k, t) {
    var id = fid(k, t), f = FILMS[k];
    if (!f) return Promise.reject(new Error("no film"));
    if (FILE[id]) return Promise.resolve(FILE[id]);
    if (!FILEP[id]) FILEP[id] = fetch(f.dir + t + ".mp4?v=" + f.v).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status); return r.blob();
    }).then(function (b) {
      var x; try { x = new File([b], fileName(k, t), { type: "video/mp4" }); } catch (e) { x = b; }
      FILE[id] = x; return x;
    }).catch(function (e) { delete FILEP[id]; throw e; });
    return FILEP[id];
  }
  function shareTap() {
    if (!KEY || !KIND) return;
    getFile(KEY, KIND).catch(function () {});  /* download it while the grown-up answers */
    gateOpen();
  }
  var GA = 0, GB = 0, ENT = "";
  function gateOpen() { GA = 6 + Math.floor(Math.random() * 4); GB = 6 + Math.floor(Math.random() * 4); ENT = ""; drawGate(); G("mfgate").classList.remove("off"); }
  function gateClose() { var g = G("mfgate"); if (g) g.classList.add("off"); }
  /* a simple times question, two numbers from 6 to 9, the same as the app's grown-ups gate */
  function drawGate() {
    G("mfgin").innerHTML = '<div class="gate"><div class="gl">' + ICON.lock + '</div><div class="gt">Grown-ups only</div>' +
      '<div class="gs">Ask a grown-up to type the answer</div><div class="gw gmul">' + GA + " × " + GB + " =</div>" +
      '<div class="gd" id="mfgd">' + [0, 1].map(function (i) { return "<i>" + (ENT[i] || "") + "</i>"; }).join("") + "</div>" +
      '<div class="gk" id="mfgk">' + [1, 2, 3, 4, 5, 6, 7, 8, 9].map(function (d) { return '<button type="button" data-k="' + d + '" aria-label="' + d + '">' + d + "</button>"; }).join("") +
      '<button type="button" data-k="del" aria-label="Delete">' + ICON.back + '</button><button type="button" data-k="0" aria-label="0">0</button>' +
      '<button type="button" class="ok" data-k="ok" aria-label="Enter">' + ICON.tick + "</button></div></div>";
    [].forEach.call(document.querySelectorAll("#mfgk button"), function (x) { x.onclick = function () { key(x.getAttribute("data-k")); }; });
  }
  function key(k) {
    if (k === "del") { ENT = ENT.slice(0, -1); drawGate(); return; }
    if (k === "ok") { submit(); return; }
    if (ENT.length < 2) ENT += k;
    drawGate();
    /* checked straight away, not on a timer, so the phone still counts the grown-up's tap when the share sheet opens */
    if (ENT.length === 2) submit();
  }
  function submit() {
    if (ENT === String(GA * GB)) { passed(); return; }
    var d = G("mfgd"); if (d) d.classList.add("shake");
    setTimeout(function () { var g = G("mfgate"); if (g && !g.classList.contains("off")) gateOpen(); }, 380);
  }
  function passed() {
    var f = FILE[fid(KEY, KIND)];
    if (f) { gateClose(); send(f); return; }
    ready();
  }
  /* the film is still downloading (or the phone wants one more tap): one big share button that the grown-up taps */
  function ready() {
    G("mfgin").innerHTML = '<button type="button" class="shc big keep wait" id="mfgo" aria-label="Share my film" disabled>' + ICON.share + "</button>";
    G("mfgate").classList.remove("off");
    var k = KEY, t = KIND, b = G("mfgo");
    b.onclick = function () { var f = FILE[fid(k, t)]; if (f) { gateClose(); send(f); } };
    getFile(k, t).then(function () { var x = G("mfgo"); if (x) { x.disabled = false; x.classList.remove("wait"); } },
      function () { setTimeout(function () { var x = G("mfgo"); if (x && !G("mfgate").classList.contains("off")) ready(); }, 1500); });
  }
  function send(f) {
    var ok = function () { setShare(true); };
    try {
      if (navigator.canShare && navigator.maxTouchPoints > 0 && navigator.canShare({ files: [f] })) {
        navigator.share({ files: [f] }).then(ok, function (e) { if (e && e.name === "NotAllowedError") ready(); });
        return;
      }
    } catch (e) {}
    var u = URL.createObjectURL(f), a = document.createElement("a");
    a.href = u; a.download = f.name || fileName(KEY, KIND);
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(u); }, 60000);
    ok();
  }

  /* the camera button: the existing Make it move with a photo of the child's own drawing, from the button that
     opened the films (the finish screen's, or the one on a photo in My drawings) */
  var SRC = null;
  function own() {
    close();
    var b = SRC || G("funbtn");
    if (b && typeof b.onclick === "function") b.onclick.call(b, { stopPropagation: function () {}, preventDefault: function () {} });
  }
  /* catch the Make it move buttons before their own handlers, only for drawings that have films:
     the finish screen's (#funbtn) and the one on a drawing's photo in My drawings (.mdxmim, 12 Nov evening) */
  document.addEventListener("click", function (e) {
    var b = e.target && e.target.closest && e.target.closest("#funbtn,.mdxmim");
    if (!b) return;
    var k = b.id === "funbtn" ? curKey() : b.getAttribute("data-key");
    if (!k || !FILMS[k]) return;
    e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation();
    SRC = b; open(k);
  }, true);
  window.__mimFilms = { films: FILMS, open: open, close: close, play: play };
})();
