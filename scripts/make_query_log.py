"""Generate query_log.md from config/query_log_narrative.md + raw/run_log.jsonl.

Every executed (source, query, version) is listed once with the hit count the
source reported, the number of records retrieved, and the benchmark recall
of that raw file (if the file is still on disk), followed by the exact query
strings of every version.
Usage: python -I scripts/make_query_log.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from benchmark import match  # noqa: E402
from common import CONFIG, RAW, ROOT, read_jsonl  # noqa: E402


def main():
    runs, seen = [], {}
    for l in open(RAW / "run_log.jsonl", encoding="utf-8"):
        d = json.loads(l)
        if d["source"].startswith("snowball"):
            continue
        k = (d["source"], d["query_id"], d["version"], d["note"] == "count only")
        if k in seen:
            continue
        seen[k] = d
        runs.append(d)
    lines = [(CONFIG / "query_log_narrative.md").read_text(encoding="utf-8"), "",
             "## Run table (generated from raw/run_log.jsonl)", "",
             "| date | source | query | version | hits reported | retrieved | benchmark recall of this run | matched |",
             "|---|---|---|---|---:|---:|---:|---|"]
    for d in runs:
        f = RAW / d["source"] / f"{d['query_id']}_{d['version']}.jsonl"
        if d["note"] == "count only":
            rec, got = "(count only)", ""
        elif f.exists():
            m = sorted({x for r in read_jsonl(f) if (x := match(r))})
            rec, got = f"{len(m)}/24", " ".join(m)
        else:
            rec, got = "(raw file superseded, see narrative)", ""
        lines.append(f"| {d['date']} | {d['source']} | {d['query_id']} | {d['version']} | "
                     f"{d['hits_reported'] if d['hits_reported'] is not None else ''} | "
                     f"{d['hits_retrieved'] if d['note'] != 'count only' else ''} | {rec} | {got} |")
    lines += ["", "## Exact query strings per executed version", ""]
    done = set()
    for d in runs:
        k = (d["source"], d["query_id"], d["version"])
        if k in done:
            continue
        done.add(k)
        lines += [f"**{d['source']} {d['query_id']} {d['version']}**", "", "```", d["query"], "```", ""]
    (ROOT / "query_log.md").write_text("\n".join(lines), encoding="utf-8")
    print("wrote", ROOT / "query_log.md", len(runs), "runs")


if __name__ == "__main__":
    main()
