# Copilot Instructions — concretecalc. (v1 — 2026-11-20)

> **How to use this file:** In VS Code, save it as `.github/copilot-instructions.md` in the project root. Copilot will then follow these rules automatically on every prompt. You can also paste the whole file into a Copilot Chat prompt when starting a new session.
>
> **Status, verified 2026-11-20 against the live files on disk:** this file describes the v1 launch exactly as built. The site is the US sister of the German `maßklar.` hub — same stack, same page shape, new colors, US English, imperial units first.

---

## 1. What this site is

- **Project:** `concretecalc.` — a free US concrete calculator hub.
- **Live pages (17, 2026-11-20):** homepage (main tool) + 8 per-shape tool pages (`slab/`, `footing/`, `sonotube/`, `stairs/`, `wall/`, `curb/`, `column/`, `cubic-yard/`) + guides index + 7 guide posts (`guides/cubic-feet-in-a-yard/`, `guides/curing-time/`, `guides/bags/`, `guides/weight/`, `guides/mix-ratio/`, `guides/cost/`, `guides/thickness/`).
- **Purpose:** Each tool answers one question: how much concrete do I need? The homepage calculator covers 8 shapes with a waste allowance, bag counts, weight, cost, and multi-pour job totals. Per-shape pages are the same calculator pre-set to one shape, with their own worked example and FAQ.
- **Audience:** United States (language `en`, locale `en-US`). Users are non-technical — homeowners, DIYers, small contractors.
- **Reference to beat:** `concretecalculatormax.com` (8 shapes, per-field units, bag sizes, cost estimator, waste slider, density presets, full guide, FAQ). Same usefulness, but cleaner, faster, and simpler — plus the gap feature nobody else has: multi-pour rows that total a whole job into one order volume. Do NOT copy their text or design.
- **Goal:** A hub of genuinely useful tools that rank in the US. No blog, no login, no account, no backend, no paywall. Money comes later, from ads — never from charging for a calculator.
- **Footers:** "A product of Hastle". Never write "Hastle Inc.".

## 2. Tech stack — DO NOT change this

- **Vanilla HTML + CSS + JavaScript only. No framework, no build step, no npm.**
- **NEVER add:** Tailwind, Bootstrap, React, Vue, jQuery, any JS library, any CSS framework, any bundler, any image asset.
- **Files per tool (keep exactly this shape):**
  - `index.html` — structure + content + SEO meta (one folder per tool/page)
  - `app.js` — that page's calculator logic, loaded with `defer`
  - Shared: root `styles.css` (one stylesheet for the whole hub, currently `styles.css?v=1`) and root `fonts/`
  - Root `index.html` is the homepage (main tool + full guide + FAQ + tool/guide grids); root `sitemap.xml` lists every page — **update it when a page is added** (17 URLs as of 2026-11-20).
- **Fonts — SELF-HOSTED, no Google Fonts:**
  - Display/headings: **Bitter** (variable, wght 100–900, serif)
  - Body: **DM Sans** (variable, wght 100–1000)
  - Numbers/labels: **DM Mono** (static 400 + 500 only)
  - Files live in `fonts/` as woff2 (`bitter-latin.woff2`, `dm-sans-latin.woff2`, `dm-mono-400/500-latin.woff2`), loaded with `@font-face` + `font-display: swap`. **Never re-add a Google Fonts import.**
- **No external JS.** No analytics, no tracking, no cookies. Every calculator must work fully offline once loaded.
- **No images.** All visuals are pure CSS. Never replace them with `<img>`, SVG files, or emoji illustrations.
- **Loading skeleton:** every page has an inline `<head>` skeleton (`#page-skeleton`, `html.is-loading` / `html.is-ready`) so the page paints before the stylesheet arrives. Keep it; do not remove it to "simplify".
- **localStorage — ALLOWED:** the homepage calculator saves its inputs under `concretecalc_main_v1`; per-shape pages save theirs under their own `concretecalc_<shape>_v1` key. Inputs are restored on load; Reset clears the stored key. Never store anything but the user's own inputs on their own device.
- **Shareable URLs:** the homepage writes its shape + inputs into the URL query string (`?shape=slab&slab-length=10&...`) on every input, and reads them back on load (URL wins over localStorage). Per-shape pages do the same for their fields.

## 3. Design system — keep it exact

These are locked. Do not invent new colours, fonts, or a new style.

```css
--paper: #f3f1ea;       /* page background */
--white: #fffefa;       /* cards */
--ink: #22272a;         /* text */
--muted: #5c666b;       /* secondary text */
--slate: #33414b;       /* primary / brand */
--slate-dark: #232e36;  /* dark sections, hover */
--line: #e3e1d8;        /* borders */
--amber: #f0a500;       /* accent only — brand period, calculate button, small details */
--amber-dark: #cf8f00;
--amber-light: #f7c948;
--error: #b34035;
```

- **Brand:** `concretecalc.` — lowercase, `cc` mark in an amber rounded square, amber period. Never write "ConcreteCalc", "Concrete Calculator" as a brand, or add a different logo.
- **Tone of the design:** calm, paper-like, editorial. Small mono uppercase eyebrows (`letter-spacing: 1.15px`, 10px), big tight Bitter headlines, generous whitespace, thin 1px borders, soft shadows only (`0 18px 48px #293e3010` on the calculator).
- **Border radius:** 4–10px only. No pill buttons, no big rounded cards.
- **Inputs:** 48px high (`.input-with-unit`), 5px radius.
- **Calculate button:** amber background, dark slate text, **60px high**, 8px radius, bold 17px. Hover = `--amber-dark`. This is the one big button on the page — do not shrink it.
- **Header CTA:** amber, 44px min-height. Header itself: 64px min-height (60px below 680px).
- **Animations:** result flash `.35s` (`.result-panel.flash`), card stagger `.4s` (`.example-card`, `card-in`), page-in `.5s`. Input transitions stay `.2s`. Keep `prefers-reduced-motion: reduce` (already in CSS).
- **Do NOT add:** dark mode, popups, modals, toasts, or confetti.

## 4. Page structure — homepage (main tool)

Keep this order. New tools copy the shape (hero → calculator → examples/table → guide → practice → FAQ → more tools), adapted to their own subject.

1. **Header (64px):** brand left, nav centre (`Calculator`, `Slab`, `Cubic yard`, `Guides`), CTA right (`Calculate now ↗`). Nav hides below 680px.
2. **Hero:** compact tool-page hero — eyebrow `Free concrete calculator`, H1 `Concrete Calculator. / How much do you need?`, GEO description (the direct answer: a 10×10 ft slab at 4 in needs 1.23 yd³). The hero example must always be mathematically correct. **The GEO paragraph stays visible on phones** — do not hide it to save space (fixed 2026-11-20; the German site hid it and that was wrong here).
3. **Calculator (`#calculator`):** 8 shape tabs (`Slab`, `Footing`, `Column`, `Wall`, `Stairs`, `Curb & gutter`, `Circular pad`, `Monolithic slab`) — Column has a Square/Round toggle inside. Every length input has its own unit picker (ft/in/yd/m/cm/mm). Live auto-calc on input; the result always shows ordered yd³, the "that is also" line (ft³ · m³), net/waste rows, weight, and bag counts for 40/50/60/80 lb. Waste slider 0–15% (default 10%). Density segmented (Standard 150 / Reinforced 156 / Lightweight 110 lb/ft³) — affects weight only. Cost estimator: optional price per cubic yard and price per 80 lb bag — cost rows appear only when a price is entered. **Multi-pour:** "Add to job" appends the current pour to a job list (max 12); the job total sums all pours net, applies the waste slider once, and shows the ordered total, weight, and cost.
4. **Examples (`#examples`):** 3 cards only — Patio slab `10 × 10 ft, 4 in · 1.23 yd³`, Driveway `12 × 30 ft, 6 in · 6.67 yd³`, Footing run `40 ft, 18 × 12 in · 2.22 yd³`. All three must be correct. Cards are buttons that autofill the calculator.
5. **Common pours table (`#common-pours`, "How much concrete do I need?"):** 10 rows, net volume before waste — patio 10×10×4″ 1.23 yd³, patio 12×12×4″ 1.78, driveway 10×20×6″ 3.70, driveway 12×30×6″ 6.67, sidewalk 3×30×4″ 1.11, garage floor 20×20×4″ 4.94, footing 40 ft 18×12″ 2.22, post hole 12″×4 ft 0.12, round column 12″×8 ft 0.23, wall 20×8×8″ minus door 3.43. Every value must be verified by calculation. Clicking a row fills the calculator with that size.
6. **Guide (`#how-it-works`, dark slate):** all formulas in the formula card (slab/footing, round column/pad, wall, stairs) + 5 steps (measure, inches→feet, multiply to ft³, divide by 27, add waste and order). Every worked example must be correct.
7. **Practice (`#practice`, "Two quick checks"):** 2 tasks with solutions hidden in `<details>`: 12×12 ft patio at 4 in = 1.78 yd³ (1.96 with 10% waste); 60 ft footing 12×8 in = 1.48 yd³ (1.63 with 10% waste). Solutions must be recomputed, never copied from elsewhere.
8. **FAQ:** 14 questions on the homepage (use `<details>/<summary>`, no JS accordion). Per-shape pages have 5 each, guide posts 5 each. Never mention "5th grader" or any grade level anywhere on the site, even though the copy is written simply enough for one.
9. **More tools + guides:** plain-text tool cards linking to all 8 per-shape pages and all 7 guides. **Footer:** brand, tagline `Concrete calculator — yards, bags, weight, and cost.`, `© <current year> concretecalc` (year set by JS, never hardcode the year), "A product of Hastle".

## 5. Sacred numbers — verify every one by hand before calling anything done

These are the numbers the whole site stands on. If a page contradicts one, the page is wrong.

- 1 yd³ = 27 ft³ ≈ 0.765 m³; 1 m³ ≈ 1.308 yd³ (35.31 ft³).
- 10′ × 10′ × 4″ slab = 33.33 ft³ = **1.23 yd³**; at 6″ = **1.85 yd³**.
- Bags per yard: 40 lb → **90**, 50 lb → **72**, 60 lb → **60**, 80 lb → **45**. Yields: 0.30 / 0.375 / 0.45 / 0.60 ft³.
- Density: standard 150 lb/ft³ → 1 yd³ ≈ **4,050 lb**; reinforced 156 → 4,212 lb; lightweight 110 → 2,970 lb.
- Waste: 5–10% clean pours, 10–15% rough ground.
- Mix 1:2:3 ≈ 17% cement / 33% sand / 50% aggregate by volume (literal parts split: 1 of 6 parts cement, 2 of 6 sand, 3 of 6 aggregate).
- Cure: walk 24–48h, drive 7 days, full strength 28 days.
- Coverage: 1 yd³ at 4″ covers **81 sq ft**; at 6″ 54 sq ft; at 2″ 162 sq ft; at 3″ 108 sq ft; at 8″ 40.5 sq ft; at 12″ 27 sq ft.
- Shape formulas: slab/footing L×W×T; round column/pad πr²×H; wall (L×H − openings)×T; stairs W×tread×riser×n(n+1)/2 (solid to grade); curb L×(curbW×curbH + gutterW×gutterT); monolithic slab (L×W×T) + 2(L+W)×edgeW×edgeD.
- **Round results like a person measures** — 2 decimals for yd³, whole numbers for bags (always round UP), commas for thousands, periods for decimals (en-US). Never six decimals.

## 6. SEO + content rules

- **Titles ≤ 60 chars, main keyword first. Descriptions ≤ 160 chars.** Count them in code, not by eye.
- **Exactly one H1 per page, H1 first, no skipped heading levels.**
- Every tool page: title → GEO paragraph (direct fact-checked answer in 2–3 short sentences under the H1) → tool → examples/table → guide → FAQ → footer.
- **Schema:** FAQPage + HowTo + BreadcrumbList JSON-LD where they fit; WebApplication on tool pages, Article on guides. FAQ visible text must be byte-identical to the FAQPage JSON-LD answers.
- Plain-text cross-links between pages (no cards everywhere). No keyword stuffing. Never invent facts, statistics, "most popular" claims, or reviews. Never state a price as a fact — prices vary by region; say so and point to the cost estimator.
- Number formatting: en-US. Canonical URLs use the GitHub Pages domain `https://codeshifter-git.github.io/concretecalc/`.
- Guide posts: one main keyword + related keywords explained in the post, step-by-step, concise, plain US English.

## 7. QA checklist (run before any deploy)

- **Math:** run the QA cases in `~/workspace/qa-concretecalc/` — slab 10×10×4″ → 1.23 yd³, bag counts, all 8 shape formulas, per-page worked examples. Recompute, don't copy.
- **Real Chromium (NOT jsdom alone)** at 1920, 1280, 768, 390: no horizontal scroll, no overlapping text, tool above the fold on the homepage at all widths. Headless Chromium is `/opt/meta-chromium/chrome`; use the CDP pattern with the Hatch WebGL policy flags (see `~/AGENTS.md` — the policy file `/tmp/hatch-webgl-policy.txt` is wiped on restart; recreate it as one line `hatch-webgl-all-origins-v1`, sha256 `8097045f0459c96c4cdc76e3a1af4e0f43f640b4b59c43d6db35e3641c0264c6`).
- **OpenSEO audit** when live (project `ConcreteCalc` id `d60218c7-beba-46bb-ba55-e583bd9a381e`, market 2840/en; audits are free) — report issues, fix, re-run.
- **Never claim done if any QA check failed** — report the failure plainly.
