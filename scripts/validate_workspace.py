#!/usr/bin/env python3
"""Validate an Agent_Workspace structure."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_ROOT = [
    "项目索引.md",
    "00_Inbox",
    "99_Shared_Materials",
    "全局方法",
    "项目",
]

REQUIRED_PROJECT_FILES = [
    "00_项目现场.md",
    "01_判断记录.md",
    "02_完成标准.md",
    "03_素材索引.md",
    "04_复盘记录.md",
    "05_会议记录",
    "06_原始材料",
    "07_产出物",
    "08_待办.md",
    "09_接班记录.md",
]


def non_empty_file(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def parse_index_paths(index: Path) -> set[str]:
    if not index.exists():
        return set()
    paths: set[str] = set()
    for line in index.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| ") or line.startswith("| 项目名 ") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 8 and cells[7]:
            paths.add(cells[7])
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="Agent_Workspace")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    errors: list[str] = []

    if not root.exists():
        errors.append(f"missing root: {root}")
    else:
        for item in REQUIRED_ROOT:
            path = root / item
            if not path.exists():
                errors.append(f"missing root item: {item}")
        index = root / "项目索引.md"
        if index.exists() and not non_empty_file(index):
            errors.append("empty root item: 项目索引.md")

    projects_dir = root / "项目"
    if projects_dir.exists():
        indexed_paths = parse_index_paths(root / "项目索引.md")
        for project in sorted(p for p in projects_dir.iterdir() if p.is_dir()):
            rel_path = f"项目/{project.name}"
            if indexed_paths and rel_path not in indexed_paths:
                errors.append(f"{project.name}: missing from 项目索引.md")
            for item in REQUIRED_PROJECT_FILES:
                path = project / item
                if not path.exists():
                    errors.append(f"{project.name}: missing {item}")
                elif path.suffix == ".md" and not non_empty_file(path):
                    errors.append(f"{project.name}: empty {item}")
        for rel_path in indexed_paths:
            if rel_path.startswith("项目/") and not (root / rel_path).exists():
                errors.append(f"项目索引.md references missing project path: {rel_path}")

    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)

    print("VALID")
    print(root)


if __name__ == "__main__":
    main()
