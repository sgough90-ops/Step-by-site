import cv2, numpy as np, json
FR='/home/claude/work/frames'
r=json.load(open('trackA.json'))
BX0,BY0,BX1,BY1=150,500,580,950
W,H=BX1-BX0,BY1-BY0
T=np.array([[1,0,-BX0],[0,1,-BY0],[0,0,1]],float)  # ref -> box coords
sel=[]
for film,out in r.items():
    for i,o in enumerate(out):
        if o and o['M'] and o['n']>=250: sel.append((film,i+1,np.array(o['M'])))
print('frames',len(sel))
sel=sel[::3]
stack=[]
core=np.zeros((H,W),np.uint8);cv2.ellipse(core,(363-BX0,724-BY0),(120,130),0,0,360,255,-1)
refbox=cv2.imread(f'{FR}/silly/0240.jpg')[BY0:BY1,BX0:BX1].astype(np.float32)
for film,i,M in sel:
    im=cv2.imread(f'{FR}/{film}/{i:04d}.jpg')
    M3=np.vstack([M,[0,0,1]])
    # box coords -> frame: M3 @ inv(T)
    A=(M3@np.linalg.inv(T))[:2]
    w=cv2.warpAffine(im,A,(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR,borderValue=(0,0,0)).astype(np.float32)
    valid=cv2.warpAffine(np.full(im.shape[:2],255,np.uint8),A,(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_NEAREST)
    g=[np.median(refbox[...,c][core>0]/np.maximum(w[...,c][core>0],1)) for c in range(3)]
    w=w*np.array(g)[None,None,:]
    w[valid==0]=np.nan
    stack.append(w)
S=np.stack(stack)
med=np.nanmedian(S,axis=0)
dev=np.nanmedian(np.abs(S-med[None]),axis=0).mean(axis=2)
np.save('B_med.npy',med);np.save('B_dev.npy',dev)
cv2.imwrite('B_med.png',np.nan_to_num(med).clip(0,255).astype(np.uint8))
d=(dev/ max(1,np.nanpercentile(dev,99))*255).clip(0,255).astype(np.uint8)
cv2.imwrite('B_dev.png',d)
print('dev pct',np.nanpercentile(dev,[10,50,90,99]))
