# STEP BY website

The live site at step-by.com. Files in `public/` are published by Cloudflare automatically when this repository changes.

Updates are published automatically by Cloudflare when Claude pushes to `main`.

Since 12 Nov 2026 the site is just Step by Draw:

- The app is `public/draw/index.html` (it uses `<base href="/">`, so its pictures and scripts sit at the top of `public/`). Keep making app changes there.
- `public/_redirects` serves that app at `/`, so step-by.com opens straight on the Draw home. `/draw/` still works too.
- `public/index.html` is only a fallback that sends people to `/draw/` if the `_redirects` rule is ever missing.
- Old Step By (`public/old/`) and Step by Block (`public/block/`) moved to the Steps Forward games site. Their old addresses on step-by.com now go to the Draw home.

## tools/
Scripts that are not published (only `public/` is). `tools/mim-face/` made the tiger films' face.json (see its README).
