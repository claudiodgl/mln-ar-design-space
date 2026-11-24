"""Full-text stage, step 1: build the 'unsure' pool, resolve each record in
OpenAlex (DOI, else title search), fill missing abstracts, and download legal
open-access PDFs (OpenAlex OA locations, arXiv). Extracted text goes to
fulltext/txt/<cid>.txt. Records without an OA copy are listed for the authors.

Usage: python -I -X utf8 scripts/fulltext_fetch.py
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import get, norm_doi, norm_title, inverted_to_text  # noqa: E402
from search_openalex import auth_params  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
PDF = ROOT / "fulltext" / "pdf"
TXT = ROOT / "fulltext" / "txt"
OA = "https://api.openalex.org/works"
FILES = [("R1", "screening.csv"), ("R2", "screening_R2.csv"),
         ("R3", "screening_R3.csv"), ("R4", "screening_R4.csv")]
UA = {"User-Agent": "Mozilla/5.0 (systematic-review full-text retrieval)"}


def eff(r):
    return (r.get("A1_decision") or r.get("final_decision") or r.get("AI_decision") or "").strip()


def resolve(r):
    doi = norm_doi(r.get("doi"))
    if doi:
        w = get(f"{OA}/doi:{doi}", auth_params())
        if w:
            return w
    t = re.sub(r"[^\w\s-]", " ", r.get("title") or "").strip()
    if len(t) < 12:
        return None
    d = get(OA, {"search": t[:200], "per_page": 3, **auth_params()})
    for w in (d or {}).get("results", []):
        if norm_title(w.get("title")) == norm_title(r.get("title")):
            return w
    return None


def pdf_urls(w):
    urls = []
    for loc in [w.get("best_oa_location")] + (w.get("locations") or []):
        if loc and loc.get("pdf_url"):
            urls.append(loc["pdf_url"])
    ids = w.get("ids") or {}
    for loc in w.get("locations") or []:
        u = (loc or {}).get("landing_page_url") or ""
        m = re.search(r"arxiv\.org/abs/([\w.\-/]+)", u)
        if m:
            urls.append(f"https://arxiv.org/pdf/{m.group(1)}")
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u); out.append(u)
    return out


def download(urls, dst):
    for u in urls:
        try:
            r = requests.get(u, headers=UA, timeout=60, allow_redirects=True)
        except requests.RequestException:
            continue
        if r.ok and r.content[:5] == b"%PDF-":
            dst.write_bytes(r.content)
            return u
    return ""


def extract(pdf, txt):
    try:
        import pymupdf
    except ImportError:  # e.g. Windows on ARM: fall back to poppler's pdftotext
        import shutil, subprocess
        if not shutil.which("pdftotext"):
            return 0
        r = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), str(txt)], capture_output=True)
        return txt.read_text(encoding="utf-8", errors="replace").count("\f") if r.returncode == 0 and txt.exists() else 0
    try:
        doc = pymupdf.open(pdf)
        txt.write_text("\n".join(p.get_text() for p in doc), encoding="utf-8")
        return len(doc)
    except Exception:
        return 0


def main():
    PDF.mkdir(parents=True, exist_ok=True); TXT.mkdir(parents=True, exist_ok=True)
    pool = []
    for rd, fn in FILES:
        for r in csv.DictReader(open(OUT / fn, encoding="utf-8-sig")):
            if eff(r) == "unsure":
                pool.append({"round": rd, "cid": r["cid"], "title": r["title"], "year": r.get("year", ""),
                             "venue": r.get("venue", ""), "doi": r.get("doi", ""),
                             "abstract": r.get("abstract", ""),
                             "screen_note": r.get("A1_note") or r.get("AI_note") or r.get("final_reason") or ""})
    out = []
    for i, p in enumerate(pool):
        w = resolve(p)
        p["openalex_id"] = (w or {}).get("id", "")
        if w and not p["doi"]:
            p["doi"] = norm_doi(w.get("doi"))
        if w and not (p["abstract"] or "").strip():
            p["abstract"] = inverted_to_text(w.get("abstract_inverted_index"))
        p["is_oa"] = str(bool(((w or {}).get("open_access") or {}).get("is_oa")))
        pdf, txt = PDF / f"{p['cid']}.pdf", TXT / f"{p['cid']}.txt"
        p["pdf_source"] = ""
        if pdf.exists():
            p["pdf_source"] = "cached"
        elif w:
            p["pdf_source"] = download(pdf_urls(w), pdf)
        p["pages"] = extract(pdf, txt) if pdf.exists() and not txt.exists() else (
            "cached" if txt.exists() else 0)
        out.append(p)
        if i % 50 == 0:
            print(i, len(pool), "pdfs so far:", sum(1 for x in out if x["pdf_source"]), flush=True)
    fields = list(out[0].keys())
    with open(OUT / "fulltext_pool.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(out)
    got = sum(1 for x in out if x["pdf_source"])
    print(f"pool {len(out)} | OA full text {got} | needs author access {len(out) - got}")


if __name__ == "__main__":
    main()
