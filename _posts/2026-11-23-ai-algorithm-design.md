---
title: "What Is Left for Humans in Algorithm Design?"
date: 2026-11-23
lang: en
ref: ai-algorithm-design
author: Fei Liu
reading_time: 15
summary: "Five stages of how AI is reshaping algorithm design, why I think we are in the third, and what that means for how we do research."
---

For most of its history, algorithm design has been a human craft. Someone understands a problem, invents a procedure, implements it, and tests it. AI has been moving into that loop for decades, first tuning the numbers inside human-designed algorithms, then designing parts of them, and now, with large language models (LLMs), writing and combining whole algorithms.

As a result, the human role is changing. Agents now do much of the designing, while people define the evaluation and supply the knowledge the agents work from. This post looks at how we got here, where things stand, and what it means for research.

**Key points**

- AI's role in algorithm design can be described in five stages. Humans first provide the algorithm, then the framework, then the evaluation and knowledge, then only the goal, and finally almost nothing.
- We are in Stage 3. Agents improve and fuse whole algorithms, but humans still write the evaluator and supply the knowledge.
- Runs need fewer iterations but are much heavier and fail in new ways, which makes evaluation the part that matters most.
- For researchers, I suggest automating as much as possible with agents. Spend your own effort on the questions, the evaluation and understanding the results, and work on real problems rather than small benchmark gains.

## 1. Five stages

The clearest way I have found to describe the progress is to ask the same question at each stage. **What does the human still have to provide?** An algorithm-design task has roughly five layers. From bottom to top, they are the parameters, the components, the overall framework, the evaluation (plus the knowledge used to design), and the goal. Each stage hands one more layer to AI. The stages describe how the human role shifts. They are not boxes for sorting papers, and one system often spans several.

<figure class="fig">
<div class="fig-scroll">{% include figures/stages-en.svg %}</div>
<figcaption><b>Figure 1.</b> Five stages of AI in algorithm design. Filled cells are designed by AI, outlined cells are provided by humans. The dashed line moves up one layer per stage. Stage 4 is only emerging and Stage 5 is a projection. The timeline gives the approximate onset of each stage, and earlier stages do not disappear when later ones arrive.</figcaption>
</figure>

**Stage 1: AI tunes parameters. Humans provide the algorithm.** Configuration tools treat a finished solver as a black box and search its parameter space. The gains can be large. Tuning CPLEX's 135 parameters sped it up by up to 52× on some MIP benchmarks ([Hutter et al., 2010](https://www.cs.ubc.ca/~hutter/papers/10-CPAIOR-MIP-Config.pdf)). But the algorithm itself does not change.

**Stage 2: AI designs components. Humans provide the framework.** AI now produces a *piece* of the algorithm while the surrounding procedure stays fixed. In MIP, branch-and-bound stays, and a neural network learns the branching rule inside it ([Gasse et al., 2019](https://arxiv.org/abs/1906.01629)).

**Stage 3: AI agents improve and fuse algorithms. Humans provide evaluation and knowledge.** The framework is no longer fixed. Agents edit whole programs, combine ideas from several algorithms and run long search loops. [EoH](https://proceedings.mlr.press/v235/liu24bs.html) evolves heuristics together with the ideas behind them, and EoH-based methods have won several algorithm-design competitions, including the [CVRPLib BKS challenge](https://galgos.inf.puc-rio.br/cvrplib/index.php/en/bks_challenge/overview). One heuristic found by [AlphaEvolve](https://arxiv.org/abs/2506.13131) now schedules Google's data centers and recovers on average 0.7% of its fleet-wide compute. Jiayi Weng's [heuristic learning](https://trinkle23897.github.io/learning-beyond-gradients/) treats this as a new way of learning, where a coding agent improves a policy by editing code, tests and memory instead of network weights. In MIP, LLMs now [configure cutting-plane separators](https://arxiv.org/abs/2412.12038) by reading the problem description together with summaries of the literature. The human input has moved up. **We write the evaluator, choose the instances and supply the knowledge.**

**Stage 4: AI solves problems end to end. Humans provide the goal.** A person states what they want. The system then formulates the problem, designs and implements a method, evaluates it and iterates. There are early signals. Sakana's ALE-Agent [won a live AtCoder heuristic contest](https://sakana.ai/ahc058/) against 804 human participants. Auto-research systems run the whole loop of ideas, experiments and write-up. A paper by [The AI Scientist-v2](https://arxiv.org/abs/2504.08066) passed peer review at a workshop, the [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954) rewrites its own agent code, and Karpathy's minimal [autoresearch](https://github.com/karpathy/autoresearch) runs about a hundred training experiments overnight on one GPU. All of them still receive their goal, and usually their metric, from humans.

**Stage 5: Creation. AI understands the world, sets its own goals, and keeps creating and solving problems.** Here the system no longer waits for a goal. It decides which problems are worth solving, defines how success is measured, and turns each result into the start of the next problem. No system does this today. I include the stage because it is where the trend points, and because it makes clear what Stage 4 still lacks, which is deciding *what* to work on.

### Why I think we are in Stage 3

The Stage-4 signals still rely on evaluation made by humans. A heuristic contest ships its own scorer, and AlphaEvolve's mathematical results rely on a verifier written for each problem. Algorithm design is also a long-horizon task with delayed reward. A design choice often pays off only after many rounds of implementation, testing and refinement, which is why benchmarks such as [ALE-Bench](https://arxiv.org/abs/2506.09050) treat it as long-horizon engineering. Stronger base models help, but they will not solve this on their own any time soon. Progress also depends on better automated frameworks for search, evaluation and feedback. Agents are very good at improving and fusing inside a well-specified loop. Specifying that loop is still a human job.

## 2. How much is automated, and where

It helps to separate what AI has been *shown* to do in a few frontier demonstrations from what is routine practice. The figures below are about the former, so they describe where the frontier is, not where the average project is.

<figure class="fig">
<div class="fig-scroll">{% include figures/lifecycle-en.svg %}</div>
<figcaption><b>Figure 2.</b> Who does conception, design and evaluation in thirteen representative systems. A rating reflects what each paper requires the human to supply. Hover over a row for details. Sources are listed at the end of the post.</figcaption>
</figure>

Design was automated first. In nearly every LLM-era system, AI writes the algorithm. Conception is still mostly human. Some systems propose ideas, but in none of them does AI choose the problem. Evaluation is the most persistent human job, and the first attempts to automate it, such as [LLM-generated benchmarks](https://arxiv.org/abs/2601.21877), are very recent. Automated evaluation is also fragile. Running AlphaEvolve on 67 problems, [Georgiev, Gómez-Serrano, Tao and Wagner](https://arxiv.org/abs/2511.02864) saw the system exploit loopholes in leaky verifiers and concluded that "designing a clever verifier that avoids this behavior is key to discover new results".

<figure class="fig">
<div class="fig-scroll">{% include figures/domains-en.svg %}</div>
<figcaption><b>Figure 3.</b> The highest stage reached by AI in eight algorithm-design domains (line and dots), and where AI-designed algorithms have been deployed or shipped in software, according to public sources (rings). Dashed segments mark early signals, meaning a few published demonstrations rather than routine practice.</figcaption>
</figure>

Most domains are in Stage 3 at the frontier, and deployment is starting to follow. Every applied domain in Figure 3 now has some public evidence of AI-designed algorithms in real use. Examples include learned components inside commercial MIP solvers such as [CPLEX](https://doi.org/10.1287/opre.2022.2267) (Stage 2), AlphaEvolve-designed heuristics in Google's data centers and in [warehouse routing at FM Logistic](https://cloud.google.com/blog/products/ai-machine-learning/how-fm-logistic-tackled-the-traveling-salesman-problem-at-warehouse-scale-with-alphaevolve), LLM-written optimization code at [Microsoft](https://www.microsoft.com/en-us/research/project/optiguide-genai-for-supply-chain-optimization/), and [Lion](https://arxiv.org/abs/2302.06675), a training optimizer found by automated program search and deployed in Google's search-ads models. Much of this is recent, several cases are described as pilots, and they come from a handful of companies. Optimization modeling is the one domain with early Stage-4 signals, because there the goal can be stated in text and the result checked automatically. MIP solver components lag behind at the frontier. Mature solvers, strict exactness and expensive evaluation make them hard to automate, and LLM-designed solver components such as [MILP-Evo](https://arxiv.org/abs/2607.18252) have appeared only recently.

### Fewer iterations, heavier runs

Early systems such as [FunSearch](https://doi.org/10.1038/s41586-023-06924-6) needed on the order of a million LLM samples. Most current systems need far fewer. But each step has become much heavier. FunSearch "needs fast evaluation (≤ 20min on 1 CPU)", while AlphaEvolve "can evaluate for hours, in parallel, on accelerators". Whole runs have grown from about an hour for EoH to weeks. One Darwin Gödel Machine run takes about two weeks and costs about $22,000.

<figure class="fig">
<div class="fig-scroll">{% include figures/trends-en.svg %}</div>
<figcaption><b>Figure 4.</b> (a) Wall-clock time of one run, log scale. (b) Error and cheating rates reported for highly automated systems. Tasks and definitions differ, so the figure shows orders of magnitude, not a controlled comparison. Sources are listed at the end of the post.</figcaption>
</figure>

Longer, more autonomous runs also fail in new ways. An [independent evaluation](https://arxiv.org/abs/2502.14297) of the AI Scientist found that 42% of its experiments failed because of coding errors. [METR](https://metr.org/blog/2025-06-05-recent-reward-hacking/) found that o3 reward-hacked in 30.4% of runs on research-engineering tasks. The more of the loop we hand over, the more the reliability of the whole depends on the part we still own, which is the evaluation.

## 3. Some thoughts

**Try AI and agent systems as much as possible, and automate as much of the workflow as possible.** If parts of your research loop, such as generating variants, running experiments or collecting results, are still done by hand, they are probably the cheapest things to automate. And the only way to learn what these systems can and cannot do is to use them on your own problems.

**The human role moves to asking the key questions and defining concrete evaluation.** In every Stage-3 system, the decisive human input is the evaluator, meaning which instances, which metric and which constraints count. An agent will optimize exactly what you measure, and it will also exploit whatever your measurement gets wrong. Designing a good evaluation therefore deserves as much care as designing the algorithm itself.

**Do not spend effort on small algorithm tweaks that gain 1% on a benchmark. Solve real needs from industry and AI applications.** Small, local improvements on fixed benchmarks are exactly what Stage-2 and Stage-3 systems now produce cheaply and in volume. What they cannot do on their own is find the problem that matters and define what success means there. Real problems also bring what benchmarks leave out, such as messy data, hard constraints and success criteria tied to actual use. That is where human judgment still matters most.

**Build understanding, not just code.** An algorithm found by search is only half a result. The other half is knowing why it works and when it fails. Mathematics is running into this right now. In 2026, AI systems produced claimed proofs of finite-time blow-up for the Navier–Stokes equations ([Quanta](https://www.quantamagazine.org/ai-has-solved-one-of-maths-1-million-millennium-prize-problems-20260908/)) and of the Riemann hypothesis ([Scientific American](https://www.scientificamerican.com/article/anthropic-mathematician-claims-to-prove-riemann-hypothesis-most-famous-problem-in-all-of-math/)). Both were checked by machine in Lean, but mathematicians are still working to understand them. AI can now produce results faster than people can understand them.

Algorithm design shows the same trend. Agents produce algorithms of hundreds of lines that work well but resist quick understanding, and Weng warns that a heuristic system that only grows, without being compressed, turns into "a big ball of mud". Compressing a complex, effective algorithm into an idea a person can grasp, check and reuse is still mostly human work, and it is what turns a result into knowledge.

**Expertise matters more, not less.** Georgiev and colleagues found that AlphaEvolve worked better "in the hands of a user who is a subject expert". Domain knowledge is how you choose the right problem, write an evaluator that cannot be gamed, and steer the search. AI changes how expertise is used. It does not make it less valuable.

<details class="sources">
<summary>Sources for the figures</summary>
<p><b>Figure 2.</b>
Algorithm configuration: <a href="https://jair.org/index.php/jair/article/view/10628">ParamILS</a>, <a href="https://www.cs.ubc.ca/~hutter/papers/11-LION5-SMAC.pdf">SMAC</a>, <a href="https://doi.org/10.1016/j.orp.2016.09.002">irace</a>, <a href="https://www.cs.ubc.ca/~hutter/papers/10-CPAIOR-MIP-Config.pdf">MIP configuration</a> ·
<a href="https://arxiv.org/abs/1906.01629">Learned branching</a> ·
<a href="https://arxiv.org/abs/1803.08475">Neural solver</a> ·
<a href="https://proceedings.mlr.press/v235/liu24bs.html">EoH</a> ·
<a href="https://proceedings.mlr.press/v235/ahmaditeshnizi24a.html">OptiMUS</a> ·
<a href="https://arxiv.org/abs/2408.06292">The AI Scientist</a> ·
<a href="https://arxiv.org/abs/2504.08066">The AI Scientist-v2</a> ·
<a href="https://arxiv.org/abs/2506.13131">AlphaEvolve</a> ·
<a href="https://arxiv.org/abs/2505.22954">Darwin Gödel Machine</a> ·
<a href="https://arxiv.org/abs/2509.19349">ShinkaEvolve</a> ·
<a href="https://arxiv.org/abs/2509.26603">DeepScientist</a> ·
<a href="https://arxiv.org/abs/2511.08522">AlphaResearch</a> ·
<a href="https://arxiv.org/abs/2601.21877">Evolution of Benchmark</a></p>
<p><b>Figure 3.</b>
MIP solver components: <a href="https://arxiv.org/abs/1906.01629">learned branching</a>, <a href="https://proceedings.mlr.press/v119/tang20a.html">learned cuts</a>, <a href="https://arxiv.org/abs/2012.13349">neural diving</a>, <a href="https://arxiv.org/abs/2412.12038">separator configuration</a>, <a href="https://arxiv.org/abs/2607.18252">MILP-Evo</a>; production: <a href="https://doi.org/10.1287/opre.2022.2267">CPLEX 12.10</a>, <a href="https://optimization-online.org/2020/12/8166/">FICO Xpress 8.9</a> ·
Optimization modeling: <a href="https://proceedings.mlr.press/v235/ahmaditeshnizi24a.html">OptiMUS</a>, <a href="https://doi.org/10.1287/opre.2024.1233">ORLM</a>, <a href="https://arxiv.org/abs/2411.01679">autoformulation</a>; deployed: <a href="https://www.microsoft.com/en-us/research/project/optiguide-genai-for-supply-chain-optimization/">OptiGuide</a>, <a href="https://www.microsoft.com/en/customers/story/26648-sight-machine-microsoft-foundry">OptiMind with Sight Machine</a> ·
CO heuristics: <a href="https://doi.org/10.1038/s41586-023-06924-6">FunSearch</a>, <a href="https://proceedings.mlr.press/v235/liu24bs.html">EoH</a>, <a href="https://arxiv.org/abs/2402.01145">ReEvo</a>, <a href="https://arxiv.org/abs/2501.08603">MCTS-AHD</a>, <a href="https://arxiv.org/abs/2412.17287">LLM4AD</a>; deployed: <a href="https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/">AlphaEvolve (Borg scheduling)</a>, <a href="https://cloud.google.com/blog/products/ai-machine-learning/how-fm-logistic-tackled-the-traveling-salesman-problem-at-warehouse-scale-with-alphaevolve">FM Logistic</a> ·
Industrial operations: <a href="https://cloud.google.com/blog/products/ai-machine-learning/how-fm-logistic-tackled-the-traveling-salesman-problem-at-warehouse-scale-with-alphaevolve">FM Logistic with AlphaEvolve</a> ·
Continuous optimization: <a href="https://arxiv.org/abs/2405.20132">LLaMEA</a>; deployed: <a href="https://arxiv.org/abs/2302.06675">Lion (Google search ads)</a> ·
ML training &amp; kernels: <a href="https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/">AlphaEvolve (Gemini kernel)</a>, <a href="https://arxiv.org/abs/2512.23236">KernelEvolve at Meta</a> ·
Systems: <a href="https://deepmind.google/discover/blog/alphadev-discovers-faster-sorting-algorithms/">AlphaDev in libc++</a>, <a href="https://deepmind.google/blog/alphaevolve-impact/">AlphaEvolve (TPU circuits)</a> ·
Mathematics: <a href="https://doi.org/10.1038/s41586-023-06924-6">FunSearch</a>, <a href="https://arxiv.org/abs/2511.02864">Georgiev et al.</a></p>
<p><b>Figure 4.</b>
(a) EoH: author's runs · <a href="https://sakana.ai/ahc058/">ALE-Agent at AHC058</a> · <a href="https://arxiv.org/abs/2504.08066">The AI Scientist-v2</a> · <a href="https://arxiv.org/abs/2505.22954">Darwin Gödel Machine</a>.
(b) <a href="https://arxiv.org/abs/2502.14297">Beel et al. on the AI Scientist</a> · <a href="https://arxiv.org/abs/2511.02824">Kosmos</a> · <a href="https://metr.org/blog/2025-06-05-recent-reward-hacking/">METR on o3</a> · <a href="https://arxiv.org/abs/2510.20270">ImpossibleBench</a>.
FunSearch vs. AlphaEvolve evaluation cost: Table 1 of the <a href="https://arxiv.org/abs/2506.13131">AlphaEvolve paper</a>.</p>
</details>
