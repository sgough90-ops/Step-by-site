/* 16 Nov 2026: Make a book (on the Grown-ups page, behind the gate).
   A hardcover book of the child's own drawings from My drawings: a front cover with their name and a cover drawing,
   one drawing on every page ("A is for Ant" under it) and a back cover with every drawing and the Step by Draw logo.
   Four screens: 1 pick the book (a set from My drawings, or all of them), 2 check the drawings (tap to leave one out,
   or to pick another photo of the same letter), 3 the child's name, cover colour and cover drawing, 4 preview.
   Then Make the PDF: the whole book is drawn here on the device (no server) and saved as one print-ready PDF.

   Made for Peecho's hardcover book, 21 x 21 cm, following their hardcover file guide (Nov 2026):
   - one PDF with the front cover, the pages and the back cover, each a single page, in that order
   - no bleed or cut marks (Peecho adds them), so backgrounds run to the edges and words and faces stay 12 mm in
   - at least 24 pages counting both covers, and an even number (an odd count leaves the back cover white), so a book
     with an odd number of drawings gets a The End page before the back cover
   - 300 dpi, RGB
   A whole A to Z set is 28 pages: front cover, 26 drawings, back cover. 21 drawings is the smallest printable book.

   TESTING: the Make the PDF button is for checking the books until ordering through Peecho is added. Before launch
   parents should press Order instead (with the PDF itself they could print the book anywhere): set PDF_BUTTON to false.
   Photos never leave this device. */
(function(){
'use strict';
var G=function(i){return document.getElementById(i)};
function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;')}
var NAVY='#081130',CREAM='#FFF8E7',GREY='#6b7079';
var FONT='"Arial Rounded MT Bold","Arial Rounded MT",-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif';
var UIFONT='-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif';
var PDF_BUTTON=true;
var MM=210,DPI=300,PX=Math.round(MM/25.4*DPI),MINPAGES=24,THUMB=420;
var COLS=[{c:'#FFC531',n:'Yellow'},{c:'#E5392B',n:'Red'},{c:'#2F7BF5',n:'Blue'},{c:'#3FA535',n:'Green'},{c:'#8B5CF6',n:'Purple'}];
var DEFCOL={animals:'#3FA535',vehicles:'#2F7BF5',house:'#E5392B',all:'#FFC531',own:'#2F7BF5',numbers:'#8B5CF6'},MAXDRAW=98;
var ABC=['#E5392B','#2F7BF5','#3FA535'];
/* what is being made (16 Nov 2026, later): the book, the alphabet poster (50 x 70 cm; 150 dpi is plenty at that size)
   and the drawing print (A4: one drawing, or 2 to 6 together as a family print). Same screens, same PDF maker. */
var KINDS={
 book:{id:'book',noun:'book',titles:['Make a book','The drawings','Name and cover','Preview'],mm:[210,210],dpi:300,max:MAXDRAW,
  lead:'A hardcover book of your child\u2019s own drawings, one drawing on every page. Which drawings should it have?',
  pickOwn:'Tap the drawings you want in the book. Each one gets its own page, in this order.',pickAll:'Each drawing gets its own page. Tap one to leave it out.',
  spec:'21 \u00d7 21 cm hardcover',next:'See the book',making:'Making the book'},
 poster:{id:'poster',noun:'poster',titles:['Make a poster','The drawings','Name and colour','Preview'],mm:[500,700],dpi:150,max:30,
  lead:'A big 50 \u00d7 70 cm poster of your child\u2019s own drawings. Which drawings should it have?',
  pickOwn:'Tap the drawings you want on the poster, up to 30.',pickAll:'Tap a drawing to leave it off the poster.',
  spec:'50 \u00d7 70 cm poster',next:'See the poster',making:'Making the poster'},
 print:{id:'print',noun:'print',titles:['Make a print','The drawings','Name and colour','Preview'],mm:[210,297],dpi:300,max:6,skip1:true,
  pickOwn:'Tap one drawing for a print of its own, or up to 6 for a family print.',
  spec:'A4 print, 21 \u00d7 29.7 cm',next:'See the print',making:'Making the print'}};
var KIND=KINDS.book,PCOLS=COLS.concat([{c:CREAM,n:'Cream'}]);
var ORDER=['AZ','az','09'],SLOTS={AZ:'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split(''),az:'abcdefghijklmnopqrstuvwxyz'.split(''),'09':'123456789'.split('')};

/* ================================================================ the child's photos (the same stores as My drawings) */
function getAll(name,os){return new Promise(function(res){try{var r=indexedDB.open(name,1);r.onupgradeneeded=function(){r.result.createObjectStore(os,{keyPath:'id'})};r.onsuccess=function(){try{var q=r.result.transaction(os).objectStore(os).getAll();q.onsuccess=function(){res(q.result||[])};q.onerror=function(){res([])}}catch(e){res([])}};r.onerror=function(){res([])}}catch(e){res([])}})}
function stars(){try{return JSON.parse(localStorage.getItem('sbstar')||'{}')||{}}catch(e){return{}}}
function isPhoto(m){return !!(m&&m.prod==='draw'&&m.kind==='img'&&m.blob)}
function sets(){return window.SBSETS||[]}
function titleMap(){var t={};try{projects('draw').forEach(function(p){if(p&&p.key)t[p.key]=p.t||''})}catch(e){}return t}
/* every set as a book (home screen order), then three more (16 Nov, later): Pick my own (any drawings, none picked to
   start), All my drawings (everything picked to start) and All the numbers (every 1 to 9 set together, so up to 27
   drawings: one numbers set alone is too few for a printed hardcover) */
function loadBooks(){return Promise.all([getAll('stepby-makes','m'),getAll('stepby-drawings','d')]).then(function(r){
 var inSet={};sets().forEach(function(cat){cat.cols.forEach(function(c){var h=c.has||{};Object.keys(h).forEach(function(s){inSet[h[s]]=1})})});
 var by={},old=[];
 r[0].filter(isPhoto).forEach(function(m){if(m.key&&inSet[m.key])(by[m.key]=by[m.key]||[]).push(m);else old.push(m)});
 r[1].filter(function(d){return d&&d.blob}).forEach(function(d){old.push(d)});
 Object.keys(by).forEach(function(k){by[k].sort(function(a,b){return(b.t||0)-(a.t||0)})});
 old.sort(function(a,b){return(a.t||0)-(b.t||0)});
 var T=titleMap(),S=stars(),books=[],every=[];
 ORDER.forEach(function(set){sets().forEach(function(cat){cat.cols.forEach(function(c){if(c.set!==set)return;var h=c.has||{},items=[];
  SLOTS[set].forEach(function(s){var k=h[s],L=k&&by[k];if(!L||!L.length)return;var pick=0;for(var i=0;i<L.length;i++)if(L[i].id===S[k])pick=i;
   items.push({slot:s,key:k,title:T[k]||'',photos:L,pick:pick})});
  books.push({id:c.id,n:c.n,set:set,cv:c.cv,pd:cat.d,kind:String(c.id).split('-')[0],items:items});
  items.forEach(function(it){every.push(it)})})})});
 old.forEach(function(o){every.push({slot:'',key:'',title:'',photos:[o],pick:0})});
 var nums=[];books.forEach(function(b){if(b.set==='09')b.items.forEach(function(it){nums.push(it)})});
 books.push({id:'own',n:'Pick my own',title:'Drawings',set:'',cv:'',pd:NAVY,kind:'own',items:every,wide:'own',off:true});
 books.push({id:'all',n:'All my drawings',title:'Drawings',set:'',cv:'',pd:NAVY,kind:'all',items:every,wide:'all'});
 books.push({id:'numbers',n:'All the numbers',title:'Numbers',set:'09',cv:'',pd:'#8B5CF6',kind:'numbers',items:nums,wide:'nums',sub:'Every 1 to 9 set together'});
 return books})}
function memory(){try{return JSON.parse(localStorage.getItem('sbbook')||'{}')||{}}catch(e){return{}}}
function remember(f){var m=memory();f(m);try{localStorage.setItem('sbbook',JSON.stringify(m))}catch(e){}}
function cleanName(s){s=String(s||'').replace(/\s+/g,' ').replace(/^\s+/,'').slice(0,16);return s?s.charAt(0).toUpperCase()+s.slice(1):''}
function poss(n){n=n.replace(/\s+$/,'');return n+'\u2019s'}
function cleanTitle(s){return String(s||'').replace(/\s+/g,' ').replace(/^\s+/,'').slice(0,28)}
function newBook(b){var m=memory(),n=0,ck=KIND.id+':'+b.id,t=KIND.id==='print'?'My Family':(b.title||b.n);
 return{id:b.id,title:t,deftitle:t,label:b.n,wide:b.wide||'',set:b.set,cv:b.cv,pd:b.pd,kind:b.kind,name:cleanName(m.name||''),
  col:(m.col&&(m.col[ck]||(KIND.id==='book'&&m.col[b.id])))||(KIND.id==='print'?CREAM:KIND.id==='poster'?'#FFC531':DEFCOL[b.kind]||COLS[0].c),cover:null,
  items:b.items.map(function(it){var on=!b.off&&n<KIND.max;if(on)n++;return{slot:it.slot,key:it.key,title:it.title,photos:it.photos,pick:it.pick,on:on}})}}
/* the print keeps the drawings in the order they were tapped (a family print: Grandad, Nan, Mum ...); the book keeps the set's order */
var PICKN=0;
function onItems(B){var on=B.items.filter(function(it){return it.on});if(KIND.id==='print')on.sort(function(a,b){return(a.ord||0)-(b.ord||0)});return on}
function cur(it){return it.photos[it.pick]||it.photos[0]}
function coverItem(B){var on=onItems(B);for(var i=0;i<on.length;i++)if(cur(on[i]).id===B.cover)return on[i];return on[0]||null}
/* the pages: front cover, a page for each drawing, The End if needed to make the count even, back cover */
function pagesOf(B){if(KIND.id==='poster')return[{t:'poster'}];if(KIND.id==='print')return[{t:'print'}];var on=onItems(B),P=[{t:'front'}];on.forEach(function(it,i){P.push({t:'draw',it:it,i:i})});if(on.length%2)P.push({t:'end'});P.push({t:'back'});return P}
function pageName(P,i){var p=P[i];if(!p)return'';if(p.t==='poster')return'The poster';if(p.t==='print')return onItems(B).length>1?'The family print':'The print';if(p.t==='front')return'Front cover';if(p.t==='back')return'Back cover';if(p.t==='end')return'The End';return'Page '+i+(p.it.slot?' \u00b7 '+p.it.slot:'')}

/* ================================================================ pictures */
function canvas(w,h){var c=document.createElement('canvas');c.width=w;c.height=h||w;return c}
function free(c){try{c.width=c.height=0}catch(e){}}
function blobImage(blob){return new Promise(function(res){var u=URL.createObjectURL(blob),im=new Image();im.onload=function(){res({im:im,u:u})};im.onerror=function(){URL.revokeObjectURL(u);res(null)};im.src=u})}
function urlImage(u){return new Promise(function(res){var im=new Image();im.onload=function(){res(im)};im.onerror=function(){res(null)};im.src=u})}
/* where the drawing is on the photo, so the page shows the drawing rather than a lot of empty paper */
function findCrop(im){var W=im.naturalWidth||im.width,H=im.naturalHeight||im.height,full={x:0,y:0,w:1,h:1};if(!W||!H)return full;
 var s=Math.min(1,220/Math.max(W,H)),w=Math.max(8,Math.round(W*s)),h=Math.max(8,Math.round(H*s)),c=canvas(w,h),g=c.getContext('2d',{willReadFrequently:true}),d;
 g.fillStyle='#fff';g.fillRect(0,0,w,h);g.drawImage(im,0,0,w,h);try{d=g.getImageData(0,0,w,h).data}catch(e){free(c);return full}free(c);
 var n=w*h,L=new Float32Array(n),C=new Float32Array(n),i,j,x,y;
 for(i=0,j=0;i<n;i++,j+=4){var r=d[j],gg=d[j+1],b=d[j+2];L[i]=.299*r+.587*gg+.114*b;C[i]=Math.max(r,gg,b)-Math.min(r,gg,b)}
 var ring=[],bw=Math.max(1,Math.round(Math.min(w,h)*.04));
 for(y=0;y<h;y++)for(x=0;x<w;x++)if(x<bw||y<bw||x>=w-bw||y>=h-bw)ring.push(L[y*w+x]);
 ring.sort(function(a,b){return a-b});var P=ring[Math.floor(ring.length*.6)]||255;
 var rows=new Int32Array(h),cols=new Int32Array(w);
 for(y=0;y<h;y++)for(x=0;x<w;x++){i=y*w+x;if(P-L[i]>34||(C[i]>48&&P-L[i]>6)){rows[y]++;cols[x]++}}
 var tr=Math.max(1,w*.01),tc=Math.max(1,h*.01),x0=-1,x1=-1,y0=-1,y1=-1;
 for(y=0;y<h;y++)if(rows[y]>tr){if(y0<0)y0=y;y1=y}
 for(x=0;x<w;x++)if(cols[x]>tc){if(x0<0)x0=x;x1=x}
 if(x0<0||y0<0)return full;
 var m=Math.max(x1-x0+1,y1-y0+1)*.08,X0=Math.max(0,x0-m),Y0=Math.max(0,y0-m),X1=Math.min(w,x1+1+m),Y1=Math.min(h,y1+1+m);
 if((X1-X0)*(Y1-Y0)>w*h*.8)return full;
 var cw=X1-X0,ch=Y1-Y0;
 /* near square (4:5 to 5:4, using more of the paper), so the cards are a similar shape from page to page */
 if(cw/ch<.8){var nw=Math.min(w,ch*.8),cx=(X0+X1)/2;X0=Math.max(0,Math.min(w-nw,cx-nw/2));X1=X0+nw}
 else if(cw/ch>1.25){var nh=Math.min(h,cw/1.25),cy=(Y0+Y1)/2;Y0=Math.max(0,Math.min(h-nh,cy-nh/2));Y1=Y0+nh}
 return{x:X0/w,y:Y0/h,w:(X1-X0)/w,h:(Y1-Y0)/h}}
/* one photo at a time (phones run out of memory decoding a whole set at once): its crop and a small picture */
var PREP={},PQ=Promise.resolve();
function prep(o){var id=o.id||('x'+Math.random());if(PREP[id])return PREP[id];
 PREP[id]=PQ=PQ.then(function(){return blobImage(o.blob)}).then(function(r){if(!r)return null;
  var im=r.im,W=im.naturalWidth,H=im.naturalHeight,cr=findCrop(im),sw=cr.w*W,sh=cr.h*H,s=Math.min(1,THUMB/Math.max(sw,sh)),
   c=canvas(Math.max(1,Math.round(sw*s)),Math.max(1,Math.round(sh*s))),g=c.getContext('2d');
  g.fillStyle='#fff';g.fillRect(0,0,c.width,c.height);g.drawImage(im,cr.x*W,cr.y*H,sw,sh,0,0,c.width,c.height);URL.revokeObjectURL(r.u);
  return new Promise(function(res){c.toBlob(function(b){var u=b?URL.createObjectURL(b):c.toDataURL('image/jpeg',.86);free(c);res({u:u,crop:cr,ar:sw/sh})},'image/jpeg',.86)})},function(){return null});
 return PREP[id]}
var TIMG={};
function thumbPic(o){return prep(o).then(function(p){if(!p)return null;if(!TIMG[p.u])TIMG[p.u]=urlImage(p.u);return TIMG[p.u].then(function(im){return im?{im:im,crop:{x:0,y:0,w:1,h:1},ar:p.ar}:null})})}
function fullPic(o){return prep(o).then(function(p){if(!p)return null;return blobImage(o.blob).then(function(r){return r?{im:r.im,crop:p.crop,ar:p.ar,u:r.u}:null})})}
var LOGO=null;function logoImg(){if(!LOGO)LOGO=urlImage('img/33811a1051920075.webp');return LOGO}

/* ================================================================ drawing the pages (sizes in mm, k = pixels per mm) */
function rr(g,x,y,w,h,r){r=Math.min(r,w/2,h/2);g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath()}
function font(px){return'bold '+Math.max(1,Math.round(px))+'px '+FONT}
function fitFont(g,text,px,maxW){g.font=font(px);var w=g.measureText(text).width;if(w>maxW){px=px*maxW/w;g.font=font(px)}return px}
function light(hex){var n=parseInt(String(hex).slice(1),16),r=n>>16,gg=(n>>8)&255,b=n&255;return(.299*r+.587*gg+.114*b)>170}
function rand(seed){var a=7;for(var i=0;i<seed.length;i++)a=(a*31+seed.charCodeAt(i))|0;return function(){a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
/* big white letters with a navy edge and a navy shadow, like the Step by Draw logo */
function outlined(g,text,x,y,px,maxW,fill){px=fitFont(g,text,px,maxW);g.save();g.textAlign='center';g.textBaseline='alphabetic';g.lineJoin='round';g.miterLimit=2;
 var sw=px*.1;g.strokeStyle=NAVY;g.fillStyle=NAVY;g.lineWidth=sw*2;
 g.strokeText(text,x,y+px*.075);g.fillText(text,x,y+px*.075);
 g.strokeText(text,x,y);g.fillStyle=fill||'#fff';g.fillText(text,x,y);g.restore();return px}
function pill(g,text,cx,cy,px,maxW){px=fitFont(g,text,px,maxW-px*1.5);var tw=g.measureText(text).width,w=tw+px*1.5,h=px*1.65;
 g.save();g.fillStyle=NAVY;rr(g,cx-w/2,cy-h/2+px*.13,w,h,h/2);g.fill();
 g.fillStyle='#fff';g.strokeStyle=NAVY;g.lineWidth=px*.1;rr(g,cx-w/2,cy-h/2,w,h,h/2);g.fill();g.stroke();
 g.fillStyle=NAVY;g.textAlign='center';g.textBaseline='middle';g.fillText(text,cx,cy+px*.05);g.restore()}
function shape(g,t,s){g.beginPath();var i;
 if(t===0){for(i=0;i<10;i++){var r=i%2?s*.45:s,an=-Math.PI/2+i*Math.PI/5;g.lineTo(Math.cos(an)*r,Math.sin(an)*r)}g.closePath();g.stroke()}
 else if(t===1){g.arc(0,0,s*.7,0,Math.PI*2);g.stroke()}
 else if(t===2){g.moveTo(-s,0);for(var x=-s;x<=s+.01;x+=s/8)g.lineTo(x,Math.sin(x/s*Math.PI*2)*s*.3);g.stroke()}
 else if(t===3){g.moveTo(-s*.7,0);g.lineTo(s*.7,0);g.moveTo(0,-s*.7);g.lineTo(0,s*.7);g.stroke()}
 else if(t===4){g.arc(0,0,s*.3,0,Math.PI*2);g.fill()}
 else{g.moveTo(0,-s*.75);g.lineTo(s*.7,s*.5);g.lineTo(-s*.7,s*.5);g.closePath();g.stroke()}}
/* little pencil doodles (stars, rings, squiggles) scattered round the cover, kept off the words and pictures */
function doodles(g,k,R,col,alpha,keep,o){o=o||{};var Wd=o.w||MM,Hd=o.h||MM,sc=o.sc||1;g.save();g.strokeStyle=col;g.fillStyle=col;g.globalAlpha=alpha;g.lineWidth=1.5*sc*k;g.lineCap='round';g.lineJoin='round';
 var cell=30*sc,nx=Math.ceil(Wd/cell),ny=Math.ceil(Hd/cell);
 for(var i=0;i<nx;i++)for(var j=0;j<ny;j++){var skip=R()<.16,s=(4.5+R()*4)*sc,x=i*cell+(5+R()*20)*sc,y=j*cell+(5+R()*20)*sc,t=Math.floor(R()*6),a=R()*Math.PI*2;if(skip)continue;
  /* nothing closer than 10 mm to the edge, where the cover folds round the board */
  x=Math.max(10*sc+s,Math.min(Wd-10*sc-s,x));y=Math.max(10*sc+s,Math.min(Hd-10*sc-s,y));
  var hit=false;(keep||[]).forEach(function(q){if(x+s>q[0]-3*sc&&x-s<q[2]+3*sc&&y+s>q[1]-3*sc&&y-s<q[3]+3*sc)hit=true});if(hit)continue;
  g.save();g.translate(x*k,y*k);g.rotate(a);shape(g,t,s*k);g.restore()}
 g.restore()}
function drawPic(g,p,x,y,w,h){var W=p.im.naturalWidth||p.im.width,H=p.im.naturalHeight||p.im.height,c=p.crop;g.fillStyle='#fff';g.fillRect(x,y,w,h);g.drawImage(p.im,c.x*W,c.y*H,c.w*W,c.h*H,x,y,w,h)}
function tape(g,k,x,y,a,col){g.save();g.translate(x,y);g.rotate(a);g.shadowColor='rgba(8,17,48,.14)';g.shadowBlur=1.6*k;g.fillStyle=col;g.fillRect(-11*k,-3.8*k,22*k,7.6*k);g.restore()}
/* a photo on a white card with a soft shadow; returns the card's size in mm */
function cardSize(p,maxW,maxH,pad){var ar=p?p.ar:.75,iw=maxW-pad*2,ih=iw/ar;if(ih>maxH-pad*2){ih=maxH-pad*2;iw=ih*ar}return{iw:iw,ih:ih,w:iw+pad*2,h:ih+pad*2}}
function card(g,k,p,cx,cy,maxW,maxH,o){o=o||{};var pad=o.pad||4,z=cardSize(p,maxW,maxH,pad),w=z.w*k,h=z.h*k,iw=z.iw*k,ih=z.ih*k;
 g.save();g.translate(cx*k,cy*k);if(o.rot)g.rotate(o.rot);
 g.save();g.shadowColor='rgba(8,17,48,.24)';g.shadowBlur=4.5*k;g.shadowOffsetY=1.8*k;g.fillStyle='#fff';rr(g,-w/2,-h/2,w,h,3.5*k);g.fill();g.restore();
 if(p){g.save();rr(g,-iw/2,-ih/2,iw,ih,2*k);g.clip();drawPic(g,p,-iw/2,-ih/2,iw,ih);g.restore()}
 else{g.fillStyle='#f3efe4';rr(g,-iw/2,-ih/2,iw,ih,2*k);g.fill()}
 if(o.tape){tape(g,k,-w/2+5*k,-h/2+1*k,-.62,o.tape);tape(g,k,w/2-5*k,-h/2+1*k,.62,o.tape)}
 g.restore();return z}
function sticker(g,k,ch,x,y,col){var r=13.5*k;g.save();g.translate(x*k,y*k);g.rotate(-.1);
 g.fillStyle=NAVY;g.beginPath();g.arc(0,1.3*k,r,0,Math.PI*2);g.fill();
 g.fillStyle='#fff';g.strokeStyle=NAVY;g.lineWidth=1.1*k;g.beginPath();g.arc(0,0,r,0,Math.PI*2);g.fill();g.stroke();
 g.font=font(18*k);g.textAlign='center';g.textBaseline='middle';g.fillStyle=col;g.fillText(ch,0,1.1*k);g.restore()}
function caption(g,k,text,cx,y,px,col){px=fitFont(g,text,px*k,176*k);var a=text.charAt(0),b=text.slice(1),wa=g.measureText(a).width,wb=g.measureText(b).width,x=cx*k-(wa+wb)/2;
 g.textAlign='left';g.textBaseline='alphabetic';g.fillStyle=col;g.fillText(a,x,y*k);g.fillStyle=NAVY;g.fillText(b,x+wa,y*k)}
function year(){return String(new Date().getFullYear())}
function monthYear(){try{return new Date().toLocaleDateString('en-GB',{month:'long',year:'numeric'})}catch(e){return year()}}

function front(g,k,B,p){var S=MM*k,bg=B.col,lt=light(bg);
 g.fillStyle=bg;g.fillRect(0,0,S,S);
 doodles(g,k,rand(B.id+'f'),'#fff',lt?.5:.24,[[16,12,194,70],[36,70,174,186],[36,186,174,204]]);
 outlined(g,B.name?poss(B.name):'My',105*k,42*k,30*k,170*k,'#fff');
 pill(g,B.title,105*k,58*k,9.5*k,172*k);
 card(g,k,p,105,129,128,104,{pad:4.5,rot:-.045,tape:lt?'rgba(47,123,245,.62)':'rgba(255,255,255,.66)'});
 g.font=font(6.2*k);g.textAlign='center';g.textBaseline='alphabetic';g.fillStyle=lt?NAVY:'#fff';
 g.fillText(B.name?'Drawn by '+B.name+' \u00b7 '+year():year(),105*k,196*k)}
function inside(g,k,B,it,p,i){var S=MM*k;g.fillStyle=CREAM;g.fillRect(0,0,S,S);
 var cap=it.title||'',capF=13,gap=cap?10:0,maxW=170,maxH=cap?140:170,pad=4,z=cardSize(p,maxW,maxH,pad),
  gh=z.h+(cap?gap+capF*.74:0),top=Math.max(14,(MM-gh)/2);
 card(g,k,p,105,top+z.h/2,maxW,maxH,{pad:pad});
 var col=ABC[i%3];
 if(it.slot)sticker(g,k,it.slot,Math.max(27,105-z.w/2+3),Math.max(27,top+3),col);
 if(cap)caption(g,k,cap,105,top+z.h+gap+capF*.74,capF,col)}
function end(g,k,B){var S=MM*k;g.fillStyle=CREAM;g.fillRect(0,0,S,S);
 doodles(g,k,rand(B.id+'e'),NAVY,.1,[[26,64,184,152]]);
 outlined(g,'The End',105*k,106*k,30*k,170*k,'#FFC531');
 g.textAlign='center';g.textBaseline='alphabetic';
 if(B.name){g.font=font(9*k);g.fillStyle=NAVY;g.fillText('Drawn by '+B.name,105*k,130*k)}
 g.font=font(6.5*k);g.fillStyle=GREY;g.fillText(monthYear(),105*k,(B.name?143:130)*k)}
function tile(g,k,p,x,y,s,slot){g.save();g.shadowColor='rgba(8,17,48,.22)';g.shadowBlur=2*k;g.shadowOffsetY=.8*k;g.fillStyle='#fff';rr(g,x*k,y*k,s*k,s*k,Math.min(3,s*.12)*k);g.fill();g.restore();
 if(p){var pad=Math.max(1.4,s*.06),bw=s-pad*2,iw=bw,ih=bw;if(p.ar>1)ih=bw/p.ar;else iw=bw*p.ar;
  g.save();rr(g,(x+pad)*k,(y+pad)*k,bw*k,bw*k,Math.min(2,s*.08)*k);g.clip();drawPic(g,p,(x+s/2-iw/2)*k,(y+s/2-ih/2)*k,iw*k,ih*k);g.restore()}
 if(slot){var r=Math.max(2.6,Math.min(6,s*.13)),cx=(x+r+.8)*k,cy=(y+r+.8)*k;g.fillStyle=NAVY;g.beginPath();g.arc(cx,cy,r*k,0,Math.PI*2);g.fill();
  g.fillStyle='#fff';g.font=font(r*1.25*k);g.textAlign='center';g.textBaseline='middle';g.fillText(slot,cx,cy+r*.08*k)}}
function brand(g,k,L,o){o=o||{};var z=o.sc||1;k=k*z;var lh=17,lw=L?lh*L.naturalWidth/L.naturalHeight:0,t1='Made with Step by Draw',t2='step-by.com';
 g.font=font(5.4*k);var tw=Math.max(g.measureText(t1).width,g.measureText(t2).width)/k,w=7+lw+(L?5:0)+tw+8,h=25,x=(o.cx!=null?o.cx/z:105)-w/2,y=o.y!=null?o.y/z:170;
 g.save();g.fillStyle=NAVY;rr(g,x*k,(y+1.3)*k,w*k,h*k,12.5*k);g.fill();
 g.fillStyle='#fff';g.strokeStyle=NAVY;g.lineWidth=.9*k;rr(g,x*k,y*k,w*k,h*k,12.5*k);g.fill();g.stroke();
 if(L)g.drawImage(L,(x+7)*k,(y+(h-lh)/2)*k,lw*k,lh*k);
 var tx=x+7+lw+(L?5:0);g.textAlign='left';g.textBaseline='alphabetic';g.font=font(5.4*k);g.fillStyle=NAVY;g.fillText(t1,tx*k,(y+11)*k);g.fillStyle=GREY;g.fillText(t2,tx*k,(y+18.5)*k);g.restore()}
function back(g,k,B,pic){var S=MM*k,bg=B.col,lt=light(bg),on=onItems(B),n=Math.max(1,on.length),GX=16,GY=37,GW=178,GH=124,gap=3.5,best=0,bc=1,c,rw,s;
 g.fillStyle=bg;g.fillRect(0,0,S,S);
 for(c=1;c<=10;c++){rw=Math.ceil(n/c);s=Math.min((GW-(c-1)*gap)/c,(GH-(rw-1)*gap)/rw);if(s>best+.01){best=s;bc=c}}
 s=Math.min(best,58);rw=Math.ceil(n/bc);var tw=bc*s+(bc-1)*gap,th=rw*s+(rw-1)*gap,ox=GX+(GW-tw)/2,oy=GY+(GH-th)/2;
 doodles(g,k,rand(B.id+'b'),'#fff',lt?.5:.24,[[ox,oy,ox+tw,oy+th],[36,166,174,200],[30,12,180,34]]);
 pill(g,countText(on.length)+(B.name?' by '+B.name:'')+' \u00b7 '+year(),105*k,23*k,7*k,170*k);
 var chain=Promise.resolve();
 on.forEach(function(it,i){chain=chain.then(function(){var r=Math.floor(i/bc),q=i%bc,inRow=Math.min(bc,on.length-r*bc),
   x=ox+(tw-(inRow*s+(inRow-1)*gap))/2+q*(s+gap),y=oy+r*(s+gap);
  return pic(cur(it),s).then(function(p){tile(g,k,p,x,y,s,it.slot)})})});
 return chain.then(logoImg).then(function(L){brand(g,k,L)})}
/* the word a drawing is for ("A is for Ant" -> "Ant") */
function wordOf(t){var m=/ is for (.+)$/i.exec(t||''),w=m?m[1]:'';return w?w.charAt(0).toUpperCase()+w.slice(1):''}
function fitGrid(n,W,H,gap,maxS){var best=0,bc=1,c,rw,s;for(c=1;c<=12;c++){rw=Math.ceil(n/c);s=Math.min((W-(c-1)*gap)/c,(H-(rw-1)*gap)/rw);if(s>best+.01){best=s;bc=c}}return{c:bc,s:Math.min(best,maxS||1e9),r:Math.ceil(n/bc)}}
function cell(f,i,n,ox,tw,oy,gap){var r=Math.floor(i/f.c),q=i%f.c,inRow=Math.min(f.c,n-r*f.c);return{x:ox+(tw-(inRow*f.s+(inRow-1)*gap))/2+q*(f.s+gap),y:oy+r*(f.s+gap)}}
function textOn(B){return(B.col===CREAM||light(B.col))?NAVY:'#fff'}
function bgFill(g,k,B,W,H,seed,keep,sc){g.fillStyle=B.col;g.fillRect(0,0,W*k,H*k);
 doodles(g,k,rand(B.id+seed),B.col===CREAM?NAVY:'#fff',B.col===CREAM?.1:(light(B.col)?.5:.24),keep,{w:W,h:H,sc:sc})}
function drawnBy(B){return(B.name?'Drawn by '+B.name+' \u00b7 ':'')+monthYear()}
/* a white card: the drawing, its letter in the corner and its word underneath (poster and family print) */
function wordTile(g,k,p,x,y,s,slot,word,h){h=h||s;var capH=word?s*.19:0,pad=s*.06,bw=s-pad*2,bh=h-pad*2-capH;
 g.save();g.shadowColor='rgba(8,17,48,.22)';g.shadowBlur=s*.05*k;g.shadowOffsetY=s*.02*k;g.fillStyle='#fff';rr(g,x*k,y*k,s*k,h*k,s*.08*k);g.fill();g.restore();
 if(p){var iw=bw,ih=bw/p.ar;if(ih>bh){ih=bh;iw=bh*p.ar}g.save();rr(g,(x+pad)*k,(y+pad)*k,bw*k,bh*k,s*.05*k);g.clip();drawPic(g,p,(x+s/2-iw/2)*k,(y+pad+bh/2-ih/2)*k,iw*k,ih*k);g.restore()}
 if(slot){var r=s*.12,cx=(x+r+s*.03)*k,cy=(y+r+s*.03)*k;g.fillStyle=NAVY;g.beginPath();g.arc(cx,cy,r*k,0,Math.PI*2);g.fill();
  g.fillStyle='#fff';g.font=font(r*1.3*k);g.textAlign='center';g.textBaseline='middle';g.fillText(slot,cx,cy+r*.08*k)}
 if(word){fitFont(g,word,capH*.62*k,(s-pad*2)*k);g.fillStyle=NAVY;g.textAlign='center';g.textBaseline='middle';g.fillText(word,(x+s/2)*k,(y+h-pad-capH*.42)*k)}}
/* the alphabet poster, 50 x 70 cm: the child's name and the title, every drawing on a card with its letter and word, the logo */
function poster(g,k,B,pic){var W=500,H=700,on=onItems(B),n=Math.max(1,on.length),gap=12,GX=30,GY=160,GW=440,GH=452,
  f=fitGrid(n,GW,GH,gap,150),tw=f.c*f.s+(f.c-1)*gap,th=f.r*f.s+(f.r-1)*gap,ox=GX+(GW-tw)/2,oy=GY+(GH-th)/2;
 bgFill(g,k,B,W,H,'p',[[34,18,466,152],[ox,oy,ox+tw,oy+th],[110,618,390,684]],2.4);
 outlined(g,B.name?poss(B.name):'My',250*k,78*k,62*k,420*k,'#fff');
 pill(g,B.title,250*k,112*k,20*k,430*k);
 g.font=font(10*k);g.textAlign='center';g.textBaseline='alphabetic';g.fillStyle=textOn(B);g.fillText(drawnBy(B),250*k,146*k);
 var chain=Promise.resolve();
 on.forEach(function(it,i){chain=chain.then(function(){var q=cell(f,i,on.length,ox,tw,oy,gap);return pic(cur(it),f.s).then(function(p){wordTile(g,k,p,q.x,q.y,f.s,it.slot,wordOf(it.title))})})});
 return chain.then(logoImg).then(function(L){brand(g,k,L,{cx:250,y:628,sc:2.1})})}
/* the drawing print, A4: one drawing with its caption, or 2 to 6 drawings as a family print with the child's name and a title */
function printPage(g,k,B,pic){var W=210,H=297,on=onItems(B),tc=textOn(B);
 if(on.length<=1){var it=on[0]||null;
  return pic(it?cur(it):null).then(function(p){var cap=it?it.title:'',z=cardSize(p,170,190,5),top=30;
   bgFill(g,k,B,W,H,'s',[[18,top-8,192,top+z.h+8],[18,top+z.h+8,192,top+z.h+34],[100,262,206,294]],1);
   card(g,k,p,105,top+z.h/2,170,190,{pad:5});
   if(it&&it.slot)sticker(g,k,it.slot,Math.max(28,105-z.w/2+3),Math.max(28,top+3),ABC[0]);
   if(cap)pill(g,cap,105*k,(top+z.h+21)*k,11*k,182*k);
   signature(g,k,B,194,284)})}
 return famPortrait(g,k,B,pic,on)}
/* the family print (17 Nov 2026): the drawings stand side by side like a family portrait, with no boxes round them.
   Each drawing is lifted off its paper (cutout), so it stands straight on the print's colour. They are all made the same
   height, feet on one line, in one or two rows (whichever lets them be biggest; the first ones tapped go in the back row),
   with each one's word underneath. The title is at the top and the child's name is signed in the bottom right corner. */
function rowSplits(n){var s=[[n]];if(n>=2)s.push([Math.ceil(n/2),Math.floor(n/2)]);if(n>=5)s.push([Math.ceil(n/3),Math.ceil((n-Math.ceil(n/3))/2),n-Math.ceil(n/3)-Math.ceil((n-Math.ceil(n/3))/2)]);return s}
function famPortrait(g,k,B,pic,on){var W=210,X0=12,XW=186,Y0=68,Y1=264,gap=5,LAB=9,RG=5,tc=textOn(B),n=on.length,mpx=Math.max(220,Math.min(1200,Math.round(95*k)));
 bgFill(g,k,B,W,297,'f',[[14,14,196,60],[4,Y0-4,206,Y1+4],[96,264,206,294]],1);
 outlined(g,B.title||'My Family',105*k,46*k,26*k,180*k,'#fff');
 return Promise.all(on.map(function(it){return pic(cur(it),95).then(function(p){return{it:it,c:cutout(p,mpx)}})})).then(function(L){
  L=L.filter(function(o){return o.c});if(!L.length){signature(g,k,B,194,284);return}
  var best=null;rowSplits(L.length).forEach(function(sp){var i=0,rows=sp.map(function(m){var r=L.slice(i,i+m);i+=m;return r}),
    hr=(Y1-Y0-(rows.length-1)*RG)/rows.length-LAB,h=hr;
   rows.forEach(function(r){var a=0;r.forEach(function(o){a+=o.c.ar});h=Math.min(h,(XW-gap*(r.length-1))/a)});
   if(!best||h>best.h+.01)best={rows:rows,h:h}});
  var h=best.h,rows=best.rows,tot=rows.length*(h+LAB)+(rows.length-1)*RG,y=Y0+(Y1-Y0-tot)/2;
  rows.forEach(function(r){var a=0;r.forEach(function(o){a+=o.c.ar});var x=X0+(XW-(h*a+gap*(r.length-1)))/2;
   r.forEach(function(o){var w=h*o.c.ar,c=o.c;g.drawImage(c.cv,c.x0,c.y0,c.bw,c.bh,x*k,y*k,w*k,h*k);free(c.cv);
    var word=wordOf(o.it.title)||o.it.title||'';if(word){var px=fitFont(g,word,5.6*k,(w+gap-1)*k);g.fillStyle=tc;g.textAlign='center';g.textBaseline='alphabetic';g.fillText(word,(x+w/2)*k,(y+h+6.6)*k)}
    x+=w+gap});
   y+=h+LAB+RG});
  signature(g,k,B,194,284)})}
/* a drawing lifted off its paper: the light is evened out first (the paper's colour is worked out from the brightest
   parts nearby, colour by colour). Small bits of paper shut in by the drawing's lines (a white moustache, the white of an
   eye) stay as part of the drawing; the paper round the outside, and bigger shut-in bits (between a fishing rod and its
   line), go see-through, with soft edges. So the drawing stands on any
   background colour like a sticker. Returns the canvas, the box round the ink (x0, y0, bw, bh, in pixels) and that box's
   width over height. */
function cutout(p,maxPx){if(!p||!p.im)return null;
 var W=p.im.naturalWidth||p.im.width,H=p.im.naturalHeight||p.im.height,c=p.crop||{x:0,y:0,w:1,h:1},sw=c.w*W,sh=c.h*H,z=Math.min(1,maxPx/Math.max(sw,sh)),
  w=Math.max(16,Math.round(sw*z)),h=Math.max(16,Math.round(sh*z)),cv=canvas(w,h),g=cv.getContext('2d'),id;
 g.drawImage(p.im,c.x*W,c.y*H,sw,sh,0,0,w,h);try{id=g.getImageData(0,0,w,h)}catch(e){return null}
 var d=id.data,WH=w*h,S=Math.max(6,Math.round(Math.max(w,h)/60)),bw=Math.ceil(w/S),bh=Math.ceil(h/S),N=bw*bh,ch,i,j,x,y,q;
 var M=[new Float32Array(N),new Float32Array(N),new Float32Array(N)];
 for(y=0;y<h;y++)for(x=0;x<w;x++){i=(y*w+x)*4;q=((y/S)|0)*bw+((x/S)|0);for(ch=0;ch<3;ch++)if(d[i+ch]>M[ch][q])M[ch][q]=d[i+ch]}
 function grow(A,R,mx){var T=new Float32Array(N);for(var by=0;by<bh;by++)for(var bx=0;bx<bw;bx++){var v=0,n=0;
   for(var yy=Math.max(0,by-R);yy<=Math.min(bh-1,by+R);yy++)for(var xx=Math.max(0,bx-R);xx<=Math.min(bw-1,bx+R);xx++){var u=A[yy*bw+xx];if(mx){if(u>v)v=u}else{v+=u;n++}}
   T[by*bw+bx]=mx?v:v/n}return T}
 for(ch=0;ch<3;ch++)M[ch]=grow(grow(grow(M[ch],3,1),1,0),1,0);
 /* 1. how much ink each pixel has, and its colour with the paper made white */
 var NC=new Uint8ClampedArray(WH*3),AL=new Float32Array(WH),INK=new Uint8Array(WH);
 for(y=0;y<h;y++){var fy=Math.min(bh-1,Math.max(0,y/S-.5)),yA=fy|0,yB=Math.min(bh-1,yA+1),ty=fy-yA;
  for(x=0;x<w;x++){var fx=Math.min(bw-1,Math.max(0,x/S-.5)),xA=fx|0,xB=Math.min(bw-1,xA+1),tx=fx-xA,mn=1;j=y*w+x;i=j*4;
   for(ch=0;ch<3;ch++){var A=M[ch],pp=(A[yA*bw+xA]*(1-tx)+A[yA*bw+xB]*tx)*(1-ty)+(A[yB*bw+xA]*(1-tx)+A[yB*bw+xB]*tx)*ty,nv=Math.min(1,d[i+ch]/Math.max(24,pp));NC[j*3+ch]=nv*255;if(nv<mn)mn=nv}
   AL[j]=Math.max(0,Math.min(1,(1-mn-.06)/.18));if(AL[j]>.45)INK[j]=1}}
 /* 2. the paper round the outside: filled in from the edges, with small gaps in the lines closed first */
 var r=Math.max(1,Math.round(Math.max(w,h)*.004));
 function dil(src){var t=new Uint8Array(WH),o=new Uint8Array(WH),cnt,xx,yy,cc;
  for(yy=0;yy<h;yy++){cnt=0;for(xx=0;xx<w+r;xx++){if(xx<w&&src[yy*w+xx])cnt++;if(xx-2*r-1>=0&&src[yy*w+xx-2*r-1])cnt--;cc=xx-r;if(cc>=0&&cc<w)t[yy*w+cc]=cnt>0?1:0}}
  for(xx=0;xx<w;xx++){cnt=0;for(yy=0;yy<h+r;yy++){if(yy<h&&t[yy*w+xx])cnt++;if(yy-2*r-1>=0&&t[(yy-2*r-1)*w+xx])cnt--;cc=yy-r;if(cc>=0&&cc<h)o[cc*w+xx]=cnt>0?1:0}}
  return o}
 var DI=dil(INK),OUT=new Uint8Array(WH),Qu=new Int32Array(WH),qh=0,qt=0;
 function push(k){if(!OUT[k]&&!DI[k]){OUT[k]=1;Qu[qt++]=k}}
 for(x=0;x<w;x++){push(x);push((h-1)*w+x)}for(y=0;y<h;y++){push(y*w);push(y*w+w-1)}
 while(qh<qt){j=Qu[qh++];x=j%w;if(x>0)push(j-1);if(x<w-1)push(j+1);if(j>=w)push(j-w);if(j<WH-w)push(j+w)}
 var LIM=WH*.012,SEEN=new Uint8Array(WH),t;
 function add(k){if(!OUT[k]&&!DI[k]&&!SEEN[k]){SEEN[k]=1;Qu[qt++]=k}}
 for(var s0=0;s0<WH;s0++){if(OUT[s0]||DI[s0]||SEEN[s0])continue;qh=0;qt=0;add(s0);
  while(qh<qt){j=Qu[qh++];x=j%w;if(x>0)add(j-1);if(x<w-1)add(j+1);if(j>=w)add(j-w);if(j<WH-w)add(j+w)}
  if(qt>LIM)for(t=0;t<qt;t++)OUT[Qu[t]]=1}
 var OG=dil(OUT);
 /* 3. outside paper goes see-through (soft edges); everything inside the drawing stays solid */
 var x0=w,y0=h,x1=-1,y1=-1;
 for(j=0;j<WH;j++){i=j*4;var a=AL[j];
  if(OG[j]&&!INK[j]){if(a<.02){d[i+3]=0;continue}for(ch=0;ch<3;ch++)d[i+ch]=Math.round(255*Math.max(0,Math.min(1,(NC[j*3+ch]/255-(1-a))/a)));d[i+3]=Math.round(255*a)}
  else{for(ch=0;ch<3;ch++)d[i+ch]=NC[j*3+ch];d[i+3]=255}
  if(INK[j]){x=j%w;y=(j/w)|0;if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y}}
 g.putImageData(id,0,0);
 if(x1<0){x0=0;y0=0;x1=w-1;y1=h-1}
 var m=Math.round(Math.max(w,h)*.015);x0=Math.max(0,x0-m);y0=Math.max(0,y0-m);x1=Math.min(w-1,x1+m);y1=Math.min(h-1,y1+m);
 return{cv:cv,x0:x0,y0:y0,bw:x1-x0+1,bh:y1-y0+1,ar:(x1-x0+1)/(y1-y0+1)}}
/* the child's name signed in the bottom right corner, as an artist signs a picture, with the year small after it */
var SIGN='"Bradley Hand","Segoe Print","Marker Felt","Noteworthy","Comic Sans MS",'+FONT;
function signature(g,k,B,rx,by){if(!B.name)return;var tc=textOn(B),yr=year();
 g.save();g.translate(rx*k,by*k);g.rotate(-.06);g.fillStyle=tc;g.strokeStyle=tc;g.textBaseline='alphabetic';g.textAlign='right';
 g.font='italic bold '+Math.round(5*k)+'px '+SIGN;var yw=g.measureText(yr).width;g.fillText(yr,0,0);
 var px=12*k;g.font='italic bold '+Math.round(px)+'px '+SIGN;var nw=g.measureText(B.name).width;if(nw>90*k){px=px*90*k/nw;g.font='italic bold '+Math.round(px)+'px '+SIGN;nw=g.measureText(B.name).width}
 g.fillText(B.name,-yw-2.5*k,0);
 g.lineWidth=.7*k;g.lineCap='round';g.beginPath();g.moveTo(-yw-2.5*k-nw,2.4*k);g.quadraticCurveTo(-yw-2.5*k-nw*.4,4.6*k,-yw*.3,1.6*k);g.stroke();
 g.restore()}

/* one page as a canvas. full: the print size with the full photos; otherwise a preview from the small pictures.
   The back cover's little tiles (up to 34 mm) use the small pictures even in print (420 px is over 300 dpi there). */
function render(B,spec,S,full){var mw=KIND.mm[0],mh=KIND.mm[1],c=canvas(S,Math.round(S*mh/mw)),g=c.getContext('2d'),k=S/mw;
 function pic(o,mm){if(!o)return Promise.resolve(null);var big=full&&!(mm&&mm*KIND.dpi/25.4<=THUMB);
  return(big?fullPic(o):thumbPic(o)).then(function(p){if(p&&p.u){URL.revokeObjectURL(p.u);delete p.u}return p})}
 var job;
 if(spec.t==='front'){var ci=coverItem(B);job=pic(ci?cur(ci):null).then(function(p){front(g,k,B,p)})}
 else if(spec.t==='draw')job=pic(cur(spec.it)).then(function(p){inside(g,k,B,spec.it,p,spec.i)});
 else if(spec.t==='end'){end(g,k,B);job=Promise.resolve()}
 else if(spec.t==='poster')job=poster(g,k,B,pic);
 else if(spec.t==='print')job=printPage(g,k,B,pic);
 else job=back(g,k,B,pic);
 return job.then(function(){return c})}

/* ================================================================ the PDF (one JPEG picture per page, 21 x 21 cm, 300 dpi) */
function pdfText(s){var h='FEFF';s=String(s||'');for(var i=0;i<s.length;i++){var c=s.charCodeAt(i).toString(16).toUpperCase();h+=('0000'+c).slice(-4)}return'<'+h+'>'}
function pdfBlob(pages,title){var parts=[],off=0,at=[],n=pages.length,last=3+n*3;
 function add(x){parts.push(x);off+=typeof x==='string'?x.length:(x.size!=null?x.size:x.length)}
 function obj(i,body){at[i]=off;add(i+' 0 obj\n'+body+'\nendobj\n')}
 add(new Uint8Array([37,80,68,70,45,49,46,52,10,37,226,227,207,211,10]));/* %PDF-1.4 and a binary comment line */
 var kids=[],i,d=new Date(),st='D:'+d.getFullYear()+('0'+(d.getMonth()+1)).slice(-2)+('0'+d.getDate()).slice(-2)+('0'+d.getHours()).slice(-2)+('0'+d.getMinutes()).slice(-2)+('0'+d.getSeconds()).slice(-2);
 for(i=0;i<n;i++)kids.push((4+i*3)+' 0 R');
 obj(1,'<< /Type /Catalog /Pages 2 0 R >>');
 obj(2,'<< /Type /Pages /Kids ['+kids.join(' ')+'] /Count '+n+' >>');
 obj(3,'<< /Title '+pdfText(title)+' /Creator (Step by Draw) /Producer (Step by Draw) /CreationDate ('+st+') >>');
 pages.forEach(function(p,j){var po=4+j*3,co=po+1,io=po+2,pw=((p.wmm||MM)/25.4*72).toFixed(2),ph=((p.hmm||MM)/25.4*72).toFixed(2),cs='q '+pw+' 0 0 '+ph+' 0 0 cm /Im0 Do Q';
  obj(po,'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 '+pw+' '+ph+'] /TrimBox [0 0 '+pw+' '+ph+'] /Resources << /XObject << /Im0 '+io+' 0 R >> /ProcSet [/PDF /ImageC] >> /Contents '+co+' 0 R >>');
  obj(co,'<< /Length '+cs.length+' >>\nstream\n'+cs+'\nendstream');
  at[io]=off;add(io+' 0 obj\n<< /Type /XObject /Subtype /Image /Width '+p.w+' /Height '+p.h+' /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length '+p.jpg.size+' >>\nstream\n');add(p.jpg);add('\nendstream\nendobj\n')});
 var xo=off,x='xref\n0 '+(last+1)+'\n0000000000 65535 f \n';
 for(i=1;i<=last;i++)x+=('0000000000'+at[i]).slice(-10)+' 00000 n \n';
 add(x+'trailer\n<< /Size '+(last+1)+' /Root 1 0 R /Info 3 0 R >>\nstartxref\n'+xo+'\n%%EOF\n');
 return new Blob(parts,{type:'application/pdf'})}
function makePdf(B,progress){var P=pagesOf(B),out=[],i=0;
 function step(){if(i>=P.length)return Promise.resolve();
  return render(B,P[i],Math.round(KIND.mm[0]/25.4*KIND.dpi),true).then(function(c){var cw=c.width,ch=c.height;return new Promise(function(res,rej){c.toBlob(function(b){free(c);if(!b){rej(new Error('page '+(i+1)));return}out.push({jpg:b,w:cw,h:ch,wmm:KIND.mm[0],hmm:KIND.mm[1]});i++;if(progress)progress(i,P.length);setTimeout(res,0)},'image/jpeg',.92)})}).then(step)}
 if(progress)progress(0,P.length);
 return step().then(function(){return pdfBlob(out,bookTitle(B))})}
function bookTitle(B){if(KIND.id==='print'&&onItems(B).length<=1){var it=onItems(B)[0];return(B.name?poss(B.name)+' ':'')+((it&&it.title)||'drawing')}
 return(B.name?poss(B.name):'My')+' '+B.title}
function fileName(B){return(bookTitle(B)+(KIND.id==='book'?'':' '+KIND.noun)).replace(/[\u2019']/g,'').replace(/[^A-Za-z0-9]+/g,'-').replace(/^-+|-+$/g,'')+'.pdf'}

/* ================================================================ the screens */
var IC={
 back:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>',
 next:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>',
 tick:'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
 plus:'<svg viewBox="0 0 24 24" fill="none" stroke="#081130" stroke-width="3.2" stroke-linecap="round" aria-hidden="true"><path d="M12 6v12M6 12h12"/></svg>',
 pics:'<svg viewBox="0 0 24 24" fill="none" stroke="#081130" stroke-width="2.2" stroke-linejoin="round" aria-hidden="true"><rect x="7" y="3" width="14" height="14" rx="2.5" fill="#d6ebff"/><path d="M4 7v12a2 2 0 0 0 2 2h12"/></svg>',
 save:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 10.5l5 5 5-5M5 20h14"/></svg>',
 book:'<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M14 8h34a4 4 0 0 1 4 4v42a4 4 0 0 1-4 4H14z" fill="#fff" stroke="#081130" stroke-width="3.2" stroke-linejoin="round"/><path d="M10 10a4 4 0 0 1 4-4h32a4 4 0 0 1 4 4v40a4 4 0 0 1-4 4H14a4 4 0 0 0-4 4z" fill="#2F7BF5" stroke="#081130" stroke-width="3.2" stroke-linejoin="round"/><path d="M10 58V10" stroke="#081130" stroke-width="3.2"/><rect x="19" y="16" width="23" height="20" rx="3" fill="#fff" stroke="#081130" stroke-width="2.6"/><path d="M23 31l5-6 4 4 3-3 4 5" fill="none" stroke="#E5392B" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="36" cy="21.5" r="2.2" fill="#FFC531"/><path d="M20 44h22" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/></svg>',
 own:'<svg viewBox="0 0 64 64" aria-hidden="true"><rect x="8" y="10" width="40" height="40" rx="6" fill="#fff" stroke="#081130" stroke-width="3.2"/><circle cx="19" cy="22" r="3.6" fill="#FFC531" stroke="#081130" stroke-width="2.2"/><path d="M12 44l10-11 7 7 6-6 9 10" fill="none" stroke="#2F7BF5" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="46" cy="46" r="12" fill="#3FA535" stroke="#081130" stroke-width="3.2"/><path d="M40.5 46.5l4 4 7-8" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 all:'<svg viewBox="0 0 64 64" aria-hidden="true"><rect x="16" y="8" width="38" height="38" rx="6" fill="#d6ebff" stroke="#081130" stroke-width="3.2" transform="rotate(6 35 27)"/><rect x="10" y="16" width="38" height="38" rx="6" fill="#fff" stroke="#081130" stroke-width="3.2"/><circle cx="21" cy="27" r="3.6" fill="#FFC531" stroke="#081130" stroke-width="2.2"/><path d="M14 48l10-11 7 7 6-6 9 10" fill="none" stroke="#3FA535" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'};
function badge(set){var t=set==='09'?['1','2','3','#8B5CF6','#EC4899','#14B8A6']:set==='az'?['a','b','c','#E5392B','#2F7BF5','#3FA535']:['A','B','C','#E5392B','#2F7BF5','#3FA535'];
 return'<svg viewBox="0 0 84 36" aria-hidden="true"><rect x="2" y="2" width="80" height="32" rx="16" fill="#fff" stroke="#081130" stroke-width="3"/><text x="42" y="26.5" text-anchor="middle" font-family="Arial Rounded MT Bold,Arial,Helvetica,sans-serif" font-weight="900" font-size="22" letter-spacing="1"><tspan fill="'+t[3]+'">'+t[0]+'</tspan><tspan fill="'+t[4]+'">'+t[1]+'</tspan><tspan fill="'+t[5]+'">'+t[2]+'</tspan></text></svg>'}
function styles(){if(G('sbbookcss'))return;var st=document.createElement('style');st.id='sbbookcss';st.textContent=[
'#sbbook{position:fixed;inset:0;z-index:97;background:#fff6e0;color:#081130;display:flex;flex-direction:column;font-family:'+UIFONT+';padding:max(12px,env(safe-area-inset-top,0px)) 16px max(14px,env(safe-area-inset-bottom,0px));-webkit-tap-highlight-color:transparent}',
'#sbbook *{box-sizing:border-box}',
'#sbbook .bktop,#sbbook .bkbody,#sbbook .bkfoot{width:100%;max-width:560px;margin-left:auto;margin-right:auto}',
'#sbbook .bktop{flex:none;display:flex;align-items:center;gap:10px}',
'#sbbook .bktop b{flex:1;text-align:center;font-size:1.35rem;font-weight:900}',
'#sbbook .bktop .round{width:54px;height:54px}#sbbook .bktop .round svg{width:26px;height:26px}',
'#sbbook .bkdots{width:54px;display:flex;gap:5px;justify-content:center;flex:none}#sbbook .bkdots i{width:8px;height:8px;border-radius:50%;background:rgba(8,17,48,.18)}#sbbook .bkdots i.on{background:#081130}',
'#sbbook .bkbody{flex:1;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;padding:16px 4px 18px;position:relative}',
'#sbbook .bkfoot{flex:none;padding-top:8px}#sbbook .bkfoot:empty{display:none}',
'#sbbook .bklead{margin:0 0 16px;font-weight:700;font-size:1rem;line-height:1.4;text-align:center;opacity:.85}',
'#sbbook .bkbtn{width:100%;min-height:62px;border:0;border-radius:999px;background:#FFC531;color:#081130;box-shadow:0 6px 0 #c79410;font:900 1.2rem/1.1 '+UIFONT+';display:flex;align-items:center;justify-content:center;gap:10px;padding:8px 22px;cursor:pointer;margin-bottom:6px}',
'#sbbook .bkbtn svg{width:26px;height:26px;flex:none}',
'#sbbook .bkbtn:active{transform:translateY(4px);box-shadow:0 2px 0 #c79410}',
'#sbbook .bkbtn.w{background:#fff;box-shadow:0 6px 0 rgba(8,17,48,.18)}#sbbook .bkbtn.w:active{box-shadow:0 2px 0 rgba(8,17,48,.18)}',
'#sbbook .bkbtn:disabled{opacity:.45;transform:none}',
'#sbbook .bksmall{text-align:center;font-weight:700;font-size:.88rem;line-height:1.35;opacity:.75;margin:8px 4px 2px}',
/* 1. the books */
'#sbbook .bksets{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px 10px}',
'#sbbook .bkcell{display:flex;flex-direction:column;align-items:center;gap:7px;min-width:0}',
'#sbbook .bkset{position:relative;width:100%;aspect-ratio:1;border:0;border-radius:16px;background:#fff;box-shadow:0 4px 0 var(--pd,rgba(8,17,48,.16));padding:8px 8px 22px;display:flex;align-items:center;justify-content:center;cursor:pointer}',
'#sbbook .bkset:active{transform:translateY(3px);box-shadow:0 1px 0 var(--pd,rgba(8,17,48,.16))}',
'#sbbook .bkset img{position:absolute;left:8px;top:8px;width:calc(100% - 16px);height:calc(100% - 30px);object-fit:contain;display:block;pointer-events:none}',
'#sbbook .bkset>svg{display:block;pointer-events:none}',
'#sbbook .bkset .sbbd{position:absolute;left:50%;bottom:6px;transform:translateX(-50%);width:56%}#sbbook .bkset .sbbd svg{display:block;width:100%;height:auto}',
'#sbbook .bkset:disabled{opacity:.35;cursor:default;transform:none}',
'#sbbook .bkcell span{font-weight:800;font-size:.82rem;opacity:.8;text-align:center;line-height:1.2}',
'#sbbook .bkallc{grid-column:1/-1}#sbbook .bkallc .bkset{aspect-ratio:auto;height:96px;flex-direction:row;gap:14px;padding:10px 18px;justify-content:flex-start;font:900 1.1rem/1.2 '+UIFONT+';color:#081130}',
'#sbbook .bkallc .bkset>svg{height:70px;width:70px;flex:none}',
'#sbbook .bkallc .bkset{height:88px}#sbbook .bkallc .bkset>span{text-align:left}',
'#sbbook .bknums{width:70px;height:70px;flex:none;display:flex;align-items:center;justify-content:center}#sbbook .bknums svg{width:70px;height:auto;display:block}',
'#sbbook .bksum .bknums{width:46px;height:46px}#sbbook .bksum .bknums svg{width:46px}',
'#sbbook .bktools{display:flex;gap:10px;justify-content:center;margin:0 0 12px}',
'#sbbook .bktools button{height:40px;padding:0 18px;border-radius:999px;border:2px solid #081130;background:#fff;color:#081130;font:800 .95rem/1 '+UIFONT+';cursor:pointer}#sbbook .bktools button:active{transform:translateY(2px)}',
/* 2. the drawings */
'#sbbook .bksum{background:#fff;border-radius:18px;box-shadow:0 4px 0 rgba(8,17,48,.12);padding:12px 16px;margin-bottom:14px;display:flex;align-items:center;gap:12px}',
'#sbbook .bksum img{width:46px;height:46px;object-fit:contain;flex:none}#sbbook .bksum>svg{width:46px;height:46px;flex:none}',
'#sbbook .bksum div{flex:1;min-width:0}#sbbook .bksum b{display:block;font-size:1.05rem;font-weight:900}#sbbook .bksum span{display:block;font-weight:700;font-size:.9rem;opacity:.75;margin-top:2px}',
'#sbbook .bksum span.ok{color:#2b7d25;opacity:1}#sbbook .bksum span.no{color:#b3261e;opacity:1}',
'#sbbook .bkgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px 10px;padding-top:6px}',
'#sbbook .bkit{position:relative;aspect-ratio:1;border:2px solid #f0e8d2;border-radius:14px;background:#fff;padding:5px;box-shadow:0 4px 0 rgba(8,17,48,.14);cursor:pointer}',
'#sbbook .bkit .ph{width:100%;height:100%;border-radius:8px;background:#f6f1e4 center/contain no-repeat;transition:opacity .15s}',
'#sbbook .bkit .bkl{position:absolute;left:3px;top:3px;min-width:24px;height:24px;padding:0 5px;border-radius:999px;background:#081130;color:#fff;display:flex;align-items:center;justify-content:center;font:900 14px/1 '+FONT+'}',
'#sbbook .bkit .bkck{position:absolute;right:-7px;top:-7px;width:26px;height:26px;border-radius:50%;background:#3FA535;border:2px solid #fff;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 0 rgba(8,17,48,.2)}#sbbook .bkit .bkck svg{width:16px;height:16px}',
'#sbbook .bkit.off .ph{opacity:.25;filter:grayscale(1)}#sbbook .bkit.off .bkck{background:#fff;border-color:#081130}',
'#sbbook .bkmany{position:absolute;right:3px;bottom:3px;height:26px;padding:0 6px 0 3px;border-radius:999px;background:#fff;border:2px solid #081130;display:flex;align-items:center;gap:2px;font:900 12px/1 '+UIFONT+';color:#081130;cursor:pointer}#sbbook .bkmany svg{width:17px;height:17px}',
'#sbbook .bkpick{position:absolute;inset:0;z-index:3;background:rgba(8,17,48,.55);display:flex;align-items:flex-end;justify-content:center;padding:16px}',
'#sbbook .bkpickin{width:100%;max-width:520px;background:#fff6e0;border-radius:22px;padding:16px;box-shadow:0 10px 30px rgba(0,0,0,.3)}',
'#sbbook .bkpickin b{display:block;text-align:center;font-weight:900;font-size:1.1rem;margin-bottom:12px}',
'#sbbook .bkpickg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-bottom:14px}',
'#sbbook .bkpickg button{aspect-ratio:1;border:3px solid #f0e8d2;border-radius:14px;background:#fff center/contain no-repeat;background-origin:content-box;padding:4px;cursor:pointer}#sbbook .bkpickg button.on{border-color:#081130}',
/* 3. name and cover */
'#sbbook .bkcv{display:block;width:min(74vw,330px);height:auto;aspect-ratio:1;margin:0 auto 18px;border-radius:5px;background:#fff;box-shadow:0 12px 26px rgba(8,17,48,.28),0 0 0 1px rgba(8,17,48,.06)}',
'#sbbook .bkfld{display:block;margin:0 0 16px}#sbbook .bkfld>span,#sbbook .bkrow>span{display:block;font-weight:900;font-size:1rem;margin:0 0 8px}',
'#sbbook .bkfld input{width:100%;height:58px;border-radius:16px;border:2px solid #e8dfc6;background:#fff;padding:0 16px;font:800 1.25rem/1 '+UIFONT+';color:#081130;outline:none;-webkit-appearance:none;appearance:none}#sbbook .bkfld input:focus{border-color:#081130}',
'#sbbook .bkrow{margin:0 0 16px}',
'#sbbook .bkcols{display:flex;gap:12px;flex-wrap:wrap}#sbbook .bkcol{width:46px;height:46px;border-radius:50%;border:3px solid #fff;background:var(--c);box-shadow:0 0 0 2px rgba(8,17,48,.16);cursor:pointer;padding:0}#sbbook .bkcol.on{box-shadow:0 0 0 3px #081130}',
'#sbbook .bkcovs{display:flex;gap:10px;overflow-x:auto;-webkit-overflow-scrolling:touch;padding:3px 3px 10px}',
'#sbbook .bkcovs button{flex:none;width:72px;height:72px;border:3px solid #f0e8d2;border-radius:14px;background:#fff center/contain no-repeat;background-origin:content-box;padding:4px;cursor:pointer}#sbbook .bkcovs button.on{border-color:#081130}',
/* 4. preview */
'#sbbook .bkpg{width:100%;max-width:440px;margin:4px auto 0;aspect-ratio:1;background:#fff;border-radius:4px;overflow:hidden;box-shadow:0 12px 26px rgba(8,17,48,.28),0 0 0 1px rgba(8,17,48,.06);touch-action:pan-y}',
'#sbbook .bkpg img{width:100%;height:100%;display:block;-webkit-user-drag:none;pointer-events:none}',
'#sbbook .bknav{display:flex;align-items:center;justify-content:center;gap:12px;margin:18px 0 6px}',
'#sbbook .bknav .round{width:52px;height:52px;flex:none}#sbbook .bknav .round svg{width:24px;height:24px}#sbbook .bknav .round:disabled{opacity:.3}',
'#sbbook .bkpl{min-width:150px;text-align:center;font-weight:900;font-size:1.1rem}',
'#sbbook .bkspec{text-align:center;font-weight:700;font-size:.9rem;opacity:.72;margin:0}',
'#sbbook .bkbusy{position:absolute;inset:0;z-index:4;background:rgba(255,246,224,.95);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;font-weight:900;font-size:1.05rem;text-align:center;padding:20px}',
'#sbbook .bkbar{width:72%;max-width:320px;height:18px;border-radius:999px;background:#fff;box-shadow:inset 0 0 0 2px #081130;overflow:hidden}#sbbook .bkbar i{display:block;height:100%;width:0;background:#3FA535;transition:width .25s}',
].join('\n');document.head.appendChild(st)}

var B=null,STEP=0,PDF=null,VIEW={i:0,cache:{},pages:[]};
function body(){return G('bkbody')}function foot(){return G('bkfoot')}
function frame(n){STEP=n;var h=G('bkh');if(h)h.textContent=KIND.titles[n-1];var d=document.querySelectorAll('#sbbook .bkdots i');[].forEach.call(d,function(x,i){x.classList.toggle('on',i<n)});
 body().innerHTML='';foot().innerHTML='';body().scrollTop=0}
function open(kind){KIND=KINDS[kind]||KINDS.book;styles();close();var w=document.createElement('div');w.id='sbbook';w.setAttribute('role','dialog');w.setAttribute('aria-label',KIND.titles[0]);
 w.innerHTML='<div class="bktop"><button class="round" id="bkback" type="button" aria-label="Back">'+IC.back+'</button><b id="bkh">'+esc(KIND.titles[0])+'</b><div class="bkdots" aria-hidden="true"><i></i><i></i><i></i><i></i></div></div><div class="bkbody" id="bkbody"></div><div class="bkfoot" id="bkfoot"></div>';
 document.body.appendChild(w);G('bkback').onclick=goBack;
 /* the print starts straight on the drawings (any of them, none picked) */
 if(KIND.skip1)loadBooks().then(function(books){var own=null;books.forEach(function(b){if(b.id==='own')own=b});if(!G('sbbook')||!own)return;B=newBook(own);step2()});else step1()}
function close(){var w=G('sbbook');if(w)w.remove();clearView();PDF=null}
function goBack(){if(STEP<=1||(STEP===2&&KIND.skip1))close();else if(STEP===2)step1();else if(STEP===3)step2();else step3()}
function bg(el,u){if(el&&u)el.style.backgroundImage='url("'+u+'")'}
function thumbInto(el,o){prep(o).then(function(p){if(p)bg(el,p.u)})}
function countText(n){return n+(n===1?' drawing':' drawings')}
function wideIcon(w){return w==='nums'?'<span class="bknums">'+badge('09')+'</span>':(IC[w]||IC.all)}

/* 1. pick the book */
function step1(){frame(1);B=null;PDF=null;
 body().innerHTML='<p class="bklead">'+esc(KIND.lead)+'</p><div class="bksets" id="bksets"></div>';
 loadBooks().then(function(books){var g=G('bksets');if(!g)return;var any=false;
  g.innerHTML=books.map(function(b,i){var n=b.items.length;if(n)any=true;
   if(b.wide)return'<div class="bkcell bkallc"><button class="bkset" type="button" data-i="'+i+'" aria-label="'+esc(b.n)+', '+(n?countText(n):'no photos yet')+'"'+(n?'':' disabled')+'>'+wideIcon(b.wide)+'<span>'+esc(b.n)+'<br><small style="font-weight:700;opacity:.75">'+(n?(b.off?'Choose any of '+countText(n):(b.sub?b.sub+' \u00b7 ':'')+countText(n)):'No photos yet')+'</small></span></button></div>';
   return'<div class="bkcell"><button class="bkset" type="button" data-i="'+i+'" style="--pd:'+b.pd+'" aria-label="'+esc(b.n)+', '+countText(n)+'"'+(n?'':' disabled')+'><img src="img/'+esc(b.cv)+'.webp" alt=""><span class="sbbd">'+badge(b.set)+'</span></button><span>'+(n?countText(n):'No photos yet')+'</span></div>'}).join('');
  if(!any)g.insertAdjacentHTML('beforebegin','<p class="bksmall" style="margin-bottom:14px">There are no photos in My drawings yet. Finish a drawing and take its photo on the trophy screen, then come back here.</p>');
  [].forEach.call(g.querySelectorAll('.bkset'),function(el){el.onclick=function(){B=newBook(books[+el.getAttribute('data-i')]);step2()}})})}

/* 2. check the drawings */
function sumHTML(){var on=onItems(B),n=on.length,P=pagesOf(B).length,ok=KIND.id==='book'?P>=MINPAGES:n>0,need=Math.max(0,21-n);
 var head=B.wide?wideIcon(B.wide):'<img src="img/'+esc(B.cv)+'.webp" alt="">';
 var s=!n?'No drawings picked':KIND.id==='book'?countText(n)+' \u00b7 '+P+' pages':KIND.id==='poster'?countText(n)+' \u00b7 50 \u00d7 70 cm':n===1?'1 drawing \u00b7 a print of its own':countText(n)+' \u00b7 a family print';
 var empty=KIND.id==='print'?'Tap 1 drawing, or up to 6':B.kind==='own'?'Tap the drawings you want':'Tap drawings to put them back in';
 return head+'<div><b>'+esc(KIND.id==='print'?'Drawing print':B.label||B.title)+'</b><span>'+s+'</span><span class="'+(ok?'ok':'no')+'">'+(n?(ok?'Ready to print':'To print it needs '+need+' more ('+MINPAGES+' pages or more)'):empty)+'</span></div>'}
function step2(){frame(2);PDF=null;clearView();
 body().innerHTML='<div class="bksum" id="bksum">'+sumHTML()+'</div><p class="bklead" style="margin-bottom:10px">'+esc(B.kind==='own'?KIND.pickOwn:KIND.pickAll)+'</p>'+
  '<div class="bktools">'+(KIND.max>=26?'<button type="button" id="bkallon">Pick all</button>':'')+'<button type="button" id="bkalloff">Clear</button></div><div class="bkgrid" id="bkgrid"></div>';
 var g=G('bkgrid');
 g.innerHTML=B.items.map(function(it,i){var m=it.photos.length;
  return'<div class="bkit'+(it.on?'':' off')+'" role="button" tabindex="0" data-i="'+i+'" aria-pressed="'+(it.on?'true':'false')+'" aria-label="'+esc(it.title||('Drawing '+(i+1)))+'"><div class="ph"></div>'+(it.slot?'<span class="bkl" aria-hidden="true">'+esc(it.slot)+'</span>':'')+'<span class="bkck" aria-hidden="true">'+(it.on?IC.tick:IC.plus)+'</span>'+(m>1?'<button class="bkmany" type="button" aria-label="Pick another photo ('+m+' photos)">'+IC.pics+m+'</button>':'')+'</div>'}).join('');
 [].forEach.call(g.querySelectorAll('.bkit'),function(el){var it=B.items[+el.getAttribute('data-i')];thumbInto(el.querySelector('.ph'),cur(it));
  el.onclick=function(){if(!it.on&&onItems(B).length>=KIND.max){full();return}it.on=!it.on;if(it.on)it.ord=++PICKN;mark(el,it);G('bksum').innerHTML=sumHTML();nextBtn()};
  var mb=el.querySelector('.bkmany');if(mb)mb.onclick=function(e){e.stopPropagation();chooser(it,el)}});
 function nextBtn(){foot().innerHTML='<button class="bkbtn" id="bknext" type="button"'+(onItems(B).length?'':' disabled')+'>Next'+IC.next+'</button>';G('bknext').onclick=step3}
 function all(on){var n=0;B.items.forEach(function(it){it.on=on&&n<KIND.max;if(it.on)n++});[].forEach.call(g.querySelectorAll('.bkit'),function(el){mark(el,B.items[+el.getAttribute('data-i')])});G('bksum').innerHTML=sumHTML();nextBtn();if(on&&B.items.length>KIND.max)full()}
 function full(){var s=G('bksum');if(s&&!s.querySelector('.bkmax'))s.querySelector('div').insertAdjacentHTML('beforeend','<span class="no bkmax">A '+KIND.noun+' can have up to '+KIND.max+' drawings</span>')}
 if(G('bkallon'))G('bkallon').onclick=function(){all(true)};G('bkalloff').onclick=function(){all(false)};
 nextBtn()}
function mark(el,it){el.classList.toggle('off',!it.on);el.setAttribute('aria-pressed',it.on?'true':'false');el.querySelector('.bkck').innerHTML=it.on?IC.tick:IC.plus}
function chooser(it,el){var w=document.createElement('div');w.className='bkpick';
 w.innerHTML='<div class="bkpickin" role="dialog" aria-label="Pick the photo"><b>'+esc(it.title||'Pick the photo')+'</b><div class="bkpickg">'+it.photos.map(function(o,i){return'<button type="button" data-i="'+i+'" class="'+(i===it.pick?'on':'')+'" aria-label="Photo '+(i+1)+'"></button>'}).join('')+'</div><button class="bkbtn w" type="button">Done</button></div>';
 G('sbbook').appendChild(w);
 [].forEach.call(w.querySelectorAll('.bkpickg button'),function(b){thumbInto(b,it.photos[+b.getAttribute('data-i')]);b.onclick=function(){it.pick=+b.getAttribute('data-i');it.on=true;w.remove();
  thumbInto(el.querySelector('.ph'),cur(it));el.classList.remove('off');el.setAttribute('aria-pressed','true');el.querySelector('.bkck').innerHTML=IC.tick;G('bksum').innerHTML=sumHTML()}});
 w.querySelector('.bkbtn').onclick=function(){w.remove()};w.onclick=function(e){if(e.target===w)w.remove()}}

/* 3. name, colour and cover drawing, with the cover drawn as you go */
var CVT=null,CVN=0;
function drawCover(){clearTimeout(CVT);CVT=setTimeout(function(){var el=G('bkcv');if(!el||!B)return;var my=++CVN;
 render(B,pagesOf(B)[0],KIND.id==='book'?680:560,false).then(function(c){if(my!==CVN||!G('bkcv')){free(c);return}var x=el.getContext('2d');el.width=c.width;el.height=c.height;x.drawImage(c,0,0);free(c)})},90)}
function portrait(){var m=KIND.mm;return m[1]>m[0]?'aspect-ratio:'+m[0]+'/'+m[1]+';':''}
function step3(){frame(3);PDF=null;clearView();var on=onItems(B),bk=KIND.id==='book',fam=KIND.id==='print'&&on.length>1;
 if(!B.cover||!coverItem(B)||cur(coverItem(B)).id!==B.cover)B.cover=on.length?cur(on[0]).id:null;
 body().innerHTML='<canvas class="bkcv" id="bkcv" width="680" height="680" style="'+(bk?'':portrait()+'width:min(58vw,250px)')+'" aria-label="'+(bk?'The front cover':'The '+KIND.noun)+'"></canvas>'+
  '<label class="bkfld"><span>Child\u2019s name</span><input id="bkname" type="text" maxlength="16" autocomplete="off" autocapitalize="words" spellcheck="false" placeholder="Their name" value="'+esc(B.name)+'"></label>'+
  (KIND.id!=='print'||fam?'<label class="bkfld"><span>'+(bk?'Book title':KIND.id==='poster'?'Poster title':'Title')+'</span><input id="bktitle" type="text" maxlength="28" autocomplete="off" spellcheck="false" placeholder="'+esc(B.deftitle||'')+'" value="'+esc(B.title)+'"></label>':'')+
  '<div class="bkrow"><span>'+(bk?'Cover colour':'Background colour')+'</span><div class="bkcols">'+(bk?COLS:PCOLS).map(function(c){return'<button class="bkcol'+(c.c===B.col?' on':'')+'" type="button" data-c="'+c.c+'" style="--c:'+c.c+'" aria-label="'+c.n+'"></button>'}).join('')+'</div></div>'+
  (bk?'<div class="bkrow"><span>Cover drawing</span><div class="bkcovs" id="bkcovs">'+on.map(function(it,i){var o=cur(it);return'<button type="button" data-i="'+i+'" class="'+(o.id===B.cover?'on':'')+'" aria-label="'+esc(it.title||('Drawing '+(i+1)))+'"></button>'}).join('')+'</div></div>':'');
 var inp=G('bkname');inp.oninput=function(){B.name=cleanName(inp.value);var nm=B.name;remember(function(m){m.name=nm});drawCover()};
 inp.onkeydown=function(e){if(e.key==='Enter')inp.blur()};
 var ti=G('bktitle')||document.createElement('input');ti.oninput=function(){B.title=cleanTitle(ti.value)||B.deftitle||'Drawings';drawCover()};ti.onkeydown=function(e){if(e.key==='Enter')ti.blur()};
 ti.onblur=function(){if(!cleanTitle(ti.value))ti.value=B.title};
 [].forEach.call(document.querySelectorAll('#sbbook .bkcol'),function(b){b.onclick=function(){B.col=b.getAttribute('data-c');var id=KIND.id+':'+B.id,col=B.col;remember(function(m){m.col=m.col||{};m.col[id]=col});
  [].forEach.call(document.querySelectorAll('#sbbook .bkcol'),function(x){x.classList.toggle('on',x===b)});drawCover()}});
 [].forEach.call(document.querySelectorAll('#bkcovs button'),function(b){var it=on[+b.getAttribute('data-i')];thumbInto(b,cur(it));b.onclick=function(){B.cover=cur(it).id;
  [].forEach.call(document.querySelectorAll('#bkcovs button'),function(x){x.classList.toggle('on',x===b)});drawCover()}});
 foot().innerHTML='<button class="bkbtn" id="bknext" type="button">'+esc(KIND.next)+IC.next+'</button>';G('bknext').onclick=function(){inp.blur();ti.blur();step4()};
 drawCover()}

/* 4. preview, page by page, then the PDF */
function clearView(){Object.keys(VIEW.cache).forEach(function(i){var p=VIEW.cache[i];p.then(function(u){if(u&&u.indexOf('blob:')===0)URL.revokeObjectURL(u)})});VIEW={i:0,cache:{},pages:[]}}
function pageURL(i){if(!VIEW.cache[i])VIEW.cache[i]=render(B,VIEW.pages[i],KIND.id==='book'?760:620,false).then(function(c){return new Promise(function(res){c.toBlob(function(b){res(b?URL.createObjectURL(b):c.toDataURL('image/jpeg',.85));free(c)},'image/jpeg',.86)})});return VIEW.cache[i]}
function showPage(i){var P=VIEW.pages;i=Math.max(0,Math.min(P.length-1,i));VIEW.i=i;var im=G('bkpgimg'),l=G('bkpl');if(!im)return;
 l.textContent=pageName(P,i);if(G('bkpv')){G('bkpv').disabled=i===0;G('bknx').disabled=i===P.length-1}
 pageURL(i).then(function(u){if(VIEW.i===i&&G('bkpgimg'))G('bkpgimg').src=u;
  /* the next pages, ready for the next tap */
  [i+1,i+2].forEach(function(j){if(j<P.length)pageURL(j)})})}
function step4(){frame(4);clearView();VIEW.pages=pagesOf(B);var P=VIEW.pages.length,ok=P>=MINPAGES,n=onItems(B).length,bk=KIND.id==='book';if(!bk)ok=true;
 body().innerHTML='<div class="bkpg" id="bkpg" style="'+(bk?'':portrait()+'max-width:min(100%,300px)')+'"><img id="bkpgimg" alt="'+(bk?'Book page':'The '+KIND.noun)+'"></div>'+
  (bk?'<div class="bknav"><button class="round" id="bkpv" type="button" aria-label="Previous page">'+IC.back+'</button><div class="bkpl" id="bkpl" aria-live="polite"></div><button class="round" id="bknx" type="button" aria-label="Next page">'+IC.next+'</button></div>':'<div class="bknav"><div class="bkpl" id="bkpl"></div></div>')+
  '<p class="bkspec">'+(bk?P+' pages \u00b7 ':'')+esc(KIND.spec)+'</p>'+
  (ok?'':'<p class="bksmall" style="color:#b3261e;opacity:1">A printed hardcover needs '+MINPAGES+' pages or more: '+(21-n>0?Math.max(1,21-n)+' more drawing'+(21-n===1?'':'s'):'more drawings')+'. You can still make the PDF to check it.</p>');
 if(G('bkpv')){G('bkpv').onclick=function(){showPage(VIEW.i-1)};G('bknx').onclick=function(){showPage(VIEW.i+1)}}
 var pg=G('bkpg'),sx=0,sy=0,on=false;
 pg.addEventListener('touchstart',function(e){if(e.touches.length!==1){on=false;return}on=true;sx=e.touches[0].clientX;sy=e.touches[0].clientY},{passive:true});
 pg.addEventListener('touchend',function(e){if(!on)return;on=false;var t=e.changedTouches&&e.changedTouches[0];if(!t)return;var dx=t.clientX-sx,dy=t.clientY-sy;if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy)*1.3)showPage(VIEW.i+(dx<0?1:-1))},{passive:true});
 pdfFoot();showPage(0)}
function pdfFoot(){var f=foot();if(!f)return;
 if(!PDF_BUTTON){f.innerHTML='<button class="bkbtn" type="button" disabled>Order the '+KIND.noun+' (coming soon)</button>';return}
 if(PDF){f.innerHTML='<button class="bkbtn" id="bksave" type="button">'+IC.save+'Save the PDF</button><p class="bksmall">'+(KIND.id==='book'?PDF.pages+' pages':esc(KIND.spec))+', '+(PDF.blob.size/1048576).toFixed(1)+' MB, ready for Peecho. Ordering a printed copy comes next.</p>';G('bksave').onclick=savePdf;return}
 f.innerHTML='<button class="bkbtn" id="bkmake" type="button">Make the PDF</button><p class="bksmall">Ordering a printed copy comes next. For now the PDF is to check the '+KIND.noun+'.</p>';G('bkmake').onclick=startPdf}
function startPdf(){if(!B)return;var w=document.createElement('div');w.className='bkbusy';w.setAttribute('role','status');
 w.innerHTML='<div>'+esc(KIND.making)+'</div><div class="bkbar"><i id="bkbari"></i></div><div id="bkbart" style="font-weight:700;opacity:.75;font-size:.95rem"></div>';G('sbbook').appendChild(w);
 var mk=G('bkmake');if(mk)mk.disabled=true;var t0=Date.now();
 makePdf(B,function(i,n){var b=G('bkbari'),t=G('bkbart');if(b)b.style.width=Math.round(i/n*100)+'%';if(t)t.textContent=i<n?(n>1?'Page '+(i+1)+' of '+n:'Drawing it at print size'):'Putting it together'}).then(function(blob){
  PDF={blob:blob,name:fileName(B),title:bookTitle(B),pages:pagesOf(B).length,ms:Date.now()-t0};w.remove();pdfFoot()},function(e){
  w.innerHTML='<div>Sorry, that didn\u2019t work.</div><div style="font-weight:700;opacity:.75;font-size:.95rem">There may not be enough memory free. Close other apps and try again.</div><button class="bkbtn w" type="button" style="max-width:260px">OK</button>';
  w.querySelector('button').onclick=function(){w.remove();pdfFoot()};if(window.console)console.error(e)})}
function touchDevice(){try{if(typeof window.SBIsPhone==='function')return !!window.SBIsPhone()}catch(e){}try{return matchMedia('(pointer:coarse)').matches}catch(e){return false}}
function savePdf(){if(!PDF)return;var f=null;try{f=new File([PDF.blob],PDF.name,{type:'application/pdf'})}catch(e){}
 if(f&&touchDevice()&&navigator.canShare&&navigator.share){try{if(navigator.canShare({files:[f]})){navigator.share({files:[f],title:PDF.title}).catch(function(){});return}}catch(e){}}
 var u=URL.createObjectURL(PDF.blob),a=document.createElement('a');a.href=u;a.download=PDF.name;a.rel='noopener';document.body.appendChild(a);a.click();setTimeout(function(){a.remove();URL.revokeObjectURL(u)},60000)}

/* ================================================================ the Grown-ups page: a shop (17 Nov 2026)
   Laid out like a high-street shop's listing page: one grid of identical photo cards on white, in the app's own navy,
   yellow and rounded headings. Five things and nothing else, in this order (as asked): the free print sheets, the
   Step by Draw books on Amazon, then the three things made from the child's own drawings: the book, the poster and the
   print. No About card, and no finished-set posters.
   Prices are what parents pay, delivered in the UK (Peecho cost: book \u00a315.21, poster \u00a314.94, print \u00a39.93).
   The book, poster and print open their makers, which make the PDF; ordering through Peecho comes later.
   The print sheets and the books each open a page of their own inside the shop; Back (the pill or the top button)
   comes back to the shop. The pictures are img/shop-*.webp (made 17 Nov 2026 from the app's own drawings). */
window.SBCAT=1;      // sb-extras.js leaves out its own print cards when the shop is here
var SHOP=[
 {id:'sheets',img:'shop-sheets2',bd:'Free',line:'Print at home',n:'Print sheets',pr:'Free',sz:'A4 or US Letter',mt:'A sheet for every drawing, with all its steps on one page.',bt:'Choose a sheet'},
 {id:'books',img:'shop-books',bd:'Coming soon',dk:1,line:'On Amazon',n:'Step by Draw books',pr:'Coming soon',sz:'7 books',mt:'Our step-by-step drawing books, one for every set.',bt:'See the books'},
 {id:'book',img:'shop-book',bd:'New',line:'From their drawings',n:'A to Z book',pr:'\u00a324.99',sz:'21 \u00d7 21 cm hardcover',mt:'One drawing on every page and their name on the cover. Delivered.',bt:'Make a book'},
 {id:'poster',img:'shop-poster',line:'From their drawings',n:'Alphabet poster',pr:'\u00a324.99',sz:'50 \u00d7 70 cm',mt:'A whole set of their drawings on one big poster. Delivered.',bt:'Make a poster'}];
/* 20 Nov 2026: the Drawing print card was taken off the Shop (the print maker below stays, unused). */
/* Step by Draw books on Amazon: one for each A to Z set, and the numbers book. When a book is on sale, put its Amazon
   address in url: its card then shows On Amazon and a View on Amazon button. Until then it shows Coming soon. */
var AMAZON=[{id:'animals-AZ',url:''},{id:'animals-az',url:''},{id:'vehicles-AZ',url:''},{id:'vehicles-az',url:''},{id:'house-AZ',url:''},{id:'house-az',url:''},{id:'numbers',n:'Numbers 1 to 9',url:''}];
var SHORDER=['AZ','az','09'],SHVIEW='main',SHSET=null,SHTH={};
var SHBACK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>';
var SHOUT='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg>';
function shCSS(){if(G('sbshopcss'))return;var st=document.createElement('style');st.id='sbshopcss';var R='ui-rounded,"SF Pro Rounded","Arial Rounded MT Bold","Trebuchet MS",system-ui,sans-serif',S='system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif';st.textContent=[
'#grown.sbshop #grin{max-width:1120px;padding-top:2px}',
'#sbcat{--ink:#081130;--mut:#5f6679;--line:#ebe8e1;--soft:#f5f3ee;--acc:#FFC531;--good:#1c7c37;--goods:#e2f3e6;color:var(--ink);font:500 15px/1.4 '+S+';background:#fff;border-radius:20px;box-shadow:0 5px 0 rgba(8,17,48,.12);padding:16px 16px 26px;margin:0 0 26px}',
'@media (min-width:600px){#sbcat{padding:22px 24px 32px}}@media (min-width:900px){#sbcat{padding:26px 30px 36px}}',
'#sbcat h2,#sbcat h3{font-family:'+R+';margin:0}',
'#sbcat .chd{display:flex;align-items:flex-end;gap:12px;border-bottom:1px solid var(--line);padding:6px 0 11px;margin:0 0 18px}',
'#sbcat .chd h2{font-size:21px;font-weight:800;line-height:1.15}#sbcat .chd p{margin:4px 0 0;font-size:13px;color:var(--mut)}',
'#sbcat .ccn{margin-left:auto;flex:none;font-size:13px;color:var(--mut);white-space:nowrap;padding-bottom:1px}',
'#sbcat .cgr{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:26px 14px}',
'@media (min-width:600px){#sbcat .cgr{grid-template-columns:repeat(3,minmax(0,1fr));gap:28px 18px}}',
'@media (min-width:900px){#sbcat .cgr{grid-template-columns:repeat(4,minmax(0,1fr));gap:30px 22px}}',
'#sbcat .cc{display:flex;flex-direction:column;align-items:flex-start;gap:4px;min-width:0}',
'#sbcat .cph{position:relative;display:block;width:100%;aspect-ratio:1/1;background:var(--soft);border-radius:8px;overflow:hidden;cursor:pointer;margin-bottom:6px}',
'#sbcat .cph>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;transition:transform .3s ease}',
'#sbcat .cc:hover .cph>img,#sbcat .cph:active>img,#sbcat .cc:hover .cph>.cbk,#sbcat .cph:active>.cbk{transform:scale(1.04)}',
'#sbcat .cph>img.cov{inset:9% 11% 24%;width:78%;height:67%;object-fit:contain;mix-blend-mode:multiply}',
'#sbcat .cph>img.thm{inset:6%;width:88%;height:88%;object-fit:contain;mix-blend-mode:multiply}',
'#sbcat .cph .csb{position:absolute;left:50%;bottom:7%;transform:translateX(-50%);width:46%}#sbcat .cph .csb svg,#sbcat .cbk .sbbd svg{display:block;width:100%;height:auto}',
'#sbcat .cbg{position:absolute;top:9px;left:9px;z-index:1;background:var(--acc);color:var(--ink);font:800 10.5px/1 '+S+';letter-spacing:.07em;text-transform:uppercase;padding:5px 7px;border-radius:5px}',
'#sbcat .cbg.dk{background:var(--ink);color:#fff}#sbcat .cbg.lt{font:800 15px/1 '+R+';letter-spacing:0;text-transform:none;padding:6px 9px;background:var(--ink);color:#fff}',
'#sbcat .cdn{position:absolute;top:9px;right:9px;z-index:1;background:var(--goods);color:var(--good);font:800 11px/1 '+S+';padding:5px 7px;border-radius:5px}',
'#sbcat .cln{font-size:10.5px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--mut)}',
'#sbcat .cnm{font-size:16px;font-weight:700;line-height:1.25}',
'#sbcat .cpr{display:flex;flex-wrap:wrap;align-items:baseline;gap:1px 8px}#sbcat .cpr b{font-size:17px;font-weight:800}#sbcat .cpr span{font-size:13px;font-weight:600;color:var(--mut)}',
'#sbcat .cmt{font-size:12.5px;line-height:1.35;color:var(--mut)}',
'#sbcat .cft{margin-top:auto;padding-top:8px}',
'#sbcat .cbt{display:inline-flex;align-items:center;gap:6px;border:1.5px solid var(--ink);background:#fff;color:var(--ink);border-radius:999px;padding:9px 15px;font:700 13.5px/1 '+S+';cursor:pointer;text-decoration:none;-webkit-appearance:none;appearance:none}',
'#sbcat .cbt:hover,#sbcat .cbt:active{background:var(--ink);color:#fff}#sbcat .cbt[disabled]{border-color:var(--line);color:var(--mut);background:#fff;cursor:default}#sbcat .cbt svg{width:14px;height:14px}',
'#sbcat .cback{position:sticky;top:0;z-index:2;background:#fff;margin:-6px -16px 0;padding:6px 16px 12px;border-radius:20px 20px 0 0}',
'@media (min-width:600px){#sbcat .cback{margin:-8px -24px 0;padding:8px 24px 12px}}@media (min-width:900px){#sbcat .cback{margin:-8px -30px 0;padding:8px 30px 12px}}',
'#sbcat .cpill{border:0;background:var(--soft);color:var(--ink);border-radius:999px;padding:9px 15px 9px 10px;font:700 13.5px/1 '+S+';display:inline-flex;align-items:center;gap:3px;cursor:pointer}#sbcat .cpill svg{width:17px;height:17px}',
'#sbcat .cbk{position:absolute;left:21%;top:12%;width:58%;height:76%;border-radius:4px 10px 10px 4px;background:#fffaf0;box-shadow:inset 8px 0 0 var(--d),inset 10px 0 0 rgba(255,255,255,.55),0 10px 16px rgba(8,17,48,.14),0 2px 3px rgba(8,17,48,.12);overflow:hidden;transition:transform .3s ease}',
'#sbcat .cbk img{position:absolute;left:15%;top:7%;width:78%;height:62%;object-fit:contain;mix-blend-mode:multiply}#sbcat .cbk .sbbd{position:absolute;left:calc(50% + 4px);bottom:8%;transform:translateX(-50%);width:62%}',
'#sbcat .cempty{grid-column:1/-1;font-size:14px;color:var(--mut);padding:8px 0}',
'#sbcat button:focus-visible,#sbcat a:focus-visible{outline:3px solid #2F7BF5;outline-offset:3px}',
'@media (prefers-reduced-motion:reduce){#sbcat .cph>img,#sbcat .cbk{transition:none}#sbcat .cc:hover .cph>img,#sbcat .cph:active>img,#sbcat .cc:hover .cph>.cbk,#sbcat .cph:active>.cbk{transform:none}}'
].join('\n');document.head.appendChild(st)}
function shSets(){return window.SBSETS||[]}
function shCol(id){var r=null;shSets().forEach(function(cat){cat.cols.forEach(function(c){if(c.id===id)r={c:c,cat:cat}})});return r}
function shNine(){var r=null;shSets().forEach(function(cat){cat.cols.forEach(function(c){if(c.set==='09'&&!r)r={c:c,cat:cat}})});return r}
function shPrintable(c){var x=window.__sbx;try{return x&&x.printable?x.printable(c):[]}catch(e){return[]}}
/* one card: picture (with a corner label), the small grey line, the name, the price line, a detail line and a pill button */
function shCard(o){return'<article class="cc"><div class="cph" data-a="'+o.a+'" aria-hidden="true">'+o.pic+(o.bd?'<span class="cbg'+(o.bdc?' '+o.bdc:'')+'">'+esc(o.bd)+'</span>':'')+(o.done?'<span class="cdn">Finished \u2713</span>':'')+'</div>'+
 (o.line?'<div class="cln">'+esc(o.line)+'</div>':'')+'<h3 class="cnm">'+esc(o.n)+'</h3><div class="cpr"><b>'+esc(o.pr)+'</b>'+(o.sz?'<span>'+esc(o.sz)+'</span>':'')+'</div>'+(o.mt?'<div class="cmt">'+esc(o.mt)+'</div>':'')+
 '<div class="cft">'+(o.href?'<a class="cbt" href="'+esc(o.href)+'" target="_blank" rel="noopener">'+esc(o.bt)+SHOUT+'</a>':'<button class="cbt" type="button" data-a="'+o.a+'"'+(o.off?' disabled':'')+'>'+esc(o.bt)+'</button>')+'</div></article>'}
function shHead(h,p,n){return'<div class="chd"><div><h2>'+esc(h)+'</h2>'+(p?'<p>'+esc(p)+'</p>':'')+'</div>'+(n?'<span class="ccn">'+esc(n)+'</span>':'')+'</div>'}
function shBackPill(){return'<div class="cback"><button class="cpill" type="button" data-a="back">'+SHBACK+'Back</button></div>'}
function shWire(root,act){[].forEach.call(root.querySelectorAll('[data-a]'),function(el){el.onclick=function(){if(el.disabled)return;act(el.getAttribute('data-a'))}})}
function shTop(){var gi=G('grin');if(gi)gi.scrollTop=0}
function shMain(){var d=G('sbcat');if(!d)return;SHVIEW='main';
 d.innerHTML='<section>'+shHead('Shop','','')+'<div class="cgr">'+SHOP.map(function(x){
  return shCard({a:x.id,pic:'<img src="img/'+x.img+'.webp" alt="" loading="lazy" decoding="async">',bd:x.bd,bdc:x.dk?'dk':'',line:x.line,n:x.n,pr:x.pr,sz:x.sz,mt:x.mt,bt:x.bt})}).join('')+'</div></section>';
 shWire(d,function(a){if(a==='sheets')shSheets();else if(a==='books')shBooks();else open(a)})}
/* the free print sheets: first the sets, then the drawings in one set */
function shSheets(){var d=G('sbcat');if(!d)return;SHVIEW='sheets';SHSET=null;var cats=shSets(),L=[];
 SHORDER.forEach(function(set){cats.forEach(function(cat){cat.cols.forEach(function(c){if(c.set!==set)return;var n=shPrintable(c).length;if(n)L.push({c:c,cat:cat,n:n})})})});
 function draw(pg){d.innerHTML=shBackPill()+'<section>'+shHead('Print sheets','Free, for home or school. Pick a set, then a drawing.',L.length+' sets')+'<div class="cgr">'+(L.length?L.map(function(o,i){var p=pg&&pg(o.c);
   return shCard({a:'s'+i,pic:'<img class="cov" src="img/'+esc(o.c.cv)+'.webp" alt="" loading="lazy" decoding="async"><span class="csb">'+badge(o.c.set)+'</span>',bd:'Free',line:'Free sheets',n:o.c.n,pr:'Free',sz:o.n+' sheet'+(o.n===1?'':'s'),
    mt:p&&p.n?(p.l===3?'Every drawing in this set is done.':'Drawn so far: '+p.n+' of '+p.t+'.'):'',done:p&&p.l===3,bt:'Open'})}).join(''):'<p class="cempty">No sheets to print yet.</p>')+'</div></section>';
  shWire(d,function(a){if(a==='back')shMain();else{var o=L[+a.slice(1)];if(o)shSet(o.c)}})}
 draw(null);shTop();
 var x=window.__sbx;if(x&&x.load&&x.progress)x.load().then(function(){if(SHVIEW==='sheets'&&G('sbcat'))draw(function(c){try{return x.progress(c)}catch(e){return null}})},function(){})}
function shThumb(p,img){if(SHTH[p.key]){img.src=SHTH[p.key];return}var x=window.__sbx;if(!x||!x.colour)return;
 setTimeout(function(){if(!img.isConnected)return;var u='';try{u=x.colour(p,420)}catch(e){}if(u){SHTH[p.key]=u;img.src=u}},0)}
function shSet(c){var d=G('sbcat');if(!d||!c)return;SHVIEW='set';SHSET=c;var L=shPrintable(c);
 d.innerHTML=shBackPill()+'<section>'+shHead(c.n,'Tap a drawing to print its sheet: all its steps on one page, to follow on their own paper.',L.length+' sheet'+(L.length===1?'':'s'))+'<div class="cgr">'+L.map(function(o,i){
  return shCard({a:'p'+i,pic:'<img class="thm" alt="" data-i="'+i+'">',bd:o.s,bdc:'lt',line:'Free sheet',n:o.p.t||o.s,pr:'Free',sz:'A4 or US Letter',bt:'Print'})}).join('')+'</div></section>';
 [].forEach.call(d.querySelectorAll('img.thm'),function(im){var o=L[+im.getAttribute('data-i')];if(o)shThumb(o.p,im)});
 shWire(d,function(a){if(a==='back'){shSheets();return}var o=L[+a.slice(1)],x=window.__sbx;if(o&&x&&x.sheet)x.sheet(o.p).then(x.openSheet)});shTop()}
/* the Step by Draw books on Amazon */
function shBooks(){var d=G('sbcat');if(!d)return;SHVIEW='books';var nine=shNine();
 d.innerHTML=shBackPill()+'<section>'+shHead('Step by Draw books','Our step-by-step drawing books, one for every set. On Amazon.',AMAZON.length+' books')+'<div class="cgr">'+AMAZON.map(function(x,i){
   var o=x.id==='numbers'?nine:shCol(x.id),c=o&&o.c,cat=o&&o.cat,n=x.n||(c&&c.n)||'',st=x.id==='numbers'?'09':(c&&c.set)||'AZ';if(!n)return'';
   return shCard({a:'b'+i,pic:'<span class="cbk" style="--d:'+((cat&&cat.d)||'#8B5CF6')+'">'+(c&&c.cv?'<img src="img/'+esc(c.cv)+'.webp" alt="" loading="lazy" decoding="async">':'')+'<span class="sbbd">'+badge(st)+'</span></span>',
    bd:x.url?'':'Coming soon',bdc:'dk',line:'On Amazon',n:n,pr:x.url?'On Amazon':'Coming soon',sz:'',mt:'Step-by-step drawing book',href:x.url||'',bt:x.url?'View on Amazon':'Coming soon',off:!x.url})}).join('')+'</div></section>';
 shWire(d,function(a){if(a==='back')shMain();else{var x=AMAZON[+a.slice(1)];if(x&&x.url)window.open(x.url,'_blank','noopener')}});shTop()}
function shBack(){if(SHVIEW==='set')shSheets();else shMain();shTop()}
/* the top Back button goes back inside the shop first; on the shop itself it goes home as before */
document.addEventListener('click',function(e){var t=e.target;if(!t||!t.closest||!t.closest('#grback'))return;if(!G('sbcat')||SHVIEW==='main'||G('sbbook')||G('sbprwrap'))return;e.stopPropagation();e.preventDefault();shBack()},true);
function shWatch(){var gi=G('grin');if(!gi)return false;if(gi.__sbsh)return true;gi.__sbsh=1;
 function check(){var gr=G('grown');if(gi.querySelector('.gate')){if(gr)gr.classList.remove('sbshop');return}
  if(G('sbcat')||!gi.querySelector('.grc'))return;
  shCSS();if(gr)gr.classList.add('sbshop');gi.innerHTML='';var d=document.createElement('div');d.id='sbcat';gi.appendChild(d);shMain();shTop()}
 new MutationObserver(check).observe(gi,{childList:true});check();return true}
if(!shWatch()){var wn=0,wt=setInterval(function(){if(shWatch()||++wn>80)clearInterval(wt)},250)}
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&G('sbbook')){var pk=document.querySelector('#sbbook .bkpick');if(pk)pk.remove();else goBack()}});

window.__sbbook={open:open,close:close,books:loadBooks,newBook:newBook,pages:pagesOf,render:render,makePdf:makePdf,pdfBlob:pdfBlob,findCrop:findCrop,
 state:function(){return B},set:function(b){B=b},step:function(n){[step1,step2,step3,step4][n-1]()},pdf:function(){return PDF},PX:PX};
})();
