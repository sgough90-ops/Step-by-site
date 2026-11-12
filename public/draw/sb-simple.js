/* 12 Nov 2026 (afternoon): a simpler Step by Draw.
   1. Pencil-coloured backgrounds. The cream, yellow and light blue pages look coloured in with a pencil and keep the same colours.
      Only the page background changes: the drawing paper on the steps, the white cards and the buttons stay plain.
   2. No play screen. Tapping a drawing in a set goes straight to step 1, and Back on the steps goes back to the set.
      The set page already shows a tick on a drawing once a photo of it is saved.
   3. No Favourites. No heart, no Favourites button on the home screen (Grown-ups is full width instead).
   Loaded after sb-extras.js, so these rules come last and win. Photos and everything else stay on this device. */
(function(){
'use strict';
var G=function(i){return document.getElementById(i)};
function has(fn){try{return typeof window[fn]==='function'}catch(e){return false}}

/* ================================================================ 1. pencil backgrounds
   Small tiles that repeat (img/pencil-cream.webp, img/pencil-yellow.webp, img/pencil-blue.webp), each made to average out to
   the page's own colour (cream #fff6e0, the Draw yellow #fee8af, the show maker's light blue #e3f1ff).
   Only the picture is added: each page keeps its own colour underneath. */
function bg(url){return 'background-image:url('+url+')!important;background-size:512px 512px!important;background-repeat:repeat!important;background-position:0 0!important'}
var CREAM=['#ach','#mydraw','#mdcrop','#fav','#cont','#holo','#grown'].map(function(i){return 'html:root body #app>'+i}).join(',');
var YEL=['#proj','#vw','#dn','#mt'].map(function(i){return 'html:root body.pcy #app>'+i}).join(',');
var st=document.createElement('style');st.id='sbx1112simple';st.textContent=[
 'html:root body{'+bg('img/pencil-cream.webp')+'}',
 CREAM+'{'+bg('img/pencil-cream.webp')+'}',
 YEL+'{'+bg('img/pencil-yellow.webp')+'}',
 'html:root body .scr.shs.pcb{'+bg('img/pencil-blue.webp')+'}',
/* ================================================================ 3. no Favourites */
 'html body #sb9 .bt[data-p="favtile"],html body #hpills #favtile{display:none!important}',
 'html body #sb9 .bt.gr[data-p="grtile"]{grid-column:1/-1!important}',
 '.pvc .th .pvhb,#pgrid .card .hb,#tabs .tab[data-t="fav"]{display:none!important}'
].join('\n');
document.body.appendChild(st);

/* the yellow tile only goes on when the set, steps and finish pages are Draw yellow, so any other colour stays as it is */
function syncY(){try{var pj=G('proj');document.body.classList.toggle('pcy',!!pj&&getComputedStyle(pj).backgroundColor==='rgb(254, 232, 175)')}catch(e){}}
syncY();
try{var pj0=G('proj');if(pj0&&window.MutationObserver)new MutationObserver(syncY).observe(pj0,{attributes:true,attributeFilter:['style','class']})}catch(e){}
if(has('showOnly')){var _so=window.showOnly;window.showOnly=function(){var r=_so.apply(this,arguments);syncY();return r}}
/* the show maker's pages are made as they open; only its light blue ones get the blue tile (the dark play screen stays dark) */
function syncB(){[].forEach.call(document.querySelectorAll('.scr.shs'),function(e){var c='';try{c=getComputedStyle(e).backgroundColor}catch(x){}e.classList.toggle('pcb',c==='rgb(227, 241, 255)')})}
var BQ=0;function soonB(){if(BQ)return;BQ=1;requestAnimationFrame(function(){BQ=0;syncB()})}
syncB();
try{var ap=G('app')||document.body;if(window.MutationObserver)new MutationObserver(soonB).observe(ap,{childList:true})}catch(e){}
/* the show maker adds its pages and styles a moment after a tap, so look again a few times */
document.addEventListener('click',function(){[0,150,500,1200].forEach(function(t){setTimeout(soonB,t)})},true);

/* ================================================================ 2. no play screen */
var BACK=false;
function isDraw(p){try{return !!(p&&p.key&&(p.type==='draw'||(typeof REG!=='undefined'&&REG[p.key]&&REG[p.key].type==='draw')))}catch(e){return false}}
/* the same as pressing play on the old card: open the drawing, then start at step 1 */
function startSteps(p){var pv=G('pv');if(pv)pv.classList.add('hide');openMat(p);var mt=G('mt'),b=G('mtgo');if(mt&&b&&!mt.classList.contains('hide'))b.click();syncY()}
if(has('openPv')){var _op=window.openPv;window.openPv=function(p){
 /* Back on the steps returns to the set, which used to reopen the card: now it just stays on the set */
 if(BACK){BACK=false;var pv=G('pv');if(pv)pv.classList.add('hide');return}
 if(isDraw(p)){startSteps(p);return}
 return _op.apply(this,arguments)}}
/* mark a Back press on the steps (tap, click or Escape) before its own handler runs */
document.addEventListener('click',function(e){var t=e.target;if(t&&t.closest&&t.closest('#vback')){BACK=true;setTimeout(function(){BACK=false},0)}},true);
})();
