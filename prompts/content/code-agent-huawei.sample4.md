# Deck: Agentic Coding Tool 体验分享（sample 4 pages）

Context:
- Audience: 工程师 / 研究人员（general）
- Use case: 可阅读/可转发的分享材料（偏“文档型 slides”，不是纯 live talk）
- Target length: 4 页（随机抽样 sample，用于 v2 流程测试）
- Language: zh（关键术语保留 English：LLM agent, agentic coding tool, Claude Code, Codex, agentic loop, tools, prompt）

Sampling note:
- 从原始材料中“随机抽样”出 4 个主题块做成 4 页：定义与背景、Claude Code loop、个人体验对比、Critical Rules + ralph-loop。
- 本文件只覆盖 sample 选中的主题块；不代表对原文的完整覆盖。

Rules:
- One main idea per page.
- 对于选中主题块：No silent dropping（该主题块内的重要信息必须进入 “Must include”）。
- 若需要图/表/代码：在本文件里明确内容或引用原始片段；若缺失则标 TODO。

## Page 1: LLM agent 与 agentic coding tool：最小但准确的定义

Intent:
- 建立“不是 chatbot”的心智模型：LLM agent = 会规划 + 会用工具 + 有记忆；agentic coding tool = coding domain 的 LLM agent。

Must include:
- 定义（中文为主，术语保留英文）：
  - **LLM agent**：以 LLM 作为 “brain”，能推理/规划并执行多步任务，不是单轮回答的 chatbot。
  - **agentic coding tool**：面向 coding domain 的 LLM agent（例：**Claude Code** / **Codex**）。
- 关键组件（控制在 3 点，避免堆字）：
  - Reasoning & Planning：拆解目标 → 子任务 → 决定下一步动作
  - Tool Use：调用外部工具（读/改文件、执行命令、搜索等）
  - Memory：短期（当前对话上下文）/长期（跨任务沉淀）
- 必须提到“图”：用一张示意图来表达 agent 的组成（brain + tools + memory）。

Optional:
- 用 1 句点出“为什么重要”：把“读代码→改代码→跑命令→验证”串成闭环。

Suggested representation:
- Primary: 左侧“定义 + 3 组件”结构化要点
- Secondary: 右侧示意图 + 一行 caption

Assets:
- `materials/code-agent-huawei/llm-agent.jpg`（caption：LLM agent vs traditional agent / brain+tools+memory）

Notes / TODO:
- 标题中文；术语保留英文（LLM agent / agentic coding tool）。

## Page 2: Claude Code 的 agentic loop：3 阶段 + tools 分类

Intent:
- 用一个清晰结构解释 Claude Code 的工作方式：loop 的三阶段 + tools 是“行动力”的来源；强调可自适应与可被用户打断/引导。

Must include:
- 三阶段 loop（保留英文短语更清晰）：gather context → take action → verify results。
- loop 的特性：
  - 会根据任务自适应（问答可能只 gather context；修 bug 会循环多轮）
  - 用户可随时 interrupt / steer（人也在 loop 中）
- “tools + models” 作为 loop 的两大组件（1 句）。
- Tools 分类（4 类即可；可把 Code intelligence 作为可选补充）：
  - File operations
  - Search
  - Execution
  - Web

Optional:
- 用一个小例子（1 行）：比如“fix failing tests”会经历 run tests → read error → search files → edit → rerun。

Suggested representation:
- Primary: 3 节点循环流程图（每个节点配一个极简 icon）
- Secondary: 2×2 卡片/表格展示 tools 四类（每类 1 行解释）

Assets:
- `materials/code-agent-huawei/cc-agentic-loop.svg`（若使用该图：需要在 styled 阶段决定是否转成插图或重绘）

Notes / TODO:
- 不要把 tools 分类表塞太多文字；每类 1 行就够。

## Page 3: 个人体验：Claude Code vs Codex（好处、风险、适用场景）

Intent:
- 把“感受”翻译成可行动结论：什么时候用 Claude Code，什么时候用 Codex；并明确风险点（placeholders）。

Must include:
- 个人体验时间线（简化为 1 行）：Copilot(tab completion) → Cursor(heavy review) → Claude Code(沉浸但会“应付”) → Codex(更干活但慢)。
- 对比要点（避免长引用，保留原意）：
  - Claude Code：更“说人话”、更 Vibe/情绪价值；但可能告诉你“完成了”而代码里全是 placeholders（需要 human review）。
  - Codex：更像“真的干活”，但慢、解释不一定好懂；需要更多人类 context switch 来把控节奏。
- 我的结论（takeaway，1–2 句）：
  - 真实科研/项目里不能完全 vibe coding；需要掌握 feature/architecture/example。
  - “Claude Code 更适合讨论需求；Codex 更适合按既定方案干重活。”

Optional:
- 可加入 1–2 条“名人短句”作为旁注（不要整段引用；保持短、可读）。

Suggested representation:
- Primary: 两列对比（Claude Code vs Codex）
- Secondary: 底部 takeaway 条（高亮）

Assets:
- 无

Notes / TODO:
- 该页容易过密：若后续扩展，可把“体验时间线”单独拆一页。

## Page 4: 方法论：Critical Rules + ralph-loop（让 agent 不丢信息、不半途而废）

Intent:
- 给出可复用的实践规则：用文件做计划/记录；2-action rule 防止信息丢失；ralph-loop 解决“agent 提前停止”。

Must include:
- “File Purposes” 的三文件结构（表格形式最合适）：
  - `task_plan.md`：phases / progress / decisions（每个 phase 后更新）
  - `findings.md`：research / discoveries（每次发现后更新）
  - `progress.md`：session log / test results（过程持续记录）
- “Critical Rules”（四条要点）：
  1. Create Plan First：复杂任务先写 `task_plan.md`（non-negotiable）
  2. The 2-Action Rule：每 2 次 view/browser/search 后立刻写入文件
  3. Read Before Decide：重大决策前读 plan，避免偏航
  4. Update After Act：完成 phase 后更新状态 + 记录错误
- ralph-loop 的核心（用最小代码片段 + 一句话解释）：
  - `while :; do cat PROMPT.md | claude-code ; done`
  - 作用：prompt 不变、文件持续累积，循环迭代直到完成
- “Perfect combination” 的一句：用 `/ralph-loop ... --completion-promise "DONE"` 作为双保险（点到为止）。

Optional:
- 如果页面过密，把 “ralph-loop” 拆成 `Page 4 (cont.)`（本 sample 先不拆）。

Suggested representation:
- Primary: 左侧表格（3 files）+ 右侧 checklist（4 rules）
- Secondary: 下方一条“loop”示意图（循环箭头 + prompt/file）
- Code snippet 单独放在小卡片里（等宽字体）

Assets:
- 无

Notes / TODO:
- 该页的价值在“可执行”：让读者能马上照做（模板化）。

