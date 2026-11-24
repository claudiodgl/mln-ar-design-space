"""Coded matrix of the additional works (same visual style as Table 2 of the paper).

Usage: python -I -X utf8 scripts/build_supplement_matrix.py <supplement_dir>
Writes tables/additional_matrix.tex (tabular body only).
"""
import sys
from pathlib import Path

SUP = Path(sys.argv[1])

# (header, cite key, platform group)
W = [
    ("Detangler", "Renoust2015detangler", "D"), ("MultiStory", "Meidiana2015multistory", "D"),
    ("Hybrid MLN", "Durant2024hybrid", "D"), ("MiRA", "Nehoray2026mira", "D"),
    ("Sparse Tangibles", "Arif2016sparse", "D"), ("Tangible BioNets", "Manshaei2019bionets", "D"),
    ("Path tracing (VR)", "McGuffin2023pathtracing", "V"),
    ("Magic lens", "Drochtert2015magiclens", "A"), ("Ego-centric AR", "Zhao2017egocentric", "A"),
    ("AI Mind-map", "Kyaw2026mindmap", "A"),
    ("Path tracing (print)", "McGuffin2023pathtracing", "P"), ("Haptic phys.", "Drogemuller2021haptic", "P"),
    ("NodeBots", "Bhattacharya2026nodebots", "P"),
]
CODES = {
    "Detangler": "Color Size Shape 2D Rotation Scale Merged Node-link NodePos Aggregated VirtEl Select",
    "MultiStory": "Color Size 2D Linked Merged Node-link NodePos Aggregated VirtEl Select Filter",
    "Hybrid MLN": "Color 2D Linked Hybrid NodeOrd Mixed",
    "MiRA": "Color Size 2D Separated Linked Merged Node-link NodePos Aggregated Shared VirtEl Select Filter",
    "Sparse Tangibles": "Color 2D Separated Node-link NodePos Mixed VirtEl Arrange Select Filter",
    "Tangible BioNets": "Color Size 2D Separated Node-link NodePos Mixed VirtEl Select",
    "Path tracing (VR)": "2D 3D Rotation Scale Floating Node-link NodePos Tangible VirtEl Arrange Select",
    "Magic lens": "Size 3D PhysAnchor Node-link NodePos Touch Tangible VirtEl Arrange Select Filter",
    "Ego-centric AR": "Color Size 2D PhysAnchor Aggregated Touch VirtEl Select",
    "AI Mind-map": "2D PhysAnchor Node-link NodePos Touch Voice VirtEl Select",
    "Path tracing (print)": "3D Rotation PhysAnchor Node-link NodePos Tangible PhysEl Arrange",
    "Haptic phys.": "2D Rotation PhysAnchor Node-link NodePos Tangible PhysEl Arrange",
    "NodeBots": "Color 2D PhysAnchor Separated Node-link NodePos Mixed Tangible PhysEl SpatialCtx Arrange Select",
}
ROWS = [
 ("v",1,"Color","color.pdf","Color"),("v",1,"Size","size2.pdf","Size"),("v",1,"Shape","shape.pdf","Shape"),("v",1,"Texture","texture.pdf","Texture"),
 ("v",2,"2D","2D.pdf","2D"),("v",2,"3D","3D.pdf","3D"),
 ("v",3,"Rotation","rotation.pdf","Rotation"),("v",3,"Scale","scale.pdf","Scale"),
 ("v",4,"PhysAnchor","holder.pdf","Phys.\\ Anchor"),("v",4,"Floating","floating.pdf","Floating"),
 ("v",5,"Separated","separated.pdf","Separated"),("v",5,"Linked","linked.pdf","Linked"),("v",5,"Merged","merged.pdf","Merged"),
 ("l",6,"Node-link","nodelink.pdf","Node-link"),("l",6,"Matrix","matrix.pdf","Matrix"),("l",6,"Hybrid","hybrid.pdf","Hybrid"),
 ("l",7,"NodePos","force.pdf","Node Pos."),("l",7,"NodeOrd","nodeordering.pdf","Node Ord."),("l",7,"Aggregated","aggregated.pdf","Aggregated"),
 ("l",8,"Shared","shared.pdf","Shared"),("l",8,"Mixed","mixed.pdf","Mixed"),("l",8,"Independent","independent.pdf","Independent"),
 ("u",9,"Midair","midair.pdf","Mid-air"),("u",9,"Touch","touch.pdf","Touch"),("u",9,"Tangible","tangible.pdf","Tangible"),("u",9,"Gaze","gaze.pdf","Gaze"),("u",9,"Voice","mic.pdf","Voice"),
 ("u",10,"PhysEl","physicalelements.pdf","Phys.\\ Elem."),("u",10,"VirtEl","virtualelements.pdf","Virt.\\ Elem."),("u",10,"SpatialCtx","spatialcontext.pdf","Spatial Ctx."),
 ("u",11,"Arrange","orientation.pdf","Arrange"),("u",11,"Select","select.pdf","Select"),("u",11,"Filter","filtering.pdf","Filter"),
]
PARTCOL = {"v": "visualizationcolor", "l": "layoutcolor", "u": "usercolor"}
PARTNAME = {"v": "Visualization State", "l": "Layout Possibilities", "u": "User Interaction"}
NA = {
    "D": {"PhysAnchor", "Floating", "Midair", "Touch", "Tangible", "Gaze", "Voice", "PhysEl", "SpatialCtx"},
    "V": {"SpatialCtx"},
    "P": {"Floating", "Midair", "Touch", "Gaze", "Voice", "VirtEl"},
}
codes = {h: set(CODES[h].split()) for h, _, _ in W}
valid = {r[2] for r in ROWS}
for h, c in codes.items():
    assert not (c - valid), (h, c - valid)

groups = ["D", "V", "A", "P"]; gname = {"D": "Desktop", "V": "VR", "A": "AR", "P": "Phys."}
counts = [sum(1 for w in W if w[2] == g) for g in groups]
ncol = 2 + len(W)
SEP = "@{\\hspace{3pt}}|@{\\hspace{3pt}}"
SEPM = "c@{\\hspace{3pt}}|@{\\hspace{3pt}}"
spec = "l|l@{\\hspace{2.5pt}}" + SEP.join("c" * n for n in counts)
hdr1 = " \\multicolumn{1}{l}{} & & " + " & ".join(
    "\\multicolumn{%d}{%s}{%s}" % (n, SEPM if i < 3 else "c", gname[g]) for i, (g, n) in enumerate(zip(groups, counts))) + " \\\\"
names = []
for i, (h, k, g) in enumerate(W):
    cell = "\\rotatebox{90}{%s~\\cite{%s}}" % (h, k)
    if ((i == len(W) - 1) or (W[i + 1][2] != g)) and g != "P":
        cell = "\\multicolumn{1}{%s}{%s}" % (SEPM, cell)
    names.append(cell)
hdr2 = " \\multicolumn{1}{l}{} & & " + " & ".join(names) + " \\\\ \\midrule"

lines = []
for idx, (part, grp, code, icon, label) in enumerate(ROWS):
    col = PARTCOL[part]
    nxt = ROWS[idx + 1] if idx + 1 < len(ROWS) else None
    first = "\\cellcolor{%s!25}" % col
    if nxt is None or nxt[0] != part:
        n = sum(1 for r in ROWS if r[0] == part)
        first += "\\multirow{-%d}{*}{\\rotatebox{90}{\\scalebox{0.85}{\\bfseries %s}}}" % (n, PARTNAME[part])
    second = "\\cellcolor{%s!25}\\tabimg{%s}%s" % (col, icon, label)

    def cell(h, g):
        if code in codes[h]:
            assert code not in NA.get(g, ()), (h, code)
            return " \\ensuremath{\\bullet} "
        return " \\cellcolor{nagray} " if code in NA.get(g, ()) else "  "
    lines.append(first + " & " + second + " &" + "&".join(cell(h, g) for h, _, g in W) + "\\\\")
    if nxt is not None:
        if nxt[0] != part:
            lines.append("\\arrayrulecolor{black}\\specialrule{0.6pt}{1.5pt}{1.5pt}")
        elif nxt[1] != grp:
            W1 = "\\noalign{\\global\\arrayrulewidth=1pt}"
            W0 = "\\noalign{\\global\\arrayrulewidth=0.4pt}"
            gap = "\\hhline{>{\\arrayrulecolor{%s!25}}->{\\arrayrulecolor{white}}*{%d}{-}}" % (col, ncol - 1)
            grey = "\\hhline{>{\\arrayrulecolor{%s!25}}->{\\arrayrulecolor{black}}|>{\\arrayrulecolor{black!35}}*{%d}{-}}" % (col, ncol - 1)
            lines.append(W1 + gap + W0 + grey + W1 + gap + W0 + "\\arrayrulecolor{black}")
lines.append("\\bottomrule")
out = "\n".join(["% generated by scripts/build_supplement_matrix.py", "\\begin{tabular}{%s}" % spec, "\\toprule", hdr1, hdr2]
                + lines + ["\\end{tabular}"])
(SUP / "tables" / "additional_matrix.tex").write_text(out + "\n", encoding="utf-8")
print("ok", len(W), "works")
