# 接棒

接棒是一个用于管理多项目交接和工作区的 agent 技能。

它帮助 AI agent 从项目上下文开始工作，而不是从一个空白聊天框开始：

- 识别或创建正确的项目工作区
- 摄取会议纪要、网页、PDF、截图、聊天记录和原始材料
- 做事前先读取项目状态
- 让决策、被否掉的方向、材料、待办和交接记录保持可见
- 任务结束后提出写回建议，而不是悄悄把临时想法变成长期规则

## 为什么需要它

Agent 经常有很多工具，但每次表现得还是像一个刚入职的新同事：

- 忘了哪些方向已经被否掉
- 从旧假设重新开始
- 只总结材料，却不更新项目状态
- 还没读取当前完成标准就开始干活

这个技能给 agent 加了一个轻量级的项目“现场”。

说白了：它让 agent 在做下一件事之前，先接住上一棒。

## 工作区结构

默认根目录：

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

每个项目包含：

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

## 快速开始

初始化一个工作区：

```bash
python3 scripts/init_workspace.py --root Agent_Workspace
```

创建一个项目：

```bash
python3 scripts/create_project.py \
  --root Agent_Workspace \
  --name "AI 课程试运行" \
  --keywords "课程,试运行,学员反馈"
```

验证工作区：

```bash
python3 scripts/validate_workspace.py --root Agent_Workspace
```

## Agent 使用方式

在开始长期项目工作前，要求 agent 使用这个技能：

```text
使用接棒来识别项目，读取当前项目现场，然后继续这个任务。
```

用于材料摄取：

```text
使用接棒把这份材料放进正确的项目现场。不要只是总结它。
```

用于任务收尾：

```text
使用接棒提出哪些内容应该写回项目现场。
```

## 重要规则

- 项目身份不明确时，不要写入项目。
- 不要覆盖旧决策；追加带日期的记录。
- 不要把密钥、token、cookie、私钥或敏感原始材料保存到公开输出里。
- 不要把单个项目的偏好变成全局方法，除非它已经在多个项目中复用过。
- 创建或更新项目文件后，始终验证工作区结构。

## 文件

- `SKILL.md`：技能说明文件
- `scripts/init_workspace.py`：创建根工作区结构
- `scripts/create_project.py`：创建带标准文件的项目
- `scripts/validate_workspace.py`：验证工作区和项目结构
- `templates/`：项目模板和提示词模板
- `examples/`：示例工作流
- `agents/openai.yaml`：示例 agent 元数据

## 许可证

MIT
