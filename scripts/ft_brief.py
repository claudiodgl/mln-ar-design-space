"""Print an assessment brief for records with a new full text: title, the
title/abstract screening note, the beginning of the text (abstract,
introduction, contribution statement), and the figure captions.

Usage: python -I -X utf8 scripts/ft_brief.py CID [CID ...] [--chars N]
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
args = [a for a in sys.argv[1:] if not a.startswith("--")]
chars = int(next((a.split("=")[1] for a in sys.argv[1:] if a.startswith("--chars=")), 2500))
meta = {}
for fn in ("fulltext_results.csv", "screening_IEEE_new.csv"):
    p = ROOT / "output" / fn
    if p.exists():
        for r in csv.DictReader(open(p, encoding="utf-8-sig")):
            meta[r["cid"]] = r
for cid in args:
    r = meta.get(cid, {})
    t = (ROOT / "fulltext" / "txt" / f"{cid}.txt")
    txt = t.read_text(encoding="utf-8", errors="replace") if t.exists() else ""
    flat = re.sub(r"\s+", " ", txt)
    caps = re.findall(r"((?:Fig\.|Figure|FIGURE)\s*\d+[.:][^.]{10,220}\.)", flat)
    print(f"=== {cid} | {r.get('title', '')[:150]} | {r.get('year', '')} | {r.get('venue', '')[:60]}")
    print(f"NOTE: {r.get('screen_note') or r.get('AI_note', '')}")
    print(f"TEXT ({len(flat)} chars): {flat[:chars]}")
    print("CAPTIONS: " + " || ".join(c[:200] for c in caps[:8]))
    print()
