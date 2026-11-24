"""Merge all retrieved records (current query versions + snowballing + manual
exports), de-duplicate, compute PRISMA identification counts, and write the
screening sheet.

De-duplication: union-find over three keys -- normalised DOI, arXiv id, and
normalised title (+ year +-1 when both years are known). A preprint and its
published version therefore collapse into one candidate (the publisher DOI is
kept as the primary identifier).

Outputs (output/):
  candidates_all.csv     one row per unique work, with full provenance
  screening.csv          screening sheet (two screeners + reason codes + a
                         clearly labelled rule-based SUGGESTION)
  prisma_counts.json     identification / de-duplication numbers
Usage: python -I scripts/merge_dedupe.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from benchmark import match, raw_files  # noqa: E402
from common import OUT, RAW, norm_title, read_csv, read_jsonl, write_csv  # noqa: E402

# ------------------------------------------------------------ pre-filter terms
RX = {
    "net": re.compile(r"\b(network|networks|graph|graphs|node-link|multigraph)\b", re.I),
    "ml_noise": re.compile(r"\b(neural network|neural networks|convolutional|graph neural|gnn|gcn|"
                           r"deep learning|transformer|knowledge graph embedding|perceptron)\b", re.I),
    "vis": re.compile(r"\b(visuali[sz]\w*|visual analytics|visual analysis|node-link|graph drawing|"
                      r"layout|physicali[sz]ation|immersive analytics)\b", re.I),
    "mln": re.compile(r"\b(multi-?layer\w*|multiplex|multi-?relational|layers?)\b", re.I),
    "dyn": re.compile(r"\b(dynamic|temporal|time-varying|evolving)\s+(network|graph)s?\b", re.I),
    "imm": re.compile(r"\b(augmented[- ]reality|mixed[- ]reality|virtual[- ]reality|extended[- ]reality|immersive|"
                      r"head-mounted|hololens|\bvr\b|\bar\b|\bxr\b|cave)\b", re.I),
    "phys": re.compile(r"\b(physicali[sz]ation|physical visuali[sz]ation|tangible|3d[- ]print\w*)\b", re.I),
    "ds": re.compile(r"\bdesign space", re.I),
    "touch": re.compile(r"\b(tangible|touch|physical (object|referent|prop)s?|handheld)\b", re.I),
    "paratext": re.compile(r"^(editor'?s evaluation|author response|reviewer|decision letter|erratum|"
                           r"correction|retraction|front matter|back matter|table of contents|"
                           r"cover|index|preface|foreword|committee)\b", re.I),
}


def suggest(r: dict) -> tuple[str, str]:
    """Transparent rule-based SUGGESTION only (humans decide).

    include? : title has network/layer AND visual/immersive/physical term, and
               the record mentions an MLN/dynamic/immersive/physical/design-space term;
               or title has immersive term AND (design space | tangible | touch).
    check    : network+visualization, or immersive+visualization, anywhere.
    exclude? : paratext, or none of the above.
    """
    t = r["title"] or ""
    txt = f"{t} {r.get('abstract') or ''}"
    f = {k: bool(v.search(txt)) for k, v in RX.items()}
    ft = {k: bool(v.search(t)) for k, v in RX.items()}
    if RX["paratext"].search(t):
        return "exclude?", "paratext (editorial/review/erratum)"
    if r.get("unstructured_ref"):
        return "check", "unresolved reference string (no DOI) - verify manually"
    topical = f["mln"] or f["dyn"] or f["imm"] or f["phys"] or f["ds"]
    if (ft["net"] or ft["mln"]) and (ft["vis"] or ft["imm"] or ft["phys"]) and topical:
        return "include?", "title: network/layer + visual/immersive/physical term"
    if ft["imm"] and (f["ds"] or RX["touch"].search(txt)) and f["vis"]:
        return "include?", "title: immersive term; text: design space or tangible/touch + visualization"
    if f["net"] and f["ml_noise"] and not f["vis"]:
        return "exclude?", "machine-learning sense of network/graph"
    if f["net"] and f["vis"]:
        return "check", "network/graph + visualization terms"
    if (f["imm"] or f["phys"]) and f["vis"]:
        return "check", "immersive/physical + visualization terms"
    if not r.get("abstract"):
        return "check", "no abstract available - screen by title/full text"
    return "exclude?", "no network+visualization and no immersive/physical+visualization terms"


class UF:
    def __init__(self):
        self.p = {}

    def f(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def u(self, a, b):
        self.p[self.f(a)] = self.f(b)


def provenance_label(src: str, rec: dict) -> str:
    if src == "snowball":
        api = rec["source"].replace("snowball-", "")
        return f"{rec['snowball_round']}:{rec['snowball_seed']}:{rec['snowball_direction']}:{api}"
    return f"{src}:{rec['query_id']}_{rec['query_version']}"


def main():
    global CR
    CR = {r["doi"]: r for r in read_jsonl(RAW / "enrich" / "crossref_meta.jsonl")}
    recs = []
    per_file = []
    for src, f in raw_files():
        rows = read_jsonl(f)
        per_file.append({"file": f"{src}/{f.stem}", "records": len(rows)})
        for r in rows:
            r["_prov"] = provenance_label(src, r)
            r["_stage"] = "snowball" if src == "snowball" else "search"
            recs.append(r)
    uf = UF()
    for i, r in enumerate(recs):
        node = f"r{i}"
        uf.f(node)
        if r["doi"]:
            uf.u(node, "d:" + r["doi"])
        if r["arxiv"]:
            uf.u(node, "a:" + r["arxiv"])
        nt = norm_title(r["title"])
        if len(nt) > 25:
            uf.u(node, "t:" + nt.replace(" ", ""))
    groups = defaultdict(list)
    for i, r in enumerate(recs):
        groups[uf.f(f"r{i}")].append(r)

    # attach unstructured Crossref reference strings (no DOI) to a candidate whose
    # normalised title occurs verbatim inside the reference string
    titled = {}
    for k, g in groups.items():
        if not all(x["source"] == "snowball-crossref" and not x["doi"] for x in g):
            for x in g:
                nt = norm_title(x["title"])
                if len(nt) > 30 and x["source"] != "snowball-crossref":
                    titled.setdefault(nt, k)
    for k in [k for k, g in groups.items() if all(x["source"] == "snowball-crossref" and not x["doi"] for x in g)]:
        s = norm_title(" ".join(x["title"] for x in groups[k]))
        hit = next((tk for nt, tk in titled.items() if nt in s), None)
        if hit:
            groups[hit] += groups.pop(k)

    cands = []
    for g in groups.values():
        def pick(field, prefer=None):
            vals = [x[field] for x in g if x.get(field)]
            if prefer:
                good = [v for v in vals if prefer(v)]
                vals = good or vals
            return max(vals, key=len) if field in ("abstract", "title") and vals else (vals[0] if vals else "")
        gt = [x for x in g if x["source"] != "snowball-crossref"] or g
        tvals = [x["title"] for x in gt if x.get("title")]
        title = max(set(tvals), key=lambda v: (tvals.count(v), -len(v))) if tvals else ""
        doi = pick("doi", lambda v: not v.startswith("10.48550/"))
        venue = pick("venue", lambda v: "arxiv" not in v.lower())
        years = sorted({int(x["year"]) for x in g if str(x.get("year", "")).isdigit()})
        prov = sorted({x["_prov"] for x in g})
        c = {
            "cid": "", "title": title, "unstructured_ref": all(x["source"] == "snowball-crossref" and not x["doi"] for x in g), "year": years[0] if years else "",
            "venue": venue, "doi": doi, "arxiv": pick("arxiv"),
            "openalex_id": pick("openalex_id"), "s2_id": pick("s2_id"), "dblp_key": pick("dblp_key"),
            "authors": pick("authors"), "type": pick("type"), "abstract": pick("abstract"),
            "found_by_search": "yes" if any(x["_stage"] == "search" for x in g) else "no",
            "found_by_snowball": "yes" if any(x["_stage"] == "snowball" for x in g) else "no",
            "provenance": " | ".join(prov), "n_records": len(g),
        }
        if c["doi"] in CR and not c["abstract"]:
            c["abstract"] = CR[c["doi"]]["abstract"]
            c["venue"] = c["venue"] or CR[c["doi"]]["venue"]
        c["benchmark_id"] = next((m for x in g if (m := match(x))), "")
        c["suggestion"], c["suggestion_rule"] = suggest(c)
        cands.append(c)
    cands.sort(key=lambda c: (c["found_by_search"] != "yes", str(c["year"]), norm_title(c["title"])))
    for i, c in enumerate(cands, 1):
        c["cid"] = f"C{i:05d}"

    cols = ["cid", "title", "year", "venue", "doi", "arxiv", "authors", "type", "found_by_search",
            "found_by_snowball", "provenance", "n_records", "benchmark_id", "openalex_id", "s2_id",
            "dblp_key", "suggestion", "suggestion_rule", "abstract"]
    write_csv(OUT / "candidates_all.csv", cands, cols)

    scr_cols = ["cid", "title", "year", "venue", "doi", "arxiv", "found_by_search", "found_by_snowball",
                "provenance", "SUGGESTION_rule_based_not_a_decision", "suggestion_rule",
                "S1_decision", "S1_reason", "S2_decision", "S2_reason", "agree",
                "final_decision", "final_reason", "fulltext_decision", "fulltext_reason",
                "category_I1_I4_B", "notes", "abstract"]
    scr = []
    for c in cands:
        s = {k: c.get(k, "") for k in scr_cols}
        s["SUGGESTION_rule_based_not_a_decision"] = c["suggestion"]
        scr.append(s)
    write_csv(OUT / "screening.csv", scr, scr_cols)

    n_search = sum(1 for r in recs if r["_stage"] == "search")
    n_snow = len(recs) - n_search
    counts = {
        "records_identified_total": len(recs),
        "records_identified_database_search": n_search,
        "records_identified_snowballing": n_snow,
        "records_per_file": per_file,
        "records_per_source": dict(Counter(r["_prov"].split(":")[0] if r["_stage"] == "search"
                                           else "snowball-" + r["source"].replace("snowball-", "")
                                           for r in recs)),
        "unique_after_dedup": len(cands),
        "unique_from_search": sum(c["found_by_search"] == "yes" for c in cands),
        "unique_only_from_snowball": sum(c["found_by_search"] == "no" for c in cands),
        "duplicates_removed": len(recs) - len(cands),
        "with_abstract": sum(bool(c["abstract"]) for c in cands),
        "suggestion_counts": dict(Counter(c["suggestion"] for c in cands)),
        "benchmark_in_candidates": sorted({c["benchmark_id"] for c in cands if c["benchmark_id"]}),
    }
    (OUT / "prisma_counts.json").write_text(json.dumps(counts, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in counts.items() if k != "records_per_file"}, indent=1))


if __name__ == "__main__":
    main()
