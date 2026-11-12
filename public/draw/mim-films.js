/* 12 Nov 2026: Make it move films.
   A drawing that has ready-made felt-toy films (D is for Digger and T is for Tiger for now) gets a film picker when its
   Make it move button is tapped: Silly, Wonky and Starring role, plus the camera button for the existing
   Make it move with a photo of your own drawing. Icons only, no words on screen.
   Drawings without films keep the Make it move button exactly as before.
   Films live in /mim-films/<drawing key>/ as silly.mp4, wonky.mp4, star.mp4 and poster.jpg. */
(function () {
  "use strict";
  var FILMS = {
    dx_digger_d: { dir: "mim-films/dx_digger_d/", v: "1" },
    /* 12 Nov 2026 (evening): the felt tiger from a 4-year-old's T is for Tiger, with the founder's voices and
       Claude's own comedy tunes played on sampled instruments (TimGM6mb sound set, GPL-2) */
    dx_tiger_t: { dir: "mim-films/dx_tiger_t/", v: "2" }   /* v2: ends on the app's Step by Draw end page */
  };
  var TYPES = [["silly", "Silly film"], ["wonky", "Wonky film"], ["star", "Starring role film"]];
  var NAVY = "#081130";
  var ICON = {
    silly: '<svg viewBox="0 0 60 60" aria-hidden="true"><circle cx="30" cy="30" r="26" fill="#ffc531" stroke="' + NAVY + '" stroke-width="3"/><circle cx="21" cy="24" r="6" fill="#fff" stroke="' + NAVY + '" stroke-width="2.5"/><circle cx="39" cy="22" r="4" fill="#fff" stroke="' + NAVY + '" stroke-width="2.5"/><circle cx="22" cy="25" r="2.5" fill="' + NAVY + '"/><circle cx="39" cy="22" r="2" fill="' + NAVY + '"/><path d="M16 36q14 16 28 0z" fill="' + NAVY + '"/><path d="M27 44q4 6 8 0" fill="#e5484d"/></svg>',
    wonky: '<svg viewBox="0 0 60 60" aria-hidden="true"><g transform="rotate(-14 30 30)"><circle cx="30" cy="30" r="26" fill="#ffc531" stroke="' + NAVY + '" stroke-width="3"/><path d="M17 25q13-13 26 0" stroke="' + NAVY + '" stroke-width="3.4" fill="none" stroke-linecap="round"/><ellipse cx="22" cy="38" rx="3.2" ry="4.2" fill="' + NAVY + '"/><ellipse cx="38" cy="38" rx="3.2" ry="4.2" fill="' + NAVY + '"/></g></svg>',
    star: '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M8 54h48" stroke="' + NAVY + '" stroke-width="4" stroke-linecap="round"/><path d="M14 54l6-16h24l6 16" fill="#e5484d" stroke="' + NAVY + '" stroke-width="3" stroke-linejoin="round"/><path d="M32 6l6.2 12.6 13.8 2-10 9.8 2.4 13.8L32 37.7l-12.4 6.5 2.4-13.8-10-9.8 13.8-2z" fill="#ffc531" stroke="' + NAVY + '" stroke-width="3" stroke-linejoin="round"/></svg>',
    cam: '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M10 22a5 5 0 0 1 5-5h7l4-6h12l4 6h7a5 5 0 0 1 5 5v24a5 5 0 0 1-5 5H15a5 5 0 0 1-5-5z" fill="#fff" stroke="' + NAVY + '" stroke-width="3.2" stroke-linejoin="round"/><circle cx="32" cy="33" r="10" fill="#d6ebff" stroke="' + NAVY + '" stroke-width="3.2"/></svg>',
    back: '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>',
    close: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
  };
  function G(id) { return document.getElementById(id); }
  function curKey() { try { return (typeof V !== "undefined" && V.p && V.p.key) || null; } catch (e) { return null; } }

  var css = document.createElement("style");
  css.textContent =
    "#mfpick{position:fixed;inset:0;z-index:900;background:#e3f1ff;display:flex;flex-direction:column;" +
    "padding:max(14px,env(safe-area-inset-top)) max(16px,env(safe-area-inset-right)) max(18px,env(safe-area-inset-bottom)) max(16px,env(safe-area-inset-left))}" +
    "#mfpick.off,#mfplay.off{display:none}" +
    "#mfpick .mftop{display:flex}" +
    "#mfpick .mfbody{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px;min-height:0}" +
    "#mfpick .mfprev{height:min(46vh,420px);aspect-ratio:9/16;border-radius:24px;overflow:hidden;background:" + NAVY + ";border:5px solid #fff;box-shadow:0 8px 0 rgba(8,17,48,.22);padding:0;cursor:pointer}" +
    "#mfpick .mfprev img{width:100%;height:100%;object-fit:cover;display:block}" +
    "#mfpick .mfrow{display:flex;gap:16px;justify-content:center}" +
    "#mfpick .mff{width:84px;height:84px;border-radius:26px;padding:8px;border:0;background:#fff;box-shadow:0 6px 0 rgba(8,17,48,.3);cursor:pointer}" +
    "#mfpick .mff svg{width:100%;height:100%;display:block}" +
    "#mfpick .mff.seen{box-shadow:0 0 0 4px #ffc531,0 6px 0 rgba(8,17,48,.3)}" +
    "#mfpick .mff:active,#mfpick .mfcam:active{transform:translateY(4px)}" +
    "#mfpick .mfcam{width:64px;height:64px;border-radius:50%;border:0;background:#fff;box-shadow:0 5px 0 rgba(8,17,48,.3);display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0}" +
    "#mfpick .mfcam svg{width:42px;height:42px}" +
    "#mfplay{position:fixed;inset:0;z-index:1000;background:#000;display:flex;align-items:center;justify-content:center}" +
    "#mfplay video{width:100%;height:100%;object-fit:contain;background:#000}" +
    "#mfplay .mfx{position:absolute;left:max(14px,env(safe-area-inset-left));top:max(14px,env(safe-area-inset-top))}" +
    "@media (max-height:700px){#mfpick .mfprev{height:40vh}#mfpick .mff{width:70px;height:70px;border-radius:22px}#mfpick .mfcam{width:56px;height:56px}}";
  document.head.appendChild(css);

  var KEY = null;
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
      '<button type="button" class="round mfx" aria-label="Close">' + ICON.close + "</button>";
    document.body.appendChild(w);
    w.querySelector(".mfx").onclick = stop;
    w.querySelector("video").addEventListener("ended", stop);
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
    var w = G("mfplay"), v = w.querySelector("video");
    v.poster = f.dir + "poster.jpg?v=" + f.v;
    v.src = f.dir + t + ".mp4?v=" + f.v;
    w.classList.remove("off");
    var b = document.querySelector('#mfpick .mff[data-t="' + t + '"]'); if (b) b.classList.add("seen");
    try { var p = v.play(); if (p && p.catch) p.catch(function () { v.controls = true; }); } catch (e) { v.controls = true; }
  }
  function stop() {
    var w = G("mfplay"); if (!w) return;
    var v = w.querySelector("video");
    try { v.pause(); } catch (e) {}
    v.removeAttribute("src"); try { v.load(); } catch (e) {}
    v.controls = false;
    w.classList.add("off");
  }
  /* the camera button: the existing Make it move with a photo of the child's own drawing */
  function own() {
    close();
    var b = G("funbtn");
    if (b && typeof b.onclick === "function") b.onclick.call(b);
  }
  /* catch the Make it move button before its own handler, only for drawings that have films */
  document.addEventListener("click", function (e) {
    var b = e.target && e.target.closest && e.target.closest("#funbtn");
    if (!b) return;
    var k = curKey();
    if (!k || !FILMS[k]) return;
    e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation();
    open(k);
  }, true);
  window.__mimFilms = { films: FILMS, open: open, close: close, play: play };
})();
