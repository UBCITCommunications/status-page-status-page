#!/usr/bin/env python3
"""Bring collected status page data into this repo's data/ folder.

The collector (the separate status-page-status-page-data repo) saves every version of the
public feeds. This script takes what the review needs from a local clone of it:

  1. The newest summary.json capture  -> data/snapshots/summary-<date>.json  (raw copy)
     and the newest capture from an earlier day, so the page has something to compare with.
  2. Every incidents.json capture     -> data/incidents/incidents-merged.json
     One file holding the newest version of every incident ever seen. Statuspage only lists
     the 50 most recent, so merging captures is how the history grows past 50.

Then run scripts/embed-snapshots.py to put the data into index.html.

    python3 scripts/import-collected.py ../status-page-status-page-data
    python3 scripts/embed-snapshots.py

Standard library only.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def captures(src, feed):
    """Saved captures of one feed, oldest first (file names sort by capture time)."""
    return sorted((src / "data" / feed).glob("*/*/*.json"))


def main(args):
    if len(args) != 1:
        sys.exit(__doc__)
    src = Path(args[0]).expanduser().resolve()
    if not (src / "data").is_dir():
        sys.exit(f"{src} doesn't look like the data repo (no data/ folder).")

    # 1. snapshots: newest, plus the newest from an earlier day
    sums = captures(src, "summary")
    picked = []
    if sums:
        picked.append(sums[-1])
        day = sums[-1].name.split("-")[1][:8]
        earlier = [f for f in sums if f.name.split("-")[1][:8] < day]
        if earlier:
            picked.append(earlier[-1])
    for f in picked:
        doc = json.loads(f.read_bytes())
        date = (doc.get("page") or {}).get("updated_at", "")[:10] or f.name.split("-")[1][:8]
        out = ROOT / "data" / "snapshots" / f"summary-{date}.json"
        shutil.copyfile(f, out)
        print(f"snapshot   {f.relative_to(src)} -> {out.relative_to(ROOT)}")

    # 2. merged incident history: newest version of each incident across every capture,
    #    plus any incidents.json already kept in this repo
    incs = [p for p in sorted((ROOT / "data" / "incidents").glob("incidents-*.json")) if p.name != "incidents-merged.json"]
    incs += captures(src, "incidents")
    if not incs:
        print("no incident captures found"); return
    newest, page, first, last = {}, None, None, None
    for f in incs:
        doc = json.loads(f.read_bytes())
        when = (doc.get("page") or {}).get("updated_at", "")
        for i in doc.get("incidents", []):
            seen = newest.get(i["id"])
            if not seen or i.get("updated_at", "") >= seen.get("updated_at", ""):
                newest[i["id"]] = i
        if not last or when >= last:
            last, page = when, doc.get("page")
        if not first or when < first:
            first = when
    merged = {
        "page": page,
        "incidents": sorted(newest.values(), key=lambda i: i.get("created_at", ""), reverse=True),
        "_merged": {"note": "Built by scripts/import-collected.py: the newest version of every incident across all captures. Not a file Statuspage serves.",
                    "captures": len(incs), "first_capture": first, "last_capture": last},
    }
    out = ROOT / "data" / "incidents" / "incidents-merged.json"
    out.write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"history    {len(incs)} captures -> {len(newest)} incidents -> {out.relative_to(ROOT)}")
    print("next: python3 scripts/embed-snapshots.py")


if __name__ == "__main__":
    main(sys.argv[1:])
