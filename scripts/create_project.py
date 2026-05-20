#!/usr/bin/env python3
"""Create a project workspace with standard files."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


PROJECT_INDEX_HEADER = "# 项目索引\n\n| 项目名 | 别名/关键词 | 状态 | 当前阶段 | 当前唯一下一步 | 参与人/对象 | 最近更新 | 项目路径 |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n"

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


def safe_name(name: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|]+", "-", name).strip()
    cleaned = re.sub(r"\s+", "-", cleaned)
    if cleaned in {"", ".", ".."}:
        return "untitled-project"
    return cleaned


def table_cell(value: str) -> str:
    cleaned = re.sub(r"[\r\n\t]+", " ", value).strip()
    cleaned = cleaned.replace("|", "/")
    return cleaned


def write_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def init_root(root: Path) -> None:
    (root / "00_Inbox").mkdir(parents=True, exist_ok=True)
    (root / "99_Shared_Materials").mkdir(parents=True, exist_ok=True)
    (root / "项目").mkdir(parents=True, exist_ok=True)
    (root / "全局方法").mkdir(parents=True, exist_ok=True)
    write_if_missing(root / "项目索引.md", PROJECT_INDEX_HEADER)
    for name in ["写作方法", "选题判断", "审稿标准", "工具使用规则"]:
        write_if_missing(root / "全局方法" / f"{name}.md", GLOBAL_METHOD.format(name=name))


def index_has_slug_collision(index_text: str, slug: str, project_name: str) -> bool:
    target = f"| 项目/{slug} |"
    for line in index_text.splitlines():
        if not line.startswith("| ") or line.startswith("| 项目名 ") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 8 and cells[7] == f"项目/{slug}" and cells[0] != project_name:
            return True
    return False


def project_files(project_name: str) -> dict[str, str]:
    today = date.today().isoformat()
    return {
        "00_项目现场.md": f"""# 项目现场

## 项目一句话

{project_name}

## 项目目标

## 当前阶段

## 最近进展

## 上次停在哪里

## 当前阻塞

## 下一步只做什么

## 关键参与者/对象

## 重要路径/链接

## 当前风险

## 最后更新

{today}
""",
        "01_判断记录.md": """# 判断记录

## 已确认判断

| 确认日期 | 判断 | 依据 | 影响 | 复核日期 | 失效条件 | 是否仍有效 |
| --- | --- | --- | --- | --- | --- | --- |

## 已否定方向

| 日期 | 否定方向 | 为什么不行 | 后续避免方式 | 复核日期 | 是否仍有效 |
| --- | --- | --- | --- | --- | --- |

## 待验证判断

| 日期 | 假设 | 需要什么证据 | 下一步 | 状态 |
| --- | --- | --- | --- | --- |
""",
        "02_完成标准.md": """# 完成标准

## 这个项目最终交付什么

## 什么叫做完

## 什么只是看起来完整

## 质量底线

## 验收方式

## 失败信号
""",
        "03_素材索引.md": """# 素材索引

| 入库日期 | 事件日期 | 素材ID | 素材名 | 类型 | 来源URL/路径 | 内容hash | 版本 | 归属问题 | 可用价值 | 核心证据 | 敏感级别 | 有效期 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
""",
        "04_复盘记录.md": """# 复盘记录

## 复盘条目
""",
        "08_待办.md": """# 待办

| 优先级 | 任务 | 所属阶段 | 截止时间 | 状态 | 备注 |
| --- | --- | --- | --- | --- | --- |
""",
        "09_接班记录.md": f"""# 接班记录

## 上次任务

## 上次停在哪里

## 为什么停

## 当前唯一下一步

## 本次接班必须继承的判断

## 本次不能再走的方向

## 本次启动建议

## 最后更新

{today}
""",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="Agent_Workspace")
    parser.add_argument("--name", required=True)
    parser.add_argument("--keywords", default="")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    project_slug = safe_name(args.name)
    project_dir = root / "项目" / project_slug

    init_root(root)

    index = root / "项目索引.md"
    text = index.read_text(encoding="utf-8")
    if index_has_slug_collision(text, project_slug, args.name):
        print(f"ERROR: project slug collision for '{project_slug}'. Choose a different project name.", file=sys.stderr)
        sys.exit(2)

    for subdir in ["05_会议记录", "06_原始材料", "07_产出物"]:
        (project_dir / subdir).mkdir(parents=True, exist_ok=True)

    for filename, content in project_files(args.name).items():
        write_if_missing(project_dir / filename, content)

    project_cell = table_cell(args.name)
    keywords_cell = table_cell(args.keywords)
    row_marker = f"| {project_cell} |"
    if row_marker not in text:
        row = f"| {project_cell} | {keywords_cell} | active | 初始化 | 补全项目现场 |  | {date.today().isoformat()} | 项目/{project_slug} |\n"
        text = text.rstrip() + "\n" + row
        index.write_text(text, encoding="utf-8")

    print(project_dir)


if __name__ == "__main__":
    main()
