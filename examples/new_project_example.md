# 新项目示例

用户输入：

```text
我要开始一个项目：AI 课程试运行。帮我建项目现场。
```

建议执行：

```bash
python scripts/init_workspace.py --root Agent_Workspace
python scripts/create_project.py --root Agent_Workspace --name "AI 课程试运行" --keywords "课程,试运行,学员反馈"
python scripts/validate_workspace.py --root Agent_Workspace
```

预期结果：

```text
Agent_Workspace/
  项目索引.md
  项目/AI-课程试运行/
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

