"""Build supplement.bib: copy the entries the supplement cites from the paper's
bib, and create entries for additional works from OpenAlex metadata (by DOI).

Usage: python -I -X utf8 scripts/build_supplement_bib.py <paper.bib> <out.bib>
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import get  # noqa: E402
from search_openalex import auth_params  # noqa: E402

FROM_PAPER = """MuxViz muxViz_book Arena3Dweb MultiNets Py3plex pymnet 7465267 9382912 Graphon NodeTrix DynTrix
matrix_cube 7390081 Pirch2021 GAV_VR networks_VR 10298000 Feyer2026layers Lee2026voice Belcher2003 8636208
James2020personal Lee2022 Li2022painters Schwajda2023 Takahira2025tangiblenet Liu2026semantic HoloGraphs 70140
state_of_the_art McGee2021 joos2025visualnetworkanalysisimmersive 10296039 KleinSedlmairSchreiber Kivela2014
14430 Cordeil2017spatio Shin2024situated 10297565 Nickerson2013 Butscher2018 Bach2018hologram""".split()

# key -> DOI for works that are not in the paper's bib
NEW = {
    "Page2021prisma": "10.1136/bmj.n71",
    "Wohlin2014snowballing": "10.1145/2601248.2601268",
    "Drochtert2015magiclens": "10.1145/2818427.2818465",
    "Kyaw2026mindmap": "10.1145/3799825.3818764",
    "Bhattacharya2026nodebots": "10.1145/3830397.3842445",
    "McGuffin2023pathtracing": "10.1109/tvcg.2023.3238989",
    "Drogemuller2021haptic": "10.1145/3411764.3445704",
    "Zhao2017egocentric": "10.1145/3139295.3139309",
    "Renoust2015detangler": "10.1111/cgf.12644",
    "Nehoray2026mira": "10.48550/arxiv.2605.09597",
    "Meidiana2015multistory": "10.1109/pacificvis.2015.7156359",
    "Durant2024hybrid": "10.2312/evp.20241084",
    "Tanhaei2023datar": "10.1145/3573381.3597222",
    "Manshaei2019bionets": "10.1145/3331156",
    "Arif2016sparse": "10.1145/2839462.2839500",
    "Bressa2022situation": "10.1109/tvcg.2021.3114835",
    "Schoettler2021geo": "10.1111/cgf.14198",
    "Zollmann2021ar": "10.1109/tvcg.2020.2986247",
    "Miller2024noneuclidean": "10.1111/cgf.15113",
    "Uhl2023tangiblexr": "10.1145/3569009.3571843",
}


def tex(s: str) -> str:
    s = s or ""
    rep = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_"}
    for a, b in rep.items():
        s = s.replace(a, b)
    out = []
    for ch in s:
        if ord(ch) < 128:
            out.append(ch)
            continue
        d = unicodedata.normalize("NFD", ch)
        base, marks = d[0], d[1:]
        acc = {"́": "'", "̀": "`", "̈": '"', "̂": "^", "̃": "~", "̌": "v", "̧": "c"}
        if marks and marks[0] in acc and ord(base) < 128:
            a = acc[marks[0]]
            out.append("{\\%s{%s}}" % (a, base) if a.isalpha() else "{\\%s%s}" % (a, base))
        else:
            out.append({"–": "--", "—": "---", "‘": "`", "’": "'", "“": "``", "”": "''", "‐": "-", "ß": "{\\ss}", "ø": "{\\o}"}.get(ch, ch))
    return "".join(out)


def entry_from_openalex(key: str, doi: str) -> str:
    w = get(f"https://api.openalex.org/works/doi:{doi}", auth_params())
    if not w:
        return f"% {key}: DOI {doi} not found in OpenAlex\n"
    authors = " and ".join(tex(a["author"]["display_name"]) for a in w.get("authorships", []))
    src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
    b = w.get("biblio") or {}
    typ = w.get("type") or ""
    kind = "article" if typ == "article" and src and "proceedings" not in src.lower() and "conference" not in src.lower() else "inproceedings"
    if "arxiv" in doi.lower():
        kind = "misc"
    f = [f"  author = {{{authors}}}", f"  title = {{{{{tex(w.get('title'))}}}}}", f"  year = {{{w.get('publication_year')}}}"]
    if kind == "article":
        f.append(f"  journal = {{{tex(src)}}}")
        if b.get("volume"): f.append(f"  volume = {{{b['volume']}}}")
        if b.get("issue"): f.append(f"  number = {{{b['issue']}}}")
    elif kind == "inproceedings":
        f.append(f"  booktitle = {{{tex(src)}}}")
    else:
        f.append("  howpublished = {arXiv preprint}")
    if b.get("first_page"):
        f.append(f"  pages = {{{b['first_page']}" + (f"--{b['last_page']}" if b.get("last_page") else "") + "}")
    f.append(f"  doi = {{{doi}}}")
    return f"@{kind}{{{key},\n" + ",\n".join(f) + "\n}\n"


def main():
    paper_bib, out = Path(sys.argv[1]), Path(sys.argv[2])
    src = paper_bib.read_text(encoding="utf-8")
    ents = {m.group(1).strip(): m.group(0) for m in re.finditer(r"@\w+\{([^,]+),.*?\n\}", src, re.S)}
    parts, missing = [], []
    for k in FROM_PAPER:
        if k in ents:
            parts.append(ents[k] + "\n")
        else:
            missing.append(k)
    parts.append("% ---- additional works (metadata from OpenAlex; check before publication)\n")
    for k, d in NEW.items():
        parts.append(entry_from_openalex(k, d))
    out.write_text("\n".join(parts), encoding="utf-8")
    print("written", out, "| missing from paper bib:", missing)


if __name__ == "__main__":
    main()
