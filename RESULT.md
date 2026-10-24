# RESULT: TASK-B-web (2026-10-24)

A static website for British Footprints: Istanbul is ready in `web/` (local git repo, branch
`main`, 4 commits, **not pushed**, no repo created, no gh commands). EN default + TR, dark
default + light, mobile first, no framework, no cookies, no trackers, self-hosted fonts.

Note: the brief said `web/` already existed as a git repo; it did not, so I created it and ran
`git init -b main`.

## Pages and URLs (after GitHub Pages is switched on)
| Page | URL | Contents |
|---|---|---|
| Landing / marketing | https://mgmemik.github.io/british-footprints-web/ | H1 "The British footprints of Istanbul, on foot", promise, store buttons (placeholders), stats (51 places, 7 walks, 104 pictures, 2 languages), What's inside (S2 art + 6 features: places, walks, engravings, offline pictures, Apple/Google Maps hand-off, location stays on phone), Free vs one-time unlock (no price), 5 screenshots, 8 FAQs, closing CTA |
| Privacy policy | https://mgmemik.github.io/british-footprints-web/privacy/ | summary card + 15 sections (see below), effective October 2026 |
| Support | https://mgmemik.github.io/british-footprints-web/support/ | app@save-all.com + 9 FAQs |

Turkish: same URLs with `?lang=tr` (hreflang en/tr/x-default on every page and in the sitemap).
Paste list for App Store Connect / Play Console: `web/README.md`.

### Privacy policy - matches app/RESULT-telemetry.md
Who (thebarnapp = sole proprietorship of Mehmet Gökhan Memik, Istanbul; no address or ID),
location (on device only; the only derived value sent is `inIstanbul` yes/no/unknown, 30 km),
TelemetryDeck GmbH (Germany): every signal group in plain words, the 5 context keys in a table
(`channel`, `entitled`, `uiLanguage`, `theme`, `inIstanbul`), SDK technical details and
session/new-install signals, salted hashed random ID, never search text/coordinates/price,
test vs live data, the Settings opt-out (one last signal, then SDK stopped), legal basis
(legitimate interest); purchases (Apple/Google, no payment data); OSM tiles see the IP;
pictures bundled; Maps hand-off sends the destination; what stays on the phone; no accounts/
ads/tracking/IDFA; this website (no cookies, localStorage only for language/theme, GitHub
Pages logs); children; rights (GDPR, UK GDPR, KVKK); content sources and licences (Wikimedia
Commons PD/CC0/CC BY/CC BY-SA 2.0-4.0, OSM ODbL, OFL fonts, pointer to Settings › Credits &
licences); changes; contact.

### Support FAQs
Restore (Settings › Full access › Restore purchases, silent check at start, Redeem code on
iPhone), Family Sharing (careful wording, see open questions), offline, location permission
(paths on iOS and Android), directions (Google Maps whole walk, Apple Maps one stop at a time,
iPhone asks once / Settings), turning statistics off, language and theme, reporting a factual
error, "bought but still locked". Button names match the app's EN/TR strings.

## SEO
Title, meta description, canonical, OG + Twitter cards (1200x630 `og-image.jpg` from S2),
JSON-LD `MobileApplication` (TravelApplication, iOS+Android, en/tr, free, publisher
thebarnapp) + `FAQPage` on the landing and the support page, `sitemap.xml` (6 URLs with
hreflang alternates), `robots.txt`, favicon/apple-touch icon/manifest from icon-512.
Copy targets the phrases from `research/aso/data` (self-guided walking tour, Istanbul
history, Crimean War Istanbul / cemetery, Scutari, offline map, Victorian engravings).
`research/aso/web/` was empty, so the copy is my own; it sits in `assets/i18n/en.json` and
`tr.json` (one file per language) and is easy to swap: edit the JSON, run
`python3 tools/build.py`.
Store rules: the build fails if titles/meta/headings contain James Bond, 007, Agatha
Christie, Orient Express, Pera Palace, Nightingale, occupation/işgal, flag/bayrak; a grep finds
none of these words anywhere in the pages or texts. No flags, no occupation content, no
price. No screenshot with the occupation flag markers or the Christie/Bond pages was used.

## Placeholders
- `href="#appstore"` and `href="#googleplay"` store buttons (`src/partials/stores.html`, used
  twice on the landing page; HTML comments mark where the real URLs go) plus the line
  "Coming soon to the App Store and Google Play." (`common.storeSoon`). Steps in README.
- JSON-LD has no `downloadUrl` yet (add it with the App Store URL).

## Structure
- `src/*.html`, `src/partials/*.html` → `tools/build.py` → `index.html`, `privacy/index.html`,
  `support/index.html` (English baked in; TR swapped in by `assets/site.js` from
  `assets/i18n/tr.json`). `--check` mode verifies EN/TR keys, unused keys, banned words, staleness.
- `assets/styles.css` (Traveller's Folio tokens from DESIGN.md: ink/cream, cobalt, turquoise,
  coral, brass; tile rule, calling cards, plate frames, tickets), `assets/fonts/` (Playfair
  Display + Lora subset to Latin + Turkish, WOFF2, 37-52 KB each, OFL texts included),
  `assets/img/` (all images < 200 KB; hero H2 195 KB at 1920 px).
- Theme: inline head script sets the theme before paint: `?theme=` (previews), else saved
  choice, else system (dark unless the system asks for light); moon/sun toggle.
- Accessibility: skip link, landmarks, `aria-current`, `aria-pressed` on EN/TR, visible
  turquoise focus ring, alt texts on every image (translated), `<details>` FAQs, contrast
  per DESIGN.md (brass only for rules/icons).
- `_config.yml` keeps `src/`, `tools/`, README, RESULT out of Pages; `_screens/` is
  git-ignored and never published.

## Verification
- `python3 tools/build.py` → `ok: 180 keys, en/tr in sync`; `--check` passes.
- `python3 tools/check_links.py` → `ok` (all local href/src/srcset targets exist, tags
  balanced, no img without alt, no duplicate ids). External links (Wikimedia Commons, GitHub
  privacy statement, OSMF privacy policy, OSM copyright) answered HTTP 200.
- Screenshots: `python3 tools/shoot.py` served the site locally and took 24 headless-Chrome
  shots into `web/_screens/` (3 pages x EN/TR x dark/light x desktop 1280 / mobile 390).
  I looked at the landing page (EN dark desktop and mobile, TR light desktop, EN light
  gallery), privacy (EN dark desktop) and support (TR light mobile). Fixes made after
  looking: features grid 3x2 instead of 4+2; screenshot gallery fits the desktop width
  instead of cutting off the fifth phone; mobile shots now render in a 390 px iframe
  (headless Chrome cannot make windows narrower than ~500 px); longer render time so the
  lazy images appear.
- Not tested: real Safari/iOS and Android browsers (only headless Chrome); Lighthouse was not run.

## Open questions (for A / the owner)
1. **Family Sharing** for `full_unlock` is not decided (off in the local StoreKit config). The
   support answer points to the store page and does not promise either way; reword it once
   it is decided.
2. Store buttons are plain styled buttons, not the official Apple/Google badges. When the
   app is live, you could swap in the official badge artwork (Apple's and Google's badge
   rules apply).
3. Support says "Settings › About" shows the app version. The app has a "Version" string,
   but I did not check that it sits under About.
4. The privacy text calls TelemetryDeck "based in Germany (EU)" and says it "states that it
   does not store" IP addresses, following its public statements. Check this against your
   TelemetryDeck agreement/DPA if you want to be sure.
5. The App Store privacy label and Play Data safety form still need the changes listed in
   `app/RESULT-telemetry.md` ("What A must still do"). The website policy already describes
   the analytics.
6. Publishing: the owner creates the public repo `mgmemik/british-footprints-web`, A pushes
   and switches Pages on (README steps). Optionally submit the sitemap in Search Console.
