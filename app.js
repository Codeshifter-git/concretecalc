// concretecalc. — main calculator: 8 shapes + multi-pour job totals.
//
// Conversion constants (sacred numbers):
//   1 yd³ = 27 ft³ ≈ 0.765 m³; 1 m³ ≈ 1.308 yd³
//   1 yd³ ≈ 4,050 lb at standard density (150 lb/ft³)
//   Bag yields: 40 lb → 0.30 ft³, 50 lb → 0.375 ft³, 60 lb → 0.45 ft³, 80 lb → 0.60 ft³
//   Bags per yard: 90 / 72 / 60 / 45
// All lengths are converted to feet via metres (unitInMeters), then volume in ft³.

(function () {
  "use strict";

  var UNIT_IN_METERS = { ft: 0.3048, in: 0.0254, yd: 0.9144, m: 1, cm: 0.01, mm: 0.001 };
  var FT3_PER_YD3 = 27;
  var FT3_PER_M3 = 35.3147; // 1 m³ in ft³ (1 yd³ = 0.764555 m³)
  var BAG_YIELDS = { 40: 0.30, 50: 0.375, 60: 0.45, 80: 0.60 }; // ft³ per bag
  var STORAGE_KEY = "concretecalc_main_v1";
  var MAX_POURS = 12;

  var form = document.getElementById("concrete-form");
  var errorBox = document.getElementById("form-error");
  var resultPanel = document.getElementById("result-panel");
  var resultValue = document.getElementById("result-value");
  var resultContext = document.getElementById("result-context");
  var resultAlso = document.getElementById("result-also");
  var resultFormula = document.getElementById("result-formula");
  var wasteSlider = document.getElementById("waste-slider");
  var wasteValue = document.getElementById("waste-value");

  var shapeTabs = Array.prototype.slice.call(document.querySelectorAll("#shape-tabs .shape-tab"));
  var activeShape = "slab";
  var activeColShape = "rect";
  var density = 150;
  var pours = [];

  // --- helpers ---------------------------------------------------------------

  function toFeet(value, unit) {
    return (value * UNIT_IN_METERS[unit]) / 0.3048;
  }

  function num(id) {
    var el = document.getElementById(id);
    if (!el) return 0;
    var v = parseFloat(el.value);
    return isNaN(v) ? 0 : v;
  }

  function len(id) {
    var el = document.getElementById(id);
    var unitEl = document.getElementById(id + "-unit");
    if (!el || !unitEl) return 0;
    var v = parseFloat(el.value);
    if (isNaN(v)) return 0;
    return toFeet(v, unitEl.value);
  }

  function areaSqFt(value, unit) {
    // sq ft from a value in sq ft or m²
    return unit === "m2" ? value * 10.7639 : value;
  }

  function fmt(n, digits) {
    var d = digits === undefined ? 2 : digits;
    return n.toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
  }

  function fmt0(n) {
    return Math.round(n).toLocaleString("en-US");
  }

  function money(n) {
    return "$" + n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  function yd3(ft3) { return ft3 / FT3_PER_YD3; }
  function m3(ft3) { return ft3 / FT3_PER_M3; }
  function bagsNeeded(ft3, lb) { return Math.ceil(ft3 / BAG_YIELDS[lb]); }

  function markInvalid(inputId, fieldId) {
    var f = document.getElementById(fieldId);
    if (f) f.classList.add("is-invalid");
  }

  function validateInputs(specs) {
    // specs: [{input, field, name}] — returns true when all are positive numbers
    var invalid = [];
    specs.forEach(function (s) {
      var el = document.getElementById(s.input);
      var f = document.getElementById(s.field);
      if (f) f.classList.remove("is-invalid");
      var v = parseFloat(el.value);
      if (el.value === "" || isNaN(v) || v <= 0) {
        invalid.push(s.name);
        if (f) f.classList.add("is-invalid");
      }
    });
    return invalid;
  }

  // --- shape volumes (ft³) ---------------------------------------------------

  function volumeSlab() {
    return len("slab-length") * len("slab-width") * len("slab-thickness");
  }

  function volumeFooting() {
    return len("footing-length") * len("footing-width") * len("footing-depth");
  }

  function volumeColumn() {
    var qty = num("column-qty");
    if (qty <= 0) qty = 1;
    if (activeColShape === "round") {
      var r = len("column-diameter") / 2;
      return Math.PI * r * r * len("column-round-height") * qty;
    }
    return len("column-width") * len("column-depth") * len("column-height") * qty;
  }

  function volumeWall() {
    var face = len("wall-length") * len("wall-height");
    var openings = areaSqFt(num("wall-openings"), document.getElementById("wall-openings-unit").value);
    return Math.max(0, face - openings) * len("wall-thickness");
  }

  function volumeStairs() {
    var n = num("stairs-steps");
    return len("stairs-width") * len("stairs-tread") * len("stairs-riser") * (n * (n + 1)) / 2;
  }

  function volumeCurb() {
    var curb = len("curb-width") * len("curb-height");
    var gutter = len("gutter-width") * len("gutter-thickness");
    return len("curb-length") * (curb + gutter);
  }

  function volumePad() {
    var r = len("pad-diameter") / 2;
    return Math.PI * r * r * len("pad-thickness");
  }

  function volumeMono() {
    var slab = len("mono-length") * len("mono-width") * len("mono-thickness");
    var perimeter = 2 * (len("mono-length") + len("mono-width"));
    var edge = perimeter * len("mono-edge-width") * len("mono-edge-depth");
    return slab + edge;
  }

  var SHAPE_SPECS = {
    slab: {
      name: "Slab",
      volume: volumeSlab,
      inputs: [
        { input: "slab-length", field: "slab-length-field", name: "length" },
        { input: "slab-width", field: "slab-width-field", name: "width" },
        { input: "slab-thickness", field: "slab-thickness-field", name: "thickness" }
      ],
      describe: function () {
        return "a " + num("slab-length") + " " + document.getElementById("slab-length-unit").value + " × " + num("slab-width") + " " + document.getElementById("slab-width-unit").value + " slab, " + num("slab-thickness") + " " + document.getElementById("slab-thickness-unit").value + " thick";
      },
      formula: function () {
        return fmt(len("slab-length"), 2) + " ft × " + fmt(len("slab-width"), 2) + " ft × " + fmt(len("slab-thickness"), 3) + " ft = " + fmt(volumeSlab(), 2) + " ft³ = " + fmt(yd3(volumeSlab()), 2) + " yd³";
      },
      label: function () {
        return "Slab " + num("slab-length") + "×" + num("slab-width") + " ft, " + num("slab-thickness") + " " + document.getElementById("slab-thickness-unit").value;
      }
    },
    footing: {
      name: "Footing",
      volume: volumeFooting,
      inputs: [
        { input: "footing-length", field: "footing-length-field", name: "length" },
        { input: "footing-width", field: "footing-width-field", name: "width" },
        { input: "footing-depth", field: "footing-depth-field", name: "depth" }
      ],
      describe: function () {
        return "a " + num("footing-length") + " " + document.getElementById("footing-length-unit").value + " footing, " + num("footing-width") + " " + document.getElementById("footing-width-unit").value + " wide and " + num("footing-depth") + " " + document.getElementById("footing-depth-unit").value + " deep";
      },
      formula: function () {
        return fmt(len("footing-length"), 2) + " ft × " + fmt(len("footing-width"), 2) + " ft × " + fmt(len("footing-depth"), 2) + " ft = " + fmt(volumeFooting(), 2) + " ft³ = " + fmt(yd3(volumeFooting()), 2) + " yd³";
      },
      label: function () {
        return "Footing " + num("footing-length") + " ft, " + num("footing-width") + "×" + num("footing-depth") + " " + document.getElementById("footing-width-unit").value;
      }
    },
    column: {
      name: "Column",
      volume: volumeColumn,
      inputs: function () {
        if (activeColShape === "round") {
          return [
            { input: "column-diameter", field: "column-diameter-field", name: "diameter" },
            { input: "column-round-height", field: "column-round-height-field", name: "height" }
          ];
        }
        return [
          { input: "column-width", field: "column-width-field", name: "width" },
          { input: "column-depth", field: "column-depth-field", name: "depth" },
          { input: "column-height", field: "column-height-field", name: "height" }
        ];
      },
      describe: function () {
        var qty = num("column-qty");
        if (activeColShape === "round") {
          return "a " + num("column-diameter") + " " + document.getElementById("column-diameter-unit").value + " round column, " + num("column-round-height") + " " + document.getElementById("column-round-height-unit").value + " tall" + (qty > 1 ? " × " + qty : "");
        }
        return "a " + num("column-width") + " × " + num("column-depth") + " " + document.getElementById("column-width-unit").value + " column, " + num("column-height") + " " + document.getElementById("column-height-unit").value + " tall";
      },
      formula: function () {
        var v = volumeColumn();
        if (activeColShape === "round") {
          var r = len("column-diameter") / 2;
          return "π × " + fmt(r, 2) + " ft² × " + fmt(len("column-round-height"), 2) + " ft = " + fmt(v, 2) + " ft³ = " + fmt(yd3(v), 2) + " yd³";
        }
        return fmt(len("column-width"), 2) + " ft × " + fmt(len("column-depth"), 2) + " ft × " + fmt(len("column-height"), 2) + " ft = " + fmt(v, 2) + " ft³ = " + fmt(yd3(v), 2) + " yd³";
      },
      label: function () {
        var qty = num("column-qty");
        if (activeColShape === "round") {
          return "Round column " + num("column-diameter") + " " + document.getElementById("column-diameter-unit").value + " dia, " + num("column-round-height") + " ft" + (qty > 1 ? " × " + qty : "");
        }
        return "Square column " + num("column-width") + "×" + num("column-depth") + " ft, " + num("column-height") + " ft";
      }
    },
    wall: {
      name: "Wall",
      volume: volumeWall,
      inputs: [
        { input: "wall-length", field: "wall-length-field", name: "length" },
        { input: "wall-height", field: "wall-height-field", name: "height" },
        { input: "wall-thickness", field: "wall-thickness-field", name: "thickness" }
      ],
      describe: function () {
        var open = num("wall-openings");
        return "a " + num("wall-length") + " " + document.getElementById("wall-length-unit").value + " wall, " + num("wall-height") + " " + document.getElementById("wall-height-unit").value + " high and " + num("wall-thickness") + " " + document.getElementById("wall-thickness-unit").value + " thick" + (open > 0 ? ", minus " + open + " sq ft of openings" : "");
      },
      formula: function () {
        var face = len("wall-length") * len("wall-height");
        var openings = areaSqFt(num("wall-openings"), document.getElementById("wall-openings-unit").value);
        return "(" + fmt(face, 2) + " ft² − " + fmt(openings, 2) + " ft² openings) × " + fmt(len("wall-thickness"), 2) + " ft = " + fmt(volumeWall(), 2) + " ft³ = " + fmt(yd3(volumeWall()), 2) + " yd³";
      },
      label: function () {
        return "Wall " + num("wall-length") + "×" + num("wall-height") + " ft, " + num("wall-thickness") + " " + document.getElementById("wall-thickness-unit").value;
      }
    },
    stairs: {
      name: "Stairs",
      volume: volumeStairs,
      inputs: [
        { input: "stairs-width", field: "stairs-width-field", name: "width" },
        { input: "stairs-tread", field: "stairs-tread-field", name: "tread" },
        { input: "stairs-riser", field: "stairs-riser-field", name: "riser" },
        { input: "stairs-steps", field: "stairs-steps-field", name: "steps" }
      ],
      describe: function () {
        return "a " + num("stairs-steps") + "-step staircase, " + num("stairs-width") + " " + document.getElementById("stairs-width-unit").value + " wide, with " + num("stairs-tread") + " " + document.getElementById("stairs-tread-unit").value + " treads and " + num("stairs-riser") + " " + document.getElementById("stairs-riser-unit").value + " risers";
      },
      formula: function () {
        var n = num("stairs-steps");
        return fmt(len("stairs-width"), 2) + " ft × " + fmt(len("stairs-tread"), 3) + " ft × " + fmt(len("stairs-riser"), 3) + " ft × " + n + "(" + n + "+1) ÷ 2 = " + fmt(volumeStairs(), 2) + " ft³ = " + fmt(yd3(volumeStairs()), 2) + " yd³";
      },
      label: function () {
        return "Stairs " + num("stairs-steps") + " steps, " + num("stairs-width") + " ft wide";
      }
    },
    curb: {
      name: "Curb & gutter",
      volume: volumeCurb,
      inputs: [
        { input: "curb-length", field: "curb-length-field", name: "length" },
        { input: "curb-width", field: "curb-width-field", name: "width" },
        { input: "curb-height", field: "curb-height-field", name: "height" },
        { input: "gutter-width", field: "gutter-width-field", name: "gutter width" },
        { input: "gutter-thickness", field: "gutter-thickness-field", name: "gutter thickness" }
      ],
      describe: function () {
        return "a " + num("curb-length") + " " + document.getElementById("curb-length-unit").value + " curb run with a " + num("gutter-width") + " " + document.getElementById("gutter-width-unit").value + " gutter";
      },
      formula: function () {
        return fmt(len("curb-length"), 2) + " ft × (" + fmt(len("curb-width"), 2) + " ft × " + fmt(len("curb-height"), 2) + " ft curb + " + fmt(len("gutter-width"), 2) + " ft × " + fmt(len("gutter-thickness"), 2) + " ft gutter) = " + fmt(volumeCurb(), 2) + " ft³ = " + fmt(yd3(volumeCurb()), 2) + " yd³";
      },
      label: function () {
        return "Curb " + num("curb-length") + " ft run";
      }
    },
    pad: {
      name: "Circular pad",
      volume: volumePad,
      inputs: [
        { input: "pad-diameter", field: "pad-diameter-field", name: "diameter" },
        { input: "pad-thickness", field: "pad-thickness-field", name: "thickness" }
      ],
      describe: function () {
        return "a round pad " + num("pad-diameter") + " " + document.getElementById("pad-diameter-unit").value + " across, " + num("pad-thickness") + " " + document.getElementById("pad-thickness-unit").value + " thick";
      },
      formula: function () {
        var r = len("pad-diameter") / 2;
        return "π × " + fmt(r, 2) + " ft² × " + fmt(len("pad-thickness"), 3) + " ft = " + fmt(volumePad(), 2) + " ft³ = " + fmt(yd3(volumePad()), 2) + " yd³";
      },
      label: function () {
        return "Circular pad " + num("pad-diameter") + " ft dia, " + num("pad-thickness") + " " + document.getElementById("pad-thickness-unit").value;
      }
    },
    mono: {
      name: "Monolithic slab",
      volume: volumeMono,
      inputs: [
        { input: "mono-length", field: "mono-length-field", name: "length" },
        { input: "mono-width", field: "mono-width-field", name: "width" },
        { input: "mono-thickness", field: "mono-thickness-field", name: "thickness" },
        { input: "mono-edge-width", field: "mono-edge-width-field", name: "edge width" },
        { input: "mono-edge-depth", field: "mono-edge-depth-field", name: "edge depth" }
      ],
      describe: function () {
        return "a " + num("mono-length") + " " + document.getElementById("mono-length-unit").value + " × " + num("mono-width") + " " + document.getElementById("mono-width-unit").value + " monolithic slab, " + num("mono-thickness") + " " + document.getElementById("mono-thickness-unit").value + " thick with a thickened edge";
      },
      formula: function () {
        var slab = len("mono-length") * len("mono-width") * len("mono-thickness");
        var perimeter = 2 * (len("mono-length") + len("mono-width"));
        var edge = perimeter * len("mono-edge-width") * len("mono-edge-depth");
        return "slab " + fmt(slab, 2) + " ft³ + edge " + fmt(edge, 2) + " ft³ = " + fmt(volumeMono(), 2) + " ft³ = " + fmt(yd3(volumeMono()), 2) + " yd³";
      },
      label: function () {
        return "Monolithic slab " + num("mono-length") + "×" + num("mono-width") + " ft";
      }
    }
  };

  // --- result rendering ------------------------------------------------------

  function getWaste() {
    return parseFloat(wasteSlider.value) || 0;
  }

  function showError(message) {
    errorBox.textContent = message;
    errorBox.hidden = false;
  }

  function hideError() {
    errorBox.hidden = true;
    errorBox.textContent = "";
  }

  function calculate() {
    var spec = SHAPE_SPECS[activeShape];
    var inputSpecs = typeof spec.inputs === "function" ? spec.inputs() : spec.inputs;
    var invalid = validateInputs(inputSpecs);
    if (invalid.length > 0) {
      showError("Please enter a value above zero for: " + invalid.join(", ") + ".");
      resultPanel.classList.remove("is-stale");
      return null;
    }
    hideError();
    var netFt3 = spec.volume();
    var waste = getWaste();
    var orderedFt3 = netFt3 * (1 + waste / 100);
    var netYd = yd3(netFt3);
    var orderedYd = yd3(orderedFt3);
    var weight = orderedFt3 * density;
    var priceYard = num("price-yard");
    var priceBag = num("price-bag");

    resultValue.textContent = fmt(orderedYd, 2) + " yd³";
    resultContext.textContent = "A " + spec.describe() + " needs " + fmt(netYd, 2) + " cubic yards — order " + fmt(orderedYd, 2) + " with " + waste + "% waste.";
    resultAlso.textContent = "That is also: " + fmt(orderedFt3, 2) + " ft³ · " + fmt(m3(orderedFt3), 2) + " m³";
    document.getElementById("row-net").textContent = fmt(netYd, 2) + " yd³";
    document.getElementById("row-waste").textContent = fmt(orderedYd - netYd, 2) + " yd³ (" + waste + "%)";
    document.getElementById("row-weight").textContent = fmt0(weight) + " lb";
    document.getElementById("row-bags-40").textContent = fmt0(bagsNeeded(orderedFt3, 40)) + " bags";
    document.getElementById("row-bags-50").textContent = fmt0(bagsNeeded(orderedFt3, 50)) + " bags";
    document.getElementById("row-bags-60").textContent = fmt0(bagsNeeded(orderedFt3, 60)) + " bags";
    document.getElementById("row-bags-80").textContent = fmt0(bagsNeeded(orderedFt3, 80)) + " bags";

    var yardWrap = document.getElementById("row-cost-yard-wrap");
    var bagWrap = document.getElementById("row-cost-bag-wrap");
    if (priceYard > 0) {
      yardWrap.hidden = false;
      document.getElementById("row-cost-yard").textContent = money(orderedYd * priceYard);
    } else {
      yardWrap.hidden = true;
    }
    if (priceBag > 0) {
      bagWrap.hidden = false;
      document.getElementById("row-cost-bag").textContent = money(bagsNeeded(orderedFt3, 80) * priceBag);
    } else {
      bagWrap.hidden = true;
    }

    resultFormula.textContent = spec.formula();
    resultPanel.classList.remove("is-stale");
    return { shape: activeShape, label: spec.label(), netFt3: netFt3, netYd: netYd, orderedYd: orderedYd };
  }

  // --- multi-pour job list ---------------------------------------------------

  function renderPours() {
    var list = document.getElementById("pour-list");
    var rows = document.getElementById("pour-rows");
    rows.innerHTML = "";
    if (pours.length === 0) {
      list.hidden = true;
      return;
    }
    list.hidden = false;
    pours.forEach(function (p, i) {
      var row = document.createElement("div");
      row.className = "pour-row";
      var name = document.createElement("span");
      name.className = "pour-name";
      name.textContent = p.label;
      var vol = document.createElement("span");
      vol.className = "pour-vol";
      vol.textContent = fmt(p.netYd, 2) + " yd³ net";
      var remove = document.createElement("button");
      remove.type = "button";
      remove.className = "pour-remove";
      remove.setAttribute("aria-label", "Remove " + p.label);
      remove.textContent = "✕";
      remove.addEventListener("click", function () {
        pours.splice(i, 1);
        renderPours();
      });
      row.appendChild(name);
      row.appendChild(vol);
      row.appendChild(remove);
      rows.appendChild(row);
    });
    var waste = getWaste();
    var netFt3 = pours.reduce(function (sum, p) { return sum + p.netFt3; }, 0);
    var orderedFt3 = netFt3 * (1 + waste / 100);
    var orderedYd = yd3(orderedFt3);
    var weight = orderedFt3 * density;
    var priceYard = num("price-yard");
    var context = fmt(yd3(netFt3), 2) + " yd³ net (" + fmt(netFt3, 2) + " ft³) across " + pours.length + (pours.length === 1 ? " pour" : " pours") + " — " + fmt(orderedYd, 2) + " yd³ to order with " + waste + "% waste, about " + fmt0(weight) + " lb";
    if (priceYard > 0) context += ", about " + money(orderedYd * priceYard);
    context += ".";
    document.getElementById("pour-total-value").textContent = fmt(orderedYd, 2) + " yd³";
    document.getElementById("pour-total-context").textContent = context;
  }

  function addPour() {
    var current = calculate();
    if (!current) return;
    if (pours.length >= MAX_POURS) {
      showError("That is the maximum of " + MAX_POURS + " pours per job. Remove one to add another.");
      return;
    }
    pours.push({ label: current.label, netFt3: current.netFt3, netYd: current.netYd });
    renderPours();
    var btn = document.getElementById("add-pour-button");
    var original = btn.textContent;
    btn.textContent = "Added ✓";
    setTimeout(function () { btn.textContent = original; }, 1200);
  }

  // --- shape switching -------------------------------------------------------

  function setShape(shape, skipCalc) {
    activeShape = shape;
    shapeTabs.forEach(function (tab) {
      tab.setAttribute("aria-pressed", tab.dataset.shape === shape ? "true" : "false");
    });
    Object.keys(SHAPE_SPECS).forEach(function (key) {
      var el = document.getElementById("fields-" + key);
      if (el) el.classList.toggle("is-active", key === shape);
    });
    if (!skipCalc) calculate();
    saveState();
  }

  function setColShape(which) {
    activeColShape = which;
    Array.prototype.slice.call(document.querySelectorAll("#column-shape-tabs button")).forEach(function (b) {
      b.setAttribute("aria-pressed", b.dataset.colshape === which ? "true" : "false");
    });
    document.getElementById("column-rect-fields").hidden = which !== "rect";
    document.getElementById("column-round-fields").hidden = which !== "round";
    calculate();
    saveState();
  }

  function setDensity(value) {
    density = value;
    Array.prototype.slice.call(document.querySelectorAll("#density-segmented button")).forEach(function (b) {
      b.setAttribute("aria-pressed", String(parseFloat(b.dataset.density)) === String(value) ? "true" : "false");
    });
    calculate();
    renderPours();
    saveState();
  }

  // --- fill from preset / table row ------------------------------------------

  function fillFromDataset(el) {
    var shape = el.dataset.shape;
    if (!shape || !SHAPE_SPECS[shape]) return;
    var fields = {
      length: ["slab", "footing", "wall", "curb", "mono"].indexOf(shape) !== -1 ? shape + "-length" : null,
      width: shape + "-width",
      thickness: shape + "-thickness",
      depth: shape + "-depth",
      height: shape + "-height",
      diameter: shape + "-diameter",
      steps: "stairs-steps",
      openings: "wall-openings"
    };
    if (shape === "column") {
      var cs = el.dataset.colshape;
      if (cs) setColShape(cs);
    }
    setShape(shape, true);
    var map = {
      length: "length", width: "width", thickness: "thickness", depth: "depth",
      height: "height", diameter: "diameter", steps: "steps", openings: "openings"
    };
    Object.keys(map).forEach(function (key) {
      if (el.dataset[key] === undefined) return;
      var base = fields[key];
      // stairs width/tread/riser use their own ids; column round height uses column-round-height
      if (shape === "stairs" && key === "width") base = "stairs-width";
      if (shape === "column" && key === "height") base = activeColShape === "round" ? "column-round-height" : "column-height";
      var input = document.getElementById(base);
      var unit = document.getElementById(base + "-unit");
      if (!input) return;
      input.value = el.dataset[key];
      if (unit && el.dataset[key + "Unit"]) unit.value = el.dataset[key + "Unit"];
    });
    // stairs tread/riser come through the same generic keys only when present in the dataset
    if (el.dataset.tread) { var t = document.getElementById("stairs-tread"); if (t) t.value = el.dataset.tread; }
    if (el.dataset.riser) { var r = document.getElementById("stairs-riser"); if (r) r.value = el.dataset.riser; }
    calculate();
    saveState();
    document.getElementById("calculator").scrollIntoView({ behavior: "smooth", block: "start" });
  }

  // --- persistence + shareable URL -------------------------------------------

  function saveState() {
    try {
      var state = { shape: activeShape, colShape: activeColShape, density: density, waste: getWaste(), values: {} };
      Array.prototype.slice.call(form.querySelectorAll("input, select")).forEach(function (el) {
        if (el.id) state.values[el.id] = el.value;
      });
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) { /* private mode — ignore */ }
  }

  function loadState() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      var state = JSON.parse(raw);
      if (!state) return;
      Object.keys(state.values || {}).forEach(function (id) {
        var el = document.getElementById(id);
        if (el && state.values[id] !== "") el.value = state.values[id];
      });
      if (state.colShape) setColShape(state.colShape);
      if (state.density) setDensity(parseFloat(state.density));
      if (state.waste !== undefined) {
        wasteSlider.value = state.waste;
        wasteValue.textContent = state.waste + "%";
      }
      if (state.shape && SHAPE_SPECS[state.shape]) setShape(state.shape, true);
    } catch (e) { /* corrupted state — ignore */ }
  }

  function loadFromURL() {
    var params = new URLSearchParams(window.location.search);
    var shape = params.get("shape");
    if (!shape || !SHAPE_SPECS[shape]) return false;
    var found = false;
    params.forEach(function (value, key) {
      if (key === "shape") return;
      var el = document.getElementById(key);
      if (el) { el.value = value; found = true; }
    });
    if (found) {
      var cs = params.get("colshape");
      if (cs) setColShape(cs);
      setShape(shape, true);
    }
    return found;
  }

  function updateShareURL() {
    try {
      var params = new URLSearchParams();
      params.set("shape", activeShape);
      var spec = SHAPE_SPECS[activeShape];
      var inputSpecs = typeof spec.inputs === "function" ? spec.inputs() : spec.inputs;
      inputSpecs.forEach(function (s) {
        var el = document.getElementById(s.input);
        var unit = document.getElementById(s.input + "-unit");
        if (el && el.value !== "") params.set(s.input, el.value);
        if (unit && unit.value !== "") params.set(s.input + "-unit", unit.value);
      });
      if (activeShape === "column") params.set("colshape", activeColShape);
      var url = window.location.pathname + "?" + params.toString() + window.location.hash;
      window.history.replaceState(null, "", url);
    } catch (e) { /* ignore */ }
  }

  // --- events ----------------------------------------------------------------

  shapeTabs.forEach(function (tab) {
    tab.addEventListener("click", function () { setShape(tab.dataset.shape); });
  });

  Array.prototype.slice.call(document.querySelectorAll("#column-shape-tabs button")).forEach(function (b) {
    b.addEventListener("click", function () { setColShape(b.dataset.colshape); });
  });

  Array.prototype.slice.call(document.querySelectorAll("#density-segmented button")).forEach(function (b) {
    b.addEventListener("click", function () { setDensity(parseFloat(b.dataset.density)); });
  });

  wasteSlider.addEventListener("input", function () {
    wasteValue.textContent = wasteSlider.value + "%";
    calculate();
    renderPours();
    saveState();
  });

  form.addEventListener("input", function () {
    calculate();
    renderPours();
    saveState();
    updateShareURL();
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    calculate();
  });

  document.getElementById("reset-button").addEventListener("click", function () {
    form.reset();
    pours = [];
    renderPours();
    setShape("slab", true);
    setColShape("rect");
    setDensity(150);
    wasteSlider.value = 10;
    wasteValue.textContent = "10%";
    try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
    calculate();
  });

  document.getElementById("copy-button").addEventListener("click", function () {
    var text = resultContext.textContent + " " + resultAlso.textContent;
    var btn = this;
    var done = function () {
      var original = btn.textContent;
      btn.textContent = "Copied ✓";
      setTimeout(function () { btn.textContent = original; }, 1200);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, done);
    } else {
      var ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(ta);
      done();
    }
  });

  document.getElementById("add-pour-button").addEventListener("click", addPour);

  Array.prototype.slice.call(document.querySelectorAll(".example-card, .scale-row")).forEach(function (el) {
    el.addEventListener("click", function () { fillFromDataset(el); });
  });

  // --- init ------------------------------------------------------------------

  loadState();
  var fromURL = loadFromURL();
  if (!fromURL && !localStorage.getItem(STORAGE_KEY)) {
    // first visit: defaults are already in the HTML
  }
  calculate();
  renderPours();
})();
