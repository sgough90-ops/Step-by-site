/* 31 Oct 2026: Make it move v2 moved onto step-by.com (it was built in the app on 24 Oct but never reached the site).
   Added today: MIM.live (living characters: a make keeps its own parts moving wherever the Show draws it),
   MIM.prep (split a photo into parts before a show starts, so slow Chromebooks don't stutter) and the tickle
   reaction (window.__pokeRx) for Silly and Cool. Nothing here uploads anything. */
/* 24 Oct 2026: Make it move v2 — every drawing is split into its real parts.
   Each Draw project has an animation plan (MIM.plans[key], or "anim" inside the project data) made from a detailed review of
   the picture: which lines and colours belong to which part, which parts stay still (the parrot's branch), which part is the
   star (the parrot) and how each part moves (wings flap, wheels turn, eyes blink, tails wag).
   Everything is worked out from the time, so a replay looks the same. Colours never change faster than twice a second. */
(function(){
"use strict";
var MIM=window.MIM||(window.MIM={});MIM.plans=MIM.plans||{};
var CACHE={};
MIM.reg=function(k,p){MIM.plans[k]=p;delete CACHE[k]};
var DEG=Math.PI/180,TAU=Math.PI*2;
function hsh(i,k){var v=Math.sin(i*12.9898+(k||0)*78.233)*43758.5453;return v-Math.floor(v)}
function cl(x){return x<0?0:x>1?1:x}
function e3(x){x=cl(x);return 1-Math.pow(1-x,3)}
function ei3(x){x=cl(x);return x*x*x}
function eio(x){x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}
function L(a,b,u){return a+(b-a)*u}
function seg(t,a,b){return cl((t-a)/(b-a))}
function win(t,a,b){return t>=a&&t<b}
function bump(t,a,b){return Math.sin(seg(t,a,b)*Math.PI)}
function noise(x){return(Math.sin(x*1.7)+Math.sin(x*2.9+1.3)*.6+Math.sin(x*5.3+.7)*.3)/1.9}

/* ---------- paths ---------- */
var PC={},CC={};
function pth(d){return PC[d]||(PC[d]=new Path2D(d))}
function cutp(d){return CC[d]||(CC[d]=new Path2D("M-9999 -9999H9999V9999H-9999Z "+d))}
function fillIt(g,it,col){g.fillStyle=col||it.fill;if(it.cut&&it.cut.length){g.save();it.cut.forEach(function(c){g.clip(cutp(c),"evenodd")});g.fill(pth(it.d));g.restore()}else g.fill(pth(it.d))}
function lineIt(g,it){g.lineWidth=(it.w||1.4)*.6;g.stroke(pth(it.d))}

/* ---------- plan to model ---------- */
function planOf(key){var o=null;try{o=DX.get(key)}catch(e){}return(o&&o.anim)||MIM.plans[key]||null}
function refs(list,P){var out=[];if(!list||list==="rest")return out;(Array.isArray(list)?list:[list]).forEach(function(r){var m=String(r).trim().match(/^(\d+)\.(\*|\d+)(?:-(\d+))?$/);if(!m)return;var s=+m[1],st=P.steps[s];if(!st)return;
 if(m[2]==="*")st.add.forEach(function(_,i){out.push(s+"."+i)});else{var a=+m[2],b=m[3]!=null?+m[3]:a;for(var i=a;i<=b;i++)if(st.add[i])out.push(s+"."+i)}});return out}
function bboxDraw(fn){var c=document.createElement("canvas");c.width=c.height=240;var g=c.getContext("2d");g.setTransform(2,0,0,2,20,20);g.fillStyle="#000";g.strokeStyle="#000";g.lineCap="round";g.lineJoin="round";fn(g);
 var d=g.getImageData(0,0,240,240).data,x0=999,y0=999,x1=-1,y1=-1;for(var y=0;y<240;y+=2)for(var x=0;x<240;x+=2)if(d[(y*240+x)*4+3]>16){if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y}
 if(x1<0)return null;return{x:(x0-20)/2,y:(y0-20)/2,w:(x1-x0+2)/2,h:(y1-y0+2)/2}}
function unionBB(list){var b=null;list.forEach(function(q){if(!q)return;if(!b){b={x:q.x,y:q.y,w:q.w,h:q.h};return}var x1=Math.max(b.x+b.w,q.x+q.w),y1=Math.max(b.y+b.h,q.y+q.h);b.x=Math.min(b.x,q.x);b.y=Math.min(b.y,q.y);b.w=x1-b.x;b.h=y1-b.y});return b||{x:0,y:0,w:100,h:100}}
function model(key){if(CACHE[key])return CACHE[key];var P=null,plan=planOf(key);try{P=DX.get(key)}catch(e){}if(!P||!plan||!plan.parts||!plan.parts.length)return null;
 var parts=[],by={},owner={},dups=[],bad=[],rest=null;
 plan.parts.forEach(function(sp){var pt={id:sp.id,role:sp.role||(sp.parent?"part":"still"),parent:sp.parent||null,pivot:sp.pivot||null,motion:sp.motion||[],behind:!!sp.behind,under:sp.under||null,react:sp.react||null,
   fills:[],lines:[],pf:[],pl:[],uf:[],kids:[],sp:sp};parts.push(pt);by[pt.id]=pt;if(sp.items==="rest")rest=pt});
 plan.parts.forEach(function(sp){if(sp.items==="rest")return;var r=refs(sp.items,P);(sp.items==null?[]:Array.isArray(sp.items)?sp.items:[sp.items]).forEach(function(x){if(!/^(\d+)\.(\*|\d+)(?:-(\d+))?$/.test(String(x).trim()))bad.push(sp.id+":"+x)});
  r.forEach(function(k){if(owner[k])dups.push(k);owner[k]=sp.id})});
 if(plan.raster)plan.parts.forEach(function(sp){if(!sp.region)return;var pt=by[sp.id];[].concat(sp.region).forEach(function(d){pt.fills.push({d:d,fill:"#000",region:1})})});
 var hero=parts.filter(function(p){return p.role==="hero"})[0]||null;
 P.steps.forEach(function(st,s){st.add.forEach(function(it,i){var k=s+"."+i,id=owner[k]||(rest?rest.id:hero?hero.id:parts[0].id),pt=by[id];(it.fill?pt.fills:pt.lines).push(it)})});
 (plan.patches||[]).forEach(function(pa){var pt=by[pa.part];if(!pt)return;(pa.fill?pt.pf:pt.pl).push(pa)});
 parts.forEach(function(pt){if(pt.parent&&by[pt.parent])by[pt.parent].kids.push(pt)});
 parts.forEach(function(pt){if(!pt.under||!pt.parent||!by[pt.parent])return;var par=by[pt.parent],col=typeof pt.under==="string"?pt.under:pt.under.color,clip=null;
  if(typeof pt.under==="object"&&pt.under.clip==="parent"){clip=new Path2D();par.fills.forEach(function(f){clip.addPath(pth(f.d))})}
  pt.fills.forEach(function(f){par.uf.push({d:f.d,cut:null,fill:col,from:pt.id,clip:clip})})});
 parts.forEach(function(pt){pt.bb=bboxDraw(function(g){pt.fills.forEach(function(f){fillIt(g,f,"#000")});pt.lines.forEach(function(l){lineIt(g,l)})});if(!pt.bb)pt.bb={x:50,y:50,w:0,h:0}});
 var M={raster:!!plan.raster,key:key,P:P,plan:plan,parts:parts,by:by,hero:hero,roots:parts.filter(function(p){return!p.parent||!by[p.parent]}),dups:dups,bad:bad,points:plan.points||{},kind:plan.kind||"walk",opt:plan.opt||{}};
 M.bb=unionBB(parts.map(function(p){return p.bb}));M.hb=hero?unionBB(desc(hero).map(function(p){return p.bb})):M.bb;
 CACHE[key]=M;return M}
function desc(pt){var out=[pt];pt.kids.forEach(function(k){out=out.concat(desc(k))});return out}

/* ---------- matrices ---------- */
function mul(A,B){return[A[0]*B[0]+A[2]*B[1],A[1]*B[0]+A[3]*B[1],A[0]*B[2]+A[2]*B[3],A[1]*B[2]+A[3]*B[3],A[0]*B[4]+A[2]*B[5]+A[4],A[1]*B[4]+A[3]*B[5]+A[5]]}
function about(px,py,o){/* T(p+t) R K S T(-p) */var c=Math.cos(o.r),s=Math.sin(o.r);var R=[c,s,-s,c,0,0];var K=[1,Math.tan(o.ky||0),Math.tan(o.kx||0),1,0,0];var S=[o.sx,0,0,o.sy,0,0];
 var m=mul([1,0,0,1,px+(o.tx||0),py+(o.ty||0)],mul(R,mul(K,mul(S,[1,0,0,1,-px,-py]))));return m}
function same(A,B){for(var i=0;i<4;i++)if(Math.abs(A[i]-B[i])>1e-4)return false;return Math.abs(A[4]-B[4])<.02&&Math.abs(A[5]-B[5])<.02}
var ID=[1,0,0,1,0,0];

/* ---------- part motions ---------- */
var DRIVE={flap:"flap",step:"walk",speak:"speak",chomp:"speak"};
var ZERO={flap:1,walk:1,speak:1,burn:1,flame:1,dig:1,tilt:1,chomp:1,beam:1,lift:1,glow:1,rustle:1,door:1,look:1,eyesShut:1,swim:0};
function blinkAt(t,every,ph,forced){var w=.16;if(forced)for(var i=0;i<forced.length;i++){var f0=forced[i]+(ph||0)*.3;if(t>=f0&&t<f0+w)return Math.sin((t-f0)/w*Math.PI)}
 var e=every||2.7,u=((t+ph*e)%e+e)%e;return u<w?Math.sin(u/w*Math.PI):0}
/* 31 Oct 2026: living mode (MIM.live) keeps only repeating motions; drivers it does not set stay at rest,
   except wind (plants sway) and swim (fins wag) */
var LIVEM={flap:1,wag:1,sway:1,step:1,swing:1,bob:1,spin:1,blink:1,pulse:1,flicker:1,flutter:1,speak:1,chomp:1,twinkle:1,extend:1,tilt:1,pose:1},LIVE1={wind:1,swim:1};
function liveOK(m){if(m.mode||m.from!=null||m.to!=null)return false;if(m.type==="glow")return!!m.always;return!!LIVEM[m.type]}
function motions(pt,C){var o={r:0,sx:1,sy:1,kx:0,ky:0,tx:0,ty:0,a:1,glow:0,gcol:null};var t=C.t;if(C.still)return o;
 pt.motion.forEach(function(m){if(C.live&&!liveOK(m))return;if(m.mode&&m.mode!==C.mode)return;if(m.from!=null&&t<m.from)return;if(m.to!=null&&t>m.to&&!(m.type==="open"&&(m.axis==="x"||m.axis==="y")))return;
  var f=m.freq||1,ph=(m.phase||0)*TAU,amp=m.amp!=null?m.amp:0,dn=m.drive||DRIVE[m.type]||null,drv=dn?(C.D[dn]!=null?C.D[dn]:(C.live?(LIVE1[dn]?1:0):(ZERO[dn]?0:1))):1,s,u,w;
  if(m.always)drv=Math.max(drv,1);
  switch(m.type){
   case"flap":w=.5-.5*Math.cos(TAU*f*t*(C.D.flapRate||1)+ph);if(m.axis==="x")o.sx*=1-(1-(m.min!=null?m.min:.25))*w*cl(drv);else if(m.axis==="y")o.sy*=1-(1-(m.min!=null?m.min:.3))*w*cl(drv);else o.r+=(amp||40)*DEG*w*Math.min(1.4,drv)*(m.dir||1);break;
   case"wag":case"sway":case"step":o.r+=(amp||10)*DEG*Math.sin(TAU*f*t*(m.type==="wag"?(C.D.wagRate||1):1)+ph)*drv*(m.dir||1);break;
   case"swing":o.r+=(amp||10)*DEG*Math.sin(TAU*f*t+ph)*drv*(m.dir||1);break;
   case"bob":u=(amp||1.5)*Math.sin(TAU*f*t+ph)*drv;if(m.axis==="x")o.tx+=u;else o.ty+=u;break;
   case"spin":if(m.roll)o.r+=(C.dist/(m.radius||5))*(m.dir||1);else o.r+=TAU*(m.speed||.5)*(m.drive==="spin"&&C.D.spinT!=null?C.D.spinT:t)*(m.dir||1);break;
   case"blink":u=blinkAt(t,m.every,m.phase||0,C.blinks);if(C.D.eyesShut)u=Math.max(u,C.D.eyesShut);o.sy*=1-.88*u;break;
   case"pulse":s=1+(amp||.06)*Math.sin(TAU*f*t+ph)*drv;o.sx*=s;o.sy*=s;break;
   case"flicker":u=noise(t*(f||6)*2+ph*3);o.sy*=1+(amp||.18)*u*drv;o.sx*=1-(amp||.18)*.35*u*drv;break;
   case"flutter":o.ky+=(amp||8)*DEG*Math.sin(TAU*f*t+ph)*drv;o.sx*=1+(amp||8)*.004*Math.sin(TAU*f*t*1.3+ph)*drv;break;
   case"speak":case"chomp":u=cl(drv);if(m.type==="chomp")u=Math.max(u,C.D.chomp||0);if(m.axis==="y")o.sy*=1+(amp||.3)*u;else if(m.axis==="ty")o.ty+=(amp||2)*u;else o.r+=(amp||14)*DEG*u*(m.dir||1);break;
   case"open":u=m.drive?cl(drv):e3(seg(t,m.at||0,(m.at||0)+(m.dur||.6)));if(m.back!=null&&!m.drive)u*=1-e3(seg(t,m.back,m.back+(m.dur||.6)));if(m.axis==="x")o.sx*=1-(1-(m.to!=null?m.to:.15))*u;else if(m.axis==="y")o.sy*=1-(1-(m.to!=null?m.to:.15))*u;else if(m.axis==="ty")o.ty+=(amp||-4)*u;else o.r+=(amp||60)*DEG*u*(m.dir||1);break;
   case"extend":w=dn?cl(drv):(.5-.5*Math.cos(TAU*f*t+ph));s=1+(amp||.25)*w;if(m.axis==="y")o.sy*=s;else o.sx*=s;break;
   case"twinkle":s=.75+.4*(.5+.5*Math.sin(TAU*(f||.8)*t+ph));o.sx*=s;o.sy*=s;o.a*=.55+.45*(.5+.5*Math.sin(TAU*(f||.8)*t+ph));break;
   case"drift":u=m.pingpong?(function(x){x=x%2;return x<1?eio(x):eio(2-x)})(t/(m.dur||3.8)+(m.phase||0)*2):(m.loop?((t/(m.dur||7.6))+(m.phase||0))%1:cl(t/(m.dur||7.6)));u*=(m.drive?drv:1);o.tx+=(m.dx||0)*u;o.ty+=(m.dy||0)*u;break;
   case"lift":u=e3(seg(t,m.at||2,(m.at||2)+(m.dur||2)));o.ty-=(m.dy||20)*u;s=1-(m.shrink!=null?m.shrink:.3)*u;o.sx*=s;o.sy*=s;if(m.fade)o.a*=1-u;break;
   case"sink":u=eio(seg(t,m.at||0,(m.at||0)+(m.dur||7)));o.ty+=(m.dy||10)*u;break;
   case"shake":o.tx+=(amp||.6)*Math.sin(t*(f||30)*TAU*.5)*drv;o.ty+=(amp||.6)*.6*Math.cos(t*(f||30)*TAU*.37)*drv;break;
   case"glow":u=m.at!=null?e3(seg(t,m.at,m.at+(m.dur||1))):(C.D.glow!=null?C.D.glow:(m.always?1:0));if(m.at!=null&&m.mode==null&&C.D.glowOff)u=0;if(m.pulse)u*=.6+.4*(.5+.5*Math.sin(TAU*(m.pulse)*t+ph));o.glow=Math.max(o.glow,u*(amp||.8));o.gcol=m.color||"#ffe066";break;
   case"hide":u=seg(t,m.at||0,(m.at||0)+(m.dur||.3));o.a*=1-u;break;
   case"show":u=seg(t,m.at||0,(m.at||0)+(m.dur||.3));o.a*=u;break;
   case"pose":u=drv;if(m.axis==="x")o.sx*=1+(amp||.2)*u;else if(m.axis==="y")o.sy*=1+(amp||.2)*u;else if(m.axis==="tx")o.tx+=(amp||3)*u;else if(m.axis==="ty")o.ty+=(amp||3)*u;else o.r+=(amp||20)*DEG*u*(m.dir||1);break;
   case"nod":o.r+=(amp||8)*DEG*Math.sin(TAU*f*t+ph)*(C.D.nod!=null?C.D.nod:1);break;
   case"tilt":o.r+=(amp||20)*DEG*cl(m.drive?drv:(C.D.tilt||0))*(m.dir||1);break;
   case"look":o.r+=(amp||10)*DEG*(C.D.look||0);break;
  }});
 return o}

/* ---------- drawing a frame of parts ---------- */
var LINE="#2b2b2b";
function painter(M,C){/* list of {pt,m,a,glow} back to front */var out=[];
 function visit(pt,parentM,pa){var o=motions(pt,C);var piv=pt.pivot||[pt.bb.x+pt.bb.w/2,pt.bb.y+pt.bb.h/2];var m=mul(parentM,about(piv[0],piv[1],o)),a=o.a;/* a part fading does not fade its children (plans use this to hide just an outline) */
  pt.kids.filter(function(k){return k.behind}).forEach(function(k){visit(k,m,a)});
  out.push({pt:pt,m:m,a:a,glow:o.glow,gcol:o.gcol});
  pt.kids.filter(function(k){return!k.behind}).forEach(function(k){visit(k,m,a)})}
 M.roots.forEach(function(r){var base=r.role==="hero"?C.HM:(C.react&&C.react[r.id]?C.react[r.id]:ID);visit(r,base,r.role==="hero"&&C.heroA!=null?C.heroA:1)});
 return out}
function drawFrame(g,M,C,B,list){/* B: base matrix units->px */list=list||painter(M,C);var groups=[],MT={};
 list.forEach(function(e){MT[e.pt.id]=e});
 function moved(by,id){var a=MT[by],b=MT[id];if(!a)return true;if(!b)return true;return a.a<.999||!same(a.m,b.m)}
 list.forEach(function(e){var last=groups[groups.length-1];if(last&&same(last.m,e.m)&&e.a>=.999&&last.a>=.999&&!e.glow&&!last.glow)last.items.push(e);else groups.push({m:e.m,a:e.a,glow:e.glow,gcol:e.gcol,items:[e]})});
 groups.forEach(function(G){
  g.save();var T=mul(B,G.m);g.setTransform(T[0]*C.dpr,T[1]*C.dpr,T[2]*C.dpr,T[3]*C.dpr,T[4]*C.dpr,T[5]*C.dpr);g.globalAlpha=G.a*(C.alpha==null?1:C.alpha);
  G.items.forEach(function(e){var pt=e.pt;
   if(pt.img){(pt.pimgs||[]).forEach(function(pi){if(pi.always||moved(pi.by,pt.id))g.drawImage(pi.img,pt.ix,pt.iy,pt.iw,pt.ih)});g.drawImage(pt.img,pt.ix,pt.iy,pt.iw,pt.ih);return}
   pt.uf.forEach(function(u){if(!moved(u.from,pt.id))return;if(u.clip){g.save();g.clip(u.clip);fillIt(g,u);g.restore()}else fillIt(g,u)});
   pt.pf.forEach(function(p){var by=p.by||(M.hero&&M.hero.id);if(moved(by,pt.id))fillIt(g,p)});
   pt.fills.forEach(function(f){fillIt(g,f)})});
  g.strokeStyle=LINE;g.lineCap="round";g.lineJoin="round";
  G.items.forEach(function(e){var pt=e.pt;if(pt.img)return;pt.pl.forEach(function(p){var by=p.by||(M.hero&&M.hero.id);if(moved(by,pt.id))lineIt(g,p)});pt.lines.forEach(function(l){lineIt(g,l)})});
  if(G.glow>0&&!C.glowLater){g.globalCompositeOperation="lighter";g.globalAlpha=G.glow*.55;G.items.forEach(function(e){e.pt.fills.forEach(function(f){fillIt(g,f,G.gcol)})});g.globalCompositeOperation="source-over"}
  g.restore()})}


/* ---------- 31 Oct 2026: the same picture as drawFrame, made from pictures of each part ----------
   drawFrame draws every shape of every part each frame (about a hundred shapes), which is slow on budget Chromebooks.
   drawFrameR draws the same thing from pictures of each part made once: within each group, fills first, then lines,
   exactly like drawFrame, so the result matches it. Each group of parts that share one position is then kept as a
   single picture, so a frame is a handful of image draws. Used in Silly, Cool and living mode, for clean drawings and photos. */
function rasterOf(M,R){var rc=M.rc;if(rc&&(rc.R>=R||rc.photo))return rc;
 if(M.parts[0]&&M.parts[0].img){/* a child's photo split into parts: the parts are pictures already */var p0=M.parts[0];rc={R:p0.img.width/p0.iw,photo:true,parts:{}};
  M.parts.forEach(function(pt){var P={x:pt.ix,y:pt.iy,w:pt.iw,h:pt.ih,fill:pt.img,line:null,uf:{},pf:{},pl:{}};(pt.pimgs||[]).forEach(function(pi){var k=pi.always?"\u0000always":pi.by;(P.pf[k]||(P.pf[k]=[])).push(pi.img)});rc.parts[pt.id]=P});
  M.rc=rc;return rc}
 rc={R:R,parts:{}};
 M.parts.forEach(function(pt){
  function heroId(p){return p.by||(M.hero&&M.hero.id)}
  var bb=bboxDraw(function(g){pt.fills.forEach(function(f){fillIt(g,f,"#000")});pt.uf.forEach(function(u){fillIt(g,u,"#000")});pt.pf.forEach(function(p){fillIt(g,p,"#000")});g.lineWidth=2.5;pt.lines.forEach(function(l){g.stroke(pth(l.d))});pt.pl.forEach(function(l){g.stroke(pth(l.d))})});
  if(!bb)return;var x0=bb.x-2,y0=bb.y-2,w=bb.w+4,h=bb.h+4,cw=Math.max(1,Math.ceil(w*R)),ch=Math.max(1,Math.ceil(h*R));
  function img(fn){var c=document.createElement("canvas");c.width=cw;c.height=ch;var g=c.getContext("2d");g.setTransform(R,0,0,R,-x0*R,-y0*R);g.strokeStyle=LINE;g.lineCap="round";g.lineJoin="round";fn(g);return c}
  var P={x:x0,y:y0,w:cw/R,h:ch/R,fill:null,line:null,uf:{},pf:{},pl:{}},grp={};
  if(pt.fills.length)P.fill=img(function(g){pt.fills.forEach(function(f){fillIt(g,f)})});
  if(pt.lines.length)P.line=img(function(g){pt.lines.forEach(function(l){lineIt(g,l)})});
  pt.uf.forEach(function(u){(grp["u"+u.from]||(grp["u"+u.from]=[])).push(u)});
  pt.pf.forEach(function(p){var k="f"+heroId(p);(grp[k]||(grp[k]=[])).push(p)});
  pt.pl.forEach(function(p){var k="l"+heroId(p);(grp[k]||(grp[k]=[])).push(p)});
  Object.keys(grp).forEach(function(k){var list=grp[k],t=k[0],by=k.slice(1);
   var c=img(function(g){list.forEach(function(u){if(t==="l"){lineIt(g,u);return}if(u.clip){g.save();g.clip(u.clip);fillIt(g,u);g.restore()}else fillIt(g,u)})});
   (t==="u"?P.uf:t==="f"?P.pf:P.pl)[by]=c});
  rc.parts[pt.id]=P});
 M.rc=rc;return rc}
function drawFrameR(g,M,C,B,list){var sc=Math.sqrt(Math.abs(B[0]*B[3]-B[1]*B[2]))*(C.dpr||1),R=Math.max(2,Math.min(8,Math.ceil(sc*1.6))),rc=M.rc&&M.rc.R>=Math.min(8,R)?M.rc:rasterOf(M,R);
 list=list||painter(M,C);var groups=[],MT={};list.forEach(function(e){MT[e.pt.id]=e});
 function moved(by,id){var a=MT[by],b=MT[id];if(!a)return true;if(!b)return true;return a.a<.999||!same(a.m,b.m)}
 list.forEach(function(e){var last=groups[groups.length-1];if(last&&same(last.m,e.m)&&e.a>=.999&&last.a>=.999&&!e.glow&&!last.glow)last.items.push(e);else groups.push({m:e.m,a:e.a,glow:e.glow,gcol:e.gcol,items:[e]})});
 /* each group (parts sharing one position) becomes one picture, kept for next time: one image draw per group per frame */
 var GC=M.gc&&M.gc.R===rc.R?M.gc:(M.gc={R:rc.R,n:0,e:{}});
 groups.forEach(function(G){var key="",mem=[];
  G.items.forEach(function(e){var P=rc.parts[e.pt.id];if(!P)return;var f={uf:{},pf:{},pl:{}},k;key+=e.pt.id+":";
   for(k in P.uf){f.uf[k]=moved(k,e.pt.id);key+=f.uf[k]?1:0}for(k in P.pf){f.pf[k]=k==="\u0000always"||moved(k,e.pt.id);key+=f.pf[k]?1:0}for(k in P.pl){f.pl[k]=moved(k,e.pt.id);key+=f.pl[k]?1:0}key+="|";mem.push({P:P,f:f})});
  if(!mem.length)return;var ent=GC.e[key];
  if(!ent){var x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;mem.forEach(function(q){x0=Math.min(x0,q.P.x);y0=Math.min(y0,q.P.y);x1=Math.max(x1,q.P.x+q.P.w);y1=Math.max(y1,q.P.y+q.P.h)});
   var R=rc.R,cv=document.createElement("canvas");cv.width=Math.max(1,Math.ceil((x1-x0)*R));cv.height=Math.max(1,Math.ceil((y1-y0)*R));var q2=cv.getContext("2d");q2.setTransform(R,0,0,R,-x0*R,-y0*R);
   function di(v,P){[].concat(v).forEach(function(im){q2.drawImage(im,P.x,P.y,P.w,P.h)})}
   mem.forEach(function(q){var P=q.P,k;for(k in P.uf)if(q.f.uf[k])di(P.uf[k],P);for(k in P.pf)if(q.f.pf[k])di(P.pf[k],P);if(P.fill)q2.drawImage(P.fill,P.x,P.y,P.w,P.h)});
   mem.forEach(function(q){var P=q.P,k;for(k in P.pl)if(q.f.pl[k])di(P.pl[k],P);if(P.line)q2.drawImage(P.line,P.x,P.y,P.w,P.h)});
   if(GC.n>40){GC.e={};GC.n=0}ent=GC.e[key]={c:cv,x:x0,y:y0,w:cv.width/R,h:cv.height/R};GC.n++}
  g.save();var T=mul(B,G.m);g.setTransform(T[0]*C.dpr,T[1]*C.dpr,T[2]*C.dpr,T[3]*C.dpr,T[4]*C.dpr,T[5]*C.dpr);g.globalAlpha=G.a*(C.alpha==null?1:C.alpha);
  g.drawImage(ent.c,ent.x,ent.y,ent.w,ent.h);
  if(G.glow>0&&!C.glowLater){g.globalCompositeOperation="lighter";g.globalAlpha=G.glow*.55;G.items.forEach(function(e){e.pt.fills.forEach(function(f){fillIt(g,f,G.gcol)})});g.globalCompositeOperation="source-over"}
  g.restore()})}
MIM.drawFrameR=drawFrameR;MIM.drawFrame=drawFrame;
/* ---------- scenes ---------- */
var X,W,H,T,ONCE,S,MODE,K;
function grad(a,b){var q=X.createLinearGradient(0,0,0,H);q.addColorStop(0,a);q.addColorStop(1,b);X.fillStyle=q;X.fillRect(0,0,W,H)}
function cloud(x,y,s){X.fillStyle="rgba(255,255,255,.95)";X.beginPath();X.arc(x,y,28*s,0,7);X.arc(x+30*s,y-14*s,34*s,0,7);X.arc(x+66*s,y,28*s,0,7);X.rect(x,y-6*s,66*s,28*s);X.fill()}
function sky(t,night){grad("#a9dcff","#e6f6ff");for(var i=0;i<3;i++){var x=((hsh(i,4)*W+t*(14+i*6))%(W+220))-140;cloud(x,90+i*110,.8+i*.15)}if(night)dark(night,t)}
function dark(k,t){X.fillStyle="rgba(11,16,53,"+(k*.86)+")";X.fillRect(0,0,W,H);for(var i=0;i<40;i++){X.globalAlpha=k*(.5+.5*Math.sin(t*1.5+i));X.fillStyle="#fff";X.beginPath();X.arc(hsh(i,7)*W,hsh(i,8)*H*.6,1.5+hsh(i,9)*2,0,7);X.fill()}X.globalAlpha=1}
function ground(y,col,col2){X.fillStyle=col;X.fillRect(0,y,W,H-y);X.fillStyle=col2;for(var i=0;i<9;i++){X.beginPath();X.ellipse(i*70,y,60,16,0,Math.PI,0);X.fill()}}
function flowers(y){for(var i=0;i<7;i++){var x=24+i*82,yy=y+18+hsh(i,2)*70;X.strokeStyle="#4c9a3a";X.lineWidth=3;X.beginPath();X.moveTo(x,yy);X.lineTo(x,yy-14);X.stroke();X.fillStyle=["#ffc531","#e5484d","#fff","#ff8fc7"][i%4];for(var k=0;k<5;k++){X.beginPath();X.arc(x+Math.cos(k*1.26)*5,yy-14+Math.sin(k*1.26)*5,4,0,7);X.fill()}X.fillStyle="#ffb100";X.beginPath();X.arc(x,yy-14,3,0,7);X.fill()}}
function meadow(t,night){sky(t);ground(H*.8,"#9fd47a","#8cc36a");flowers(H*.8);if(night)dark(night,t)}
function hills(t){sky(t);X.fillStyle="#bfe3a8";X.beginPath();X.ellipse(W*.2,H*1.02,W*.7,H*.2,0,0,7);X.fill();X.fillStyle="#a8d78f";X.beginPath();X.ellipse(W*.85,H*1.05,W*.6,H*.22,0,0,7);X.fill()}
function underwater(t){grad("#5ec8f2","#1b4f8a");X.fillStyle="rgba(255,255,255,.12)";for(var r=0;r<4;r++){X.beginPath();var x0=60+r*130+Math.sin(t*.6+r)*20;X.moveTo(x0,0);X.lineTo(x0+60,0);X.lineTo(x0+140,H*.85);X.lineTo(x0+40,H*.85);X.fill()}
 X.fillStyle="#f1d39b";X.fillRect(0,H*.87,W,H*.13);for(var s=0;s<5;s++){var bx=40+s*115;X.strokeStyle="#2fb344";X.lineWidth=10;X.lineCap="round";X.beginPath();X.moveTo(bx,H*.9);for(var k=1;k<=5;k++)X.lineTo(bx+Math.sin(t*2+k+s)*10,H*.9-k*26);X.stroke()}
 for(var b=0;b<14;b++){var y=H-((t*60*(1+b%3)+hsh(b,3)*H)%H);X.strokeStyle="rgba(255,255,255,.6)";X.lineWidth=2.5;X.beginPath();X.arc(hsh(b,5)*W+Math.sin(t*3+b)*6,y,4+b%4*2,0,7);X.stroke()}}
function seaTop(t,rough,y0){sky(t);y0=y0||H*.66;X.fillStyle="#2a8fd6";X.beginPath();X.moveTo(0,H);for(var x=0;x<=W;x+=10)X.lineTo(x,y0+Math.sin(x/50+t*2)*10*(rough||1));X.lineTo(W,H);X.fill();
 X.fillStyle="#1b6fb0";X.beginPath();X.moveTo(0,H);for(var x2=0;x2<=W;x2+=10)X.lineTo(x2,y0+40+Math.sin(x2/40-t*2.4)*8*(rough||1));X.lineTo(W,H);X.fill()}
function seaFront(t,rough,y0){y0=y0||H*.66;X.fillStyle="rgba(27,111,176,.92)";X.beginPath();X.moveTo(0,H);for(var x=0;x<=W;x+=10)X.lineTo(x,y0+26+Math.sin(x/36-t*2.6)*7*(rough||1));X.lineTo(W,H);X.fill()}
function road(t,sp){sky(t);ground(H*.68,"#9fd47a","#8cc36a");X.fillStyle="#565c66";X.fillRect(0,H*.72,W,H*.16);X.fillStyle="#fff";var off=((sp||0)%120+120)%120;for(var i=-1;i<7;i++)X.fillRect(i*120-off,H*.795,60,8)}
function rails(t,sp){sky(t);ground(H*.7,"#9fd47a","#8cc36a");var off=((sp||0)%44+44)%44;X.fillStyle="#8a5a35";for(var i=-1;i<14;i++)X.fillRect(i*44-off,H*.815,18,26);X.fillStyle="#7b8794";X.fillRect(0,H*.818,W,6);X.fillRect(0,H*.842,W,6)}
function field(t,sp){sky(t);X.fillStyle="#9fd47a";X.fillRect(0,H*.7,W,H*.3);X.fillStyle="#8b5a2b";X.fillRect(0,H*.78,W,H*.22);X.strokeStyle="#6e4520";X.lineWidth=5;var off=((sp||0)%60+60)%60;for(var i=-1;i<11;i++){X.beginPath();X.moveTo(i*60-off,H*.8);X.lineTo(i*60-off-40,H);X.stroke()}}
function space(t){grad("#0b1035","#232a7a");for(var i=0;i<60;i++){X.globalAlpha=.55+.45*Math.sin(t*1.3+i);X.fillStyle="#fff";X.beginPath();X.arc(hsh(i,11)*W,hsh(i,12)*H,1+hsh(i,13)*2,0,7);X.fill()}X.globalAlpha=1;
 X.fillStyle="#ff9a52";X.beginPath();X.arc(W*.82,H*.16,40,0,7);X.fill();X.strokeStyle="#ffd39b";X.lineWidth=6;X.beginPath();X.ellipse(W*.82,H*.16,66,16,-.3,0,7);X.stroke()}
function moonGround(t){space(t);X.fillStyle="#cfd3dc";X.beginPath();X.ellipse(W/2,H*1.15,W*.9,H*.36,0,0,7);X.fill();X.fillStyle="#b4b9c4";[[.2,.86,26],[.7,.9,34],[.45,.95,18]].forEach(function(c){X.beginPath();X.ellipse(W*c[0],H*c[1],c[2],c[2]*.4,0,0,7);X.fill()})}
function ice(t){grad("#cdeeff","#f3fbff");X.fillStyle="#fff";X.fillRect(0,H*.8,W,H*.2);X.fillStyle="#e2f3ff";X.fillRect(0,H*.8,W,10);for(var i=0;i<30;i++){X.fillStyle="#fff";X.beginPath();X.arc(hsh(i,1)*W+Math.sin(t+i)*20,(hsh(i,2)*H+t*50*(1+i%3))%H,2+i%3,0,7);X.fill()}}
function party(t){X.fillStyle="#fff6e0";X.fillRect(0,0,W,H);for(var i=0;i<22;i++){var x=hsh(i,1)*W,y=(hsh(i,2)*H+t*40*(1+i%3))%(H+40)-20;X.fillStyle=["#ffc531","#e5484d","#2a8fd6","#2fb344"][i%4];X.globalAlpha=.3;X.beginPath();X.arc(x,y,6+i%4*2,0,7);X.fill()}X.globalAlpha=1;X.fillStyle="#f1e3bf";X.fillRect(0,H*.8,W,H*.2)}
function stage(t){grad("#1b2a6b","#3b3fa8");X.fillStyle="rgba(255,255,255,.12)";X.beginPath();X.moveTo(W/2-60,0);X.lineTo(W/2+60,0);X.lineTo(W/2+230,H*.82);X.lineTo(W/2-230,H*.82);X.fill();X.fillStyle="#232a5e";X.fillRect(0,H*.82,W,H*.18)}
function table(t){X.fillStyle="#fff6e0";X.fillRect(0,0,W,H);X.fillStyle="#f6d7c3";for(var i=0;i<6;i++)for(var j=0;j<4;j++)if((i+j)%2===0)X.fillRect(i*W/6,H*.62+j*H*.095,W/6,H*.095);X.fillStyle="rgba(229,72,77,.28)";X.fillRect(0,H*.62,W,H*.38);X.fillStyle="#fff";X.globalAlpha=.6;for(var k=0;k<5;k++){X.beginPath();X.arc(60+k*110,90+hsh(k,3)*80,14,0,7);X.fill()}X.globalAlpha=1}
function pond(t){sky(t);X.fillStyle="#9fd47a";X.fillRect(0,H*.7,W,H*.3);X.fillStyle="#5ec8f2";X.beginPath();X.ellipse(W/2,H*.86,W*.62,H*.1,0,0,7);X.fill();X.fillStyle="#2fb344";[[.18,.86],[.8,.84],[.62,.92]].forEach(function(p,i){X.beginPath();X.ellipse(W*p[0],H*p[1],34,12,0,.3,TAU-.3);X.lineTo(W*p[0],H*p[1]);X.fill()})}
function garden(t,night){sky(t);ground(H*.8,"#9fd47a","#8cc36a");X.fillStyle="#d9c3a0";X.beginPath();X.moveTo(W*.45,H*.8);X.lineTo(W*.55,H*.8);X.lineTo(W*.7,H);X.lineTo(W*.3,H);X.fill();flowers(H*.8);if(night)dark(night,t)}
function nightSky(t){grad("#0b1035","#2a3a8c");for(var i=0;i<50;i++){X.globalAlpha=.5+.5*Math.sin(t*1.4+i);X.fillStyle="#fff";X.beginPath();X.arc(hsh(i,21)*W,hsh(i,22)*H*.7,1+hsh(i,23)*2,0,7);X.fill()}X.globalAlpha=1;X.fillStyle="#2c4a2a";X.fillRect(0,H*.8,W,H*.2)}
function own(t){X.fillStyle="#fff6e0";X.fillRect(0,0,W,H)}
function savannah(t){grad("#ffcf8f","#fff1d6");X.fillStyle="rgba(255,244,214,.9)";X.beginPath();X.arc(W*.72,H*.3,70,0,7);X.fill();X.fillStyle="#e7b86d";X.beginPath();X.ellipse(W*.25,H*.82,W*.7,H*.09,0,Math.PI,0);X.fill();X.fillStyle="#e8c36a";X.fillRect(0,H*.8,W,H*.2);
 [[.14,.8,1],[.86,.79,.8]].forEach(function(a){var x=W*a[0],y=H*a[1],k=a[2];X.strokeStyle="#7a5a2e";X.lineWidth=10*k;X.beginPath();X.moveTo(x,y);X.lineTo(x+6*k,y-120*k);X.stroke();X.fillStyle="#8aa04a";X.beginPath();X.ellipse(x+6*k,y-130*k,90*k,22*k,0,0,7);X.fill()});
 for(var i=0;i<24;i++){var gx=hsh(i,81)*W,gy=H*.8+hsh(i,82)*H*.18;X.strokeStyle="#c9a04e";X.lineWidth=3;X.beginPath();X.moveTo(gx,gy);X.lineTo(gx-6+Math.sin(t*1.5+i)*3,gy-18);X.moveTo(gx,gy);X.lineTo(gx+6+Math.sin(t*1.5+i)*3,gy-16);X.stroke()}}
function jungle(t){grad("#8fd9a8","#e9f8ee");for(var i=0;i<6;i++){var vx=40+i*95,sw=Math.sin(t*1.1+i)*8;X.strokeStyle="#4c9a3a";X.lineWidth=5;X.beginPath();X.moveTo(vx,0);X.quadraticCurveTo(vx+sw,H*.18,vx+sw*1.6,H*(.22+hsh(i,91)*.15));X.stroke();X.fillStyle="#5fb34a";X.beginPath();X.ellipse(vx+sw*1.6,H*(.22+hsh(i,91)*.15),12,7,.6,0,7);X.fill()}
 [[0,.52,1],[1,.58,-1],[0,.7,1],[1,.72,-1]].forEach(function(a,j){var x=W*a[0],y=H*a[1],d=a[2];X.fillStyle=j%2?"#2f8f46":"#3fae55";X.beginPath();X.moveTo(x,y);X.quadraticCurveTo(x+d*180,y-90,x+d*240,y+10+Math.sin(t+j)*6);X.quadraticCurveTo(x+d*150,y+40,x,y+30);X.fill()});
 X.fillStyle="#4c9a3a";X.fillRect(0,H*.82,W,H*.18);X.fillStyle="#5fb34a";for(var k=0;k<9;k++){X.beginPath();X.ellipse(k*68,H*.82,46,16,0,Math.PI,0);X.fill()}}
function bamboo(t){grad("#dff3e4","#f6fff7");for(var i=0;i<7;i++){var bx=20+i*84+(i%2)*20,sw=Math.sin(t*.9+i)*4;X.strokeStyle=i%2?"#8cc36a":"#7db85c";X.lineWidth=16;X.beginPath();X.moveTo(bx,H);X.lineTo(bx+sw,0);X.stroke();X.strokeStyle="#5f9a45";X.lineWidth=3;for(var j=1;j<9;j++){var jy=H-j*110+hsh(i,j)*20;X.beginPath();X.moveTo(bx-9+sw*(1-jy/H),jy);X.lineTo(bx+9+sw*(1-jy/H),jy);X.stroke();if(j%3===i%3){X.fillStyle="#6fb84f";X.beginPath();X.ellipse(bx+22,jy-8,22,6,-.5,0,7);X.fill()}}}
 X.fillStyle="#9fd47a";X.fillRect(0,H*.8,W,H*.2);X.fillStyle="#8cc36a";for(var k=0;k<9;k++){X.beginPath();X.ellipse(k*70,H*.8,60,16,0,Math.PI,0);X.fill()}}
function prehistoric(t){grad("#ffb38a","#ffe6cc");X.fillStyle="#e3a785";X.beginPath();X.moveTo(0,H*.8);X.lineTo(0,H*.62);X.quadraticCurveTo(W*.18,H*.5,W*.36,H*.64);X.quadraticCurveTo(W*.55,H*.52,W*.74,H*.62);X.quadraticCurveTo(W*.9,H*.55,W,H*.6);X.lineTo(W,H*.8);X.fill();
 for(var i=0;i<3;i++){var bx=((t*12+i*200)%(W+160))-80,by=H*(.18+i*.07);X.strokeStyle="#7a4a3a";X.lineWidth=4;X.lineCap="round";X.beginPath();X.moveTo(bx-18,by);X.quadraticCurveTo(bx-8,by-8+Math.sin(t*6+i)*5,bx,by);X.quadraticCurveTo(bx+8,by-8+Math.sin(t*6+i)*5,bx+18,by);X.stroke()}
 X.fillStyle="#c49a6c";X.fillRect(0,H*.8,W,H*.2);[[.08,.8],[.3,.81],[.9,.82]].forEach(function(p,j){var x=W*p[0],y=H*p[1];for(var k=0;k<5;k++){var an=-Math.PI/2+(k-2)*.38+Math.sin(t*1.2+j+k)*.05;X.strokeStyle="#5d9c45";X.lineWidth=7;X.beginPath();X.moveTo(x,y);X.quadraticCurveTo(x+Math.cos(an)*40,y+Math.sin(an)*60,x+Math.cos(an)*70,y+Math.sin(an)*80);X.stroke()}})}
var SCENES={savannah:savannah,jungle:jungle,bamboo:bamboo,prehistoric:prehistoric,sky:sky,meadow:meadow,hills:hills,tree:hills,underwater:underwater,sea:function(t){seaTop(t,1)},road:road,rails:rails,field:field,space:space,moon:moonGround,ice:ice,party:party,stage:stage,table:table,pond:pond,garden:garden,night:nightSky,own:own};

/* ---------- effects ---------- */
function star(x,y,r,col,a){X.globalAlpha=a==null?1:a;X.fillStyle=col;X.beginPath();for(var i=0;i<10;i++){var q=i*Math.PI/5-Math.PI/2,rr=i%2?r*.45:r;X.lineTo(x+Math.cos(q)*rr,y+Math.sin(q)*rr)}X.closePath();X.fill();X.globalAlpha=1}
function sparkles(x,y,R,t,n){for(var i=0;i<(n||6);i++){var q=i/(n||6)*TAU+t*.8,ph=(t*1.6+i*.37)%1;star(x+Math.cos(q)*R*(.7+hsh(i,3)*.5),y+Math.sin(q)*R*.8*(.7+hsh(i,4)*.5),6+10*Math.sin(ph*Math.PI),"#ffc531",Math.sin(ph*Math.PI))}}
function dizzy(x,y,t,r){for(var i=0;i<3;i++){var q=t*5+i*2.09;star(x+Math.cos(q)*(r||60),y+Math.sin(q)*16,12,"#ffc531")}}
function burst(x,y,t0,n,sp,cols,life,gr,sz){var a=T-t0;if(a<0||a>life)return;for(var i=0;i<n;i++){var q=hsh(i,21)*TAU,v=sp*(.4+hsh(i,22)*.8);X.globalAlpha=1-a/life;X.fillStyle=cols[i%cols.length];X.beginPath();X.arc(x+Math.cos(q)*v*a,y+Math.sin(q)*v*a+gr*a*a,Math.max(.5,(sz||8)*(1-a/life*.5)),0,7);X.fill()}X.globalAlpha=1}
function stream(t0,t1,rate,f){var n=Math.floor((Math.min(T,t1)-t0)*rate);for(var i=0;i<=n;i++){var b=t0+i/rate,a=T-b;if(a>=0)f(i,a)}}
function puff(x,y,a,life,s,col){if(a<0||a>life)return;X.globalAlpha=.55*(1-a/life);X.fillStyle=col||"#e9edf2";X.beginPath();X.arc(x,y,(s||14)+a*40,0,7);X.fill();X.globalAlpha=1}
function smoke(x,y,t0,t1,rate,dir,col,s){stream(t0,t1,rate||6,function(i,a){if(a>2.2)return;puff(x+(dir||0)*a*40+Math.sin(i*1.7+a*2)*10,y-a*70,a,2.2,s||8,col)})}
function bubble(x,y,r,a){X.strokeStyle="rgba(255,255,255,"+Math.max(0,.85-a*.4)+")";X.lineWidth=3;X.beginPath();X.arc(x,y,r,0,7);X.stroke()}
function bubbles(x,y,t0,t1,rate){stream(t0,t1,rate||4,function(i,a){if(a<2)bubble(x+Math.sin(i*2+a*3)*10,y-a*110,5+i%3*3,a)})}
function zzz(x,y,t){for(var i=0;i<3;i++){var a=((t*.7+i/3)%1);X.globalAlpha=Math.sin(a*Math.PI);X.fillStyle="#2a3a8c";X.font="900 "+(18+a*22)+"px ui-rounded,system-ui,sans-serif";X.fillText("z",x+a*60+i*4,y-a*90)}X.globalAlpha=1}
function note(x,y,a){X.globalAlpha=Math.max(0,1-a/1.6);X.fillStyle="#081130";X.beginPath();X.ellipse(x,y,9,7,-.4,0,7);X.fill();X.fillRect(x+6,y-30,4,30);X.globalAlpha=1}
function notes(x,y,t0,t1,rate){stream(t0,t1,rate||2,function(i,a){if(a<1.6)note(x+(i%2?1:-1)*(20+a*40),y-a*90,a)})}
function heart(x,y,r,a){X.globalAlpha=a;X.fillStyle="#e5484d";X.beginPath();X.moveTo(x,y+r*.9);X.bezierCurveTo(x-r*1.6,y-r*.2,x-r*.6,y-r*1.3,x,y-r*.4);X.bezierCurveTo(x+r*.6,y-r*1.3,x+r*1.6,y-r*.2,x,y+r*.9);X.fill();X.globalAlpha=1}
function hearts(x,y,t0,t1){stream(t0,t1,2.5,function(i,a){if(a<1.8)heart(x+Math.sin(i*2.1)*50,y-a*100,10+i%3*3,1-a/1.8)})}
function water(x,y,t0,t1,ang,sp,col){stream(t0,t1,30,function(i,a){if(a>1.1)return;var q=ang+(hsh(i,5)-.5)*.25,v=sp*(.85+hsh(i,6)*.3);X.globalAlpha=1-a/1.1;X.fillStyle=col||"#5ec8f2";X.beginPath();X.arc(x+Math.cos(q)*v*a,y+Math.sin(q)*v*a+380*a*a,4+hsh(i,7)*3,0,7);X.fill()});X.globalAlpha=1}
function speed(x,y,dir,n,h){X.strokeStyle="rgba(8,17,48,.35)";X.lineWidth=6;X.lineCap="round";for(var i=0;i<(n||5);i++){var yy=y-(h||80)*.2-i*(h||80)*.15;X.beginPath();X.moveTo(x-dir*(60+i*8),yy);X.lineTo(x-dir*(150+i*20),yy);X.stroke()}}
function confettiRain(t,t0){if(t<t0)return;for(var i=0;i<30;i++){var y=((t-t0)*260+hsh(i,2)*H*.6)-H*.3;if(y>H)continue;X.save();X.translate(hsh(i,1)*W+Math.sin(t*3+i)*14,y);X.rotate(t*4+i);X.fillStyle=["#ffc531","#e5484d","#2a8fd6","#2fb344"][i%4];X.fillRect(-5,-8,10,16);X.restore()}}
function dust(x,y,t0,n){for(var k=0;k<(n||4);k++)puff(x+(k-1.5)*26,y-6,(T-t0)-k*.04,.9,9,"#e8dcc8")}
function bigText(s,a,col,y){X.save();X.globalAlpha=a;X.fillStyle=col||"#fff";X.strokeStyle="#081130";X.lineWidth=10;X.textAlign="center";X.font="900 150px ui-rounded,system-ui,sans-serif";X.strokeText(s,W/2,y||H*.3);X.fillText(s,W/2,y||H*.3);X.restore()}
function word(s,x,y,a,col,size){X.save();X.globalAlpha=a;X.fillStyle=col||"#ffc531";X.strokeStyle="#081130";X.lineWidth=7;X.textAlign="center";X.font="900 "+(size||56)+"px ui-rounded,system-ui,sans-serif";X.strokeText(s,x,y);X.fillText(s,x,y);X.restore()}
function shadow(x,y,w,a){X.fillStyle="rgba(8,17,48,"+(a==null?.15:a)+")";X.beginPath();X.ellipse(x,y,Math.max(4,w),Math.max(2,w*.16),0,0,7);X.fill()}
function beam(x,y,ang,len,spread,a,col){X.save();X.globalAlpha=a;X.fillStyle=col||"#fff3b0";X.beginPath();X.moveTo(x,y);X.lineTo(x+Math.cos(ang-spread)*len,y+Math.sin(ang-spread)*len);X.lineTo(x+Math.cos(ang+spread)*len,y+Math.sin(ang+spread)*len);X.closePath();X.fill();X.restore()}
function flameFx(x,y,s,t){X.save();X.translate(x,y);X.scale(s,s*(1+.15*noise(t*9)));X.fillStyle="#ff922b";X.beginPath();X.moveTo(-12,0);X.quadraticCurveTo(-14,-22,0,-40);X.quadraticCurveTo(14,-22,12,0);X.closePath();X.fill();X.fillStyle="#ffd43b";X.beginPath();X.moveTo(-6,0);X.quadraticCurveTo(-7,-12,0,-24);X.quadraticCurveTo(7,-12,6,0);X.closePath();X.fill();X.restore()}

/* ---------- sounds ---------- */
var tone=function(){if(S&&S.tone)S.tone.apply(null,arguments)},nz=function(){if(S&&S.noise)S.noise.apply(null,arguments)},sfx=function(n,a){try{if(S&&S.SFX&&S.SFX[n])S.SFX[n](a)}catch(e){}};
var SND={
 squawk:function(){tone(900,.12,"square",.1,0,1500);tone(1100,.14,"square",.08,.15,700)},
 tweet:function(){tone(2200,.08,"sine",.08,0,2900);tone(2400,.08,"sine",.08,.12,3100)},
 hoot:function(){tone(420,.3,"sine",.16,0,380);tone(420,.4,"sine",.16,.4,360)},
 buzz:function(){tone(180,.9,"sawtooth",.05,0,200);tone(185,.9,"sawtooth",.04,.02,190)},
 honk:function(){tone(330,.22,"square",.12);tone(330,.22,"square",.12,.3)},
 beepbeep:function(){tone(1000,.12,"square",.1);tone(1000,.12,"square",.1,.25)},
 screech:function(){nz(.7,.18,3200,0,"highpass")},
 chug:function(){for(var i=0;i<4;i++)nz(.12,.2,500,i*.22,"lowpass")},
 choochoo:function(){tone(520,.35,"triangle",.12,0,500);tone(660,.35,"triangle",.1,0,640);tone(520,.5,"triangle",.12,.45,480);tone(660,.5,"triangle",.1,.45,620)},
 siren:function(){tone(700,.5,"triangle",.08,0,950);tone(950,.5,"triangle",.08,.5,700)},
 thud:function(){tone(110,.25,"sine",.4,0,45)},
 splash:function(){nz(.6,.25,700,0,"bandpass");nz(.4,.12,2400,.05,"bandpass")},
 click:function(){tone(2000,.04,"square",.12);tone(1300,.05,"square",.1,.08)},
 sparkle:function(){[1568,2093,2637].forEach(function(f,i){tone(f,.2,"sine",.06,i*.08)})},
 roar:function(){nz(1.2,.3,220,0,"lowpass");tone(90,1.1,"sawtooth",.1,0,60)},
 bigroar:function(){nz(1.6,.34,180,0,"lowpass");tone(70,1.5,"sawtooth",.12,0,45);tone(140,1.2,"square",.04,.1,90)},
 squeak:function(){tone(1400,.12,"sine",.1,0,2000)},
 howl:function(){tone(380,1.4,"sine",.14,0,760);tone(760,.6,"sine",.08,1.1,520)},
 woof:function(){nz(.12,.25,500,0,"bandpass");tone(260,.12,"square",.12,0,180);nz(.12,.25,500,.3,"bandpass");tone(260,.12,"square",.12,.3,180)},
 meow:function(){tone(700,.45,"sine",.12,0,1000);tone(1000,.3,"sine",.1,.3,600)},
 ribbit:function(){tone(220,.12,"square",.12,0,180);tone(240,.14,"square",.12,.18,170)},
 neigh:function(){tone(900,.6,"sawtooth",.06,0,500);tone(700,.4,"sawtooth",.05,.3,1100)},
 trumpet:function(){tone(300,.7,"sawtooth",.12,0,520);tone(520,.4,"sawtooth",.08,.5,380)},
 hiss:function(){nz(.6,.15,4000,0,"highpass")},
 munch:function(){tone(160,.08,"square",.15);tone(140,.08,"square",.15,.14);tone(160,.08,"square",.15,.28)},
 spit:function(){nz(.15,.2,2400,0,"bandpass");tone(600,.1,"sine",.08,.05,200)},
 burp:function(){tone(95,.45,"sawtooth",.16,0,60)},
 robo:function(){tone(300,.08,"square",.1);tone(600,.08,"square",.1,.1);tone(450,.12,"square",.1,.2)},
 pew:function(){tone(1400,.3,"square",.08,0,300)},
 blow:function(){nz(.6,.22,900,0,"bandpass")},
 sizzle:function(){nz(.8,.08,5000,0,"highpass")},
 slurp:function(){tone(300,.4,"sine",.1,0,800);nz(.3,.06,1500,.1,"bandpass")},
 pop:function(){sfx("pop")},boing:function(){sfx("boing")},whoosh:function(){sfx("whoosh")},toot:function(){sfx("toot")},flap:function(){sfx("flap")},bubble:function(){sfx("bubble")},
 cheer:function(){sfx("cheer")},twinkle:function(){sfx("twinkle")},spin:function(){sfx("spin")},wiggle:function(){sfx("wiggle")},rumble:function(){sfx("rumble")},engine:function(){sfx("engine")},horn:function(){sfx("horn")},grow:function(){sfx("grow")},bass:function(){sfx("bass")},beep:function(h){sfx("beep",h)},clap:function(){sfx("clap")}};
function snd(k,name,at){if(at!=null&&T<at)return;ONCE(k,function(){var f=SND[name];if(f)f()})}

/* ---------- helpers for choreography ---------- */
function st(o){return Object.assign({x:0,y:0,r:0,sx:1,sy:1,a:1},o||{})}
var KINDS={};
/* home placement: kinds say how big the drawing is and where it sits */
var PLACE={perch:{box:430,cy:.47},fly:{box:330,cy:.45},swim:{box:330,cy:.47},drive:{box:420,gy:.81},sail:{box:420,gy:.69},launch:{box:400,gy:.83},erupt:{box:430,gy:.82},
 float:{box:340,cy:.46},walk:{box:360,gy:.82},crawl:{box:380,gy:.82},waddle:{box:330,gy:.82},jelly:{box:340,gy:.82},robot:{box:340,gy:.82},spin:{box:360,cy:.46},
 sun:{box:360,cy:.42},grow:{box:420,gy:.82},house:{box:430,gy:.82},food:{box:360,gy:.8},roll:{box:300,gy:.8,ac:1},scene:{box:500,cy:.47},sit:{box:360,gy:.8}};

/* ---- perch: a bird or bug sitting on something that stays (the branch). It flies off and comes back to it. ---- */
function nearAng(a,ref){while(a-ref>Math.PI)a-=TAU;while(ref-a>Math.PI)a+=TAU;return a}
KINDS.perch=function(t,silly){var f=(K.M.opt.face||1),cry=K.M.opt.sound||"squawk",sleepy=!!K.M.opt.sleepy,R={h:st({}),D:{flap:0,speak:0},scene:K.M.plan.scene||"tree"},h=R.h;
 R.kicks=silly?[[.9,.7],[5.4,1.5],[7.2,1]]:[[1,1.1],[6.2,1.3]];
 var cs=.62,bh=K.hb.h*cs,room=Math.max(160,K.ay-bh-60),A=Math.min(85,room*.3),rise=Math.min(330,room-A),side=Math.min(150,W*.5-K.hb.w*cs*.5-10);
 function turn(vx){return Math.max(-1,Math.min(1,vx*f/15))||.02}
 var sc=1;
 if(!silly){
  if(t<1){R.blinks=[.35];R.D.speak=bump(t,.2,.45);snd("q0",cry,.2);if(t>.7){var c=seg(t,.7,1);h.sy=1-.1*c;h.sx=1+.05*c}}
  else if(t<2){var u=seg(t,1,2),ue=e3(u);h.x=f*L(0,side,ue);h.y=-L(0,rise,ue);h.r=-f*.22*bump(t,1,2);sc=L(1,cs,ue);h.sx=turn(side*3*(1-u)*(1-u)*f);R.D.flap=1.3;R.D.flapRate=1.15;snd("w1","whoosh",1);snd("fl1","flap",1.02)}
  else if(t<4.6){var q=seg(t,2,4.6)*TAU;h.x=f*side*Math.cos(q);h.y=-rise-A*Math.sin(2*q);h.sx=turn(-side*Math.sin(q)*f*2.4);h.r=-.25*Math.cos(2*q)*(h.sx>0?1:-1)*e3(seg(t,2,2.35));sc=cs;R.D.flap=.55+.45*Math.abs(Math.cos(2*q));R.trail=1;snd("fl2","flap",2.7);snd("q1",cry,3.7);R.D.speak=bump(t,3.7,4)}
  else if(t<5.8){var u2=eio(seg(t,4.6,5.8));h.x=f*L(side,0,u2);h.y=-L(rise,24,u2);h.sx=t<5.1?Math.min(1,Math.max(-1,-seg(t,4.6,4.75)*1)):(-1+2*eio(seg(t,5.1,5.6)));if(h.sx===0)h.sx=-.02;h.r=f*.12*bump(t,4.6,5.8);sc=L(cs,1,u2);R.D.flap=1.15}
  else if(t<6.2){var u3=seg(t,5.8,6.2);h.y=L(-24,0,e3(u3));R.D.flap=L(1.2,0,u3);h.sy=1-.08*bump(t,6,6.2)}
  else{h.sy=1+.05*bump(t,6.4,7);h.sx=1/h.sy;R.D.speak=bump(t,6.5,6.9);snd("q2",cry,6.5);R.spark=1;R.blinks=[7.05];snd("tw","sparkle",6.4)}}
 else{var rad=Math.min(110,room*.32),hc=Math.min(240,room-rad*2+20),up=Math.min(K.ay-70,hc+rad*.5+bh*.85),sideS=Math.min(110,side);
  function cruise(z){return{x:f*(50+Math.sin(z*5)*sideS),y:-up+Math.sin(z*8)*16,sx:Math.cos(z*5)>=0?1:-1}}
  if(t<.8){h.r=f*Math.sin(t*9)*.05*(1-seg(t,.6,.8));R.blinks=[.3]}
  else if(t<1.4){var a=e3(seg(t,.8,1.4));h.r=-f*a*.9;R.D.flap=1.5;R.D.flapRate=1.7;R.D.speak=1;snd("s0",cry,.85)}
  else if(t<2){var b=e3(seg(t,1.4,2));h.r=-f*L(.9,2.2,b);h.x=f*L(0,50,b)+Math.sin(t*30)*5*bump(t,1.4,2);h.y=-L(0,hc,b);sc=L(1,cs,b);R.D.flap=1.5;R.D.flapRate=1.7;snd("w0","whoosh",1.4)}
  else if(t<3.3){var q2=seg(t,2,3.3);h.x=f*(50+Math.sin(q2*TAU)*rad);h.y=-hc-(1-Math.cos(q2*TAU))*rad;h.r=-f*(2.2+q2*TAU);sc=cs;R.D.flap=1;snd("lp","spin",2)}
  else if(t<4.6){var z=t-3.3,cv=cruise(z),bl=e3(seg(t,3.3,3.75)),r0=-f*(2.2+TAU);h.x=L(f*50,cv.x,bl);h.y=L(-hc,cv.y,bl);h.r=L(r0,nearAng(Math.PI,r0),bl);h.sx=bl<1?L(1,cv.sx,bl)||.02:cv.sx;sc=cs;R.D.flap=.8;snd("t1","toot",3.5);snd("t2","toot",4.1);R.D.speak=bump(t,3.5,3.7)+bump(t,4.1,4.3)}
  else if(t<5.4){var u4=eio(seg(t,4.6,5.4)),c1=cruise(1.3);h.x=L(c1.x,0,u4);h.y=L(c1.y,0,u4);h.r=Math.PI;h.sx=L(c1.sx,1,seg(t,4.6,4.9))||.02;sc=L(cs,1,u4);R.D.flap=L(.8,.15,u4);snd("bo","boing",5.35)}
  else if(t<6.6){var z2=t-5.4;h.r=Math.PI+Math.sin(z2*5)*.38*Math.exp(-z2*.7);R.D.speak=bump(t,5.7,6)+bump(t,6.1,6.3);snd("s1","squeak",5.7);snd("s2","squeak",6.1);R.blinks=[6.35]}
  else if(t<7.2){var u5=eio(seg(t,6.6,7.2)),rs=Math.PI+Math.sin(1.2*5)*.38*Math.exp(-1.2*.7);h.r=L(rs,TAU,u5);R.D.flap=1;snd("w2","whoosh",6.6)}
  else{h.sy=1+.07*bump(t,7.2,7.55);h.sx=1/h.sy;R.D.speak=bump(t,7.22,7.55);snd("s3",cry,7.22)}}
 h.sx*=sc;h.sy*=sc;
 if(sleepy&&t<.9){R.D.eyesShut=1;R.zz=1;R.D.speak=0;R.blinks=null}else if(sleepy&&t<1.05){R.D.eyesShut=1-seg(t,.9,1.05)}
 R.front=function(){var p=heroPx(R.h);if(R.trail)stream(2,4.6,14,function(i,a){if(a<.8){var tt=T-a,q=seg(tt,2,4.6)*TAU;var x=K.ax+f*side*Math.cos(q),y=K.ay-rise-A*Math.sin(2*q)-bh*.45;star(x,y,7*(1-a/.8)+2,"#ffc531",1-a/.8)}});
  if(R.spark)sparkles(p.x,p.y-K.hb.h*.5,K.hb.w*.7,t,7);if(R.zz)zzz(p.x+f*K.hb.w*.35,p.y-K.hb.h*.9,t)};
 return R};

/* ---- fly: a flying thing with no perch (bee, butterfly, ladybird, dragon). ---- */
KINDS.fly=function(t,silly){var f=K.M.opt.face||1,R={h:st({}),D:{flap:1,speak:0},scene:K.M.plan.scene||"meadow"},h=R.h;R.D.flapRate=K.M.opt.flapRate||1;
 var buzz=K.M.opt.sound||"flap";
 if(!silly){
  if(t<1.6){var u=e3(t/1.6);h.x=f*L(-W*.75,0,u);h.y=L(-260,0,u)+Math.sin(u*Math.PI)*-120;h.r=f*L(.25,0,u);snd("bz",buzz,.1)}
  else if(t<4.2){var q=seg(t,1.6,4.2)*TAU;h.x=Math.sin(q)*130;h.y=-Math.sin(q*2)*80;h.r=Math.cos(q)*.15*f;R.trail=1}
  else if(t<5.4){var u2=seg(t,4.2,5.4);h.y=-Math.sin(u2*Math.PI)*220;h.r=f*u2*TAU;snd("sp","spin",4.2)}
  else if(t<6.4){h.y=Math.sin(t*3)*10;R.D.flap=.5;R.D.flapRate=.5;R.flower=1}
  else{h.y=Math.sin(t*3)*8;R.D.flap=.3;R.D.flapRate=.4;R.spark=1;snd("tw","sparkle",6.5)}}
 else{
  if(t<1.2){var a=e3(t/1.2);h.x=f*L(-W*.7,0,a)+Math.sin(t*20)*20;h.y=Math.sin(t*14)*40;R.D.flapRate=1.8;snd("bz",buzz,0)}
  else if(t<3.2){var u3=seg(t,1.2,3.2),side=Math.floor(u3*4);h.x=[1,-1,1,-1][side]*W*.32*Math.sin((u3*4%1)*Math.PI)*f;h.y=-Math.abs(Math.sin(u3*12))*120+Math.sin(u3*30)*20;h.r=Math.sin(t*12)*.3;R.D.flapRate=2;[1.7,2.2,2.7].forEach(function(b,i){snd("bk"+i,"boing",b)})}
  else if(t<4){h.r=Math.sin(t*20)*.4;h.y=Math.sin(t*25)*10;R.dizzy=1;R.D.flapRate=.4;R.D.flap=.4;snd("dz","wiggle",3.2)}
  else if(t<5.2){var q2=seg(t,4,5.2)*TAU;h.x=Math.sin(q2)*120*f;h.y=-(1-Math.cos(q2))*110;h.r=-q2*f;R.D.flapRate=1.6;snd("lp","spin",4)}
  else if(t<6.4){h.r=Math.PI*bump(t,5.2,6.4)*0;h.y=Math.sin(t*6)*30;h.sx=1+.12*Math.sin(t*16);h.sy=1-.12*Math.sin(t*16);snd("t1","toot",5.4);snd("t2","toot",5.9);R.D.speak=bump(t,5.4,5.6)+bump(t,5.9,6.1)}
  else{h.y=-Math.abs(Math.sin(t*7))*40;R.spark=1;snd("ch","cheer",6.6)}}
 R.back=function(){if(R.flower){var x=K.ax,y=K.ay+K.hb.h*.62;X.strokeStyle="#4c9a3a";X.lineWidth=8;X.beginPath();X.moveTo(x,H);X.lineTo(x,y);X.stroke();X.fillStyle="#ff8fc7";for(var k=0;k<6;k++){X.beginPath();X.arc(x+Math.cos(k*1.05)*22,y+Math.sin(k*1.05)*12,14,0,7);X.fill()}X.fillStyle="#ffc531";X.beginPath();X.arc(x,y,12,0,7);X.fill()}};
 R.front=function(){var p=heroPx(R.h);if(R.trail)stream(1.6,4.2,12,function(i,a){if(a<.7){var tt=T-a,q=seg(tt,1.6,4.2)*TAU;star(K.ax+Math.sin(q)*130,K.ay-Math.sin(q*2)*80,6*(1-a/.7)+2,"#ffc531",1-a/.7)}});if(R.dizzy)dizzy(p.x,p.y-K.hb.h*.6,t,K.hb.w*.4);if(R.spark)sparkles(p.x,p.y,K.hb.w*.8,t,7)};
 return R};

/* ---- swim ---- */
KINDS.swim=function(t,silly){var f=K.M.opt.face||1,R={h:st({}),D:{swim:1,speak:0,flap:1},scene:K.M.plan.scene||"underwater"},h=R.h,mp=pointPx("mouth");
 if(!silly){
  if(t<2){var u=eio(t/2);h.x=-f*L(W*.8,0,u);h.y=Math.sin(t*3)*30}
  else if(t<4.2){var q=seg(t,2,4.2)*TAU;h.x=Math.sin(q)*120;h.y=Math.sin(q*2)*60;h.r=Math.cos(q)*.12*f}
  else if(t<5.2){var u2=seg(t,4.2,5.2);h.sx=Math.cos(u2*TAU);snd("sp","spin",4.2)}
  else{h.y=Math.sin(t*2.4)*14;R.spark=1;R.D.swim=.5;snd("tw","sparkle",5.4)}
  R.bub=[0,7.6,3];R.D.speak=bump(t,5.6,6)}
 else{
  if(t<1.6){h.x=-f*L(W*.8,0,e3(t/1.6));h.y=Math.sin(t*5)*50;h.r=Math.cos(t*5)*.18;snd("b1","bubble",.2)}
  else if(t<2.8){h.r=Math.sin(t*20)*.05;R.D.speak=bump(t,1.9,2.05)+bump(t,2.25,2.4)+bump(t,2.6,2.75);[1.9,2.25,2.6].forEach(function(b,i){snd("h"+i,"burp",b)});R.hic=1}
  else if(t<4.2){h.r=seg(t,2.8,4.2)*TAU*2;R.D.swim=2;snd("sp","spin",2.8);R.swirl=1}
  else if(t<5.4){h.x=f*L(0,W*.9,ei3(seg(t,4.2,5.4)));R.D.swim=2.5;snd("wh","whoosh",4.2)}
  else if(t<6.4){h.x=-f*L(W*.9,0,e3(seg(t,5.4,6.4)));h.r=TAU*e3(seg(t,5.4,6.4))}
  else{h.sx=1+Math.sin(t*16)*.08;h.sy=1-Math.sin(t*16)*.08;R.D.speak=.6;snd("g","wiggle",6.4)}}
 R.front=function(){var p=heroPx(R.h),m=mp?heroPoint(R.h,mp):{x:p.x+f*K.hb.w*.45,y:p.y-K.hb.h*.55};if(R.bub)bubbles(m.x,m.y,0,7.6,2.5);if(R.hic)[1.9,2.25,2.6].forEach(function(b,i){var a=T-b;if(a>0&&a<2)bubble(m.x+f*10,m.y-a*200,16+i*6,a)});
  if(R.swirl)for(var i=0;i<10;i++){var q=i*.63+t*6;bubble(p.x+Math.cos(q)*K.hb.w*.7,p.y-K.hb.h*.5+Math.sin(q)*K.hb.w*.7,8,0)}if(R.spark)sparkles(p.x,p.y-K.hb.h*.5,K.hb.w*.8,t)};
 return R};

/* ---- drive: vehicles. Wheels turn with the ground as it moves. opt.vehicle: car | tractor | train | digger | fireengine ---- */
function integ(v,t){var n=Math.max(1,Math.ceil(t*120)),dt=t/n,d=0;for(var i=0;i<n;i++)d+=v((i+.5)*dt)*dt;return d}
function roadCool(t){return t<1.8?0:t<3?1000*e3(seg(t,1.8,2.2)):t<4.4?1000*(1-eio(seg(t,3,4.4))):0}
function roadSilly(t){return t<1.5?400*(1-seg(t,1.1,1.5)):t<3?0:t<4.2?-180*Math.sin(seg(t,3,4.2)*Math.PI):t<5.2?1200*seg(t,4.2,5.2):t<6.2?1200*(1-e3(seg(t,5.2,6.2))):0}
function waterTo(x0,y0,x1,y1,t0,t1,col){var Tf=.75,vx=(x1-x0)/Tf,vy=(y1-y0-380*Tf*Tf)/Tf;stream(t0,t1,30,function(i,a){if(a>Tf+.08)return;var jx=(hsh(i,5)-.5)*.16,jv=.92+hsh(i,6)*.16;X.globalAlpha=Math.min(1,(Tf+.08-a)*6);X.fillStyle=col||"#5ec8f2";X.beginPath();X.arc(x0+vx*jv*a+jx*vx*a*.3,y0+vy*jv*a+380*a*a,4+hsh(i,7)*3,0,7);X.fill()});X.globalAlpha=1}
KINDS.drive=function(t,silly){var o=K.M.opt,f=o.face||1,v=o.vehicle||"car",R={h:st({}),D:{speak:0},scene:K.M.plan.scene||(v==="train"?"rails":v==="tractor"||v==="digger"?"field":"road"),sp:0},h=R.h,ex=pointPx(o.exhaust||"exhaust");
 function bumpy(a){return-Math.abs(Math.sin(t*14))*a}
 var road=integ(silly?roadSilly:roadCool,t);R.sp=road*f;R.roll=road*f;
 if(!silly){
  if(t<1.8){h.x=-f*W*.5;R.lights=Math.min(2,Math.floor(t/.6));snd("c"+R.lights,"beep",t-(t%.6)+.001);h.r=Math.sin(t*40)*.008}
  else if(t<3){var u=e3(seg(t,1.8,3));h.x=-f*L(W*.5,0,u);R.lines=1;snd("go","horn",1.8);snd("en","engine",1.85);R.smk=1}
  else if(t<4.4){var u2=seg(t,3,4.4);h.x=f*Math.sin(u2*Math.PI)*40;h.r=-f*.07*Math.sin(u2*Math.PI);R.drift=1;snd("dr","screech",3)}
  else if(t<6){R.act=1}
  else{h.y=-Math.abs(Math.sin(t*Math.PI*2))*10;R.spark=1;snd("tw","sparkle",6.1)}}
 else{
  if(t<1.5){h.x=-f*L(W*.85,40,e3(t/1.5));h.y=bumpy(12);snd("en","engine",0);R.smk=1}
  else if(t<2.1){h.x=-f*40;snd("hk",v==="train"?"choochoo":"honk",1.5);h.sy=1+Math.sin(t*30)*.04;R.D.speak=1}
  else if(t<3){h.x=-f*40;h.r=-f*.28*Math.sin(seg(t,2.1,3)*Math.PI);h.y=bumpy(10);snd("bo","boing",2.1)}
  else if(t<4.2){h.x=-f*L(40,150,seg(t,3,4.2));[3.1,3.5,3.9].forEach(function(b,i){snd("bb"+i,"beep",b)})}
  else if(t<5.2){var u3=ei3(seg(t,4.2,5.2));h.x=f*L(-150,W*.9,u3);R.lines=1;snd("wh","whoosh",4.2)}
  else if(t<6.2){var u4=e3(seg(t,5.2,6.2));h.x=-f*L(W*.9,0,u4);if(u4>.6){R.skid=1;snd("sc","screech",5.75)}}
  else{h.y=-Math.abs(Math.sin(t*9))*26;snd("hk2",v==="train"?"choochoo":"honk",6.3);R.D.speak=bump(t,6.3,6.8)}}
 R.D.walk=1;R.D.speak=Math.max(R.D.speak,R.act?1:0);
 /* vehicle signature in Cool 4.4–6: digger digs, fire engine puts out a fire, train puffs, car flashes its lights */
 if(R.act){if(v==="digger"){R.D.dig=Math.sin(seg(t,4.4,6)*TAU)*.5+.5;snd("dg","rumble",4.5)}
  else if(v==="fireengine"){R.D.glow=.5+.5*Math.sin(t*Math.PI*2*1.5);snd("sr","siren",4.4);snd("sr2","siren",5.2)}
  else if(v==="train"){snd("cc","choochoo",4.5);R.smk=2}
  else{R.D.glow=.6;snd("hk","honk",4.6)}}
 function fire(){var U=K.hbU,front=f>0?K.X0+(U.x+U.w)*K.s:K.X0+U.x*K.s;return{x:f>0?Math.min(W-45,front+55):Math.max(45,front-55),y:K.gy}}
 R.back=function(){if(v==="fireengine"&&!silly&&t>=4.2&&t<6.4){var F=fire();var a=(1-seg(t,5.4,6.2))*seg(t,4.2,4.5);if(a>0){flameFx(F.x,F.y,1.6*a,t);flameFx(F.x+f*26,F.y,1.1*a,t+1);flameFx(F.x-f*20,F.y,.9*a,t+2)}}};
 R.front=function(){var p=heroPx(R.h),hw=K.hb.w,hh=K.hb.h;var e=ex?heroPoint(R.h,ex):{x:p.x-f*hw*.5,y:p.y-hh*.25};
  if(R.smk){var rate=R.smk===2?8:4;if(v==="train"){var fu=pointPx("funnel")||pointPx("chimney");var c=fu?heroPoint(R.h,fu):{x:p.x+f*hw*.3,y:p.y-hh};stream(0,7.6,rate,function(i,a){if(a<2.2)puff(c.x-f*a*50+Math.sin(i)*8,c.y-a*60,a,2.2,9)})}else stream(0,7.6,rate,function(i,a){if(a<1.2)puff(e.x-f*a*60,e.y-a*20,a,1.2,7)})}
  if(R.lines)speed(p.x,p.y,f,4,hh);if(R.skid)for(var k=0;k<4;k++)puff(p.x-f*hw*.45-f*k*24,p.y-10,(t-5.75)-k*.05,1,10);
  if(R.drift)for(var k2=0;k2<6;k2++)puff(p.x-f*hw*.45,p.y-10,(t-3)-k2*.18,1.2,12);
  if(R.lights!=null){var cx=W/2;[0,1,2].forEach(function(i){X.fillStyle="#081130";X.beginPath();X.arc(cx-80+i*80,150,34,0,7);X.fill();X.fillStyle=i<=R.lights?["#e5484d","#ffc531","#2fb344"][i]:"#3a4058";X.beginPath();X.arc(cx-80+i*80,150,24,0,7);X.fill()})}
  if(v==="fireengine"&&!silly&&t>=4.6&&t<6.2){var hp=pointPx("hose")||pointPx("nozzle");var hq=hp?heroPoint(R.h,hp):{x:p.x+f*hw*.4,y:p.y-hh*.8};var F=fire();waterTo(hq.x,hq.y,F.x,F.y-30,4.6,6.2);stream(4.95,6.5,7,function(i,a){if(a<1.3)puff(F.x+Math.sin(i*2.3)*24,F.y-40-a*70,a,1.3,12,"#eef1f5")})}
  if(v==="digger"&&!silly&&t>=4.4&&t<6.2){var bp=pointPx("bucket");if(bp){var bq=heroPoint(R.h,bp);if(t>5.2)burst(bq.x,bq.y,5.25,14,160,["#8b5a2b","#a9713b"],.9,500,6)}}
  if(R.spark)sparkles(p.x,p.y-hh*.5,hw*.7,t)};
 return R};

/* ---- sail ---- */
KINDS.sail=function(t,silly){var f=K.M.opt.face||1,R={h:st({}),D:{},scene:"sea",rough:1},h=R.h;
 if(silly){R.rough=t>2&&t<4.5?2.6:1.4;if(t<1.8)h.x=-f*L(W*.8,0,e3(t/1.8));if(t>=2.4&&t<4){var u=seg(t,2.4,4);h.y=-Math.sin(u*Math.PI)*280;h.r=u*TAU;snd("wh","whoosh",2.4)}if(t>=4&&t<6){h.r=Math.sin(t*8)*.25;h.sx=1+Math.sin(t*12)*.05;snd("spl","splash",4)}if(t>=6){h.r=Math.sin(t*3)*.08;snd("hk","honk",6)}snd("tw","tweet",1.9)}
 else{if(t<2.5)h.x=-f*L(W*.8,0,eio(t/2.5));snd("hk","honk",2.6);if(t>3)R.spark=1;snd("tw","sparkle",3.1)}
 h.y+=Math.sin(t*2)*8;h.r+=Math.sin(t*2)*.06;R.D.wind=1+(R.rough-1)*.5;
 R.back=function(){seaTop(t,R.rough,K.ay-K.M.s*2)};R.scene="none";
 R.front=function(){var p=heroPx(R.h);seaFront(t,R.rough,K.ay-K.M.s*2);if(silly)burst(p.x,K.ay-10,4,14,260,["#fff","#bfe6ff"],.8,500,8);if(R.spark)sparkles(p.x,p.y-K.hb.h*.5,K.hb.w*.7,t)};
 return R};

/* ---- launch: rocket ---- */
KINDS.launch=function(t,silly){var R={h:st({}),D:{flame:0},scene:"none",noShadow:1},h=R.h,k=0,nz=pointPx("nozzle");
 if(!silly){
  if(t<2.4){var n=3-Math.floor(t/.8);h.x=Math.sin(t*50)*t*1.2;R.count=n;R.D.flame=t>1.6?.4:0;snd("c"+n,"beep",t-(t%.8)+.001)}
  else if(t<4.4){var u=seg(t,2.4,4.4);k=u;h.y=-L(0,H*1.3,u*u);R.D.flame=1;snd("go","horn",2.4);snd("rr","roar",2.45);R.fire=1}
  else{k=1;var u2=e3(seg(t,4.4,6));h.y=L(-H,-(K.ay-H*.6),u2);h.r=Math.sin(t*1.2)*.2;R.D.flame=.6;R.fire=1;if(t>6){R.spark=1;snd("tw","sparkle",6)}}}
 else{
  if(t<1.2){h.x=Math.sin(t*50)*3*t}
  else if(t<2.2){var a=seg(t,1.2,2.2);h.y=-Math.sin(a*Math.PI)*90;R.D.flame=.4;snd("f","toot",1.2);snd("bo","boing",2.15)}
  else if(t<3){h.x=Math.sin(t*60)*6}
  else if(t<5){var b=seg(t,3,5);h.y=-L(0,H*1.1,b*b);h.x=Math.sin(b*14)*120*b;h.r=Math.cos(b*14)*.4*b;R.D.flame=1;R.fire=1;k=b;snd("rr","roar",3)}
  else{var c=seg(t,5.2,7.2);k=1-c;h.y=-L(H*.9,0,c);h.r=Math.sin(t*3)*.15;R.chute=t<7.3;if(c>.98)snd("bo2","boing",7.15)}}
 R.k=k;
 R.back=function(){if(k>=1&&!silly)space(t);else{sky(t,k);var gy=K.ay+(silly?0:(t>2.4&&t<4.4?seg(t,2.4,4.4)*600:0));if(!(k>=1))ground(gy,"#9fd47a","#8cc36a")}};
 R.front=function(){var p=heroPx(R.h),n=nz?heroPoint(R.h,nz):{x:p.x,y:p.y};if(R.fire)stream(0,7.6,30,function(i,a){if(a<1)puff(n.x+Math.sin(i*3)*14,n.y+a*140,a,1,10)});
  if(R.count>0)bigText(String(R.count),1-(t%.8)/.8*.5);
  if(R.chute){var ty=p.y-K.hb.h-70;X.fillStyle="#e5484d";X.beginPath();X.arc(p.x,ty,90,Math.PI,0);X.fill();X.fillStyle="#fff";for(var s=0;s<3;s++){X.beginPath();X.moveTo(p.x-90+s*60,ty);X.arc(p.x-60+s*60,ty,30,Math.PI,0);X.fill()}X.strokeStyle="#081130";X.lineWidth=2;X.beginPath();X.moveTo(p.x-90,ty);X.lineTo(p.x-K.hb.w*.2,p.y-K.hb.h*.85);X.moveTo(p.x+90,ty);X.lineTo(p.x+K.hb.w*.2,p.y-K.hb.h*.85);X.stroke()}
  if(R.spark)sparkles(p.x,p.y-K.hb.h*.5,K.hb.w*.9,t)};
 return R};

/* ---- erupt: volcano stays, the eruption comes out of the crater ---- */
KINDS.erupt=function(t,silly){var R={h:st({}),D:{rumble:0,glow:0},scene:silly?"meadow":"none"},h=R.h,cpu=pointPx("crater"),t0=silly?3:2;
 if(silly){if(t<1.5)R.D.rumble=t/1.5*.6;else if(t<2.4){R.D.rumble=.3;snd("bp","burp",1.5)}else if(t<3)R.D.rumble=1;else if(t<6){R.D.rumble=.5;h.sy=1+Math.abs(Math.sin(t*6))*.03}snd("rm","rumble",2.4)}
 else{if(t<2)R.D.rumble=t/2;else if(t<6)R.D.rumble=.8;R.D.glow=cl((t-2)/.6)*(t<6.6?1:1-seg(t,6.6,7.4));snd("rm","rumble",.1)}
 h.x=Math.sin(t*45)*R.D.rumble*4;
 R.back=function(){if(!silly){meadow(t,Math.min(1,t/1.5))}};
 R.front=function(){var cq=cpu?heroPoint(R.h,cpu):{x:K.ax+h.x,y:K.ay-K.hb.h*.85},cx=cq.x,cy=cq.y;if(silly&&t>1.5&&t<2.4)stream(1.5,2.4,10,function(i,a){puff(cx+Math.sin(i)*10,cy-a*80,a,.9,10)});
  if(t>t0){snd("er","cheer",t0);stream(t0,6.4,24,function(i,a){if(a>1.6)return;var q=-Math.PI/2+(hsh(i,31)-.5)*1.4,v=380+hsh(i,32)*260;X.fillStyle=silly&&i%3===0?["#2a8fd6","#2fb344","#ffc531"][i%3]:["#ff6b1a","#e5484d","#ffc531"][i%3];X.beginPath();X.arc(cx+Math.cos(q)*v*a,cy+Math.sin(q)*v*a+520*a*a,Math.max(1,11-a*3),0,7);X.fill()});
   stream(t0,7.4,4,function(i,a){puff(cx+Math.sin(i*2)*40,cy-40-a*120,a,2,20)})}
  if(!silly&&t>2){X.globalAlpha=.22*R.D.glow;X.fillStyle="#ff9a52";X.beginPath();X.arc(cx,cy,150,0,7);X.fill();X.globalAlpha=1}};
 return R};

/* ---- float: balloon, astronaut, flying saucer ---- */
KINDS.float=function(t,silly){var o=K.M.opt,v=o.floater||"balloon",R={h:st({}),D:{},scene:K.M.plan.scene||(v==="balloon"?"sky":"space")},h=R.h;
 if(v==="balloon"){h.y=L(H*.5,0,e3(t/2.4));h.x=Math.sin(t*.9)*60;h.r=Math.sin(t*1.1)*.06;R.D.swing=1;
  if(silly){if(t>2.6&&t<4.2){h.y=-L(0,K.ay-K.hb.h-20,e3(seg(t,2.6,3.4)));snd("bo","boing",3.4)}if(t>=4.2){h.y=-L(K.ay-K.hb.h-20,0,e3(seg(t,4.2,6)))+Math.sin(t*6)*8*(1-seg(t,4.2,6));R.D.swing=2}snd("tw","tweet",2.4);snd("tw2","tweet",5);R.D.burn=bump(t,1,1.6)+bump(t,5.2,5.8)}
  else{R.D.burn=bump(t,2.6,3.4)+bump(t,5,5.6);if(t>3)R.spark=1;snd("tw","sparkle",3)}
  if(R.D.burn>.1)snd("bn"+(t<4?1:2),"blow",t<4?(silly?1:2.6):(silly?5.2:5))}
 else if(v==="ufo"){if(silly){h.x=Math.sin(t*2.2)*150;h.y=Math.sin(t*3.1)*90;h.r=Math.sin(t*4)*.25;if(t>3&&t<4.5){h.sx=Math.cos(seg(t,3,4.5)*TAU*2);snd("sp","spin",3)}[1,2.5,5].forEach(function(b,i){snd("pw"+i,"pew",b)})}
  else{h.x=-L(W*.8,0,e3(t/1.6));h.y=Math.sin(t*2)*16;R.D.beam=cl((t-2)*2)*(t>6?Math.max(0,(6.5-t)*2):1);snd("bm","sparkle",2.2);if(t>6.5){R.spark=1}}
  R.D.lift=silly?0:1}
 else{h.x=Math.sin(t*.8)*80;h.y=Math.sin(t*1.1)*60;h.r=t*(silly?2.4:.5);R.D.wave=1;if(!silly){if(t>3)R.spark=1;snd("tw","twinkle",.5)}else{snd("w","whoosh",.3);snd("w2","whoosh",4)}}
 R.front=function(){var p=heroPx(R.h);if(R.spark)sparkles(p.x,p.y-K.hb.h*.5,K.hb.w*.8,t);
  if(v==="balloon"&&R.D.burn>.05){var bp=pointPx("burner");if(bp){var b=heroPoint(R.h,bp);flameFx(b.x,b.y,1.2*R.D.burn,t)}}
  if(v==="ufo"&&R.D.beam>0&&!o.ownBeam){var bs=pointPx("beam")||{x:K.ax,y:K.ay};var q=heroPoint(R.h,bs);X.globalAlpha=.35*R.D.beam;X.fillStyle="#ffe58a";X.beginPath();X.moveTo(q.x-30,q.y);X.lineTo(q.x+30,q.y);X.lineTo(q.x+150,H*.95);X.lineTo(q.x-150,H*.95);X.fill();X.globalAlpha=1}};
 return R};

/* ---- walk: animals on the ground. opt.act: roar | howl | spray | bark | meow | tongue | stomp | sparkle | munch | spit | hiss ---- */
function actWindow(silly){return silly?[2.5,3.5]:[2.2,3.6]}
KINDS.walk=function(t,silly){var o=K.M.opt,f=o.face||1,act=o.act||"",R={h:st({}),D:{walk:0,speak:0,wagRate:1,tilt:0,nod:0},scene:K.M.plan.scene||"meadow"},h=R.h,A=actWindow(silly),sound=o.sound||"";if(o.sleepy&&t<1.2){R.zz=1;R.D.eyesShut=1}
 if(!silly){
  if(t<1.8){var u=t/1.8;if(o.gait==="hop"){var gp=(t%.6)/.6,gn=Math.floor(t/.6);h.x=f*L(-W*.85,0,Math.min(1,(gn+e3(gp))/3));h.y=-Math.sin(gp*Math.PI)*110;h.sy=gp<.1||gp>.92?.86:1.04;h.sx=1/h.sy;snd("gh"+gn,"boing",gn*.6+.02)}else{h.x=f*L(-W*.85,0,e3(u));R.D.walk=1-u*.6;h.y=-Math.abs(Math.sin(t*Math.PI*2.4))*10;h.r=Math.sin(t*Math.PI*2.4)*.04}}
  else if(t<A[0]){R.blinks=[2]}
  else if(t<A[1]){R.actT=seg(t,A[0],A[1])}
  else if(t<5){var b=Math.floor((t-3.6)*2);h.x=(b%2?50:-50)*e3(((t-3.6)*2)%1)*f;h.r=(b%2?.1:-.1);h.y=-Math.abs(Math.sin(t*Math.PI*2))*18;R.D.walk=1;if(((t-3.6)*2)%1<.1)snd("bt"+b,"bass",t)}
  else if(t<5.8){var u2=seg(t,5,5.8);h.y=-Math.sin(u2*Math.PI)*150;h.sx=Math.cos(u2*TAU);snd("sp","spin",5)}
  else{h.y=-Math.abs(Math.sin(t*Math.PI*2))*8;R.spark=1;R.D.wagRate=2;R.D.speak=bump(t,6.2,6.6);snd("tw","sparkle",5.9);if(sound)snd("snd2",sound,6.2);R.notes=1}}
 else{
  if(t<1.6){var hp=(t%.53)/.53;h.x=f*L(-W*.8,0,t/1.6);h.y=-Math.sin(hp*Math.PI)*120;h.sy=hp<.12||hp>.9?.86:1.05;h.sx=1/h.sy;R.D.walk=.6;snd("h"+Math.floor(t/.53),"boing",Math.floor(t/.53)*.53+.01)}
  else if(t<A[0]){var u3=seg(t,1.6,2.5);h.y=-Math.sin(u3*Math.PI)*280;h.r=f*u3*TAU;snd("fl","whoosh",1.6);snd("ld","boing",2.45)}
  else if(t<A[1]){R.actT=seg(t,A[0],A[1])}
  else if(t<4.8){if(t<4.2){R.D.walk=2.5;h.y=-Math.abs(Math.sin(t*20))*6}else{h.x=f*L(0,W*.95,ei3(seg(t,4.2,4.8)));R.lines=1;R.D.walk=2.5;snd("wh","whoosh",4.2)}}
  else if(t<5.6){var u4=e3(seg(t,4.8,5.6));h.x=-f*L(W*.95,0,u4);R.D.walk=2.5*(1-u4);if(u4>.6){R.skid=1;snd("sc","screech",5.3)}}
  else if(t<6.4){var u5=seg(t,5.6,5.9);h.r=-f*L(0,Math.PI/2,e3(u5));if(u5>=1){R.dizzy=1;R.D.eyesShut=.9}snd("tp","thud",5.88)}
  else{var u6=e3(seg(t,6.4,6.7));h.r=-f*L(Math.PI/2,0,u6);h.y=-Math.abs(Math.sin(t*8))*30*u6;R.D.speak=bump(t,6.8,7.2);R.D.wagRate=2.5;if(sound)snd("snd3",sound,6.8);else snd("gg","wiggle",6.8)}}
 /* signature act */
 if(R.actT!=null){var a=R.actT,ta=A[0];
  if(act==="roar"||act==="stomp"){R.D.speak=bump(t,ta+.2,A[1]-.1)*1.1;R.D.tilt=bump(t,ta,A[1])*.4;h.x+=Math.sin(t*50)*4*bump(t,ta+.2,A[1]-.2);snd("ra",silly?"squeak":(act==="stomp"?"bigroar":"roar"),ta+.2);R.roarLines=!silly;if(act==="stomp"){var sb=Math.floor(a*3);h.y=-Math.abs(Math.sin(a*3*Math.PI))*24;snd("st"+sb,"thud",ta+sb/3*(A[1]-ta)+.01);R.shake=1}}
  else if(act==="howl"){R.D.tilt=bump(t,ta,A[1]);R.D.speak=bump(t,ta+.2,A[1]-.1);snd("hw",silly?"squeak":"howl",ta+.2);R.moon=1}
  else if(act==="spray"){R.D.tilt=bump(t,ta,A[1]);R.spray=bump(t,ta+.3,A[1]-.1)>.2;snd("tr","trumpet",ta+.1);if(R.spray)snd("sp","splash",ta+.35)}
  else if(act==="bark"){R.D.speak=bump(t,ta+.1,ta+.4)+bump(t,ta+.6,ta+.9);R.D.wagRate=3;h.y=-Math.abs(Math.sin(a*2*Math.PI))*20;snd("wf","woof",ta+.1)}
  else if(act==="meow"){R.D.speak=bump(t,ta+.1,ta+.7);R.D.tilt=bump(t,ta,A[1])*.5;snd("mw","meow",ta+.1);R.hearts=1}
  else if(act==="tongue"){R.tongue=bump(t,ta+.2,ta+.9);R.D.speak=R.tongue;snd("rb","ribbit",ta+.05);if(t>ta+.9)R.fly=0;else R.fly=1;snd("gl","pop",ta+.55)}
  else if(act==="munch"){R.D.speak=Math.abs(Math.sin(a*5*Math.PI));snd("mn","munch",ta+.1);R.leaf=1}
  else if(act==="spit"){R.D.speak=bump(t,ta+.3,ta+.6);R.D.tilt=bump(t,ta,ta+.4)*-.3;snd("sp","spit",ta+.4);R.spit=1}
  else if(act==="hiss"){R.D.speak=bump(t,ta+.1,A[1]-.1);snd("hs","hiss",ta+.1)}
  else if(act==="sparkle"){R.D.tilt=bump(t,ta,A[1])*.6;snd("nh",o.sound||"neigh",ta+.05);R.horn=1;h.y=-Math.sin(a*Math.PI)*40}
  else{h.sx=1+Math.sin(t*14)*.06;h.r=Math.sin(t*14)*.1;snd("wg","wiggle",ta)}}
 R.front=function(){var p=heroPx(R.h),hw=K.hb.w,hh=K.hb.h,mp=pointPx("mouth"),m=mp?heroPoint(R.h,mp):{x:p.x+f*hw*.4,y:p.y-hh*.7};
  if(R.roarLines){X.strokeStyle="rgba(8,17,48,.5)";X.lineWidth=6;X.lineCap="round";for(var i=0;i<5;i++){var q=-.6+i*.3,r0=40+((t*200)%60);X.beginPath();X.arc(m.x,m.y,r0+20,q*f+(f<0?Math.PI:0)-.12,q*f+(f<0?Math.PI:0)+.12);X.stroke()}}
  if(R.moon){X.fillStyle="#fff3b0";X.beginPath();X.arc(W*.82,H*.14,40,0,7);X.fill()}
  if(R.spray){var tp=pointPx("trunk");var q2=tp?heroPoint(R.h,tp):m;water(q2.x,q2.y,actWindow(silly)[0]+.3,actWindow(silly)[1],f>0?-1.1:Math.PI+1.1,silly?560:460)}
  if(R.tongue>0){var fx=m.x+f*190,fy=m.y-40;X.strokeStyle="#e5484d";X.lineWidth=7;X.lineCap="round";X.beginPath();X.moveTo(m.x,m.y);X.lineTo(L(m.x,fx,R.tongue),L(m.y,fy,R.tongue));X.stroke();}
  if(R.fly){var ax0=actWindow(silly)[0];var fx2=m.x+f*190+Math.sin(t*9)*10,fy2=m.y-40+Math.cos(t*11)*8;if(t>ax0+.55){fx2=L(fx2,m.x,seg(t,ax0+.55,ax0+.9));fy2=L(fy2,m.y,seg(t,ax0+.55,ax0+.9))}X.fillStyle="#081130";X.beginPath();X.arc(fx2,fy2,5,0,7);X.fill();X.fillStyle="rgba(255,255,255,.8)";X.beginPath();X.ellipse(fx2-4,fy2-5,5,3,-.5,0,7);X.ellipse(fx2+4,fy2-5,5,3,.5,0,7);X.fill()}
  if(R.leaf){X.fillStyle="#2fb344";X.beginPath();X.ellipse(m.x+f*20,m.y+6,18,6,f*.3,0,7);X.fill()}
  if(R.spit){var ax1=actWindow(silly)[0]+.4;var a2=T-ax1;if(a2>0&&a2<1){X.fillStyle="#bfe6ff";X.beginPath();X.arc(m.x+f*a2*300,m.y-80*a2+260*a2*a2,7,0,7);X.fill()}}
  if(R.horn){var hp2=pointPx("horn");var hq=hp2?heroPoint(R.h,hp2):{x:p.x+f*hw*.3,y:p.y-hh};sparkles(hq.x,hq.y,50,t,6)}
  if(R.hearts)hearts(m.x,m.y-20,actWindow(silly)[0]+.1,actWindow(silly)[1]);
  if(R.lines)speed(p.x,p.y,f,4,hh);if(R.skid)dust(p.x-f*hw*.4,p.y,5.3,4);if(R.dizzy)dizzy(p.x-f*hh*.5,p.y-hw*.3,t,50);
  if(R.notes)notes(p.x,p.y-hh,5.9,7.6,2);if(R.spark)sparkles(p.x,p.y-hh*.5,hw*.8,t);if(R.zz)zzz(p.x+f*hw*.3,p.y-hh,t)};
 return R};

/* ---- sit: a head (or a sitting animal) that stays where it is. Same timing as walk, so the signature act is the same.
   opt.front: fence | hedge | grass | bush (the head peeks up from behind it); without it, the animal sits on the ground. ---- */
function eob(x){x=cl(x);var c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}
function cover(kind,y0,t){var i;if(kind==="fence"){X.fillStyle="#7fc35f";X.fillRect(0,y0+40,W,H-y0);for(i=-1;i<13;i++){var x=i*46+6;X.fillStyle="#d79a62";X.strokeStyle="#8a5a32";X.lineWidth=3;X.beginPath();X.moveTo(x,H);X.lineTo(x,y0+8);X.lineTo(x+18,y0-8);X.lineTo(x+36,y0+8);X.lineTo(x+36,H);X.closePath();X.fill();X.stroke()}X.fillStyle="#c48650";X.fillRect(0,y0+34,W,16);X.strokeRect(-2,y0+34,W+4,16);X.fillRect(0,y0+92,W,16);X.strokeRect(-2,y0+92,W+4,16)}
 else if(kind==="grass"){X.fillStyle="#6fb84f";X.fillRect(0,y0+30,W,H-y0);for(i=0;i<70;i++){var gx=hsh(i,61)*W,gh=50+hsh(i,62)*70,sw=Math.sin(t*1.6+i*.7)*8;X.fillStyle=i%3?"#7cc35a":"#5aa545";X.beginPath();X.moveTo(gx-9,H);X.lineTo(gx+sw,y0+40-gh*.4-hsh(i,63)*20);X.lineTo(gx+9,H);X.closePath();X.fill()}}
 else if(kind==="bush"){X.fillStyle="#2f8f46";X.fillRect(0,y0+34,W,H-y0);for(i=0;i<9;i++){var bx=i*68,by=y0+30+hsh(i,71)*18;X.fillStyle=i%2?"#3fae55":"#349e4c";X.beginPath();X.arc(bx,by,48,0,7);X.fill();X.fillStyle="rgba(255,255,255,.12)";X.beginPath();X.arc(bx-12,by-16,16,0,7);X.fill()}}
 else{X.fillStyle="#3f8f3a";X.fillRect(0,y0+20,W,H-y0);for(i=0;i<16;i++){var hx=i*38,hy=y0+22+Math.sin(i*1.9)*5;X.fillStyle=i%2?"#4a9d43":"#3f8f3a";X.beginPath();X.arc(hx,hy,26,0,7);X.fill()}X.fillStyle="rgba(255,255,255,.1)";for(i=0;i<16;i++){X.beginPath();X.arc(i*38-6,y0+14+Math.sin(i*1.9)*5,8,0,7);X.fill()}}}
KINDS.sit=function(t,silly){var o=K.M.opt,f=o.face||1,cv=o.front||null,R=KINDS.walk(t,silly),h=R.h,dn=K.hb.h*.95,mo=Math.max(30,Math.min(W*.24,W*.5-K.hb.w*.5-8));
 function clear(){h.x=0;h.y=0;h.r=0;h.sx=1;h.sy=1;R.lines=0;R.skid=0}
 if(!silly){
  if(t<1.8){clear();R.D.walk=0;if(cv){h.y=L(dn,0,eob(seg(t,.15,1.05)));snd("pp","pop",.45)}else{h.y=-bump(t,.3,.8)*30;var q=bump(t,.8,1);h.sy=1-.1*q;h.sx=1+.06*q}h.r=.09*Math.sin(seg(t,1.1,1.8)*TAU);R.blinks=[1.35]}
  else if(t>=3.6&&t<5&&cv){h.x*=.6}}
 else{
  if(t<1.6){clear();R.D.walk=0;if(cv){if(t<.6)h.y=L(dn,0,eob(seg(t,.12,.55)));else h.y=-Math.abs(Math.sin((t-.6)*Math.PI*2))*36;snd("p0","boing",.3);snd("p1","boing",1.1)}else{var gp=(t%.53)/.53;h.y=-Math.sin(gp*Math.PI)*90;h.sy=gp<.12||gp>.9?.86:1.05;h.sx=1/h.sy}}
  else if(t>=3.5&&t<5.6){if(cv){clear();R.D.walk=0;
    if(t<3.85)h.y=L(0,dn,ei3(seg(t,3.5,3.85)));else if(t<4.25){h.y=dn;h.x=f*mo}else if(t<4.6){h.x=f*mo;h.y=L(dn,0,eob(seg(t,4.25,4.6)));snd("m1","boing",4.3)}
    else if(t<4.9){h.x=f*mo;h.y=L(0,dn,ei3(seg(t,4.6,4.9)))}else if(t<5.2){h.y=dn;h.x=-f*mo}else{h.x=-f*mo*(1-e3(seg(t,5.2,5.6)));h.y=L(dn,0,eob(seg(t,5.2,5.5)));snd("m2","boing",5.25)}
    if(t>=3.5&&t<3.6)snd("dk","whoosh",3.5)}
   else{clear();if(t<4.6){h.x=f*L(0,W*.95,ei3(seg(t,3.5,4.6)));R.lines=1;snd("rl","whoosh",3.5)}else{h.x=-f*L(W*.95,0,e3(seg(t,4.6,5.6)))}h.r=h.x/(K.hb.h*.5)}}
  else if(t>=5.6&&t<6.4&&cv){h.r=Math.sin((t-5.6)*7)*.22*(1-seg(t,6.1,6.4));h.x=0;if(t>5.65){R.dizzy=1;R.D.eyesShut=.9}}
  else if(t>=6.4&&cv){h.r=0}}
 if(cv){R.noShadow=1;var wf=R.front;R.front=function(){cover(cv,K.gy-K.hb.h*.07,t);if(R.dizzy){R.dizzy=0;wf();var p=heroPx(R.h);dizzy(p.x,p.y-K.hb.h-6,t,60);R.dizzy=1}else wf()}}
 return R};

/* ---- crawl: snail and caterpillar ---- */
KINDS.crawl=function(t,silly){var f=K.M.opt.face||1,R={h:st({}),D:{walk:1,speak:0},scene:K.M.plan.scene||"meadow"},h=R.h,inch=1+.06*Math.sin(t*6);h.sx=inch;h.sy=1/inch;
 if(silly){if(t<3)h.x=f*L(-W*.75,0,t/3);else if(t<3.4){h.r=Math.sin(t*20)*.06;R.D.walk=0}else if(t<4.2){h.x=f*L(0,W*.95,e3(seg(t,3.4,4.2)));h.sx=1.25;h.sy=.82;R.lines=1;R.D.walk=3;snd("wh","whoosh",3.4)}
  else if(t<5.2){var u=e3(seg(t,4.2,5.2));h.x=-f*L(W*.95,0,u);h.sx=1.25;h.sy=.82;R.D.walk=3;if(u>.7){R.skid=1;snd("sc","screech",4.9)}}else if(t<6.4){h.r=Math.sin(t*6)*.08;R.dizzy=1;R.D.walk=0}else{h.y=-Math.abs(Math.sin(t*8))*36;snd("hp","boing",6.4)}}
 else{h.x=f*L(-W*.75,0,e3(t/4));R.trail=1;if(t>4&&t<5){h.sx=Math.cos(seg(t,4,5)*TAU);snd("sp","spin",4)}if(t>5){R.spark=1;R.D.walk=.3;snd("tw","sparkle",5.1)}}
 R.front=function(){var p=heroPx(R.h);if(R.trail){X.strokeStyle="rgba(255,197,49,.7)";X.lineWidth=8;X.lineCap="round";X.beginPath();X.moveTo(f>0?-50:W+50,K.ay+4);X.lineTo(p.x,K.ay+4);X.stroke()}if(R.lines)speed(p.x,p.y,f,4,K.hb.h);if(R.skid)dust(p.x-f*K.hb.w*.4,p.y,4.9,4);if(R.dizzy)dizzy(p.x,p.y-K.hb.h-10,t,50);if(R.spark)sparkles(p.x,p.y-K.hb.h*.5,K.hb.w*.8,t)};
 return R};

/* ---- waddle: penguin ---- */
KINDS.waddle=function(t,silly){var f=K.M.opt.face||1,R={h:st({}),D:{walk:0,flap:0,speak:0},scene:"ice"},h=R.h;
 if(silly){if(t<2.4){h.x=f*L(-W*.75,0,t/2.4);h.r=Math.sin(t*9)*.2;h.y=-Math.abs(Math.sin(t*9))*8;R.D.walk=1;R.D.flap=.4}
  else if(t<2.9){h.r=-f*L(0,Math.PI/2,e3(seg(t,2.4,2.9)));snd("fl","thud",2.8);R.D.flap=1}
  else if(t<4.3){h.r=-f*Math.PI/2;h.x=f*L(0,W*.9,e3(seg(t,2.9,4.3)));snd("wh","whoosh",2.9);R.snow=1;R.D.flap=.6}
  else if(t<5.3){h.r=-f*Math.PI/2;h.x=-f*L(W*.9,0,e3(seg(t,4.3,5.3)))}
  else if(t<5.9){h.r=-f*L(Math.PI/2,0,e3(seg(t,5.3,5.9)))}
  else{h.y=-Math.abs(Math.sin(t*7))*46;R.D.flap=1;R.D.speak=bump(t,6.2,6.6);snd("hp","boing",5.95);snd("sq","squawk",6.2)}}
 else{if(t<2.6){h.x=-f*L(W*.75,0,t/2.6);h.r=Math.sin(t*8)*.16;h.y=-Math.abs(Math.sin(t*8))*6;R.D.walk=1;R.D.flap=.3}
  else if(t<3.6){h.sx=Math.cos(seg(t,2.6,3.6)*TAU);snd("sp","spin",2.6)}
  else{h.y=-Math.abs(Math.sin(t*Math.PI*2))*10;h.r=Math.sin(t*Math.PI*2)*.06;R.D.flap=.5;R.spark=1;snd("tw","sparkle",3.7)}}
 R.front=function(){var p=heroPx(R.h);if(R.snow)burst(p.x,K.ay,2.9,14,200,["#fff","#dff3ff"],.8,300,7);if(R.spark)sparkles(p.x,p.y-K.hb.h*.5,K.hb.w*.8,t)};
 R.lying=Math.abs(h.r)>1;return R};

/* ---- jelly: monsters (blink lots of eyes, wobble, chomp) ---- */
KINDS.jelly=function(t,silly){if(!silly){var R0=KINDS.walk(t,false);R0.scene=K.M.plan.scene||"stage";return R0}
 var R={h:st({}),D:{speak:0,walk:0,wagRate:1.5},scene:K.M.plan.scene==="stage"?"party":(K.M.plan.scene||"party")},h=R.h;
 if(t<1){h.y=-L(K.ay+60,0,seg(t,0,1)*seg(t,0,1))}
 else if(t<2.2){var d=Math.exp(-(t-1)*3);h.sy=1-.4*Math.cos((t-1)*18)*d;h.sx=1/h.sy;snd("sp","thud",1)}
 else if(t<4.6){var u=(t-2.2)*1.2,ph=u%1,side=Math.floor(u)%2;h.x=(side?L(W*.25,-W*.25,ph):L(-W*.25,W*.25,ph));h.y=-Math.sin(ph*Math.PI)*220;snd("b"+Math.floor(u),"boing",2.2+Math.floor(u)/1.2+.01)}
 else if(t<5.6){var u2=seg(t,4.6,5.6);h.sy=1+Math.sin(u2*Math.PI)*.6;h.sx=1-Math.sin(u2*Math.PI)*.3;snd("tt","toot",5.3);R.D.speak=bump(t,5.2,5.6)}
 else{h.sy=1+Math.sin(t*12)*.12;h.sx=1-Math.sin(t*12)*.1;R.D.speak=Math.abs(Math.sin(t*6));snd("g","munch",5.7)}
 R.blinks=[2.3,2.6,4.7,6.2];R.front=function(){};return R};

/* ---- robot ---- */
KINDS.robot=function(t,silly){var R={h:st({}),D:{speak:0,walk:0,glow:.5+.5*Math.sin(t*Math.PI)},scene:silly?"party":"stage"},h=R.h;
 if(silly){var stp=Math.floor(t*3);if(t<4){h.r=[0,.25,0,-.25][stp%4];h.x=[0,30,0,-30][stp%4];R.D.walk=1;R.D.robo=stp%4;if(stp%2===0)snd("r"+stp,"robo",stp/3+.01)}
  else if(t<5.4){h.x=Math.sin(t*60)*8;h.r=Math.sin(t*40)*.1;snd("bz","wiggle",4);R.sparks=1;R.D.glow=Math.floor(t*2)%2}
  else if(t<5.9){h.sy=L(1,.75,seg(t,5.4,5.9));h.r=.5*seg(t,5.4,5.9);R.D.glow=0}
  else{h.sy=L(.75,1,e3(seg(t,5.9,6.4)));h.r=L(.5,0,e3(seg(t,5.9,6.4)));if(t>6.4){snd("ok","robo",6.4);h.y=-Math.abs(Math.sin(t*6))*40;R.D.glow=1}}}
 else{var s2=Math.floor(t*2);h.x=[0,50,0,-50][s2%4];h.r=[0,.1,0,-.1][s2%4];h.y=-(s2%2?20:0);R.D.walk=1;R.D.robo=s2%4;if(t>5)R.spark=1;snd("b"+s2,"bass",s2/2+.01);if(s2%4===0)snd("rb"+s2,"robo",s2/2+.02)}
 R.D.speak=R.D.robo===1||R.D.robo===3?1:0;
 R.front=function(){var p=heroPx(R.h);if(R.sparks){burst(p.x,p.y-K.hb.h*.7,4.2,16,240,["#ffc531","#ff9a52"],.6,200,5);burst(p.x,p.y-K.hb.h*.5,4.8,16,240,["#ffc531","#ff9a52"],.6,200,5)}if(R.spark)sparkles(p.x,p.y-K.hb.h*.5,K.hb.w*.8,t)};
 return R};

/* ---- spin: an object (key) ---- */
KINDS.spin=function(t,silly){var R={h:st({}),D:{},scene:silly?"party":"stage"},h=R.h;
 if(silly){if(t<3){h.sx=Math.cos(t*14);h.y=-Math.sin(seg(t,0,3)*Math.PI)*150;h.x=Math.sin(t*3)*120;snd("sp","spin",0)}else if(t<4.4){h.r=Math.sin(t*10)*.4;h.y=Math.sin(t*20)*10;R.dizzy=1}else{h.r=seg(t,4.4,5)*Math.PI/2;snd("ck","click",5);if(t>5.1){snd("ch","cheer",5.1);R.conf=1}}}
 else{h.sx=Math.cos(t*2.2);h.y=Math.sin(t*1.5)*20;R.glowR=1;snd("tw","twinkle",.3);snd("tw2","sparkle",5)}
 R.back=function(){if(R.glowR){var p=heroPx(R.h);X.globalAlpha=.3;X.fillStyle="#ffe58a";X.beginPath();X.arc(p.x,p.y-K.hb.h*.5,K.hb.h*.62,0,7);X.fill();X.globalAlpha=1}};
 R.front=function(){var p=heroPx(R.h);if(R.glowR)sparkles(p.x,p.y-K.hb.h*.5,K.hb.h*.6,t,8);if(R.dizzy)dizzy(p.x,p.y-K.hb.h-10,t,60);if(R.conf)confettiRain(t,5.1)};
 return R};

/* ---- sun ---- */
KINDS.sun=function(t,silly){var R={h:st({}),D:{speak:0,spinT:silly?(t<2?t:t<4?2+(t-2)*5:12+(t-4)):t},scene:"sky"},h=R.h;h.y=L(H*.62,0,e3(t/2));
 if(silly){if(t>2&&t<4){snd("sp","spin",2)}else if(t>=4&&t<6){h.y=-Math.abs(Math.sin(t*6))*90;snd("b"+Math.floor(t*6/Math.PI),"boing",Math.floor(t*6/Math.PI)*Math.PI/6+.01)}else if(t>=6){h.sx=1+Math.sin(t*10)*.08;h.sy=1-Math.sin(t*10)*.08;R.D.speak=1;snd("g","wiggle",6)}}
 else{R.glowR=1;if(t>2)R.spark=1;snd("tw","twinkle",.4);R.D.speak=bump(t,4,5)}
 R.back=function(){if(R.glowR){var p=heroPx(R.h);var gl=1+Math.sin(t*2)*.05;X.globalAlpha=.35;X.fillStyle="#fff3b0";X.beginPath();X.arc(p.x,p.y-K.hb.h*.5,K.hb.h*.7*gl,0,7);X.fill();X.globalAlpha=1}};
 R.front=function(){var p=heroPx(R.h);if(R.spark)sparkles(p.x,p.y-K.hb.h*.5,K.hb.h*.7,t,8)};
 return R};

/* ---- grow: a flower growing up out of the ground ---- */
KINDS.grow=function(t,silly){var R={h:st({}),D:{wind:1,speak:0},scene:"meadow"},h=R.h,g=e3(t/1.6);h.sy=g<1?g*(1+.2*Math.sin(g*Math.PI)):1;snd("gr","grow",.05);
 if(silly){h.r=t>2?Math.sin(t*5)*.3*(t<5?1:.4):0;R.D.wind=t>2&&t<5?4:1;if(t>2)snd("wd","whoosh",2);snd("sn","burp",5.2);R.petals=t>5.3;if(t>6.2)h.sy=1+Math.sin(t*12)*.08}
 else{h.r=Math.sin(t*1.4)*.05;if(t>2)R.spark=1;snd("tw","sparkle",2);R.bee=t>2.4}
 R.front=function(){var p=heroPx(R.h),top=p.y-K.hb.h*.82;if(R.petals)burst(p.x,top,5.3,18,260,["#ffc531","#ff9a52"],1.2,200,9);if(R.spark)stream(2,7.6,1.5,function(i,a){if(a<2.5)star(p.x+(i%2?-1:1)*(80+a*60),top-a*80,8,"#ffc531",1-a/2.5)});
  if(R.bee){var bx=p.x+Math.cos(t*2.2)*K.hb.w*.6,by=top+Math.sin(t*4.4)*40;X.fillStyle="#ffc531";X.beginPath();X.ellipse(bx,by,12,8,0,0,7);X.fill();X.fillStyle="#081130";X.fillRect(bx-3,by-8,3,16);X.fillRect(bx+4,by-7,3,14);X.fillStyle="rgba(255,255,255,.85)";X.beginPath();X.ellipse(bx-2,by-10,6,4,-.4+Math.sin(t*40)*.4,0,7);X.fill()}};
 return R};

/* ---- house: buildings. Silly: it hops. Cool: night falls, windows light up, door opens, fireworks. ---- */
KINDS.house=function(t,silly){var o=K.M.opt,R={h:st({}),D:{glow:0,wind:1},scene:K.M.plan.scene||"garden"},h=R.h,ch=pointPx("chimney");
 if(silly){var hp=(t%.9)/.9;if(t<3){h.y=-Math.sin(hp*Math.PI)*70;h.sy=hp<.12||hp>.9?.86:1.04;h.sx=1/h.sy;h.x=Math.sin(t*2)*60;snd("h"+Math.floor(t/.9),"thud",Math.floor(t/.9)*.9+.01)}
  else if(t<4.4){var u=seg(t,3,4.4);h.y=-Math.sin(u*Math.PI)*260;h.r=Math.sin(u*Math.PI)*.4;snd("wh","whoosh",3);snd("cr","thud",4.35)}
  else if(t<5.6){h.r=Math.sin(t*12)*.08;h.sx=1+Math.sin(t*24)*.04;snd("g","wiggle",4.4)}
  else{h.sy=1+Math.sin(t*9)*.06;R.conf=1;snd("ch","cheer",5.6)}
  R.D.door=bump(t,5.6,7.4)}
 else{R.night=Math.min(1,t/2.4);R.D.glow=cl((t-1.6)/.8);R.D.door=e3(seg(t,2.6,3.2))*(1-e3(seg(t,6.6,7.2)));R.fw=1;R.D.wind=1.5}
 R.back=function(){if(!silly){garden(t,R.night);var p=heroPx(R.h);X.globalAlpha=.25*R.D.glow;X.fillStyle="#ffe58a";X.beginPath();X.arc(p.x,p.y-K.hb.h*.5,K.hb.h*.65,0,7);X.fill();X.globalAlpha=1}};
 if(!silly)R.scene="none";
 R.front=function(){var p=heroPx(R.h);if(ch){var c=heroPoint(R.h,ch);smoke(c.x,c.y,0,7.6,3,.2)}
  if(R.fw)[3,4.2,5.4,6.4].forEach(function(b,i){burst(80+hsh(i,41)*(W-160),140+hsh(i,42)*180,b,22,220,[["#ffc531","#e5484d"],["#2a8fd6","#fff"],["#2fb344","#ffc531"],["#e5484d","#fff"]][i],1.4,80,5);snd("fw"+i,"pop",b)});
  if(R.conf)confettiRain(t,5.6)};
 return R};

/* ---- food: cake, burger, ice cream, milkshake, apple ---- */
KINDS.food=function(t,silly){var o=K.M.opt,fd=o.food||"cake",R={h:st({}),D:{speak:0,chomp:0,flame:1},scene:silly?"party":"table"},h=R.h;
 if(silly){if(t<1){var u=seg(t,0,1);h.y=-L(K.ay+40,0,u*u)}else if(t<2.2){var d=Math.exp(-(t-1)*3);h.sy=1-.35*Math.cos((t-1)*18)*d;h.sx=1/h.sy;snd("pl","thud",1)}
  else if(t<3.6){var hp=((t-2.2)%.7)/.7;h.y=-Math.sin(hp*Math.PI)*110;snd("b"+Math.floor((t-2.2)/.7),"boing",2.2+Math.floor((t-2.2)/.7)*.7+.01)}
  else if(t<4.6){h.r=seg(t,3.6,4.6)*TAU;h.y=-Math.sin(seg(t,3.6,4.6)*Math.PI)*160;snd("sp","spin",3.6)}
  else{h.sx=1+Math.sin(t*14)*.06;h.sy=1-Math.sin(t*14)*.06;R.conf=1;snd("bp","burp",5.2);snd("ch","munch",6.4);R.D.chomp=Math.abs(Math.sin(t*7))*(t>5?1:0)}}
 else{h.y=-L(K.ay+40,0,e3(t/1.4));if(t>1.4){h.sx=Math.cos((t-1.4)*1.8);R.spark=1;snd("tw","twinkle",1.5)}
  if(fd==="cake"){h.sx=1;R.D.flame=t<4.2?1:0;if(t>=4.2&&t<4.5)snd("bl","blow",4.2);if(t>4.4){R.smk=1}if(t>5.2){R.conf=1;snd("hb","cheer",5.2)}}
  if(fd==="burger"){h.sx=1;R.D.chomp=t>2.4&&t<5?Math.abs(Math.sin((t-2.4)*6)):0;if(t>2.4)snd("mn","munch",2.4);if(t>3.6)snd("mn2","munch",3.6)}
  if(fd==="milkshake"){h.sx=1;R.slurp=t>2.4&&t<4.6;if(R.slurp)snd("sl","slurp",2.4)}
  if(fd==="icecream"){h.sx=1;R.drip=t>2.6;R.D.wob=1}}
 R.back=function(){if(!silly){X.fillStyle="#e9edf2";var p=heroPx(R.h);X.beginPath();X.ellipse(K.ax,K.ay+4,K.hb.w*.62,24,0,0,7);X.fill();X.fillStyle="#cfd5de";X.fillRect(K.ax-K.hb.w*.62,K.ay+4,K.hb.w*1.24,12)}};
 R.front=function(){var p=heroPx(R.h);if(R.spark)sparkles(p.x,p.y-K.hb.h*.5,K.hb.w*.8,t);
  if(R.smk){(o.flames||[]).forEach(function(nm,i){var q=pointPx(nm);if(q){var c=heroPoint(R.h,q);smoke(c.x,c.y,4.4,6.4,6,.1,"#e9edf2",5)}})}
  if(R.slurp){var sp2=pointPx("straw");if(sp2){var c2=heroPoint(R.h,sp2);bubbles(c2.x,c2.y,2.4,4.6,5)}}
  if(R.drip){var dp=pointPx("drip");if(dp){var c3=heroPoint(R.h,dp);var a=((t-2.6)%1.6);if(a<1.2){X.fillStyle=o.dripColor||"#faa2c1";X.beginPath();X.ellipse(c3.x,c3.y+a*a*180,6,8,0,0,7);X.fill()}}}
  if(R.conf)confettiRain(t,silly?4.6:5.2)};
 return R};

/* ---- apple-style: a single round object that bonks, bounces and rolls ---- */
KINDS.roll=function(t,silly){var R={h:st({}),D:{wind:1},scene:silly?"meadow":"table"},h=R.h,cx=0,rd=Math.max(40,Math.min(W*.3,W*.5-K.hb.w*.5-12));
 if(silly){if(t<1){var u=seg(t,0,1);h.y=-L(K.ay+40,0,u*u);snd("bk","thud",.97)}else if(t<2.2){h.y=-Math.abs(Math.sin((t-1)*6))*120*Math.exp(-(t-1)*1.6);snd("bo","boing",1.05)}
  else if(t<4.4){h.x=L(0,rd,eio(seg(t,2.2,3.3)))-L(0,2*rd,eio(seg(t,3.3,4.4)));h.r=h.x/(K.hb.w*.5)}else if(t<5.6){h.x=-rd+L(0,rd,eio(seg(t,4.4,5.6)));h.r=h.x/(K.hb.w*.5)}
  else{h.sx=1+Math.sin(t*14)*.06;h.sy=1-Math.sin(t*14)*.06;snd("ch","munch",5.7)}}
 else{h.y=-L(K.ay+40,0,e3(t/1.4));if(t>1.4){h.sx=Math.cos((t-1.4)*1.8);R.spark=1;snd("tw","twinkle",1.5)}}
 R.back=function(){if(!silly){X.fillStyle="#e9edf2";X.beginPath();X.ellipse(K.ax,K.ay+4,K.hb.w*.62,24,0,0,7);X.fill()}};
 R.front=function(){var p=heroPx(R.h);if(R.spark)sparkles(p.x,p.y-K.hb.h*.5,K.hb.w*.8,t)};
 R.anchorC=1;return R};

/* ---- scene: a whole picture with its own background (lighthouse, moon base). Nothing leaves; parts move in place. ---- */
KINDS.scene=function(t,silly){var o=K.M.opt,R={h:st({}),D:{night:0,glow:0,wind:silly?2:1,beam:1,walk:1,speak:0},scene:"own",frame:1},lp=pointPx("lamp");
 if(silly){R.D.speed=2.2;if(t>2.5&&t<4){R.h.x=Math.sin(t*40)*4*bump(t,2.5,4);snd("sh","rumble",2.5)}R.D.glow=Math.floor(t*1.5)%2?1:.3;if(t>5)R.conf=1;snd("hk","honk",1);snd("ch","cheer",5)}
 else{R.D.night=o.noNight?0:cl((t-.5)/2.5);R.D.glow=cl((t-1.5)/1);R.D.speed=1;snd("tw","twinkle",1.5);if(t>5)R.spark=1}
 R.front=function(){if(lp&&(o.beam||lp)){var q=basePoint(lp);var ang=(silly?t*2.4:Math.sin(t*1.2)*1.1)+Math.PI;var a=silly?.45:.45*R.D.glow;beam(q.x,q.y,ang,W*1.3,.16,a);beam(q.x,q.y,ang+Math.PI,W*1.3,.16,a)}
  if(R.conf)confettiRain(t,5);if(R.spark)sparkles(W/2,H*.4,W*.38,t,8)};
 return R};

/* ---------- placement and helpers that need the model ---------- */
function heroPx(h){return{x:K.ax+h.x,y:K.ay+h.y}}
function pointPx(name){var p=K.M.points[name];return p?{u:p[0],v:p[1]}:null}
function basePoint(p){return{x:K.X0+p.u*K.s,y:K.Y0+p.v*K.s}}
function heroPoint(h,p){/* a point on the hero after the hero's move */var x=K.X0+p.u*K.s-K.ax,y=K.Y0+p.v*K.s-K.ay;var c=Math.cos(h.r),s=Math.sin(h.r);x*=h.sx;y*=h.sy;return{x:K.ax+h.x+x*c-y*s,y:K.ay+h.y+x*s+y*c}}

/* reactions: still parts dip and wobble when the hero takes off or lands on them */
function reactions(M,R){var out={};M.roots.forEach(function(r){if(r.role==="hero"||!r.react)return;var dy=0,rot=0;(R.kicks||[]).forEach(function(k){var a=T-k[0];if(a<0||a>2.4)return;var e=Math.exp(-a*3)*Math.sin(a*14)*(k[1]||1);dy+=e*(r.react.amp||2.2);rot+=e*(r.react.rot||1.5)*DEG});
  var pv=r.react.pivot||r.pivot||[r.bb.x+r.bb.w,r.bb.y+r.bb.h/2];out[r.id]=about(pv[0],pv[1],{r:rot,sx:1,sy:1,tx:0,ty:dy})});return out}

function hexRGB(c){if(!c||typeof c!=="string")return null;var m=c.trim().match(/^#?([0-9a-f]{3}|[0-9a-f]{6})$/i);if(!m)return null;var x=m[1];if(x.length===3)x=x.replace(/./g,function(ch){return ch+ch});return[parseInt(x.slice(0,2),16),parseInt(x.slice(2,4),16),parseInt(x.slice(4,6),16)]}
function cdist(a,r,g,b){return Math.abs(a[0]-r)+Math.abs(a[1]-g)+Math.abs(a[2]-b)}
/* ---------- photo of the child's drawing: line it up with the plan and split it into the same parts ---------- */
var SPLIT=typeof WeakMap!=="undefined"?new WeakMap():null;
function splitPhoto(M,canvas){if(SPLIT&&SPLIT.has(canvas)){var c0=SPLIT.get(canvas);return c0&&c0.key===M.key?c0:null}var res=null;try{res=doSplit(M,canvas)}catch(e){res=null}if(SPLIT)SPLIT.set(canvas,res);return res}
function doSplit(M,canvas){var W0=canvas.width,H0=canvas.height,k=Math.min(1,520/Math.max(W0,H0)),w=Math.max(8,Math.round(W0*k)),h=Math.max(8,Math.round(H0*k));
 var c=document.createElement("canvas");c.width=w;c.height=h;var g=c.getContext("2d",{willReadFrequently:true});g.drawImage(canvas,0,0,w,h);var D=g.getImageData(0,0,w,h),dd=D.data;
 /* ink bbox of the photo */var x0=w,y0=h,x1=-1,y1=-1,N=w*h,i;for(i=0;i<N;i++)if(dd[i*4+3]>40){var x=i%w,y=(i/w)|0;if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y}if(x1<0)return null;
 var B=M.bb,pw=x1-x0+1,ph=y1-y0+1;/* map photo px -> units (stretch box to box) */var su=B.w/pw,sv=B.h/ph;
 /* part masks in photo pixels */var nP=M.parts.length,own=new Int16Array(N).fill(-1);var lab=[];M.parts.forEach(function(pt,pi){var mc=document.createElement("canvas");mc.width=w;mc.height=h;var mg=mc.getContext("2d",{willReadFrequently:true});
   mg.setTransform(1/su,0,0,1/sv,x0-B.x/su,y0-B.y/sv);mg.fillStyle="#000";mg.strokeStyle="#000";mg.lineCap="round";mg.lineJoin="round";pt.fills.forEach(function(f){fillIt(mg,f,"#000")});pt.lines.forEach(function(l){mg.lineWidth=(l.w||1.4)*.6+3*su;mg.stroke(pth(l.d))});
   lab.push(mg.getImageData(0,0,w,h).data)});
 /* score: how much of the photo ink lands on the plan, and the other way round */var inkN=0,hit=0;
 for(i=0;i<N;i++){if(dd[i*4+3]<=40)continue;var real=dd[i*4]+dd[i*4+1]+dd[i*4+2]<690;if(real)inkN++;for(var p=nP-1;p>=0;p--)if(lab[p][i*4+3]>20){own[i]=p;if(real)hit++;break}}
 var planN=0,planHit=0;for(i=0;i<N;i+=2){var any=false;for(var p2=0;p2<nP;p2++)if(lab[p2][i*4+3]>20){any=true;break}if(any){planN++;if(dd[i*4+3]>40&&dd[i*4]+dd[i*4+1]+dd[i*4+2]<690)planHit++}}
 var score=M.raster?Math.max(0,1-2*Math.abs(Math.log((pw/ph)/(B.w/B.h)))):Math.min(hit/Math.max(1,inkN),planHit/Math.max(1,planN));if(score<.3)return{key:M.key,fail:true,score:score};
 /* unassigned ink goes to the nearest part (multi-source spread) */var q=[],dist=new Int32Array(N).fill(1e9);for(i=0;i<N;i++)if(own[i]>=0){q.push(i);dist[i]=0}
 for(var hd=0;hd<q.length;hd++){var cur=q[hd],cx=cur%w,cy=(cur/w)|0,nb=[cx>0?cur-1:-1,cx<w-1?cur+1:-1,cy>0?cur-w:-1,cy<h-1?cur+w:-1];for(var n=0;n<4;n++){var j=nb[n];if(j>=0&&dist[j]>dist[cur]+1){dist[j]=dist[cur]+1;own[j]=own[cur];q.push(j)}}}
 /* layers: each part keeps its own pixels; a part that moves leaves the parent's colour behind */var layers=M.parts.map(function(pt,pi){var lc=document.createElement("canvas");lc.width=w;lc.height=h;var lg=lc.getContext("2d");var L2=lg.createImageData(w,h),ld=L2.data;for(var a=0;a<N;a++)if(own[a]===pi&&dd[a*4+3]>8){ld[a*4]=dd[a*4];ld[a*4+1]=dd[a*4+1];ld[a*4+2]=dd[a*4+2];ld[a*4+3]=dd[a*4+3]}lg.putImageData(L2,0,0);return lc});
 M.parts.forEach(function(pt,pi){if(!pt.under||!pt.parent)return;var par=M.by[pt.parent];if(!par)return;var pj=M.parts.indexOf(par),want=hexRGB(typeof pt.under==="string"?pt.under:pt.under.color);var r=0,gg=0,b=0,n2=0;
   for(var a=0;a<N;a++){if(own[a]!==pi)continue;[a-1,a+1,a-w,a+w].forEach(function(nb2){if(nb2<0||nb2>=N||own[nb2]!==pj||dd[nb2*4+3]<=40)return;var R0=dd[nb2*4],G0=dd[nb2*4+1],B0=dd[nb2*4+2];if(R0+G0+B0<200||R0+G0+B0>690)return;if(want&&cdist(want,R0,G0,B0)>150)return;r+=R0;gg+=G0;b+=B0;n2++})}
   var rr,g2,b2;if(n2>20){rr=Math.round(r/n2);g2=Math.round(gg/n2);b2=Math.round(b/n2)}else if(want){rr=want[0];g2=want[1];b2=want[2]}else return;
   var lg=layers[pj].getContext("2d");var im=lg.getImageData(0,0,w,h),id=im.data;for(var a2=0;a2<N;a2++)if(own[a2]===pi&&dd[a2*4+3]>40){id[a2*4]=rr;id[a2*4+1]=g2;id[a2*4+2]=b2;id[a2*4+3]=255}lg.putImageData(im,0,0)});
 /* what a moving part uncovers: filled from the child's own colours next to it, plus the missing outline (paper patches are not needed: the photo already has white paper) */
 var T0=[1/su,0,0,1/sv,x0-B.x/su,y0-B.y/sv];
 var pim=M.parts.map(function(pt,pi){var G={};pt.pf.concat(pt.pl).forEach(function(p){var by=p.by||(M.hero&&M.hero.id);if(!M.by[by])return;(G[by]||(G[by]={f:[],l:[]}))[p.fill?"f":"l"].push(p)});
  return Object.keys(G).map(function(by){var g2=G[by];function mask(extra){var mc=document.createElement("canvas");mc.width=w;mc.height=h;var mg=mc.getContext("2d",{willReadFrequently:true});mg.setTransform(T0[0],T0[1],T0[2],T0[3],T0[4],T0[5]);mg.fillStyle="#000";mg.strokeStyle="#000";mg.lineJoin="round";g2.f.forEach(function(p){fillIt(mg,p,"#000");if(extra){mg.lineWidth=extra*su;mg.stroke(pth(p.d))}});return mg.getImageData(0,0,w,h).data}
   var m0=g2.f.length?mask(0):null,m0d=g2.f.length?mask(6):null,m1=g2.f.length?mask(8):null,oc=document.createElement("canvas");oc.width=w;oc.height=h;var og=oc.getContext("2d");
   var want=g2.f.length?hexRGB(g2.f[0].fill):null;
   if(m0){var seeds=[];for(var a=0;a<N;a++)if(m1[a*4+3]>=20&&own[a]===pi&&dd[a*4+3]>40){var R1=dd[a*4],G1=dd[a*4+1],B1=dd[a*4+2],S1=R1+G1+B1;if(S1<200||S1>700)continue;if(want&&cdist(want,R1,G1,B1)>170)continue;seeds.push(a)}
    var OD=og.createImageData(w,h),od=OD.data,use=seeds.length>30;for(var b=0;b<N;b++){if(m0[b*4+3]<20&&!(m0d[b*4+3]>=20&&dd[b*4+3]>40&&own[b]!==pi))continue;var mine=own[b]===pi&&dd[b*4+3]>40;if(mine){var S2=dd[b*4]+dd[b*4+1]+dd[b*4+2];if(S2>=200&&S2<=700&&(!want||cdist(want,dd[b*4],dd[b*4+1],dd[b*4+2])<=170))continue}
     if(use){var sp=seeds[Math.floor(hsh(b,97)*seeds.length)];od[b*4]=dd[sp*4];od[b*4+1]=dd[sp*4+1];od[b*4+2]=dd[sp*4+2]}else if(want){od[b*4]=want[0];od[b*4+1]=want[1];od[b*4+2]=want[2]}else continue;od[b*4+3]=255}og.putImageData(OD,0,0)}
   og.setTransform(T0[0],T0[1],T0[2],T0[3],T0[4],T0[5]);og.strokeStyle="rgb(43,43,43)";og.lineCap="round";og.lineJoin="round";g2.l.forEach(function(p){og.lineWidth=(p.w||1.4)*.6;og.stroke(pth(p.d))});
   return{by:by,img:oc}})});
 /* units: layer pixel (px,py) -> unit (B.x+(px-x0)*su, ...) */
 var parts=M.parts.map(function(pt,pi){return Object.assign({},pt,{img:layers[pi],pimgs:pim[pi],ix:B.x-x0*su,iy:B.y-y0*sv,iw:w*su,ih:h*sv,kids:[],uf:[],pf:[],pl:[]})});var by={};parts.forEach(function(p){by[p.id]=p});parts.forEach(function(p){if(p.parent&&by[p.parent])by[p.parent].kids.push(p)});
 return{key:M.key,score:score,M:Object.assign({},M,{parts:parts,by:by,hero:M.hero?by[M.hero.id]:null,roots:parts.filter(function(p){return!p.parent||!by[p.parent]})})}}
function drawGlows(g,M,C,B,list){(list||painter(M,C)).forEach(function(e){if(!(e.glow>0)||e.pt.img)return;var T2=mul(B,e.m);g.save();g.setTransform(T2[0],T2[1],T2[2],T2[3],T2[4],T2[5]);g.globalCompositeOperation="lighter";g.globalAlpha=e.glow*.6;e.pt.fills.forEach(function(f){fillIt(g,f,e.gcol)});g.restore()})}
MIM.split=function(key,canvas){var M=model(key);return M?splitPhoto(M,canvas):null};

/* ---------- the frame ---------- */
function frame(ctx,w,h,t,once,mode,canvas,item,sound){var M=model(item.key);if(!M)return false;if(M.raster&&(item.src==="sample"||!canvas))return false;
 var useM=M,photo=false;
 if(item.src!=="sample"&&canvas){var sp=splitPhoto(M,canvas);if(sp&&!sp.fail){useM=sp.M;photo=true}else{/* photo doesn't match the plan: the whole photo moves as one */useM=wholePhoto(M,canvas);photo=true}}
 X=ctx;W=w;H=h;T=t;ONCE=once;S=sound||{};MODE=mode;var kind=KINDS[M.kind]?M.kind:"walk",pl=PLACE[kind]||PLACE.walk;
 var bb=useM.bb,box=(M.plan.size||1)*pl.box,s=Math.min(box/bb.w,(box*1.25)/bb.h,7);var X0=W/2-(bb.x+bb.w/2)*s,Y0=pl.gy?H*pl.gy-(bb.y+bb.h)*s:H*pl.cy-(bb.y+bb.h/2)*s;
 var hb=useM.hb||bb,anc=M.points.anchor||(pl.gy&&!pl.ac||kind==="perch"?[hb.x+hb.w/2,hb.y+hb.h]:[hb.x+hb.w/2,hb.y+hb.h/2]);if(kind==="perch"&&M.points.feet)anc=M.points.feet;
 K={M:useM,s:s,X0:X0,Y0:Y0,ax:X0+anc[0]*s,ay:Y0+anc[1]*s,gy:Y0+(hb.y+hb.h)*s,hb:{w:hb.w*s,h:hb.h*s},hbU:hb,anc:anc};useM.s=s;
 var R=KINDS[kind](t,mode==="silly");if(window.__pokeRx&&R.h){try{var rx=window.__pokeRx(t);if(rx){R.h.x+=rx.dx||0;R.h.y+=rx.dy||0;R.h.r+=rx.r||0;R.h.sx*=rx.sx||1;R.h.sy*=rx.sy||1}}catch(e){}}
 var AW=actWindow(mode==="silly"),shk=R.shake?bump(t,AW[0],AW[1]):0;if(shk){X.save();X.translate(W/2+Math.sin(t*57)*7*shk,H/2+Math.cos(t*43)*5*shk);X.scale(1.035,1.035);X.translate(-W/2,-H/2)}else shk=0;
 /* scene */var sc=R.scene;if(sc&&sc!=="none"){var fn=SCENES[sc]||SCENES.sky;fn(t,R.sp||0)}if(R.back)R.back();
 if(R.frame||sc==="own"){X.save();var fx=X0+bb.x*s-14,fy=Y0+bb.y*s-14,fw=bb.w*s+28,fh=bb.h*s+28;X.fillStyle="#fffef9";X.shadowColor="rgba(8,17,48,.18)";X.shadowBlur=18;X.fillRect(fx,fy,fw,fh);X.restore()}
 var framed=!!(R.frame||sc==="own");if(framed&&useM.hero){var hx0=X0+hb.x*s,hx1=X0+(hb.x+hb.w)*s,hy0=Y0+hb.y*s,hy1=Y0+(hb.y+hb.h)*s,fx0=X0+bb.x*s-8,fx1=X0+(bb.x+bb.w)*s+8,fy0=Y0+bb.y*s-8,fy1=Y0+(bb.y+bb.h)*s+8;R.h.x=soft(R.h.x,fx0-hx0,fx1-hx1);R.h.y=soft(R.h.y,fy0-hy0,fy1-hy1)}
 /* hero matrix in unit space */var hS=R.h,au=anc[0],av=anc[1];var HM=mul([1,0,0,1,au+hS.x/s,av+hS.y/s],mul([Math.cos(hS.r),Math.sin(hS.r),-Math.sin(hS.r),Math.cos(hS.r),0,0],mul([hS.sx,0,0,hS.sy,0,0],[1,0,0,1,-au,-av])));
 var D=R.D||{};var rus=0;(R.kicks||[]).forEach(function(k){var a=t-k[0];if(a>=0&&a<2.2)rus+=Math.exp(-a*2.2)*(k[1]||1)});D.rustle=rus;var C={t:t,mode:mode,D:D,HM:HM,blinks:R.blinks,dist:((hS.x+(R.roll||0))/s),react:reactions(useM,R),dpr:1,glowLater:!!(R.frame||sc==="own")};
 if(D.wind==null)D.wind=1;
 if(R.frame||sc==="own"){X.save();X.beginPath();X.rect(X0+bb.x*s-14,Y0+bb.y*s-14,bb.w*s+28,bb.h*s+28);X.clip()}
 var gnd=pl.gy&&kind!=="sail"&&kind!=="scene"&&!R.frame&&!R.noShadow;if(gnd&&useM.hero&&hS.a!==0){X.fillStyle="rgba(8,17,48,.13)";var lift=Math.max(0,-hS.y);X.beginPath();X.ellipse(K.ax+hS.x,K.gy+4,Math.max(8,K.hb.w*.42*(1-lift/700)),Math.max(3,K.hb.w*.07*(1-lift/700)),0,0,7);X.fill()}
 drawFrameR(X,useM,C,[s,0,0,s,X0,Y0]);
 if(framed){if(D.night>0){X.fillStyle="rgba(11,16,53,"+(.62*D.night)+")";X.fillRect(0,0,W,H)}drawGlows(X,useM,C,[s,0,0,s,X0,Y0]);if(R.front)R.front();X.restore()}
 else if(R.front)R.front();
 if(shk)X.restore();
 return true}
function soft(v,lo,hi){if(v>0)return hi<=1?0:hi*Math.tanh(v/hi);if(v<0)return lo>=-1?0:lo*Math.tanh(v/lo);return 0}
function wholePhoto(M,canvas){if(SPLIT&&SPLIT.has(canvas)){var c0=SPLIT.get(canvas);if(c0&&c0.whole)return c0.whole}var B=M.bb,cw=canvas.width,ch=canvas.height,s=Math.min(B.w/cw,B.h/ch);var iw=cw*s,ih=ch*s;
 var hero={id:"all",role:"hero",img:canvas,ix:B.x+(B.w-iw)/2,iy:B.y+(B.h-ih),iw:iw,ih:ih,kids:[],uf:[],pf:[],pl:[],motion:[],bb:{x:B.x+(B.w-iw)/2,y:B.y+(B.h-ih),w:iw,h:ih}};
 var W2=Object.assign({},M,{parts:[hero],by:{all:hero},hero:hero,roots:[hero],hb:hero.bb,bb:hero.bb});if(SPLIT){var prev=SPLIT.get(canvas)||{};prev.whole=W2;SPLIT.set(canvas,prev)}return W2}

/* ---------- checks used by the app's Draw QA ---------- */
var KNOWN_MOTIONS={pose:1,flap:1,wag:1,sway:1,step:1,swing:1,bob:1,spin:1,blink:1,pulse:1,flicker:1,flutter:1,speak:1,chomp:1,open:1,extend:1,twinkle:1,drift:1,lift:1,sink:1,shake:1,glow:1,hide:1,show:1,nod:1,tilt:1,look:1};
MIM.check=function(key){var out=[],plan=planOf(key);function R(rule,pass,msg){out.push({rule:rule,pass:!!pass,msg:msg||""})}
 R("Has a Make it move plan (what is in the picture, which parts move and which stay still)",!!plan,plan?"":"no plan yet: review the picture and add one");if(!plan)return out;
 var M=model(key);R("The plan can be read",!!M,M?"":"plan has no parts");if(!M)return out;
 R("Plan says what the picture shows",!!(plan.seen&&plan.seen.length>20),plan.seen?"":"add 'seen': a short description of every thing in the picture");
 R("Every part name in the item lists is valid",!M.bad.length,M.bad.join(", "));
 R("No line or colour is given to two parts",!M.dups.length,M.dups.slice(0,12).join(", "));
 R("The kind of move is known",!!KINDS[M.kind],M.kind);
 var badM=[];M.parts.forEach(function(p){p.motion.forEach(function(m){if(!KNOWN_MOTIONS[m.type])badM.push(p.id+":"+m.type)});if(p.parent&&!M.by[p.parent])badM.push(p.id+": parent "+p.parent+" missing")});R("Every part motion is known",!badM.length,badM.join(", "));
 var badP=[];M.parts.forEach(function(p){if(p.pivot&&(p.pivot[0]<-10||p.pivot[0]>110||p.pivot[1]<-10||p.pivot[1]>110))badP.push(p.id)});R("Pivots are on the paper",!badP.length,badP.join(", "));
 R("There is a star part that moves (or it is a whole-picture scene)",!!M.hero||M.kind==="scene",M.hero?M.hero.id:"no hero");
 var empty=M.parts.filter(function(p){return!p.fills.length&&!p.lines.length&&!p.pf.length&&!p.pl.length}).map(function(p){return p.id});R("Every part has something in it",!empty.length,empty.join(", "));
 var diff=M.raster?0:homeDiff(M);R("At rest the parts look exactly like the finished drawing",diff<.01,(diff*100).toFixed(2)+"% of the drawing differs");
 return out};
function homeDiff(M){var a=document.createElement("canvas"),b=document.createElement("canvas");a.width=a.height=b.width=b.height=300;var ga=a.getContext("2d",{willReadFrequently:true}),gb=b.getContext("2d",{willReadFrequently:true});
 ga.fillStyle=gb.fillStyle="#fff";ga.fillRect(0,0,300,300);gb.fillRect(0,0,300,300);ga.setTransform(3,0,0,3,0,0);
 M.P.steps.forEach(function(st){st.add.forEach(function(it){if(it.fill)fillIt(ga,it)})});ga.strokeStyle=LINE;ga.lineCap="round";ga.lineJoin="round";M.P.steps.forEach(function(st){st.add.forEach(function(it){if(!it.fill)lineIt(ga,it)})});
 drawFrame(gb,M,{t:0,mode:"cool",D:{},HM:ID,blinks:null,dist:0,react:{},dpr:1,still:true},[3,0,0,3,0,0]);
 var da=ga.getImageData(0,0,300,300).data,db=gb.getImageData(0,0,300,300).data,n=0,ink=0;for(var i=0;i<da.length;i+=4){var sa=da[i]+da[i+1]+da[i+2],sb=db[i]+db[i+1]+db[i+2];if(sa<750||sb<750)ink++;if(Math.abs(da[i]-db[i])+Math.abs(da[i+1]-db[i+1])+Math.abs(da[i+2]-db[i+2])>90)n++}return n/Math.max(1,ink)}
MIM.homeDiff=function(key){var M=model(key);return M?homeDiff(M):1};
MIM.model=model;MIM.kinds=Object.keys(KINDS);MIM.motions=Object.keys(KNOWN_MOTIONS);MIM.scenes=Object.keys(SCENES);

/* connect to the Show player: replaces the first Make it move engine when a drawing has a plan */
var OLD=window.__mimAnim;
window.__mimAnim=function(ctx,w,h,t,once,mode,canvas,item,sound){if(item&&item.key&&planOf(item.key)){try{return frame(ctx,w,h,t,once,mode,canvas,item,sound)}catch(e){if(window.console)console.error(e)}}return OLD?OLD(ctx,w,h,t,once,mode,canvas,item,sound):false};
MIM.frame=frame;
/* ---------- 31 Oct 2026: living characters ----------
   MIM.live(ctx, canvas, item, x, y, w, h, opt) draws a make exactly where ctx.drawImage(canvas, x, y, w, h) would, but
   split into the drawing's own parts, each doing its gentle repeating motion: eyes blink, tails wag, plants sway,
   wings flap while it is moved through the air, legs step while it moves along, wheels turn with the distance it
   travels, and the mouth or beak opens with opt.talk (0..1, the voice level). Returns false when the drawing has no
   plan or the child's photo doesn't line up with it well (a stricter match than Silly/Cool, as it runs everywhere);
   the caller then draws the flat picture as before. */
var LIVEST=typeof WeakMap!=="undefined"?new WeakMap():null;
MIM.live=function(g,canvas,item,dx,dy,dw,dh,o){o=o||{};
 if(!item||!item.key||!canvas||!dw||!dh||!planOf(item.key))return false;
 var M=model(item.key);if(!M)return false;
 var U,Bl,vec=item.src==="sample";if(vec&&M.raster)return false;
 if(vec){/* a "Try one" sample: the clean drawing itself, placed exactly where the Show's sample picture sits */
  var sb=sampleBox(item.key,M);if(!sb)return false;var kx=dw/canvas.width,ky=dh/canvas.height;U=M;Bl=[6*kx,0,0,6*ky,dx-sb[0]*kx,dy-sb[1]*ky]}
 else{/* the child's photo, split into the same parts (the photo must line up with the plan well enough) */
  var sp=splitPhoto(M,canvas);if(!sp||sp.fail||!sp.M||!(sp.score>=.5))return false;U=sp.M;var p0=U.parts[0];if(!p0||!p0.iw||!p0.ih)return false;
  var sx=dw/p0.iw,sy=dh/p0.ih;Bl=[sx,0,0,sy,dx-p0.ix*sx,dy-p0.iy*sy]}
 var Mc=[1,0,0,1,0,0];
 if(!g.getTransform)return false;try{var Tm=g.getTransform();Mc=[Tm.a,Tm.b,Tm.c,Tm.d,Tm.e,Tm.f]}catch(e){return false}
 var B=mul(Mc,Bl),bx=M.bb.x+M.bb.w/2,by=M.bb.y+M.bb.h/2,cx=B[0]*bx+B[2]*by+B[4],cy=B[1]*bx+B[3]*by+B[5];
 var now=o.t!=null?o.t:performance.now()/1000,s=LIVEST?LIVEST.get(canvas):null;
 if(!s){s={x:cx,y:cy,t:now,vx:0,vy:0,dist:0};if(LIVEST)LIVEST.set(canvas,s)}
 var dt=now-s.t,ux=Math.abs(B[0])>1e-3?B[0]:(B[0]<0?-1e-3:1e-3);
 if(dt>0&&dt<.25){var k=Math.min(1,dt*9);s.vx+=((cx-s.x)/dt-s.vx)*k;s.vy+=((cy-s.y)/dt-s.vy)*k;s.dist+=(cx-s.x)/ux+(o.roll?o.roll*dt/ux:0)}
 else if(dt!==0){s.vx=0;s.vy=0}
 s.x=cx;s.y=cy;s.t=now;
 var sp2=Math.sqrt(s.vx*s.vx+s.vy*s.vy),kind=M.kind,D={};
 D.flap=cl((sp2-60)/220);if(kind==="fly"&&vec)D.flap=Math.max(D.flap,.55);
 D.walk=cl((Math.abs(s.vx)-30)/150);if(o.flap)D.flap=Math.max(D.flap,cl(o.flap));if(o.walk)D.walk=Math.max(D.walk,cl(o.walk));
 D.speak=cl(o.talk||0);D.wind=1;D.swim=1;D.flame=.6;
 var C={t:now,mode:"live",live:true,D:D,HM:ID,blinks:null,dist:s.dist,react:{},dpr:1,alpha:g.globalAlpha};
 drawFrameR(g,U,C,B);return true};
/* where the Show's sample picture of a drawing starts, in its 600 x 600 drawing (the same trim the Show does: ink box minus 8 px) */
var SBOX={};
function sampleBox(key,M){if(SBOX[key])return SBOX[key];try{var c=document.createElement("canvas");c.width=c.height=600;var x=c.getContext("2d",{willReadFrequently:true}),lines=[];x.scale(6,6);x.lineCap="round";x.lineJoin="round";
 M.P.steps.forEach(function(st){(st.add||[]).forEach(function(a){if(a.fill){x.fillStyle=a.fill;x.fill(new Path2D(a.d+" "+(a.cut||[]).join(" ")),"evenodd")}else lines.push(a)})});x.strokeStyle="#1c1c1c";lines.forEach(function(a){x.lineWidth=a.w||1.2;x.stroke(new Path2D(a.d))});
 var d=x.getImageData(0,0,600,600).data,a0=600,b0=600,e=0,f=0;for(var y=0;y<600;y+=2)for(var X2=0;X2<600;X2+=2){if(d[(y*600+X2)*4+3]>20){if(X2<a0)a0=X2;if(X2>e)e=X2;if(y<b0)b0=y;if(y>f)f=y}}
 if(e<=a0||f<=b0)return null;SBOX[key]=[a0-8,b0-8];return SBOX[key]}catch(err){return null}}
/* get a make ready ahead of time (the Show calls this while it shows its loading dots): split a photo into parts,
   or make the part pictures of a clean drawing */
MIM.prep=function(item,canvas){try{if(item&&item.key&&canvas&&planOf(item.key)){var M=model(item.key);if(!M)return;if(item.src==='sample')rasterOf(M,7);else splitPhoto(M,canvas)}}catch(e){}};
MIM.has=function(item){try{return!!(item&&item.key&&planOf(item.key))}catch(e){return false}};

})();
/* 24 Oct 2026: built-in QA. The app's Draw checker (SBE.validate) also checks the Make it move plan, so a new drawing
   cannot pass QA until its picture has been reviewed and given a plan (as "anim" in its project data, or MIM.reg). */
(function(){
function keyOf(P){try{var L=(window.REALS&&REALS.draw)||[];for(var i=0;i<L.length;i++){var k=L[i].key,o=null;try{o=DX.get(k)}catch(e){}if(o&&(o===P||(o.id===P.id&&o.title===P.title)))return k}}catch(e){}return null}
function hook(){var B=null;try{B=SBE}catch(e){}if(!B||!B.validate||B.validate.__mim)return!!(B&&B.validate&&B.validate.__mim);var ov=B.validate;
 B.validate=function(m){var R=ov.apply(this,arguments);try{if(m&&m.kind==="draw"){var k=keyOf(m);R=(R||[]).concat(k?MIM.check(k):[{rule:"Has a Make it move plan (what is in the picture, which parts move and which stay still)",pass:false,msg:"drawing not registered yet: review the picture and add its plan"}])}}catch(e){}return R};B.validate.__mim=1;return true}
if(!hook()){setTimeout(hook,800);setTimeout(hook,2200)}
MIM.keyOf=keyOf;
})();
