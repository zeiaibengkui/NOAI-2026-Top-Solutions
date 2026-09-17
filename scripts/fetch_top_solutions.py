#!/usr/bin/env python3
"""Download the top-N NOAI 2026 submissions listed in the notebook index.

Reads ``NOAI2026原始notebook链接.csv`` and pulls each task's highest scoring
notebooks (ranked by ``A榜分数``, the public leaderboard) into
``solutions/<task-slug>/rankNN_<original name>.ipynb``.

Existing files are never overwritten, so locally annotated copies of a
notebook survive a re-run. Use ``--force`` to redownload them.

Examples
--------
    python3 scripts/fetch_top_solutions.py --dry-run
    python3 scripts/fetch_top_solutions.py --top 5
    python3 scripts/fetch_top_solutions.py --task task4-maze --top 3
"""

from __future__ import annotations

import argparse
import csv
import json
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_CSV = REPO_ROOT / "NOAI2026原始notebook链接.csv"
SOLUTIONS_DIR = REPO_ROOT / "solutions"

TASK_SLUGS = {
    "NOAI 2026 知乎场景下的用户意图识别": "task1-intent-recognition",
    "NOAI 2026 基于NVIDIA Isaac Sim的具身智能Sim2Real轨迹预测问题": "task2-isaac-sim2real",
    "NOAI 2026 积·和": "task3-sum-and-product",
    "NOAI 2026 迷宫信息预测": "task4-maze",
}


def as_score(value: str) -> int:
    """A榜/B榜 scores are integers, but be forgiving about blanks."""
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return -1


def quote_url(url: str) -> str:
    """Percent-encode the path so links with Chinese filenames work."""
    parts = urllib.parse.urlsplit(url.strip())
    return urllib.parse.urlunsplit(
        (parts.scheme, parts.netloc, urllib.parse.quote(parts.path), parts.query, parts.fragment)
    )


def fetch(url: str, timeout: int = 30) -> bytes:
    request = urllib.request.Request(quote_url(url), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def load_rankings(top: int) -> dict[str, list[dict]]:
    with INDEX_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    rankings: dict[str, list[dict]] = {}
    for task in TASK_SLUGS:
        task_rows = [row for row in rows if row["题目名称"] == task]
        task_rows.sort(key=lambda row: -as_score(row["A榜分数"]))
        rankings[task] = task_rows[:top]
    return rankings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--top", type=int, default=5, help="how many notebooks per task (default: 5)")
    parser.add_argument("--task", action="append", choices=sorted(TASK_SLUGS.values()), help="limit to these task slugs")
    parser.add_argument("--dry-run", action="store_true", help="print the plan without downloading")
    parser.add_argument("--force", action="store_true", help="overwrite files that already exist")
    args = parser.parse_args()

    rankings = load_rankings(args.top)
    downloaded = skipped = failed = 0

    for task, rows in rankings.items():
        slug = TASK_SLUGS[task]
        if args.task and slug not in args.task:
            continue
        target_dir = SOLUTIONS_DIR / slug
        print(f"\n{slug}  (top {len(rows)} of {task})")

        for rank, row in enumerate(rows, start=1):
            name = urllib.parse.unquote(row["下载链接"].rsplit("/", 1)[-1]) or f"rank{rank:02d}.ipynb"
            path = target_dir / f"rank{rank:02d}_{name}"
            label = f"  rank{rank:02d} A={row['A榜分数']:>5s} B={row['B榜分数']:>5s} {name[:40]}"

            if path.exists() and not args.force:
                print(f"{label}  [kept]")
                skipped += 1
                continue
            if args.dry_run:
                print(f"{label}  [would fetch]")
                continue

            try:
                data = fetch(row["下载链接"])
                json.loads(data)  # a real notebook, not an error page
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
                print(f"{label}  [ok {len(data)} bytes]")
                downloaded += 1
            except Exception as exc:  # noqa: BLE001 - report and keep going
                print(f"{label}  [FAILED {type(exc).__name__}: {exc}]")
                failed += 1

    if not args.dry_run:
        print(f"\ndownloaded={downloaded} kept={skipped} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
