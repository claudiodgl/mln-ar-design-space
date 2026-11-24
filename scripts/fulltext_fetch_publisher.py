"""Full-text stage, step 3: for records still lacking a full text, try the
publisher's own open copy via the DOI:
  * ACM Digital Library (open access since January 2026): dl.acm.org/doi/pdf/<doi>
  * any publisher: resolve https://doi.org/<doi> and follow the landing page's
    <meta name="citation_pdf_url">; accepted only if the response is a PDF.
Nothing is circumvented: paywalled or bot-protected copies simply fail.

Input : output/fulltext_results.csv (ft_decision == needs_fulltext) and
        output/screening_IEEE_new.csv (AI_decision == unsure)
Output: fulltext/pdf/<cid>.pdf, fulltext/txt/<cid>.txt,
        output/fulltext_publisher_fetch.csv (cid, doi, status, url)
Usage : python -I -X utf8 scripts/fulltext_fetch_publisher.py
"""
from __future__ import annotations

import csv
import html
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import norm_doi  # noqa: E402
from fulltext_fetch import PDF, TXT, OUT, extract  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120 Safari/537.36 (systematic-review full-text retrieval)",
      "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.8"}
S = requests.Session(); S.headers.update(UA)
_last: dict[str, float] = {}


PLAIN = {"User-Agent": "mln-ar-litsearch/1.0 (systematic-review full-text retrieval)", "Accept": "application/pdf"}


def fetch(url: str, headers: dict | None = None):
    host = urlparse(url).netloc
    w = 1.0 - (time.time() - _last.get(host, 0))
    if w > 0:
        time.sleep(w)
    _last[host] = time.time()
    try:
        return S.get(url, timeout=240, allow_redirects=True, headers=headers)
    except requests.RequestException:
        return None


def is_pdf(r) -> bool:
    return r is not None and r.ok and r.content[:5] == b"%PDF-"


def try_doi(doi: str):
    cands = []
    if doi.startswith("10.1145/"):
        cands.append(f"https://dl.acm.org/doi/pdf/{doi}")
    if doi.startswith("10.1007/"):   # Springer serves the PDF only where it is free to read
        cands.append(f"https://link.springer.com/content/pdf/{doi}.pdf")
    for u in cands:
        r = fetch(u, PLAIN if "springer" in u else None)   # Springer serves an HTML viewer to browsers
        if is_pdf(r):
            return "ok", u, r.content
    r = fetch(f"https://doi.org/{doi}")
    if r is None:
        return "error", "", None
    if is_pdf(r):
        return "ok", r.url, r.content
    if not r.ok:
        return f"http {r.status_code}", r.url, None
    m = re.search(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', r.text, re.I) \
        or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url', r.text, re.I)
    if not m:
        return "no pdf link", r.url, None
    u = urljoin(r.url, html.unescape(m.group(1)))
    r2 = fetch(u)
    if is_pdf(r2):
        return "ok", u, r2.content
    return "pdf link not open", u, None


def main():
    pool = [r for r in csv.DictReader(open(OUT / "fulltext_results.csv", encoding="utf-8-sig"))
            if r["ft_decision"] == "needs_fulltext"]
    ieee = OUT / "screening_IEEE_new.csv"
    if ieee.exists():
        pool += [r for r in csv.DictReader(open(ieee, encoding="utf-8-sig")) if r.get("AI_decision") == "unsure"]
    prefix = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--prefix=")), "")
    if prefix:   # re-run for one publisher only; results are merged into the existing log
        pool = [r for r in pool if norm_doi(r.get("doi")).startswith(prefix)]
    out = []
    for i, r in enumerate(pool):
        cid, doi = r["cid"], norm_doi(r.get("doi"))
        pdf, txt = PDF / f"{cid}.pdf", TXT / f"{cid}.txt"
        if pdf.exists():
            status, url = "already", ""
        elif not doi or doi.startswith("10.48550/"):
            status, url = "no doi", ""
        else:
            status, url, content = try_doi(doi)
            if content:
                pdf.write_bytes(content)
        if pdf.exists() and not txt.exists():
            extract(pdf, txt)
        out.append({"cid": cid, "doi": doi, "status": status, "url": url})
        if i % 25 == 0:
            print(i, len(pool), "new PDFs:", sum(x["status"] == "ok" for x in out), flush=True)
    log = OUT / "fulltext_publisher_fetch.csv"
    if prefix and log.exists():
        new = {x["cid"]: x for x in out}
        old = list(csv.DictReader(open(log, encoding="utf-8-sig")))
        out = [new.pop(x["cid"], x) for x in old] + list(new.values())
    with open(log, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["cid", "doi", "status", "url"]); w.writeheader(); w.writerows(out)
    from collections import Counter
    print(Counter(x["status"] for x in out))


if __name__ == "__main__":
    main()
