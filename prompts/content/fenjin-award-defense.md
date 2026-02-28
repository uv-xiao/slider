# Deck: 奋进奖学金答辩｜敏捷芯片设计与软硬件协同工具链（8页）

Context:
- Audience: 奋进奖学金评审委员（集成电路方向）
- Use case: live talk（答辩PPT，强调叙事与可视化证据）
- Target length: 8 slides（不严格卡时长，优先质量与信息可读性）
- Language: 中文

Rules:
- 一页一个主旨（intent）。
- No silent dropping：`materials/fenjin-award-defense/source_ppt_pages.md` 中的逐页要点都要在“Must include”里落位。
- 第2页的 Apple/ISSCC 图片仅作“理解与重绘基准”，最终以“重绘信息图”呈现，避免拼贴与拥挤。

## Page 1: 封面｜一句话定主线

Intent:
- 用 1 句把“产业痛点→我的主线→工具链闭环”立起来，让评委提前知道你在解决什么。

Must include:
- 标题：奋进奖学金答辩
- 署名：肖有为｜北京大学集成电路学院｜奖励方向：1. 集成电路设计
- 主线短句：算力紧缺 → 生产力不足 → 协同闭环与开源工具链

Suggested representation:
- Primary: 标题页（大标题+副标题+一行主线）
- Optional: “Chip + Compiler + Toolchain”极简图标组（线性图标）

Assets:
- 无（图标可在 styled 阶段指定为自绘矢量风格）

Notes / TODO:
- 无

## Page 2: 产业痛点｜Apple ISSCC 2026「三图证据链」重绘信息图

Intent:
- 用权威背书把“生产力是瓶颈、必须全栈协同优化”讲成产业共识，为后续三类能力铺垫。

Must include:
- 标题：产业共识：复杂度与产品线扩张倒逼“全栈协同优化”（Apple｜ISSCC 2026）
- 三张证据卡（每卡=重绘小图+一句结论）：
  1) 复杂度↑（晶体管数趋势） vs 人才供给（EE学位）不匹配 → 工具链生产力成瓶颈
  2) Apple-designed processors 产品家族/层级扩张 → 协同与适配成本飙升，必须框架化/可复用
  3) Full-stack engineering（应用→器件） → 优化必须跨栈，需端到端闭环与可重定向编译
- 底部结论横幅：把“协同优化”工具链化，才能把生产力变成系统能力。
- 来源脚注：`https://tspasemiconductor.substack.com/p/apple-empowering-the-next-wave-of`

Suggested representation:
- Primary: 信息图（白底 editorial infographic：三张“证据卡”纵向堆叠，统一视觉语言）
- Optional: 右上角小“Source tag”而非大截图（避免照片感）

Assets:
- 原图（仅用于理解与重绘基准；PPT中建议使用重绘版）：
  - `materials/fenjin-award-defense/assets/apple_fig1.jpg`（talent pipeline vs transistor count）
  - `materials/fenjin-award-defense/assets/apple_fig2.jpg`（Apple-designed application processors 产品线扩张）
  - `materials/fenjin-award-defense/assets/apple_fig3.webp`（Full-stack engineering）

Notes / TODO:
- 重绘时不需要精确数值，强调趋势与“gap/expansion/across-stack”三点即可。

## Page 3: 总览｜三类工具链能力对应三类产业痛点

Intent:
- 用最干净的结构把你的所有工作“归类”，避免堆名词；只给三类能力标签（A/B/C），细节放到后面展开。

Must include:
- 标题：我的总体贡献：三类“工具链能力”对应三类产业痛点
- 三行对照（痛点→能力→意义）：
  - 协同闭环痛点：应用迭代快、协同跟不上 → 可重定向编译 + 端到端协同闭环 → 协同变成可复用框架能力
  - 前端生产力痛点：RTL抽象低、效率与可靠性受限 → 事务/时序语义抽象 + 规则化描述 + AI辅助方法学 → 提产、可组合、可验证
  - 综合优化痛点：优化割裂、质量与扩展性难兼得 → 多层IR方法学 + e-graph联合决策（选择/调度一体化）→ 系统化、可扩展
- 底部闭环小图：应用→IR/编译→定制→前端实现抽象→综合优化→评测/落地→回到应用

Suggested representation:
- Primary: 三行对照表 + 细条闭环图（信息密度低、可扫读）

Assets:
- 无（闭环图在 styled 阶段自绘）

Notes / TODO:
- 本页禁止出现具体项目名（APS/Cement/HECTOR 等），只出现 A/B/C 三类标签。

## Page 4: A类展开｜协同闭环 + 自动定制（APS/Aquas/Clay/ISAMORE/Cayman）

Intent:
- 讲清“如何把协同优化做成工具链能力”：MLIR统一接口 + e-graph可重定向编译 + 定制（指令/微架构/加速器）+ 端到端评测闭环。

Must include:
- 标题：A类能力：协同闭环与自动定制（敏捷专用化的工具链化）
- 中心“闭环框架图”五段：Workload → MLIR IR → E-Graph Opt → Specialization → Eval&Loop
- 数字卡：`9.27×`（端到端协同优化结果之一）
- 三张成果卡（各2行：做什么/意义）：
  1) 端到端协同：框架化能力（APS + Aquas）
  2) 指令/微架构定制：可复用/自动化（Clay + ISAMORE）
  3) 自动加速器生成：纳入闭环（Cayman）
- 证据栏（会议’年份）：APS（ICCAD’25 Invited）｜Clay（ICCAD’25）｜ISAMORE（ASPLOS’26）｜Cayman（DAC’25）｜Aquas（arXiv’25）

Suggested representation:
- Primary: 中央框架图 + 右侧卡片 + 底部证据栏

Assets:
- 无（框架图在 styled 阶段自绘）

Notes / TODO:
- 强调“协同闭环/可重定向/可复用”，避免把重点讲成单点性能。

## Page 5: B类展开｜硬件前端生产力 + AI辅助方法学（Cement/OriGen/LLM评测）

Intent:
- 把“前端提产”讲成方法学：语义化抽象→规则化描述→AI辅助与评测闭环；强调“工程生产力”，不讲性能。

Must include:
- 标题：B类能力：把硬件前端从“低层RTL”提升为“语义化、可组合、可评测”
- 语义阶梯图（3阶）：RTL → 事务/时序语义 → AI辅助+评测闭环
- 三块卡片（做法→意义→证据）：
  1) 语义抽象：事务/周期级语义提升抽象与效率；证据（FPGA’24）+（arXiv’25：Cement2）
  2) 规则化描述：Rust时序语义规则化（cmt2）；证据（LATTE’25 workshop）
  3) AI辅助与评测：OriGen + FPGA’25系统比较LLM vs HLS；证据（ICCAD’24）+（FPGA’25）

Suggested representation:
- Primary: 上方阶梯图 + 下方三卡

Assets:
- 无（阶梯图与卡片在 styled 阶段自绘）

Notes / TODO:
- “AI辅助RTL生成”必须配“评测边界认知”，避免显得空泛。

## Page 6: C类展开｜综合方法学 + 联合决策优化（HECTOR + SkyEgg）

Intent:
- 讲清“为什么需要方法学框架”以及“联合选择/调度的系统性收益”，用硬指标收束。

Must include:
- 标题：C类能力：统一方法学的综合框架 + 联合决策优化（选择×调度）
- 左侧 HECTOR 方法学三点：多层IR｜可扩展｜可复用（证据：ICCAD’22）
- 右侧联合优化一句话：e-graph 统一表示变换与实现选择，“选择+调度”联合决策
- 硬指标：平均 `3.01×`｜最高 `5.22×`（vs Vitis HLS）
- 自绘两层示意图（等价变换空间→联合决策），配一个小柱状图（Vitis / Ours avg / Ours best）
- 底部证据栏：HECTOR（ICCAD’22）｜联合选择/调度（arXiv’25）

Suggested representation:
- Primary: 左方法学要点 + 右示意图+指标

Assets:
- 无（示意图在 styled 阶段自绘）

Notes / TODO:
- 右侧示意图要“极简可讲”，避免数学细节。

## Page 7: 未来计划 ONLY｜框架整合、商业级落地、开源与校企验证闭环

Intent:
- 只讲未来三年规划：整合→增强→落地→验证→生态；不回顾既有经历。

Must include:
- 标题：未来三年：把“敏捷芯片设计与软件生态适配”做成可落地的开源平台
- 三段路线图（近期/中期/长期，各3条）：
  - 近期：统一IR接口｜标准化评测回归｜可复用模块库
  - 中期：复杂多元架构自动适配｜工程级可验证可维护可调试｜与产业工具链协同
  - 长期：更多校企验证｜教程/文档/社区治理｜持续迭代形成事实标准
- 目标系统图：Platform（中心）+ Apps/Architectures/Toolchains 三个接口

Suggested representation:
- Primary: 路线图（三段分区）+ 目标系统图

Assets:
- 无（系统图在 styled 阶段自绘）

Notes / TODO:
- 此页语气宏大但要具体（每条都能落地成“模块/接口/基准/工程能力/合作验证”）。

## Page 8: 履历与升华｜证据墙 + 时间线 + 国情表决心

Intent:
- 用“证据墙+时间线”快速覆盖履历（全取），最后用国情/长期投入意愿收束。

Must include:
- 标题：履历与承诺：以开源与落地推动我国集成电路关键能力提升
- 左侧证据墙（最多10条，图标+短条）：
  - 竞赛：EDAthon 2020 Second Place；EDAthon 2021 Third Place
  - 专利：202310967153.2（公布/实审）；2025100662753（受理）
  - 奖学金/荣誉：院士奖学金（2019）；深交所奖学金（2020）；北大三好学生
  - 教程：ASP-DAC 2025/2026；DATE 2025；ASPLOS 2025；ISEDA 2025（共同主讲/组织）
  - 产学研：国家重点研发计划相关课题；校企合作落地；PTO开源贡献关键模块
- 右侧时间线（2019→2026，6-7节点）
- 底部表决心（2-3句，坚定、对齐国情）：自主可控、紧缺人才、开源协同、校企闭环、长期投入

Suggested representation:
- Primary: 证据墙（徽章/图标列表）+ 时间线 + 结尾 pull-quote

Assets:
- 可选：在 styled 阶段用“证据图标”替代真实证书照片，保持 editorial infographic 风格。

Notes / TODO:
- 证据墙的文字要对齐 `docs/材料逐项填写内容与PPT逐页内容.md` 的口径（Second Place/Third Place、专利号、会议名）。

