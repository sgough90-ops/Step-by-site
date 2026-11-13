# Make it move: the child's own face on a film (13 Nov 2026)

These scripts made `public/mim-films/dx_tiger_t/face.json`. That file lets the app put a photo of the child's own
tiger drawing on the real-body tiger films, in place of the drawn face. Nothing here is published (only `public/` is).

They read the films' frames from a scratch folder (`/home/claude/work/frames/<film>/0001.jpg …`, made with
`ffmpeg -i <film>.mp4 -q:v 2 frames/<film>/%04d.jpg`) and write next to themselves. Change the paths at the top if needed.

Run them in this order:

1. `trackA.py`: a first guess of where the face is in every frame (SIFT from one clean frame, silly frame 240).
2. `trackB.py`: lines up ~300 frames on that guess and takes the median, giving a clean picture of the drawn face (`B_med.npy`) and how steady each pixel is (`B_dev.npy`).
3. `maskC.py`: the face's outline from the steady pixels (`C_mask.npy`).
4. `trackD.py <film> <first> <last>`: the accurate track per frame (SIFT from the clean face + ECC refinement, the best of several starts). Writes `trackD_<film>_<first>.json`; join them into `trackD.json` (one list of 525 frames per film).
5. `exportE.py`: per frame, the light on the face and what's in front of it (props differ from the face picture), saved as masks in `occE/`.
6. `rockF.py`: Starring role only. The grey rock looks like the dawn-lit muzzle, so the rock is tracked on its own and added as "in front" whenever the face is behind it.
7. `posterG.py`: the same for `poster.jpg`.
8. `packH.py`: packs it all into `face.json` (the per-frame maps, the light, the masks, the face outline and the poster).

Also made from the films: `silly.m4a`, `wonky.m4a`, `star.m4a` (`ffmpeg -i x.mp4 -vn -c:a copy x.m4a`). The app records the film with the
child's face while it plays and uses these as its sound.

**If the films are remade, run all of this again and re-make the .m4a files**, or the face won't sit on the new films.
The same steps work for another drawing whose films move one drawn picture around (check the frames: props in front
of the face need to differ from the face's own colours, or be tracked like the rock).

face.json layout: `W`,`H` = the face picture's size; `sil` = its outline (x,y pairs, 2 px bigger); `c`,`area` = its centre and size;
`paper` = its paper colour. For each film, `f[i]` is frame i (at 30 fps): `[a,b,c,d,e,f, red,green,blue light, mask]`, where
(x,y) in the face picture lands at (a·x+b·y+c, d·x+e·y+f) in the 720×1280 film, or 0 when the face isn't in shot; `mask` indexes `o`,
a half-size box `b:[x,y,w,h]` with run lengths `r` (0s and 1s alternating, 0s first) of what's in front of the face.
