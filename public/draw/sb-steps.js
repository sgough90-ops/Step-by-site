/* 13 Nov 2026: Draw steps page.
   1. The finished picture sits in the top right of the drawing paper, so you can see what it will look like when it's done.
   2. No pencil tile under the drawing (left over from the other products; the colour on the screen already shows which pencil).
   3. The drawing's name sits at the top, between the buttons and the paper (for example "B is for Beetle"), and the paper moves down to make room.
   Loaded last, so these rules win. Other products are unchanged. */
(function(){
'use strict';
var G=function(i){return document.getElementById(i)};
var st=document.createElement('style');st.id='sbx1113steps';st.textContent=[
 'body.sbdraw #vw #vbs{display:none!important}',
 'body.sbdraw #vw #vpv{display:block!important;top:12px!important;right:12px!important;left:auto!important;width:clamp(84px,24vw,150px)!important;height:clamp(84px,24vw,150px)!important;background:#fff!important;border-radius:16px!important;border:1.5px solid #081130!important;box-shadow:0 2px 6px rgba(8,17,48,.15)!important;z-index:3}',
 '#vttl{display:none}',
 'body.sbdraw #vw #vttl{display:block;margin:2px 16px 6px;text-align:center;font-weight:800;font-size:clamp(1.25rem,5.6vw,1.9rem);line-height:1.15;color:#081130;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
].join('\n');
document.head.appendChild(st);
var tp=document.querySelector('#vw .tp'),t=document.createElement('div');t.id='vttl';
if(tp&&tp.parentNode)tp.parentNode.insertBefore(t,tp.nextSibling);
function isDraw(){try{return typeof V!=='undefined'&&V&&V.type==='draw'&&V.p}catch(e){return false}}
function name(){try{var k=V.p.key,d=(typeof REG!=='undefined'&&REG[k])||{};return V.p.t||V.p.title||d.title||V.p.name||d.name||''}catch(e){return ''}}
function after(){var d=isDraw();document.body.classList.toggle('sbdraw',!!d);if(!d)return;
 t.textContent=name();
 try{var pv=G('vpv');pv.style.display='block';paintFinal(pv,{type:'draw',key:V.p.key})}catch(e){}}
if(typeof renderV==='function'){var _r=renderV;renderV=function(){var r=_r.apply(this,arguments);after();return r}}
})();
