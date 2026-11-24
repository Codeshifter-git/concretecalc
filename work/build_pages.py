#!/usr/bin/env python3
"""Generate the 8 ConcreteCalc tool pages (index.html + app.js each).

Model: ~/workspace/github-demos/massklar/massstabsrechner/ (page shape only).
Every number in the content below was hand-verified with python3 before
writing; see the verification notes in the final report.
Run: python3 build_pages.py  (writes into ../<slug>/)
"""
import json, os, html

BASE = "https://codeshifter-git.github.io/concretecalc"
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(ROOT)  # ~/workspace/github-demos/concretecalc

UNIT_OPTIONS = ["ft", "in", "yd", "m", "cm", "mm"]
AREA_UNITS = ["ft2", "m2", "yd2"]
AREA_LABEL = {"ft2": "ft²", "m2": "m²", "yd2": "yd²"}

# ---------------------------------------------------------------- data
# field: dict(key, label, value, unit, kind) kind: dim | area | int | shape-only
PAGES = []

PAGES.append(dict(
    slug="slab", title="Concrete Slab Calculator | concretecalc.",
    desc="Slab concrete calculator: enter length, width, and thickness for cubic yards, bags, weight, and cost. A 10×10 slab at 4 inches needs 1.23 cubic yards.",
    keyword="concrete slab calculator",
    eyebrow="The concrete slab calculator",
    h1_main="Concrete Slab Calculator.",
    h1_sub="For patios, driveways, and shed bases.",
    geo="A 10 ft by 10 ft slab at 4 inches thick needs 1.23 cubic yards of concrete. That is 33.33 cubic feet. With 10% extra for waste, order 1.36 cubic yards.",
    aside_num="GOOD TO KNOW", aside_title="Measure twice, pour once.",
    aside_text="Measure the length and width where the slab will go, and pick the thickness. The calculator turns it into cubic yards, bags, and weight — you do not have to work out the math.",
    fields=[
        dict(key="length", label="Length", value="10", unit="ft", kind="dim"),
        dict(key="width", label="Width", value="10", unit="ft", kind="dim"),
        dict(key="thickness", label="Thickness", value="4", unit="in", kind="dim"),
    ],
    volume_js="v.length * v.width * v.thickness",
    dims_js="`${f.length} × ${f.width} × ${f.thickness}`",
    formula_js="`${fmtFt(v.length)} ft × ${fmtFt(v.width)} ft × ${fmtFt(v.thickness)} ft = ${fmt2(netFt3)} ft³ ÷ 27 = ${fmt2(netYd3)} yd³`",
    context_js="`A ${dims} slab needs ${fmt2(netYd3)} cubic yards. With ${wastePct}% waste, order ${fmt2(ordYd3)} cubic yards — about ${fmtInt(weightLb)} lb of concrete.`",
    presets=[
        ("Patio 10×10 ft · 4 in", dict(length="10", lengthUnit="ft", width="10", widthUnit="ft", thickness="4", thicknessUnit="in")),
        ("Driveway 12×20 ft · 6 in", dict(length="12", lengthUnit="ft", width="20", widthUnit="ft", thickness="6", thicknessUnit="in")),
        ("Shed base 8×10 ft · 4 in", dict(length="8", lengthUnit="ft", width="10", widthUnit="ft", thickness="4", thicknessUnit="in")),
    ],
    examples=[
        ("▦", "Patio slab", "10 × 10 ft · 4 in — 1.23 yd³", dict(length="10", lengthUnit="ft", width="10", widthUnit="ft", thickness="4", thicknessUnit="in")),
        ("⌂", "Driveway slab", "12 × 20 ft · 6 in — 4.44 yd³", dict(length="12", lengthUnit="ft", width="20", widthUnit="ft", thickness="6", thicknessUnit="in")),
        ("▤", "Shed base", "8 × 10 ft · 4 in — 0.99 yd³", dict(length="8", lengthUnit="ft", width="10", widthUnit="ft", thickness="4", thicknessUnit="in")),
    ],
    table_title="How much ground does one cubic yard cover?",
    table_intro="One cubic yard covers less ground as the slab gets thicker. Read the thickness, then the square feet it covers. The math is 27 ÷ thickness in feet.",
    table_html="""<table class="scale-table">
            <thead><tr><th scope="col">Slab thickness</th><th scope="col">Square feet per cubic yard</th><th scope="col">How it is worked out</th></tr></thead>
            <tbody>
              <tr><th scope="row">2 in</th><td>162 sq ft</td><td>27 ÷ 0.17 ft</td></tr>
              <tr><th scope="row">3 in</th><td>108 sq ft</td><td>27 ÷ 0.25 ft</td></tr>
              <tr><th scope="row">4 in</th><td>81 sq ft</td><td>27 ÷ 0.33 ft</td></tr>
              <tr><th scope="row">6 in</th><td>54 sq ft</td><td>27 ÷ 0.50 ft</td></tr>
              <tr><th scope="row">8 in</th><td>40.5 sq ft</td><td>27 ÷ 0.67 ft</td></tr>
              <tr><th scope="row">12 in</th><td>27 sq ft</td><td>27 ÷ 1 ft</td></tr>
            </tbody>
          </table>""",
    formula_card=["Volume = length × width × thickness", "Cubic yards = cubic feet ÷ 27", "Ordered yards = net yards × (1 + waste)"],
    formula_note="One cubic yard = 27 cubic feet = 0.765 cubic meters.",
    guide_intro="A slab is a flat box. Its volume is length times width times thickness — then divide by 27 to get cubic yards.",
    steps=[
        ("Measure length and width", "Measure the slab in feet, where it will go. A patio that is 10 ft long and 10 ft wide covers 100 square feet.", "10 ft × 10 ft = 100 sq ft"),
        ("Turn thickness into feet", "Thickness is often given in inches. Divide inches by 12 to get feet. 4 inches is 0.33 feet.", "4 in ÷ 12 = 0.33 ft"),
        ("Multiply to get cubic feet", "Length times width times thickness gives cubic feet. This is the net volume, before waste.", "10 ft × 10 ft × 0.33 ft = 33.33 ft³"),
        ("Divide by 27 for cubic yards", "One cubic yard holds 27 cubic feet, so divide the cubic feet by 27.", "33.33 ft³ ÷ 27 = 1.23 yd³"),
        ("Add waste, then order", "Spills, uneven ground, and a little extra in the forms eat concrete. Add 10% for a clean job, 15% for rough ground.", "1.23 yd³ × 1.10 = 1.36 yd³"),
    ],
    practice=[
        ("Task 1: A patio is 12 ft by 15 ft and 4 in thick. How many cubic yards, before waste?",
         "A patio is 12 ft long, 15 ft wide, and 4 in thick. Work out the cubic yards, before any waste is added.",
         "<strong>Solution:</strong> 4 in is 4 ÷ 12 = 0.33 ft. 12 ft × 15 ft × 0.33 ft = 60 cubic feet. 60 ÷ 27 = 2.22 cubic yards."),
        ("Task 2: How many 80-lb bags for the 10×10 ft slab at 4 in thick, with 10% waste?",
         "Take the 10 ft by 10 ft slab at 4 in thick, add 10% waste, then work out how many 80-lb bags that is. One 80-lb bag fills 0.60 cubic feet.",
         "<strong>Solution:</strong> Net volume is 33.33 cubic feet. With 10% waste that is 36.67 cubic feet. 36.67 ÷ 0.60 = 61.11, so round up to 62 bags."),
    ],
    faqs=[
        ("How much concrete do I need for a 10×10 slab?",
         "At 4 inches thick, a 10 ft by 10 ft slab needs 1.23 cubic yards, or 33.33 cubic feet. With 10% waste, order 1.36 cubic yards. At 6 inches thick, the same slab needs 1.85 cubic yards."),
        ("How thick should a concrete slab be?",
         "A 4-inch slab suits a patio or walkway. A driveway or a slab that holds a car usually needs 6 inches. When in doubt, ask a local contractor — the right thickness depends on the soil and the load."),
        ("How many bags of concrete do I need for a slab?",
         "Divide the ordered cubic feet by the yield of one bag. An 80-lb bag fills 0.60 cubic feet, a 60-lb bag fills 0.45, a 50-lb bag fills 0.375, and a 40-lb bag fills 0.30. For the 10×10 ft slab at 4 in thick with 10% waste, that is 36.67 cubic feet, or 62 bags of 80-lb mix. The calculator shows all four bag sizes."),
        ("How many cubic yards do I need for a driveway?",
         "It depends on the size and the thickness. A 12 ft by 20 ft driveway at 6 inches thick needs 4.44 cubic yards. Measure your own driveway, pick the thickness, and the calculator does the rest. For help picking a thickness, see the <a href=\"../guides/\">thickness guide</a>."),
        ("Is this slab calculator free?",
         "Yes. It is free, with no sign-up. Use it as often as you like, on a phone or a computer."),
    ],
))

PAGES.append(dict(
    slug="footing", title="Concrete Footing Calculator | concretecalc.",
    desc="Footing concrete calculator: total run, width, and depth to cubic yards, bags, and cost. A 40 ft footing at 18×12 in needs 2.22 cubic yards.",
    keyword="concrete footing calculator",
    eyebrow="The concrete footing calculator",
    h1_main="Concrete Footing Calculator.",
    h1_sub="For a straight run of footing, end to end.",
    geo="A 40 ft footing that is 18 inches wide and 12 inches deep needs 2.22 cubic yards of concrete. That is 60 cubic feet. Add 10% waste for a hand-dug trench and order 2.44 cubic yards.",
    aside_num="GOOD TO KNOW", aside_title="Add up the whole run first.",
    aside_text="Walk the footing and add up every straight stretch into one total length. The calculator treats it as one long box, so a bent run still works if the total length is right.",
    fields=[
        dict(key="length", label="Total length", value="40", unit="ft", kind="dim"),
        dict(key="width", label="Width", value="18", unit="in", kind="dim"),
        dict(key="depth", label="Depth", value="12", unit="in", kind="dim"),
    ],
    volume_js="v.length * v.width * v.depth",
    dims_js="`${f.length} long × ${f.width} wide × ${f.depth} deep`",
    formula_js="`${fmtFt(v.length)} ft × ${fmtFt(v.width)} ft × ${fmtFt(v.depth)} ft = ${fmt2(netFt3)} ft³ ÷ 27 = ${fmt2(netYd3)} yd³`",
    context_js="`A ${dims} footing needs ${fmt2(netYd3)} cubic yards. With ${wastePct}% waste, order ${fmt2(ordYd3)} cubic yards — about ${fmtInt(weightLb)} lb of concrete.`",
    presets=[
        ("House footing 40 ft · 18×12 in", dict(length="40", lengthUnit="ft", width="18", widthUnit="in", depth="12", depthUnit="in")),
        ("Garden wall 30 ft · 16×12 in", dict(length="30", lengthUnit="ft", width="16", widthUnit="in", depth="12", depthUnit="in")),
        ("Long run 60 ft · 24×12 in", dict(length="60", lengthUnit="ft", width="24", widthUnit="in", depth="12", depthUnit="in")),
    ],
    examples=[
        ("▦", "House footing", "40 ft · 18×12 in — 2.22 yd³", dict(length="40", lengthUnit="ft", width="18", widthUnit="in", depth="12", depthUnit="in")),
        ("▤", "Garden wall footing", "30 ft · 16×12 in — 1.48 yd³", dict(length="30", lengthUnit="ft", width="16", widthUnit="in", depth="12", depthUnit="in")),
        ("⌂", "Long footing run", "60 ft · 24×12 in — 4.44 yd³", dict(length="60", lengthUnit="ft", width="24", widthUnit="in", depth="12", depthUnit="in")),
    ],
    table_title="Footing volume per 10 ft of run",
    table_intro="Pick a width and a depth to see the concrete in 10 feet of footing. Multiply by your run: a 40 ft run is four times the 10 ft figure.",
    table_html="""<table class="scale-table">
            <thead><tr><th scope="col">Width × depth</th><th scope="col">Cubic feet per 10 ft</th><th scope="col">Cubic yards per 10 ft</th></tr></thead>
            <tbody>
              <tr><th scope="row">12 in × 8 in</th><td>6.67 ft³</td><td>0.25 yd³</td></tr>
              <tr><th scope="row">12 in × 12 in</th><td>10.00 ft³</td><td>0.37 yd³</td></tr>
              <tr><th scope="row">16 in × 8 in</th><td>8.89 ft³</td><td>0.33 yd³</td></tr>
              <tr><th scope="row">16 in × 12 in</th><td>13.33 ft³</td><td>0.49 yd³</td></tr>
              <tr><th scope="row">18 in × 8 in</th><td>10.00 ft³</td><td>0.37 yd³</td></tr>
              <tr><th scope="row">18 in × 12 in</th><td>15.00 ft³</td><td>0.56 yd³</td></tr>
              <tr><th scope="row">24 in × 8 in</th><td>13.33 ft³</td><td>0.49 yd³</td></tr>
              <tr><th scope="row">24 in × 12 in</th><td>20.00 ft³</td><td>0.74 yd³</td></tr>
            </tbody>
          </table>""",
    formula_card=["Volume = total length × width × depth", "Cubic yards = cubic feet ÷ 27", "Ordered yards = net yards × (1 + waste)"],
    formula_note="One cubic yard = 27 cubic feet = 0.765 cubic meters. Hand-dug trenches: allow 10–15% waste.",
    guide_intro="A footing is a long, low box under a wall. Its volume is the total run times the width times the depth.",
    steps=[
        ("Add up the total run", "Measure every stretch of footing and add them into one total length. A 40 ft run is one number, even if it turns corners.", "25 ft + 15 ft = 40 ft"),
        ("Turn width and depth into feet", "Width and depth are often given in inches. Divide by 12. 18 inches is 1.5 feet, and 12 inches is 1 foot.", "18 in ÷ 12 = 1.5 ft · 12 in ÷ 12 = 1 ft"),
        ("Multiply to get cubic feet", "Total length times width times depth gives cubic feet. This is the net volume, before waste.", "40 ft × 1.5 ft × 1 ft = 60 ft³"),
        ("Divide by 27 for cubic yards", "One cubic yard holds 27 cubic feet, so divide the cubic feet by 27.", "60 ft³ ÷ 27 = 2.22 yd³"),
        ("Add waste for a hand-dug trench", "A trench dug by hand is never exact, and the sides crumble a little. Add 10% on a clean trench, 15% on a rough one.", "2.22 yd³ × 1.10 = 2.44 yd³"),
    ],
    practice=[
        ("Task 1: A footing is 25 ft long, 12 in wide, and 12 in deep. How many cubic yards?",
         "Work out the cubic yards for a 25 ft footing that is 12 inches wide and 12 inches deep, before waste.",
         "<strong>Solution:</strong> 12 in is 1 ft. 25 ft × 1 ft × 1 ft = 25 cubic feet. 25 ÷ 27 = 0.93 cubic yards."),
        ("Task 2: The 40 ft footing at 18×12 in, with 10% waste — how many 80-lb bags?",
         "Take the 40 ft footing at 18 inches wide and 12 inches deep, add 10% waste, then work out the 80-lb bags. One 80-lb bag fills 0.60 cubic feet.",
         "<strong>Solution:</strong> Net volume is 60 cubic feet. With 10% waste that is 66 cubic feet. 66 ÷ 0.60 = 110 bags."),
    ],
    faqs=[
        ("How deep should a footing be?",
         "It depends on your local building code and the frost line where you live. In cold places the footing must sit below the frost line so the ground cannot lift it. Check with your local building office before you dig — this calculator does not set the depth for you."),
        ("What is the difference between a continuous footing and a spread footing?",
         "A continuous footing runs in one long strip under a whole wall — that is what this calculator works out. A spread footing is a wide, flat pad under one post or column, spreading its load over a bigger patch of ground."),
        ("How many bags of concrete do I need for a footing?",
         "Divide the ordered cubic feet by the yield of one bag. An 80-lb bag fills 0.60 cubic feet. The 40 ft footing at 18×12 in is 60 cubic feet before waste, which is 100 bags of 80-lb mix. The calculator shows all four bag sizes, with waste included."),
        ("How much waste should I allow for a hand-dug footing?",
         "Allow 10–15%. Hand-dug trenches are never exact: the sides crumble, the bottom is uneven, and a little concrete always spills. Use 10% for a clean trench and 15% for rough ground."),
        ("Is this footing calculator free?",
         "Yes. It is free, with no sign-up. Use it as often as you like, on a phone or a computer."),
    ],
))

PAGES.append(dict(
    slug="sonotube", title="Sonotube Concrete Calculator | concretecalc.",
    desc="Sonotube calculator: tube diameter, depth, and count to cubic yards and bags. A 12-inch tube 4 feet deep takes 3.14 cubic feet.",
    keyword="concrete calculator for sonotube",
    eyebrow="The sonotube concrete calculator",
    h1_main="Concrete Calculator for Sonotube.",
    h1_sub="For deck posts, fence posts, and porch posts.",
    geo="One 12-inch tube that is 4 feet deep takes 3.14 cubic feet of concrete. That is 0.12 cubic yards, or about 6 bags of 80-lb mix.",
    aside_num="GOOD TO KNOW", aside_title="One tube, one round column.",
    aside_text="A sonotube is a round cardboard form. The concrete inside it is a cylinder, so the math uses the circle area — pi times the radius squared — times the depth.",
    fields=[
        dict(key="diameter", label="Tube diameter", value="12", unit="in", kind="dim"),
        dict(key="depth", label="Depth", value="4", unit="ft", kind="dim"),
        dict(key="quantity", label="Number of tubes", value="1", unit=None, kind="int"),
    ],
    volume_js="Math.PI * Math.pow(v.diameter / 2, 2) * v.depth * v.quantity",
    dims_js="`${f.diameter} diameter × ${f.depth} deep`",
    formula_js="`π × ${fmtFt(v.diameter / 2)}² ft × ${fmtFt(v.depth)} ft × ${v.quantity} = ${fmt2(netFt3)} ft³`",
    context_js="`${v.quantity} tube${v.quantity === 1 ? '' : 's'} at ${dims} take${v.quantity === 1 ? 's' : ''} ${fmt2(netFt3)} cubic feet. With ${wastePct}% waste, order ${fmt2(ordYd3)} cubic yards — about ${bags[80]} bags of 80-lb mix.`",
    presets=[
        ("Deck post 12 in × 4 ft", dict(diameter="12", diameterUnit="in", depth="4", depthUnit="ft", quantity="1")),
        ("Fence posts 8 in × 2 ft × 6", dict(diameter="8", diameterUnit="in", depth="2", depthUnit="ft", quantity="6")),
        ("Porch posts 10 in × 3 ft × 4", dict(diameter="10", diameterUnit="in", depth="3", depthUnit="ft", quantity="4")),
    ],
    examples=[
        ("◉", "One deck post", "12 in × 4 ft · 1 tube — 3.14 ft³", dict(diameter="12", diameterUnit="in", depth="4", depthUnit="ft", quantity="1")),
        ("▦", "Four porch posts", "10 in × 3 ft · 4 tubes — 6.54 ft³", dict(diameter="10", diameterUnit="in", depth="3", depthUnit="ft", quantity="4")),
        ("▤", "Six fence posts", "8 in × 2 ft · 6 tubes — 4.19 ft³", dict(diameter="8", diameterUnit="in", depth="2", depthUnit="ft", quantity="6")),
    ],
    table_title="Concrete in one tube",
    table_intro="Cubic feet in a single tube, by diameter and depth. Multiply by the number of tubes you are pouring.",
    table_html="""<table class="scale-table">
            <thead><tr><th scope="col">Tube diameter</th><th scope="col">2 ft deep</th><th scope="col">3 ft deep</th><th scope="col">4 ft deep</th></tr></thead>
            <tbody>
              <tr><th scope="row">8 in</th><td>0.70 ft³ · 0.03 yd³</td><td>1.05 ft³ · 0.04 yd³</td><td>1.40 ft³ · 0.05 yd³</td></tr>
              <tr><th scope="row">10 in</th><td>1.09 ft³ · 0.04 yd³</td><td>1.64 ft³ · 0.06 yd³</td><td>2.18 ft³ · 0.08 yd³</td></tr>
              <tr><th scope="row">12 in</th><td>1.57 ft³ · 0.06 yd³</td><td>2.36 ft³ · 0.09 yd³</td><td>3.14 ft³ · 0.12 yd³</td></tr>
            </tbody>
          </table>""",
    formula_card=["Volume per tube = π × radius² × depth", "Radius = diameter ÷ 2", "Total = volume per tube × number of tubes"],
    formula_note="π is 3.1416. One cubic yard = 27 cubic feet = 0.765 cubic meters.",
    guide_intro="A sonotube pour is a cylinder. Work out the circle area, multiply by the depth, then multiply by the number of tubes.",
    steps=[
        ("Halve the diameter to get the radius", "The radius is half the diameter. A 12-inch tube has a radius of 6 inches, which is 0.5 feet.", "12 in ÷ 2 = 6 in = 0.5 ft"),
        ("Work out the circle area", "Multiply pi by the radius squared. Pi is 3.1416.", "3.1416 × 0.5² ft = 0.79 sq ft"),
        ("Multiply by the depth", "Circle area times depth gives the volume of one tube in cubic feet.", "0.79 sq ft × 4 ft = 3.14 ft³"),
        ("Multiply by the number of tubes", "Pouring more than one tube? Multiply the one-tube volume by the count.", "3.14 ft³ × 4 tubes = 12.57 ft³"),
        ("Divide by 27 for cubic yards", "One cubic yard holds 27 cubic feet, so divide the cubic feet by 27 — then add waste.", "12.57 ft³ ÷ 27 = 0.47 yd³"),
    ],
    practice=[
        ("Task 1: One 10-inch tube, 3 ft deep. How many cubic feet, and how many 80-lb bags?",
         "Work out the volume of one 10-inch tube that is 3 feet deep, then the 80-lb bags. One 80-lb bag fills 0.60 cubic feet.",
         "<strong>Solution:</strong> Radius is 5 in, or 0.42 ft. 3.1416 × 0.42² × 3 = 1.64 cubic feet. 1.64 ÷ 0.60 = 2.73, so round up to 3 bags."),
        ("Task 2: Four 12-inch tubes, 4 ft deep, with 10% waste. How many cubic yards to order?",
         "Work out the volume of four 12-inch tubes at 4 feet deep, add 10% waste, and give the ordered cubic yards.",
         "<strong>Solution:</strong> One tube is 3.14 cubic feet, so four tubes are 12.57 cubic feet. With 10% waste that is 13.82 cubic feet. 13.82 ÷ 27 = 0.51 cubic yards."),
    ],
    faqs=[
        ("What is a sonotube?",
         "A sonotube is a round cardboard tube used as a form for a concrete footing. You set the tube in a hole, pour concrete into it, and peel the cardboard away once the concrete has set. It is often used under deck posts and fence posts."),
        ("How many bags of concrete do I need per tube?",
         "It depends on the tube size. A 12-inch tube 4 feet deep takes 3.14 cubic feet, which is 6 bags of 80-lb mix. A 10-inch tube 3 feet deep takes 1.64 cubic feet, which is 3 bags of 80-lb mix. The calculator shows all four bag sizes."),
        ("Should I subtract the volume of the post inside the tube?",
         "No — the calculator counts the full tube, and that is the safe order. A 4×4 post inside the tube displaces only a little concrete, and the extra covers spills and an uneven hole. Order the full-tube figure."),
        ("How deep should a sonotube footing go?",
         "It depends on your local building code and the frost line where you live. In cold places the footing must sit below the frost line so the ground cannot lift it. Check with your local building office before you dig."),
        ("Is this sonotube calculator free?",
         "Yes. It is free, with no sign-up. Use it as often as you like, on a phone or a computer."),
    ],
))

PAGES.append(dict(
    slug="stairs", title="Concrete Stairs Calculator | concretecalc.",
    desc="Concrete stairs calculator: width, tread, riser, and step count to cubic yards and bags. Five 7×11 in steps, 4 ft wide, need 1.19 cubic yards.",
    keyword="concrete stairs calculator",
    eyebrow="The concrete stairs calculator",
    h1_main="Concrete Stairs Calculator.",
    h1_sub="Solid steps, from the first tread to the last.",
    geo="Five steps that are 4 feet wide, with 11-inch treads and 7-inch risers, need 1.19 cubic yards of concrete. That is 32.08 cubic feet. This treats the flight as solid concrete all the way down to the ground.",
    aside_num="GOOD TO KNOW", aside_title="Steps stack like a staircase of blocks.",
    aside_text="Think of each step as a block. The bottom step is the widest, the top step is one block wide — so the blocks add up to 1 + 2 + 3 + 4 + 5 = 15 blocks for five steps.",
    fields=[
        dict(key="width", label="Width", value="4", unit="ft", kind="dim"),
        dict(key="tread", label="Tread depth", value="11", unit="in", kind="dim"),
        dict(key="riser", label="Riser height", value="7", unit="in", kind="dim"),
        dict(key="steps", label="Number of steps", value="5", unit=None, kind="int"),
    ],
    volume_js="v.width * v.tread * v.riser * v.steps * (v.steps + 1) / 2",
    dims_js="`${f.width} wide · ${f.tread} tread · ${f.riser} riser`",
    formula_js="`${fmtFt(v.width)} ft × ${fmtFt(v.tread)} ft × ${fmtFt(v.riser)} ft × ${v.steps * (v.steps + 1) / 2} = ${fmt2(netFt3)} ft³`",
    context_js="`${v.steps} steps at ${dims} need ${fmt2(netYd3)} cubic yards. With ${wastePct}% waste, order ${fmt2(ordYd3)} cubic yards — about ${fmtInt(weightLb)} lb of concrete.`",
    presets=[
        ("Porch steps 4 ft · 5 steps", dict(width="4", widthUnit="ft", tread="11", treadUnit="in", riser="7", riserUnit="in", steps="5")),
        ("Garden steps 3 ft · 3 steps", dict(width="3", widthUnit="ft", tread="11", treadUnit="in", riser="7", riserUnit="in", steps="3")),
        ("Wide entry 5 ft · 8 steps", dict(width="5", widthUnit="ft", tread="12", treadUnit="in", riser="7", riserUnit="in", steps="8")),
    ],
    examples=[
        ("▦", "Porch steps", "4 ft wide · 5 steps — 1.19 yd³", dict(width="4", widthUnit="ft", tread="11", treadUnit="in", riser="7", riserUnit="in", steps="5")),
        ("⌂", "Garden steps", "3 ft wide · 3 steps — 0.36 yd³", dict(width="3", widthUnit="ft", tread="11", treadUnit="in", riser="7", riserUnit="in", steps="3")),
        ("▤", "Wide entry steps", "5 ft wide · 8 steps — 3.89 yd³", dict(width="5", widthUnit="ft", tread="12", treadUnit="in", riser="7", riserUnit="in", steps="8")),
    ],
    table_title="Stair volume by step count",
    table_intro="Concrete for a 4 ft wide flight with 11-inch treads and 7-inch risers. More steps add more than one step's worth, because each new step sits on top of the ones below it.",
    table_html="""<table class="scale-table">
            <thead><tr><th scope="col">Number of steps</th><th scope="col">Cubic feet</th><th scope="col">Cubic yards</th></tr></thead>
            <tbody>
              <tr><th scope="row">3 steps</th><td>12.83 ft³</td><td>0.48 yd³</td></tr>
              <tr><th scope="row">4 steps</th><td>21.39 ft³</td><td>0.79 yd³</td></tr>
              <tr><th scope="row">5 steps</th><td>32.08 ft³</td><td>1.19 yd³</td></tr>
              <tr><th scope="row">6 steps</th><td>44.92 ft³</td><td>1.66 yd³</td></tr>
              <tr><th scope="row">8 steps</th><td>77.00 ft³</td><td>2.85 yd³</td></tr>
              <tr><th scope="row">10 steps</th><td>117.64 ft³</td><td>4.36 yd³</td></tr>
            </tbody>
          </table>""",
    formula_card=["Volume = width × tread × riser × n(n+1)/2", "n is the number of steps", "Cubic yards = cubic feet ÷ 27"],
    formula_note="This treats the flight as solid concrete all the way down to the ground. One cubic yard = 27 cubic feet.",
    guide_intro="A solid flight of steps is a stack of blocks. Count the blocks, work out one block, and multiply.",
    steps=[
        ("Count the blocks", "Each step adds a row of blocks. For 5 steps the rows are 1 + 2 + 3 + 4 + 5 blocks. The short way to add that is n(n+1)/2.", "5 × 6 ÷ 2 = 15 blocks"),
        ("Work out one block", "One block is one tread deep and one riser high, across the full width of the stairs.", "4 ft × 0.92 ft × 0.58 ft = 2.14 ft³"),
        ("Multiply blocks by block size", "15 blocks times one block gives the net volume in cubic feet.", "15 × 2.14 ft³ = 32.08 ft³"),
        ("Divide by 27 for cubic yards", "One cubic yard holds 27 cubic feet, so divide the cubic feet by 27.", "32.08 ft³ ÷ 27 = 1.19 yd³"),
        ("Add waste, then order", "Steps have lots of corners and edges, so allow 10% waste — 15% if the forms are rough.", "1.19 yd³ × 1.10 = 1.31 yd³"),
    ],
    practice=[
        ("Task 1: A flight 3 ft wide, 11 in tread, 7 in riser, 4 steps. How many cubic yards?",
         "Work out the cubic yards for a 3 ft wide flight with 11-inch treads, 7-inch risers, and 4 steps, before waste.",
         "<strong>Solution:</strong> Blocks = 4 × 5 ÷ 2 = 10. One block is 3 ft × 0.92 ft × 0.58 ft = 1.60 cubic feet. 10 × 1.60 = 16.04 cubic feet. 16.04 ÷ 27 = 0.59 cubic yards."),
        ("Task 2: Six steps, 4 ft wide, 11×7 in, with 10% waste — how many 80-lb bags?",
         "Take six steps at 4 ft wide with 11-inch treads and 7-inch risers, add 10% waste, then work out the 80-lb bags. One 80-lb bag fills 0.60 cubic feet.",
         "<strong>Solution:</strong> Net volume is 44.92 cubic feet. With 10% waste that is 49.41 cubic feet. 49.41 ÷ 0.60 = 82.35, so round up to 83 bags."),
    ],
    faqs=[
        ("How is the volume of concrete stairs worked out?",
         "The flight is treated as solid concrete all the way down to the ground. The volume is width × tread × riser × n(n+1)/2, where n is the number of steps. For 5 steps, n(n+1)/2 is 15. Divide the cubic feet by 27 to get cubic yards."),
        ("What size are a typical tread and riser?",
         "A 7-inch riser and an 11-inch tread are common sizes for outdoor steps. The riser is the height of one step, and the tread is the flat part you stand on. Check your local building code — it sets the limits for riser height and tread depth."),
        ("Does this calculator count the steps as solid?",
         "Yes. It treats the flight as solid concrete all the way down to the ground. If your steps are built over a hollow base or an existing slope, you will need less — use the solid figure as the safe order, or work out the fill under the steps separately."),
        ("How many bags of concrete do I need for stairs?",
         "Divide the ordered cubic feet by the yield of one bag. An 80-lb bag fills 0.60 cubic feet. Five steps at 4 ft wide with 11-inch treads and 7-inch risers need 32.08 cubic feet before waste, which is 54 bags of 80-lb mix. The calculator shows all four bag sizes, with waste included."),
        ("Is this stairs calculator free?",
         "Yes. It is free, with no sign-up. Use it as often as you like, on a phone or a computer."),
    ],
))

PAGES.append(dict(
    slug="wall", title="Concrete Wall Calculator | concretecalc.",
    desc="Concrete wall calculator: length, height, and thickness, minus door and window openings, to cubic yards and bags.",
    keyword="concrete wall calculator",
    eyebrow="The concrete wall calculator",
    h1_main="Concrete Wall Calculator.",
    h1_sub="Length, height, and thickness — minus the openings.",
    geo="A wall 20 feet long and 8 feet high, 8 inches thick, with a 3 by 7 foot door, needs 3.43 cubic yards of concrete. That is 92.67 cubic feet after the door is taken out.",
    aside_num="GOOD TO KNOW", aside_title="Take the openings out first.",
    aside_text="A door or a window is a hole with no concrete in it. Work out the wall area, subtract the area of every opening, and only then multiply by the thickness.",
    fields=[
        dict(key="length", label="Length", value="20", unit="ft", kind="dim"),
        dict(key="height", label="Height", value="8", unit="ft", kind="dim"),
        dict(key="thickness", label="Thickness", value="8", unit="in", kind="dim"),
        dict(key="openings", label="Openings area", value="21", unit="ft2", kind="area"),
    ],
    volume_js="(v.length * v.height - v.openings) * v.thickness",
    dims_js="`${f.length} long × ${f.height} high × ${f.thickness} thick`",
    formula_js="`(${fmtFt(v.length)} ft × ${fmtFt(v.height)} ft − ${fmt2(v.openings)} ft²) × ${fmtFt(v.thickness)} ft = ${fmt2(netFt3)} ft³`",
    context_js="`A ${dims} wall, minus ${fmt2(v.openings)} sq ft of openings, needs ${fmt2(netYd3)} cubic yards. With ${wastePct}% waste, order ${fmt2(ordYd3)} cubic yards — about ${fmtInt(weightLb)} lb of concrete.`",
    presets=[
        ("Basement wall 20 ft · 8 ft · 8 in, one door", dict(length="20", lengthUnit="ft", height="8", heightUnit="ft", thickness="8", thicknessUnit="in", openings="21", openingsUnit="ft2")),
        ("Garden wall 30 ft · 8 ft · 8 in", dict(length="30", lengthUnit="ft", height="8", heightUnit="ft", thickness="8", thicknessUnit="in", openings="0", openingsUnit="ft2")),
        ("Shed wall 12 ft · 8 ft · 6 in, one door", dict(length="12", lengthUnit="ft", height="8", heightUnit="ft", thickness="6", thicknessUnit="in", openings="21", openingsUnit="ft2")),
    ],
    examples=[
        ("▦", "Basement wall, one door", "20 × 8 ft · 8 in — 3.43 yd³", dict(length="20", lengthUnit="ft", height="8", heightUnit="ft", thickness="8", thicknessUnit="in", openings="21", openingsUnit="ft2")),
        ("⌂", "Garden wall, no openings", "30 × 8 ft · 8 in — 5.93 yd³", dict(length="30", lengthUnit="ft", height="8", heightUnit="ft", thickness="8", thicknessUnit="in", openings="0", openingsUnit="ft2")),
        ("▤", "Shed wall, one door", "12 × 8 ft · 6 in — 1.39 yd³", dict(length="12", lengthUnit="ft", height="8", heightUnit="ft", thickness="6", thicknessUnit="in", openings="21", openingsUnit="ft2")),
    ],
    table_title="Wall volume per 10 ft of run, 8 ft high",
    table_intro="Concrete in 10 feet of wall at 8 feet high, with no openings. For a longer wall, multiply: a 20 ft wall is twice the 10 ft figure.",
    table_html="""<table class="scale-table">
            <thead><tr><th scope="col">Wall thickness</th><th scope="col">Cubic feet per 10 ft</th><th scope="col">Cubic yards per 10 ft</th></tr></thead>
            <tbody>
              <tr><th scope="row">6 in</th><td>40.00 ft³</td><td>1.48 yd³</td></tr>
              <tr><th scope="row">8 in</th><td>53.33 ft³</td><td>1.98 yd³</td></tr>
              <tr><th scope="row">10 in</th><td>66.67 ft³</td><td>2.47 yd³</td></tr>
              <tr><th scope="row">12 in</th><td>80.00 ft³</td><td>2.96 yd³</td></tr>
            </tbody>
          </table>""",
    formula_card=["Wall area = length × height", "Net area = wall area − openings", "Volume = net area × thickness"],
    formula_note="Openings are in square feet. One cubic yard = 27 cubic feet = 0.765 cubic meters.",
    guide_intro="A wall is a tall, thin box with holes in it. Work out the area, subtract the openings, then multiply by the thickness.",
    steps=[
        ("Work out the wall area", "Length times height gives the wall area in square feet.", "20 ft × 8 ft = 160 sq ft"),
        ("Subtract the openings", "Measure each door and window, work out its area, and add them up. A 3 by 7 foot door is 21 square feet.", "160 sq ft − 21 sq ft = 139 sq ft"),
        ("Turn thickness into feet", "Thickness is often given in inches. Divide by 12. 8 inches is 0.67 feet.", "8 in ÷ 12 = 0.67 ft"),
        ("Multiply to get cubic feet", "Net area times thickness gives cubic feet. This is the net volume, before waste.", "139 sq ft × 0.67 ft = 92.67 ft³"),
        ("Divide by 27, then add waste", "One cubic yard holds 27 cubic feet. Divide, then add 10% waste for spills and uneven forms.", "92.67 ft³ ÷ 27 = 3.43 yd³ · × 1.10 = 3.78 yd³"),
    ],
    practice=[
        ("Task 1: A wall 15 ft long, 8 ft high, 8 in thick, with one 3×7 ft door. How many cubic yards?",
         "Work out the cubic yards for a 15 ft wall, 8 ft high and 8 inches thick, with one door that is 3 by 7 feet, before waste.",
         "<strong>Solution:</strong> Wall area is 15 × 8 = 120 square feet. The door is 3 × 7 = 21 square feet. Net area is 99 square feet. 99 × 0.67 ft = 66 cubic feet. 66 ÷ 27 = 2.44 cubic yards."),
        ("Task 2: A 10 ft wall, 8 ft high, 6 in thick, no openings. How many 80-lb bags?",
         "Work out the 80-lb bags for a 10 ft wall, 8 ft high and 6 inches thick, with no openings, before waste. One 80-lb bag fills 0.60 cubic feet.",
         "<strong>Solution:</strong> 10 × 8 × 0.5 = 40 cubic feet. 40 ÷ 0.60 = 66.67, so round up to 67 bags."),
    ],
    faqs=[
        ("How do I count door and window openings?",
         "Measure each opening and work out its area: width times height. A 3 by 7 foot door is 21 square feet. Add up the areas of all the doors and windows and type the total into the openings box. The calculator subtracts it from the wall area before working out the volume."),
        ("How thick should a concrete foundation wall be?",
         "It depends on the design of the building and the soil it sits on, so a builder or an engineer should set the thickness. This calculator does not pick a thickness for you — type the thickness from your plan and it works out the concrete."),
        ("How many bags of concrete do I need for a wall?",
         "Divide the ordered cubic feet by the yield of one bag. An 80-lb bag fills 0.60 cubic feet. The 20 ft wall at 8 ft high and 8 inches thick, minus one door, is 92.67 cubic feet before waste, which is 155 bags of 80-lb mix. The calculator shows all four bag sizes, with waste included."),
        ("Is this wall calculator free?",
         "Yes. It is free, with no sign-up. Use it as often as you like, on a phone or a computer."),
    ],
))

PAGES.append(dict(
    slug="curb", title="Concrete Curb Calculator | concretecalc.",
    desc="Curb and gutter calculator: run length, curb size, and gutter width to cubic yards, bags, and cost.",
    keyword="concrete curb calculator",
    eyebrow="The concrete curb calculator",
    h1_main="Concrete Curb Calculator.",
    h1_sub="Curb and gutter, by the foot.",
    geo="100 feet of curb and gutter — a 6 by 6 inch curb with an 18-inch gutter, 6 inches thick — needs 3.70 cubic yards of concrete. That is 100 cubic feet.",
    aside_num="GOOD TO KNOW", aside_title="Two shapes, one pour.",
    aside_text="A curb and gutter pour is two boxes side by side: the upright curb and the flat gutter. Work out each cross-section, add them, and multiply by the run length.",
    fields=[
        dict(key="length", label="Run length", value="100", unit="ft", kind="dim"),
        dict(key="curbWidth", label="Curb width", value="6", unit="in", kind="dim"),
        dict(key="curbHeight", label="Curb height", value="6", unit="in", kind="dim"),
        dict(key="gutterWidth", label="Gutter width", value="18", unit="in", kind="dim"),
        dict(key="gutterThickness", label="Gutter thickness", value="6", unit="in", kind="dim"),
    ],
    volume_js="v.length * (v.curbWidth * v.curbHeight + v.gutterWidth * v.gutterThickness)",
    dims_js="`${f.length} of curb and gutter`",
    formula_js="`${fmtFt(v.length)} ft × (${fmtFt(v.curbWidth)} ft × ${fmtFt(v.curbHeight)} ft + ${fmtFt(v.gutterWidth)} ft × ${fmtFt(v.gutterThickness)} ft) = ${fmt2(netFt3)} ft³`",
    context_js="`${dims} needs ${fmt2(netYd3)} cubic yards. With ${wastePct}% waste, order ${fmt2(ordYd3)} cubic yards — about ${fmtInt(weightLb)} lb of concrete.`",
    presets=[
        ("Street run 100 ft · 6×6 curb · 18 in gutter", dict(length="100", lengthUnit="ft", curbWidth="6", curbWidthUnit="in", curbHeight="6", curbHeightUnit="in", gutterWidth="18", gutterWidthUnit="in", gutterThickness="6", gutterThicknessUnit="in")),
        ("Short run 50 ft · same sizes", dict(length="50", lengthUnit="ft", curbWidth="6", curbWidthUnit="in", curbHeight="6", curbHeightUnit="in", gutterWidth="18", gutterWidthUnit="in", gutterThickness="6", gutterThicknessUnit="in")),
        ("Long run 200 ft · 6×8 curb · 24 in gutter", dict(length="200", lengthUnit="ft", curbWidth="6", curbWidthUnit="in", curbHeight="8", curbHeightUnit="in", gutterWidth="24", gutterWidthUnit="in", gutterThickness="6", gutterThicknessUnit="in")),
    ],
    examples=[
        ("▦", "Street run", "100 ft · 6×6 curb · 18 in gutter — 3.70 yd³", dict(length="100", lengthUnit="ft", curbWidth="6", curbWidthUnit="in", curbHeight="6", curbHeightUnit="in", gutterWidth="18", gutterWidthUnit="in", gutterThickness="6", gutterThicknessUnit="in")),
        ("⌂", "Short run", "50 ft · same sizes — 1.85 yd³", dict(length="50", lengthUnit="ft", curbWidth="6", curbWidthUnit="in", curbHeight="6", curbHeightUnit="in", gutterWidth="18", gutterWidthUnit="in", gutterThickness="6", gutterThicknessUnit="in")),
        ("▤", "Long run, wide gutter", "200 ft · 6×8 curb · 24 in gutter — 9.88 yd³", dict(length="200", lengthUnit="ft", curbWidth="6", curbWidthUnit="in", curbHeight="8", curbHeightUnit="in", gutterWidth="24", gutterWidthUnit="in", gutterThickness="6", gutterThicknessUnit="in")),
    ],
    table_title="Curb and gutter volume per 100 ft",
    table_intro="Concrete in 100 feet of curb and gutter for common size pairs. The curb is width × height, the gutter is width × thickness.",
    table_html="""<table class="scale-table">
            <thead><tr><th scope="col">Curb × gutter</th><th scope="col">Cubic feet per 100 ft</th><th scope="col">Cubic yards per 100 ft</th></tr></thead>
            <tbody>
              <tr><th scope="row">6×6 in curb · 12×6 in gutter</th><td>75.00 ft³</td><td>2.78 yd³</td></tr>
              <tr><th scope="row">6×6 in curb · 18×6 in gutter</th><td>100.00 ft³</td><td>3.70 yd³</td></tr>
              <tr><th scope="row">6×6 in curb · 24×6 in gutter</th><td>125.00 ft³</td><td>4.63 yd³</td></tr>
              <tr><th scope="row">6×8 in curb · 18×6 in gutter</th><td>108.33 ft³</td><td>4.01 yd³</td></tr>
              <tr><th scope="row">8×8 in curb · 24×6 in gutter</th><td>144.44 ft³</td><td>5.35 yd³</td></tr>
            </tbody>
          </table>""",
    formula_card=["Curb area = curb width × curb height", "Gutter area = gutter width × gutter thickness", "Volume = length × (curb area + gutter area)"],
    formula_note="All sizes are turned into feet first. One cubic yard = 27 cubic feet = 0.765 cubic meters.",
    guide_intro="A curb and gutter pour is two boxes side by side. Work out each cross-section, add them, and multiply by the run.",
    steps=[
        ("Work out the curb cross-section", "The curb is the upright box. Width times height, in feet. A 6 by 6 inch curb is 0.5 by 0.5 feet.", "0.5 ft × 0.5 ft = 0.25 sq ft"),
        ("Work out the gutter cross-section", "The gutter is the flat strip next to the curb. Width times thickness, in feet. An 18-inch gutter at 6 inches thick is 1.5 by 0.5 feet.", "1.5 ft × 0.5 ft = 0.75 sq ft"),
        ("Add the two areas", "Add the curb area and the gutter area to get the full cross-section.", "0.25 sq ft + 0.75 sq ft = 1.00 sq ft"),
        ("Multiply by the run length", "Cross-section times length gives cubic feet. This is the net volume, before waste.", "1.00 sq ft × 100 ft = 100 ft³"),
        ("Divide by 27, then add waste", "One cubic yard holds 27 cubic feet. Divide, then add 10% waste for spills and uneven forms.", "100 ft³ ÷ 27 = 3.70 yd³ · × 1.10 = 4.07 yd³"),
    ],
    practice=[
        ("Task 1: 80 ft of curb and gutter at the standard sizes. How many cubic yards?",
         "Work out the cubic yards for 80 feet of curb and gutter with a 6 by 6 inch curb and an 18-inch gutter at 6 inches thick, before waste.",
         "<strong>Solution:</strong> Cross-section is 0.25 + 0.75 = 1.00 square foot. 1.00 × 80 = 80 cubic feet. 80 ÷ 27 = 2.96 cubic yards."),
        ("Task 2: 150 ft of curb and gutter, 6×6 in curb, 12 in gutter at 6 in thick. How many cubic yards?",
         "Work out the cubic yards for 150 feet of curb and gutter with a 6 by 6 inch curb and a 12-inch gutter at 6 inches thick, before waste.",
         "<strong>Solution:</strong> Curb is 0.25 square feet and the gutter is 1.0 × 0.5 = 0.50 square feet, so the cross-section is 0.75 square feet. 0.75 × 150 = 112.50 cubic feet. 112.50 ÷ 27 = 4.17 cubic yards."),
    ],
    faqs=[
        ("What is curb and gutter?",
         "It is the concrete edge along a street. The curb is the upright edge that keeps cars off the sidewalk, and the gutter is the flat strip beside it that carries rain water to the drain. They are usually poured together as one piece."),
        ("What size is a standard curb and gutter?",
         "Sizes vary by city — each city sets its own standard in its street rules, so there is no single standard size. A 6 by 6 inch curb with an 18-inch gutter at 6 inches thick is a common size, and it is the default on this page. Check your city rules before you order."),
        ("How many bags of concrete do I need for curb and gutter?",
         "Divide the ordered cubic feet by the yield of one bag. An 80-lb bag fills 0.60 cubic feet. 100 feet of curb and gutter at the default sizes is 100 cubic feet before waste, which is 167 bags of 80-lb mix. The calculator shows all four bag sizes, with waste included."),
        ("Is this curb calculator free?",
         "Yes. It is free, with no sign-up. Use it as often as you like, on a phone or a computer."),
    ],
))

PAGES.append(dict(
    slug="column", title="Concrete Column Calculator | concretecalc.",
    desc="Concrete column calculator for round and square columns: size and height to cubic yards, bags, and cost.",
    keyword="concrete column calculator",
    eyebrow="The concrete column calculator",
    h1_main="Concrete Column Calculator.",
    h1_sub="Round or square, one column or many.",
    geo="A square column 1 foot by 1 foot and 10 feet tall needs 0.37 cubic yards of concrete. That is 10 cubic feet. A round 12-inch column the same height needs 0.29 cubic yards.",
    aside_num="GOOD TO KNOW", aside_title="Round or square, the math is close.",
    aside_text="A square column is width times depth times height. A round column is the circle area times height. Pick the shape at the top of the form and the right boxes appear.",
    fields=[
        dict(key="width", label="Width", value="1", unit="ft", kind="dim", shape="rect"),
        dict(key="depth", label="Depth", value="1", unit="ft", kind="dim", shape="rect"),
        dict(key="diameter", label="Diameter", value="12", unit="in", kind="dim", shape="round"),
        dict(key="height", label="Height", value="10", unit="ft", kind="dim"),
        dict(key="quantity", label="Number of columns", value="1", unit=None, kind="int"),
    ],
    volume_js="shape === 'round' ? Math.PI * Math.pow(v.diameter / 2, 2) * v.height * v.quantity : v.width * v.depth * v.height * v.quantity",
    dims_js="shape === 'round' ? `${f.diameter} diameter × ${f.height} high` : `${f.width} × ${f.depth} × ${f.height} high`",
    formula_js="shape === 'round' ? `π × ${fmtFt(v.diameter / 2)}² ft × ${fmtFt(v.height)} ft × ${v.quantity} = ${fmt2(netFt3)} ft³` : `${fmtFt(v.width)} ft × ${fmtFt(v.depth)} ft × ${fmtFt(v.height)} ft × ${v.quantity} = ${fmt2(netFt3)} ft³`",
    context_js="`${v.quantity} ${shape === 'round' ? 'round' : 'square'} column${v.quantity === 1 ? '' : 's'} at ${dims} need${v.quantity === 1 ? 's' : ''} ${fmt2(netYd3)} cubic yards. With ${wastePct}% waste, order ${fmt2(ordYd3)} cubic yards — about ${fmtInt(weightLb)} lb of concrete.`",
    presets=[
        ("Square 1×1 ft · 10 ft", dict(shape="rect", width="1", widthUnit="ft", depth="1", depthUnit="ft", height="10", heightUnit="ft", quantity="1")),
        ("Round 12 in · 10 ft", dict(shape="round", diameter="12", diameterUnit="in", height="10", heightUnit="ft", quantity="1")),
        ("Two square 2×2 ft · 8 ft", dict(shape="rect", width="2", widthUnit="ft", depth="2", depthUnit="ft", height="8", heightUnit="ft", quantity="2")),
    ],
    examples=[
        ("▦", "Square column", "1 × 1 ft · 10 ft — 0.37 yd³", dict(shape="rect", width="1", widthUnit="ft", depth="1", depthUnit="ft", height="10", heightUnit="ft", quantity="1")),
        ("◉", "Round column", "12 in dia · 10 ft — 0.29 yd³", dict(shape="round", diameter="12", diameterUnit="in", height="10", heightUnit="ft", quantity="1")),
        ("▤", "Two square columns", "2 × 2 ft · 8 ft × 2 — 2.37 yd³", dict(shape="rect", width="2", widthUnit="ft", depth="2", depthUnit="ft", height="8", heightUnit="ft", quantity="2")),
    ],
    table_title="Concrete in one column",
    table_intro="Cubic feet and cubic yards in a single column. Multiply by the number of columns you are pouring.",
    table_html="""<table class="scale-table">
            <thead><tr><th scope="col">Column</th><th scope="col">Cubic feet</th><th scope="col">Cubic yards</th></tr></thead>
            <tbody>
              <tr><th scope="row">Square 1×1 ft · 8 ft</th><td>8.00 ft³</td><td>0.30 yd³</td></tr>
              <tr><th scope="row">Square 1×1 ft · 10 ft</th><td>10.00 ft³</td><td>0.37 yd³</td></tr>
              <tr><th scope="row">Square 2×2 ft · 10 ft</th><td>40.00 ft³</td><td>1.48 yd³</td></tr>
              <tr><th scope="row">Round 12 in dia · 8 ft</th><td>6.28 ft³</td><td>0.23 yd³</td></tr>
              <tr><th scope="row">Round 12 in dia · 10 ft</th><td>7.85 ft³</td><td>0.29 yd³</td></tr>
              <tr><th scope="row">Round 18 in dia · 10 ft</th><td>17.67 ft³</td><td>0.65 yd³</td></tr>
            </tbody>
          </table>""",
    formula_card=["Square column = width × depth × height", "Round column = π × radius² × height", "Total = one column × number of columns"],
    formula_note="Radius = diameter ÷ 2. One cubic yard = 27 cubic feet = 0.765 cubic meters.",
    guide_intro="A column is a tall box or a tall cylinder. Work out one column, then multiply by the count.",
    steps=[
        ("Pick the shape", "Square columns use width and depth. Round columns use one number: the diameter. Pick the shape at the top of the form.", "Square: 1 ft × 1 ft · Round: 12 in dia"),
        ("Work out one column", "Square: width times depth times height. Round: pi times the radius squared times height.", "Square: 1 × 1 × 10 = 10 ft³ · Round: 3.1416 × 0.5² × 10 = 7.85 ft³"),
        ("Multiply by the number of columns", "Pouring more than one of the same column? Multiply the one-column volume by the count.", "10 ft³ × 2 columns = 20 ft³"),
        ("Divide by 27 for cubic yards", "One cubic yard holds 27 cubic feet, so divide the cubic feet by 27.", "20 ft³ ÷ 27 = 0.74 yd³"),
        ("Add waste, then order", "Columns are a small pour, so a spill matters more. Add 10% waste.", "0.74 yd³ × 1.10 = 0.81 yd³"),
    ],
    practice=[
        ("Task 1: One round column, 18 in diameter, 9 ft tall. How many cubic yards?",
         "Work out the cubic yards for one round column that is 18 inches across and 9 feet tall, before waste.",
         "<strong>Solution:</strong> Radius is 9 in, or 0.75 ft. 3.1416 × 0.75² × 9 = 15.90 cubic feet. 15.90 ÷ 27 = 0.59 cubic yards."),
        ("Task 2: Three square columns, 1×1 ft, 10 ft tall. How many 80-lb bags?",
         "Work out the 80-lb bags for three square columns, each 1 by 1 foot and 10 feet tall, before waste. One 80-lb bag fills 0.60 cubic feet.",
         "<strong>Solution:</strong> One column is 1 × 1 × 10 = 10 cubic feet, so three columns are 30 cubic feet. 30 ÷ 0.60 = 50 bags."),
    ],
    faqs=[
        ("What is the difference between a round and a square column?",
         "Only the shape of the cross-section. A square column is width times depth times height. A round column is the circle area — pi times the radius squared — times height. A round 12-inch column holds less concrete than a square 1 by 1 foot column of the same height: 7.85 cubic feet against 10 cubic feet."),
        ("How many bags of concrete do I need per column?",
         "Divide the column volume by the yield of one bag. An 80-lb bag fills 0.60 cubic feet. A square 1 by 1 foot column at 10 feet tall is 10 cubic feet, which is 17 bags of 80-lb mix. The calculator shows all four bag sizes, with waste included."),
        ("Does rebar change how much concrete I need?",
         "No, not in any way that matters for ordering. The steel bars take up a tiny part of the column, far less than the waste allowance. Work out the full volume and add the usual 10% waste."),
        ("Is this column calculator free?",
         "Yes. It is free, with no sign-up. Use it as often as you like, on a phone or a computer."),
    ],
))

PAGES.append(dict(
    slug="cubic-yard", title="Cubic Yard Calculator | concretecalc.",
    desc="Cubic yard calculator: enter length, width, and depth to get cubic yards, cubic feet, and cubic meters — plus bag counts.",
    keyword="cubic yard calculator",
    eyebrow="The cubic yard calculator",
    h1_main="Cubic Yard Calculator.",
    h1_sub="Cubic feet and cubic meters, in one step.",
    geo="A 10 ft by 10 ft area at 4 inches deep is 33.33 cubic feet. That is 1.23 cubic yards, or 0.94 cubic meters. One cubic yard always holds 27 cubic feet.",
    aside_num="GOOD TO KNOW", aside_title="A yard is a cube, 3 feet on each side.",
    aside_text="Picture a box that is 3 feet long, 3 feet wide, and 3 feet high. That box is one cubic yard, and it holds 27 cubic feet.",
    fields=[
        dict(key="length", label="Length", value="10", unit="ft", kind="dim"),
        dict(key="width", label="Width", value="10", unit="ft", kind="dim"),
        dict(key="depth", label="Depth", value="4", unit="in", kind="dim"),
    ],
    volume_js="v.length * v.width * v.depth",
    dims_js="`${f.length} × ${f.width} × ${f.depth}`",
    formula_js="`${fmtFt(v.length)} ft × ${fmtFt(v.width)} ft × ${fmtFt(v.depth)} ft = ${fmt2(netFt3)} ft³ ÷ 27 = ${fmt2(netYd3)} yd³`",
    context_js="`${dims} is ${fmt2(netFt3)} cubic feet — ${fmt2(netYd3)} cubic yards, or ${fmt2(netM3)} cubic meters.`",
    presets=[
        ("Slab 10×10 ft · 4 in", dict(length="10", lengthUnit="ft", width="10", widthUnit="ft", depth="4", depthUnit="in")),
        ("Deep pour 12×12 ft · 6 in", dict(length="12", lengthUnit="ft", width="12", widthUnit="ft", depth="6", depthUnit="in")),
        ("Small pad 5×5 ft · 4 in", dict(length="5", lengthUnit="ft", width="5", widthUnit="ft", depth="4", depthUnit="in")),
    ],
    examples=[
        ("▦", "Slab pour", "10 × 10 ft · 4 in — 1.23 yd³", dict(length="10", lengthUnit="ft", width="10", widthUnit="ft", depth="4", depthUnit="in")),
        ("⌂", "Deep pour", "12 × 12 ft · 6 in — 2.67 yd³", dict(length="12", lengthUnit="ft", width="12", widthUnit="ft", depth="6", depthUnit="in")),
        ("▤", "Small pad", "5 × 5 ft · 4 in — 0.31 yd³", dict(length="5", lengthUnit="ft", width="5", widthUnit="ft", depth="4", depthUnit="in")),
    ],
    table_title="Cubic feet to cubic yards",
    table_intro="One cubic yard holds 27 cubic feet. Read the cubic feet on the left, the cubic yards on the right — and back again.",
    table_html="""<table class="scale-table">
            <thead><tr><th scope="col">Cubic feet</th><th scope="col">Cubic yards</th><th scope="col">Cubic meters</th></tr></thead>
            <tbody>
              <tr><th scope="row">27 ft³</th><td>1 yd³</td><td>0.76 m³</td></tr>
              <tr><th scope="row">54 ft³</th><td>2 yd³</td><td>1.53 m³</td></tr>
              <tr><th scope="row">81 ft³</th><td>3 yd³</td><td>2.29 m³</td></tr>
              <tr><th scope="row">108 ft³</th><td>4 yd³</td><td>3.06 m³</td></tr>
              <tr><th scope="row">135 ft³</th><td>5 yd³</td><td>3.82 m³</td></tr>
              <tr><th scope="row">270 ft³</th><td>10 yd³</td><td>7.65 m³</td></tr>
            </tbody>
          </table>""",
    formula_card=["Volume = length × width × depth", "Cubic yards = cubic feet ÷ 27", "Cubic meters = cubic feet × 0.0283168"],
    formula_note="1 yd³ = 27 ft³ = 0.765 m³. 1 m³ = 1.31 yd³ = 35.31 ft³.",
    guide_intro="A cubic yard is a volume: length times width times depth, with the answer divided by 27.",
    steps=[
        ("Turn every size into feet", "Length, width, and depth must all be in feet before you multiply. Divide inches by 12. 4 inches is 0.33 feet.", "4 in ÷ 12 = 0.33 ft"),
        ("Multiply to get cubic feet", "Length times width times depth gives cubic feet.", "10 ft × 10 ft × 0.33 ft = 33.33 ft³"),
        ("Divide by 27 for cubic yards", "One cubic yard holds 27 cubic feet, so divide the cubic feet by 27.", "33.33 ft³ ÷ 27 = 1.23 yd³"),
        ("Multiply for cubic meters", "One cubic foot is 0.0283168 cubic meters. Multiply the cubic feet by that number.", "33.33 ft³ × 0.0283168 = 0.94 m³"),
        ("Work out the bags", "Divide the cubic feet by the yield of one bag. An 80-lb bag fills 0.60 cubic feet, so round up to whole bags.", "33.33 ft³ ÷ 0.60 = 55.56 → 56 bags"),
    ],
    practice=[
        ("Task 1: A pour 20 ft by 10 ft at 6 in deep. How many cubic yards?",
         "Work out the cubic yards for a 20 ft by 10 ft pour at 6 inches deep.",
         "<strong>Solution:</strong> 6 in is 0.5 ft. 20 × 10 × 0.5 = 100 cubic feet. 100 ÷ 27 = 3.70 cubic yards."),
        ("Task 2: How many cubic feet are in 2.5 cubic yards?",
         "Turn 2.5 cubic yards back into cubic feet.",
         "<strong>Solution:</strong> One cubic yard holds 27 cubic feet, so multiply. 2.5 × 27 = 67.50 cubic feet."),
    ],
    faqs=[
        ("How many cubic feet are in a cubic yard?",
         "27. A cubic yard is a cube 3 feet on each side, and 3 × 3 × 3 = 27. So a cubic yard holds 27 cubic feet."),
        ("How many square feet does a cubic yard cover at 4 inches thick?",
         "81 square feet. One cubic yard is 27 cubic feet, and 4 inches is 0.33 feet, so 27 ÷ 0.33 = 81. At 6 inches thick the same yard covers 54 square feet."),
        ("What is the difference between a cubic yard and a cubic meter?",
         "Both are volumes, in different unit systems. One cubic yard is 0.765 cubic meters, and one cubic meter is 1.31 cubic yards. In the US, concrete is ordered in cubic yards; in most other countries it is ordered in cubic meters."),
        ("Where can I learn more about cubic feet?",
         "The <a href=\"../guides/\">cubic-feet guide</a> walks through cubic feet, cubic yards, and cubic meters with worked examples. This calculator also shows all three units for every pour you type in."),
        ("Is this cubic yard calculator free?",
         "Yes. It is free, with no sign-up. Use it as often as you like, on a phone or a computer."),
    ],
    no_waste=True,
))

# ---------------------------------------------------------------- templates
SKELETON_CSS = """<style>
      /* Loading skeleton — inline so it paints before the stylesheet arrives. */
      .page-skeleton { position: fixed; inset: 0; z-index: 60; background: #f3f1ea; opacity: 0; visibility: hidden; transition: opacity .3s ease, visibility 0s linear .3s; }
      html.is-loading .page-skeleton { opacity: 1; visibility: visible; transition: opacity .15s ease; }
      html.is-ready .page-skeleton { display: none; }
      .sk-inner { max-width: 1050px; margin: 0 auto; padding: 26px 7% 0; }
      .sk-brand { display: flex; align-items: center; gap: 10px; margin-bottom: 52px; }
      .sk-mark { width: 30px; height: 30px; border-radius: 9px 9px 9px 3px; background: #f0a500; color: #232e36; display: grid; place-items: center; font: 600 12px monospace; }
      .sk-bar { position: relative; height: 16px; max-width: 520px; margin: 0 0 14px; border-radius: 4px; background: #e6e4d8; overflow: hidden; }
      .sk-bar--title { height: 34px; max-width: 420px; }
      .sk-bar--short { max-width: 300px; }
      .sk-bar::after, .sk-card::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, #fffdf8 50%, transparent); transform: translateX(-100%); animation: sk-shimmer 1.4s infinite; }
      .sk-card { position: relative; height: 220px; margin-top: 34px; border-radius: 10px; background: #e6e4d8; overflow: hidden; }
      @keyframes sk-shimmer { to { transform: translateX(100%); } }
      @media (prefers-reduced-motion: reduce) { .sk-bar::after, .sk-card::after { animation: none; } }
    </style>"""

SKELETON_SCRIPT = """<script>
      /* Loading skeleton: this timer lives in <head> (before any stylesheet) so a slow connection can't delay it. */
      (function () {
        var root = document.documentElement;
        var done = false;
        setTimeout(function () { if (!done && document.readyState !== "complete") root.classList.add("is-loading"); }, 400);
        function hide() {
          if (done) return;
          done = true;
          root.classList.remove("is-loading");
          setTimeout(function () { root.classList.add("is-ready"); }, 400);
        }
        window.addEventListener("load", hide);
        setTimeout(hide, 2500);
      })();
    </script>"""

def data_attrs(d):
    parts = []
    for k, v in d.items():
        parts.append(f'data-{k}="{html.escape(str(v), quote=True)}"')
    return " ".join(parts)

def field_html(f, slug):
    key, label = f["key"], f["label"]
    if f["kind"] == "int":
        return f"""<div class="field" id="{key}-field">
                  <label for="{key}">{label}</label>
                  <div class="input-with-unit">
                    <input id="{key}" name="{key}" type="number" min="1" step="1" value="{f['value']}" inputmode="numeric">
                  </div>
                  <small class="field-hint">Whole number, 1 or more.</small>
                </div>"""
    units = AREA_UNITS if f["kind"] == "area" else UNIT_OPTIONS
    opts = "".join(
        f'<option value="{u}"{" selected" if u == f["unit"] else ""}>{AREA_LABEL[u] if f["kind"] == "area" else u}</option>'
        for u in units
    )
    hint = ""
    if f["kind"] == "area":
        hint = '<small class="field-hint">Add up every door and window. Use 0 if there are none.</small>'
    return f"""<div class="field" id="{key}-field">
                  <label for="{key}">{label}</label>
                  <div class="input-with-unit">
                    <input id="{key}" name="{key}" type="number" min="0" step="any" value="{f['value']}" inputmode="decimal">
                    <select id="{key}-unit" name="{key}Unit" aria-label="Unit for {label.lower()}">
                      {opts}
                    </select>
                  </div>
                  {hint}
                </div>"""

def render_html(p):
    slug = p["slug"]
    name = p["title"].replace(" | concretecalc.", "")
    canonical = f"{BASE}/{slug}/"
    has_waste = not p.get("no_waste")
    has_shape = slug == "column"

    # --- JSON-LD
    webapp = {"@context": "https://schema.org", "@type": "WebApplication",
              "name": name, "applicationCategory": "UtilitiesApplication",
              "operatingSystem": "Any", "inLanguage": "en", "description": p["desc"]}
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}}
                             for q, a in p["faqs"]]}
    bread = {"@context": "https://schema.org", "@type": "BreadcrumbList",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                 {"@type": "ListItem", "position": 2, "name": name, "item": canonical}]}
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": name,
             "step": [{"@type": "HowToStep", "name": t, "text": f"{txt} {eq}"}
                      for t, txt, eq in p["steps"]]}

    # --- fields
    if has_shape:
        rect = "".join(field_html(f, slug) for f in p["fields"] if f.get("shape") == "rect")
        rnd = "".join(field_html(f, slug) for f in p["fields"] if f.get("shape") == "round")
        common = "".join(field_html(f, slug) for f in p["fields"] if not f.get("shape"))
        fields_html = f"""<div class="shape-tabs" role="group" aria-label="Column shape" id="shape-tabs">
                <button type="button" class="shape-tab" id="shape-rect" data-shape="rect" aria-pressed="true">Rectangular</button>
                <button type="button" class="shape-tab" id="shape-round" data-shape="round" aria-pressed="false">Round</button>
              </div>
              <div class="input-grid shape-fields is-active" id="fields-rect">
                {rect}
              </div>
              <div class="input-grid shape-fields" id="fields-round">
                {rnd}
              </div>
              <div class="input-grid">
                {common}
              </div>"""
    else:
        fields_html = '<div class="input-grid">\n' + "".join(field_html(f, slug) for f in p["fields"]) + "\n              </div>"

    options_html = ""
    if has_waste:
        options_html = f"""<div class="calc-options">
                <div class="field">
                  <label for="waste-slider">Waste allowance</label>
                  <div class="waste-row">
                    <input type="range" id="waste-slider" min="0" max="15" step="1" value="10">
                    <span class="waste-value" id="waste-value">10%</span>
                  </div>
                  <small class="field-hint">5–10% for a clean job, 10–15% for rough ground.</small>
                </div>
                <div class="field">
                  <label id="density-label">Concrete density</label>
                  <div class="density-segmented" role="group" aria-labelledby="density-label" id="density-segmented">
                    <button type="button" data-density="150" aria-pressed="true">Standard · 150 lb/ft³</button>
                    <button type="button" data-density="156" aria-pressed="false">Reinforced · 156 lb/ft³</button>
                    <button type="button" data-density="110" aria-pressed="false">Lightweight · 110 lb/ft³</button>
                  </div>
                  <small class="field-hint">Density sets the weight. Standard concrete is 150 lb per cubic foot.</small>
                </div>
              </div>
              <div class="cost-grid">
                <div class="field">
                  <label for="price-yard">Price per cubic yard (optional)</label>
                  <div class="input-with-unit">
                    <input id="price-yard" name="priceYard" type="number" min="0" step="any" placeholder="e.g. 150" inputmode="decimal">
                    <span aria-hidden="true">$ / yd³</span>
                  </div>
                </div>
                <div class="field">
                  <label for="price-bag">Price per bag (optional)</label>
                  <div class="input-with-unit">
                    <input id="price-bag" name="priceBag" type="number" min="0" step="any" placeholder="e.g. 6" inputmode="decimal">
                    <span aria-hidden="true">$ / bag</span>
                  </div>
                </div>
              </div>"""
    else:
        options_html = f"""<div class="cost-grid">
                <div class="field">
                  <label for="price-yard">Price per cubic yard (optional)</label>
                  <div class="input-with-unit">
                    <input id="price-yard" name="priceYard" type="number" min="0" step="any" placeholder="e.g. 150" inputmode="decimal">
                    <span aria-hidden="true">$ / yd³</span>
                  </div>
                </div>
                <div class="field">
                  <label for="price-bag">Price per bag (optional)</label>
                  <div class="input-with-unit">
                    <input id="price-bag" name="priceBag" type="number" min="0" step="any" placeholder="e.g. 6" inputmode="decimal">
                    <span aria-hidden="true">$ / bag</span>
                  </div>
                </div>
              </div>"""

    presets_html = "".join(
        f'<button type="button" class="preset-chip" {data_attrs(d)}>{label}</button>' for label, d in p["presets"]
    )
    examples_html = "".join(
        f'''<button type="button" class="example-card" {data_attrs(d)}><span class="example-symbol">{sym}</span><span class="example-text"><span class="example-title">{t}</span><span class="example-sub">{s}</span></span><span class="example-arrow" aria-hidden="true">↗</span></button>'''
        for sym, t, s, d in p["examples"]
    )
    steps_html = "".join(
        f'''<article class="guide-step"><span class="step-number">{i:02d}</span><div><h3>{t}</h3><p>{txt}</p><span class="step-equation">{eq}</span></div></article>'''
        for i, (t, txt, eq) in enumerate(p["steps"], 1)
    )
    practice_html = "".join(
        f'''<details><summary>{q} <span aria-hidden="true">+</span></summary><p>{txt}</p><p>{sol}</p></details>'''
        for q, txt, sol in p["practice"]
    )
    faq_html = "".join(
        f'''<details><summary>{q} <span aria-hidden="true">+</span></summary><p>{a}</p></details>'''
        for q, a in p["faqs"]
    )
    formula_html = "".join(f"<strong>{x}</strong>" for x in p["formula_card"])

    others = [o for o in PAGES if o["slug"] != slug]
    sib_links = " · ".join(
        f'<a href="../{o["slug"]}/">{o["keyword"].title()}</a>' for o in others[:3]
    )

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#f3f1ea">
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%23f0a500'/%3E%3Ctext x='16' y='21' font-family='monospace' font-size='13' font-weight='700' text-anchor='middle' fill='%23232e36'%3Ecc%3C/text%3E%3C/svg%3E">
    <meta name="description" content="{html.escape(p['desc'], quote=True)}">
    <title>{html.escape(p['title'])}</title>
    <meta property="og:type" content="website">
    <meta property="og:locale" content="en_US">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{html.escape(p['title'])}">
    <meta property="og:description" content="{html.escape(p['desc'], quote=True)}">
{SKELETON_SCRIPT}
    <link rel="preload" href="../fonts/bitter-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="../fonts/dm-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
{SKELETON_CSS}
    <link rel="stylesheet" href="../styles.css?v=1">
    <script type="application/ld+json">
{json.dumps(webapp, indent=2, ensure_ascii=False)}
    </script>
    <script type="application/ld+json">
{json.dumps(faq_ld, indent=2, ensure_ascii=False)}
    </script>
    <script type="application/ld+json">
{json.dumps(bread, indent=2, ensure_ascii=False)}
    </script>
    <script type="application/ld+json">
{json.dumps(howto, indent=2, ensure_ascii=False)}
    </script>
    <script src="app.js" defer></script>
  </head>
  <body class="tool-page">
    <div class="page-skeleton" id="page-skeleton" aria-hidden="true">
      <div class="sk-inner">
        <div class="sk-brand"><span class="sk-mark">cc</span></div>
        <div class="sk-bar sk-bar--title"></div>
        <div class="sk-bar sk-bar--title sk-bar--short"></div>
        <div class="sk-bar"></div>
        <div class="sk-bar sk-bar--short"></div>
        <div class="sk-card"></div>
      </div>
    </div>
    <header class="site-header">
      <a class="brand" href="../" aria-label="concretecalc. home">
        <span class="brand-mark" aria-hidden="true">cc</span>
        <span>concretecalc<span class="brand-period">.</span></span>
      </a>
      <nav class="top-nav" aria-label="Main navigation">
        <a href="../">All calculators</a>
        <a href="../slab/">Slab</a>
        <a href="../cubic-yard/">Cubic yard</a>
        <a href="../guides/">Guides</a>
      </nav>
      <a class="header-cta" href="#calculator">Calculate now <span aria-hidden="true">↗</span></a>
    </header>

    <main>
      <section class="hero">
        <div class="hero-copy">
          <p class="eyebrow"><span class="eyebrow-dot"></span> {p['eyebrow']}</p>
          <h1>{p['h1_main']}<br><span>{p['h1_sub']}</span></h1>
          <p class="hero-description">{p['geo']}</p>
          <div class="hero-actions">
            <a class="text-link calc-link" href="#calculator">Open the calculator <span aria-hidden="true">↓</span></a>
            <a class="text-link" href="#guide">How it works <span aria-hidden="true">↓</span></a>
          </div>
        </div>
      </section>

      <section class="calculator-section" id="calculator">
        <div class="calculator">
          <div class="calc-main">
            <div class="calc-toolbar">
              <span class="live-indicator"><span></span> Ready — type a number</span>
              <button class="reset-button" type="button" id="reset-button">Reset <span aria-hidden="true">↺</span></button>
            </div>
            <form id="{slug}-form" novalidate>
              {fields_html}
              {options_html}
              <p class="form-error" id="form-error" role="alert" hidden></p>
              <button class="calculate-button" type="submit">Calculate <span aria-hidden="true">↗</span></button>
              <p class="live-hint">No need to press the button: the answer updates as you type.</p>
            </form>

            <div class="result-panel" id="result-panel" aria-live="polite" aria-atomic="true">
              <div class="result-topline"><span>YOUR RESULT</span><span class="result-check" aria-hidden="true">✓</span></div>
              <div class="result-value" id="result-value">—</div>
              <p class="result-context" id="result-context"></p>
              <p class="result-also" id="result-also"></p>
              <div class="result-rows" id="result-rows"></div>
              <div class="result-meta"><span id="result-formula"></span><div class="result-actions"><button type="button" id="copy-button">Copy result <span aria-hidden="true">⧉</span></button></div></div>
              <div class="preset-chips" role="group" aria-label="Common sizes">
                <span class="preset-label">Common sizes:</span>
                {presets_html}
              </div>
            </div>
            <noscript><p class="form-error">This page needs JavaScript to calculate. {p['geo']}</p></noscript>
          </div>
          <aside class="calc-aside">
            <span class="aside-number">{p['aside_num']}</span>
            <p class="aside-title">{p['aside_title']}</p>
            <p>{p['aside_text']}</p>
            <a href="#guide">How it works <span aria-hidden="true">→</span></a>
          </aside>
        </div>
      </section>

      <!-- Ad slot placeholder — reserved space for future AdSense (2026-11-24). -->
      <div class="ad-slot" aria-hidden="true">
        <span class="ad-slot-label">Advertisement</span>
        <div class="ad-slot-box">Ad space</div>
      </div>

      <section class="quick-examples" id="examples">
        <div class="quick-title"><span class="eyebrow">Common sizes</span><h2>Three sizes to try.</h2></div>
        <p class="examples-hint">Tap one — the calculator fills itself in.</p>
        <div class="example-strip">
          {examples_html}
        </div>
      </section>

      <section class="table-section" id="table">
        <div class="quick-title"><span class="eyebrow">Reference table</span><h2>{p['table_title']}</h2></div>
        <p class="table-intro">{p['table_intro']}</p>
        <div class="table-wrap">
          {p['table_html']}
        </div>
      </section>

      <section class="guide-section" id="guide">
        <div class="guide-intro">
          <p class="eyebrow">How it works</p>
          <h2>How the {p['keyword']} works.</h2>
          <p>{p['guide_intro']}</p>
          <div class="formula-card"><span>The formulas you need</span>{formula_html}<small>{p['formula_note']}</small></div>
        </div>
        <div class="guide-steps">
          {steps_html}
        </div>
      </section>

      <section class="practice-section" id="practice">
        <div class="quick-title"><span class="eyebrow">Try it yourself</span><h2>Two tasks to try.</h2></div>
        <p class="table-intro">Tap a task to see the worked solution.</p>
        <div class="faq-list">
          {practice_html}
        </div>
      </section>

      <section class="faq-section">
        <div class="faq-heading"><p class="eyebrow">Still wondering?</p><h2>Questions people ask.</h2></div>
        <div class="faq-list">
          {faq_html}
        </div>
      </section>

      <section class="more-tools">
        <div class="quick-title"><span class="eyebrow">More calculators</span><h2>More concrete calculators.</h2></div>
        <p class="more-tools-link"><a href="../">All concrete calculators <span aria-hidden="true">→</span></a></p>
        <p class="more-tools-link">{sib_links}</p>
        <p class="more-tools-link"><a href="../guides/">Concrete guides <span aria-hidden="true">→</span></a></p>
      </section>
    </main>

    <footer class="site-footer">
      <a class="brand footer-brand" href="../"><span class="brand-mark" aria-hidden="true">cc</span><span>concretecalc<span class="brand-period">.</span></span></a>
      <p>Concrete calculators — simple, fast, and free. A product of Hastle.</p>
      <span>© <span id="current-year"></span> concretecalc</span>
    </footer>
  </body>
</html>
"""

# ---------------------------------------------------------------- app.js
JS_TEMPLATE = r"""// concretecalc. — @@SLUG@@ calculator. Vanilla JS only. No framework, no tracking.
// Every size is turned into feet first, then the volume is worked out in
// cubic feet. 1 yd³ = 27 ft³ ≈ 0.765 m³. Bag yields: 40 lb → 0.30 ft³,
// 50 lb → 0.375 ft³, 60 lb → 0.45 ft³, 80 lb → 0.60 ft³.
const FT_PER_UNIT = { ft: 1, in: 1 / 12, yd: 3, m: 3.280839895, cm: 0.03280839895, mm: 0.003280839895 };
const FT2_PER_UNIT = { ft2: 1, m2: 10.763910417, yd2: 9 };
const AREA_LABEL = { ft2: "ft²", m2: "m²", yd2: "yd²" };
const BAG_YIELD = { 40: 0.30, 50: 0.375, 60: 0.45, 80: 0.60 };
const STORAGE_KEY = "concretecalc_@@SLUG@@_v1";
const HAS_WASTE = @@HAS_WASTE@@;
const HAS_SHAPE = @@HAS_SHAPE@@;

const fmt = new Intl.NumberFormat("en-US", { maximumSignificantDigits: 8 });
const fmt2 = (n) => new Intl.NumberFormat("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(n);
const fmtInt = (n) => new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 }).format(n);
const fmtMoney = (n) => "$" + new Intl.NumberFormat("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(n);
const fmtFt = (n) => fmt.format(n);

const FIELDS = @@FIELDS_JSON@@;
const DEFAULTS = @@DEFAULTS_JSON@@;

const form = document.querySelector("#@@SLUG@@-form");
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
    let netFt3 = @@VOLUME_JS@@;
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
    const dims = @@DIMS_JS@@;
    const priceYard = Number(priceYardInput.value);
    const priceBag = Number(priceBagInput.value);

    resultValue.textContent = `${fmt2(baseYd3)} cubic yards`;
    resultContext.textContent = @@CONTEXT_JS@@;
    resultAlso.textContent = HAS_WASTE
      ? `Also: ${fmt2(ordFt3)} cubic feet · ${fmt2(ordM3)} cubic meters`
      : `Also: ${fmt2(netFt3)} cubic feet · ${fmt2(netM3)} cubic meters`;
    resultFormula.textContent = @@FORMULA_JS@@ + (HAS_WASTE ? ` + ${wastePct}% waste = ${fmt2(ordYd3)} yd³` : "");

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
"""

def render_js(p):
    slug = p["slug"]
    has_waste = not p.get("no_waste")
    fields_json = json.dumps([
        {"key": f["key"], "label": f["label"], "kind": f["kind"],
         "unit": bool(f.get("unit")), **({"shape": f["shape"]} if f.get("shape") else {})}
        for f in p["fields"]
    ])
    defaults = {}
    for f in p["fields"]:
        defaults[f["key"]] = f["value"]
        if f.get("unit"):
            defaults[f["key"] + "Unit"] = f["unit"]
    if slug == "column":
        defaults["shape"] = "rect"
    defaults["waste"] = "10"
    defaults["density"] = 150
    js = JS_TEMPLATE
    js = js.replace("@@SLUG@@", slug)
    js = js.replace("@@HAS_WASTE@@", "true" if has_waste else "false")
    js = js.replace("@@HAS_SHAPE@@", "true" if slug == "column" else "false")
    js = js.replace("@@FIELDS_JSON@@", fields_json)
    js = js.replace("@@DEFAULTS_JSON@@", json.dumps(defaults))
    js = js.replace("@@VOLUME_JS@@", p["volume_js"])
    js = js.replace("@@DIMS_JS@@", p["dims_js"])
    js = js.replace("@@FORMULA_JS@@", p["formula_js"])
    js = js.replace("@@CONTEXT_JS@@", p["context_js"])
    return js

# ---------------------------------------------------------------- main
def main():
    written = []
    for p in PAGES:
        d = os.path.join(OUT, p["slug"])
        os.makedirs(d, exist_ok=True)
        html_path = os.path.join(d, "index.html")
        js_path = os.path.join(d, "app.js")
        with open(html_path, "w", encoding="utf-8") as fh:
            fh.write(render_html(p))
        with open(js_path, "w", encoding="utf-8") as fh:
            fh.write(render_js(p))
        written.append((p["slug"], html_path, js_path, len(p["title"]), len(p["desc"])))
    for slug, hp, jp, tl, dl in written:
        print(f"{slug}: {hp} (title {tl} chars, desc {dl} chars) + {jp}")
    print(f"{len(written) * 2} files written.")

if __name__ == "__main__":
    main()
