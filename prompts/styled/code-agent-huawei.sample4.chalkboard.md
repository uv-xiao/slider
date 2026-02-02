# Deck-level style/formatting contract (apply to every slide)

- Style brief: `styles/chalkboard.md` (chalkboard background + colorful chalk drawings).
- Canvas: 16:9. Background color `#1C2B1C` (green-black chalkboard) with subtle chalk dust, scratches, faint eraser smudges; no gradients/gloss.
- Safe margin: 8% on all sides (keep all text/diagrams inside).
- Typography feel:
  - Titles: hand-drawn bold chalk lettering (imperfect baseline), usually Chalk White `#F5F5F5`, with 1 accent word in Chalk Yellow `#FFE566`.
  - Body: neater chalk handwriting, slightly thinner strokes; keep legible (no tiny fonts).
- Color roles:
  - Primary text/lines: `#F5F5F5`
  - Highlights: `#FFE566` (key terms), `#66B3FF` (structure/links), `#90EE90` (success/“good practice”), `#FFB366` (warnings), `#FF9999` (caution/risk).
- Reusable components (use consistently across slides):
  - Chalk “card” container: hand-drawn rounded rectangle (imperfect), white outline 2–3px, faint chalk dust around edges.
  - Underline: sketchy chalk stroke (yellow or blue).
  - Callout bubble: small cloud/rounded bubble with pink outline for “风险/注意”.
  - Icons: simple chalk doodles (magnifier, wrench, check, brain, folder, note) outline-only, consistent stroke.
  - Arrows: hand-drawn, slightly wavy; consistent stroke; arrowheads simple.
- Language: 中文为主；关键术语保留 English（LLM agent, agentic coding tool, Claude Code, Codex, agentic loop, tools, prompt）。
- Guardrails: no slide numbers/footers/logos; avoid perfect geometry; add subtle doodles but never clutter.

## Slide 1: LLM agent 与 agentic coding tool：最小但准确的定义

Layout decision:
- Left: definition + 3 components (with small chalk icons).
- Right: pinned “photo card” showing the provided LLM agent illustration + 1-line caption.

Element spec (bbox in %, x,y,w,h; top-left origin):
- id: bg
  type: shape
  bbox: 0,0,100,100
  z: background
  content: green-black chalkboard texture (#1C2B1C) with subtle dust/smudges.
  style: no border.
- id: title
  type: title
  bbox: 8,6,84,10
  z: content
  content: "LLM agent 与 agentic coding tool：最小但准确的定义"
  style: chalk title; mostly #F5F5F5; highlight “agentic coding tool” in #FFE566; left aligned.
- id: underline
  type: line
  bbox: 8,16,60,1
  z: content
  content: sketchy underline stroke
  style: chalk stroke #66B3FF with chalk dust.

- id: left_card
  type: shape
  bbox: 8,22,52,68
  z: content
  content: chalk card container for text
  style: hand-drawn rounded rect; white outline 3px; faint dust; no fill (transparent).
- id: def_block
  type: text
  bbox: 11,25,46,18
  z: content
  content: |
    **LLM agent**：以 LLM 作为 “brain”，能推理/规划并执行多步任务，不是单轮回答的 chatbot。
    **agentic coding tool**：面向 coding domain 的 LLM agent（例如 **Claude Code** / **Codex**）。
  style: neat chalk handwriting; #F5F5F5; emphasize keywords with #FFE566.
- id: components_header
  type: text
  bbox: 11,44,46,6
  z: content
  content: "3 个关键组件："
  style: bold chalk; #66B3FF.
- id: components
  type: bullets
  bbox: 11,50,46,38
  z: content
  content: |
    - (🧠) **Reasoning & Planning**：拆解目标 → 子任务 → 决定下一步动作
    - (🛠️) **Tool Use**：调用外部工具（读/改文件、执行命令、搜索等）
    - (🗂️) **Memory**：短期（当前上下文）/长期（跨任务沉淀）
  style: chalk bullets; #F5F5F5; icon doodles should look like chalk drawings (not emoji).
- id: why_matters
  type: callout
  bbox: 11,88,46,6
  z: content
  content: "为什么重要：把“读代码→改代码→跑命令→验证”串成闭环。"
  style: bubble outline #90EE90; text #F5F5F5; small.

- id: right_photo_card
  type: shape
  bbox: 63,22,29,68
  z: content
  content: pinned photo card container
  style: white outline 3px; add 2 small “tape” doodles on top corners in #FFB366.
- id: llm_agent_img
  type: image
  bbox: 65,26,25,50
  z: content
  content: "Place attached image; fit contain; preserve readability."
  style: add thin chalk frame line around image in #F5F5F5.
- id: img_caption
  type: text
  bbox: 65,78,25,10
  z: content
  content: "示意：brain + tools + memory"
  style: small chalk caption; #F5F5F5; centered; faint dust effect.

Rendering notes:
- Keep the left block readable; do not over-doodle.
- Use chalk texture on all strokes; avoid clean digital lines.

Assets:
- alt: LLM agent illustration | src: materials/code-agent-huawei/llm-agent.jpg

## Slide 2: Claude Code 的 agentic loop：3 阶段 + tools 分类

Layout decision:
- Top: 3-stage cyclic loop diagram (gather context → take action → verify results → back).
- Bottom: 2×2 “tool cards” with icon doodles.

Element spec:
- id: title
  type: title
  bbox: 8,6,84,10
  z: content
  content: "Claude Code 的 agentic loop：3 阶段 + tools"
  style: chalk title #F5F5F5; highlight “agentic loop” in #FFE566.
- id: underline
  type: line
  bbox: 8,16,54,1
  z: content
  content: underline
  style: chalk stroke #FFE566.

- id: loop_canvas
  type: shape
  bbox: 8,22,84,36
  z: content
  content: diagram area container
  style: hand-drawn rounded rect; outline #F5F5F5; dust.
- id: loop_diagram
  type: diagram
  bbox: 10,24,80,32
  z: content
  content: |
    Draw 3 chalk boxes arranged in a triangle/cycle with wavy arrows:
      1) "gather context"
      2) "take action"
      3) "verify results"
    Arrows: white chalk; show a clear cycle 1→2→3→1.
    Add mini icons near each node: magnifier (context), wrench (action), checkmark (verify).
  style: chalk white lines; accent node borders in #66B3FF.
- id: loop_note
  type: callout
  bbox: 62,52,28,6
  z: content
  content: "特点：会自适应任务；用户可随时 interrupt/steer"
  style: pink bubble outline #FF9999; text #F5F5F5.

- id: tools_grid_label
  type: text
  bbox: 8,60,40,5
  z: content
  content: "Tools 四类（每类 1 行）："
  style: chalk text; #66B3FF.
- id: tool_card_1
  type: shape
  bbox: 8,66,40,12
  z: content
  content: "File operations：读/改文件、重构"
  style: chalk card outline #F5F5F5; add folder doodle; highlight label in #FFE566.
- id: tool_card_2
  type: shape
  bbox: 52,66,40,12
  z: content
  content: "Search：找文件、正则检索、定位引用"
  style: chalk card outline #F5F5F5; add magnifier doodle; accent #66B3FF.
- id: tool_card_3
  type: shape
  bbox: 8,80,40,12
  z: content
  content: "Execution：跑命令、测试、git"
  style: chalk card outline #F5F5F5; add terminal doodle; accent #90EE90.
- id: tool_card_4
  type: shape
  bbox: 52,80,40,12
  z: content
  content: "Web：搜文档、查报错、获取最新信息"
  style: chalk card outline #F5F5F5; add globe doodle; accent #FFB366.

Rendering notes:
- Keep node text English for clarity; explanations in Chinese.
- Avoid tables that get too small; use 2×2 cards.

## Slide 3: 个人体验：Claude Code vs Codex（好处、风险、适用场景）

Layout decision:
- Middle: two-column comparison cards.
- Bottom: highlighted takeaway ribbon (1–2 sentences).
- Tiny top-left mini timeline (Copilot → Cursor → Claude Code → Codex) as a chalk arrow line.

Element spec:
- id: title
  type: title
  bbox: 8,6,84,10
  z: content
  content: "个人体验：Claude Code vs Codex"
  style: chalk title #F5F5F5; highlight “vs” in #FFE566.
- id: underline
  type: line
  bbox: 8,16,44,1
  z: content
  content: underline
  style: chalk stroke #66B3FF.

- id: timeline
  type: diagram
  bbox: 8,19,60,8
  z: content
  content: |
    Draw a small chalk arrow timeline with 4 labeled dots:
    Copilot(tab completion) → Cursor(heavy review) → Claude Code(placeholders 风险) → Codex(更干活但慢)
  style: thin chalk white line; dot highlights in #FFE566.

- id: left_col
  type: shape
  bbox: 8,28,40,48
  z: content
  content: "Claude Code column"
  style: chalk card outline #F5F5F5; add small heart/star doodle in #FF9999.
- id: right_col
  type: shape
  bbox: 52,28,40,48
  z: content
  content: "Codex column"
  style: chalk card outline #F5F5F5; add small gear/wrench doodle in #66B3FF.
- id: left_header
  type: text
  bbox: 10,30,36,6
  z: content
  content: "Claude Code（更 Vibe）"
  style: bold chalk; #FFE566.
- id: right_header
  type: text
  bbox: 54,30,36,6
  z: content
  content: "Codex（更干活）"
  style: bold chalk; #FFE566.
- id: left_points
  type: bullets
  bbox: 10,36,36,38
  z: content
  content: |
    - 更“说人话”，更 Vibe/情绪价值
    - 适合讨论需求/方向
    - 风险：可能“完成了但代码是 placeholders”→ 需要 human review
  style: chalk bullets #F5F5F5; highlight “placeholders” in #FF9999.
- id: right_points
  type: bullets
  bbox: 54,36,36,38
  z: content
  content: |
    - 更像“真的干活”
    - 慢；解释不一定好懂
    - 需要更多人类 context switch 来把控节奏
  style: chalk bullets #F5F5F5; highlight “context switch” in #FFB366.

- id: takeaway_ribbon
  type: shape
  bbox: 8,79,84,14
  z: content
  content: takeaway ribbon
  style: hand-drawn banner outline #90EE90; add light chalk dust; no solid fill.
- id: takeaway_text
  type: text
  bbox: 10,81,80,10
  z: content
  content: |
    结论：真实科研/项目里不能完全 vibe coding；需要掌握 feature/architecture/example。
    Claude Code 更适合讨论需求；Codex 更适合按既定方案干重活。
  style: readable chalk; #F5F5F5; key words in #FFE566.

Rendering notes:
- Keep this slide “one message”: comparison + takeaway; avoid extra quotes.

## Slide 4: 方法论：Critical Rules + ralph-loop（不丢信息、不半途而废）

Layout decision:
- Left: “File Purposes” table (3 rows × 3 columns, readable).
- Right: “Critical Rules” checklist (4 items) with colored highlights.
- Bottom: ralph-loop code snippet + loop doodle.

Element spec:
- id: title
  type: title
  bbox: 8,6,84,10
  z: content
  content: "方法论：Critical Rules + ralph-loop"
  style: chalk title #F5F5F5; highlight “Critical Rules” in #FFE566.
- id: underline
  type: line
  bbox: 8,16,58,1
  z: content
  content: underline
  style: chalk stroke #FFE566.

- id: left_table_card
  type: shape
  bbox: 8,22,44,44
  z: content
  content: "Table container"
  style: chalk card outline #F5F5F5; add small folder doodle in #66B3FF.
- id: file_purposes_title
  type: text
  bbox: 10,24,40,5
  z: content
  content: "File Purposes（3 个文件）："
  style: bold chalk; #66B3FF.
- id: file_table
  type: table
  bbox: 10,30,40,34
  z: content
  content: |
    | File | Purpose | When to Update |
    |---|---|---|
    | `task_plan.md` | Phases / progress / decisions | After each phase |
    | `findings.md` | Research / discoveries | After ANY discovery |
    | `progress.md` | Session log / test results | Throughout session |
  style: chalk table lines; headers in #FFE566; body text #F5F5F5; row separators thin.

- id: right_rules_card
  type: shape
  bbox: 56,22,36,44
  z: content
  content: "Checklist container"
  style: chalk card outline #F5F5F5; add small checkmark doodle in #90EE90.
- id: rules_title
  type: text
  bbox: 58,24,32,5
  z: content
  content: "Critical Rules（4 条）："
  style: bold chalk; #66B3FF.
- id: rules_list
  type: bullets
  bbox: 58,30,32,34
  z: content
  content: |
    - ✅ **Create Plan First**：复杂任务先写 `task_plan.md`（non-negotiable）
    - ⏱️ **The 2-Action Rule**：每 2 次 view/browser/search 后立刻写入文件
    - 📖 **Read Before Decide**：重大决策前读 plan，避免偏航
    - 📝 **Update After Act**：完成 phase 后更新状态 + 记录错误
  style: chalk checklist; #F5F5F5; highlight rule names in #FFE566; warning emphasis for 2-action in #FFB366.

- id: bottom_code_card
  type: shape
  bbox: 8,69,84,23
  z: content
  content: "Code + loop area"
  style: chalk card outline #F5F5F5; add small loop arrow doodle in #90EE90.
- id: ralph_code
  type: code
  bbox: 10,72,44,17
  z: content
  content: |
    while :; do
      cat PROMPT.md | claude-code
    done
  style: chalk-like monospace feel; #F5F5F5; code on a darker inset panel (#1A1A1A) with chalk border.
- id: ralph_explain
  type: text
  bbox: 56,72,34,17
  z: content
  content: |
    核心：prompt 不变、文件持续累积 → 循环迭代直到完成。
    “Perfect combination”：`/ralph-loop ... --completion-promise \"DONE\"`（点到为止）
  style: chalk text; #F5F5F5; highlight “prompt 不变 / 文件累积” in #90EE90.

Rendering notes:
- This slide is dense; keep table and checklist readable (no tiny fonts).
- Keep the code block clearly separated with a darker inset panel.

