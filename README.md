# British Footprints: Istanbul - website

Landing page, privacy policy and support page for the **British Footprints: Istanbul** app
(iOS + Android), served by GitHub Pages. Plain HTML, CSS and one small script; no framework,
no cookies, no trackers, fonts self-hosted.

Live (after publishing): <https://mgmemik.github.io/british-footprints-web/>

| Page | Path |
|---|---|
| Home (marketing) | `/` |
| Privacy policy | `/privacy/` |
| Support | `/support/` |

English is the default; Turkish via the EN/TR switch (remembered in localStorage) or `?lang=tr`.

## URLs for the stores

**Do not change these paths later** - the stores point at them.

| Field | Value |
|---|---|
| App Store Connect > App Information > Privacy Policy URL | `https://mgmemik.github.io/british-footprints-web/privacy/` |
| App Store Connect > version > Support URL | `https://mgmemik.github.io/british-footprints-web/support/` |
| App Store Connect > version > Marketing URL (optional) | `https://mgmemik.github.io/british-footprints-web/` |
| Play Console > App content > Privacy policy | `https://mgmemik.github.io/british-footprints-web/privacy/` |
| Play Console > Store settings > Website | `https://mgmemik.github.io/british-footprints-web/` |
| Play Console > Store settings > E-mail | `app@save-all.com` |

The Turkish versions are the same URLs with `?lang=tr` (e.g. for the Turkish localization's
privacy URL in App Store Connect, if wanted).

## Publishing (GitHub Pages)

1. Create the public repo `mgmemik/british-footprints-web` (empty, no README).
2. `git remote add origin git@github.com:mgmemik/british-footprints-web.git && git push -u origin main`
3. Repo > Settings > Pages > Source: *Deploy from a branch*, branch `main`, folder `/ (root)`.
   Or: `gh api -X POST repos/mgmemik/british-footprints-web/pages -f "source[branch]=main" -f "source[path]=/"`
4. After a minute the site is at the URL above. Pages runs Jekyll, which only copies the HTML;
   `_config.yml` keeps `src/`, `tools/`, `README.md`, `RESULT.md` out, and `_screens/` is
   never published (folders starting with `_` are skipped; it is also git-ignored).
5. Optional: Google Search Console > add the URL prefix property and submit `sitemap.xml`.

## When the app is live: store links

The store buttons are placeholders: `href="#appstore"` and `href="#googleplay"` in
`src/partials/stores.html` (comments mark them). Replace them with
`https://apps.apple.com/app/id<APP_ID>` and
`https://play.google.com/store/apps/details?id=<PACKAGE_NAME>`, change the
`common.storeSoon` text in both language files (e.g. to an empty string or "Free on the App
Store and Google Play"), optionally add `"downloadUrl"` to the `MobileApplication` JSON-LD in
`src/index.html`, then run the build.

## Editing texts

- All texts live in `assets/i18n/en.json` and `assets/i18n/tr.json` (one file per language,
  same keys; values may contain simple inline HTML).
- Page structure lives in `src/*.html` and `src/partials/*.html`.
- After any change: `python3 tools/build.py` - it bakes the English text into
  `index.html`, `privacy/index.html`, `support/index.html` (what search engines see), checks
  that EN and TR have the same keys and that no store-banned words appear in titles, meta tags
  or headings. `python3 tools/build.py --check` only checks.
- `site.js` swaps in the Turkish texts at runtime.
- Do not edit the generated HTML files directly.

## Checking locally

```bash
python3 -m http.server 8000      # then open http://localhost:8000/ (and ?lang=tr, ?theme=light)
python3 tools/check_links.py     # local links, alt texts, balanced tags
python3 tools/shoot.py [filter]  # screenshots (EN/TR x dark/light x desktop/mobile) into _screens/
```

`?theme=light|dark` forces a theme for previews; otherwise the site follows the visitor's
choice (moon/sun button) or the system setting, dark by default.

## Images

Web copies made from the store art and app screenshots in `../research/` (WebP, all < 200 KB):
`hero-h2-*` (header H2), `app-s2-*` (search art S2), `og-image.jpg` (1200x630 crop of S2),
`screen-*` (dark/light app screens), `icon-*` + `favicon.ico` (app icon).
