# 接棒

接棒 is an agent skill for managing multi-project handoffs and workspaces.

It helps an AI agent start from the project context instead of an empty chat box:

- identify or create the right project workspace
- ingest meeting notes, webpages, PDFs, screenshots, chats, and raw materials
- read project state before doing work
- keep decisions, rejected directions, materials, todos, and handoff notes visible
- propose writeback after a task without silently turning temporary thoughts into long-term rules

## Why this exists

Agents often have many tools but still behave like a new teammate every time:

- they forget what was already rejected
- they restart from old assumptions
- they summarize materials without updating the project state
- they do work before reading the current completion standard

This skill adds a lightweight project "worksite" around the agent.
In plain Chinese: it makes the agent 接住上一棒 before doing the next task.

## Workspace Structure

Default root:

```text
Agent_Workspace/
  00_Inbox/
  99_Shared_Materials/
  项目索引.md
  全局方法/
    写作方法.md
    选题判断.md
    审稿标准.md
    工具使用规则.md
  项目/
    项目A/
    项目B/
```

Each project contains:

```text
项目名/
  00_项目现场.md
  01_判断记录.md
  02_完成标准.md
  03_素材索引.md
  04_复盘记录.md
  05_会议记录/
  06_原始材料/
  07_产出物/
  08_待办.md
  09_接班记录.md
```

## Quick Start

Initialize a workspace:

```bash
python3 scripts/init_workspace.py --root Agent_Workspace
```

Create a project:

```bash
python3 scripts/create_project.py \
  --root Agent_Workspace \
  --name "AI 课程试运行" \
  --keywords "课程,试运行,学员反馈"
```

Validate the workspace:

```bash
python3 scripts/validate_workspace.py --root Agent_Workspace
```

## Agent Usage

Ask the agent to use the skill before doing long-running project work:

```text
Use 接棒 to identify the project, read the current worksite, then continue this task.
```

For material ingestion:

```text
Use 接棒 to put this material into the right project worksite. Do not just summarize it.
```

For task closeout:

```text
Use 接棒 to propose what should be written back to the project worksite.
```

## Important Rules

- Do not write into a project when project identity is ambiguous.
- Do not overwrite old decisions; append dated records.
- Do not save secrets, tokens, cookies, private keys, or sensitive raw materials into public outputs.
- Do not turn single-project preferences into global methods unless they have been reused across projects.
- Always validate the workspace structure after creating or updating project files.

## Files

- `SKILL.md`: the skill instruction file
- `scripts/init_workspace.py`: create the root workspace structure
- `scripts/create_project.py`: create a project with standard files
- `scripts/validate_workspace.py`: validate workspace and project structure
- `templates/`: project and prompt templates
- `examples/`: example workflows
- `agents/openai.yaml`: example agent metadata

## License

MIT
