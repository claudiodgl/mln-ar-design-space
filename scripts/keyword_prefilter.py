"""Documented automatic keyword exclusion applied before title/abstract screening
of snowballing rounds >= 2 (protocol section 6, workload rule).

A record is KEPT for screening if its title+abstract (title only when no abstract)
matches at least one of:
  A. a network/graph term AND a visualization/immersive/physical term
  B. an immersive/AR/VR/physical term AND a visualization term
  C. a multilayer/multiplex/multi-relational term
  D. (no abstract available) any network, visualization, or immersive term in the title
Otherwise it is excluded automatically with reason code E0 (keyword rule).

Usage:
  python -I scripts/keyword_prefilter.py <in.csv> <out_kept.csv> [--validate output/screening.csv]
--validate reports how many records with a verified include/background decision
in an earlier round the rule would have kept (recall check of the rule).
"""
import argparse, csv, re

W = lambda pats: re.compile(r"(?i)" + "|".join(x.replace(" ", r"[- ]?") for x in pats))   # spaces also match hyphens
NET = W([r"\bnetworks?\b", r"\bgraphs?\b", r"node-link", r"multi-?layer", r"multiplex", r"multi-relational",
         r"\bconnectom", r"knowledge graph", r"\bhypergraph"])
VIS = W([r"visuali[sz]", r"visual analy", r"immersive", r"virtual reality", r"augmented reality", r"mixed reality",
         r"extended reality", r"hololens", r"head-?mounted", r"\bVR\b", r"\bAR\b", r"\bXR\b", r"\bMR\b",
         r"physicali[sz]", r"tangible", r"stereoscop", r"\b3D\b", r"three-dimensional", r"node-link", r"matrix cube",
         r"layout", r"graph drawing"])
ARX = W([r"augmented reality", r"mixed reality", r"hololens", r"\bAR\b", r"\bMR\b"])
VIS2 = W([r"visuali[sz]", r"visual analy", r"situated analytics", r"immersive analytics", r"visual represent", r"data", r"space-time cube"])
ARSPEC = W([r"tangible", r"\btouch", r"physical", r"situated", r"anchor", r"spatial", r"handheld", r"embedded", r"referent"])
IMM = W([r"immersive", r"virtual reality", r"augmented reality", r"mixed reality", r"\bVR\b", r"\bAR\b",
         r"physicali[sz]", r"tangible", r"hololens", r"situated", r"head-?mounted", r"see-through"])

def _norm(s):
    s = s or ""
    if s and " " not in s.strip() and len(s) > 25:          # titles stored without spaces
        s = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", s)
    return s

MLN = W([r"multi-?layer", r"multiplex", r"multi-relational", r"multi-?layered", r"multi-?faceted", r"interdependent"])

def keep(title, abstract):
    title, abstract = _norm(title), (abstract or "")
    txt = f"{title} {abstract}"
    if NET.search(txt) and VIS.search(txt): return "A"          # network/graph + vis/immersive/physical
    if IMM.search(txt) and VIS2.search(txt): return "B"         # immersive/AR/physical + visualization
    if MLN.search(txt): return "C"                               # multilayer/multiplex networks
    if not abstract.strip() and (NET.search(title) or VIS2.search(title) or IMM.search(title)): return "D"
    return ""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--validate"); a = ap.parse_args()
    rows = list(csv.DictReader(open(a.inp, encoding="utf-8-sig")))
    kept = []
    for r in rows:
        k = keep(r.get("title", ""), r.get("abstract", ""))
        if k: r["prefilter_rule"] = k; kept.append(r)
    with open(a.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) + ["prefilter_rule"]); w.writeheader(); w.writerows(kept)
    print(f"input {len(rows)} | kept {len(kept)} | excluded by keyword rule (E0) {len(rows)-len(kept)}")
    if a.validate:
        v = list(csv.DictReader(open(a.validate, encoding="utf-8-sig")))
        dec = lambda r: (r.get("final_decision") or r.get("AI_decision"))
        for lab in ("include", "background"):
            pos = [r for r in v if dec(r) == lab]
            miss = [r for r in pos if not keep(r["title"], r.get("abstract", ""))]
            print(f"validation on earlier round, {lab}: {len(pos)-len(miss)}/{len(pos)} kept")
            for r in miss: print("  would miss:", r["cid"], r["title"][:90])

if __name__ == "__main__":
    main()
