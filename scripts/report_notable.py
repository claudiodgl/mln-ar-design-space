"""List non-benchmark candidates whose TITLE alone signals the core topics, so the
authors can decide early whether to code them or record an exclusion reason.
This is a reading aid, not a screening decision.

Output: output/notable_candidates.csv
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import OUT, read_csv, write_csv  # noqa: E402

NET = re.compile(r"network|graph|node-link", re.I)
NOISE = re.compile(r"neural|convolution|scene graph|perceptron", re.I)
GROUPS = [
    ("AR/MR + network", re.compile(r"augmented reality|mixed reality|\bAR\b|\bMR\b|hololens|"
                                   r"augmented|mixed-reality", re.I)),
    ("physical/tangible + network", re.compile(r"physicali[sz]|tangible|3d[- ]print|tactile|haptic", re.I)),
    ("multilayer/multiplex + visual", re.compile(r"multi-?layer|multiplex|multi-?relational", re.I)),
    ("VR/immersive + network", re.compile(r"virtual reality|immersive|\bVR\b|head-mounted|\bCAVE\b", re.I)),
]
VIS = re.compile(r"visuali|visual|explor|layout|drawing|interact|navigat|immersive|percept|"
                 r"physicali|tangible|selection|comparison|analytics", re.I)


def main():
    rows = []
    for c in read_csv(OUT / "candidates_all.csv"):
        t = c["title"]
        if c["benchmark_id"] or not NET.search(t) or NOISE.search(t):
            continue
        for name, rx in GROUPS:
            if rx.search(t) and VIS.search(t):
                rows.append({"group": name, "cid": c["cid"], "year": c["year"], "title": t,
                             "venue": c["venue"], "doi": c["doi"], "n_records": c["n_records"],
                             "found_by_search": c["found_by_search"],
                             "found_by_snowball": c["found_by_snowball"],
                             "provenance": c["provenance"]})
                break
    order = {g[0]: i for i, g in enumerate(GROUPS)}
    rows.sort(key=lambda r: (order[r["group"]], -int(r["n_records"]), str(r["year"])))
    write_csv(OUT / "notable_candidates.csv", rows, list(rows[0].keys()))
    from collections import Counter
    print(Counter(r["group"] for r in rows))


if __name__ == "__main__":
    main()
