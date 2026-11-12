/* 12 Nov 2026: Step by Draw, the waiting list done in one go.
   1. No "What you need" page. Play goes straight to the steps; Back on the steps goes back to the drawing's card.
   2. A heart on each drawing's card puts it in Favourites.
   3. Swipe left or right on a set (and on a set in My drawings) to go to the next set in the same row as the home screen.
   4. My drawings is a collecting game: progress and a bronze, silver or gold medal for every set (bronze at 5 drawings,
      or 3 for a numbers set; silver at half; gold for the whole set). Nine golds win the trophy, and a finished set can be
      seen as one poster. The My trophies page and its home button are gone.
   5. Free print sheets: one page per drawing (the steps along the top, a box to draw in, a small colour picture, the logo and
      step-by.com), sized to fit A4 and US Letter. Printing is only on the Grown-ups page (behind the gate): every sheet, and
      the poster of any finished set. A photo of a print sheet is cut down to the drawing box, found by its four corner squares.
   6. Home pictures for the ABC and abc rows are drawings from each set (COVERS below). The 123 row keeps its pictures.
   7. (later 12 Nov) The home screen is nine big tiles (rows ABC, abc, 123; each row swipes sideways once more themes are added),
      then Keep going, Make a show and My drawings, then Favourites and Grown-ups. It replaces the washing line, whose hidden
      pictures still open each set, so nothing about how sets open has changed.
   (later 12 Nov) A drawing opened in My drawings has the finish screen's Make it move button (the blue film clapper) beside
      the cross. It plays that photo and comes back to it. No camera there, so no retake at the end. The big star is off
      that view for now (VIEWSTAR); the small star on each photo of a letter still picks the main one.
   (evening 12 Nov) Tapping a letter in My drawings goes straight to its main photo (the starred one, or the newest) with
      Make it move and the cross; the page of a letter's photos is no longer in the way. If the letter has more than one
      photo, that view also has an all-photos button (with the count). It opens every photo of the letter together: tapping
      a photo or its star makes it the main one and goes straight back to the Make it move view with it. Back does the same
      without changing anything. The cross goes back to the set.
   Photos and everything else stay on this device. */
(function(){
'use strict';
var G=function(i){return document.getElementById(i)};
function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;')}
function has(fn){try{return typeof window[fn]==='function'}catch(e){return false}}
var FONT='-apple-system,BlinkMacSystemFont,"Arial Rounded MT Bold",Arial,sans-serif';

/* ---------------------------------------------------------------- sets */
var ORDER=['AZ','az','09'];
var SLOTS={AZ:'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split(''),az:'abcdefghijklmnopqrstuvwxyz'.split(''),'09':'0123456789'.split('')};
function sets(){return window.SBSETS||[]}
function colIn(cat,set){var r=null;cat.cols.forEach(function(c){if(c.set===set)r=c});return r}
function colById(id){var r=null;sets().forEach(function(cat){cat.cols.forEach(function(c){if(c.id===id)r={c:c,cat:cat}})});return r}
function colOfKey(key){var r=null;sets().forEach(function(cat){cat.cols.forEach(function(c){var h=c.has||{};Object.keys(h).forEach(function(s){if(h[s]===key)r={c:c,cat:cat,slot:s}})})});return r}
/* rows in the same order as the home screen's lines */
function rows(){var out=[];[].forEach.call(document.querySelectorAll('#sswl .wlrow'),function(r){var ids=[].map.call(r.querySelectorAll('.wlcard[data-set]'),function(b){return b.getAttribute('data-set')});if(ids.length)out.push(ids)});
 if(!out.length)ORDER.forEach(function(set){var r=[];sets().forEach(function(cat){var c=colIn(cat,set);if(c)r.push(c.id)});out.push(r)});return out}
/* 12 Nov 2026: swiping runs through all nine sets in home order (ABC row, then abc, then 123) and goes round: after the ninth comes the first, and back from the first goes to the ninth */
function flat(){return [].concat.apply([],rows())}
function neighbour(id,dir){var F=flat(),j=F.indexOf(id);if(j<0||F.length<2)return null;return F[(j+dir+F.length)%F.length]}
function badge(a,b,c,ca,cb,cc){return'<svg viewBox="0 0 84 36" aria-hidden="true"><rect x="2" y="2" width="80" height="32" rx="16" fill="#fff" stroke="#081130" stroke-width="3"/><text x="42" y="26.5" text-anchor="middle" font-family="Arial Rounded MT Bold,Arial,Helvetica,sans-serif" font-weight="900" font-size="22" letter-spacing="1"><tspan fill="'+ca+'">'+a+'</tspan><tspan fill="'+cb+'">'+b+'</tspan><tspan fill="'+cc+'">'+c+'</tspan></text></svg>'}
var BADGE={AZ:badge('A','B','C','#E5392B','#2F7BF5','#3FA535'),az:badge('a','b','c','#E5392B','#2F7BF5','#3FA535'),'09':badge('1','2','3','#8B5CF6','#EC4899','#14B8A6')};
/* open a set the same way the home screen does (its picture on the washing line holds the set's own code) */
var PASS=false;
function clickSet(id){var b=document.querySelector('.wlcard[data-set="'+id+'"]');if(!b)return false;PASS=true;try{b.click()}finally{PASS=false}return true}
function goHomeScreen(){[].forEach.call(document.querySelectorAll('#app > section.scr'),function(s){s.classList.add('hide')});['pv','sheet'].forEach(function(i){var e=G(i);if(e)e.classList.add('hide')});var h=G('home');if(h)h.classList.remove('hide')}

/* ---------------------------------------------------------------- icons */
var IC={
 x:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
 back:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>',
 printer:'<svg viewBox="0 0 24 24" fill="none" stroke="#081130" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M7 9V3.5h10V9" fill="#fff"/><rect x="3" y="9" width="18" height="8.5" rx="2.2" fill="#d6ebff"/><path d="M7 14h10v6.5H7z" fill="#fff"/><path d="M9.5 17h5" stroke-linecap="round"/><circle cx="17.6" cy="12" r="1" fill="#081130" stroke="none"/></svg>',
 star:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.6l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 17.4l-5.8 3.1 1.1-6.5L2.6 9.4l6.5-.9z"/></svg>',
 cup:'<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M14 6h20v10a10 10 0 0 1-20 0z" fill="#FFC531" stroke="#081130" stroke-width="2.6" stroke-linejoin="round"/><path d="M14 10H7v3a7 7 0 0 0 7 7M34 10h7v3a7 7 0 0 1-7 7" fill="none" stroke="#081130" stroke-width="2.6" stroke-linejoin="round"/><path d="M24 26v7" stroke="#081130" stroke-width="2.6"/><path d="M17 42h14l-1.5-9h-11z" fill="#FFC531" stroke="#081130" stroke-width="2.6" stroke-linejoin="round"/><path d="M24 9.5l1.6 3.3 3.6.5-2.6 2.5.6 3.6-3.2-1.7-3.2 1.7.6-3.6-2.6-2.5 3.6-.5z" fill="#fff"/></svg>',
 frame:'<svg viewBox="0 0 24 24" fill="none" stroke="#081130" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2" fill="#FFC531"/><rect x="6" y="6" width="5" height="5" rx="1" fill="#fff"/><rect x="13" y="6" width="5" height="5" rx="1" fill="#fff"/><rect x="6" y="13" width="5" height="5" rx="1" fill="#fff"/><rect x="13" y="13" width="5" height="5" rx="1" fill="#fff"/></svg>',
 /* the finish screen's Make it move film clapper, exactly as it is there */
 mim:'<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="7" y="18" width="34" height="22" rx="3" fill="#fff" stroke="#081130" stroke-width="2.6"/><path d="M7 18l2-8 34-4 1 8z" fill="#fff" stroke="#081130" stroke-width="2.6" stroke-linejoin="round"/><path d="M15 9l4 7M24 8l4 7M33 7l4 7" stroke="#081130" stroke-width="2.6"/><path d="M21 24l9 5-9 5z" fill="#2a8fd6"/></svg>',
 /* (evening 12 Nov) all the photos of a letter: two photos stacked */
 pics:'<svg viewBox="0 0 24 24" fill="none" stroke="#081130" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><rect x="8.5" y="2.5" width="13" height="13" rx="2.5" fill="#d6ebff"/><rect x="2.5" y="8.5" width="13" height="13" rx="2.5" fill="#fff"/><path d="M5 19l3-3.4 2.4 2.2 1.6-1.5 1.6 2.7" stroke-linecap="round"/><circle cx="11.6" cy="12" r="1.4" fill="#FFC531" stroke-width="1.4"/></svg>'
};
function heart(on){try{if(typeof I!=='undefined'&&I&&I.heart)return I.heart(on)}catch(e){}return'<svg viewBox="0 0 24 24"><path d="M12 21s-8-5.2-8-11a4.6 4.6 0 0 1 8-3 4.6 4.6 0 0 1 8 3c0 5.8-8 11-8 11z" fill="'+(on?'#E5392B':'none')+'" stroke="#081130" stroke-width="2.4" stroke-linejoin="round"/></svg>'}
function medal(l){var col=['#e7e1d2','#cd7f32','#cfd4db','#FFC531'][l],rim=l?'#081130':'#c9c1ad';
 return'<svg viewBox="0 0 34 44" aria-hidden="true"><path d="M8 1h7l3 14h-7z" fill="'+(l?'#E5392B':'#e7e1d2')+'" stroke="'+rim+'" stroke-width="1.8" stroke-linejoin="round"/><path d="M26 1h-7l-3 14h7z" fill="'+(l?'#2F7BF5':'#e7e1d2')+'" stroke="'+rim+'" stroke-width="1.8" stroke-linejoin="round"/><circle cx="17" cy="28" r="13" fill="'+col+'" stroke="'+rim+'" stroke-width="2.2"/>'+(l?'<path d="M17 21.5l2 4.1 4.5.6-3.3 3.2.8 4.5-4-2.1-4 2.1.8-4.5-3.3-3.2 4.5-.6z" fill="#fff" fill-opacity=".85"/>':'')+'</svg>'}

/* ---------------------------------------------------------------- styles (added last, so they win) */
var st=document.createElement('style');st.id='sbx1112';st.textContent=[
/* 1. no What you need */
'#tabs .tab[data-t="need"]{display:none!important}',
/* 2. heart and printer on the card */
'.pvc .th .pvhb{position:absolute;right:10px;top:10px;z-index:3;width:52px;height:52px;border-radius:50%;border:0;background:#fff;box-shadow:0 4px 0 rgba(8,17,48,.18);display:flex;align-items:center;justify-content:center;padding:0;color:#081130;cursor:pointer;-webkit-tap-highlight-color:transparent}',
'.pvc .th .pvhb svg{width:30px;height:30px}.pvc .th .pvhb:active{transform:translateY(3px);box-shadow:0 1px 0 rgba(8,17,48,.18)}',
'.pvc .th .pvhb.pop svg{animation:sbhpop .45s cubic-bezier(.3,1.6,.5,1)}@keyframes sbhpop{0%{transform:scale(.5)}100%{transform:none}}',
/* 3. swiping between sets */
'#proj.sbcolm #pgrid{margin-bottom:26px!important}',
'.sbsdots{position:absolute;left:0;right:0;bottom:max(10px,env(safe-area-inset-bottom,0px));display:flex;justify-content:center;gap:8px;pointer-events:none;z-index:2}',
'.sbsdots i{width:8px;height:8px;border-radius:4px;background:rgba(8,17,48,.22);transition:width .2s}.sbsdots i.on{background:#081130;width:20px}.sbsdots{gap:6px!important}.sbsdots b{width:8px}',
'#proj:not(.sbcolm) .sbsdots{display:none!important}',
'@keyframes sbsl{from{transform:translateX(48px);opacity:.15}to{transform:none;opacity:1}}@keyframes sbsr{from{transform:translateX(-48px);opacity:.15}to{transform:none;opacity:1}}',
'@keyframes sbnl{0%,100%{transform:none}40%{transform:translateX(-16px)}}@keyframes sbnr{0%,100%{transform:none}40%{transform:translateX(16px)}}',
'.sbsl{animation:sbsl .28s ease-out both}.sbsr{animation:sbsr .28s ease-out both}.sbnl{animation:sbnl .3s ease-out}.sbnr{animation:sbnr .3s ease-out}',
/* 4. My trophies off the home screen; Show + Keep going, then Favourites + My drawings */
'html body #hpills #achtile{display:none!important}',
'html body #sstudio.wl #hpills{grid-template-columns:repeat(6,minmax(0,1fr))!important}',
'html body #sstudio.wl #hpills>#showtile{grid-column:span 4!important}html body #sstudio.wl #hpills>#conttile{grid-column:span 2!important}',
'html body #sstudio.wl #hpills>#favtile,html body #sstudio.wl #hpills>#drawtile{grid-column:span 3!important}',
/* 4. My drawings */
'#mdin.mdx{display:flex!important;flex-direction:column;overflow:hidden;padding:12px 2px 6px;gap:12px}',
'#mydraw .achtop b.mdxh{display:flex;align-items:center;justify-content:center;gap:7px;height:54px;min-width:0}',
'#mydraw .achtop b.mdxh img{height:48px;width:48px;object-fit:contain;display:block;flex:none}',
'#mydraw .achtop b.mdxh .sbbd{width:64px;flex:none;filter:drop-shadow(0 3px 0 rgba(8,17,48,.18))}#mydraw .achtop b.mdxh .sbbd svg{display:block;width:100%;height:auto}',
'#mydraw .achtop b.mdxh .mdxl{min-width:52px;height:52px;padding:0 14px;border-radius:999px;background:#081130;color:#fff;display:flex;align-items:center;justify-content:center;font:900 30px/1 '+FONT+'}',
'#mydraw .achtop b.mdxh .mdxhm{width:26px;flex:none}#mydraw .achtop b.mdxh .mdxhm svg{display:block;width:100%;height:auto}',
'#mydraw .achtop b.mdxh .mdxcnt{flex:none;font:900 14px/1 '+FONT+';color:#081130;background:#fff;border-radius:999px;padding:6px 8px;box-shadow:0 3px 0 rgba(8,17,48,.14);white-space:nowrap}',
'#mydraw .achtop .sp{display:flex;align-items:center;justify-content:center}',
'#mydraw .achtop .mdxpost{width:54px;height:54px;background:#fff8dc;box-shadow:0 5px 0 #c79410}#mydraw .achtop .mdxpost svg{width:30px;height:30px}',
'.mdxstrip{flex:none;height:52px;border-radius:20px;background:#fff;box-shadow:0 5px 0 rgba(8,17,48,.14);display:flex;align-items:center;justify-content:space-between;padding:0 8px 0 12px;gap:3px}',
'.mdxdot{flex:none;width:clamp(18px,6.2vw,28px);height:clamp(18px,6.2vw,28px);border-radius:50%;border:2.5px dashed rgba(8,17,48,.24);display:flex;align-items:center;justify-content:center;box-sizing:border-box}',
'.mdxdot.on{border:2.5px solid #081130;background:#FFC531}.mdxdot svg{width:64%;height:64%}.mdxdot svg path{fill:#fff;stroke:#081130;stroke-width:2;stroke-linejoin:round}',
'.mdxcup{flex:none;width:46px;height:46px;border:0;background:none;padding:0;display:flex;align-items:center;justify-content:center;filter:grayscale(1);opacity:.32;cursor:pointer;-webkit-tap-highlight-color:transparent}',
'.mdxcup svg{width:42px;height:42px}.mdxcup.won{filter:none;opacity:1;animation:sbglow 1.8s ease-in-out infinite}@keyframes sbglow{0%,100%{transform:none}50%{transform:scale(1.12)}}',
'.mdxcup.wig,.mdxcard.wig{animation:wig .4s}',
'.mdxrow{flex:1 1 0;min-height:0;display:flex;align-items:stretch;justify-content:center;gap:12px}',
'.mdxcard{position:relative;flex:1 1 0;min-width:0;max-width:210px;height:100%;max-height:260px;background:#fff;border:0;border-radius:20px;box-shadow:0 6px 0 var(--pd,#c48a0c);padding:12px 8px 50px;display:flex;align-items:center;justify-content:center;cursor:pointer;font:inherit;-webkit-tap-highlight-color:transparent}',
'.mdxcard:active{transform:translateY(5px);box-shadow:0 1px 0 var(--pd,#c48a0c)}',
'.mdxcard.gold{box-shadow:0 6px 0 #c79410,0 0 0 4px #FFC531}',
'.mdxcard>img{max-width:100%;max-height:100%;object-fit:contain;display:block;pointer-events:none}',
'.mdxcard .sbbd{position:absolute;left:50%;bottom:23px;transform:translateX(-50%);width:58%;max-width:76px;pointer-events:none}.mdxcard .sbbd svg{display:block;width:100%;height:auto}',
'.mdxbar{position:absolute;left:11px;right:11px;bottom:10px;height:9px;border-radius:5px;background:#ece4cf;overflow:hidden;pointer-events:none}',
'.mdxbar i{display:block;height:100%;min-width:0;border-radius:5px;background:#3FA535}.mdxcard.gold .mdxbar i{background:#FFC531}',
'.mdxmed{position:absolute;left:-6px;top:-9px;width:32px;pointer-events:none;z-index:2}.mdxmed svg{display:block;width:100%;height:auto}.mdxmed.no{opacity:.5}',
'.mdxold{flex:none;display:flex;gap:10px;overflow-x:auto;scrollbar-width:none;padding:2px 2px 8px}.mdxold::-webkit-scrollbar{display:none}',
'.mdxold .mdc{flex:none;width:64px;height:64px;padding:4px;border-radius:14px}',
'.mdxgrid{flex:1 1 auto;min-height:0;display:grid;justify-content:center;align-content:center;gap:10px;overflow:hidden;margin-bottom:22px}',
'#mdin .sbslot.mdxno{cursor:default}#mdin .sbslot.mdxno .sbgl{color:rgba(8,17,48,.2)}#mdin .sbslot .sbth img{object-fit:contain}',
'.mdxmore{position:absolute;right:5px;bottom:5px;z-index:2;min-width:calc(var(--s,80px)*.28);height:calc(var(--s,80px)*.28);padding:0 4px;border-radius:999px;background:#fff;color:#081130;box-shadow:0 0 0 2px #081130;display:flex;align-items:center;justify-content:center;font:900 calc(var(--s,80px)*.17)/1 '+FONT+';pointer-events:none}',
'.mdxph{position:relative;border-radius:18px;background:#fff;box-shadow:0 5px 0 var(--sbd,#c48a0c);min-width:0;min-height:0}',
'.mdxph.on{box-shadow:0 5px 0 var(--sbd,#c48a0c),0 0 0 4px #FFC531}',
'.mdxph>button.mdxpic{position:absolute;inset:5px;border:0;padding:0;border-radius:14px;overflow:hidden;background:#fff;cursor:pointer;-webkit-tap-highlight-color:transparent}',
'.mdxph>button.mdxpic img{width:100%;height:100%;object-fit:contain;display:block;pointer-events:none}',
'.mdxstar{position:absolute;right:-4px;top:-4px;z-index:2;width:clamp(44px,calc(var(--s,120px)*.3),60px);height:clamp(44px,calc(var(--s,120px)*.3),60px);border-radius:50%;border:0;background:#fff;box-shadow:0 3px 0 rgba(8,17,48,.22);display:flex;align-items:center;justify-content:center;padding:0;cursor:pointer}',
'.mdxstar svg{width:68%;height:68%}.mdxstar svg path{fill:#fff;stroke:#081130;stroke-width:2;stroke-linejoin:round}',
'.mdxph.on .mdxstar svg path,.mdview .mdxstar.on svg path{fill:#FFC531}.mdview .mdxstar{position:static;width:72px;height:72px}',
'.mdview.mdxposter img{max-height:calc(100% - 120px)}',
/* (later 12 Nov) the Make it move button on a drawing opened in My drawings: the same blue film clapper as the finish screen */
'.mdview .mdvb{align-items:center}',
'.mdview .mdxmim{flex:none;width:76px;height:76px;border:0;border-radius:50%;background:#2a8fd6;box-shadow:0 6px 0 #1b5f94;display:flex;align-items:center;justify-content:center;padding:0;cursor:pointer;animation:funwig 2.6s ease-in-out 1s infinite;-webkit-tap-highlight-color:transparent}',
'.mdview .mdxmim svg{width:52px;height:52px;display:block}',
'.mdview .mdxmim:active{transform:translateY(5px);box-shadow:0 1px 0 #1b5f94}',
'@media (max-width:380px){.mdview .mdxmim{width:66px;height:66px}.mdview .mdxmim svg{width:46px;height:46px}}',
'@media (prefers-reduced-motion:reduce){.mdview .mdxmim{animation:none}}',
/* (evening 12 Nov) the all-photos button beside Make it move, with how many photos the letter has */
'.mdview .mdvb .mdxall{position:relative}',
'.mdview .mdxall .mdxn{position:absolute;right:-6px;top:-6px;min-width:28px;height:28px;padding:0 7px;box-sizing:border-box;border-radius:999px;background:#FFC531;color:#081130;box-shadow:0 0 0 2.5px #081130;display:flex;align-items:center;justify-content:center;font:900 16px/1 '+FONT+';pointer-events:none}',
/* the medal moment */
'#mdxwin{position:fixed;inset:0;z-index:96;background:rgba(8,17,48,.74);display:flex;align-items:center;justify-content:center;animation:fade .2s both;cursor:pointer}',
'#mdxwin .w{position:relative;width:min(70vw,300px);aspect-ratio:3/4;background:#fff;border-radius:28px;box-shadow:0 8px 0 var(--pd,#c79410);display:flex;align-items:center;justify-content:center;padding:18px 18px 80px;animation:pop .45s cubic-bezier(.3,1.5,.5,1) both}',
'#mdxwin .w>img{max-width:100%;max-height:100%;object-fit:contain}',
'#mdxwin .w .sbbd{position:absolute;left:50%;bottom:34px;transform:translateX(-50%);width:44%}#mdxwin .w .sbbd svg{display:block;width:100%;height:auto}',
'#mdxwin .md{position:absolute;left:50%;top:-46px;width:96px;margin-left:-48px;animation:mdxpop .75s cubic-bezier(.3,1.6,.5,1) .3s both}#mdxwin .md svg{display:block;width:100%;height:auto}',
'#mdxwin .wt{width:min(56vw,230px);animation:mdxpop .8s cubic-bezier(.3,1.6,.5,1) .1s both}#mdxwin .wt svg{display:block;width:100%;height:auto}',
'@keyframes mdxpop{from{transform:scale(0) rotate(-30deg);opacity:0}to{transform:none;opacity:1}}',
/* 5. print sheet */
'#sbprwrap{position:fixed;inset:0;z-index:98;background:rgba(8,17,48,.88);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;padding:max(16px,env(safe-area-inset-top,0px)) 16px max(16px,env(safe-area-inset-bottom,0px));--acc:#FFC531;--deep:#c79410;--ink:#081130;--navy:#081130}',
'#sbprwrap .sbprpage{width:min(100%,calc((100vh - 150px) * 186 / 255));aspect-ratio:186/255;background:#fff;border-radius:6px;box-shadow:0 10px 30px rgba(0,0,0,.35);overflow:hidden;flex:none}',
'@supports (height:100dvh){#sbprwrap .sbprpage{width:min(100%,calc((100dvh - 150px) * 186 / 255))}}',
'#sbprwrap .sbprpage>svg{display:block;width:100%;height:100%}',
'#sbprwrap .sbprbar{display:flex;gap:16px;align-items:center;flex:none}',
'#sbprwrap .sbprbar .round{width:64px;height:64px}#sbprwrap .sbprbar .big{width:auto;min-width:170px;height:64px;padding:0 30px;margin:0}',
'#sbprwrap .sbprbar svg{width:34px;height:34px}',
'@media print{@page{size:auto;margin:12mm}',
' html.sbprinting,html.sbprinting body{background:#fff!important;height:auto!important;min-height:0!important;overflow:visible!important;position:static!important}',
' html.sbprinting body>*:not(#sbprwrap){display:none!important}',
' html.sbprinting #sbprwrap{position:static!important;display:block!important;background:#fff!important;padding:0!important;inset:auto!important}',
' html.sbprinting #sbprwrap .sbprbar{display:none!important}',
' html.sbprinting #sbprwrap .sbprpage{width:186mm!important;height:255mm!important;box-shadow:none!important;border-radius:0!important;margin:0!important;aspect-ratio:auto!important}',
' html.sbprinting #sbprwrap .sbprpage>svg{width:186mm!important;height:255mm!important}}',
/* 5. print section on the Grown-ups page */
'.grc.sbprc .sbprg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:12px}',
'.sbprs,.sbprd{position:relative;aspect-ratio:1;border:0;border-radius:16px;background:#fff6e0;box-shadow:0 4px 0 var(--pd,rgba(8,17,48,.16));padding:6px 6px 20px;display:flex;align-items:center;justify-content:center;cursor:pointer;-webkit-tap-highlight-color:transparent}',
'.sbprd{background:#fff;box-shadow:0 4px 0 rgba(8,17,48,.16);padding:6px;border:2px solid #f0e8d2}',
'.sbprs:disabled{opacity:.35;cursor:default}.sbprs img,.sbprd img{max-width:100%;max-height:100%;object-fit:contain;display:block;pointer-events:none}',
'.sbprs .sbbd{position:absolute;left:50%;bottom:5px;transform:translateX(-50%);width:56%}.sbprs .sbbd svg{display:block;width:100%;height:auto}',
'.sbprd .sbl{position:absolute;left:4px;top:4px;min-width:24px;height:24px;padding:0 5px;border-radius:999px;background:#081130;color:#fff;display:flex;align-items:center;justify-content:center;font:900 14px/1 '+FONT+'}',
'.sbprhd{grid-column:1/-1;display:flex;align-items:center;gap:10px}.sbprhd .round{width:44px;height:44px}.sbprhd .round svg{width:22px;height:22px}',
'.sbprhd img{height:44px;width:44px;object-fit:contain}.sbprhd .sbbd{width:62px}.sbprhd .sbbd svg{display:block;width:100%;height:auto}'
].join('\n');
document.body.appendChild(st);

/* ================================================================ 1. no "What you need" page */
function fromSteps(){var p=(typeof V!=='undefined'&&V)?V.p:null,info=p&&p.key?colOfKey(p.key):null;
 if(info&&clickSet(info.c.id)){if(has('showOnly'))showOnly('proj');if(p)openPv(p);return}
 if(has('showOnly'))showOnly('proj');try{renderProj()}catch(e){}if(p)openPv(p)}
function wireBack(){var vb=G('vback');if(vb&&vb.onclick!==fromSteps)vb.onclick=fromSteps}
wireBack();

/* ================================================================ 2. the card: play, heart, printer */
function canPrint(p){try{return !!(p&&p.key&&p.type==='draw'&&typeof DX!=='undefined'&&DX.has(p.key))}catch(e){return false}}
function decorate(p){var pv=G('pv');if(!pv||!p)return;var th=pv.querySelector('.pvc .th');if(!th)return;
 /* play goes straight to the steps */
 var go=G('pvgo');if(go&&!go.__sbx){go.__sbx=1;var oc=go.onclick;go.onclick=function(e){if(oc)oc.call(this,e);var mt=G('mt'),b=G('mtgo');if(mt&&b&&!mt.classList.contains('hide'))b.click()}}
 /* the heart */
 var on=false;try{on=isFav(p)}catch(e){}
 var h=document.createElement('button');h.className='pvhb';h.setAttribute('aria-label','Favourite');h.setAttribute('aria-pressed',on?'true':'false');h.innerHTML=heart(on);
 h.onclick=function(e){e.stopPropagation();try{var k=dk(p);if(FAV[k])delete FAV[k];else FAV[k]=1;saveFav();var o=!!FAV[k];h.innerHTML=heart(o);h.setAttribute('aria-pressed',o?'true':'false');h.classList.remove('pop');void h.offsetWidth;if(o)h.classList.add('pop')}catch(x){}};
 th.appendChild(h)}
if(has('openPv')){var _op=window.openPv;window.openPv=function(p){var r=_op.apply(this,arguments);try{decorate(p)}catch(e){if(window.console)console.error(e)}return r}}

/* ================================================================ 3. swiping between sets */
var SWT=0;
document.addEventListener('click',function(e){if(!PASS&&Date.now()-SWT<450){e.preventDefault();e.stopPropagation()}},true);
function swiper(el,can,go){if(!el||el.__sbsw)return;el.__sbsw=1;var sx=0,sy=0,stt=0,on=false;
 function down(x,y){if(!can())return;on=true;sx=x;sy=y;stt=Date.now()}
 function up(x,y){if(!on)return;on=false;var dx=x-sx,dy=y-sy;if(Math.abs(dx)>55&&Math.abs(dx)>Math.abs(dy)*1.4&&Date.now()-stt<900){SWT=Date.now();go(dx<0?1:-1)}}
 el.addEventListener('touchstart',function(e){if(e.touches.length===1)down(e.touches[0].clientX,e.touches[0].clientY);else on=false},{passive:true});
 el.addEventListener('touchend',function(e){var t=e.changedTouches&&e.changedTouches[0];if(t)up(t.clientX,t.clientY)},{passive:true});
 el.addEventListener('touchcancel',function(){on=false},{passive:true});
 el.addEventListener('pointerdown',function(e){if(e.pointerType==='mouse'||e.pointerType==='pen')down(e.clientX,e.clientY)});
 el.addEventListener('pointerup',function(e){if(e.pointerType==='mouse'||e.pointerType==='pen')up(e.clientX,e.clientY)})}
function anim(el,cls){if(!el)return;['sbsl','sbsr','sbnl','sbnr'].forEach(function(c){el.classList.remove(c)});void el.offsetWidth;el.classList.add(cls)}
function dotsFor(host,id){if(!host)return;var d=host.querySelector(':scope > .sbsdots');if(!d){d=document.createElement('div');d.className='sbsdots';d.setAttribute('aria-hidden','true');host.appendChild(d)}
 var R=rows(),n=0;R.forEach(function(r){n+=r.length});
 if(!id||n<2){d.style.display='none';return}d.style.display='';d.innerHTML=R.map(function(r){return r.map(function(x){return'<i'+(x===id?' class="on"':'')+'></i>'}).join('')}).join('<b></b>')}
/* the set screen inside Draw */
function curSetId(){var el=document.querySelector('#proj.sbcolm #plogo .sbch');if(!el)return null;var n=el.getAttribute('aria-label'),id=null;sets().forEach(function(cat){cat.cols.forEach(function(c){if(c.n===n)id=c.id})});return id}
function setScreenOn(){var pj=G('proj'),pv=G('pv');return !!(pj&&!pj.classList.contains('hide')&&pj.classList.contains('sbcolm')&&(!pv||pv.classList.contains('hide'))&&!G('sbprwrap'))}
function goSet(dir){var id=curSetId();if(!id)return;var nx=neighbour(id,dir);if(!nx){anim(G('pgrid'),dir>0?'sbnl':'sbnr');return}if(clickSet(nx))anim(G('pgrid'),dir>0?'sbsl':'sbsr')}
if(has('renderProj')){var _rp=window.renderProj;window.renderProj=function(){var r=_rp.apply(this,arguments);try{var pj=G('proj');if(pj&&pj.classList.contains('sbcolm'))dotsFor(pj,curSetId())}catch(e){}return r}}
swiper(G('proj'),setScreenOn,goSet);
document.addEventListener('keydown',function(e){if(e.key!=='ArrowLeft'&&e.key!=='ArrowRight')return;
 if(setScreenOn()){e.preventDefault();goSet(e.key==='ArrowRight'?1:-1)}
 else if(mdSetOn()){e.preventDefault();mdGo(e.key==='ArrowRight'?1:-1)}});

/* ================================================================ 4. My drawings, the collecting game */
function getAll(name,os){return new Promise(function(res){try{var r=indexedDB.open(name,1);r.onupgradeneeded=function(){r.result.createObjectStore(os,{keyPath:'id'})};r.onsuccess=function(){try{var q=r.result.transaction(os).objectStore(os).getAll();q.onsuccess=function(){res(q.result||[])};q.onerror=function(){res([])}}catch(e){res([])}};r.onerror=function(){res([])}}catch(e){res([])}})}
function starsMap(){try{return JSON.parse(localStorage.getItem('sbstar')||'{}')||{}}catch(e){return{}}}
function setStar(key,id){var s=starsMap();s[key]=id;try{localStorage.setItem('sbstar',JSON.stringify(s))}catch(e){}}
function chosen(key,list){var id=starsMap()[key];for(var i=0;i<list.length;i++)if(list[i].id===id)return list[i];return list[0]}
function need(c){var t=SLOTS[c.set].length;return{b:c.set==='09'?3:5,s:Math.ceil(t/2),g:t,t:t}}
function level(c,n){var q=need(c);return n>=q.g?3:n>=q.s?2:n>=q.b?1:0}
function isPhoto(m){return m&&m.prod==='draw'&&m.kind==='img'&&m.blob}
function countIn(c,keys){var h=c.has||{},n=0;Object.keys(h).forEach(function(s){if(keys[h[s]])n++});return n}
function keysOf(recs){var k={};(recs||[]).forEach(function(m){if(isPhoto(m)&&m.key)k[m.key]=1});return k}

var BY={},OLD=[],URLS={},ST={lv:0,c:null,cat:null,slot:null};
function url(o){if(!URLS[o.id])URLS[o.id]=URL.createObjectURL(o.blob);return URLS[o.id]}
function made(c){var k={};Object.keys(BY).forEach(function(x){if(BY[x].length)k[x]=1});return countIn(c,k)}
function load(){return Promise.all([getAll('stepby-makes','m'),getAll('stepby-drawings','d')]).then(function(r){
 var inSet={};sets().forEach(function(cat){cat.cols.forEach(function(c){var h=c.has||{};Object.keys(h).forEach(function(s){inSet[h[s]]=1})})});
 BY={};OLD=[];
 r[0].filter(isPhoto).forEach(function(m){if(m.key&&inSet[m.key])(BY[m.key]=BY[m.key]||[]).push(m);else OLD.push(m)});
 r[1].filter(function(d){return d.blob}).forEach(function(d){OLD.push(d)});
 Object.keys(BY).forEach(function(k){BY[k].sort(function(a,b){return(b.t||0)-(a.t||0)})});OLD.sort(function(a,b){return(b.t||0)-(a.t||0)});
 var live={};Object.keys(BY).forEach(function(k){BY[k].forEach(function(o){live[o.id]=1})});OLD.forEach(function(o){live[o.id]=1});
 Object.keys(URLS).forEach(function(id){if(!live[id]){URL.revokeObjectURL(URLS[id]);delete URLS[id]}})})}

function head(h,cls){var b=document.querySelector('#mydraw .achtop b');if(!b)return;b.className=cls||'';b.innerHTML=h}
function spacer(h){var s=document.querySelector('#mydraw .achtop .sp');if(s)s.innerHTML=h||''}
function fit(g){if(!g)return;var n=g.children.length;if(!n)return;var r=g.getBoundingClientRect(),W=r.width,H=r.height,gap=10,best=0,bc=1;if(W<50||H<50)return;
 for(var c=1;c<=8;c++){var rw=Math.ceil(n/c),s=Math.min((W-(c-1)*gap)/c,(H-(rw-1)*gap)/rw);if(s>best+.5){best=s;bc=c}}
 best=Math.floor(Math.min(best,n<3?300:220));var rr=Math.ceil(n/bc);
 g.style.gridTemplateColumns='repeat('+bc+','+best+'px)';g.style.gridTemplateRows='repeat('+rr+','+best+'px)';g.style.setProperty('--s',best+'px')}
function refit(){var g=document.querySelector('#mdin .mdxgrid');if(g)fit(g)}
function closeView(){[].forEach.call(document.querySelectorAll('#mydraw .mdview'),function(v){v.remove()})}
/* (later 12 Nov) the big star is off the opened drawing for now: just Make it move and the cross. The small star on each
   photo of the letter still picks the main one. Set VIEWSTAR to true to bring the big star back. */
var VIEWSTAR=false;
function view(o,key){closeView();var v=document.createElement('div');v.className='mdview mdv1';
 var all=key?(BY[key]||[]):[],on=key&&chosen(key,all).id===o.id,mv=!!(key&&canMove()),many=all.length>1;
 v.innerHTML='<img src="'+url(o)+'" alt=""><div class="mdvb">'+(many?'<button class="round mdxall" type="button" aria-label="All '+all.length+' drawings">'+IC.pics+'<span class="mdxn" aria-hidden="true">'+all.length+'</span></button>':'')+(key&&VIEWSTAR?'<button class="mdxstar'+(on?' on':'')+'" aria-label="Show this one for the letter" aria-pressed="'+(on?'true':'false')+'">'+IC.star+'</button>':'')+(mv?'<button class="mdxmim" type="button" aria-label="Make it move">'+IC.mim+'</button>':'')+'<button class="round" aria-label="Close">'+IC.x+'</button></div>';
 v.onclick=function(){v.remove()};
 var a=v.querySelector('.mdxall');if(a)a.onclick=function(e){e.stopPropagation();openAll(key)};
 var s=v.querySelector('.mdxstar');if(s)s.onclick=function(e){e.stopPropagation();setStar(key,o.id);v.remove();draw()};
 var m=v.querySelector('.mdxmim');if(m)m.onclick=function(e){e.stopPropagation();makeItMove(o,key)};
 G('mydraw').appendChild(v)}
/* (evening 12 Nov) a letter's photos all together, opened from its Make it move view; back from there, or picking a
   photo, returns to the Make it move view with the main photo */
function openAll(key){var c=ST.c,s=null;if(c){var h=c.has||{};Object.keys(h).forEach(function(x){if(h[x]===key)s=x})}
 if(s)ST={lv:2,c:c,cat:ST.cat,slot:s};else{var w=colOfKey(key);if(!w)return;ST={lv:2,c:w.c,cat:w.cat,slot:w.slot}}
 closeView();draw()}
function backToPhoto(key){var L=BY[key]||[];ST.lv=1;draw();if(L.length)view(chosen(key,L),key)}
var pickT=null;
function pickPhoto(key,o){if(!o)return;setStar(key,o.id);draw();clearTimeout(pickT);
 /* a moment to see the star move, then straight back to Make it move with that photo */
 pickT=setTimeout(function(){if(ST.lv===2&&ST.c&&(ST.c.has||{})[ST.slot]===key)backToPhoto(key)},280)}

/* (later 12 Nov) Make it move from My drawings: plays this photo, the same story films as the finish screen.
   No camera here (photos only come from the finish screen), so the end has the three faces, Magic and save, but no retake.
   Closing it comes back to this same photo in My drawings. */
function canMove(){var S=window.__showTest;return !!(S&&typeof S.run==='function')}
function projOf(key){try{return(typeof REG!=='undefined'&&REG[key])||null}catch(e){return null}}
function makeItMove(o,key){var S=window.__showTest,md=G('mydraw');if(!S||!S.run||!o||!o.blob)return;var p=projOf(key);
 var item={src:'make',blob:o.blob,key:key,title:o.title||(p&&(p.t||p.title))||key};
 function back(){var pl=G('shplay');if(pl)pl.classList.add('hide');if(md)md.classList.remove('hide')}
 if(md)md.classList.add('hide');
 /* started straight from the tap, so the sound can play on phones */
 S.run([item],'cool',back,{mim:true,magic:function(){back();magicFor(o,key)}})}
/* Magic hands needs a drawing to be open; if none is (opened straight from My drawings) it borrows this one until it closes */
function magicFor(o,key){var M=window.__magicHands;if(!M||typeof M.open!=='function')return;var lent=null;
 try{if(typeof V!=='undefined'&&V&&!V.p){var p=projOf(key);if(p){V.p=p;lent=p}}}catch(e){}
 try{M.open(o)}catch(e){}
 if(lent){var n=0,t=setInterval(function(){if(!G('mh')||++n>7200){clearInterval(t);try{if(V.p===lent)V.p=null}catch(e){}}},250)}}
function wiggle(el){if(!el)return;el.classList.remove('wig');void el.offsetWidth;el.classList.add('wig')}

/* level 0: the nine sets */
function drawSets(){var m=G('mdin'),cats=sets();head('My drawings','');spacer('');dotsFor(G('mydraw'),null);
 var total=0,golds=0;ORDER.forEach(function(set){cats.forEach(function(cat){var c=colIn(cat,set);if(c){total++;if(level(c,made(c))===3)golds++}})});
 var h='<div class="mdxstrip" role="img" aria-label="'+golds+' of '+total+' sets finished">';
 for(var i=0;i<total;i++)h+='<span class="mdxdot'+(i<golds?' on':'')+'">'+(i<golds?IC.star:'')+'</span>';
 h+='<button class="mdxcup'+(total&&golds>=total?' won':'')+'" aria-label="Trophy">'+IC.cup+'</button></div>';
 h+=ORDER.map(function(set){return'<div class="mdxrow">'+cats.map(function(cat,ci){var c=colIn(cat,set);if(!c)return'';var n=made(c),q=need(c),l=level(c,n);
  return'<button class="mdxcard'+(l===3?' gold':'')+'" data-c="'+ci+'" data-s="'+set+'" style="--pd:'+cat.d+'" aria-label="'+esc(c.n)+', '+n+' of '+q.t+'"><img src="img/'+c.cv+'.webp" alt="" draggable="false"><span class="mdxmed'+(l?'':' no')+'">'+medal(l)+'</span><span class="sbbd">'+BADGE[set]+'</span><span class="mdxbar"><i style="width:'+Math.round(n/q.t*100)+'%"></i></span></button>'}).join('')+'</div>'}).join('');
 if(OLD.length)h+='<div class="mdxold">'+OLD.map(function(o,i){return'<button class="mdc" data-i="'+i+'" aria-label="Drawing"><img src="'+url(o)+'" alt=""></button>'}).join('')+'</div>';
 m.innerHTML=h;
 [].forEach.call(m.querySelectorAll('.mdxcard'),function(b){b.onclick=function(){var cat=cats[+b.getAttribute('data-c')],c=colIn(cat,b.getAttribute('data-s'));ST={lv:1,c:c,cat:cat,slot:null};draw()}});
 var cup=m.querySelector('.mdxcup');if(cup)cup.onclick=function(){if(cup.classList.contains('won'))celebrate(null,null,0,true);else wiggle(cup)};
 [].forEach.call(m.querySelectorAll('.mdxold .mdc'),function(b){b.onclick=function(){view(OLD[+b.getAttribute('data-i')],null)}})}

/* level 1: one set, every letter or number */
function drawSet(){var m=G('mdin'),c=ST.c,cat=ST.cat,hs=c.has||{},n=made(c),q=need(c),l=level(c,n);
 head('<img src="img/'+c.cv+'.webp" alt=""><span class="sbbd">'+BADGE[c.set]+'</span><span class="mdxhm">'+medal(l)+'</span><span class="mdxcnt">'+n+'/'+q.t+'</span>','mdxh');
 spacer(l===3?'<button class="round mdxpost" aria-label="See the whole set as one picture">'+IC.frame+'</button>':'');
 var pb=document.querySelector('#mydraw .mdxpost');if(pb)pb.onclick=function(){openPoster(c,cat)};
 m.innerHTML='<div class="mdxgrid" style="--sbd:'+cat.d+'">'+SLOTS[c.set].map(function(s,i){var L=hs[s]&&BY[hs[s]],dl='animation-delay:'+(i*14)+'ms';
  if(L&&L.length)return'<button class="sbslot sbm" data-s="'+s+'" style="'+dl+'" aria-label="'+s+', '+L.length+(L.length>1?' drawings':' drawing')+'"><span class="sbth"><img src="'+url(chosen(hs[s],L))+'" alt="" draggable="false"></span><span class="sbl" aria-hidden="true">'+s+'</span>'+(L.length>1?'<span class="mdxmore" aria-hidden="true">'+L.length+'</span>':'')+'</button>';
  return'<button class="sbslot sbsoon mdxno" style="'+dl+'" aria-label="'+s+' (no drawing yet)"><span class="sbgl" aria-hidden="true">'+s+'</span></button>'}).join('')+'</div>';
 /* (evening 12 Nov) a letter with drawings opens straight on its main photo, ready for Make it move */
 [].forEach.call(m.querySelectorAll('.sbslot'),function(b){b.onclick=b.classList.contains('sbm')?function(){var s=b.getAttribute('data-s'),key=hs[s],L=BY[key]||[];if(!L.length)return;ST.slot=s;view(chosen(key,L),key)}:function(){wiggle(b)}});
 dotsFor(G('mydraw'),c.id);refit();requestAnimationFrame(refit)}

/* level 2: one letter, every photo of it; the star picks the one that shows. (evening 12 Nov) Opened only from the
   all-photos button; tapping a photo or its star makes it the main one and goes back to Make it move with it */
function drawSlot(){var m=G('mdin'),c=ST.c,cat=ST.cat,key=(c.has||{})[ST.slot],L=BY[key]||[];
 if(!L.length){ST.lv=1;return drawSet()}
 var pick=chosen(key,L).id;spacer('');dotsFor(G('mydraw'),null);
 head('<img src="img/'+c.cv+'.webp" alt=""><span class="mdxl">'+esc(ST.slot)+'</span>','mdxh');
 m.innerHTML='<div class="mdxgrid" style="--sbd:'+cat.d+'">'+L.map(function(o,i){var on=o.id===pick;
  return'<div class="mdxph'+(on?' on':'')+'"><button class="mdxpic" data-i="'+i+'" aria-label="Drawing '+(L.length-i)+'"><img src="'+url(o)+'" alt="" draggable="false"></button><button class="mdxstar" data-i="'+i+'" aria-label="Show this one for the letter" aria-pressed="'+(on?'true':'false')+'">'+IC.star+'</button></div>'}).join('')+'</div>';
 [].forEach.call(m.querySelectorAll('.mdxpic,.mdxstar'),function(b){b.onclick=function(){pickPhoto(key,L[+b.getAttribute('data-i')])}});
 refit();requestAnimationFrame(refit)}

function draw(){var m=G('mdin');if(!m)return;closeView();m.classList.add('mdx');if(ST.lv===2)drawSlot();else if(ST.lv===1)drawSet();else drawSets()}
function mdSetOn(){var s=G('mydraw');return !!(s&&!s.classList.contains('hide')&&ST.lv===1&&!s.querySelector('.mdview')&&!G('sbprwrap'))}
function mdGo(dir){var nx=ST.c?neighbour(ST.c.id,dir):null,g=document.querySelector('#mdin .mdxgrid');if(!nx){anim(g,dir>0?'sbnl':'sbnr');return}
 var o=colById(nx);if(!o)return;ST={lv:1,c:o.c,cat:o.cat,slot:null};draw();anim(document.querySelector('#mdin .mdxgrid'),dir>0?'sbsl':'sbsr')}
var homeBack=null;
function back(){if(ST.lv===2){var bk=((ST.c&&ST.c.has)||{})[ST.slot];clearTimeout(pickT);if(bk)backToPhoto(bk);else{ST.lv=1;draw()}}else if(ST.lv===1){ST={lv:0,c:null,cat:null,slot:null};draw()}else if(homeBack)homeBack();else goHomeScreen()}
function open(state){var s=G('mydraw');if(!s)return;
 [].forEach.call(document.querySelectorAll('#app > section.scr'),function(x){x.classList.add('hide')});['pv','sheet'].forEach(function(i){var e=G(i);if(e)e.classList.add('hide')});
 s.classList.remove('hide');var bk=G('mdback');if(bk&&bk.onclick!==back){homeBack=bk.onclick;bk.onclick=back}
 swiper(s,mdSetOn,mdGo);
 ST=state||{lv:0,c:null,cat:null,slot:null};load().then(draw)}
/* the home buttons open this page (caught first, so the older list never shows) */
document.addEventListener('click',function(e){var t=e.target&&e.target.closest&&e.target.closest('#drawtile,#mdtile');if(!t)return;e.preventDefault();e.stopPropagation();open()},true);
window.addEventListener('resize',refit);

/* the medal moment: when a new photo earns a set its next medal */
function celebrate(c,cat,l,all){var w=G('mdxwin');if(w)w.remove();w=document.createElement('div');w.id='mdxwin';w.setAttribute('role','dialog');
 if(all){w.setAttribute('aria-label','Trophy');w.innerHTML='<div class="wt">'+IC.cup+'</div>'}
 else{w.setAttribute('aria-label',['','Bronze','Silver','Gold'][l]+' medal');w.innerHTML='<div class="w" style="--pd:'+cat.d+'"><img src="img/'+c.cv+'.webp" alt=""><span class="sbbd">'+BADGE[c.set]+'</span><span class="md">'+medal(l)+'</span></div>'}
 w.onclick=function(){w.remove()};document.body.appendChild(w);try{if(has('confetti'))confetti()}catch(e){}
 setTimeout(function(){if(w.parentNode)w.remove()},3800)}
function hookPut(){var M=window.__showTest&&window.__showTest.makes;if(!M)return false;if(M.__medal)return true;M.__medal=1;var put=M.put;
 M.put=function(rec){var self=this,args=arguments,info=isPhoto(rec)&&rec.key?colOfKey(rec.key):null;if(!info)return put.apply(self,args);
  return M.all().then(function(a){var before=keysOf(a),after=keysOf(a.concat([rec])),l0=level(info.c,countIn(info.c,before)),l1=level(info.c,countIn(info.c,after));
   return Promise.resolve(put.apply(self,args)).then(function(v){if(l1>l0){var all=true;sets().forEach(function(cat){cat.cols.forEach(function(c){if(level(c,countIn(c,after))<3)all=false})});
     setTimeout(function(){celebrate(info.c,info.cat,l1,all&&l1===3)},700)}return v})},function(){return put.apply(self,args)})};
 return true}
if(!hookPut()){var hp=0,ht=setInterval(function(){if(hookPut()||++hp>40)clearInterval(ht)},250)}

/* a finished set as one picture */
function loadImg(src){return new Promise(function(res){var im=new Image();im.onload=function(){res(im)};im.onerror=function(){res(null)};im.src=src})}
function rr(g,x,y,w,h,r){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath()}
function posterCanvas(c){var slots=SLOTS[c.set],hs=c.has||{},cols=c.set==='09'?5:6,rn=Math.ceil(slots.length/cols),W=1800,pad=70,gap=26,cell=Math.floor((W-pad*2-gap*(cols-1))/cols),top=320,H=top+rn*cell+(rn-1)*gap+pad;
 var bu=URL.createObjectURL(new Blob([BADGE[c.set].replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" width="840" height="360" ')],{type:'image/svg+xml'}));
 var jobs=[loadImg('img/'+c.cv+'.webp'),loadImg(bu)].concat(slots.map(function(s){var L=hs[s]&&BY[hs[s]];return L&&L.length?loadImg(url(chosen(hs[s],L))):Promise.resolve(null)}));
 return Promise.all(jobs).then(function(im){URL.revokeObjectURL(bu);var cv=document.createElement('canvas');cv.width=W;cv.height=H;var g=cv.getContext('2d');
  g.fillStyle='#fff6e0';g.fillRect(0,0,W,H);
  var cov=im[0],bd=im[1],ch=230,cw=cov?ch*cov.width/cov.height:0,bw=320,bh=bw*36/84,tw=cw+(cov?40:0)+bw,x0=(W-tw)/2;
  if(cov)g.drawImage(cov,x0,44,cw,ch);if(bd)g.drawImage(bd,x0+cw+(cov?40:0),44+(ch-bh)/2,bw,bh);
  slots.forEach(function(s,i){var r=Math.floor(i/cols),k=i%cols,inRow=Math.min(cols,slots.length-r*cols),off=(cols-inRow)*(cell+gap)/2,x=pad+off+k*(cell+gap),y=top+r*(cell+gap);
   g.save();g.shadowColor='rgba(8,17,48,.16)';g.shadowOffsetY=10;rr(g,x,y,cell,cell,30);g.fillStyle='#fff';g.fill();g.restore();
   var ph=im[2+i];if(ph){var sc=Math.min((cell-28)/ph.width,(cell-28)/ph.height),w=ph.width*sc,h=ph.height*sc;g.save();rr(g,x+8,y+8,cell-16,cell-16,24);g.clip();g.drawImage(ph,x+(cell-w)/2,y+(cell-h)/2,w,h);g.restore()}
   rr(g,x+12,y+12,66,66,33);g.fillStyle='#081130';g.fill();g.fillStyle='#fff';g.font='900 46px Arial,Helvetica,sans-serif';g.textAlign='center';g.textBaseline='middle';g.fillText(s,x+45,y+47)});
  return cv})}
/* (printing a poster is on the Grown-ups page only) */
function openPoster(c,cat){posterCanvas(c).then(function(cv){var u=cv.toDataURL('image/jpeg',.9);closeView();var v=document.createElement('div');v.className='mdview mdxposter';
 v.innerHTML='<img src="'+u+'" alt="'+esc(c.n)+'"><div class="mdvb"><button class="round mdxpx" aria-label="Close">'+IC.x+'</button></div>';
 v.onclick=function(){v.remove()};G('mydraw').appendChild(v)})}

/* ================================================================ 5. print sheets */
var LOGO=null;
function logo(){if(LOGO)return Promise.resolve(LOGO);return loadImg('img/33811a1051920075.webp').then(function(im){if(!im)return null;try{var c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;c.getContext('2d').drawImage(im,0,0);LOGO={u:c.toDataURL('image/png'),w:im.naturalWidth,h:im.naturalHeight}}catch(e){LOGO={u:'img/33811a1051920075.webp',w:im.naturalWidth||3,h:im.naturalHeight||1}}return LOGO})}
function colourURL(p,px,type){var cv=document.createElement('canvas'),u='';cv.style.cssText='position:fixed;left:-9999px;top:0;width:'+px+'px;height:'+px+'px';document.body.appendChild(cv);try{paintFinal(cv,p);u=cv.toDataURL(type||'image/png')}catch(e){}cv.remove();return u}
function paths(items,col,k){return items.map(function(a){return'<path d="'+esc(a.d)+'" fill="none" stroke="'+col+'" stroke-width="'+((a.w||1.4)*k).toFixed(2)+'" stroke-linecap="round" stroke-linejoin="round"/>'}).join('')}
function lineSteps(key){var P=DX.get(key),out=[],prev=[];P.steps.forEach(function(s){var ls=(s.add||[]).filter(function(a){return !a.fill&&a.d});if(ls.length){out.push({old:prev.slice(),add:ls});prev=prev.concat(ls)}});return out}
function svgOpen(){return'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 186 255" preserveAspectRatio="xMidYMid meet"><rect width="186" height="255" fill="#fff"/>'}
function nested(svg,x,y,w,h){return svg.replace('<svg ','<svg x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" ')}
var TXT='font-family="Arial Rounded MT Bold,Arial,Helvetica,sans-serif" font-weight="900"';
/* one sheet per drawing: steps along the top, a box to draw in; the four black squares let the camera find the box */
function drawingSheet(p){return logo().then(function(L){var steps=lineSteps(p.key),N=steps.length,info=colOfKey(p.key),o=[svgOpen()],lw=0;
 if(L){var lh=15;lw=lh*L.w/L.h;o.push('<image href="'+L.u+'" x="0" y="0" width="'+lw.toFixed(2)+'" height="'+lh+'"/>')}
 if(info)o.push(nested(BADGE[info.c.set],(lw+4).toFixed(2),3,22,9.4));
 o.push('<text x="0" y="29" '+TXT+' font-size="7.4" fill="#081130">'+esc(p.t)+'</text>');
 o.push('<rect x="150" y="0" width="36" height="36" rx="4" fill="#fff" stroke="#d5d9df" stroke-width=".4"/><image href="'+colourURL(p,300)+'" x="151.5" y="1.5" width="33" height="33"/>');
 var gap=3,cols=N<=6?Math.max(1,N):Math.ceil(N/2),rn=N<=6?1:2,cell=Math.min((186-(cols-1)*gap)/cols,34),gy=41;
 steps.forEach(function(s,i){var r=Math.floor(i/cols),k=i%cols,inRow=Math.min(cols,N-r*cols),gx=(186-(inRow*cell+(inRow-1)*gap))/2,x=gx+k*(cell+gap),y=gy+r*(cell+gap);
  o.push('<rect x="'+x.toFixed(2)+'" y="'+y.toFixed(2)+'" width="'+cell.toFixed(2)+'" height="'+cell.toFixed(2)+'" rx="3" fill="#fff" stroke="#cfd4da" stroke-width=".4"/>');
  o.push('<svg x="'+(x+1).toFixed(2)+'" y="'+(y+1).toFixed(2)+'" width="'+(cell-2).toFixed(2)+'" height="'+(cell-2).toFixed(2)+'" viewBox="-4 -4 108 108">'+paths(s.old,'#b9bec6',.8)+paths(s.add,'#111',1)+'</svg>');
  o.push('<circle cx="'+(x+3.8).toFixed(2)+'" cy="'+(y+3.8).toFixed(2)+'" r="2.9" fill="#081130"/><text x="'+(x+3.8).toFixed(2)+'" y="'+(y+5.1).toFixed(2)+'" text-anchor="middle" '+TXT+' font-size="3.6" fill="#fff">'+(i+1)+'</text>')});
 var by=gy+rn*cell+(rn-1)*gap+9,bx=3,bw=180,bh=244-by,m=6,g2=2;
 /* the box: four lines that stop short of the corner squares, so each square stands alone */
 o.push('<g stroke="#444" stroke-width=".8" stroke-linecap="butt">'+
  '<line x1="'+(bx+m/2+g2)+'" y1="'+by.toFixed(2)+'" x2="'+(bx+bw-m/2-g2)+'" y2="'+by.toFixed(2)+'"/>'+
  '<line x1="'+(bx+m/2+g2)+'" y1="'+(by+bh).toFixed(2)+'" x2="'+(bx+bw-m/2-g2)+'" y2="'+(by+bh).toFixed(2)+'"/>'+
  '<line x1="'+bx+'" y1="'+(by+m/2+g2).toFixed(2)+'" x2="'+bx+'" y2="'+(by+bh-m/2-g2).toFixed(2)+'"/>'+
  '<line x1="'+(bx+bw)+'" y1="'+(by+m/2+g2).toFixed(2)+'" x2="'+(bx+bw)+'" y2="'+(by+bh-m/2-g2).toFixed(2)+'"/></g>');
 [[bx,by],[bx+bw,by],[bx,by+bh],[bx+bw,by+bh]].forEach(function(q){o.push('<rect x="'+(q[0]-m/2).toFixed(2)+'" y="'+(q[1]-m/2).toFixed(2)+'" width="'+m+'" height="'+m+'" fill="#000"/>')});
 o.push('<text x="93" y="252.5" text-anchor="middle" '+TXT+' font-size="4.2" fill="#6b7079">step-by.com</text></svg>');
 return o.join('')})}
function posterSheet(u,c){return logo().then(function(L){var o=[svgOpen()],lw=0;
 if(L){var lh=15;lw=lh*L.w/L.h;o.push('<image href="'+L.u+'" x="0" y="0" width="'+lw.toFixed(2)+'" height="'+lh+'"/>')}
 o.push(nested(BADGE[c.set],(lw+4).toFixed(2),3,22,9.4));
 o.push('<image href="'+u+'" x="0" y="22" width="186" height="222" preserveAspectRatio="xMidYMid meet"/>');
 o.push('<text x="93" y="252.5" text-anchor="middle" '+TXT+' font-size="4.2" fill="#6b7079">step-by.com</text></svg>');return o.join('')})}
function closeSheet(){var w=G('sbprwrap');if(w)w.remove();document.documentElement.classList.remove('sbprinting')}
function openSheet(svg){closeSheet();var w=document.createElement('div');w.id='sbprwrap';w.setAttribute('role','dialog');w.setAttribute('aria-label','Print sheet');
 w.innerHTML='<div class="sbprpage">'+svg+'</div><div class="sbprbar"><button class="round" id="sbprx" aria-label="Close">'+IC.x+'</button><button class="big" id="sbprgo" aria-label="Print">'+IC.printer+'</button></div>';
 document.body.appendChild(w);document.documentElement.classList.add('sbprinting');
 G('sbprx').onclick=closeSheet;G('sbprgo').onclick=function(){try{window.print()}catch(e){}}}
/* printing only happens from the Grown-ups page, which is behind its own gate */
document.addEventListener('click',function(e){if(e.target&&e.target.closest&&e.target.closest('#grback'))closeSheet()},true);
function printDrawing(p){drawingSheet(p).then(openSheet)}
/* the print section on the Grown-ups page */
var TH={};
function thumb(p){if(!TH[p.key])TH[p.key]=colourURL(p,150,'image/jpeg');return TH[p.key]}
function printable(c){var h=c.has||{},by={};try{projects('draw').forEach(function(p){by[p.key]=p})}catch(e){}
 return SLOTS[c.set].filter(function(s){var p=h[s]&&by[h[s]];return p&&canPrint(p)}).map(function(s){return{s:s,p:by[h[s]]}})}
function prSets(){var g=G('sbprg');if(!g)return;var cats=sets();
 g.innerHTML=ORDER.map(function(set){return cats.map(function(cat,ci){var c=colIn(cat,set);if(!c)return'';var n=printable(c).length;
  return'<button class="sbprs" data-c="'+ci+'" data-s="'+set+'" style="--pd:'+cat.d+'" aria-label="'+esc(c.n)+', '+n+' to print"'+(n?'':' disabled')+'><img src="img/'+c.cv+'.webp" alt=""><span class="sbbd">'+BADGE[set]+'</span></button>'}).join('')}).join('');
 [].forEach.call(g.querySelectorAll('.sbprs'),function(b){b.onclick=function(){var cat=cats[+b.getAttribute('data-c')];prList(colIn(cat,b.getAttribute('data-s')))}})}
function prList(c){var g=G('sbprg');if(!g||!c)return;var L=printable(c);
 g.innerHTML='<div class="sbprhd"><button class="round" aria-label="All sets">'+IC.back+'</button><img src="img/'+c.cv+'.webp" alt=""><span class="sbbd">'+BADGE[c.set]+'</span></div>'+
  L.map(function(o,i){return'<button class="sbprd" data-i="'+i+'" aria-label="Print '+esc(o.p.t)+'"><img src="'+thumb(o.p)+'" alt=""><span class="sbl" aria-hidden="true">'+esc(o.s)+'</span></button>'}).join('');
 g.querySelector('.sbprhd .round').onclick=prSets;
 [].forEach.call(g.querySelectorAll('.sbprd'),function(b){b.onclick=function(){printDrawing(L[+b.getAttribute('data-i')].p)}})}
/* finished sets: their poster, made from the child's own photos (shown only once a set is finished) */
function addPosters(gi){load().then(function(){var done=[];sets().forEach(function(cat){ORDER.forEach(function(set){var c=colIn(cat,set);if(c&&level(c,made(c))===3)done.push({c:c,cat:cat})})});
 var old=gi.querySelector('.sbpost');if(old)old.remove();if(!done.length)return;
 var d=document.createElement('div');d.className='grc sbprc sbpost';
 d.innerHTML='<b>Print a finished set</b><p>Every drawing in the set on one poster, made from your child\'s own photos.</p><div class="sbprg">'+done.map(function(o,i){return'<button class="sbprs" data-i="'+i+'" style="--pd:'+o.cat.d+'" aria-label="Print the '+esc(o.c.n)+' poster"><img src="img/'+o.c.cv+'.webp" alt=""><span class="sbbd">'+BADGE[o.c.set]+'</span></button>'}).join('')+'</div>';
 var first=gi.querySelector('.sbprc');if(first&&first.nextSibling)gi.insertBefore(d,first.nextSibling);else gi.appendChild(d);
 [].forEach.call(d.querySelectorAll('.sbprs'),function(b){b.onclick=function(){var o=done[+b.getAttribute('data-i')];posterCanvas(o.c).then(function(cv){return posterSheet(cv.toDataURL('image/jpeg',.92),o.c)}).then(openSheet)}})})}
function addPrintSection(gi){var d=document.createElement('div');d.className='grc sbprc';
 d.innerHTML='<b>Print a drawing</b><p>Free sheets for home or school: the steps along the top and a box to draw in. They fit A4 and US Letter paper.</p><div class="sbprg" id="sbprg"></div>';
 gi.insertBefore(d,gi.firstChild);prSets();addPosters(gi)}
function watchGrown(){var gi=G('grin');if(!gi)return false;if(gi.__sbx)return true;gi.__sbx=1;
 new MutationObserver(function(){if(!gi.querySelector('.grc'))return;if(!gi.querySelector('.sbprc'))addPrintSection(gi)}).observe(gi,{childList:true});return true}
if(!watchGrown()){var wg=0,wt=setInterval(function(){if(watchGrown()||++wg>60)clearInterval(wt)},250)}

/* the camera: a photo of a print sheet is cut down to the drawing box */
function findBox(cv){var W0=cv.width,H0=cv.height;if(W0<80||H0<80)return null;
 var s=Math.min(1,560/Math.max(W0,H0)),w=Math.max(40,Math.round(W0*s)),h=Math.max(40,Math.round(H0*s));
 var a=document.createElement('canvas');a.width=w;a.height=h;var x=a.getContext('2d',{willReadFrequently:true});x.drawImage(cv,0,0,w,h);
 var d=x.getImageData(0,0,w,h).data,n=w*h,lum=new Uint8Array(n),dark=new Uint8Array(n),i,j;
 for(i=0,j=0;i<n;i++,j+=4){var L=(d[j]*299+d[j+1]*587+d[j+2]*114)/1000;lum[i]=L;dark[i]=L<100?1:0}
 var lab=new Int32Array(n),stack=new Int32Array(n),comps=[];
 for(var p=0;p<n;p++){if(!dark[p]||lab[p])continue;var id=comps.length+1,sp=0,cnt=0,x0=w,x1=0,y0=h,y1=0;stack[sp++]=p;lab[p]=id;
  while(sp){var q=stack[--sp],qx=q%w,qy=(q-qx)/w;cnt++;if(qx<x0)x0=qx;if(qx>x1)x1=qx;if(qy<y0)y0=qy;if(qy>y1)y1=qy;
   if(qx>0&&dark[q-1]&&!lab[q-1]){lab[q-1]=id;stack[sp++]=q-1}if(qx<w-1&&dark[q+1]&&!lab[q+1]){lab[q+1]=id;stack[sp++]=q+1}
   if(qy>0&&dark[q-w]&&!lab[q-w]){lab[q-w]=id;stack[sp++]=q-w}if(qy<h-1&&dark[q+w]&&!lab[q+w]){lab[q+w]=id;stack[sp++]=q+w}}
  comps.push({x0:x0,x1:x1,y0:y0,y1:y1,n:cnt})}
 var Lm=Math.max(w,h),minS=Lm*.008,maxS=Lm*.06;
 var cand=comps.filter(function(c){var cw=c.x1-c.x0+1,ch=c.y1-c.y0+1;if(cw<minS||ch<minS||cw>maxS||ch>maxS)return false;return Math.min(cw,ch)/Math.max(cw,ch)>.7&&c.n/(cw*ch)>.72})
  .map(function(c){return{x:(c.x0+c.x1)/2,y:(c.y0+c.y1)/2,s:((c.x1-c.x0)+(c.y1-c.y0))/2+1}});
 if(cand.length<4||cand.length>80)return null;
 var tol=Lm*.03,best=null,A,B,C,D;
 for(var i1=0;i1<cand.length;i1++)for(var i2=0;i2<cand.length;i2++){if(i1===i2)continue;A=cand[i1];B=cand[i2];if(B.x-A.x<w*.45||Math.abs(B.y-A.y)>tol)continue;
  for(var i3=0;i3<cand.length;i3++){if(i3===i1||i3===i2)continue;C=cand[i3];if(C.y-A.y<h*.22||Math.abs(C.x-A.x)>tol)continue;
   for(var i4=0;i4<cand.length;i4++){if(i4===i1||i4===i2||i4===i3)continue;D=cand[i4];if(Math.abs(D.x-B.x)>tol||Math.abs(D.y-C.y)>tol)continue;
    var ss=[A.s,B.s,C.s,D.s],mn=Math.min.apply(null,ss),mx=Math.max.apply(null,ss);if(mx>mn*1.6)continue;
    var area=(B.x-A.x)*(C.y-A.y);if(!best||area>best.area)best={A:A,B:B,C:C,D:D,area:area,ms:(A.s+B.s+C.s+D.s)/4}}}}
 if(!best)return null;
 function edge(P,Q){var len=Math.hypot(Q.x-P.x,Q.y-P.y),ux=(Q.x-P.x)/len,uy=(Q.y-P.y)/len,nx=-uy,ny=ux,s0=best.ms*1.3,hits=0,tot=0;
  for(var t=s0;t<len-s0;t+=2){tot++;var ok=false;for(var o=-3;o<=3&&!ok;o++){var px=Math.round(P.x+ux*t+nx*o),py=Math.round(P.y+uy*t+ny*o);if(px>=0&&py>=0&&px<w&&py<h&&lum[py*w+px]<170)ok=true}if(ok)hits++}
  return tot?hits/tot:0}
 if(Math.min(edge(best.A,best.B),edge(best.C,best.D),edge(best.A,best.C),edge(best.B,best.D))<.6)return null;
 var ins=best.ms*.95,r={x:(Math.max(best.A.x,best.C.x)+ins)/s,y:(Math.max(best.A.y,best.B.y)+ins)/s,x2:(Math.min(best.B.x,best.D.x)-ins)/s,y2:(Math.min(best.C.y,best.D.y)-ins)/s};
 if(r.x2-r.x<W0*.3||r.y2-r.y<H0*.2)return null;return r}
function cropBox(res){try{if(!res||!res.page||res.__box)return res;res.__box=1;var b=findBox(res.page);if(!b)return res;
 var cw=Math.round(b.x2-b.x),ch=Math.round(b.y2-b.y),c=document.createElement('canvas');c.width=cw;c.height=ch;c.getContext('2d').drawImage(res.page,Math.round(b.x),Math.round(b.y),cw,ch,0,0,cw,ch);
 res.page=c;res.info=res.info||{};res.info.printBox=true}catch(e){}return res}
function hookScan(){var S=window.SBScan;if(!S)return false;if(S.__box)return true;S.__box=1;
 var pi=S.processImage;S.processImage=function(src,opt){return pi.call(S,src,opt).then(cropBox)};
 var op=S.open;S.open=function(o){o=o||{};var f=o.onPhoto,o2={};for(var k in o)o2[k]=o[k];o2.onPhoto=function(r){if(f)f(cropBox(r))};return op.call(S,o2)};return true}
if(!hookScan()){var hs2=0,hst=setInterval(function(){if(hookScan()||++hs2>40)clearInterval(hst)},250)}

/* ================================================================ 6. home pictures: a drawing from each set (the 123 row keeps its pictures) */
var COVERS={'animals-AZ':'cov_d_parrot','vehicles-AZ':'cov_d_digger','house-AZ':'cov_d_fireplace','animals-az':'cov_d_ladybird','vehicles-az':'cov_d_bus','house-az':'cov_d_coffee'};
function covers(){var cards=document.querySelectorAll('.wlcard[data-set]');if(!cards.length)return false;
 Object.keys(COVERS).forEach(function(id){var o=colById(id);if(o)o.c.cv=COVERS[id];var b=document.querySelector('.wlcard[data-set="'+id+'"] img');if(b)b.src='img/'+COVERS[id]+'.webp'});return true}
if(!covers()){var cv0=0,cvt=setInterval(function(){if(covers()||++cv0>60)clearInterval(cvt)},150)}

/* ================================================================ 7. the home screen: nine big tiles and two rows of buttons */
var HIC={
 play:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="#fff" stroke="#081130" stroke-width="1.8"/><path d="M10 7.5v9l7-4.5z" fill="#081130"/></svg>',
 show:'<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="6" y="19" width="36" height="22" rx="4" fill="#2F7BF5" stroke="#081130" stroke-width="3" stroke-linejoin="round"/><path d="M6 19l3-10 33 5-2 5z" fill="#fff" stroke="#081130" stroke-width="3" stroke-linejoin="round"/><path d="M16 10.2l3 8M25 11.6l3 7.4M34 13l2.5 6" stroke="#081130" stroke-width="3" stroke-linecap="round"/><path d="M21 25v10l9-5z" fill="#fff" stroke="#081130" stroke-width="2.4" stroke-linejoin="round"/></svg>',
 pic:'<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="6" y="9" width="36" height="30" rx="5" fill="#fff" stroke="#081130" stroke-width="3"/><circle cx="17" cy="19" r="4" fill="#FFC531" stroke="#081130" stroke-width="2.4"/><path d="M8 35l10-10 7 6 6-8 9 10" fill="none" stroke="#3FA535" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 hour:'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 3h10M7 21h10M8 3v3a4 4 0 0 0 2 3.5L12 11l2-1.5A4 4 0 0 0 16 6V3M8 21v-3a4 4 0 0 1 2-3.5L12 13l2 1.5a4 4 0 0 1 2 3.5v3"/></svg>',
 lock:'<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4.5" y="10.5" width="15" height="10.5" rx="2.6" fill="#FFC531" stroke="#fff" stroke-width="1.6"/><path d="M8 10.5V7.8a4 4 0 018 0v2.7" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/><circle cx="12" cy="15.4" r="1.7" fill="#081130"/></svg>'
};
var hst=document.createElement('style');hst.id='sbx1112home';hst.textContent=[
'html body #sstudio.sb9 #sswl,html body #sstudio.sb9 #hpills,html body #sstudio.sb9 #ssgrbig,html body #sstudio.sb9 #ssms,html body #sstudio.sb9>.ssg{display:none!important}',
'#sb9{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;gap:10px;width:100%;max-width:560px;margin:0 auto}',
'#sb9 .r{flex:1 1 0;min-height:0;display:flex;gap:10px;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;scrollbar-width:none;-webkit-overflow-scrolling:touch;margin:0 -16px;padding:0 16px 7px;touch-action:pan-x}',
'#sb9 .r::-webkit-scrollbar{display:none}',
'#sb9 .t{position:relative;flex:0 0 calc((100% - 20px) / 3);min-width:0;scroll-snap-align:start;background:#fff;border:0;border-radius:20px;box-shadow:0 6px 0 var(--d,#c48a0c);padding:10px 8px 42px;display:flex;align-items:center;justify-content:center;cursor:pointer;font:inherit;-webkit-tap-highlight-color:transparent}',
'#sb9 .t:active{transform:translateY(5px);box-shadow:0 1px 0 var(--d,#c48a0c)}',
'#sb9 .t>img{max-width:100%;max-height:100%;object-fit:contain;display:block;pointer-events:none}',
'#sb9 .t .sbbd{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);width:62%;max-width:84px;pointer-events:none;filter:drop-shadow(0 2px 0 rgba(8,17,48,.14))}#sb9 .t .sbbd svg{display:block;width:100%;height:auto}',
'#sb9 .t .hg{position:absolute;right:7px;top:7px;width:26px;height:26px;border-radius:50%;background:#081130;display:flex;align-items:center;justify-content:center;pointer-events:none}#sb9 .t .hg svg{width:15px;height:15px}',
'#sb9 .b3,#sb9 .b2{flex:none;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;padding-bottom:6px}',
'#sb9 .bt{height:clamp(52px,7.4vh,66px);border:0;border-radius:20px;display:flex;align-items:center;justify-content:center;gap:10px;padding:0;cursor:pointer;font:inherit;-webkit-tap-highlight-color:transparent;background:var(--bg,#fff);box-shadow:0 6px 0 var(--sh,rgba(8,17,48,.16));color:#081130}',
'#sb9 .bt:active{transform:translateY(5px);box-shadow:0 1px 0 var(--sh,rgba(8,17,48,.16))}',
'#sb9 .bt svg{width:40px;height:40px;flex:none}',
'#sb9 .bt.gr{grid-column:span 2;--bg:#081130;--sh:#000;color:#fff}#sb9 .bt.gr svg{width:30px;height:30px}#sb9 .bt.gr b{font-weight:900;font-size:1.3rem}',
'@media (max-height:640px){#sb9 .t{padding-bottom:36px}#sb9 .t .sbbd{bottom:7px;width:54%}}',
'@media (min-width:700px){#sb9{max-width:720px}#sb9 .bt{height:76px}#sb9 .bt svg{width:50px;height:50px}#sb9 .bt.gr svg{width:36px;height:36px}#sb9 .bt.gr b{font-size:1.5rem}}'
].join('\n');document.body.appendChild(hst);
function proxy(id){return function(){var b=G(id);if(b)b.click()}}
function buildHome(){var s=G('sstudio'),head=G('sshead');if(!s||!head)return false;var wl=document.querySelectorAll('#sswl .wlrow');if(!wl.length)return false;
 covers();var box=G('sb9');if(!box){box=document.createElement('div');box.id='sb9';head.parentNode.insertBefore(box,head.nextSibling)}
 var h=[].map.call(wl,function(row){return'<div class="r">'+[].map.call(row.querySelectorAll('.wlcard[data-set]'),function(w){var id=w.getAttribute('data-set'),o=colById(id);if(!o)return'';
   return'<button class="t" data-set="'+esc(id)+'" style="--d:'+o.cat.d+'" aria-label="'+esc(w.getAttribute('aria-label')||o.c.n)+'"><img src="img/'+o.c.cv+'.webp" alt="" draggable="false"><span class="sbbd">'+BADGE[o.c.set]+'</span>'+(w.querySelector('.wlhg')?'<span class="hg">'+HIC.hour+'</span>':'')+'</button>'}).join('')+'</div>'}).join('');
 var gw=G('ssgrbig'),gwb=gw&&gw.querySelector('b'),word=gwb?gwb.textContent:'Grown-ups';
 h+='<div class="b3"><button class="bt" data-p="conttile" style="--bg:#ffe9a6;--sh:#d4b13a" aria-label="Keep going">'+HIC.play+'</button><button class="bt" data-p="showtile" style="--bg:#d6ebff;--sh:#3b7fc4" aria-label="Make a show">'+HIC.show+'</button><button class="bt" data-p="drawtile" style="--bg:#dff3d6;--sh:#6aa84f" aria-label="My drawings">'+HIC.pic+'</button></div>';
 h+='<div class="b2"><button class="bt" data-p="favtile" aria-label="Favourites">'+heart(true)+'</button><button class="bt gr" data-p="grtile" aria-label="'+esc(word)+'">'+HIC.lock+'<b>'+esc(word)+'</b></button></div>';
 box.innerHTML=h;
 [].forEach.call(box.querySelectorAll('.t'),function(b){b.onclick=function(){clickSet(b.getAttribute('data-set'))}});
 [].forEach.call(box.querySelectorAll('.bt'),function(b){b.onclick=proxy(b.getAttribute('data-p'))});
 s.classList.add('sb9');return true}
if(!buildHome()){var bh0=0,bht=setInterval(function(){if(buildHome()||++bh0>80)clearInterval(bht)},150)}

/* ================================================================ 8. pencil colouring: every coloured area gets a pencil grain
   (paper flecks showing through and darker strokes, all at one slant), like real colouring pencils. Outlines stay smooth.
   Same drawing data, so every drawing (old and new) gets it, in the steps, the cards, the thumbnails and Make it move pictures. */
(function(){if(typeof DX==='undefined'||!DX||!DX.paint||DX.__pencil)return;DX.__pencil=1;
 function grain(dark){var n=document.createElement('canvas');n.width=n.height=320;var g=n.getContext('2d'),ang=-0.62,i,dx,dy;
  for(i=0;i<(dark?1500:2600);i++){var x=Math.random()*320,y=Math.random()*320,l=4+Math.random()*12,a=ang+(Math.random()-.5)*.35;
   g.strokeStyle=dark?'rgba(0,0,0,'+(0.05+Math.random()*0.09)+')':'rgba(255,255,255,'+(0.25+Math.random()*0.5)+')';g.lineWidth=.6+Math.random()*1.1;
   for(dx=-320;dx<=320;dx+=320)for(dy=-320;dy<=320;dy+=320){g.beginPath();g.moveTo(x+dx,y+dy);g.lineTo(x+dx+Math.cos(a)*l,y+dy+Math.sin(a)*l);g.stroke()}}return n}
 var GL=grain(false),GD=grain(true),PC={},CC={},LC={};
 function pth(d){return PC[d]||(PC[d]=new Path2D(d))}
 function cutp(d){return CC[d]||(CC[d]=new Path2D('M-9999 -9999H9999V9999H-9999Z '+d))}
 function pe(d){if(!LC[d]){var e=document.createElementNS('http://www.w3.org/2000/svg','path');e.setAttribute('d',d);LC[d]={e:e,len:e.getTotalLength()}}return LC[d]}
 function pencil(g,x,y){g.save();g.translate(x,y);g.rotate(.55);g.lineJoin='round';g.lineWidth=.6;g.strokeStyle='#1b1f4b';g.setLineDash([]);g.fillStyle='#8a93a3';g.beginPath();g.moveTo(0,0);g.lineTo(-2,-5);g.lineTo(2,-5);g.closePath();g.fill();g.stroke();g.fillStyle='#d7dce4';g.beginPath();g.moveTo(-2,-5);g.lineTo(2,-5);g.lineTo(2,-18);g.quadraticCurveTo(2,-20,0,-20);g.quadraticCurveTo(-2,-20,-2,-18);g.closePath();g.fill();g.stroke();g.fillStyle='#1b1f4b';g.beginPath();g.moveTo(0,0);g.lineTo(-.7,-1.8);g.lineTo(.7,-1.8);g.closePath();g.fill();g.restore()}
 function texture(g,path,C,s){var pl=g.createPattern(GL,'repeat'),pd=g.createPattern(GD,'repeat');if(!pl||!pd)return;try{var M=new DOMMatrix().scale(1.2/s);pl.setTransform(M);pd.setTransform(M)}catch(e){}
  var a=g.globalAlpha;g.save();g.clip(path);g.globalCompositeOperation='multiply';g.fillStyle=pd;g.fillRect(-10,-10,C.w+20,C.h+20);g.globalCompositeOperation='source-over';g.globalAlpha=a*.85;g.fillStyle=pl;g.fillRect(-10,-10,C.w+20,C.h+20);g.restore()}
 var old=DX.paint;
 DX.paint=function(g,cw,ch,key,i,p,final){var PR=DX.get(key);if(!PR||PR.rx||!PR.steps)return old.apply(this,arguments);
  try{var C=PR.canvas;g.fillStyle='#fffef9';g.fillRect(0,0,cw,ch);
  var s=Math.min(cw,ch)*.94/C.w,ox=(cw-C.w*s)/2,oy=(ch-C.h*s)/2;g.save();g.translate(ox,oy);g.scale(s,s);var j,tip=null;
  for(j=0;j<=i;j++)PR.steps[j].add.forEach(function(it){if(!it.fill)return;g.globalAlpha=(j===i&&!final)?p:1;g.fillStyle=it.fill;g.save();
    if(it.cut)it.cut.forEach(function(c){g.clip(cutp(c),'evenodd')});g.fill(pth(it.d));texture(g,pth(it.d),C,s);g.restore();g.globalAlpha=1});
  g.lineCap='round';g.lineJoin='round';
  for(j=0;j<=i;j++){var cur=j===i&&!final,items=PR.steps[j].add,n=items.filter(function(a){return !a.fill}).length,k2=0;
   items.forEach(function(it){g.setLineDash([]);
    if(it.fill){if(cur){g.strokeStyle='#e63946';g.lineWidth=1.2;g.setLineDash([2.5,2]);g.stroke(pth(it.d));g.setLineDash([])}return}
    g.lineWidth=(it.w||1.4)*.6;
    if(final){g.strokeStyle='#2b2b2b';g.stroke(pth(it.d));return}
    if(!cur){g.strokeStyle='#6b7079';g.stroke(pth(it.d));return}
    var q=Math.max(0,Math.min(1,p*n-k2)),o=pe(it.d),L=o.len+1;k2++;if(q<=0)return;
    g.strokeStyle='#e63946';g.setLineDash([L,L]);g.lineDashOffset=L*(1-q);g.stroke(pth(it.d));
    if(q<1){var pt=o.e.getPointAtLength(o.len*q);tip=[pt.x,pt.y]}})}
  if(tip)pencil(g,tip[0],tip[1]);g.restore();g.setLineDash([])}catch(e){try{g.restore()}catch(x){}return old.apply(this,arguments)}}
 /* the card pictures were made before this loaded: make them again with the pencil look */
 try{if(typeof thumbURL==='function')projects('draw').forEach(function(p){if(p&&p.type==='draw'&&p.key&&DX.has(p.key)&&!DX.get(p.key).rx){var u=thumbURL(p);if(u)p.svg='<img src="'+u+'" alt="">'}})}catch(e){}})();

window.__sbx={open:open,state:function(){return ST},celebrate:celebrate,posterCanvas:posterCanvas,sheet:drawingSheet,openSheet:openSheet,findBox:findBox,cropBox:cropBox,goSet:goSet,mdGo:mdGo};
})();
