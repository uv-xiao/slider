# Deck-level style/formatting contract (apply to every slide)

- Style brief: `styles/editorial-infographic.md`（高端杂志式信息图，清晰叙事、结构化版面、可视化锚点）。
- Canvas: 16:9。背景 `#FFFFFF`（纯白）；分区浅底 `#F8F9FA`；分割线 `#D1D5DB`。
- Safe margin: 7%（所有文字/图形不得贴边）。
- Typography feel（可读优先）：
  - 标题：粗体现代无衬线（杂志标题感），近黑 `#1A1A1A`，左对齐。
  - 小标题/分区标题：半粗无衬线，强调色或近黑。
  - 正文：人文无衬线，行距 1.5~1.7；次要说明 `#4A5568`。
- Accent colors（全篇统一，少而精）：
  - Editorial Blue `#2563EB`（主强调/关键箭头/框架主线）
  - Coral `#F97316`（次强调/扩张/风险提示）
  - Emerald `#10B981`（正向/增益/“提升”）
  - Amber `#F59E0B`（注意/关键结论条）
- Reusable components（全篇复用）：
  - `section_badge`：圆角胶囊标签（填充浅色，边框同色 2px），用于 A/B/C 分类。
  - `evidence_card`：浅灰底卡片（#F8F9FA）+ 细边框（#D1D5DB）+ 左上角小标题。
  - `metric_chip`：数字胶囊（深色字+浅底），用于 9.27×、3.01×、5.22× 等硬指标。
  - `evidence_strip`：底部“证据栏”（会议’年份标签一排，像杂志 footnote）。
  - `pull_quote`：结尾一段加粗引述块（左侧 6px 竖线，蓝色）。
- Icon/diagram rules：
  - 图标：线性扁平、统一线宽（2px），不混风格，不用 emoji。
  - 图表：只画“趋势/结构/关系”，不追求精确数值；所有线条干净、对比强。
  - 禁止：照片风格大图、杂乱拼贴、无意义装饰。
- Language: 全中文；项目名/会议名允许保留英文缩写（MLIR, e-graph, RTL, HLS）。
- Guardrails: 不加页码/水印/Logo（除非作为“来源标签”）。
- Debug/坐标禁令：**绝对禁止**在画面中绘制任何布局调试信息（bbox 边框、角标、坐标/百分比文字）。例如不得出现“7%x,10%y / 93%x,48%y / 20% / 60% / 86%”等。`bbox` 仅用于内部布局推理，不能作为可见内容。

## Slide 1: 奋进奖学金答辩｜把协同优化做成工具链能力

Layout decision:
- 纯封面：左上大标题 + 左下身份信息 + 右下“一句话主线”；右侧放一个极简“Chip-Compiler-Toolchain”图标组作为视觉锚点。

Element spec（bbox 仅用于布局，不可见；不要画 bbox 框/坐标角标）:
- id: bg
  type: shape
  bbox: 0,0,100,100
  z: background
  content: pure white background
  style: fill #FFFFFF; no border.
- id: title
  type: title
  bbox: 7,10,70,16
  z: content
  content: "奋进奖学金答辩"
  style: headline; very large; #1A1A1A; left aligned.
- id: subtitle
  type: text
  bbox: 7,28,70,10
  z: content
  content: "肖有为｜北京大学集成电路学院｜奖励方向：1. 集成电路设计"
  style: subhead; #4A5568; left aligned.
- id: mainline_label
  type: shape
  bbox: 7,80,86,12
  z: content
  content: rounded banner container
  style: fill #F8F9FA; border 2px #D1D5DB; radius 16px.
- id: mainline_text
  type: text
  bbox: 9,82,82,8
  z: content
  content: "主线：算力紧缺 → 生产力不足 → 协同闭环与开源工具链"
  style: bold body; #1A1A1A; left aligned; highlight “协同闭环/开源工具链” in #2563EB.
- id: icon_cluster
  type: diagram
  bbox: 73,18,20,30
  z: content
  content: |
    Minimal line icons in a row: (1) microchip, (2) compiler/IR bracket, (3) toolchain loop arrows.
    Use consistent 2px stroke, rounded caps, no fill. Color #2563EB with 1 accent in #F97316.
  style: clean editorial iconography.

Rendering notes:
- 保持留白与高级感；不要堆文字。
- 禁止出现任何坐标/百分比角标、bbox 边框或调试文字。

Assets:
- none

## Slide 2: 产业共识｜复杂度×产品线×全栈优化：生产力成为瓶颈（Apple｜ISSCC 2026）

Layout decision:
- 顶部标题；中部 3 张纵向“证据卡片”（每张卡：左侧重绘小图 + 右侧一句结论）；底部一条结论横幅。右上角放“来源标签”（非大截图）。

Element spec:
- id: title
  type: title
  bbox: 7,6,86,10
  z: content
  content: "产业共识：复杂度与产品线扩张倒逼全栈协同优化（Apple｜ISSCC 2026）"
  style: headline; #1A1A1A; left aligned.
- id: source_tag
  type: badge
  bbox: 78,6,15,8
  z: content
  content: "Source: Apple ISSCC 2026 Keynote"
  style: small badge; border 1.5px #D1D5DB; fill #FFFFFF; text #4A5568; radius 10px; centered.

- id: card1
  type: shape
  bbox: 7,18,86,20
  z: content
  content: evidence_card container
  style: fill #F8F9FA; border 1.5px #D1D5DB; radius 14px.
- id: card1_chart
  type: diagram
  bbox: 9,20,34,16
  z: content
  content: |
    Redraw a simple 2-line trend chart (2013–2023 x-axis).
    - Green line (complexity): rising steadily, steeper after ~2018.
    - Orange line (talent supply): rises then declines/plateaus, crossing green around ~2020.
    Add a small "gap" bracket after the crossing. No exact values, only trend.
  style: white mini-canvas inside card; thin gridlines #D1D5DB; line colors #10B981 and #F97316; labels in #4A5568.
- id: card1_takeaway
  type: text
  bbox: 45,21,46,16
  z: content
  content: "复杂度增长快于人才供给，工具链生产力成为决定性瓶颈。"
  style: bold body; #1A1A1A; left aligned; emphasize “生产力” in #2563EB.

- id: card2
  type: shape
  bbox: 7,40,86,20
  z: content
  content: evidence_card container
  style: fill #F8F9FA; border 1.5px #D1D5DB; radius 14px.
- id: card2_chart
  type: diagram
  bbox: 9,42,34,16
  z: content
  content: |
    Redraw a family+tier expansion infographic (2010–2025).
    Use a horizontal timeline with grouped rows:
    - A-series row (baseline continuous),
    - M-series row (starts later; tiers appear: base / Pro / Max / Ultra as stacked small blocks),
    - S/W/H rows (shorter segments).
    Only show family letters (A/M/S/W/H) and tier tags (Pro/Max/Ultra), NOT every model.
    Visually convey growth from single row to multi-row multi-tier.
  style: blocks with thin borders; accent #2563EB for new tiers, #F97316 for "expansion" highlight.
- id: card2_takeaway
  type: text
  bbox: 45,43,46,16
  z: content
  content: "产品线与层级爆炸使架构/软件适配成为常态，协同必须框架化与可复用。"
  style: bold body; #1A1A1A; left aligned; emphasize “框架化/可复用” in #2563EB.

- id: card3
  type: shape
  bbox: 7,62,86,20
  z: content
  content: evidence_card container
  style: fill #F8F9FA; border 1.5px #D1D5DB; radius 14px.
- id: card3_chart
  type: diagram
  bbox: 9,64,34,16
  z: content
  content: |
    Redraw a full-stack ladder:
    Application → Algorithms → Programming Language → OS/VM → Microarchitecture → RTL → Circuits → CMOS Devices.
    Show as stacked rounded bars. Add a right-side brace with label "Optimization across the stack".
    Highlight the middle chain (Language/OS/Microarchitecture/RTL) slightly darker to imply toolchain focus.
  style: rounded bars; text #1A1A1A; subtle fills #E5E7EB; highlight bar borders in #2563EB.
- id: card3_takeaway
  type: text
  bbox: 45,65,46,16
  z: content
  content: "优化跨栈联动成为主流，需要端到端闭环与可重定向编译。"
  style: bold body; #1A1A1A; left aligned; emphasize “端到端闭环/可重定向编译” in #2563EB.

- id: bottom_banner
  type: shape
  bbox: 7,84,86,10
  z: callout
  content: conclusion banner
  style: fill #2563EB; radius 14px; no border.
- id: bottom_banner_text
  type: text
  bbox: 9,85.5,82,7
  z: callout
  content: "结论：把“协同优化”工具链化，才能把生产力变成系统能力。"
  style: bold; white #FFFFFF; centered.
- id: footnote
  type: text
  bbox: 7,95,86,4
  z: content
  content: "来源：tspasemiconductor.substack.com（Apple ISSCC 2026 Keynote 摘要整理）"
  style: tiny caption; #4A5568; left aligned.

Rendering notes:
- 三张卡片风格必须一致（同样圆角/边框/留白）；图形极简，不追求精确数据。

Assets:
- none (redraw; do not paste photos)

## Slide 3: 总览｜三类工具链能力对应三类产业痛点

Layout decision:
- 上方标题；中部三行对照表（痛点→能力→意义），每行一个 A/B/C 标签；底部一条细闭环箭头图。

Element spec:
- id: title
  type: title
  bbox: 7,6,86,10
  z: content
  content: "我的总体贡献：三类“工具链能力”对应三类产业痛点"
  style: headline; #1A1A1A.

- id: table_container
  type: shape
  bbox: 7,18,86,58
  z: content
  content: clean table container
  style: fill #FFFFFF; border 1.5px #D1D5DB; radius 14px.
- id: row1_badge
  type: badge
  bbox: 9,21,6,6
  z: content
  content: "A"
  style: section_badge; fill #E8F0FF; border 2px #2563EB; text #2563EB; centered.
- id: row1_text
  type: text
  bbox: 16,20,75,12
  z: content
  content: |
    痛点：应用迭代快、协同跟不上
    能力：可重定向编译 + 端到端协同闭环（统一IR/接口，快速验证迭代）
    意义：把协同做成“可复用框架能力”
  style: body; #1A1A1A; key phrases in #2563EB.

- id: divider1
  type: line
  bbox: 9,33,82,1
  z: content
  content: thin divider
  style: stroke #D1D5DB 2px.

- id: row2_badge
  type: badge
  bbox: 9,36,6,6
  z: content
  content: "B"
  style: section_badge; fill #ECFDF5; border 2px #10B981; text #10B981; centered.
- id: row2_text
  type: text
  bbox: 16,35,75,12
  z: content
  content: |
    痛点：RTL抽象低，效率与可靠性受限
    能力：事务/时序语义抽象 + 规则化描述 + AI辅助方法学
    意义：把硬件前端“提产、可组合、可验证”
  style: body; #1A1A1A; key phrases in #10B981.

- id: divider2
  type: line
  bbox: 9,48,82,1
  z: content
  content: thin divider
  style: stroke #D1D5DB 2px.

- id: row3_badge
  type: badge
  bbox: 9,51,6,6
  z: content
  content: "C"
  style: section_badge; fill #FFF7ED; border 2px #F97316; text #F97316; centered.
- id: row3_text
  type: text
  bbox: 16,50,75,12
  z: content
  content: |
    痛点：优化割裂，质量与扩展性难兼得
    能力：多层IR方法学 + e-graph联合决策（选择/调度一体化）
    意义：把综合优化“系统化、可扩展”
  style: body; #1A1A1A; key phrases in #F97316.

- id: loop_diagram
  type: diagram
  bbox: 7,78,86,16
  z: content
  content: |
    Thin loop arrow diagram with 6 nodes:
    应用/工作负载 → IR/编译 → 定制（指令/微架构/加速器） → 前端实现抽象 → 综合与优化 → 评测/落地 → 回到应用.
    Use rounded rectangles and arrows; keep minimal text.
  style: stroke #2563EB 2px; node fill #F8F9FA; text #1A1A1A.

Assets:
- none

## Slide 4: A类能力｜协同闭环与自动定制（APS/Aquas/Clay/ISAMORE/Cayman）

Layout decision:
- 左侧大框架图（闭环）+ 右侧三张成果卡 + 底部证据栏；左上角放 A 徽章；右上角放 9.27× 数字卡。

Element spec:
- id: badgeA
  type: badge
  bbox: 7,6,6,6
  z: content
  content: "A"
  style: section_badge; fill #E8F0FF; border 2px #2563EB; text #2563EB.
- id: title
  type: title
  bbox: 14,6,79,10
  z: content
  content: "A类能力：协同闭环与自动定制（敏捷专用化的工具链化）"
  style: headline; #1A1A1A.

- id: loop_frame
  type: diagram
  bbox: 7,18,60,62
  z: content
  content: |
    Draw a 5-stage loop (left-to-right with a return arrow):
    1) Workload（应用/模型）
    2) MLIR IR（统一接口）
    3) E-Graph Opt（可重定向编译）
    4) Specialization（指令/微架构/加速器定制）
    5) Eval&Loop（端到端评测与迭代）
    Use rounded rectangles; arrows in #2563EB; return arrow indicates iteration.
  style: clean editorial diagram; node fill #F8F9FA; borders #D1D5DB.
- id: metric_927
  type: badge
  bbox: 58,18,9,7
  z: callout
  content: "9.27×"
  style: metric_chip; fill #ECFDF5; border 2px #10B981; text #10B981; centered; bold.
- id: metric_caption
  type: text
  bbox: 48,25,19,4
  z: content
  content: "端到端协同优化结果之一"
  style: tiny caption; #4A5568; right aligned.

- id: cardA1
  type: shape
  bbox: 69,18,24,18
  z: content
  content: evidence_card
  style: fill #F8F9FA; border 1.5px #D1D5DB; radius 14px.
- id: cardA1_text
  type: text
  bbox: 71,20,20,14
  z: content
  content: |
    端到端协同闭环
    把应用驱动协同做成框架能力
    （APS + Aquas）
  style: body; #1A1A1A; first line bold; emphasis #2563EB.

- id: cardA2
  type: shape
  bbox: 69,38,24,18
  z: content
  content: evidence_card
  style: fill #F8F9FA; border 1.5px #D1D5DB; radius 14px.
- id: cardA2_text
  type: text
  bbox: 71,40,20,14
  z: content
  content: |
    指令/微架构定制
    从专家经验→可复用/可自动化
    （Clay + ISAMORE）
  style: body; #1A1A1A; emphasis #2563EB.

- id: cardA3
  type: shape
  bbox: 69,58,24,18
  z: content
  content: evidence_card
  style: fill #F8F9FA; border 1.5px #D1D5DB; radius 14px.
- id: cardA3_text
  type: text
  bbox: 71,60,20,14
  z: content
  content: |
    自动加速器生成
    把“生成+优化”纳入闭环
    （Cayman）
  style: body; #1A1A1A; emphasis #2563EB.

- id: evidence_strip
  type: text
  bbox: 7,82,86,10
  z: content
  content: "证据：APS（ICCAD’25 Invited）｜Clay（ICCAD’25）｜ISAMORE（ASPLOS’26）｜Cayman（DAC’25）｜Aquas（arXiv’25）"
  style: evidence_strip; small; #4A5568; left aligned; use separators as thin dots.

Assets:
- none

## Slide 5: B类能力｜语义化抽象 + 规则化描述 + AI辅助评测（Cement/OriGen/LLM评测）

Layout decision:
- 左侧“语义阶梯图”作为视觉锚点；右侧三张卡片（抽象/规则/AI评测）；底部证据栏。

Element spec:
- id: badgeB
  type: badge
  bbox: 7,6,6,6
  z: content
  content: "B"
  style: section_badge; fill #ECFDF5; border 2px #10B981; text #10B981.
- id: title
  type: title
  bbox: 14,6,79,10
  z: content
  content: "B类能力：把硬件前端从“低层RTL”提升为“语义化、可组合、可评测”"
  style: headline; #1A1A1A.

- id: ladder
  type: diagram
  bbox: 7,20,38,60
  z: content
  content: |
    A 3-step “semantic ladder” with ascending blocks:
    Step1: RTL（低层、易错、迭代慢）
    Step2: 事务/时序语义（可组合、可验证）
    Step3: AI辅助 + 评测闭环（可复现边界、可规模化迭代）
    Use subtle depth via spacing only (no shadows).
  style: blocks fill #F8F9FA; borders #D1D5DB; step highlight border colors: Step2 #10B981, Step3 #2563EB.

- id: cardB1
  type: shape
  bbox: 48,20,45,18
  z: content
  content: evidence_card
  style: fill #F8F9FA; border 1.5px #D1D5DB; radius 14px.
- id: cardB1_text
  type: text
  bbox: 50,22,41,14
  z: content
  content: |
    语义抽象：事务/周期级语义提升抽象与效率
    证据：（FPGA’24）+（arXiv’25：Cement2）
  style: body; #1A1A1A; emphasize “语义抽象” in #10B981.

- id: cardB2
  type: shape
  bbox: 48,40,45,18
  z: content
  content: evidence_card
  style: fill #F8F9FA; border 1.5px #D1D5DB; radius 14px.
- id: cardB2_text
  type: text
  bbox: 50,42,41,14
  z: content
  content: |
    规则化描述：Rust时序语义规则化，沉淀可复用模式
    证据：（LATTE’25 workshop：cmt2）
  style: body; #1A1A1A; emphasize “规则化” in #10B981.

- id: cardB3
  type: shape
  bbox: 48,60,45,18
  z: content
  content: evidence_card
  style: fill #F8F9FA; border 1.5px #D1D5DB; radius 14px.
- id: cardB3_text
  type: text
  bbox: 50,62,41,14
  z: content
  content: |
    AI辅助与评测：提升RTL生成质量，并用系统评测明确边界
    证据：（ICCAD’24：OriGen）+（FPGA’25：LLM vs HLS评测）
  style: body; #1A1A1A; emphasize “评测边界” in #2563EB.

- id: evidence_strip
  type: text
  bbox: 7,82,86,10
  z: content
  content: "证据：Cement（FPGA’24）｜Cement2（arXiv’25）｜cmt2（LATTE’25 workshop）｜OriGen（ICCAD’24）｜LLM评测（FPGA’25）"
  style: evidence_strip; small; #4A5568; left aligned.

Assets:
- none

## Slide 6: C类能力｜多层IR方法学 + e-graph联合决策（HECTOR + SkyEgg）

Layout decision:
- 左侧：HECTOR 方法学三点（清单）；右侧：两层示意图 + 大号硬指标 + 小柱状图；底部证据栏。

Element spec:
- id: badgeC
  type: badge
  bbox: 7,6,6,6
  z: content
  content: "C"
  style: section_badge; fill #FFF7ED; border 2px #F97316; text #F97316.
- id: title
  type: title
  bbox: 14,6,79,10
  z: content
  content: "C类能力：统一方法学的综合框架 + 联合决策优化（选择×调度）"
  style: headline; #1A1A1A.

- id: left_box
  type: shape
  bbox: 7,20,38,56
  z: content
  content: evidence_card
  style: fill #F8F9FA; border 1.5px #D1D5DB; radius 14px.
- id: left_header
  type: text
  bbox: 9,22,34,6
  z: content
  content: "HECTOR：综合方法学框架（ICCAD’22）"
  style: subhead; bold; #1A1A1A.
- id: left_bullets
  type: bullets
  bbox: 9,30,34,42
  z: content
  content: |
    - 多层IR：统一表达不同综合方法
    - 可扩展：优化/后端可插拔
    - 可复用：把综合能力框架化
  style: body bullets; #1A1A1A; bullet dots in #F97316.

- id: right_box
  type: shape
  bbox: 48,20,45,56
  z: content
  content: evidence_card
  style: fill #FFFFFF; border 1.5px #D1D5DB; radius 14px.
- id: right_header
  type: text
  bbox: 50,22,41,6
  z: content
  content: "SkyEgg：选择+调度联合决策（e-graph）"
  style: subhead; bold; #1A1A1A.
- id: right_statement
  type: text
  bbox: 50,29,41,8
  z: content
  content: "**用 e-graph 统一表示变换与实现选择，把“选择+调度”做联合决策。**"
  style: body; #1A1A1A; emphasize in #2563EB.
- id: metric
  type: badge
  bbox: 50,38,41,10
  z: callout
  content: "平均 3.01× ｜ 最高 5.22×  （vs Vitis HLS）"
  style: metric_chip; fill #E8F0FF; border 2px #2563EB; text #2563EB; centered; bold.
- id: joint_diagram
  type: diagram
  bbox: 50,50,27,24
  z: content
  content: |
    Two-layer minimalist diagram:
    - Top cloud labeled “等价变换空间（e-graph）”
    - Bottom: two boxes “Implementation Selection” and “Scheduling”
    - Between them: a small node “Joint Objective” connecting both.
    Arrows flow downward from cloud to the two boxes; thin blue lines.
  style: stroke #2563EB 2px; fills #F8F9FA; text #1A1A1A.
- id: small_bars
  type: diagram
  bbox: 79,50,12,24
  z: content
  content: |
    Tiny bar chart with 3 bars:
    Vitis (gray), Ours avg (blue), Ours best (emerald).
    Label only the key numbers “3.01×” and “5.22×”.
  style: clean chart; axis minimal; text #4A5568.

- id: evidence_strip
  type: text
  bbox: 7,82,86,10
  z: content
  content: "证据：HECTOR（ICCAD’22）｜联合选择/调度（arXiv’25）"
  style: evidence_strip; small; #4A5568; left aligned.

Assets:
- none

## Slide 7: 未来三年｜把敏捷芯片设计与软件生态适配做成可落地的开源平台

Layout decision:
- 左侧三段路线图（近期/中期/长期三列卡片）；右侧目标系统图（Platform + 3 interfaces）；底部一句“闭环路线”。

Element spec:
- id: title
  type: title
  bbox: 7,6,86,10
  z: content
  content: "未来三年：把“敏捷芯片设计与软件生态适配”做成可落地的开源平台"
  style: headline; #1A1A1A.

- id: roadmap1
  type: shape
  bbox: 7,20,28,44
  z: content
  content: roadmap card
  style: fill #F8F9FA; border 1.5px #D1D5DB; radius 14px.
- id: roadmap1_text
  type: text
  bbox: 9,22,24,40
  z: content
  content: |
    **近期：框架整合与关键特性增强**
    - 统一IR与接口，降低集成成本
    - 标准化评测基准与回归体系
    - 形成可复用模块库
  style: body; #1A1A1A; bullets.

- id: roadmap2
  type: shape
  bbox: 37,20,28,44
  z: content
  content: roadmap card
  style: fill #F8F9FA; border 1.5px #D1D5DB; radius 14px.
- id: roadmap2_text
  type: text
  bbox: 39,22,24,40
  z: content
  content: |
    **中期：支持商业落地级架构与编译栈**
    - 面向复杂多元架构的自动适配
    - 工程级可验证/可维护/可调试
    - 与产业工具链协同工作流
  style: body; #1A1A1A; bullets.

- id: roadmap3
  type: shape
  bbox: 67,20,26,44
  z: content
  content: roadmap card
  style: fill #F8F9FA; border 1.5px #D1D5DB; radius 14px.
- id: roadmap3_text
  type: text
  bbox: 69,22,22,40
  z: content
  content: |
    **长期：开源生态 + 校企合作验证闭环**
    - 更多校企合作项目验证
    - 教程/文档/社区治理体系
    - 持续迭代形成事实标准
  style: body; #1A1A1A; bullets.

- id: platform_diagram
  type: diagram
  bbox: 7,66,86,22
  z: content
  content: |
    Target system diagram:
    Center big rounded rectangle labeled “Platform（开源工具链平台）”.
    Three outward connectors to smaller boxes: “Apps”, “Architectures”, “Toolchains”.
    Under Platform add tiny labels: “IR/接口 | 评测回归 | 模块库 | 工程能力”.
  style: stroke #2563EB 2px; fills #F8F9FA; text #1A1A1A.
- id: bottom_line
  type: text
  bbox: 7,90,86,6
  z: callout
  content: "闭环路线：整合 → 增强 → 落地 → 验证 → 生态"
  style: pull_quote; #2563EB; centered; bold.

Assets:
- none

## Slide 8: 履历与承诺｜证据墙 + 时间线 + 国情表决心

Layout decision:
- 左：证据墙（图标+短条，最多10条）；右：2019→2026 时间线；底部 pull-quote 作为价值观/表决心收束。

Element spec:
- id: title
  type: title
  bbox: 7,6,86,10
  z: content
  content: "履历与承诺：以开源与落地推动我国集成电路关键能力提升"
  style: headline; #1A1A1A.

- id: wall
  type: shape
  bbox: 7,20,50,56
  z: content
  content: evidence wall card
  style: fill #F8F9FA; border 1.5px #D1D5DB; radius 14px.
- id: wall_text
  type: bullets
  bbox: 9,22,46,52
  z: content
  content: |
    - 竞赛：EDAthon 2020 Second Place；EDAthon 2021 Third Place
    - 专利：202310967153.2（公布/实审）；2025100662753（受理）
    - 奖学金/荣誉：院士奖学金（2019）；深交所奖学金（2020）；北大三好学生
    - 教程：ASP-DAC 2025/2026；DATE 2025；ASPLOS 2025；ISEDA 2025（共同主讲/组织）
    - 产学研：国家重点研发计划相关课题；校企合作落地；PTO开源贡献关键模块
  style: body bullets; #1A1A1A; add small line icons per bullet (trophy/patent/medal/mic/handshake) in #2563EB.

- id: timeline
  type: diagram
  bbox: 60,20,33,56
  z: content
  content: |
    Horizontal timeline 2019→2026 with 6–7 nodes:
    2019-2020（奖学金/荣誉）
    2021-2022（HECTOR 核心开发→ICCAD’22）
    2022-2024（Cement 方法体系→FPGA’24）
    2023-2025（APS 开源协同框架→ICCAD’25 Invited）
    2024-2026（ISAMORE ASPLOS’26 / Cayman DAC’25 / 教程推广）
    Use dots + short labels; keep clean; avoid clutter.
  style: line #D1D5DB; key nodes accent #2563EB.

- id: pledge
  type: callout
  bbox: 7,80,86,16
  z: callout
  content: |
    面向国家集成电路产业自主可控与高层次紧缺人才培养需求，持续在“工具链生产力”这一关键环节攻关与落地；
    以开源协同汇聚社区力量，以校企合作验证闭环推动技术转化，为我国高能效计算与芯片设计方法体系建设贡献长期力量。
  style: pull_quote block; left 6px blue bar (#2563EB); fill #FFFFFF; border 1.5px #D1D5DB; radius 14px; text #1A1A1A.

Rendering notes:
- 禁止出现任何坐标/百分比角标、bbox 边框或调试文字。
- 证据墙与时间线保持“杂志信息图”克制：图标小、信息密度高但不拥挤；优先对齐与留白。

Assets:
- none
