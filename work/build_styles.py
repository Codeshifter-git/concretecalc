#!/usr/bin/env python3
"""Build concretecalc/styles.css from the massklar stylesheet.

Token swap only: green palette -> slate, orange accent -> safety amber,
paper/ink -> warm concrete tones. Layout, class names and breakpoints are
kept exactly (they are proven). New concrete-specific components are
appended at the end.
"""
import re
from pathlib import Path

SRC = Path("/home/hatch/workspace/github-demos/massklar/styles.css")
DST = Path("/home/hatch/workspace/github-demos/concretecalc/styles.css")

text = SRC.read_text()

# --- variable renames (do these first, before hex swaps) ---
text = text.replace("var(--green-dark)", "var(--slate-dark)")
text = text.replace("var(--green)", "var(--slate)")
text = text.replace("var(--orange-dark)", "var(--amber-dark)")
text = text.replace("var(--orange-light)", "var(--amber-light)")
text = text.replace("var(--orange)", "var(--amber)")
text = text.replace("var(--lime)", "var(--amber-pale)")

# --- hex swaps, longest first (alpha-suffixed values keep their suffix) ---
HEX = {
    "#f5f4ed": "#f3f1ea",  # paper
    "#fffefa": "#fffdf8",  # cards
    "#fffdf6": "#fffdf8",
    "#fafaf5": "#faf8f2",
    "#f8f9f4": "#f8f7f1",
    "#1d2925": "#22272a",  # ink
    "#5a6a62": "#5c666b",  # muted
    "#4f5f56": "#4a545a",
    "#64716c": "#646e75",
    "#849283": "#7f8a90",
    "#8d9991": "#8a939a",
    "#87918a": "#8a939a",
    "#9aa39b": "#9aa2a8",
    "#72836d": "#7d8890",
    "#8a938c": "#8a939a",
    "#89958c": "#8a939a",
    "#34443b": "#2c3841",
    "#245c48": "#33414b",  # slate primary
    "#193f34": "#232e36",  # slate dark
    "#21483c": "#2a3742",
    "#254c40": "#2e3d47",
    "#426055": "#46565f",
    "#49675c": "#4c5b64",
    "#355849": "#33414b",
    "#26352f": "#232e36",
    "#293e30": "#2b3338",  # shadow tint
    "#d7ed7b": "#f2d98c",  # pale amber (was lime)
    "#e4edcf": "#f6ecd2",
    "#edf2e4": "#f4ecda",
    "#eef1e6": "#f4efe2",
    "#f1f5e9": "#faf3df",
    "#f3f5ec": "#f5f1e6",
    "#e6ecdc": "#eee6cf",
    "#dce9c7": "#f2e2b0",
    "#fbeedd": "#fbefc9",
    "#fbeedf": "#fdf3da",
    "#e9eae0": "#ebe8dd",
    "#f4f3ea": "#f2f0e6",
    "#eaece3": "#ece9df",
    "#e6e7dd": "#e6e4d8",
    "#e7e8df": "#e6e3d8",
    "#eef0e9": "#efece2",
    "#eff0e9": "#efece2",
    "#e2e7dc": "#e3dfd2",
    "#cbd6c3": "#d9cfb4",
    "#d6dfc9": "#e0d9c2",
    "#f1f0e2": "#f0eee3",
    "#e9e5d6": "#e6e1d2",
    "#82a993": "#7d94a3",
    "#76a876": "#7d9b7a",  # valid-state green (kept greenish, desaturated)
    "#98ae9d": "#8d9aa3",
    "#aebfb2": "#a7b0b5",
    "#afbeb3": "#a7b0b5",
    "#c2cec5": "#bcc2c6",
    "#c0cdc4": "#bcc2c6",
    "#e79a62": "#f0a500",  # amber accent
    "#d9824a": "#cf8f00",  # amber dark
    "#eda878": "#f7c948",  # amber light (text on dark slate)
    "#e09059": "#d99a00",
}
for old, new in sorted(HEX.items(), key=lambda kv: -len(kv[0])):
    text = text.replace(old, new)

# --- :root token block: rename + new values ---
text = text.replace(
    """  --paper: #f3f1ea;
  --white: #fffdf8;
  --ink: #22272a;
  --muted: #5c666b;
  --error: #b34035;
  --green: #33414b;
  --green-dark: #232e36;
  --lime: #f2d98c;
  --line: #e4e6dc;
  --orange: #f0a500;
  --orange-dark: #cf8f00;
  --orange-light: #f7c948; /* same accent, lighter — for text on dark green (passes contrast) */""",
    """  --paper: #f3f1ea;       /* warm concrete paper */
  --white: #fffdf8;       /* cards */
  --ink: #22272a;         /* charcoal text */
  --muted: #5c666b;       /* secondary text */
  --error: #b34035;
  --slate: #33414b;       /* primary / brand */
  --slate-dark: #232e36;  /* dark sections, hover */
  --amber-pale: #f2d98c;  /* pale amber highlight */
  --line: #e3e1d8;        /* borders */
  --amber: #f0a500;       /* accent only — brand period, calculate button, small details */
  --amber-dark: #cf8f00;
  --amber-light: #f7c948; /* same accent, lighter — for text on dark slate (passes contrast) */""",
)

# The hero comment still says "green" in one place; fix wording.
text = text.replace("/* same accent, lighter — for text on dark green (passes contrast) */", "")

# Centered hero (2026-11-20): the base hero was a two-column grid with
# asymmetric padding (12.2% right, 14% left), which left the H1 7px
# off-center at 1280px. Single column, symmetric padding, centered text.
text = text.replace(
  ".hero { position: relative; min-height: 480px; display: grid; grid-template-columns: 1fr 1fr; align-items: center; padding: 48px 12.2% 60px 14%; overflow: hidden; }",
  ".hero { position: relative; min-height: 480px; display: grid; grid-template-columns: 1fr; align-items: center; padding: 48px 13% 60px; overflow: hidden; text-align: center; }",
)
text = text.replace(
  ".hero-description { max-width: 430px; margin: 22px 0 28px;",
  ".hero-description { max-width: 430px; margin: 22px auto 28px;",
)
text = text.replace(
  ".tool-page .hero-description { margin: 14px 0 0; }",
  ".tool-page .hero-description { margin: 14px auto 0; }",
)
assert "grid-template-columns: 1fr 1fr; align-items: center; padding: 48px 12.2% 60px 14%" not in text, "hero centering replace did not apply"
assert "margin: 22px auto 28px" in text and "margin: 14px auto 0" in text, "hero description centering did not apply"

# --- append concrete-specific components ---
text += """
/* ============ concretecalc. additions ============ */
/* Shape tabs — 8 shapes, wrapping button row (the 3-way segmented control
   from the German site does not fit 8 shapes). */
.shape-tabs { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 21px; }
.shape-tab { min-height: 44px; padding: 8px 14px; border: 1px solid #e3dfd2; border-radius: 20px; background: #fff; color: var(--slate); font: 600 13px var(--sans); cursor: pointer; transition: border-color .2s, background .2s; }
.shape-tab:hover { border-color: var(--slate); background: #faf3df; }
.shape-tab[aria-pressed="true"] { border-color: var(--slate); background: var(--slate); color: #fffdf8; }
/* Shape field groups: only the active shape's fields are shown. */
.shape-fields { display: none; }
.shape-fields.is-active { display: grid; }
/* Waste slider + density segmented row */
.calc-options { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 18px; }
.calc-options .field label { display: block; margin-bottom: 10px; color: #4a545a; font-size: 14px; font-weight: 600; letter-spacing: .2px; }
.waste-row { display: flex; align-items: center; gap: 12px; height: 48px; }
.waste-row input[type="range"] { flex: 1; accent-color: var(--slate); }
.waste-value { min-width: 52px; text-align: right; color: var(--ink); font: 500 16px var(--mono); }
.density-segmented { display: flex; padding: 4px; border-radius: 8px; background: #f4efe2; }
.density-segmented button { flex: 1; min-height: 40px; padding: 6px 4px; border: 0; border-radius: 6px; background: transparent; color: #5c666b; font: 600 12px var(--sans); cursor: pointer; }
.density-segmented button[aria-pressed="true"] { background: var(--white); color: var(--slate-dark); box-shadow: 0 2px 8px #2b333820; }
/* Cost inputs */
.cost-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 18px; }
/* Multi-pour job list (homepage only) */
.pour-list { display: flex; flex-direction: column; gap: 10px; margin-top: 18px; }
.pour-row { display: grid; grid-template-columns: 1fr auto auto auto; gap: 10px; align-items: center; padding: 12px 14px; border: 1px solid #e6e3d8; border-radius: 8px; background: #fff; }
.pour-row .pour-label { font: 600 14px var(--sans); }
.pour-row .pour-vol { color: var(--slate); font: 500 14px var(--mono); }
.pour-remove { min-height: 44px; padding: 0 10px; border: 0; background: transparent; color: var(--error); font: 600 13px var(--sans); cursor: pointer; }
.pour-add { min-height: 44px; margin-top: 10px; padding: 0 16px; border: 1px dashed #c9c4b4; border-radius: 8px; background: transparent; color: var(--slate); font: 600 14px var(--sans); cursor: pointer; }
.pour-add:hover { border-color: var(--slate); background: #faf3df; }
.pour-total { margin-top: 14px; padding: 16px; border-radius: 8px; background: var(--slate-dark); color: #fffdf8; }
.pour-total .pour-total-label { color: #bcc2c6; font: 500 11px var(--mono); text-transform: uppercase; letter-spacing: .8px; }
.pour-total .pour-total-value { margin: 4px 0 2px; font: 700 28px var(--display); }
.pour-total p { margin: 0; color: #bcc2c6; font-size: 14px; }
/* Bag + weight + cost result rows */
.result-rows { display: grid; grid-template-columns: 1fr 1fr; gap: 8px 20px; margin: 0 0 12px; }
.result-row { display: flex; justify-content: space-between; gap: 10px; padding: 8px 0; border-bottom: 1px solid #e6e3d8; font-size: 14px; }
.result-row:last-child { border-bottom: 0; }
.result-row span:first-child { color: #4a545a; }
.result-row span:last-child { color: var(--ink); font: 500 14px var(--mono); text-align: right; }
/* Slab hero visual — pure CSS slab with dimension labels (homepage only) */
.slab-card { position: relative; z-index: 1; width: min(390px, 100%); padding: 22px; border: 1px solid #e5e3d6; border-radius: 4px; background: #fffdf8; box-shadow: 0 20px 50px #2b333815; transform: rotate(2deg); }
.slab-card-top { display: flex; align-items: center; justify-content: space-between; color: #8a939a; font: 9px var(--mono); letter-spacing: .5px; }
.slab-drawing { position: relative; height: 150px; margin: 14px 0 10px; border: 2px solid var(--slate); border-radius: 4px; background: linear-gradient(135deg, #ece9df 0%, #e3dfd2 100%); }
.slab-drawing::before { content: ""; position: absolute; inset: 10px; border: 1px dashed #b9b4a4; border-radius: 2px; }
.slab-dim { position: absolute; color: var(--slate); font: 600 11px var(--mono); background: #fffdf8; padding: 2px 6px; border-radius: 3px; }
.slab-dim--length { top: -9px; left: 50%; transform: translateX(-50%); }
.slab-dim--width { top: 50%; right: -14px; transform: translateY(-50%) rotate(90deg); }
.slab-dim--thick { bottom: 8px; left: 12px; }
.slab-note { display: flex; align-items: center; gap: 12px; padding: 12px 14px; border: 1px solid #ecece2; border-radius: 7px; background: var(--white); box-shadow: 0 9px 25px #2b333812; }
.slab-note strong { font: 700 15px var(--display); }
.slab-note small { display: block; padding-top: 2px; color: var(--muted); font-size: 11px; }
/* Guide posts — worked examples + key-facts table (shared, was inline in the German Ratgeber) */
.guide-article { padding: 34px 11.2% 70px; }
.guide-article .article-body { max-width: 760px; margin: 0 auto; }
.guide-article h2 { margin: 34px 0 12px; font: 600 26px/1.3 var(--display); letter-spacing: -.3px; }
.guide-article h3 { margin: 26px 0 10px; font: 600 19px/1.35 var(--display); }
.guide-article p, .guide-article li { color: #4a545a; font-size: 16px; line-height: 1.8; }
.guide-article p { margin: 0 0 14px; }
.guide-article ul, .guide-article ol { margin: 0 0 16px; padding-left: 22px; }
.guide-article li { margin-bottom: 8px; }
.guide-article a { color: var(--slate); font-weight: 700; }
.guide-article a:hover { text-decoration: underline; }
.example-block { max-width: 760px; margin: 0 auto 14px; padding: 22px 24px; border-radius: 8px; background: #fffdf8; box-shadow: 0 2px 10px #2b33380d; }
.example-block h3 { margin: 0 0 8px; font: 600 19px/1.35 var(--display); }
.example-block p { margin: 0 0 10px; color: #4a545a; font-size: 15px; line-height: 1.8; }
.example-block p:last-child { margin-bottom: 0; }
.example-math { color: var(--ink); font: 500 16px/1.7 var(--mono); }
.example-math strong { color: var(--slate); }
.key-facts { width: 100%; max-width: 760px; margin: 0 auto 20px; border-collapse: collapse; font-size: 15px; line-height: 1.5; }
.key-facts th, .key-facts td { padding: 12px 14px; text-align: left; border-bottom: 1px solid #eef0e9; }
.key-facts thead th { color: var(--slate); font: 600 12px var(--mono); text-transform: uppercase; letter-spacing: .8px; }
.key-facts tbody td:last-child { font-family: var(--mono); color: var(--ink); }
.guide-index-list { max-width: 760px; margin: 0 auto; }
.guide-index-list a { display: block; padding: 18px 0; border-bottom: 1px solid #e6e3d8; }
.guide-index-list a h3 { margin: 0 0 4px; font: 600 18px var(--display); }
.guide-index-list a p { margin: 0; color: #5c666b; font-size: 14px; }
@media (max-width: 900px) {
  .calc-options, .cost-grid { grid-template-columns: 1fr; }
  .result-rows { grid-template-columns: 1fr; }
}
@media (max-width: 680px) {
  .pour-row { grid-template-columns: 1fr auto; }
  .pour-row .pour-vol { grid-column: 1; }
}
/* Hero actions — "How it works" secondary button beside the calculator link (2026-11-20). */
.hero-actions { display: flex; gap: 16px; justify-content: center; align-items: center; flex-wrap: wrap; }
.hero-btn { min-height: 44px; display: inline-flex; align-items: center; padding: 10px 18px; border: 1.5px solid var(--slate); border-radius: 6px; background: transparent; color: var(--slate); font-size: 14px; font-weight: 700; }
.hero-btn:hover { background: #33414b12; }
.hero-btn:active { transform: scale(.97); }
/* Restored QA fixes (2026-11-20, v1 QA): the "$ / yd³" unit labels must not
   wrap, and the tool-page intro must stay visible on phones — it is the
   direct answer (GEO), and hiding it would cost the page its answer on the
   device most people use. These live here now so regeneration cannot drop them. */
.input-with-unit span { white-space: nowrap; padding-right: 12px; color: #4a545a; font: 13px var(--mono); }
@media (max-width: 680px) {
  .tool-page .hero-description { display: block; font-size: 15px; line-height: 1.65; }
}
@media print {
  .shape-tabs, .pour-list, .pour-add, .calc-options, .cost-grid { display: none !important; }
}
"""

DST.write_text(text)
print("wrote", DST, len(text), "chars")
# sanity: no leftover old tokens
for bad in ["--green", "--orange", "#245c48", "#e79a62", "#193f34", "#f5f4ed"]:
    assert bad not in text, f"leftover token {bad}"
print("no leftover German tokens")
