#!/usr/bin/env python3
"""Initialize an Agent_Workspace directory."""

from __future__ import annotations

import argparse
from pathlib import Path


PROJECT_INDEX = """# 项目索引

| 项目名 | 别名/关键词 | 状态 | 当前阶段 | 当前唯一下一步 | 参与人/对象 | 最近更新 | 项目路径 |
| --- | --- | --- | --- | --- | --- | --- | --- |
"""

GLOBAL_METHOD = """# {name}

## 适用场景

## 不适用场景

## 输入

## 输出

## 操作步骤

## 完成标准

## 失败边界

## 已复用项目
"""


def write_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="Agent_Workspace")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    (root / "00_Inbox").mkdir(parents=True, exist_ok=True)
    (root / "99_Shared_Materials").mkdir(parents=True, exist_ok=True)
    (root / "项目").mkdir(parents=True, exist_ok=True)
    (root / "全局方法").mkdir(parents=True, exist_ok=True)

    write_if_missing(root / "项目索引.md", PROJECT_INDEX)

    for name in ["写作方法", "选题判断", "审稿标准", "工具使用规则"]:
        write_if_missing(root / "全局方法" / f"{name}.md", GLOBAL_METHOD.format(name=name))

    print(root)


if __name__ == "__main__":
    main()

