"""Render the concept-block queries of config/queries.json into each source's syntax.

A query is a list of *groups* that are AND-ed; each group is a list of block
names whose terms are OR-ed.  Example: [["MLN"], ["NET"], ["VIS"]] means
(MLN terms) AND (NET terms) AND (VIS terms).

Run `python -I scripts/querybuild.py` to print every rendered string (this is
what goes verbatim into protocol.md / the supplement).
"""
from __future__ import annotations

import re

WB = chr(92) + "b"  # regex word boundary
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load_queries  # noqa: E402


def _terms(blocks: dict, group: list[str]) -> list[str]:
    out: list[str] = []
    for b in group:
        for t in blocks[b]:
            if t not in out:
                out.append(t)
    return out


def _q(t: str) -> str:
    return f'"{t}"' if re.search(r"[\s\-]", t) else t


# ------------------------------------------------------------------ OpenAlex
def openalex(blocks, groups) -> str:
    """Value for filter=title_and_abstract.search:<...> (boolean, stemmed)."""
    return " AND ".join("(" + " OR ".join(_q(t) for t in _terms(blocks, g)) + ")" for g in groups)


# --------------------------------------------------------- Semantic Scholar
def s2(blocks, groups) -> str:
    """/paper/search/bulk query syntax: + AND, | OR, "phrase", ( )."""
    return " + ".join("(" + " | ".join(_q(t) for t in _terms(blocks, g)) + ")" for g in groups)


# -------------------------------------------------------------------- arXiv
def arxiv(blocks, groups) -> str:
    parts = []
    for g in groups:
        ors = []
        for t in _terms(blocks, g):
            tt = f'"{t}"' if re.search(r"[\s\-]", t) else t
            ors += [f"ti:{tt}", f"abs:{tt}"]
        parts.append("(" + " OR ".join(ors) + ")")
    return " AND ".join(parts)


# ------------------------------------------------- Eurographics DL (DSpace/Solr)
def _egdl_term(t: str) -> str:
    w = re.split(r"[\s\-]+", t)
    return w[0] if len(w) == 1 else "(" + " AND ".join(w) + ")"


def egdl(blocks, groups) -> str:
    parts = []
    for g in groups:
        inner = " OR ".join(_egdl_term(t) for t in _terms(blocks, g))
        parts.append("(" + " OR ".join(f"{f}:({inner})" for f in
                                       ("dc.title", "dc.description.abstract", "dc.subject")) + ")")
    return " AND ".join(parts)


# ---------------------------------------------------------------- IEEE Xplore
IEEE_FIELDS = ("Document Title", "Abstract")
IEEE_MAX_TERMS = 25   # Xplore command search limit on search terms per query (verify in UI)


def ieee(blocks, groups) -> list[str]:
    """querytext(s) for the Xplore Metadata API / the 'Command Search' box.

    Each field:term pair counts as one search term. If a query exceeds
    IEEE_MAX_TERMS, the largest OR-group is halved recursively; the union of
    the resulting sub-queries is logically identical to the full query
    (records are merged and de-duplicated afterwards).
    """
    nf = len(IEEE_FIELDS)

    def split(tl: list[list[str]]) -> list[list[list[str]]]:
        if sum(len(t) for t in tl) * nf <= IEEE_MAX_TERMS or all(len(t) == 1 for t in tl):
            return [tl]
        big = max(range(len(tl)), key=lambda i: len(tl[i]))
        h = (len(tl[big]) + 1) // 2
        a = [t if i != big else t[:h] for i, t in enumerate(tl)]
        b = [t if i != big else t[h:] for i, t in enumerate(tl)]
        return split(a) + split(b)

    def grp(ts):
        return "(" + " OR ".join(f'"{f}":{_q(t)}' for t in ts for f in IEEE_FIELDS) + ")"

    return [" AND ".join(grp(t) for t in tl) for tl in split([_terms(blocks, g) for g in groups])]


# -------------------------------------------------------------------- ACM DL
def acm(blocks, groups) -> str:
    """String for ACM DL Advanced Search -> 'Edit search' (query syntax)."""
    parts = []
    for g in groups:
        inner = " OR ".join(_q(t) for t in _terms(blocks, g))
        parts.append(f"(Title:({inner}) OR Abstract:({inner}) OR Keyword:({inner}))")
    return " AND ".join(parts)


# ------------------------------------------------------------ DBLP (titles)
def dblp_regexes(blocks, groups) -> list[str]:
    """One case-insensitive regex per AND-group, applied to dblp titles."""
    out = []
    for g in groups:
        alts = []
        for t in _terms(blocks, g):
            stem = re.escape(t.lower()).replace(r"\-", "[- ]?").replace(r"\ ", "[- ]")
            if t.isupper() and len(t) <= 3:      # acronyms: VR, AR, XR, MR
                stem = stem + WB
            alts.append(WB + stem)
        out.append("(" + "|".join(alts) + ")")
    return out


RENDER = {"openalex": openalex, "s2": s2, "arxiv": arxiv, "egdl": egdl,
          "ieee": ieee, "acm": acm, "dblp": dblp_regexes}


def iter_queries(source: str, only: set[str] | None = None):
    cfg = load_queries()
    blocks = cfg["blocks"]
    for q in cfg["queries"]:
        if source not in q.get("sources", RENDER.keys()):
            continue
        if only and q["id"] not in only:
            continue
        groups = q.get(f"{source}_groups", q["groups"])
        yield q, RENDER[source](blocks, groups)


if __name__ == "__main__":
    for src in RENDER:
        print(f"\n######## {src}")
        for q, s in iter_queries(src):
            if isinstance(s, list) and src == "ieee":
                for i, sub in enumerate(s, 1):
                    print(f"\n[{q['id']} {q['version']} part {i}/{len(s)}] {sub}")
            else:
                print(f"\n[{q['id']} {q['version']}] {s}")
