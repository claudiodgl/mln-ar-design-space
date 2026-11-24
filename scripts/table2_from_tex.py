"""Regenerate config/table2_codes.json from Table 2 (label tab:coding) of the paper.

Usage: python -I -X utf8 scripts/table2_from_tex.py <paper.tex>
Each work gets the values marked with a bullet (codes), the values that are
not applicable to its platform (grey cells), and, if any, values marked with
a hollow dot (studied on edges within a single network).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
tex = Path(sys.argv[1]).read_text(encoding="utf-8")
tab = tex[tex.index(r"\label{tab:coding}"):]
tab = tab[:tab.index(r"\end{tabular}")]
hdr = next(l for l in tab.splitlines() if r"\rotatebox{90}{muxViz" in l)
works = re.findall(r"\\rotatebox\{90\}\{(.+?)~\\cite\{([^}]+)\}\}", hdr)
assert len(works) == 28, len(works)
# platform blocks from the header row: \multicolumn{n}{...}{Desktop|VR|AR|Phys.}
prow = next(l for l in tab.splitlines() if "{Desktop}" in l)
blocks = [(re.search(r"\\multicolumn\{(\d+)\}", cell).group(1), p)
          for cell in prow.split("&")
          for p in re.findall(r"\{(Desktop|VR|AR|Phys\.)\}", cell)]
plat = [("Physicalization" if p == "Phys." else p) for n, p in blocks for _ in range(int(n))]
assert len(plat) == 28, blocks

values, group_of = [], {}
codes = [[] for _ in works]; na = [[] for _ in works]; hollow = [[] for _ in works]
pending = []
for line in tab.splitlines():
    m = re.search(r"\\tabimg\{[^}]+\}(.+?) &(.*)\\\\\s*$", line)
    if not m:
        continue
    label = m.group(1).replace("\\ ", " ").strip()
    cells = m.group(2).split("&")
    assert len(cells) == 28, (label, len(cells))
    values.append(label); pending.append(label)
    g = re.search(r"\\bfseries ([^}]+)\}", line)
    if g:  # the group label sits on the last row of its group
        for v in pending:
            group_of[v] = g.group(1)
        pending = []
    for i, c in enumerate(cells):
        if r"\bullet" in c:
            codes[i].append(label)
        elif "nnb" in c:
            hollow[i].append(label)
        elif "nagray" in c:
            na[i].append(label)

out = {"source": "Table 2 (tab:coding) of the paper; regenerate with scripts/table2_from_tex.py",
       "values": [{"value": v, "group": group_of.get(v, "")} for v in values], "works": []}
for (lab, key), p, c, n, h in zip(works, plat, codes, na, hollow):
    lab = lab.replace("\\ ", " ").replace('B{\\"u}schel', "Büschel")
    w = {"label": lab, "key": key, "platform": p, "codes": c, "not_applicable": n}
    if h:
        w["codes_single_network_edges"] = h
    out["works"].append(w)
(ROOT / "config" / "table2_codes.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print(len(values), "values;", len(out["works"]), "works")
for w in out["works"]:
    print(f"  {w['platform']:15s} {w['label']:22s} {len(w['codes']):2d} codes")
