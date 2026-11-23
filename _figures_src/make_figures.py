#!/usr/bin/env python3
"""Generate the inline-SVG figures for the post "What Is Left for Humans in Algorithm Design?".

Run from the repo root:  python3 _figures_src/make_figures.py
Writes _includes/figures/{stages,lifecycle,domains,trends}-{en,zh}.svg
Styling (light + dark) lives in assets/css/blog.css under the `bf-` classes.
Every data point comes from the sources listed under "Sources for the figures" in the post.
"""
import math
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "_includes" / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def t(x, y, s, cls="", anchor="start"):
    c = f' class="{cls}"' if cls else ""
    return f'<text x="{x:g}" y="{y:g}"{c} style="text-anchor:{anchor}">{s}</text>'


def svg_open(w, h, lang, key, title, desc, extra_cls=""):
    return [f'<svg class="bf {extra_cls}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{key}t-{lang} {key}d-{lang}" xmlns="http://www.w3.org/2000/svg">',
            f'<title id="{key}t-{lang}">{title}</title><desc id="{key}d-{lang}">{desc}</desc>']


# ── data ─────────────────────────────────────────────────────────────────────
STAGES = [
    # en name, en subtitle, zh name, zh subtitle, AI-owned layers (from bottom), en human, zh human, status
    ("Tuning", "AI tunes parameters", "调参", "AI 调整参数", 1, ["the algorithm"], ["算法"], ""),
    ("Components", "AI designs components", "部件设计", "AI 设计算法部件", 2, ["the framework"], ["算法框架与流程"], ""),
    ("Agentic design", "AI improves &amp; fuses", "智能体设计", "AI 改进与融合算法", 3, ["evaluation &amp;", "knowledge"], ["评估手段与", "知识参考"], ""),
    ("Autonomous", "AI solves end-to-end", "自主求解", "AI 端到端解决问题", 4, ["the goal"], ["目标"], "emerging"),
    ("Creation", "AI sets its own goals", "自主创造", "AI 自定目标、持续创造", 5, ["almost nothing"], ["几乎无需提供"], "future"),
]
LAYERS_EN = ["Goal", "Evaluation &amp; knowledge", "Framework &amp; procedure", "Components", "Parameters"]
LAYERS_ZH = ["目标", "评估与知识", "算法框架与流程", "算法部件", "参数"]

LIFECYCLE = [
    # year, en name, zh name, refs, conception, design, evaluation, en note, zh note
    ("2009–16", "Algorithm configuration", "算法配置", "2–5", "H", "H", "H",
     "Humans design the algorithm and supply its parameter space, instances and cost metric; AI only picks parameter values.",
     "人提供带参数的求解器、实例和代价指标；AI 选择参数值。"),
    ("2019", "Learned branching", "学习分支策略", "7", "H", "S", "H",
     "A network learns the branching rule inside a human-built branch-and-bound solver.",
     "神经网络在人搭建的分支定界求解器内学习分支规则。"),
    ("2019", "Neural solver", "神经求解器", "49", "H", "S", "H",
     "Humans design the network and training; the model learns a construction policy for routing problems.",
     "人设计网络与训练方式；模型学习路径问题的构造策略。"),
    ("2024", "EoH", "EoH", "12", "S", "A", "H",
     "Humans choose the problem and give the function signature, task description and fitness instances; the LLM explicitly proposes and evolves algorithmic ideas (\u201cthoughts\u201d) alongside the code.",
     "人选定问题，给出函数签名、任务描述和评估实例；LLM 显式地提出并演化算法思路（“thought”），与代码一同演化。"),
    ("2024", "OptiMUS", "OptiMUS", "18", "H", "A", "S",
     "Human gives the problem in natural language; the agent formulates, codes, debugs and checks.",
     "人用自然语言描述问题；智能体建模、写代码、调试并检查。"),
    ("2024", "The AI Scientist", "AI Scientist", "28", "S", "A", "S",
     "Human provides a code template and 1–2 seed ideas; an LLM reviewer evaluates.",
     "人提供代码模板和 1–2 个种子想法；由 LLM 审稿人评估。"),
    ("2025", "The AI Scientist-v2", "AI Scientist-v2", "39", "S", "A", "S",
     "Humans give a broad topic and pick ideas and the final paper; AI writes ideas, code and paper; an LLM reviewer evaluates.",
     "人给出大致主题并挑选想法与最终论文；AI 生成想法、代码和论文；由 LLM 审稿人评估。"),
    ("2025", "AlphaEvolve", "AlphaEvolve", "15", "H", "A", "H",
     "User supplies an evaluate function and a complete (possibly rudimentary) initial program.",
     "用户提供 evaluate 函数和一个完整（可以很粗糙）的初始程序。"),
    ("2025", "Darwin Gödel Machine", "Darwin Gödel Machine", "43", "H", "A", "H",
     "The agent rewrites its own code; humans fix the objective (coding benchmarks) and the compute budget.",
     "智能体改写自身代码；目标（代码基准）与算力预算由人设定。"),
    ("2025", "ShinkaEvolve", "ShinkaEvolve", "38", "H", "A", "H",
     "Human supplies an initial program with evolve markers and an evaluate script returning a score.",
     "人提供带演化标记的初始程序，以及返回分数的评估脚本。"),
    ("2025", "DeepScientist", "DeepScientist", "42", "S", "A", "H",
     "Agent proposes and tests thousands of ideas on frontier tasks chosen by humans, against human benchmarks.",
     "智能体在人选定的前沿任务上提出并验证数千个想法，以人的基准衡量。"),
    ("2025", "AlphaResearch", "AlphaResearch", "30", "S", "A", "S",
     "AI proposes ideas screened by a learned reviewer; problems are human-defined.",
     "AI 提出想法并由学习到的审稿模型筛选；问题由人定义。"),
    ("2026", "Evolution of Benchmark", "Evolution of Benchmark", "31", "H", "-", "S",
     "The LLM evolves the benchmark programs themselves; humans set the objectives.",
     "LLM 演化基准测试程序本身；目标由人设定。"),
]

DOMAINS = [
    # en, zh, frontier stage, early-signal stage, deployed/shipped stage ("na" = not applicable),
    # en humans-provide, zh, en production note, zh production note
    ("MIP solver components", "MIP 求解器部件", 2, 3, 2,
     "solver, target component, instances", "求解器、目标部件、实例",
     "CPLEX, FICO Xpress", "CPLEX、FICO Xpress"),
    ("Optimization modeling", "优化建模", 3, 4, 3,
     "problem in words, reference answers", "文字描述的问题、参考答案",
     "Microsoft OptiGuide, OptiMind", "微软 OptiGuide、OptiMind"),
    ("CO heuristics", "组合优化启发式", 3, None, 3,
     "evaluator, instances, code template", "评估器、实例、代码模板",
     "Google Borg scheduling", "Google Borg 调度"),
    ("Industrial operations", "工业运营", 3, None, 3,
     "seed algorithm, objective, data", "初始算法、目标、数据",
     "FM Logistic warehouses", "FM Logistic 仓库"),
    ("Continuous optimization", "连续优化算法", 3, None, 3,
     "benchmark suite and budget", "基准测试集与预算",
     "Lion optimizer, Google Ads", "Lion 优化器、Google 广告"),
    ("ML training & kernels", "机器学习训练与内核", 3, None, 3,
     "kernel, correctness check, timing", "内核代码、正确性检查、计时",
     "Gemini training, Meta", "Gemini 训练、Meta"),
    ("Systems & low-level code", "系统与底层代码", 3, None, 3,
     "correctness checks, simulator", "正确性检查、模拟器",
     "TPU circuits, libc++ sort", "TPU 电路、libc++ 排序"),
    ("Mathematical discovery", "数学发现", 3, None, "na",
     "a verifier for each problem", "每个问题的验证器",
     "n/a", "不适用"),
]

HOURS = [("EoH", 1, "~1 h", "约 1 小时"),
         ("ALE-Agent (AHC058)", 4, "4 h", "4 小时"),
         ("AI Scientist-v2", 15, "up to 15 h", "最长 15 小时"),
         ("Darwin Gödel Machine", 14 * 24, "~2 weeks", "约 2 周")]
RATES = [("AI Scientist", "实验因代码错误失败", "experiments failed (coding errors)", 42.0, "45"),
         ("Kosmos", "结论不准确", "statements not accurate", 20.6, "46"),
         ("o3 on RE-Bench", "奖励作弊", "runs with reward hacking", 30.4, "47"),
         ("GPT-5 on ImpossibleBench", "作弊", "cheating on impossible tasks", 54.0, "48")]


# ── Figure 1: five stages ────────────────────────────────────────────────────
def fig_stages(lang):
    zh = lang == "zh"
    x0, pitch, cw = 190, 114, 102
    top, rp, rh = 72, 38, 28
    W, H = x0 + 5 * pitch, 370
    o = svg_open(W, H, lang, "f1",
                 "AI 参与算法设计的五个阶段" if zh else "Five stages of AI in algorithm design",
                 ("五个设计层次在五个阶段中由 AI 设计或由人提供。AI 负责的层次逐阶段上移：人依次提供算法、算法框架、评估与知识、目标，到第五阶段几乎无需提供。我们目前处于第三阶段。"
                  if zh else
                  "Five layers of an algorithm-design task across five stages. The layers designed by AI move up stage by stage: humans provide the algorithm, then the framework, then evaluation and knowledge, then only the goal, and in Stage 5 almost nothing. We are currently in Stage 3."))
    # soft band behind the current stage
    bx = x0 + 2 * pitch - 8
    o.append(f'<rect x="{bx}" y="2" width="{cw + 16}" height="{H - 4}" class="bf-band"/>')
    for c, (en, sub, zn, zsub, n_ai, hu_en, hu_zh, status) in enumerate(STAGES):
        cx = x0 + c * pitch + cw / 2
        tag = {"emerging": ("正在出现", "emerging")}.get(status)
        o.append(t(cx, 16, f"阶段 {c + 1}" if zh else f"Stage {c + 1}", "bf-small bf-muted", "middle"))
        o.append(t(cx, 38, zn if zh else en, "bf-head bf-head-fit", "middle"))
        if tag:
            o.append(t(cx, 56, tag[0] if zh else tag[1], "bf-note bf-tag", "middle"))
        for r in range(5):
            y = top + r * rp
            if (5 - r) <= n_ai:
                cls = "bf-cell-ai" + (f" bf-{status}" if status else "")
            else:
                cls = "bf-cell-hu"
            o.append(f'<rect x="{x0 + c * pitch}" y="{y}" width="{cw}" height="{rh}" class="{cls}"/>')
        for j, line in enumerate(hu_zh if zh else hu_en):
            o.append(t(cx, 284 + j * 17, line, "bf-label bf-hu-text", "middle"))
    for r, lab in enumerate(LAYERS_ZH if zh else LAYERS_EN):
        o.append(t(x0 - 12, top + r * rp + 19, lab, "bf-label", "end"))
    o.append(t(x0 - 12, 284, "人提供" if zh else "Humans provide", "bf-note bf-hu-text", "end"))
    # boundary between human-provided and AI-designed layers
    pts = []
    for c, st in enumerate(STAGES):
        y = top + rp * (5 - st[4]) - 5
        pts += [(x0 + c * pitch - (7 if c else 10), y), (x0 + c * pitch + cw + 7, y)]
    o.append('<path class="bf-stair" d="M ' + " L ".join(f"{x:g} {y:g}" for x, y in pts) + '"/>')
    # legend, top left
    o.append(f'<rect x="8" y="9" width="12" height="12" class="bf-cell-ai"/>')
    o.append(t(26, 20, "AI 设计" if zh else "Designed by AI", "bf-small bf-muted"))
    o.append(f'<rect x="8" y="30" width="12" height="12" class="bf-cell-hu"/>')
    o.append(t(26, 41, "人提供" if zh else "Provided by humans", "bf-small bf-muted"))
    # timeline
    ay = 334
    o.append(f'<line x1="{x0 - 10}" y1="{ay}" x2="{W - 4}" y2="{ay}" class="bf-axis"/>')
    o.append(f'<path d="M{W - 2},{ay} l-7,-3.5 v7 z" class="bf-axis-head"/>')
    onsets = (["1950 年代", "1980 年代", "2025 年", "约 2030 年", "2030 年以后"] if zh else
              ["from 1950s", "from 1980s", "from 2025", "from ~2030", "after 2030"])
    for c, lab in enumerate(onsets):
        if c:
            x = x0 + c * pitch - 7
            o.append(f'<line x1="{x}" y1="{ay - 4}" x2="{x}" y2="{ay + 4}" class="bf-axis"/>')
        o.append(t(x0 + c * pitch + cw / 2, ay + 22, lab, "bf-small bf-muted", "middle"))
    nx = x0 + 2 * pitch - 7 + (2026 - 2025) / 5 * pitch
    o.append(f'<circle cx="{nx:g}" cy="{ay}" r="4" class="bf-now"/>')
    o.append(t(nx, ay - 10, "现在" if zh else "now", "bf-annot", "middle"))
    o.append("</svg>")
    return "\n".join(o)


# ── Figure 2: who does each phase (Harvey-ball matrix) ───────────────────────
def _ball(cx, cy, level, r=7):
    if level == "-":
        return f'<line x1="{cx - 5}" y1="{cy}" x2="{cx + 5}" y2="{cy}" class="bf-faint-line"/>'
    if level == "A":
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" class="bf-ball-full"/>'
    if level == "S":
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" class="bf-ball-empty"/>'
                f'<path d="M{cx},{cy - r} A{r},{r} 0 0 0 {cx},{cy + r} Z" class="bf-ball-half"/>')
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" class="bf-ball-empty"/>'


def fig_lifecycle(lang):
    zh = lang == "zh"
    cols = ["构思", "设计", "评估"] if zh else ["Conception", "Design", "Evaluation"]
    cxs = [476, 580, 684]
    W, top, pitch = 760, 56, 30
    H = top + pitch * len(LIFECYCLE) + 50
    o = svg_open(W, H, lang, "f2",
                 "设计流程各环节由谁完成" if zh else "Who does each phase of algorithm design",
                 ("13 个代表性系统在构思、设计、评估三个环节中由人、人与 AI 共同或 AI 完成。设计大多由 AI 完成，构思几乎全由人完成，评估在多数系统中仍由人完成。"
                  if zh else
                  "For 13 representative systems, whether conception, design and evaluation are done by humans, shared, or by AI. Design is mostly done by AI, conception almost entirely by humans, and evaluation by humans in most systems."),
                 )
    for c, x in zip(cols, cxs):
        o.append(t(x, 32, c, "bf-colhead", "middle"))
    o.append(f'<line x1="10" y1="{top - 12}" x2="{W - 10}" y2="{top - 12}" class="bf-rule"/>')
    for r, (yr, en, zhn, refs, *ph, note_en, note_zh) in enumerate(LIFECYCLE):
        y = top + r * pitch
        name = zhn if zh else en
        o.append(f'<g class="bf-row"><title>{escape(name)}: {escape(note_zh if zh else note_en)}</title>')
        o.append(f'<rect x="10" y="{y - 13}" width="{W - 20}" height="{pitch}" class="bf-hit"/>')
        o.append(t(14, y + 5, yr, "bf-small bf-muted bf-num"))
        o.append(t(86, y + 5, escape(name), "bf-label"))
        for x, p in zip(cxs, ph):
            o.append(_ball(x, y, p, r=8))
        o.append("</g>")
    ly = top + pitch * len(LIFECYCLE) + 14
    o.append(f'<line x1="10" y1="{ly - 14}" x2="{W - 10}" y2="{ly - 14}" class="bf-rule"/>')
    items = [("A", "AI"), ("S", "人与 AI 共同" if zh else "Shared"), ("H", "人" if zh else "Human")]
    x = 14
    for lv, lab in items:
        o.append(_ball(x + 7, ly + 8, lv, r=7))
        o.append(t(x + 21, ly + 12, lab, "bf-small bf-muted"))
        x += 21 + len(lab) * (13 if zh else 7.5) + 26
    o.append(t(W - 14, ly + 12, "依据各论文要求人提供的内容" if zh else "Based on what each paper requires humans to supply", "bf-note", "end"))
    o.append("</svg>")
    return "\n".join(o)


# ── Figure 3: stage reached per domain (lollipop) + production marker ──────
def fig_domains(lang):
    zh = lang == "zh"
    sx, sp = 318, 50                    # first stage x, stage spacing
    px = sx + 4 * sp + 36               # "in production" column
    W, top, pitch = 760, 66, 34
    H = top + pitch * len(DOMAINS) + 38
    o = svg_open(W, H, lang, "f3",
                 "各领域达到的阶段与实际应用" if zh else "Stage reached in each domain, and production use",
                 ("八个领域中 AI 参与算法设计达到的最高阶段（与图 1 一致），以及 AI 设计的算法已部署或进入软件的情况。多数领域处于第三阶段；每个应用领域都有公开的部署证据，MIP 求解器部件在第二阶段，其余在第三阶段。"
                  if zh else
                  "Highest stage (as in Figure 1) reached by AI in eight domains, and where AI-designed algorithms have been deployed or shipped. Most domains are at Stage 3; every applied domain has some public evidence of deployment, at Stage 2 for MIP solver components and at Stage 3 elsewhere."))
    for i in range(5):
        o.append(t(sx + i * sp, 30, str(i + 1), "bf-colhead", "middle"))
    o.append(t(sx - 22, 30, "阶段" if zh else "Stage", "bf-colhead", "end"))
    o.append(t(px, 30, "已部署或已进入软件" if zh else "Deployed or shipped", "bf-colhead"))
    o.append(f'<line x1="10" y1="{top - 26}" x2="{W - 10}" y2="{top - 26}" class="bf-rule"/>')
    for r, (en, zhn, reached, early, prod, hp_en, hp_zh, pn_en, pn_zh) in enumerate(DOMAINS):
        y = top + r * pitch
        name = zhn if zh else en
        hp = hp_zh if zh else hp_en
        pn = pn_zh if zh else pn_en
        st = (f"阶段 {reached}" + (f"，阶段 {early} 早期信号" if early else "")) if zh else \
             (f"Stage {reached}" + (f"; early Stage-{early} signals" if early else ""))
        if isinstance(prod, int):
            st += (f"；已部署或进入软件：阶段 {prod}（{pn}）" if zh else f"; deployed or shipped at Stage {prod} ({pn})")
        o.append(f'<g class="bf-row"><title>{escape(name)}: {escape(st)}. {("人仍需提供：" if zh else "Humans still provide: ") + escape(hp)}</title>')
        o.append(f'<rect x="10" y="{y - 17}" width="{W - 20}" height="{pitch}" class="bf-hit"/>')
        o.append(t(14, y + 5, escape(name), "bf-label"))
        for i in range(5):
            o.append(f'<circle cx="{sx + i * sp}" cy="{y}" r="2.2" class="bf-tick-dot"/>')
        xr = sx + (reached - 1) * sp
        o.append(f'<line x1="{sx}" y1="{y}" x2="{xr}" y2="{y}" class="bf-stem"/>')
        if early:
            xe = sx + (early - 1) * sp
            o.append(f'<line x1="{xr}" y1="{y}" x2="{xe}" y2="{y}" class="bf-stem-early"/>')
            o.append(f'<circle cx="{xe}" cy="{y}" r="5" class="bf-ball-empty"/>')
        o.append(f'<circle cx="{xr}" cy="{y}" r="5" class="bf-ball-full"/>')
        if isinstance(prod, int):
            xp = sx + (prod - 1) * sp
            o.append(f'<circle cx="{xp}" cy="{y}" r="9.5" class="bf-prod-ring"/>')
            o.append(t(px, y + 5, escape(pn), "bf-label"))
        else:
            o.append(t(px, y + 5, escape(pn), "bf-label bf-muted"))
        o.append("</g>")
    ly = top + pitch * len(DOMAINS) + 2
    o.append(f'<line x1="10" y1="{ly - 12}" x2="{W - 10}" y2="{ly - 12}" class="bf-rule"/>')
    o.append(f'<line x1="16" y1="{ly + 6}" x2="34" y2="{ly + 6}" class="bf-stem"/><circle cx="34" cy="{ly + 6}" r="5" class="bf-ball-full"/>')
    o.append(t(46, ly + 10, "已有明确证据" if zh else "Demonstrated", "bf-small bf-muted"))
    o.append(f'<line x1="160" y1="{ly + 6}" x2="178" y2="{ly + 6}" class="bf-stem-early"/><circle cx="178" cy="{ly + 6}" r="5" class="bf-ball-empty"/>')
    o.append(t(190, ly + 10, "早期信号" if zh else "Early signals only", "bf-small bf-muted"))
    o.append(f'<circle cx="346" cy="{ly + 6}" r="5" class="bf-ball-full"/><circle cx="346" cy="{ly + 6}" r="9.5" class="bf-prod-ring"/>')
    o.append(t(362, ly + 10, "已部署或已进入软件（有公开证据）" if zh else "Deployed or shipped (public evidence)", "bf-small bf-muted"))
    o.append("</svg>")
    return "\n".join(o)


# ── Figure 4: run length and failure rates (dot plots) ───────────────────────
def fig_trends(lang):
    zh = lang == "zh"
    W, lab_x, ax0, aw, pitch = 760, 226, 240, 360, 32
    ph = 40 + 4 * pitch + 34
    H = 2 * ph + 4
    o = svg_open(W, H, lang, "f4",
                 "单次运行更重，失败方式更多" if zh else "Heavier runs, new failure modes",
                 ("(a) 单次运行时长：EoH 约 1 小时，ALE-Agent 4 小时，AI Scientist-v2 最长 15 小时，Darwin Gödel Machine 约 2 周。(b) 报告的错误与作弊率：AI Scientist 42%，Kosmos 20.6%，o3 30.4%，GPT-5 54%。"
                  if zh else
                  "(a) Wall-clock time of one run: EoH about 1 hour, ALE-Agent 4 hours, AI Scientist-v2 up to 15 hours, Darwin Gödel Machine about 2 weeks. (b) Reported error and cheating rates: AI Scientist 42%, Kosmos 20.6%, o3 30.4%, GPT-5 54%."))

    def panel(y0, letter, title, sub, rows, X, ticks, dot_cls):
        o.append(t(10, y0 + 16, f"({letter}) {title}", "bf-head-s"))
        o.append(t(10, y0 + 34, sub, "bf-note"))
        top = y0 + 58
        for v, lab in ticks:
            x = X(v)
            o.append(f'<line x1="{x:g}" y1="{top - 10}" x2="{x:g}" y2="{top + 4 * pitch - 14}" class="bf-grid"/>')
            o.append(t(x, top + 4 * pitch + 2, lab, "bf-small bf-muted bf-num", "middle"))
        for i, (name, v, vlab, tip) in enumerate(rows):
            y = top + i * pitch
            x = X(v)
            o.append(f'<g class="bf-row"><title>{escape(name)}: {escape(tip)}</title>')
            o.append(t(lab_x, y + 5, escape(name), "bf-label", "end"))
            o.append(f'<line x1="{ax0}" y1="{y}" x2="{x:g}" y2="{y}" class="bf-leader"/>')
            o.append(f'<circle cx="{x:g}" cy="{y}" r="6" class="{dot_cls}"/>')
            o.append(t(x + 12, y + 5, vlab, "bf-value"))
            o.append("</g>")

    lo, hi = math.log10(1 / 6), math.log10(24 * 7 * 3)
    Xa = lambda h: ax0 + (math.log10(h) - lo) / (hi - lo) * aw
    ticks_a = [(1 / 6, "10 分钟" if zh else "10 min"), (1, "1 小时" if zh else "1 h"),
               (24, "1 天" if zh else "1 day"), (24 * 7, "1 周" if zh else "1 week")]
    rows_a = [(n, h, zl if zh else el, zl if zh else el) for n, h, el, zl in HOURS]
    panel(0, "a", "单次运行的时长" if zh else "Wall-clock time of one run",
          "对数坐标" if zh else "Log scale", rows_a, Xa, ticks_a, "bf-ball-full")

    Xb = lambda p: ax0 + p / 100 * aw
    ticks_b = [(p, f"{p}%") for p in (0, 25, 50, 75, 100)]
    rows_b = [(n, v, f"{v:g}%  ·  {wz if zh else we}", f"{v:g}%, {wz if zh else we}") for n, wz, we, v, _ in RATES]
    panel(ph, "b", "错误与作弊率" if zh else "Reported error and cheating rates",
          "高度自动化系统中报告的比例" if zh else "In highly automated systems", rows_b, Xb, ticks_b, "bf-ball-accent")
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    for lang in ("en", "zh"):
        (OUT / f"stages-{lang}.svg").write_text(fig_stages(lang) + "\n")
        (OUT / f"lifecycle-{lang}.svg").write_text(fig_lifecycle(lang) + "\n")
        (OUT / f"domains-{lang}.svg").write_text(fig_domains(lang) + "\n")
        (OUT / f"trends-{lang}.svg").write_text(fig_trends(lang) + "\n")
    print("wrote", sorted(p.name for p in OUT.glob("*.svg")))
