// concretecalc. — column calculator. Vanilla JS only. No framework, no tracking.
// Every size is turned into feet first, then the volume is worked out in
// cubic feet. 1 yd³ = 27 ft³ ≈ 0.765 m³. Bag yields: 40 lb → 0.30 ft³,
// 50 lb → 0.375 ft³, 60 lb → 0.45 ft³, 80 lb → 0.60 ft³.
const FT_PER_UNIT = { ft: 1, in: 1 / 12, yd: 3, m: 3.280839895, cm: 0.03280839895, mm: 0.003280839895 };
const FT2_PER_UNIT = { ft2: 1, m2: 10.763910417, yd2: 9 };
const AREA_LABEL = { ft2: "ft²", m2: "m²", yd2: "yd²" };
const BAG_YIELD = { 40: 0.30, 50: 0.375, 60: 0.45, 80: 0.60 };
const STORAGE_KEY = "concretecalc_column_v1";
const HAS_WASTE = true;
const HAS_SHAPE = true;

const fmt = new Intl.NumberFormat("en-US", { maximumSignificantDigits: 8 });
const fmt2 = (n) => new Intl.NumberFormat("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(n);
const fmtInt = (n) => new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 }).format(n);
const fmtMoney = (n) => "$" + new Intl.NumberFormat("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(n);
const fmtFt = (n) => fmt.format(n);

const FIELDS = [{"key": "width", "label": "Width", "kind": "dim", "unit": true, "shape": "rect"}, {"key": "depth", "label": "Depth", "kind": "dim", "unit": true, "shape": "rect"}, {"key": "diameter", "label": "Diameter", "kind": "dim", "unit": true, "shape": "round"}, {"key": "height", "label": "Height", "kind": "dim", "unit": true}, {"key": "quantity", "label": "Number of columns", "kind": "int", "unit": false}];
const DEFAULTS = {"width": "1", "widthUnit": "ft", "depth": "1", "depthUnit": "ft", "diameter": "12", "diameterUnit": "in", "height": "10", "heightUnit": "ft", "quantity": "1", "shape": "rect", "waste": "10", "density": 150};

const form = document.querySelector("#column-form");
const errorMessage = document.querySelector("#form-error");
const resultPanel = document.querySelector("#result-panel");
const resultValue = document.querySelector("#result-value");
const resultContext = document.querySelector("#result-context");
const resultAlso = document.querySelector("#result-also");
const resultRows = document.querySelector("#result-rows");
const resultFormula = document.querySelector("#result-formula");
const copyButton = document.querySelector("#copy-button");
const wasteSlider = document.querySelector("#waste-slider");
const wasteValue = document.querySelector("#waste-value");
const priceYardInput = document.querySelector("#price-yard");
const priceBagInput = document.querySelector("#price-bag");

let density = 150;
let shape = "rect";
let lastValue = "";

function fieldEls(f) {
  return {
    input: document.querySelector("#" + f.key),
    unit: f.unit ? document.querySelector("#" + f.key + "-unit") : null,
  };
}
function activeFields() {
  if (!HAS_SHAPE) return FIELDS;
  return FIELDS.filter((f) => !f.shape || f.shape === shape);
}
function markField(fieldId, state) {
  const field = document.querySelector("#" + fieldId + "-field");
  if (!field) return;
  field.classList.toggle("is-valid", state === "valid");
  field.classList.toggle("is-invalid", state === "invalid");
}
function clearFieldStates() {
  for (const f of FIELDS) markField(f.key, "");
}
function fail(message, badKey) {
  errorMessage.textContent = message;
  errorMessage.hidden = false;
  resultPanel.hidden = true;
  clearFieldStates();
  if (badKey) markField(badKey, "invalid");
}
function readField(f) {
  const { input, unit } = fieldEls(f);
  const raw = input.value.trim();
  const value = Number(raw);
  if (f.kind === "int") {
    if (!raw || !Number.isFinite(value) || value < 1 || Math.floor(value) !== value) {
      const err = new Error(`${f.label}: enter a whole number of 1 or more.`);
      err.fieldKey = f.key;
      throw err;
    }
    return value;
  }
  if (f.kind === "area") {
    if (!raw || !Number.isFinite(value) || value < 0) {
      const err = new Error(`${f.label}: enter a number of 0 or more.`);
      err.fieldKey = f.key;
      throw err;
    }
    return value * FT2_PER_UNIT[unit.value];
  }
  if (!raw || !Number.isFinite(value) || value <= 0) {
    const err = new Error(`${f.label}: enter a number greater than 0.`);
    err.fieldKey = f.key;
    throw err;
  }
  return value * FT_PER_UNIT[unit.value];
}
function displayValue(f) {
  const { input, unit } = fieldEls(f);
  if (f.kind === "int") return input.value.trim();
  if (f.kind === "area") return `${input.value.trim()} ${AREA_LABEL[unit.value]}`;
  return `${input.value.trim()} ${unit.value}`;
}

function setShape(next, save = true) {
  shape = next;
  document.querySelector("#shape-rect").setAttribute("aria-pressed", String(next === "rect"));
  document.querySelector("#shape-round").setAttribute("aria-pressed", String(next === "round"));
  document.querySelector("#fields-rect").classList.toggle("is-active", next === "rect");
  document.querySelector("#fields-round").classList.toggle("is-active", next === "round");
  if (save) saveState();
}
function setDensity(next, save = true) {
  density = next;
  document.querySelectorAll("#density-segmented button").forEach((b) =>
    b.setAttribute("aria-pressed", String(Number(b.dataset.density) === next)));
  if (save) saveState();
}

function saveState() {
  try {
    const s = { shape, density, waste: wasteSlider ? wasteSlider.value : "0" };
    for (const f of FIELDS) {
      const { input, unit } = fieldEls(f);
      s[f.key] = input.value;
      if (unit) s[f.key + "Unit"] = unit.value;
    }
    s.priceYard = priceYardInput.value;
    s.priceBag = priceBagInput.value;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
  } catch { /* private mode — the calculator still works, it just forgets */ }
}
function updateShareURL() {
  try {
    const params = new URLSearchParams();
    for (const f of activeFields()) {
      const { input, unit } = fieldEls(f);
      params.set(f.key, input.value);
      if (unit) params.set(f.key + "Unit", unit.value);
    }
    if (HAS_SHAPE) params.set("shape", shape);
    if (HAS_WASTE) { params.set("waste", wasteSlider.value); params.set("density", String(density)); }
    if (priceYardInput.value.trim()) params.set("priceYard", priceYardInput.value);
    if (priceBagInput.value.trim()) params.set("priceBag", priceBagInput.value);
    history.replaceState(null, "", `${location.pathname}?${params}`);
  } catch { /* ignore */ }
}
function applyValues(s) {
  for (const f of FIELDS) {
    if (s[f.key] === undefined) continue;
    const { input, unit } = fieldEls(f);
    input.value = s[f.key];
    if (unit && s[f.key + "Unit"] && (FT_PER_UNIT[s[f.key + "Unit"]] !== undefined || FT2_PER_UNIT[s[f.key + "Unit"]] !== undefined)) {
      unit.value = s[f.key + "Unit"];
    }
  }
  if (HAS_SHAPE && (s.shape === "rect" || s.shape === "round")) setShape(s.shape, false);
  if (HAS_WASTE) {
    if (s.waste !== undefined) { wasteSlider.value = s.waste; wasteValue.textContent = `${s.waste}%`; }
    if (s.density !== undefined && [150, 156, 110].includes(Number(s.density))) setDensity(Number(s.density), false);
  }
  if (s.priceYard !== undefined) priceYardInput.value = s.priceYard;
  if (s.priceBag !== undefined) priceBagInput.value = s.priceBag;
}
function loadFromURL() {
  try {
    const p = new URLSearchParams(location.search);
    if ([...p.keys()].length === 0) return false;
    const s = {};
    for (const [k, val] of p.entries()) s[k] = val;
    applyValues(s);
    return true;
  } catch { return false; }
}
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return false;
    applyValues(JSON.parse(raw));
    return true;
  } catch { return false; }
}

function calculate(event, silent = false) {
  if (event) event.preventDefault();
  errorMessage.hidden = true;
  try {
    const v = {};
    const f = {};
    for (const field of activeFields()) {
      v[field.key] = readField(field);
      f[field.key] = displayValue(field);
    }
    let netFt3 = shape === 'round' ? Math.PI * Math.pow(v.diameter / 2, 2) * v.height * v.quantity : v.width * v.depth * v.height * v.quantity;
    if (!Number.isFinite(netFt3) || netFt3 <= 0) {
      const err = new Error("The openings are bigger than the wall. Make the openings smaller than the wall area.");
      err.fieldKey = "openings";
      throw err;
    }
    const wastePct = HAS_WASTE ? Number(wasteSlider.value) : 0;
    const netYd3 = netFt3 / 27;
    const netM3 = netFt3 * 0.0283168;
    const wasteFt3 = netFt3 * (wastePct / 100);
    const ordFt3 = netFt3 + wasteFt3;
    const ordYd3 = ordFt3 / 27;
    const ordM3 = ordFt3 * 0.0283168;
    const weightLb = ordFt3 * density;
    const baseFt3 = HAS_WASTE ? ordFt3 : netFt3;
    const baseYd3 = HAS_WASTE ? ordYd3 : netYd3;
    const bags = {};
    for (const size of [40, 50, 60, 80]) bags[size] = Math.ceil(baseFt3 / BAG_YIELD[size]);
    const dims = shape === 'round' ? `${f.diameter} diameter × ${f.height} high` : `${f.width} × ${f.depth} × ${f.height} high`;
    const priceYard = Number(priceYardInput.value);
    const priceBag = Number(priceBagInput.value);

    resultValue.textContent = `${fmt2(baseYd3)} cubic yards`;
    resultContext.textContent = `${v.quantity} ${shape === 'round' ? 'round' : 'square'} column${v.quantity === 1 ? '' : 's'} at ${dims} need${v.quantity === 1 ? 's' : ''} ${fmt2(netYd3)} cubic yards. With ${wastePct}% waste, order ${fmt2(ordYd3)} cubic yards — about ${fmtInt(weightLb)} lb of concrete.`;
    resultAlso.textContent = HAS_WASTE
      ? `Also: ${fmt2(ordFt3)} cubic feet · ${fmt2(ordM3)} cubic meters`
      : `Also: ${fmt2(netFt3)} cubic feet · ${fmt2(netM3)} cubic meters`;
    resultFormula.textContent = shape === 'round' ? `π × ${fmtFt(v.diameter / 2)}² ft × ${fmtFt(v.height)} ft × ${v.quantity} = ${fmt2(netFt3)} ft³` : `${fmtFt(v.width)} ft × ${fmtFt(v.depth)} ft × ${fmtFt(v.height)} ft × ${v.quantity} = ${fmt2(netFt3)} ft³` + (HAS_WASTE ? ` + ${wastePct}% waste = ${fmt2(ordYd3)} yd³` : "");

    const rows = [];
    if (HAS_WASTE) {
      rows.push(["Net volume", `${fmt2(netFt3)} ft³ · ${fmt2(netYd3)} yd³`]);
      rows.push(["Waste volume", `${fmt2(wasteFt3)} ft³`]);
      rows.push(["Ordered volume", `${fmt2(ordFt3)} ft³ · ${fmt2(ordYd3)} yd³`]);
      rows.push(["Weight (ordered)", `${fmtInt(weightLb)} lb`]);
    } else {
      rows.push(["Volume", `${fmt2(netFt3)} ft³`]);
      rows.push(["Cubic meters", `${fmt2(netM3)} m³`]);
      rows.push(["Cubic yards", `${fmt2(netYd3)} yd³`]);
    }
    for (const size of [40, 50, 60, 80]) rows.push([`${size}-lb bags`, `${fmtInt(bags[size])} bags`]);
    if (priceYardInput.value.trim() && Number.isFinite(priceYard) && priceYard > 0) {
      rows.push(["Cost (concrete)", fmtMoney(baseYd3 * priceYard)]);
    }
    if (priceBagInput.value.trim() && Number.isFinite(priceBag) && priceBag > 0) {
      rows.push(["Cost (bags, 80-lb)", fmtMoney(bags[80] * priceBag)]);
    }
    resultRows.innerHTML = rows.map(([label, val]) =>
      `<div class="result-row"><span>${label}</span><span>${val}</span></div>`).join("");

    resultPanel.hidden = false;
    clearFieldStates();
    for (const field of activeFields()) markField(field.key, "valid");
    if (resultValue.textContent !== lastValue) {
      resultPanel.classList.remove("flash");
      void resultPanel.offsetWidth;
      resultPanel.classList.add("flash");
      lastValue = resultValue.textContent;
    }
    saveState();
    updateShareURL();
  } catch (error) {
    // Silent while typing: clearing a field mid-typing must not flash the
    // error or hide the last good result. The error only shows on submit.
    if (silent) { errorMessage.hidden = true; return; }
    fail(error.message, error.fieldKey);
  }
}

function resetCalculator() {
  try { localStorage.removeItem(STORAGE_KEY); } catch { /* ignore */ }
  applyValues(DEFAULTS);
  if (HAS_WASTE) { wasteSlider.value = "10"; wasteValue.textContent = "10%"; setDensity(150, false); }
  priceYardInput.value = "";
  priceBagInput.value = "";
  calculate();
}

function applyData(el) {
  const s = {};
  for (const k of Object.keys(el.dataset)) s[k] = el.dataset[k];
  applyValues(s);
  calculate();
  document.querySelector("#calculator").scrollIntoView({ behavior: "smooth" });
}

form.addEventListener("submit", (event) => calculate(event));
for (const f of FIELDS) {
  const { input, unit } = fieldEls(f);
  input.addEventListener("input", () => calculate(null, true));
  input.addEventListener("change", () => calculate(null, true));
  if (unit) {
    unit.addEventListener("input", () => calculate(null, true));
    unit.addEventListener("change", () => calculate(null, true));
  }
  input.addEventListener("focus", () => input.scrollIntoView({ block: "nearest", behavior: "smooth" }));
}
if (HAS_WASTE) {
  wasteSlider.addEventListener("input", () => {
    wasteValue.textContent = `${wasteSlider.value}%`;
    calculate(null, true);
  });
  document.querySelectorAll("#density-segmented button").forEach((b) =>
    b.addEventListener("click", () => { setDensity(Number(b.dataset.density)); calculate(); }));
}
if (HAS_SHAPE) {
  document.querySelectorAll("#shape-tabs button").forEach((b) =>
    b.addEventListener("click", () => { setShape(b.dataset.shape); calculate(); }));
}
for (const el of [priceYardInput, priceBagInput]) {
  el.addEventListener("input", () => calculate(null, true));
  el.addEventListener("change", () => calculate(null, true));
}
document.querySelectorAll(".example-card").forEach((card) =>
  card.addEventListener("click", () => applyData(card)));
document.querySelectorAll(".preset-chip").forEach((chip) =>
  chip.addEventListener("click", () => applyData(chip)));
document.querySelector("#reset-button").addEventListener("click", resetCalculator);
copyButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(`${resultValue.textContent} — ${resultContext.textContent}`);
    copyButton.classList.add("copied");
    copyButton.textContent = "Copied ✓";
    window.setTimeout(() => {
      copyButton.classList.remove("copied");
      copyButton.innerHTML = 'Copy result <span aria-hidden="true">⧉</span>';
    }, 1600);
  } catch {
    errorMessage.textContent = "Copy did not work in this browser. Select the result and copy it yourself.";
    errorMessage.hidden = false;
  }
});
document.querySelector("#current-year").textContent = new Date().getFullYear();
if (!loadFromURL() && !loadState()) { /* defaults are already in the HTML */ }
calculate();
