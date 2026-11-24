"""Shared helpers for the MLN-in-AR literature search.

* one HTTP session with a generic User-Agent (no personal data);
* optional contact e-mail for OpenAlex/Crossref "polite pool" read from the
  MAILTO env var (default: empty -> not sent);
* optional API keys read from env vars (OPENALEX_API_KEY, S2_API_KEY,
  IEEE_API_KEY); nothing is hard-coded;
* per-host minimum interval between requests + exponential back-off on 429/5xx;
* an on-disk response cache (raw/cache/) so that re-running a script does not
  re-query the APIs and the exact responses used for the paper are archived;
* record normalisation (DOI, arXiv id, title) used for de-duplication and
  benchmark matching.
"""
from __future__ import annotations

import csv
import datetime as _dt
import hashlib
import html
import json
import os
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import urlencode, urlparse

import requests

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
CACHE = RAW / "cache"
OUT = ROOT / "output"
CONFIG = ROOT / "config"
for _p in (RAW, CACHE, OUT):
    _p.mkdir(parents=True, exist_ok=True)

USER_AGENT = "mln-ar-litsearch/1.0 (reproducible literature search script; python-requests)"
MAILTO = os.environ.get("MAILTO", "").strip()  # optional; default empty

# minimum seconds between two requests to the same host
MIN_INTERVAL = {
    "api.openalex.org": 0.15,
    "api.semanticscholar.org": 1.1 if not os.environ.get("S2_API_KEY") else 0.35,
    "export.arxiv.org": 3.1,          # arXiv API terms: 1 request / 3 s
    "api.crossref.org": 0.2,
    "sparql.dblp.org": 1.0,
    "diglib.eg.org": 1.0,
    "ieeexploreapi.ieee.org": 0.5,
}
_last: dict[str, float] = {}

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})

TODAY = _dt.date.today().isoformat()


def _cache_path(url: str, body: str | None) -> Path:
    h = hashlib.sha256((url + "\n" + (body or "")).encode()).hexdigest()[:24]
    host = urlparse(url).netloc.replace(":", "_")
    d = CACHE / host
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{h}.json"


def _strip_secrets(url: str) -> str:
    return re.sub(r"(api_key|apikey)=[^&]+", r"\1=***", url)


def get(url: str, params: dict | None = None, *, accept: str = "json",
        headers: dict | None = None, use_cache: bool = True, max_tries: int = 6):
    """GET with cache, rate limit and back-off. Returns parsed JSON or text."""
    full = url + ("?" + urlencode(params, doseq=True) if params else "")
    key_url = _strip_secrets(full)
    cp = _cache_path(key_url, None)
    if use_cache and cp.exists():
        rec = json.loads(cp.read_text(encoding="utf-8"))
        return rec["body"]
    host = urlparse(url).netloc
    delay = 2.0
    for attempt in range(max_tries):
        wait = MIN_INTERVAL.get(host, 0.5) - (time.time() - _last.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        _last[host] = time.time()
        try:
            r = SESSION.get(full, headers=headers, timeout=60)
        except requests.RequestException as e:  # network hiccup
            print(f"  ! {host}: {e}; retry in {delay:.0f}s", file=sys.stderr)
            time.sleep(delay); delay *= 2; continue
        if r.status_code in (429, 500, 502, 503, 504):
            ra = r.headers.get("Retry-After")
            w = float(ra) if ra and ra.isdigit() else delay
            print(f"  ! {host}: HTTP {r.status_code}; retry in {w:.0f}s", file=sys.stderr)
            time.sleep(w); delay *= 2; continue
        if r.status_code == 404:
            body = None
        else:
            r.raise_for_status()
            body = r.json() if accept == "json" else r.text
        cp.write_text(json.dumps({"url": key_url, "retrieved": TODAY,
                                  "status": r.status_code, "body": body}),
                      encoding="utf-8")
        return body
    raise RuntimeError(f"giving up on {key_url}")


# ---------------------------------------------------------------- normalise
def norm_doi(d: str | None) -> str:
    if not d:
        return ""
    d = d.strip().lower()
    d = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", d)
    d = d.removeprefix("doi:")
    return d


def arxiv_from_doi(doi: str) -> str:
    m = re.match(r"10\.48550/arxiv\.(.+)", doi or "")
    return m.group(1) if m else ""


def norm_arxiv(a: str | None) -> str:
    if not a:
        return ""
    a = a.strip().lower()
    a = re.sub(r"^(https?://)?arxiv\.org/(abs|pdf)/", "", a)
    a = a.removeprefix("arxiv:")
    return re.sub(r"v\d+$", "", a)


def norm_title(t: str | None) -> str:
    if not t:
        return ""
    t = html.unescape(t)
    t = re.sub(r"<[^>]+>", " ", t)  # JATS / html tags
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower().replace("visualisation", "visualization")
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def inverted_to_text(inv: dict | None) -> str:
    if not inv:
        return ""
    pos = []
    for w, idx in inv.items():
        for i in idx:
            pos.append((i, w))
    return " ".join(w for _, w in sorted(pos))


# ---------------------------------------------------------------- records
FIELDS = ["source", "query_id", "query_version", "snowball_round", "snowball_seed",
          "snowball_direction", "title", "year", "venue", "doi", "arxiv",
          "openalex_id", "s2_id", "dblp_key", "type", "authors", "abstract",
          "retrieved"]


def record(**kw) -> dict:
    r = {k: "" for k in FIELDS}
    r.update({k: ("" if v is None else v) for k, v in kw.items()})
    r["doi"] = norm_doi(r["doi"])
    if not r["arxiv"]:
        r["arxiv"] = arxiv_from_doi(r["doi"])
    r["arxiv"] = norm_arxiv(r["arxiv"])
    r["retrieved"] = r["retrieved"] or TODAY
    return r


def write_jsonl(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def write_csv(path: Path, rows: list[dict], fields: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_queries() -> dict:
    return json.loads((CONFIG / "queries.json").read_text(encoding="utf-8"))


def log_run(source: str, qid: str, ver: str, query: str, n_reported, n_got: int, note: str = ""):
    """Append one line to raw/run_log.jsonl (machine log behind query_log.md)."""
    p = RAW / "run_log.jsonl"
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps({"date": TODAY, "source": source, "query_id": qid,
                            "version": ver, "query": query,
                            "hits_reported": n_reported, "hits_retrieved": n_got,
                            "note": note}, ensure_ascii=False) + "\n")
