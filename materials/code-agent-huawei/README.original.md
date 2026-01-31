# Agentic Coding Tool Experience

This material is used to generate a slide to share my experience using agentic coding tools. 

Requirements: the final slides shoudl be in Chinese for most contents. But for terms, such as "agentic coding tool", we should still use English to guarantee precise meaning. 

## Background

What is agentic coding tool? A class of domain-specific LLM agents.

### So first, what is an LLM agent?

An LLM agent is an AI system that utilizes a Large Language Model (LLM) as its "brain" to reason through complex problems, plan, and autonomously execute multi-step tasks. Unlike chatbots that provide direct, single-turn responses, agents use tools, memory, and reasoning to achieve specific goals, such as interacting with APIs or navigating software workflows. 

Key Characteristics and Components:

- Reasoning & Planning: Agents break down complex objectives into smaller, manageable subtasks, using techniques like Chain-of-Thought (CoT) to decide on actions.
- Tool Use: Agents can invoke external tools (APIs, calculators, code interpreters, databases) to retrieve live data or execute actions.
- Memory Management:
  - Short-term memory: Manages the context of the current conversation or immediate, ongoing steps.
  - Long-term memory: Stores information from past interactions over time, enabling the agent to learn from experience.

[Figure](llm-agent.jpg) shows an illustration, which presents how LLM agent compares to traditional agent.

### Now, what is an agentic coding tool?

Let's see how Anthropic and OpenAI introduce their products.

#### **Claude Code (CC)**:

Claude Code, Anthropic’s agentic coding tool that lives in your terminal and helps you turn ideas into code faster than ever before.

What Claude Code does for you:

- Build features from descriptions: Tell Claude what you want to build in plain English. It will make a plan, write the code, and ensure it works.
- Debug and fix issues: Describe a bug or paste an error message. Claude Code will analyze your codebase, identify the problem, and implement a fix.
- Navigate any codebase: Ask anything about your team’s codebase, and get a thoughtful answer back. Claude Code maintains awareness of your entire project structure, can find up-to-date information from the web, and with MCP can pull from external data sources like Google Drive, Figma, and Slack.
- Automate tedious tasks: Fix fiddly lint issues, resolve merge conflicts, and write release notes. Do all this in a single command from your developer machines, or automatically in CI.

We'll talk about detailed usage later. Let's first understand how CC works.

**How CC works?**

When you give Claude a task, it works through three phases: gather context, take action, and verify results. This is illustrated by [figure](cc-agentic-loop.svg).

The loop adapts to what you ask. A question about your codebase might only need context gathering. A bug fix cycles through all three phases repeatedly. A refactor might involve extensive verification. Claude decides what each step requires based on what it learned from the previous step, chaining dozens of actions together and course-correcting along the way.

You’re part of this loop too. You can interrupt at any point to steer Claude in a different direction, provide additional context, or ask it to try a different approach. Claude works autonomously but stays responsive to your input.

The agentic loop is powered by two components: models that reason and tools that act. Claude Code serves as the agentic harness around Claude: it provides the tools, context management, and execution environment that turn a language model into a capable coding agent.

**The most important part: Tools**

Tools are what make Claude Code agentic. Without tools, Claude can only respond with text. With tools, Claude can act: read your code, edit files, run commands, search the web, and interact with external services. Each tool use returns information that feeds back into the loop, informing Claude’s next decision.

The built-in tools generally fall into four categories, each representing a different kind of agency.

| Category	| What Claude can do |
| --- | --- |
| File operations |	Read files, edit code, create new files, rename and reorganize|
|Search |	Find files by pattern, search content with regex, explore codebases |
| Execution | 	Run shell commands, start servers, run tests, use git |
| Web	| Search the web, fetch documentation, look up error messages |
| Code intelligence |	See type errors and warnings after edits, jump to definitions, find references (requires *code intelligence* (LSP) plugins) |


These are the primary capabilities. Claude also has tools for spawning subagents, asking you questions, and other orchestration tasks.

Claude chooses which tools to use based on your prompt and what it learns along the way. When you say “fix the failing tests,” Claude might:

- Run the test suite to see what’s failing
- Read the error output
- Search for the relevant source files
- Read those files to understand the code
- Edit the files to fix the issue
- Run the tests again to verify

Each tool use gives Claude new information that informs the next step. This is the agentic loop in action.


Extending the base capabilities: The built-in tools are the foundation. You can extend what Claude knows with skills, connect to external services with MCP, automate workflows with hooks, and offload tasks to subagents. These extensions form a layer on top of the core agentic loop. We'll go back to this later.


#### And Codex?

Reference: https://openai.com/index/unrolling-the-codex-agent-loop/ 

> Before we dive in, a quick note on terminology: at OpenAI, “Codex” encompasses a suite of software agent offerings, including Codex CLI, Codex Cloud, and the Codex VS Code extension. This post focuses on the Codex harness, which provides the core agent loop and execution logic that underlies all Codex experiences and is surfaced through the Codex CLI. For ease here, we’ll use the terms “Codex” and “Codex CLI” interchangeably.

This article was just released one week ago!

It's open-sourced, but I haven't spare time to learn it. I'm just a 普通用户. I believe most guys are 普通用户.

We look at the agent loop, illustrated in [figure](codex-loop-agent.svg)

To start, the agent takes input from the user to include in the set of textual instructions it prepares for the model known as a prompt.

The next step is to query the model by sending it our instructions and asking it to generate a response, a process known as inference. During inference, the textual prompt is first translated into a sequence of input tokens⁠(opens in a new window)—integers that index into the model’s vocabulary. These tokens are then used to sample the model, producing a new sequence of output tokens.

The output tokens are translated back into text, which becomes the model’s response. Because tokens are produced incrementally, this translation can happen as the model runs, which is why many LLM-based applications display streaming output. In practice, inference is usually encapsulated behind an API that operates on text, abstracting away the details of tokenization.

As the result of the inference step, the model either (1) produces a final response to the user’s original input, or (2) requests a tool call that the agent is expected to perform (e.g., “run ls and report the output”). In the case of (2), the agent executes the tool call and appends its output to the original prompt. This output is used to generate a new input that’s used to re-query the model; the agent can then take this new information into account and try again.

This process repeats until the model stops emitting tool calls and instead produces a message for the user (referred to as an assistant message in OpenAI models). In many cases, this message directly answers the user’s original request, but it may also be a follow-up question for the user.

Because the agent can execute tool calls that modify the local environment, its “output” is not limited to the assistant message. In many cases, the primary output of a software agent is the code it writes or edits on your machine. Nevertheless, each turn always ends with an assistant message—such as “I added the architecture.md you asked for”—which signals a termination state in the agent loop. From the agent’s perspective, its work is complete and control returns to the user.

The journey from user input to agent response shown in the diagram is referred to as one turn of a conversation (a thread in Codex). Though this conversation turn can include many iterations between the model inference and tool calls. Every time you send a new message to an existing conversation, the conversation history is included as part of the prompt for the new turn, which includes the messages and tool calls from previous turns.


**Example**

1. Building the initial prompt. Query => prompt (JSON). [Figure](codex-1st-snapshot.svg)
2. The first turn, append with reply of tool call output. [Figure](codex-2nd-snapshot.svg)
3. The next turn, keep appending! [Figure](codex-3rd-snapshot.svg)

There involves prompt caching for performance considerations, but not we user's concerns!

Let's just move to Practice!

## Practice

### Which CLI/Model(s) to use!

My experience before:

I used Copilot at first, **tab completion**.

Then Cursor, human **review** intensive.

Then Claude Code, 完全沉浸,难以自拔. 幡然醒悟: CC在应付我! 他告诉我他完成了各种feature, 然后代码里全是placeholders.

Now Codex, 真的干活,但不那么听话,并且讲得话也不太好看懂. And, really slow. Have to do human context switch, but this is not a pleasure. I feel comfortable to finish things one by one.

《为什么Codex似乎更强，Claude Code却更流行？》-- 微信公众号
```
今天我们不讲细节，只讲感受。下面融合了我的感受，和技术大牛们的感受。

Claude Code说人话，Codex不说人话。Claude Code提供情绪价值，像是一位善解人意的女程序员，循循善诱。Codex不提供情绪价值，像是一位情商为零的中年黑客，恃才傲物。

Claude就像一个靠谱的硅谷工程师，按时吃药、情绪稳定。Codex 就像一个东欧野路子程序员，不管用什么办法，反正能把活干完 —— Emad （Stability AI 创始人）

Claude Code快得像是没思考，Codex慢得像是怕你怀疑他没思考。

Claude Code的使用体验是真正的Vibe，停不下来。Codex的使用体验像是和谢耳朵打交道，得停下来思考，不够Vibe。

Claude Code适合所有人，Codex只适合少数人。

Codex 语义理解似乎比 Claude Code 更强。Claude 对文件更'尊重'，不容易搞乱代码。但 GPT5.2 确实更强...—— antirez（Redis 作者）

Claude Code适合讨论需求，Codex适合根据既定方案干重活。(《「对需求」这件事，我只用Claude Code》)

用Claude Code做结对编程，用Codex处理定义明确的任务。 —— @affixalex

用Claude Code迭代，用Codex获取建议。Claude是更好的对话模型，它从简短提示推断意图的能力无可匹敌。 —— @KeshTFE

Claude Code是绝对主力，Codex适合跑长时间后台任务 —— @theo (Theo Browne，知名Youtuber、T3 Stack 创始人)
```

我的观点:

我个人无法在真实科研和项目开发中完全使用vibe coding. 我需要至少掌握: feature, architecture, example (隐患也依然存在).

在项目/科研上,情商/对话可能真的不重要,谁真的希望一轮又一轮地跟agent对话呢,一个字都不想多说的啊!


Mix: Claude Code + Codex?
  - Let CC use Codex to find problem (review), give design suggestions, provide coding advice. CC completes the final coding and reports fast. Problem is, CC still fools me in codes...
  - Let CC use Codex to do all things, just let CC acts as a 监军 (就像平时工作中经常需要中译中一样...) -- I think this is good, but at the day I started this practice, our lab's CC is banned.

Alternative: Kimi Code + Codex
  - Also, delegate real tasks to Codex. This is good! 
  - I subscribe Kimi Code's 小杯, not very abundant, even most tasks are done by Codex.

Alternative: Claude Code (Kimi Code model) + Codex

Or, just Codex!

### Case study: EggMind

Egglog: language and engine for EqSAT optimization.

```
(datatype Expr
  (Num i64)
  (Var String)
  (Add Expr Expr)
  (Mul Expr Expr))

; expr1 = 2 * (x * 3)
(let expr1 (Mul (Num 2) (Mul (Var "x") (Num 3))))
; commutativity and associativity for multiplication.
(rewrite (Mul x y) (Mul y x))
(rewrite (Mul x (Mul y z)) (Mul (Mul x y) z))
(run 10)
(extract expr1) ; gives (Mul (Num 6) (Var "x"))
```

For a specific problem, need specific usage of Egglog for scalable (super)optimization. Example is Isaria (distinguished paper of ASPLOS 2025).

My idea: an intelligent engine for superoptimization of the given domain.

How I use Claude to do the research?

#### First commit:
```
misc: initialize project with README.md, egglog as submodule, and reference papers.

Files:
.gitmodules
CLAUDE.md
README.md
docs
 - egglog.pdf
 - guided-eqsat.pdf
 - guided-tensor-lifting.pdf
 - isaria.pdf
 - llm-eqsat.pdf
egglog
```

where README.md is like:

```
## Background

The overall flow of an EqSat optimization is to.. (omitted)

People take interest in EqSat optimization since it theorically explores the complete design space given the rewrite rules. However, (challenge).

**Strategy** is essential for EqSat optimization. It defines how rewrite rules are applied, extract, prune, annotate, etc. We want an intelligent strategy generator? Or an agent? LLM?

## Techniques


We want: an online, adaptive, intelligent (probably LLM) agent for action decisions.
 
For the agent, what are the **actions**? 

**A: Egglog commands?**

Egglog looks ready for LLM. So the problem is how to use LLM here?

### LLM Interfaces

#### Evaluator

Is current state good for the optimization?

1. Run extraction to see the solution quality.
2. Analysis reports.

#### Give LLM what?

1. Evaluator's report
2. *represent current state*
3. ...

#### What is the response? How to use?

1. Egglog code?
2. Template? 

### Engine Skeleton
... (omitted)
```

This is the very start, tell CC basics about future tasks. No coding yet.

#### Start coding

I'll list some prompts examples (not real).

- We want EggMind's infrastructure implemented in Python, but it should interact with egglog, which is in Rust. Give architecture design according to README.md with cross-language problem in mind.
- Use Pixi for environment setup.
- We should create a multi-process architecture, where isolated processes for egglog, LLM, and agent run concurrently and communicate with each other.
- We should have a functor-based system. The engine's agentic loop's processes are all functors to be either fixed or evolved by LLM.
- Write documents for framework architecture and setup.
- Write tests to validate feature implementation.
- ...

Commits:

```
feat: complete core infrastructure with Rust bindings and multiprocess communication
refactor: migrate to class-based Functor system with FixedFunctor
feat: Enhance LLM client with YAML configuration support and error handling
feat: add performance metrics tracking and evolved function logging
feat: add in-memory snapshot/rollback system and agent forking
feat: add customizable metrics system and Makefile for cached builds
docs: add comprehensive Meta-Control system design
feat: implement Meta-Control system for agent orchestration
feat: add LocalMetaCtrl demo and reorganize documentation
feat: add interactive debug visualizer with process tree and message flow
... more
```

This is somehow rapid, but not easy/automatic. I have to discuss with CC very frequently even for some simple, straightforward features. I spend over 10h every day with CC, and the repo 总有向屎山演变的迹象, 而且是不经意间发生, 因为CC不会告诉你他刚写了一个屎山, 他总是汇报很美好的任务完成结论. 

我在这个项目上对CC的使用局限于“频繁对话” + “文档创建”.

#### Even Manuscript Writing

我在paper writing上反而更信任vibe coding, 因为他做的所有事情都是摆在明面上的. 比如EggMind的manuscript就是把所有feature documents喂给CC并经过了多轮对话调优,比如“you should provide motivational example in the background session", "you should write more dicussion about the techniques' rationale, what challenge it tries to solve and how?", "you should look at @pdfs/xxx to learn how to write high-quaility paper to be submitted for xxx conference." 

I got a over-30-page manuscript, but 内容是一团糟. 但这其实已经是论文不错的starting point.

#### 方法与教训

- 纯对话式迭代: 费时间,每隔1分钟要看一次response,再画2分钟写comments,反复重复. 如果卡住了,就得去看代码,发现全是假的...
  - 这里可以画个示意图,随着对话进行(轮数很多),CC汇报的任务进度和实际任务进度的走势(CC汇报的猛涨,同时实际任务进度很低;再用很多轮对话让实际任务进度慢慢追上CC的进度).
- 文档总结: 部分解决遗忘! But, 很多叮嘱只存在在context(conversation)里, 一旦compact,就瞬间丧失无法复原,就错误会重新出现.
- CC让生活很充实..

### planning-with-files + ralph-loop


#### Planning with Files

https://github.com/OthmanAdi/planning-with-files

> Work like Manus — the AI agent company Meta acquired for $2 billion.

A Claude Code plugin that transforms your workflow to use persistent markdown files for planning, progress tracking, and knowledge storage — the exact pattern that made Manus worth billions.

这个解决了对话式迭代的问题,先通过快速对话敲定设计细节后,使用planning-with-files展开多任务的实施计划(一定要有验证!),然后就可以让coding agent自己实现,我们去做项目级并发.

And, it is implemented as a Skill.

**What is a Skill**

https://agentskills.io/home

Agent Skills are folders of instructions, scripts, and resources that agents can discover and use to do things more accurately and efficiently.

Skills solve this by giving agents access to procedural knowledge and company-, team-, and user-specific context they can load on demand. Agents with access to a set of skills can extend their capabilities based on the task they’re working on.

What can Agent Skills enable?

- Domain expertise: Package specialized knowledge into reusable instructions, from legal review processes to data analysis pipelines.
- New capabilities: Give agents new capabilities (e.g. creating presentations, building MCP servers, analyzing datasets).
- Repeatable workflows: Turn multi-step tasks into consistent and auditable workflows.
- Interoperability: Reuse the same skill across different skills-compatible agent products.

At its core, a skill is a folder containing a SKILL.md file. This file includes metadata (name and description, at minimum) and instructions that tell an agent how to perform a specific task. Skills can also bundle scripts, templates, and reference materials.
```
my-skill/
├── SKILL.md          # Required: instructions + metadata
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
└── assets/           # Optional: templates, resources
```

How skills work

Skills use progressive disclosure to manage context efficiently:

- Discovery: At startup, agents load only the name and description of each available skill, just enough to know when it might be relevant.
- Activation: When a task matches a skill’s description, the agent reads the full SKILL.md instructions into context.
- Execution: The agent follows the instructions, optionally loading referenced files or executing bundled code as needed.

This approach keeps agents fast while giving them access to more context on demand.

I find skills at [skillsmp.com](https://skillsmp.com)

How to compose skills?

Let agent do this. For example, in Codex, just write "$skill-creator, create a skill for xxx". 

And, compare skill to some related concepts?

- Hooks: automate workflows around tool events. We can understand this as Skill triggered at some events, like PostToolUse
- Subagents: **own context window** with a custom system prompt, specific tool access, and independent permissions. Several built-in subagents like Explore, and Plan. 我很不喜欢也基本不用subagents, 因为独立的context意味着前文对话信息的丧失! 比如这里的Plan, 我使用的效果总是很差.
- Plugin: 组装一些skills, hooks, agents, 比如/ralph-loop:start/stop, 这里ralph-loop就是一个插件,包含一些skills (start, stop).
- MCP: MCP servers give Claude Code access to your tools, databases, and APIs. 其实不需要自己配置什么,常用的比如github, 会在CC/Codex里内置.

Go back to planning-with-files, let's see a snippet of the SKILL.md: 

```
## File Purposes

| File | Purpose | When to Update |
|------|---------|----------------|
| `task_plan.md` | Phases, progress, decisions | After each phase |
| `findings.md` | Research, discoveries | After ANY discovery |
| `progress.md` | Session log, test results | Throughout session |

## Critical Rules

### 1. Create Plan First
Never start a complex task without `task_plan.md`. Non-negotiable.

### 2. The 2-Action Rule
> "After every 2 view/browser/search operations, IMMEDIATELY save key findings to text files."

This prevents visual/multimodal information from being lost.

### 3. Read Before Decide
Before major decisions, read the plan file. This keeps goals in your attention window.

### 4. Update After Act
After completing any phase:
- Mark phase status: `in_progress` → `complete`
- Log any errors encountered
```

#### Ralph-loop

这个其实解决的是CC不能执行完整个task_plan.md就停止的问题. 

https://ghuntley.com/ralph/

Ralph is a technique. In its purest form, Ralph is a Bash loop.
```bash
while :; do cat PROMPT.md | claude-code ; done
```

Geoff's version is to run prompts again and agains in different contexts. 

Claude Code's Ralph Wiggum Plugin:

Ralph is a development methodology based on continuous AI agent loops. As Geoffrey Huntley describes it: "Ralph is a Bash loop" - a simple while true that repeatedly feeds an AI agent a prompt file, allowing it to iteratively improve its work until completion.

The technique is named after Ralph Wiggum from The Simpsons, embodying the philosophy of persistent iteration despite setbacks.


This plugin implements Ralph using a Stop hook that intercepts Claude's exit attempts:

```
# You run ONCE:
/ralph-loop "Your task description" --completion-promise "DONE"

# Then Claude Code automatically:
# 1. Works on the task
# 2. Tries to exit
# 3. Stop hook blocks exit
# 4. Stop hook feeds the SAME prompt back
# 5. Repeat until completion
```

The loop happens inside your current session - you don't need external bash loops. The Stop hook in hooks/stop-hook.sh creates the self-referential feedback loop by blocking normal session exit.

This creates a self-referential feedback loop where:

The prompt never changes between iterations
Claude's previous work persists in files
Each iteration sees modified files and git history
Claude autonomously improves by reading its own past work in files.

#### Perfect combination: 

/ralph-loop "Run tasks in @plan_task.md. Print <promise>DONE</promise> when all tasks are done" --completion-promise "DONE"

But actually, the planning-with-files skill already provide hooks to achieve the don't stop until completion goal. This looks like a 双保险.

### Case Study: PTO-WSP

OK, 现在我感觉自己猛的可怕.

这个项目是想试验自己Ascend平台算子编程的想法.

https://github.com/uv-xiao/pto-wsp


问题: pto-isa项目能够编程一个kernel. 但我们现在想编程多个kernel执行的runtime.

我先给CC提供了:
- pto-isa的仓库
- 汪超师兄提供的需求文档 〈- 这个很重要
- 因为我个人觉得USL (user-scheduling language)是编程runtime的正确打开方式,所以把Halide, TVM, 以及更多论文的pdf直接提供给CC. 
- 同时,我觉得flashinfer的JIT思路是正确的,所以相关的代码和论文也都给CC.
- 我还希望实现megakernel!也都给!
- 毕竟是面向Ascend平台,我把CANN的一些文档也喂给CC.

我得到了:
```
01_flashinfer.md    05_ascend_hw.md                  09_sparsetir.md   13_pto_isa_lh.md  17_dam.md
02_gpu_patterns.md  06_megakernels.md                10_relax.md       14_pto_isa_wc.md
03_pl_design.md     07_cuda_streams_workstealing.md  11_flashinfer.md  15_allo.md
04_pto_isa.md       08_tvm.md                        12_pypto.md       16_dato.md
```

现在,我只要求CC帮我生成满足需求文档的设计,不Coding (反正CC也挺难写对的). 然后我浪费了接近一周的时间得到了7个我很满意的版本:
```
v1: raw task graph, 无动态循环支持
v2: task gen (thread 0) + task graph execution (thread 1-N). 其实这个和目前pto-runtime的设想就很相似了,但是并不满足我的预期. 仍然是动态任务生成,而非JIT,对dispatch的编程弱.
v3-v4: Plan-Descriptor-Execute. 我要求对JIT,给的例子是flashinfer,导致过拟合. 任务图支持直接没了
v5: task graph + dispatch-issue. 通过区分dispatch-issue把JIT和task graph结合. 但完全没提供对dispatch-issue的编程能力. CC还把之前的USL的东西全扔了,退回task graph了.
v6: 仍然是task graph... 加了一套基于event handler callback的编程接口用于dispatch-issue编程. 太难受. 我给了一套详细的直接指明方案的comments
v7: Workload-Schedule. 比较符合我的预期了, 结合JIT+task graph的可编程runtime, workload自带依赖分析. 把event-driven模型换成了CSP模型,这是个人审美. 但这个版本的CSP和workload spec竟然是割裂的两套,并且从TVM家族中集成了很多没用的特性.
v8: 有机合并CSP进入workload,删减特性. 得到比较满意的版本. 使用ralph-loop + planning-with-files完成prototyping代码,跑通CPU Sim. 
v9: 这时看到了廖博的版本,强调python binding.向其靠拢. 得到python+CppIR+codegen的版本. 在这个版本开始使用Codex. 初用起来体验并不好,无法像CC一样ralph-loop+planning-with-files快速出代码,因为codex没有hook机制,ralph-loop是残废的. 并且Python-CppIR的bridge并不trivial. 但在codex比较严厉的执行检查下,feature的文档和实现基本对齐. Prompt: 
  - Is the problems in docs/implementation_review.md all resolved? Do the review again
  - $create-plan create plans to solve the remaining real gaps . docs/v9_fix_plan.md and docs/v9_fix_tracker.md shoudl be summarized into docs/task_plan.md . And we should put the new plan in renewed docs/v9_fix_plan.md and docs/v9_fix_tracker.md for tracking
  - Write the detailed, fully clarified plan to docs/v9_fix_plan.md (renew from empty) and the task tracking to docs/v9_fix_tracker.md (also renewed).
  - $ralph-loop start doing and complete tasks in docs/v9_fix_tracker.md .
  - Review the implementation again per docs/implementation_review.md , is the features in docs/features.md well implemented? Update the related documents to reflect the up-to-date status.

v10 (in plan): 汪超师兄的pto-runtime项目解耦了npu目标代码生成,计划将PTO-WSP与其集成. Prompt: We are working on a decoupled pto-runtime, cloned in @references/pto-runtime. For v10, instead of migrating backend architecture from pto-isa-lh, we actually should target the pto-runtime. We should do detailed analysis on the pto-runtime. Indeed, the upcoming features of pto-runtime is previewed in docs/future/pto-runtime-task-buffer.md, we should take it into consideration. We should also think about how to
integrate pto-wsp with pto-runtime (submodule?). Write down all note and update documents under @docs/future
```

这个过程中我也尝试了Kimi Code + Codex, 这里codex也是skill (怎么创建? 让agent自己创建就好). 在AGENTS.md里写:

```
## Important: Delegate to Codex (even for other agents)

This repo is designed so **all concrete work is executed through Codex** (by the codex Skill).
```

Kimi Code的界面和操作还是比较舒服的,甚至有GUI.但还是没有Hook等机制,所以不是CC一样合格的监军. 所以最好还是让CC调Kimi API:

```
export ANTHROPIC_BASE_URL=https://api.kimi.com/coding/
export ANTHROPIC_API_KEY=sk-kimi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx # Fill in the API Key generated on the membership page

claude
```

然而我其实现在更习惯直接用Codex了. 虽然他语言晦涩,但也基本习惯了,而且codex自己的planning模式也好用起来了. 而加一层Kimi Code,他经常会自作主张,不好好传递任务,导致额度不够用,任务完成的也不好.

## Haven't Covered

### Superpowers

Superpowers is a complete software development workflow for your coding agents, built on top of a set of composable "skills" and some initial instructions that make sure your agent uses them.

It starts from the moment you fire up your coding agent. As soon as it sees that you're building something, it doesn't just jump into trying to write code. Instead, it steps back and asks you what you're really trying to do.

Once it's teased a spec out of the conversation, it shows it to you in chunks short enough to actually read and digest.

After you've signed off on the design, your agent puts together an implementation plan that's clear enough for an enthusiastic junior engineer with poor taste, no judgement, no project context, and an aversion to testing to follow. It emphasizes true red/green TDD, YAGNI (You Aren't Gonna Need It), and DRY.

Next up, once you say "go", it launches a subagent-driven-development process, having agents work through each engineering task, inspecting and reviewing their work, and continuing forward. It's not uncommon for Claude to be able to work autonomously for a couple hours at a time without deviating from the plan you put together.

There's a bunch more to it, but that's the core of the system. And because the skills trigger automatically, you don't need to do anything special. Your coding agent just has Superpowers.

```
The Basic Workflow

brainstorming - Activates before writing code. Refines rough ideas through questions, explores alternatives, presents design in sections for validation. Saves design document.

using-git-worktrees - Activates after design approval. Creates isolated workspace on new branch, runs project setup, verifies clean test baseline.

writing-plans - Activates with approved design. Breaks work into bite-sized tasks (2-5 minutes each). Every task has exact file paths, complete code, verification steps.

subagent-driven-development or executing-plans - Activates with plan. Dispatches fresh subagent per task with two-stage review (spec compliance, then code quality), or executes in batches with human checkpoints.

test-driven-development - Activates during implementation. Enforces RED-GREEN-REFACTOR: write failing test, watch it fail, write minimal code, watch it pass, commit. Deletes code written before tests.

requesting-code-review - Activates between tasks. Reviews against plan, reports issues by severity. Critical issues block progress.

finishing-a-development-branch - Activates when tasks complete. Verifies tests, presents options (merge/PR/keep/discard), cleans up worktree.
```

这个看起来太强大复杂了,我个人是不喜欢功能过剩的. 但我后续也会实测一下.

### Parallel Vibe Coding

我觉得这个也是重要的,但我还没有到一个项目多个特性并发.我是多个项目的并发.之后会尝试这个.

Run parallel Claude Code sessions with Git worktrees

Suppose you need to work on multiple tasks simultaneously with complete code isolation between Claude Code instances.

```text
1. Understand Git worktrees

Git worktrees allow you to check out multiple branches from the same repository into separate directories. Each worktree has its own working directory with isolated files, while sharing the same Git history. Learn more in the official Git worktree documentation.

2. Create a new worktree

# Create a new worktree with a new branch 
git worktree add ../project-feature-a -b feature-a

# Or create a worktree with an existing branch
git worktree add ../project-bugfix bugfix-123
This creates a new directory with a separate working copy of your repository.

3. Run Claude Code in each worktree

# Navigate to your worktree 
cd ../project-feature-a

# Run Claude Code in this isolated environment
claude

4. Run Claude in another worktree

cd ../project-bugfix
claude

5. Manage your worktrees

# List all worktrees
git worktree list

# Remove a worktree when done
git worktree remove ../project-feature-a


Tips:
Each worktree has its own independent file state, making it perfect for parallel Claude Code sessions
Changes made in one worktree won’t affect others, preventing Claude instances from interfering with each other
All worktrees share the same Git history and remote connections
For long-running tasks, you can have Claude working in one worktree while you continue development in another
Use descriptive directory names to easily identify which task each worktree is for
Remember to initialize your development environment in each new worktree according to your project’s setup. Depending on your stack, this might include:
JavaScript projects: Running dependency installation (npm install, yarn)
Python projects: Setting up virtual environments or installing with package managers
Other languages: Following your project’s standard setup process
```

### ClawdBot/MoltBot/OpenClaw

我玩ClawdBot把组里CC搞封号了...

这东西名字天天变,打算再等稳定下.

之后等国内Channel和模型适配(MiniMax在国内用问题还很多)好一些,蹲些靠谱的教程再来尝试.

我对这个比较期待的用处,是能用消息通知我某个repo的任务完成了,需要我的审批. 化身人形infra开启work stealing!

## Personal Practice Guidelines

1. Write a README.md.
2. Let agent to create the file structures.
3. Download/clone reference papers/repos to analyze and generate reports.
4. Install/create useful skills. (This can be done whenever during the development).
5. Discuss design/features with agent.
6. Write down detailed plans to execute and track.
7. Do version iterations.


