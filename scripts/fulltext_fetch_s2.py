"""Full-text stage, step 2: for records still lacking full text, query Semantic
Scholar (DOI or title match) for an abstract and an open-access PDF, and arXiv
(exact title match) for a preprint. Writes fulltext/txt/<cid>.txt for new PDFs
and output/fulltext_s2_enrich.csv (cid, abstract_new, pdf_source).

Usage: python -I -X utf8 scripts/fulltext_fetch_s2.py
"""
from __future__ import annotations

import csv
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import get, norm_doi, norm_title  # noqa: E402
from fulltext_fetch import download, extract, PDF, TXT, OUT  # noqa: E402

S2 = "https://api.semanticscholar.org/graph/v1/paper"
F = "title,abstract,openAccessPdf,externalIds"


def s2_lookup(r):
    doi = norm_doi(r.get("doi"))
    if doi:
        w = get(f"{S2}/DOI:{doi}", {"fields": F})
        if w:
            return w
    t = re.sub(r"[^\w\s-]", " ", r.get("title") or "").strip()
    if len(t) < 12:
        return None
    d = get(f"{S2}/search/match", {"query": t[:250], "fields": F})
    for w in (d or {}).get("data", []) or []:
        if norm_title(w.get("title")) == norm_title(r.get("title")):
            return w
    return None


def arxiv_lookup(title):
    t = re.sub(r"[^\w\s]", " ", title or "").strip()
    if len(t) < 15:
        return ""
    x = get("http://export.arxiv.org/api/query",
            {"search_query": 'ti:"%s"' % t[:200], "max_results": 3}, accept="text")
    if not x:
        return ""
    ns = {"a": "http://www.w3.org/2005/Atom"}
    try:
        root = ET.fromstring(x)
    except ET.ParseError:
        return ""
    for e in root.findall("a:entry", ns):
        if norm_title(e.findtext("a:title", "", ns)) == norm_title(title):
            aid = e.findtext("a:id", "", ns).rsplit("/abs/", 1)[-1]
            return f"https://arxiv.org/pdf/{aid}"
    return ""


def main():
    rows = [r for r in csv.DictReader(open(OUT / "fulltext_results.csv", encoding="utf-8-sig"))
            if r["ft_decision"] == "needs_fulltext"]
    out = []
    for i, r in enumerate(rows):
        cid = r["cid"]
        pdf, txt = PDF / f"{cid}.pdf", TXT / f"{cid}.txt"
        rec = {"cid": cid, "abstract_new": "", "pdf_source": ""}
        w = s2_lookup(r)
        if w and not (r.get("abstract") or "").strip() and w.get("abstract"):
            rec["abstract_new"] = w["abstract"]
        urls = []
        if w and (w.get("openAccessPdf") or {}).get("url"):
            urls.append(w["openAccessPdf"]["url"])
        ax = (w or {}).get("externalIds", {}) or {}
        if ax.get("ArXiv"):
            urls.append(f"https://arxiv.org/pdf/{ax['ArXiv']}")
        if not pdf.exists():
            if not urls:
                u = arxiv_lookup(r["title"])
                if u:
                    urls.append(u)
            if urls:
                rec["pdf_source"] = download(urls, pdf)
        if pdf.exists() and not txt.exists():
            extract(pdf, txt)
        if pdf.exists() and not rec["pdf_source"]:
            rec["pdf_source"] = "cached"
        out.append(rec)
        if i % 50 == 0:
            print(i, len(rows), "new pdfs:", sum(1 for x in out if x["pdf_source"]),
                  "new abstracts:", sum(1 for x in out if x["abstract_new"]), flush=True)
    with open(OUT / "fulltext_s2_enrich.csv", "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.DictWriter(f, fieldnames=["cid", "abstract_new", "pdf_source"]); wr.writeheader(); wr.writerows(out)
    print(f"checked {len(out)} | new PDFs {sum(1 for x in out if x['pdf_source'])} | "
          f"new abstracts {sum(1 for x in out if x['abstract_new'])}")


if __name__ == "__main__":
    main()
