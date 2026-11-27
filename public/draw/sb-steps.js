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
/* 27 Nov 2026: a long name never ends in "...". Where there is room below it (the Chromebook's side column) it goes
   onto a second line; on a phone it gets a little smaller until it fits (never below 60%). */
function fit(){t.style.fontSize='';t.style.whiteSpace='';
 if(!t.clientWidth||t.scrollWidth<=t.clientWidth+1)return;
 var cs=getComputedStyle(t),f=parseFloat(cs.fontSize)||20,lh=parseFloat(cs.lineHeight)||f*1.15,m=f*.6;
 if(t.clientHeight>=lh*2.4){t.style.whiteSpace='normal';return}
 while(t.scrollWidth>t.clientWidth+1&&f>m){f-=.5;t.style.fontSize=f+'px'}}
function after(){var d=isDraw();document.body.classList.toggle('sbdraw',!!d);if(!d)return;
 t.textContent=name();fit();
 try{var pv=G('vpv');pv.style.display='block';paintFinal(pv,{type:'draw',key:V.p.key})}catch(e){}}
window.addEventListener('resize',function(){if(document.body.classList.contains('sbdraw'))fit()});
/* 27 Nov 2026: no part of the drawing hides under the small finished picture (top right) or the step number (top left).
   On shorter screens (an iPhone with Safari's bars showing, small phones, a phone on its side, an iPad) the picture box
   covered the top of some drawings, for example all of the kangaroo's ears in step 5. Now, if any line or colour of the
   finished drawing would sit under either box, the drawing moves down (or left) and, only if it still has to, gets a
   little smaller. A drawing that is clear of both boxes is painted exactly as before. Every step of a drawing uses the
   same place, so nothing jumps between steps. */
var _dp=DX&&DX.paint,INK={},PLACE={};
function inkOf(key){if(INK[key])return INK[key];var PR=DX.get(key),R=160,c=document.createElement('canvas');c.width=c.height=R;
 var g=c.getContext('2d');_dp(g,R,R,key,DX.n(key)-1,1,true);var d=g.getImageData(0,0,R,R).data,s=R*.94/PR.canvas.w,o=(R-PR.canvas.w*s)/2,pts=[],b=[1e9,1e9,-1e9,-1e9];
 for(var y=0;y<R;y++)for(var x=0;x<R;x++){var i=(y*R+x)*4;if(Math.abs(d[i]-255)+Math.abs(d[i+1]-254)+Math.abs(d[i+2]-249)>60){var X=(x+.5-o)/s,Y=(y+.5-o)/s;pts.push(X,Y);if(X<b[0])b[0]=X;if(Y<b[1])b[1]=Y;if(X>b[2])b[2]=X;if(Y>b[3])b[3]=Y}}
 return INK[key]={p:pts,b:b,w:PR.canvas.w}}
function boxIn(id,A){var e=G(id);if(!e||e.offsetParent===null)return null;var B=e.getBoundingClientRect();if(!B.width)return null;return[B.left-A.left-4,B.top-A.top-4,B.right-A.left+4,B.bottom-A.top+4]}
function placeFor(key,cw,ch,boxes){var I=inkOf(key),P=I.p,W=I.w,s0=Math.min(cw,ch)*.94/W;
 function clear(s,ox,oy){if(ox+I.b[0]*s<1||oy+I.b[1]*s<1||ox+I.b[2]*s>cw-1||oy+I.b[3]*s>ch-1)return false;
  for(var k=0;k<P.length;k+=2){var x=ox+P[k]*s,y=oy+P[k+1]*s;for(var j=0;j<boxes.length;j++){var q=boxes[j];if(x>q[0]&&x<q[2]&&y>q[1]&&y<q[3])return false}}return true}
 var cx=(cw-W*s0)/2,cy=(ch-W*s0)/2;if(clear(s0,cx,cy))return null;
 for(var f=1;f>=.6;f-=.02){var s=s0*f,ox0=(cw-W*s)/2,oy0=(ch-W*s)/2,dyM=Math.max(0,ch-1-I.b[3]*s-oy0),dxM=Math.max(0,ox0+I.b[0]*s-1),best=null;
  for(var a=0;a<=8;a++)for(var c=0;c<=8;c++){var dy=dyM*a/8,dx=dxM*c/8;if(best&&dy+dx>=best[3])continue;if(clear(s,ox0-dx,oy0+dy))best=[s,ox0-dx,oy0+dy,dy+dx]}
  if(best)return best}
 return null}
if(_dp)DX.paint=function(g,cw,ch,key,i,p,final){
 try{var cv=g&&g.canvas;if(cv&&cv.id==='vcv'&&document.body.classList.contains('sbdraw')&&DX.has(key)){var PR=DX.get(key);
  if(PR&&PR.steps&&!PR.rx){var A=cv.getBoundingClientRect(),bx=[boxIn('vpv',A),boxIn('vnum',A)].filter(Boolean);
   if(bx.length){var ck=key+'|'+Math.round(cw)+'x'+Math.round(ch)+'|'+bx.map(function(q){return q.map(Math.round).join(',')}).join(';');
    if(!(ck in PLACE))PLACE[ck]=placeFor(key,cw,ch,bx);var L=PLACE[ck];
    if(L){var vs=L[0]*PR.canvas.w/.94,o=(vs-PR.canvas.w*L[0])/2;g.save();g.fillStyle='#fffef9';g.fillRect(0,0,cw,ch);g.translate(L[1]-o,L[2]-o);
     try{return _dp.call(this,g,vs,vs,key,i,p,final)}finally{g.restore()}}}}}}catch(e){}
 return _dp.apply(this,arguments)};
if(typeof renderV==='function'){var _r=renderV;renderV=function(){var r=_r.apply(this,arguments);after();return r}}
})();
