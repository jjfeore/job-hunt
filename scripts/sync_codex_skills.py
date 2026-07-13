#!/usr/bin/env python3
"""Mirror skills/ into .agents/skills/ for OpenAI Codex discovery.

Codex discovers repo skills under .agents/skills; Claude plugins keep them
under skills/. Git symlinks don't survive checkout reliably on Windows, so
this repo commits a plain-directory mirror instead. Run this after editing
anything under skills/:

    python scripts/sync_codex_skills.py          # rewrite the mirror
    python scripts/sync_codex_skills.py --check  # exit 1 if out of sync

Stdlib only; works on Windows, macOS, and Linux.
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "skills"
MIRROR = REPO_ROOT / ".agents" / "skills"


def trees_match(a: Path, b: Path) -> bool:
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return False
    return all(
        trees_match(a / sub, b / sub) for sub in cmp.common_dirs
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the mirror matches skills/ without writing anything",
    )
    args = parser.parse_args()

    if not SOURCE.is_dir():
        print(f"error: {SOURCE} not found", file=sys.stderr)
        return 2

    if args.check:
        if MIRROR.is_dir() and trees_match(SOURCE, MIRROR):
            print(".agents/skills is in sync with skills/")
            return 0
        print(
            ".agents/skills is OUT OF SYNC with skills/ — run "
            "`python scripts/sync_codex_skills.py`",
            file=sys.stderr,
        )
        return 1

    if MIRROR.exists():
        shutil.rmtree(MIRROR)
    shutil.copytree(SOURCE, MIRROR)
    skill_count = sum(1 for _ in MIRROR.rglob("SKILL.md"))
    print(f"Mirrored skills/ -> {MIRROR.relative_to(REPO_ROOT)} ({skill_count} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
