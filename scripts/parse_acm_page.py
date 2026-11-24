"""Parse ACM DL search-result pages copied as plain text (no premium export).

Usage: python -I scripts/parse_acm_page.py exports/acm/pages/Q1_v4_p01.txt [more pages...] -o exports/acm/Q1_v4_results.csv
Each record on the page has: type line, date line, [Published By ACM], title line,
author line ("Author Picture..." or plain names), venue line containing the DOI URL.
The reported total ("N Results for:") is printed so it can be logged.
"""
import argparse, csv, re, sys

MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"

def parse(text):
    lines = [l.strip() for l in text.splitlines()]
    m = re.search(r"([\d,]+) Results for:", text)
    reported = int(m.group(1).replace(",", "")) if m else None
    recs = []
    for i, l in enumerate(lines):
        dm = re.search(r"https://doi\.org/(\S+)", l)
        date_i = None
        if dm or (i > 2 and re.match(rf"^({MONTHS}) \d{{4}}$", lines[i - 4] if i >= 4 else "") and "Pages" in l):
            pass
        if not dm:
            continue
        doi = dm.group(1).rstrip(".")
        venue = l[:dm.start()].strip()
        # walk back: author line, title line, optional "Published By ACM", date line
        j = i - 1
        while j >= 0 and not lines[j]: j -= 1
        author_line = lines[j]; j -= 1
        while j >= 0 and not lines[j]: j -= 1
        title = lines[j]; j -= 1
        year = ""
        for k in range(j, max(j - 4, -1), -1):
            ym = re.match(rf"^({MONTHS}) (\d{{4}})$", lines[k])
            if ym: year = ym.group(2); break
        yv = re.search(r"\b(19|20)\d{2}\b", venue)
        recs.append(dict(title=title, doi=doi, year=year, venue=re.sub(r"Pages? .*$|Article No\..*$", "", venue).strip()))
    return reported, recs

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("pages", nargs="+"); ap.add_argument("-o", required=True)
    a = ap.parse_args()
    allrecs, rep = [], None
    for p in a.pages:
        r, recs = parse(open(p, encoding="utf8").read()); rep = rep or r; allrecs += recs
    seen = set(); out = []
    for r in allrecs:
        if r["doi"] not in seen: seen.add(r["doi"]); out.append(r)
    with open(a.o, "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=["title", "doi", "year", "venue"]); w.writeheader(); w.writerows(out)
    print(f"reported={rep} parsed={len(out)} -> {a.o}")
    for r in out: print(" ", r["year"], r["doi"], "|", r["title"][:80])
