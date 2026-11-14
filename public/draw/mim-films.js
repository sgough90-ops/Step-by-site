/* 12 Nov 2026: Make it move films.
   A drawing that has ready-made films (D is for Digger, T is for Tiger, a is for ambulance for now) gets a film picker when its
   Make it move button is tapped: Silly, Wonky and Starring role, plus the camera button for the existing
   Make it move with a photo of your own drawing. Icons only, no words on screen.
   Drawings without films keep the Make it move button exactly as before.
   Films live in /mim-films/<drawing key>/ as silly.mp4, wonky.mp4, star.mp4 and poster.jpg.
   12 Nov 2026 (later): every film ends on the Step by Draw end page (logo, step-by.com, bouncing stars), which is
   part of the film, so shared films carry it. The end page stays on screen with a replay button and a big green
   share button. Share asks the grown-ups times question first (the same gate as the shopping links), then opens
   the phone's share sheet with the film (Instagram, Messages, Save Video). Computers download the film instead.
   13 Nov 2026 (afternoon): the tiger's films screen never shows the drawn face the films were made with (it showed as
   "the old tiger"): its picture has a blank paper face with the camera until the child's own photo is on it, Make it
   move on the finish screen always starts without a photo (earlier ones stay in My drawings), and the camera button
   opens the phone's camera (and Photo Library while testing) in one tap.
   13 Nov 2026 (later still): Make it move on a finish screen opens the blank camera page for every drawing (photo saved
   or not); the tiger's films follow once the photo is in. And the photo is cleaned before it goes on (cleanFace): only
   the drawing is kept, as one solid piece of paper (no lined-paper lines, paper edge or holes), so it is sized from the
   drawing itself and fits the tiger instead of coming out far too big. */
(function () {
  "use strict";
  var FILMS = {
    dx_digger_d: { dir: "mim-films/dx_digger_d/", v: "4", name: "digger" },   /* v2: ends on the Step by Draw end page */
    /* 13 Nov 2026: T is for Tiger, remade: a real tigress body (ChatGPT photos, cut out of green) wearing the
       4-year-old's drawn face, with drawn props (butterfly, flower, rock, sun). Silly = sneezes a flower bald and
       hiccups into the sky; Wonky = the lame chase (pounces an inch, tiny "rawr", the butterfly roars back);
       Starring role = the dawn roar that wakes the jungle. Founder's voices (incl. his tiger sounds); Claude's
       stand-in tunes on sampled instruments (TimGM6mb, GPL-2) until licensed music is chosen.
       v3 replaces the felt-tiger films (v2). */
    /* 13 Nov 2026 (later): face.json lets the child's own photographed face replace the drawn one in all three films
       (see "the child's own face" below); silly.m4a etc. are the films' sound for the shareable recording */
    dx_tiger_t: { dir: "mim-films/dx_tiger_t/", v: "5", name: "tiger", face: "1" },
    /* 13 Nov 2026: a is for ambulance, drawn as a child would colour it, on the founder's street. Silly slot = Icy rush
       (a call on a snowy night, it slips on the ice), Wonky slot = Rainy day (sad, soggy, through puddles),
       Starring role = the teddy rescue. Founder's voices; Claude's stand-in tunes (TimGM6mb, GPL-2) */
    dx_ambulance_a: { dir: "mim-films/dx_ambulance_a/", v: "3", name: "ambulance" }
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
    /* the child's own face: the film is drawn into this canvas, which sits exactly over the video */
    "#mfplay canvas.mfcv{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;pointer-events:none}" +
    "#mfplay canvas.mfcv.off{display:none}" +
    "#mfpick .mfprev{position:relative}" +
    "#mfpick .mfprev canvas{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}" +
    "#mfpick .mfprev canvas.off,#mfpick .mfcam.off{display:none}" +
    /* 13 Nov 2026: a film that can wear the child's face never shows its own poster (it has the drawn face the films
       were made with); the picture is drawn into the canvas instead, with a blank paper face until there is a photo */
    "#mfpick .mfprev img.off{visibility:hidden}" +
    "#mfpick .mfcam.again{animation:mfno .5s}" +
    "@keyframes mfno{0%,100%{translate:0}25%{translate:-8px}75%{translate:8px}}" +
    /* 14 Nov 2026: the end page's sound is now just a fast pencil scribble as it comes on (the "Wahey!" and whoosh are off)
       on all nine films; film versions bumped */
    /* the film ends on the Step by Draw end page (13 Nov 2026: sky-blue coloured pencil, "Free \u00b7 No ads \u00b7 No sign-up" at the top,
       the founder's "Wahey!" and a soft whoosh), so the screen around it turns that blue too */
    "#mfplay.done,#mfplay.done video{background:#bbddf8}" +
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
      '<button type="button" class="mfprev" id="mfprev" aria-label="Silly film"><img id="mfposter" alt=""><canvas id="mfpcv" class="off" width="540" height="960"></canvas></button>' +
      '<div class="mfrow">' + faces + "</div>" +
      '<button type="button" class="mfcam" id="mfcam" aria-label="Make your own drawing move">' + ICON.cam + "</button>" +
      "</div>";
    document.body.appendChild(s);
    G("mfback").onclick = close;
    /* the picture plays the Silly film; while it has the blank face and the camera on it, it takes the photo instead */
    G("mfprev").onclick = function () {
      var st = G("mfprev").getAttribute("data-st");
      if (st === "cam") own(); else if (st !== "wait") play("silly");
    };
    G("mfcam").onclick = own;
    [].forEach.call(s.querySelectorAll(".mff"), function (b) {
      b.onclick = function () { play(b.getAttribute("data-t")); };
    });
    var w = document.createElement("div");
    w.id = "mfplay"; w.className = "off";
    w.innerHTML = '<video playsinline webkit-playsinline preload="auto"></video><canvas class="mfcv off" id="mfcv" width="720" height="1280"></canvas>' +
      '<button type="button" class="round mfx" aria-label="Close">' + ICON.close + "</button>" +
      '<div class="mfend off" id="mfend">' +
      '<button type="button" class="shc" id="mfagain" aria-label="Watch again">' + ICON.replay + "</button>" +
      '<button type="button" class="shc big keep" id="mfshare" aria-label="Share my film">' + ICON.share + "</button>" +
      "</div>";
    document.body.appendChild(w);
    w.querySelector(".mfx").onclick = stop;
    var vv = w.querySelector("video");
    vv.addEventListener("ended", endUI);
    vv.addEventListener("ended", function () { recEnd(); });
    vv.addEventListener("playing", function () { recPlaying(vv); });
    vv.addEventListener("waiting", function () { recWaiting(); });
    vv.addEventListener("loadeddata", function () { if (faceOn()) drawNow(vv); });
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
    /* a face only belongs to its own drawing (and, 13 Nov 2026, Make it move on the finish screen always starts
       without one: see the click catcher at the bottom) */
    if (FACE && FACE.key !== k) FACE = null;
    var cam = G("mfcam"); if (cam) cam.classList.toggle("off", !!(SRC && SRC.classList && SRC.classList.contains("mdxmim")));
    G("mfpick").classList.remove("off");
    if (f.face) faceData(k);   /* fetched early, so a new photo is on the films straight away */
    posterFace();
  }
  function close() { stop(); var s = G("mfpick"); if (s) s.classList.add("off"); }
  function play(t) {
    var f = FILMS[KEY]; if (!f) return;
    KIND = t; hideEnd(); setShare(false);
    var w = G("mfplay"), v = w.querySelector("video");
    recDrop(); drawStop();
    var fo = faceOn(), cv = G("mfcv");
    /* 13 Nov 2026: the film's own poster has the drawn face on it, so with the child's face the film starts on the
       picker's picture (their face) until its first frame is drawn, instead of flashing the drawn face */
    if (fo) v.removeAttribute("poster"); else v.poster = f.dir + "poster.jpg?v=" + f.v;
    v.src = f.dir + t + ".mp4?v=" + f.v;
    cv.classList.toggle("off", !fo);
    if (fo) { firstPic(cv); actx(true); drawStart(v); recArm(); }
    w.classList.remove("off");
    var b = document.querySelector('#mfpick .mff[data-t="' + t + '"]'); if (b) b.classList.add("seen");
    go(v);
  }
  function go(v) { try { var p = v.play(); if (p && p.catch) p.catch(function () { v.controls = true; }); } catch (e) { v.controls = true; } }
  function stop() {
    gateClose(); hideEnd(); recDrop(); drawStop();
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
  function replay() {
    var v = G("mfplay").querySelector("video"); hideEnd();
    if (faceOn()) { actx(true); drawStart(v); recArm(); }
    try { v.currentTime = 0; } catch (e) {} go(v);
  }
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
  var SHAREF = null;
  function shareTap() {
    if (!KEY || !KIND) return;
    var rid = faceOn() ? FACE.id + "|" + KIND : null;
    SHAREF = rid ? (RECD[rid] || null) : null;
    /* the film with the child's face is still being saved: wait for it */
    if (!SHAREF && rid && PEND[rid]) PEND[rid].then(function (x) { if (x) SHAREF = x; else getFile(KEY, KIND).catch(function () {}); });
    else if (!SHAREF) getFile(KEY, KIND).catch(function () {});  /* download it while the grown-up answers */
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
    var f = SHAREF || FILE[fid(KEY, KIND)];
    if (f) { gateClose(); send(f); return; }
    ready();
  }
  /* the film is still downloading (or the phone wants one more tap): one big share button that the grown-up taps */
  function ready() {
    G("mfgin").innerHTML = '<button type="button" class="shc big keep wait" id="mfgo" aria-label="Share my film" disabled>' + ICON.share + "</button>";
    G("mfgate").classList.remove("off");
    var k = KEY, t = KIND, b = G("mfgo");
    b.onclick = function () { var f = SHAREF || FILE[fid(k, t)]; if (f) { gateClose(); send(f); } };
    var rid = faceOn() ? FACE.id + "|" + t : null;
    (SHAREF ? Promise.resolve(SHAREF) : rid && PEND[rid] ? PEND[rid].then(function (x) { if (x) { SHAREF = x; return x; } return getFile(k, t); }) : getFile(k, t)).then(function () { var x = G("mfgo"); if (x) { x.disabled = false; x.classList.remove("wait"); } },
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

  /* ---- the child's own face (13 Nov 2026) ----
     For a drawing with face.json (T is for Tiger for now), a photo of the child's own drawing replaces the drawn face
     in all three films. face.json was worked out from the films themselves: for every frame, where the drawn face is
     (an affine map from the face's own picture to the frame), how the light falls on it, and which bits of the scene
     are in front of it (the flower, the butterfly, the rock, dizzy stars) as small masks.
     Each frame: the film frame, then a paper-coloured cut-out over the old face (so none of it peeks out), then the
     child's face (cut out of the paper by the app, sized to cover the old face, lit like the film), then the bits of
     the scene that are in front of the face, copied back from the film. Nothing leaves the phone.
     The film with the child's face records itself as it plays (canvas + the film's own sound), so Share sends that. */
  var FACE = null, FACEDATA = {}, FDR = {}, RECD = {}, FACEN = 0;
  function faceData(k) {
    var f = FILMS[k]; if (!f || !f.face) return Promise.resolve(null);
    if (!FACEDATA[k]) FACEDATA[k] = fetch(f.dir + "face.json?v=" + f.face).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status); return r.json();
    }).then(function (d) { d.path = silPath(d); FDR[k] = d; return d; }).catch(function () { delete FACEDATA[k]; return null; });
    return FACEDATA[k];
  }
  function silPath(d) {
    var p = new Path2D(), s = d.sil;
    for (var i = 0; i < s.length; i += 2) { if (i) p.lineTo(s[i], s[i + 1]); else p.moveTo(s[i], s[i + 1]); }
    p.closePath(); return p;
  }
  function loadImage(src) {
    return new Promise(function (res, rej) {
      var u = null;
      if (typeof src !== "string") { u = URL.createObjectURL(src); }
      var im = new Image();
      im.onload = function () { if (u) URL.revokeObjectURL(u); res(im); };
      im.onerror = function (e) { if (u) URL.revokeObjectURL(u); rej(e); };
      im.src = u || src;
    });
  }
  /* src: the cut-out photo (a Blob from the camera page, or the photo's address in My drawings) */
  function setFace(k, src, how) {
    var id = ++FACEN;
    FACE = { key: k, t: Date.now(), src: how, id: id, F: null, D: null };
    var me = FACE;
    /* 13 Nov 2026: a photo that can't be used gives the blank face back and a shake of the camera button, so it's
       clear to try again (it used to fall back to the drawn face quietly) */
    var nope = function () { if (FACE !== me) return; FACE = null; posterFace(); shakeCam(); };
    Promise.all([faceData(k), loadImage(src)]).then(function (r) {
      if (FACE !== me) return;
      if (!r[0]) { nope(); return; }
      var F = prepFace(r[1], r[0]);
      if (!F) { nope(); return; }
      me.D = r[0]; me.F = F;
      posterFace();
      TYPES.forEach(function (t) { audioBuf(k, t[0]).catch(function () {}); });   /* ready for the recording */
    }).catch(nope);
  }
  function shakeCam() {
    var c = G("mfcam"); if (!c || c.classList.contains("off")) return;
    c.classList.remove("again"); void c.offsetWidth; c.classList.add("again");
    setTimeout(function () { c.classList.remove("again"); }, 600);
  }
  function faceOn() { return !!(FACE && FACE.key === KEY && FACE.D && FACE.F && FACE.D[KIND]); }
  /* ---- 13 Nov 2026 (later): just the drawing, as one solid paper cut-out ----
     The photo's cut-out can hold much more than the face: the lines of lined paper running right across (they made the
     face far too big on the films, as the size is worked out from the cut-out), the paper's own edge, a name, and
     holes where an outline has gaps. Before the face is sized, this finds the drawing itself and keeps only that:
     1. ink = anything darker or more colourful than the paper around it;
     2. ruled lines (and a margin line) = thin ink lying in long straight rows (or columns) right across the picture,
        found at the best of a few small tilts: taken out;
     3. the drawing = the biggest group of what's left (strokes close together count as one group), not touching the
        edge (the paper's edge does), plus any group close by (an ear drawn apart);
     4. its outline with small gaps closed and the inside filled, so it's one solid piece of paper (if the outline is
        too open for that, a cut round its outside instead);
     5. inside that, the ruled lines are painted over with the paper next to them, and any holes with the paper.
     Gives back a canvas (transparent outside the drawing), or null to use the cut-out as it is. */
  function chamfer(M, w, h, inv) {
    /* distance (x3) to the nearest pixel of M (or of not-M when inv), two passes */
    var N = w * h, D = new Int32Array(N), BIG = 1 << 28, x, y, i, v;
    for (i = 0; i < N; i++) D[i] = (inv ? !M[i] : M[i]) ? 0 : BIG;
    for (y = 0; y < h; y++) for (x = 0; x < w; x++) {
      i = y * w + x; v = D[i]; if (!v) continue;
      if (x > 0 && D[i - 1] + 3 < v) v = D[i - 1] + 3;
      if (y > 0) {
        if (D[i - w] + 3 < v) v = D[i - w] + 3;
        if (x > 0 && D[i - w - 1] + 4 < v) v = D[i - w - 1] + 4;
        if (x < w - 1 && D[i - w + 1] + 4 < v) v = D[i - w + 1] + 4;
      }
      D[i] = v;
    }
    for (y = h - 1; y >= 0; y--) for (x = w - 1; x >= 0; x--) {
      i = y * w + x; v = D[i]; if (!v) continue;
      if (x < w - 1 && D[i + 1] + 3 < v) v = D[i + 1] + 3;
      if (y < h - 1) {
        if (D[i + w] + 3 < v) v = D[i + w] + 3;
        if (x < w - 1 && D[i + w + 1] + 4 < v) v = D[i + w + 1] + 4;
        if (x > 0 && D[i + w - 1] + 4 < v) v = D[i + w - 1] + 4;
      }
      D[i] = v;
    }
    return D;
  }
  function cleanFace(img, DBG) {
    var iw = img.naturalWidth || img.width, ih = img.naturalHeight || img.height;
    if (!iw || !ih) return null;
    var sc = Math.min(1, 640 / Math.max(iw, ih)), w = Math.max(1, Math.round(iw * sc)), h = Math.max(1, Math.round(ih * sc)), N = w * h;
    if (w < 24 || h < 24) return null;
    var cv = document.createElement("canvas"); cv.width = w; cv.height = h;
    var cx = cv.getContext("2d", { willReadFrequently: true }); cx.drawImage(img, 0, 0, w, h);
    var id = cx.getImageData(0, 0, w, h), d = id.data, i, j, x, y, k, q, big = Math.max(w, h);
    var A = new Uint8Array(N), L = new Float32Array(N), S = new Float32Array(N), ls = [];
    for (i = 0; i < N; i++) {
      if (d[i * 4 + 3] < 128) continue;
      var r = d[i * 4], g = d[i * 4 + 1], b = d[i * 4 + 2];
      A[i] = 1; L[i] = 0.299 * r + 0.587 * g + 0.114 * b; S[i] = Math.max(r, g, b) - Math.min(r, g, b); ls.push(L[i]);
    }
    if (ls.length < 400) return null;
    ls.sort(function (a1, b1) { return a1 - b1; });
    var pT = ls[Math.floor(ls.length * 0.9)], pr = 0, pg = 0, pb = 0, ps = 0, pn = 0;
    for (i = 0; i < N; i++) if (A[i] && L[i] >= pT) { pr += d[i * 4]; pg += d[i * 4 + 1]; pb += d[i * 4 + 2]; ps += S[i]; pn++; }
    if (!pn) return null;
    pr /= pn; pg /= pn; pb /= pn; ps /= pn;
    /* 1. ink, against the paper's brightness nearby (so a shadow across the page isn't ink): K = clear ink,
       KF = faint too (pale ruled lines are often only faint) */
    var R = Math.max(6, Math.round(0.045 * big)), W1 = w + 1;
    var IC = new Float64Array(W1 * (h + 1)), IL = new Float64Array(W1 * (h + 1));
    for (y = 0; y < h; y++) {
      var rc = 0, rl = 0;
      for (x = 0; x < w; x++) {
        i = y * w + x; var pp = A[i] && L[i] >= 0.8 * pT && S[i] <= ps + 30 ? 1 : 0;
        rc += pp; rl += pp ? L[i] : 0;
        IC[(y + 1) * W1 + x + 1] = IC[y * W1 + x + 1] + rc; IL[(y + 1) * W1 + x + 1] = IL[y * W1 + x + 1] + rl;
      }
    }
    var K = new Uint8Array(N), KF = new Uint8Array(N), nk = 0;
    for (y = 0; y < h; y++) for (x = 0; x < w; x++) {
      i = y * w + x; if (!A[i]) continue;
      var x0 = Math.max(0, x - R), y0 = Math.max(0, y - R), x1 = Math.min(w, x + R + 1), y1 = Math.min(h, y + R + 1);
      var m = IC[y1 * W1 + x1] - IC[y0 * W1 + x1] - IC[y1 * W1 + x0] + IC[y0 * W1 + x0];
      var lp = m > 8 ? (IL[y1 * W1 + x1] - IL[y0 * W1 + x1] - IL[y1 * W1 + x0] + IL[y0 * W1 + x0]) / m : pT;
      if (L[i] < lp * 0.8 || S[i] > ps + 45) { K[i] = 1; nk++; }
      if (L[i] < lp * 0.9 || S[i] > ps + 30) KF[i] = 1;
    }
    if (nk < 150) return null;
    /* 2. ruled lines: thin faint-or-clear ink (a short run across it), lined up in long rows right across the
       picture, at the best of a few tilts (the page may not be quite straight) */
    var VR = new Uint16Array(N), HR = new Uint16Array(N), T = Math.max(3, Math.round(0.012 * big));
    for (x = 0; x < w; x++) for (y = 0; y < h;) {
      if (!KF[y * w + x]) { y++; continue; }
      for (j = y; j < h && KF[j * w + x]; j++);
      for (k = y; k < j; k++) VR[k * w + x] = j - y;
      y = j;
    }
    for (y = 0; y < h; y++) for (x = 0; x < w;) {
      if (!KF[y * w + x]) { x++; continue; }
      for (j = x; j < w && KF[y * w + j]; j++);
      for (k = x; k < j; k++) HR[y * w + k] = j - x;
      x = j;
    }
    var LM = new Uint8Array(N), nLines = 0, LSYS = [];   /* 1 = part of a row line, 2 = part of a column line */
    [true, false].forEach(function (rows) {
      var span = rows ? w : h, len = rows ? h : w, P = [];
      for (i = 0; i < N; i++) if (KF[i] && (rows ? VR[i] : HR[i]) <= T) P.push(i);
      if (P.length < span * 0.3) return;
      var best = null;
      for (var a = -6; a <= 6.001; a += 0.5) {
        var t = Math.tan(a * Math.PI / 180), off = Math.ceil(Math.abs(t) * span / 2) + 2, nb = len + 2 * off, cnt = new Float32Array(nb), sc2 = 0;
        for (q = 0; q < P.length; q++) {
          var px = P[q] % w, py = (P[q] / w) | 0;
          cnt[(rows ? Math.round(py - (px - w / 2) * t) : Math.round(px - (py - h / 2) * t)) + off]++;
        }
        for (q = 0; q < nb; q++) sc2 += cnt[q] * cnt[q];
        if (!best || sc2 > best.sc) best = { sc: sc2, t: t, off: off, cnt: cnt, nb: nb };
      }
      var lo = new Float32Array(best.nb).fill(1e9), hi = new Float32Array(best.nb).fill(-1e9), bins = new Int32Array(P.length);
      for (q = 0; q < P.length; q++) {
        var qx = P[q] % w, qy = (P[q] / w) | 0, along = rows ? qx : qy;
        var bn = (rows ? Math.round(qy - (qx - w / 2) * best.t) : Math.round(qx - (qy - h / 2) * best.t)) + best.off;
        bins[q] = bn; if (along < lo[bn]) lo[bn] = along; if (along > hi[bn]) hi[bn] = along;
      }
      /* a line = three neighbouring bands together (a page photographed a little out of square has lines at slightly
         different tilts) holding a quarter of the width or more, spread across most of it */
      var isL = new Uint8Array(best.nb), any = 0, C3 = best.cnt;
      for (q = 1; q < best.nb - 1; q++) {
        var c3 = C3[q - 1] + C3[q] + C3[q + 1], l3 = Math.min(lo[q - 1], lo[q], lo[q + 1]), h3 = Math.max(hi[q - 1], hi[q], hi[q + 1]);
        if (c3 >= span * 0.25 && h3 - l3 >= span * 0.6 && C3[q] >= C3[q - 1] && C3[q] >= C3[q + 1]) { isL[q] = 1; nLines++; any = 1; }
      }
      var near2 = function (bq2) { for (var z2 = -2; z2 <= 2; z2++) if (bq2 + z2 >= 0 && bq2 + z2 < best.nb && isL[bq2 + z2]) return true; return false; };
      var cntL = 0; for (q = 0; q < best.nb; q++) cntL += isL[q];
      if (any) LSYS.push({ rows: rows, t: best.t, off: best.off, nb: best.nb, isL: isL, near: near2, n: cntL, P: P, bins: bins, cnt: best.cnt });
    });
    /* lined paper = 3 or more lines one way (then a margin line the other way counts too); one long straight line on
       its own (the paper's edge, a fold, or a long stroke of the drawing) doesn't. Once it's clearly lined, shorter
       lines at the same spacing count too (where the cut-out cut a line short) */
    var ruled = LSYS.some(function (Z) { return Z.n >= 3; });
    LSYS.forEach(function (Z) {
      if (Z.n < 3) return;
      var pos = [];
      for (q = 0; q < Z.nb; q++) if (Z.isL[q] && (!pos.length || q - pos[pos.length - 1] >= 3)) pos.push(q);
      var gaps = []; for (q = 1; q < pos.length; q++) gaps.push(pos[q] - pos[q - 1]);
      gaps.sort(function (g1, g2) { return g1 - g2; });
      var per = gaps[Math.floor(gaps.length / 2)];
      if (!(per >= 6)) return;
      var span2 = Z.rows ? w : h, C4 = Z.cnt, add = [], pi = 0;
      for (q = 1; q < Z.nb - 1; q++) {
        if (Z.near(q)) continue;
        var c4 = C4[q - 1] + C4[q] + C4[q + 1];
        if (c4 < span2 * 0.08 || C4[q] < C4[q - 1] || C4[q] < C4[q + 1]) continue;
        /* at a whole number of spacings from the nearest long line */
        while (pi < pos.length - 1 && Math.abs(pos[pi + 1] - q) <= Math.abs(pos[pi] - q)) pi++;
        var dq = Math.abs(q - pos[pi]), kq = Math.round(dq / per);
        if (kq >= 1 && kq <= 12 && Math.abs(dq - kq * per) <= 2) add.push(q);
      }
      add.forEach(function (q2) { Z.isL[q2] = 1; Z.n++; });
    });
    LSYS = ruled ? LSYS : [];
    nLines = 0;
    LSYS.forEach(function (Z) {
      nLines += Z.n;
      for (q = 0; q < Z.P.length; q++) if (Z.near(Z.bins[q])) LM[Z.P[q]] = Z.rows ? 1 : 2;
      Z.P = Z.bins = Z.cnt = null;
    });
    var band = function (p10, want) {
      /* which way the ruled line runs, if this pixel lies in one's band (1 rows, 2 columns), else 0 */
      var bx = p10 % w, by = (p10 / w) | 0;
      for (var z = 0; z < LSYS.length; z++) {
        var Z = LSYS[z]; if (want && (Z.rows ? 1 : 2) !== want) continue;
        var bn2 = (Z.rows ? Math.round(by - (bx - w / 2) * Z.t) : Math.round(bx - (by - h / 2) * Z.t)) + Z.off;
        if (Z.near(bn2)) return Z.rows ? 1 : 2;
      }
      return 0;
    };
    /* where a stroke of the drawing crosses a ruled line, that bit is the stroke's: ink just beyond the line's band on
       both sides, close by */
    var LM2 = new Uint8Array(LM), rx2 = Math.max(2, Math.round(T / 3));
    var inkAt = function (xx, yy) { return xx >= 0 && yy >= 0 && xx < w && yy < h && K[yy * w + xx] && !band(yy * w + xx); };
    for (i = 0; i < N; i++) {
      var dl = LM[i]; if (!dl || !K[i]) continue;
      var lx = i % w, ly = (i / w) | 0, s1, e1, side1 = false, side2 = false, dd;
      if (dl === 1) {
        for (s1 = ly; s1 > 0 && band((s1 - 1) * w + lx, 1) && ly - s1 < 2 * T; s1--);
        for (e1 = ly; e1 < h - 1 && band((e1 + 1) * w + lx, 1) && e1 - ly < 2 * T; e1++);
        for (dd = -rx2; dd <= rx2 && !(side1 && side2); dd++) {
          if (inkAt(lx + dd, s1 - 1) || inkAt(lx + dd, s1 - 2)) side1 = true;
          if (inkAt(lx + dd, e1 + 1) || inkAt(lx + dd, e1 + 2)) side2 = true;
        }
      } else {
        for (s1 = lx; s1 > 0 && band(i - (lx - s1) - 1, 2) && lx - s1 < 2 * T; s1--);
        for (e1 = lx; e1 < w - 1 && band(i + (e1 - lx) + 1, 2) && e1 - lx < 2 * T; e1++);
        for (dd = -rx2; dd <= rx2 && !(side1 && side2); dd++) {
          if (inkAt(s1 - 1, ly + dd) || inkAt(s1 - 2, ly + dd)) side1 = true;
          if (inkAt(e1 + 1, ly + dd) || inkAt(e1 + 2, ly + dd)) side2 = true;
        }
      }
      if (side1 && side2) LM2[i] = 0;
    }
    LM = LM2;
    /* 3. the paper's edge, if the photo's corners took in some of the table: thick dark ink joined to the edge of the
       picture (only thick ink, so lines and strokes don't lead it into the drawing), and only if it really is a band
       round the edge (a drawing that fills the picture is not) */
    var FR = new Uint8Array(N), es = Math.max(5, Math.round(0.03 * big)), eb = Math.round(0.12 * big), frame = false;
    var NP = new Uint8Array(N); for (i = 0; i < N; i++) NP[i] = K[i] && !LM[i] ? 1 : 0;
    var DN = chamfer(NP, w, h, true), ER = new Uint8Array(N);
    for (i = 0; i < N; i++) ER[i] = DN[i] > 6 ? 1 : 0;              /* thinner than ~4 px: gone */
    var DE = chamfer(ER, w, h, false), OP = new Uint8Array(N);
    for (i = 0; i < N; i++) OP[i] = DE[i] <= 6 && NP[i] ? 1 : 0;   /* the thick ink, back to its own size */
    var Q0 = new Int32Array(N), h0 = 0, t0 = 0, nfr = 0, nband = 0, nstrip = 0;
    for (y = 0; y < h; y++) for (x = 0; x < w; x++) {
      if (x >= es && y >= es && x < w - es && y < h - es) continue;
      nstrip++; i = y * w + x; if (OP[i] && !FR[i]) { FR[i] = 1; Q0[t0++] = i; }
    }
    var seeds = t0;
    while (h0 < t0) {
      var p0 = Q0[h0++], zx = p0 % w, zy = (p0 / w) | 0;
      nfr++; if (zx < eb || zy < eb || zx >= w - eb || zy >= h - eb) nband++;
      if (zx > 0 && OP[p0 - 1] && !FR[p0 - 1]) { FR[p0 - 1] = 1; Q0[t0++] = p0 - 1; }
      if (zx < w - 1 && OP[p0 + 1] && !FR[p0 + 1]) { FR[p0 + 1] = 1; Q0[t0++] = p0 + 1; }
      if (zy > 0 && OP[p0 - w] && !FR[p0 - w]) { FR[p0 - w] = 1; Q0[t0++] = p0 - w; }
      if (zy < h - 1 && OP[p0 + w] && !FR[p0 + w]) { FR[p0 + w] = 1; Q0[t0++] = p0 + w; }
    }
    /* a frame runs along the edge (a good part of the strip round it), not just touching it here and there */
    if (nfr >= N * 0.03 && nband >= nfr * 0.6 && seeds >= nstrip * 0.2) {
      frame = true;
      var DF0 = chamfer(FR, w, h, false);
      for (i = 0; i < N; i++) if (DF0[i] <= 9 && NP[i]) FR[i] = 1;    /* and its soft edge */
    } else FR.fill(0);
    var ein = seeds, etot = nstrip;
    var K2 = new Uint8Array(N), nk2 = 0;
    for (i = 0; i < N; i++) if (K[i] && !LM[i] && !FR[i]) { K2[i] = 1; nk2++; }
    if (DBG) { DBG.w = w; DBG.h = h; DBG.K = K; DBG.LM = LM; DBG.FR = FR; DBG.T = T; DBG.pT = pT; DBG.paper = [pr, pg, pb, ps]; DBG.frame = frame; DBG.edgeInk = Math.round(ein / Math.max(1, etot) * 100) / 100; }
    if (nk2 < 150) return null;
    /* 4. the drawing: groups of the ink that's left (strokes a small gap apart count as one); the biggest, and any
       group close by */
    var rd = Math.max(3, Math.round(0.012 * big)), DG = chamfer(K2, w, h, false);
    var lab = new Int32Array(N), Q = new Int32Array(N), comps = [], nc = 0;
    for (i = 0; i < N; i++) {
      if (lab[i] || DG[i] > rd * 3) continue;
      nc++; var hd = 0, tl = 0, C = { n: 0, x0: w, y0: h, x1: 0, y1: 0, tr: 0, tc: 0 };
      Q[tl++] = i; lab[i] = nc;
      while (hd < tl) {
        var p = Q[hd++], ux = p % w, uy = (p / w) | 0;
        if (K2[p]) {
          C.n++; if (ux < C.x0) C.x0 = ux; if (ux > C.x1) C.x1 = ux; if (uy < C.y0) C.y0 = uy; if (uy > C.y1) C.y1 = uy;
          if (VR[p] <= T) C.tr++; if (HR[p] <= T) C.tc++;
        }
        if (ux > 0 && !lab[p - 1] && DG[p - 1] <= rd * 3) { lab[p - 1] = nc; Q[tl++] = p - 1; }
        if (ux < w - 1 && !lab[p + 1] && DG[p + 1] <= rd * 3) { lab[p + 1] = nc; Q[tl++] = p + 1; }
        if (uy > 0 && !lab[p - w] && DG[p - w] <= rd * 3) { lab[p - w] = nc; Q[tl++] = p - w; }
        if (uy < h - 1 && !lab[p + w] && DG[p + w] <= rd * 3) { lab[p + w] = nc; Q[tl++] = p + w; }
      }
      comps[nc] = C;
    }
    var main = 0;
    for (k = 1; k <= nc; k++) if (!main || comps[k].n > comps[main].n) main = k;
    if (!main || comps[main].n < 120) return null;
    /* the groups near it, in turn, as the drawing grows (an outline with gaps comes in pieces) */
    var M0 = comps[main], keep = new Uint8Array(nc + 1), gx0 = M0.x0, gy0 = M0.y0, gx1 = M0.x1, gy1 = M0.y1, more = true, rounds = 0;
    keep[main] = 1;
    while (more && rounds++ < 5) {
      more = false;
      var ex = 0.15 * Math.max(gx1 - gx0, gy1 - gy0);
      for (k = 1; k <= nc; k++) {
        var C2 = comps[k];
        if (keep[k] || C2.n < M0.n * 0.03 || C2.x1 < gx0 - ex || C2.x0 > gx1 + ex || C2.y1 < gy0 - ex || C2.y0 > gy1 + ex) continue;
        var bw2 = C2.x1 - C2.x0 + 1, bh2 = C2.y1 - C2.y0 + 1;
        if ((C2.tr >= C2.n * 0.85 && bw2 >= bh2 * 6) || (C2.tc >= C2.n * 0.85 && bh2 >= bw2 * 6)) continue;   /* a bit of ruled line */
        keep[k] = 1; more = true;
        gx0 = Math.min(gx0, C2.x0); gy0 = Math.min(gy0, C2.y0); gx1 = Math.max(gx1, C2.x1); gy1 = Math.max(gy1, C2.y1);
      }
    }
    if (DBG) { DBG.lab = lab; DBG.comps = comps; DBG.main = main; DBG.keep = keep; }
    var F = new Uint8Array(N), fx0 = w, fy0 = h, fx1 = 0, fy1 = 0;
    for (i = 0; i < N; i++) if (K2[i] && keep[lab[i]]) {
      F[i] = 1; x = i % w; y = (i / w) | 0;
      if (x < fx0) fx0 = x; if (x > fx1) fx1 = x; if (y < fy0) fy0 = y; if (y > fy1) fy1 = y;
    }
    /* 5. one solid piece: close the gaps in the outline (grow, fill the inside, shrink back), trying small gaps first;
       if even big gaps don't close it (an outline drawn very open), cut round its outside instead */
    var pts = [], lowp = [], upp = [], how = "hull", fsz = Math.max(fx1 - fx0, fy1 - fy0);
    for (y = fy0; y <= fy1; y++) {
      var a0 = -1, a1 = -1;
      for (x = fx0; x <= fx1; x++) if (F[y * w + x]) { if (a0 < 0) a0 = x; a1 = x; }
      if (a0 >= 0) { pts.push([a0, y]); if (a1 !== a0) pts.push([a1, y]); }
    }
    pts.sort(function (p4, p5) { return p4[0] - p5[0] || p4[1] - p5[1]; });
    var crs = function (o, a2, b3) { return (a2[0] - o[0]) * (b3[1] - o[1]) - (a2[1] - o[1]) * (b3[0] - o[0]); };
    for (q = 0; q < pts.length; q++) { while (lowp.length >= 2 && crs(lowp[lowp.length - 2], lowp[lowp.length - 1], pts[q]) <= 0) lowp.pop(); lowp.push(pts[q]); }
    for (q = pts.length - 1; q >= 0; q--) { while (upp.length >= 2 && crs(upp[upp.length - 2], upp[upp.length - 1], pts[q]) <= 0) upp.pop(); upp.push(pts[q]); }
    var H = lowp.slice(0, -1).concat(upp.slice(0, -1)), harea = 0;
    for (q = 0; q < H.length; q++) { var u1 = H[q], u2 = H[(q + 1) % H.length]; harea += u1[0] * u2[1] - u2[0] * u1[1]; }
    harea = Math.abs(harea) / 2;
    var DF = chamfer(F, w, h, false), SH = new Uint8Array(N), nS = 0, ratio = 0, G = new Uint8Array(N), out = new Uint8Array(N);
    [0.05, 0.1, 0.15].some(function (fr) {
      var rcl = Math.max(3, Math.round(fr * fsz)), hd2 = 0, tl2 = 0;
      for (i = 0; i < N; i++) { G[i] = DF[i] <= rcl * 3 ? 1 : 0; out[i] = 0; }
      var seed = function (p2) { if (!G[p2] && !out[p2]) { out[p2] = 1; Q[tl2++] = p2; } };
      for (x = 0; x < w; x++) { seed(x); seed(N - w + x); }
      for (y = 0; y < h; y++) { seed(y * w); seed(y * w + w - 1); }
      while (hd2 < tl2) {
        var p3 = Q[hd2++], vx = p3 % w, vy = (p3 / w) | 0;
        if (vx > 0) seed(p3 - 1); if (vx < w - 1) seed(p3 + 1); if (vy > 0) seed(p3 - w); if (vy < h - 1) seed(p3 + w);
      }
      var DO = chamfer(out, w, h, false); nS = 0;
      for (i = 0; i < N; i++) { SH[i] = (!out[i] && DO[i] > rcl * 3) || F[i] ? 1 : 0; nS += SH[i]; }
      ratio = harea ? nS / harea : 1;
      if (ratio >= 0.85) { how = "close" + Math.round(fr * 100); return true; }
      return false;
    });
    if (how === "hull" && H.length >= 3) {
      var hc = document.createElement("canvas"); hc.width = w; hc.height = h;
      var hx = hc.getContext("2d", { willReadFrequently: true });
      hx.beginPath(); H.forEach(function (p6, n6) { if (n6) hx.lineTo(p6[0] + 0.5, p6[1] + 0.5); else hx.moveTo(p6[0] + 0.5, p6[1] + 0.5); }); hx.closePath();
      hx.fillStyle = "#000"; hx.strokeStyle = "#000"; hx.lineJoin = "round"; hx.lineWidth = Math.max(2, 0.03 * fsz); hx.fill(); hx.stroke();
      var hd3 = hx.getImageData(0, 0, w, h).data; nS = 0;
      for (i = 0; i < N; i++) { SH[i] = hd3[i * 4 + 3] > 127 || F[i] ? 1 : 0; nS += SH[i]; }
    }
    /* 6. the picture: the drawing as photographed, ruled lines painted over with the paper beside them, holes and
       anything left of the paper's edge as paper */
    var bx0 = w, by0 = h, bx1 = 0, by1 = 0;
    for (i = 0; i < N; i++) if (SH[i]) { x = i % w; y = (i / w) | 0; if (x < bx0) bx0 = x; if (x > bx1) bx1 = x; if (y < by0) by0 = y; if (y > by1) by1 = y; }
    if (bx1 <= bx0 || by1 <= by0) return null;
    var pad = 3; bx0 = Math.max(0, bx0 - pad); by0 = Math.max(0, by0 - pad); bx1 = Math.min(w - 1, bx1 + pad); by1 = Math.min(h - 1, by1 + pad);
    var ow = bx1 - bx0 + 1, oh = by1 - by0 + 1, oc = document.createElement("canvas"); oc.width = ow; oc.height = oh;
    var ox = oc.getContext("2d"), od = ox.createImageData(ow, oh), o = od.data;
    var isPaper = function (p7) { return A[p7] && !KF[p7] && !FR[p7] && !band(p7); };
    var near = function (p8, dir) {
      /* the colour of the nearest paper either side of a line (above/below a row line, left/right of a column line) */
      var px2 = p8 % w, py2 = (p8 / w) | 0, n = 0, rr = 0, gg = 0, bb = 0;
      for (var s2 = -1; s2 <= 1; s2 += 2) for (var t2 = 1; t2 <= T + 6; t2++) {
        var qx2 = dir === 1 ? px2 : px2 + s2 * t2, qy2 = dir === 1 ? py2 + s2 * t2 : py2;
        if (qx2 < 0 || qy2 < 0 || qx2 >= w || qy2 >= h) break;
        var p9 = qy2 * w + qx2;
        if (isPaper(p9)) { rr += d[p9 * 4]; gg += d[p9 * 4 + 1]; bb += d[p9 * 4 + 2]; n++; break; }
      }
      return n ? [rr / n, gg / n, bb / n] : [pr, pg, pb];
    };
    for (y = by0; y <= by1; y++) for (x = bx0; x <= bx1; x++) {
      i = y * w + x; var di = ((y - by0) * ow + (x - bx0)) * 4;
      if (!SH[i]) continue;
      var col = null, dir = F[i] ? 0 : LM[i] || band(i);
      if (dir) col = near(i, dir);
      else if (A[i] && !FR[i]) col = [d[i * 4], d[i * 4 + 1], d[i * 4 + 2]];
      else col = [pr, pg, pb];
      o[di] = col[0]; o[di + 1] = col[1]; o[di + 2] = col[2]; o[di + 3] = 255;
    }
    ox.putImageData(od, 0, 0);
    oc.__clean = { lines: nLines, groups: nc, how: how, fill: Math.round(ratio * 100) / 100, frame: frame, w: ow, h: oh, from: [w, h] };
    return oc;
  }
  /* the face picture: white-balanced to the film's paper, and placed (scale + centre) so it covers the old face.
     13 Nov 2026 (later): it starts from just the drawing (cleanFace above), so its size comes from the drawing, not
     from everything else in the cut-out */
  function prepFace(img, D) {
    var iw = img.naturalWidth || img.width, ih = img.naturalHeight || img.height;
    if (!iw || !ih) return null;
    var c = null; try { c = cleanFace(img); } catch (e) { c = null; }
    if (!c) {
      var sc = Math.min(1, 640 / Math.max(iw, ih));
      c = document.createElement("canvas"); c.width = Math.max(1, Math.round(iw * sc)); c.height = Math.max(1, Math.round(ih * sc));
      c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
    }
    var cinfo = c.__clean || null, w = c.width, h = c.height;
    var x = c.getContext("2d", { willReadFrequently: true });
    var id = x.getImageData(0, 0, w, h), d = id.data, n = 0, sx = 0, sy = 0, i, L = [];
    for (var yy = 0; yy < h; yy++) for (var xx = 0; xx < w; xx++) {
      i = (yy * w + xx) * 4;
      if (d[i + 3] > 127) { n++; sx += xx; sy += yy; L.push(0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2]); }
    }
    if (n < 200) return null;
    /* the paper inside the drawing = its brightest tenth; make that match the film's paper colour */
    L.sort(function (a, b) { return a - b; });
    var thr = L[Math.floor(L.length * 0.9)], pr = 0, pg = 0, pb = 0, pn = 0;
    for (i = 0; i < d.length; i += 4) {
      if (d[i + 3] > 127 && 0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2] >= thr) { pr += d[i]; pg += d[i + 1]; pb += d[i + 2]; pn++; }
    }
    if (pn) {
      pr /= pn; pg /= pn; pb /= pn;
      var P = D.paper, neutral = Math.max(pr, pg, pb) - Math.min(pr, pg, pb) < 40;
      var cl = function (v) { return Math.max(0.85, Math.min(1.7, v)); };
      var lum = cl((0.299 * P[0] + 0.587 * P[1] + 0.114 * P[2]) / Math.max(1, 0.299 * pr + 0.587 * pg + 0.114 * pb));
      var gr = neutral ? cl(P[0] / Math.max(1, pr)) : lum, gg = neutral ? cl(P[1] / Math.max(1, pg)) : lum, gb = neutral ? cl(P[2] / Math.max(1, pb)) : lum;
      if (Math.abs(gr - 1) > 0.02 || Math.abs(gg - 1) > 0.02 || Math.abs(gb - 1) > 0.02) {
        for (i = 0; i < d.length; i += 4) { d[i] = Math.min(255, d[i] * gr); d[i + 1] = Math.min(255, d[i + 1] * gg); d[i + 2] = Math.min(255, d[i + 2] * gb); }
        x.putImageData(id, 0, 0);
      }
    }
    /* a thin paper edge all round, as if it was cut out with scissors; it also helps hide the old face's edges */
    var P2 = D.paper, r = Math.max(3, Math.round(0.022 * Math.max(w, h))), pw = w + 2 * r + 2, ph = h + 2 * r + 2;
    var sil = document.createElement("canvas"); sil.width = w; sil.height = h;
    var sx2 = sil.getContext("2d"); sx2.drawImage(c, 0, 0); sx2.globalCompositeOperation = "source-in";
    sx2.fillStyle = "rgb(" + P2[0] + "," + P2[1] + "," + P2[2] + ")"; sx2.fillRect(0, 0, w, h);
    var c2 = document.createElement("canvas"); c2.width = pw; c2.height = ph;
    var x2 = c2.getContext("2d", { willReadFrequently: true });
    for (var ring = 0.5; ring <= 1.001; ring += 0.5) for (var an = 0; an < 24; an++) {
      x2.drawImage(sil, r + 1 + Math.cos(an * Math.PI / 12) * r * ring, r + 1 + Math.sin(an * Math.PI / 12) * r * ring);
    }
    x2.drawImage(c, r + 1, r + 1);
    c = c2; w = pw; h = ph;
    var d2 = x2.getImageData(0, 0, w, h).data; n = 0; sx = 0; sy = 0;
    for (yy = 0; yy < h; yy++) for (xx = 0; xx < w; xx++) if (d2[(yy * w + xx) * 4 + 3] > 127) { n++; sx += xx; sy += yy; }
    var cx = sx / n, cy = sy / n, s0 = Math.sqrt(D.area / n);
    /* size and place it so it covers the old face: the smallest size (up to 50% bigger) that, nudged a little,
       covers at least 98.5% of it; checked on a small grid */
    var q = 0.25, RW = Math.ceil(D.W * q), RH = Math.ceil(D.H * q), PAD = 6, GW = RW + 2 * PAD, GH = RH + 2 * PAD;
    var g = document.createElement("canvas"); g.width = GW; g.height = GH;
    var gx = g.getContext("2d", { willReadFrequently: true });
    gx.setTransform(q, 0, 0, q, PAD, PAD); gx.fillStyle = "#000"; gx.fill(D.path);
    var refd = gx.getImageData(0, 0, GW, GH).data, refi = [];
    for (i = 3; i < refd.length; i += 4) if (refd[i] > 127) refi.push((i - 3) >> 2);
    /* 13 Nov 2026 (later): at most 30% bigger (was 50%), and each step bigger has to cover clearly more of the old
       face, so a drawing shaped unlike the old face isn't blown up to cover it (the paper behind covers the rest) */
    var KMAX = 1.3, best = { k: 1, dx: 0, dy: 0, cov: -1, sc: -9 };
    for (var k = 1; k <= KMAX + 0.0001 && best.cov < 0.985; k += 0.05) {
      var s = s0 * k;
      gx.setTransform(1, 0, 0, 1, 0, 0); gx.clearRect(0, 0, GW, GH);
      gx.setTransform(q * s, 0, 0, q * s, PAD + q * (D.c[0] - s * cx), PAD + q * (D.c[1] - s * cy));
      gx.drawImage(c, 0, 0);
      var cd = gx.getImageData(0, 0, GW, GH).data;
      for (var ddy = -4; ddy <= 4; ddy++) for (var ddx = -4; ddx <= 4; ddx++) {
        var both = 0;
        for (var m = 0; m < refi.length; m++) {
          var pi = refi[m], px = pi % GW - ddx, py = (pi / GW | 0) - ddy;
          if (px >= 0 && py >= 0 && px < GW && py < GH && cd[(py * GW + px) * 4 + 3] > 127) both++;
        }
        var cov = both / Math.max(1, refi.length), pen = (Math.abs(ddx) + Math.abs(ddy)) * 0.0004, scr = cov - pen - 0.2 * (k - 1);
        if (scr > best.sc) best = { k: k, dx: ddx / q, dy: ddy / q, cov: cov, sc: scr };
      }
    }
    return { img: c, s: s0 * best.k, cx: cx - best.dx / (s0 * best.k), cy: cy - best.dy / (s0 * best.k), cov: best.cov, tint: null, tk: "",
      dbg: { clean: cinfo, k: Math.round(best.k * 100) / 100 } };
  }
  /* the face lit like the film: multiplied by the frame's light (only ever darker; the films never get brighter
     than the frame the face was measured on, give or take a few per cent) */
  function tinted(F, r, g, b) {
    r = Math.min(1, r); g = Math.min(1, g); b = Math.min(1, b);
    if (r > 0.985 && g > 0.985 && b > 0.985) return F.img;
    var k = Math.round(r * 50) + "," + Math.round(g * 50) + "," + Math.round(b * 50);
    if (F.tk === k && F.tint) return F.tint;
    var c = F.tint || document.createElement("canvas");
    c.width = F.img.width; c.height = F.img.height;
    var x = c.getContext("2d");
    x.globalCompositeOperation = "source-over"; x.clearRect(0, 0, c.width, c.height); x.drawImage(F.img, 0, 0);
    x.globalCompositeOperation = "multiply";
    x.fillStyle = "rgb(" + Math.round(r * 255) + "," + Math.round(g * 255) + "," + Math.round(b * 255) + ")";
    x.fillRect(0, 0, c.width, c.height);
    x.globalCompositeOperation = "destination-in"; x.drawImage(F.img, 0, 0);
    x.globalCompositeOperation = "source-over";
    F.tint = c; F.tk = k; return c;
  }
  /* a small mask (half the face picture's size), run-length coded: 0s and 1s alternating, starting with 0s */
  function occMask(o) {
    if (o.__c) return o.__c;
    var w = o.b[2], h = o.b[3], c = document.createElement("canvas"); c.width = w; c.height = h;
    var x = c.getContext("2d"), id = x.createImageData(w, h), d = id.data, p = 0, on = 0, r = o.r;
    for (var i = 0; i < r.length; i++) {
      var n = r[i];
      if (on) for (var j = 0; j < n; j++) d[(p + j) * 4 + 3] = 255;
      p += n; on = 1 - on;
    }
    x.putImageData(id, 0, 0); o.__c = c; return c;
  }
  var SCR = null;
  /* one frame: e = [a, b, c, d, e, f, red, green, blue light, mask index] from face.json */
  function compose(ctx, src, sw, sh, e, D, occs, F) {
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.globalCompositeOperation = "source-over";
    ctx.drawImage(src, 0, 0, sw, sh);
    if (!e || !F || !D) return;
    var a = e[0], b = e[1], c = e[2], d = e[3], ee = e[4], f = e[5];
    ctx.setTransform(a, d, b, ee, c, f);
    var r = Math.min(1, e[6]), g = Math.min(1, e[7]), bl = Math.min(1, e[8]);
    ctx.fillStyle = "rgb(" + Math.round(D.paper[0] * r) + "," + Math.round(D.paper[1] * g) + "," + Math.round(D.paper[2] * bl) + ")";
    ctx.fill(D.path);
    ctx.save();
    ctx.transform(F.s, 0, 0, F.s, D.c[0] - F.s * F.cx, D.c[1] - F.s * F.cy);
    ctx.drawImage(tinted(F, e[6], e[7], e[8]), 0, 0);
    ctx.restore();
    var o = e[9] >= 0 && occs ? occs[e[9]] : null;
    if (!o) return;
    var bx = o.b[0] * 2, by = o.b[1] * 2, bw = o.b[2] * 2, bh = o.b[3] * 2, det = a * ee - b * d;
    if (!det) return;
    if (!SCR) SCR = document.createElement("canvas");
    if (SCR.width < bw) SCR.width = bw;
    if (SCR.height < bh) SCR.height = bh;
    var ox = SCR.getContext("2d");
    ox.setTransform(1, 0, 0, 1, 0, 0); ox.globalCompositeOperation = "source-over"; ox.clearRect(0, 0, bw, bh);
    /* the film frame mapped back into the face picture's own space, just this box */
    var i00 = ee / det, i01 = -b / det, i02 = (b * f - ee * c) / det, i10 = -d / det, i11 = a / det, i12 = (d * c - a * f) / det;
    ox.setTransform(i00, i10, i01, i11, i02 - bx, i12 - by);
    ox.drawImage(src, 0, 0, sw, sh);
    ox.setTransform(1, 0, 0, 1, 0, 0);
    ox.globalCompositeOperation = "destination-in";
    ox.drawImage(occMask(o), 0, 0, bw, bh);
    ox.globalCompositeOperation = "source-over";
    ctx.drawImage(SCR, 0, 0, bw, bh, bx, by, bw, bh);
  }
  /* the picker's picture with the child's face on it.
     13 Nov 2026: until there is a face, the drawn face the films were made with isn't shown either (asked for on 13 Nov:
     the old tiger should only be in My drawings). The picture gets a blank paper face, the same cut-out the child's face goes
     on, with the camera on it; tapping it takes the photo, like the camera button. Films without face.json keep their
     poster as it is. If face.json can't be fetched, the poster is shown as it is rather than nothing. */
  var PVN = 0;
  function prevState(st) {
    var p = G("mfprev"); if (!p) return;
    p.setAttribute("data-st", st);
    p.setAttribute("aria-label", st === "cam" ? "Make your own drawing move" : "Silly film");
  }
  function camShown() { var c = G("mfcam"); return !!c && !c.classList.contains("off"); }
  var PIM = {};
  function posterImg(k) {
    var f = FILMS[k];
    if (PIM[k]) return Promise.resolve(PIM[k]);
    return loadImage(f.dir + "poster.jpg?v=" + f.v).then(function (im) { PIM[k] = im; return im; });
  }
  function posterFace() {
    var cv = G("mfpcv"), pim = G("mfposter"), k = KEY, f = FILMS[k], my = ++PVN;
    if (!cv || !pim || !f) return;
    var plain = function () { cv.classList.add("off"); pim.classList.remove("off"); prevState("play"); };
    if (!f.face) { plain(); return; }
    var on = !!(FACE && FACE.key === k && FACE.D && FACE.F && FACE.D.poster);
    var F = on ? FACE.F : null;
    /* a photo is still being put on: the blank face, and the picture waits */
    var st = on ? "play" : FACE && FACE.key === k ? "wait" : camShown() ? "cam" : "play";
    prevState(st);
    pim.classList.add("off");
    var draw = function (D, im) {
      var P = D && D.poster;
      if (!P) { plain(); return; }
      cv.width = P.w; cv.height = P.h;
      var x = cv.getContext("2d");
      compose(x, im, P.w, P.h, P.A.concat(P.g, [P.o ? 0 : -1]), D, P.o ? [P.o] : null, F || blankFace(D));
      if (st === "cam") camBadge(x, D, P.A);
      cv.classList.remove("off");
    };
    /* drawn straight away once fetched, so an earlier picture is never left on show */
    if (FDR[k] && PIM[k]) { draw(FDR[k], PIM[k]); return; }
    cv.classList.add("off");
    Promise.all([faceData(k), posterImg(k)]).then(function (r) {
      if (my !== PVN || KEY !== k) return;
      draw(r[0], r[1]);
    }).catch(function () { if (my === PVN) plain(); });
  }
  /* the blank paper face, drawn in the face picture's own space so it sits exactly where the face goes: the face's
     outline smoothed (the tracked one is jagged), a little bigger so none of the old face peeks out, in the films' paper
     colour, with a soft shadow and a dashed line where the edge of the drawing goes */
  function smoothPath(D) {
    if (D.smooth) return D.smooth;
    var s = D.sil, n = s.length / 2, P = [], Q = [], i, j;
    for (i = 0; i < n; i++) P.push([s[2 * i], s[2 * i + 1]]);
    /* the outline every 4 px, then each point averaged with its neighbours 20 px either side */
    for (i = 0; i < n; i++) {
      var a = P[i], b = P[(i + 1) % n], m = Math.max(1, Math.round(Math.hypot(b[0] - a[0], b[1] - a[1]) / 4));
      for (j = 0; j < m; j++) Q.push([a[0] + (b[0] - a[0]) * j / m, a[1] + (b[1] - a[1]) * j / m]);
    }
    var N = Q.length, M = 5, path = new Path2D();
    for (i = 0; i < N; i++) {
      var sx = 0, sy = 0;
      for (j = -M; j <= M; j++) { var q = Q[(i + j + N) % N]; sx += q[0]; sy += q[1]; }
      sx /= 2 * M + 1; sy /= 2 * M + 1;
      if (i) path.lineTo(sx, sy); else path.moveTo(sx, sy);
    }
    path.closePath();
    D.smooth = path; return path;
  }
  function blankFace(D) {
    if (D.blank) return D.blank;
    var c = document.createElement("canvas"); c.width = D.W; c.height = D.H;
    var x = c.getContext("2d"), sp = smoothPath(D), pc = "rgb(" + D.paper.join(",") + ")";
    var paper = function () { x.fillStyle = pc; x.strokeStyle = pc; x.lineWidth = 24; x.fill(sp); x.stroke(sp); };
    x.lineJoin = "round"; x.lineCap = "round";
    x.save(); x.shadowColor = "rgba(8,17,48,.32)"; x.shadowBlur = 16; x.shadowOffsetY = 7; paper(); x.restore();
    paper();
    x.setLineDash([20, 15]); x.lineWidth = 6; x.strokeStyle = "rgba(8,17,48,.35)"; x.stroke(sp);
    D.blank = { img: c, s: 1, cx: D.c[0], cy: D.c[1], tint: null, tk: "" };
    return D.blank;
  }
  /* the app's yellow camera button, upright, in the middle of the blank face */
  var CAMBODY = null, CAMLENS = null;
  function camBadge(x, D, A) {
    if (!CAMBODY) {
      CAMBODY = new Path2D("M10 22a5 5 0 0 1 5-5h7l4-6h12l4 6h7a5 5 0 0 1 5 5v24a5 5 0 0 1-5 5H15a5 5 0 0 1-5-5z");
      CAMLENS = new Path2D(); CAMLENS.arc(32, 33, 10, 0, Math.PI * 2);
    }
    var cx = A[0] * D.c[0] + A[1] * D.c[1] + A[2], cy = A[3] * D.c[0] + A[4] * D.c[1] + A[5];
    var sc = Math.sqrt(Math.abs(A[0] * A[4] - A[1] * A[3])), R = 0.27 * D.bb[2] * sc;
    x.save();
    x.setTransform(1, 0, 0, 1, 0, 0); x.globalCompositeOperation = "source-over";
    x.fillStyle = "rgba(8,17,48,.25)"; x.beginPath(); x.arc(cx, cy + R * 0.09, R, 0, Math.PI * 2); x.fill();
    x.fillStyle = "#ffc531"; x.strokeStyle = NAVY; x.lineWidth = R * 0.065;
    x.beginPath(); x.arc(cx, cy, R, 0, Math.PI * 2); x.fill(); x.stroke();
    var k = R * 1.2 / 64;
    x.setTransform(k, 0, 0, k, cx - 32 * k, cy - 31 * k);
    x.lineWidth = 3.4; x.lineJoin = "round";
    x.fillStyle = "#fff"; x.fill(CAMBODY); x.stroke(CAMBODY);
    x.fillStyle = "#d6ebff"; x.fill(CAMLENS); x.stroke(CAMLENS);
    x.restore();
  }
  /* a film with the child's face starts on the picker's picture until its first frame is drawn */
  function firstPic(cv) {
    var p = G("mfpcv"), x = cv.getContext("2d");
    x.setTransform(1, 0, 0, 1, 0, 0); x.globalCompositeOperation = "source-over";
    x.fillStyle = "#000"; x.fillRect(0, 0, cv.width, cv.height);
    if (p && !p.classList.contains("off") && p.width > 1) { try { x.drawImage(p, 0, 0, cv.width, cv.height); } catch (e) {} }
  }
  /* playing: every film frame is drawn with the face, in step with the video */
  var RVF = 0, RAFI = 0, LASTK = -1;
  function drawNow(v) {
    if (!faceOn()) return;
    var cv = G("mfcv"), D = FACE.D, tr = D[KIND];
    if (v.videoWidth && (cv.width !== v.videoWidth || cv.height !== v.videoHeight)) { cv.width = v.videoWidth; cv.height = v.videoHeight; }
    var t = v.__mt != null ? v.__mt : v.currentTime, k = Math.max(0, Math.round(t * (D.fps || 30)));
    var e = tr.f[k] || null;
    compose(cv.getContext("2d"), v, cv.width, cv.height, e, D, tr.o, FACE.F);
    LASTK = k;
  }
  function drawStart(v) {
    drawStop();
    if (v.requestVideoFrameCallback) {
      var cb = function (now, meta) { v.__mt = meta && meta.mediaTime != null ? meta.mediaTime : null; drawNow(v); RVF = v.requestVideoFrameCallback(cb); };
      RVF = v.requestVideoFrameCallback(cb);
      v.__rvf = true;
    } else {
      var loop = function () { v.__mt = null; if (!v.paused || LASTK < 0) drawNow(v); RAFI = requestAnimationFrame(loop); };
      RAFI = requestAnimationFrame(loop);
    }
  }
  function drawStop() {
    var w = G("mfplay"), v = w && w.querySelector("video");
    if (RVF && v && v.cancelVideoFrameCallback) { try { v.cancelVideoFrameCallback(RVF); } catch (e) {} }
    if (RAFI) cancelAnimationFrame(RAFI);
    RVF = 0; RAFI = 0; LASTK = -1;
    if (v) v.__mt = null;
  }
  /* ---- recording the film with the face, so it can be shared ---- */
  var AC = null, AUD = {}, AUDB = {}, REC = null, ARM = false, PEND = {};
  function actx(wake) {
    if (!AC) { var C = window.AudioContext || window.webkitAudioContext; if (C) { try { AC = new C(); } catch (e) { AC = null; } } }
    if (AC && wake && AC.state === "suspended") { try { AC.resume(); } catch (e) {} }
    return AC;
  }
  function audioBuf(k, t) {
    var f = FILMS[k], id = k + "/" + t + "/" + (f && f.v);
    if (!f) return Promise.reject(new Error("no film"));
    if (!AUD[id]) AUD[id] = fetch(f.dir + t + ".m4a?v=" + f.v).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status); return r.arrayBuffer();
    }).then(function (ab) {
      var a = actx(false); if (!a) throw new Error("no audio");
      return new Promise(function (res, rej) { var p = a.decodeAudioData(ab, res, rej); if (p && p.then) p.then(res, rej); });
    }).then(function (buf) { AUDB[id] = buf; return buf; });
    AUD[id].catch(function () { delete AUD[id]; });
    return AUD[id];
  }
  function recArm() { recDrop(); ARM = true; }
  function recPlaying(v) {
    if (REC && REC.paused) { try { if (AC) AC.resume(); REC.mr.resume(); } catch (e) {} REC.paused = false; return; }
    if (!ARM || !faceOn()) return;
    ARM = false;
    var id = FACE.id + "|" + KIND, f = FILMS[KEY];
    if (RECD[id] || !window.MediaRecorder) return;
    var cv = G("mfcv"); if (!cv.captureStream) return;
    var buf = AUDB[KEY + "/" + KIND + "/" + f.v], a = actx(true); if (!a) return;
    /* the sound for the recording isn't ready yet (only if a film is tapped the moment the photo is in):
       hold the film for a moment, then start again with it */
    if (!buf) {
      var held = true, kk = KEY, kd = KIND;
      try { v.pause(); } catch (e) {}
      var goOn = function () { if (!held) return; held = false; if (KEY === kk && KIND === kd && !G("mfplay").classList.contains("off")) { ARM = !!AUDB[kk + "/" + kd + "/" + f.v]; go(v); } };
      audioBuf(kk, kd).then(goOn, goOn); setTimeout(goOn, 3000);
      return;
    }
    var st, dest, bs, ty = "", mr;
    try { st = cv.captureStream(30); dest = a.createMediaStreamDestination(); bs = a.createBufferSource(); bs.buffer = buf; bs.connect(dest); }
    catch (e) { return; }
    dest.stream.getAudioTracks().forEach(function (tr) { st.addTrack(tr); });
    /* H.264 + AAC in MP4 first: what phones' share sheets, Instagram and Save Video take best */
    var types = ["video/mp4;codecs=avc1.42E01E,mp4a.40.2", "video/mp4;codecs=avc1,mp4a", "video/mp4;codecs=avc1", "video/mp4", "video/webm;codecs=vp9,opus", "video/webm;codecs=vp8,opus", "video/webm"];
    for (var i = 0; i < types.length; i++) { try { if (MediaRecorder.isTypeSupported(types[i])) { ty = types[i]; break; } } catch (e) {} }
    try { mr = ty ? new MediaRecorder(st, { mimeType: ty, videoBitsPerSecond: 5000000 }) : new MediaRecorder(st); } catch (e) { return; }
    var R = { mr: mr, ch: [], st: st, bs: bs, id: id, keep: false, paused: false, name: fileName(KEY, KIND), done: null };
    PEND[id] = new Promise(function (res) { R.done = res; });
    mr.ondataavailable = function (e) { if (e.data && e.data.size) R.ch.push(e.data); };
    mr.onstop = function () {
      try { R.bs.stop(); } catch (e) {}
      R.st.getTracks().forEach(function (tr) { try { tr.stop(); } catch (e) {} });
      if (!R.keep || !R.ch.length) { delete PEND[R.id]; R.done(null); return; }
      var mt = (mr.mimeType || ty || "video/webm").split(";")[0], blob = new Blob(R.ch, { type: mt });
      var name = R.name.replace(/\.mp4$/, /mp4/.test(mt) ? ".mp4" : ".webm"), x;
      try { x = new File([blob], name, { type: mt }); } catch (e) { x = blob; x.name = name; }
      RECD[R.id] = x; delete PEND[R.id]; R.done(x);
    };
    try { mr.start(250); bs.start(0, Math.max(0, v.currentTime)); } catch (e) { return; }
    REC = R;
  }
  /* a hiccup in the download: pause the recording and its sound together, so they stay in step */
  function recWaiting() { if (REC && !REC.paused) { try { REC.mr.pause(); if (AC) AC.suspend(); } catch (e) {} REC.paused = true; } }
  function recEnd() { var R = REC; REC = null; ARM = false; if (!R) return; R.keep = true; try { if (AC && AC.state === "suspended") AC.resume(); R.mr.stop(); } catch (e) {} }
  function recDrop() { var R = REC; REC = null; ARM = false; if (!R) return; R.keep = false; try { R.mr.stop(); } catch (e) {} }

  /* the camera button: the existing Make it move with a photo of the child's own drawing, from the button that
     opened the films (the finish screen's, or the one on a photo in My drawings) */
  var SRC = null;
  var OWNK = null;
  function own() {
    close();
    OWNK = KEY;
    var b = SRC || G("funbtn");
    if (b && typeof b.onclick === "function") b.onclick.call(b, { stopPropagation: function () {}, preventDefault: function () {} });
    /* 13 Nov 2026: from the finish screen's films, the camera button goes straight on to the phone's camera (and, while
       testing, its Photo Library: see TEMP-PHOTO-LIBRARY in index.html), with the blank camera page behind it, so one tap
       does it. Still inside the tap, so the phone allows it. Back on that page returns to the films, as before. */
    var M = window.__mimTest;
    if (b && b.id === "funbtn" && M && typeof M.cam === "function" && M.key && M.key()) { try { M.cam(); } catch (e) {} }
  }
  /* catch the Make it move button on a drawing's photo in My drawings (.mdxmim, 12 Nov evening), only for drawings
     that have films.
     13 Nov 2026 (later): the finish screen's Make it move (#funbtn) isn't caught any more. It opens the blank camera
     page ("Take a photo of yours") for every drawing, films or not, photo saved or not, as asked for. Once the photo is
     in, a drawing whose films wear the child's face (T is for Tiger) goes on to its films (the camera page calls
     withFace); every other drawing plays its Make it move story with the photo, as before. D is for Digger's and
     a is for ambulance's films are still on the Make it move button of their photo in My drawings. */
  document.addEventListener("click", function (e) {
    var b = e.target && e.target.closest && e.target.closest("#funbtn,.mdxmim");
    if (!b) return;
    /* a fresh start: no earlier face, and Back on the camera page goes back to the finish screen */
    if (b.id === "funbtn") { FACE = null; SRC = null; OWNK = null; return; }
    var k = b.getAttribute("data-key");
    if (!k || !FILMS[k]) return;
    e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation();
    SRC = b;
    if (b.classList.contains("mdxmim") && FILMS[k].face) {
      var vw = b.closest(".mdview"), im = vw && vw.querySelector("img");
      if (im && im.src) setFace(k, im.src, "md");
    }
    open(k);
  }, true);
  /* Back on the blank camera page (opened from the films' camera button) returns to the films */
  document.addEventListener("click", function (e) {
    var b = e.target && e.target.closest && e.target.closest("#mimback");
    if (!b || !OWNK) return;
    var k = OWNK; OWNK = null;
    setTimeout(function () { open(k); }, 0);
  }, true);
  window.__mimFilms = {
    films: FILMS, open: open, close: close, play: play,
    /* used by the app's camera page: a drawing whose films can wear the child's own face */
    hasFace: function (k) { return !!(FILMS[k] && FILMS[k].face); },
    withFace: function (k, blob) { OWNK = null; SRC = null; setFace(k, blob, "cam"); open(k); },
    _face: function () { return FACE; }, _rec: function () { return RECD; },
    /* for checking the clean-up of a photo (cleanFace) */
    _clean: function (img) { var o = {}, c = null; try { c = cleanFace(img, o); } catch (e) { o.err = String(e && e.stack || e); } return { c: c, o: o }; }
  };
})();
