---
name: agent-design-principles
description: Principles for designing and evolving AI agent tools, prompts, and architecture. Use when self-improving prompts, adding/removing tools, redesigning agent workflows, or evaluating whether current agent behavior is optimal. Essential skill for self_dev and prompt optimization tasks.
license: MIT license
metadata:
    skill-author: BeesGo-Agent
    source: Claude Code team article by Thariq (Anthropic, 2026)
    url: https://x.com/trq212/article/2027463795355095314
---

# Agent Design Principles

Distilled from a year of building Claude Code at Anthropic. These principles guide how to design tools, prompts, and architecture for AI agents that improve over time.

## When to Use This Skill

Apply these principles when:
- **Self-improving prompts** — editing `prompts/*.md` files to fix failure patterns
- **Adding or removing tools** — evaluating whether a new tool is justified
- **Redesigning agent workflows** — changing how tiers delegate, search, or report
- **Evaluating agent behavior** — diagnosing why the agent makes wrong choices
- **Upgrading to a new model** — revisiting assumptions that may no longer apply
- **Building new subagents** — designing their tool set and prompt structure

## The Six Core Principles

### P1: Design Tools Shaped to Agent Abilities

> "Even the best designed tool doesn't work if Claude doesn't understand how to call it."

Tools must feel **natural** to the LLM. The test isn't whether the tool is logically correct — it's whether the model *likes calling it* and produces good outputs when it does.

**How to apply:**
- If an LLM consistently avoids calling a tool, the tool's interface is wrong — not the LLM
- If a tool confuses the model (e.g., asking for a plan AND questions simultaneously), split it
- Frame tool descriptions positively: "Use for X" before "Don't use for Y"
- Test by reading actual LLM outputs — does the tool get called correctly?

**Anti-pattern:** Combining multiple functions into one tool to reduce tool count. This confuses the model more than having an extra tool.

**BeesGo application:** `gui_agent.md` uses positive framing first ("Use for interactive visual tasks"), then rules. The `deep_task` tool description guides natural delegation.

---

### P2: Structured Tools Over Free-Form Output

> "Claude would append extra sentences, omit options, or use a different format altogether."

When you need structured output from the LLM, use a **dedicated tool with parameters** — not markdown parsing instructions.

**How to apply:**
- If you need JSON output, make a tool that accepts JSON parameters
- If you need a specific report format, define explicit sections (Status, Done, Failed, Next Steps)
- If the LLM keeps breaking your expected format, you're fighting it — use a tool instead
- Structured output via tools is guaranteed; structured output via prompt instructions is not

**Anti-pattern:** Adding complex markdown parsing instructions to the system prompt. The LLM will sometimes follow them, sometimes not.

**BeesGo application:** `final_report.md` uses a structured template (Status/Done/Failed/Outputs/Next Steps). `locate_element.md` requires exact JSON format (`{"x": 100, "y": 200}`).

---

### P3: Revisit Tools as Model Capabilities Improve

> "As models improved, they not only did not need to be reminded of the Todo List but could find it limiting."

What helps a weaker model may **constrain** a stronger one. Regularly audit your prompts and tools for legacy rules that no longer apply.

**How to apply:**
- After upgrading models, test without restrictive rules — the new model may perform better
- If the LLM ignores a rule consistently, the rule may be counterproductive — remove it
- System reminders that were needed for forgetful models become noise for better ones
- Rigid budget tables should become adaptive estimates
- Tools that once helped may now be unnecessary overhead

**Audit checklist:**
1. Read each prompt file. Would a smart human need this instruction?
2. Check for overly specific rules (exact iteration counts, rigid if-else chains)
3. Look for "Avoid" rules — are they still necessary or just historical?
4. Test removing constraints and observe if behavior improves

**BeesGo application:** `director.md` uses adaptive budget guidance ("estimate based on complexity") instead of fixed iteration tables. `heartbeat.md` was simplified — the model doesn't need detailed self-diagnostic instructions.

---

### P4: Progressive Disclosure — Let Agents Build Their Own Context

> "By giving Claude a Grep tool, we could let it search for files and build context itself."

Don't preload everything into the system prompt. Give agents **search tools** and let them find context incrementally.

**How to apply:**
- **Search local first**: codebase (grep/find) → memory (hindsight) → documents → web
- Skills are **reference chains**: SKILL.md → sub-files → API docs → examples. Don't inline everything.
- Give the agent just enough context to start, then let it discover more as needed
- Files that reference other files create a natural discovery tree
- The agent should build understanding through exploration, not receive it passively

**The progressive disclosure stack:**
```
Level 0: System prompt (identity, core tools, bank directory)
Level 1: Hindsight auto-recall (instance bank — past conversations)
Level 2: On-demand recall (skills, shared knowledge, tool registry)
Level 3: File reading (SKILL.md → sub-files → referenced docs)
Level 4: Web search (external APIs, documentation, StackOverflow)
```

**Anti-pattern:** Dumping all skill descriptions, all tool docs, and all memory into the system prompt. This creates context rot and wastes tokens on irrelevant information.

**BeesGo application:** Only 5 core tools in the system prompt; 24+ others are discovered via Hindsight. Skills are searched by query, not listed. The HindsightRouter pre-searches banks before each turn.

---

### P5: Small Tool Count with High Bar to Add

> "The bar to add a new tool is high, because this gives the model one more option to think about."

Every tool adds cognitive load. Before adding a tool, ask: can this be achieved via progressive disclosure instead?

**How to apply:**
- Before adding a tool, try solving it with a skill (file-based instructions) or a subagent
- If a tool is rarely used, consider removing it and making it discoverable instead
- Core tools (always available) should be 5-7 maximum
- Specialized tools should be recalled on-demand, not always present
- Tools should be high-leverage: one tool should handle many use cases

**Decision framework:**
1. Can this be done with existing tools + instructions? → Skill, not tool
2. Is this needed every conversation? → Core tool
3. Is this needed sometimes? → Discoverable tool (indexed in Hindsight)
4. Is this a one-off? → Subagent with custom instructions

**BeesGo application:** 5 core tools (exec, message, hindsight, deep_task, task_control). All others (GUI, web, media, hardware) are discoverable. The `mainloop_tools.md` prompt explains this pattern.

---

### P6: Subagents for Domain-Specific Retrieval

> "We built the Claude Code Guide subagent which Claude is prompted to call when you ask about itself."

Instead of loading domain knowledge into the main agent, create **specialized subagents** that search efficiently and return only what's needed.

**How to apply:**
- If a domain requires deep knowledge, create a subagent that knows how to search it
- The subagent should return **answers**, not raw search results
- Main agent stays fast and focused; subagents handle the complexity
- Subagent prompts should include search-first instructions: "grep first, read docs second"
- The D/W/R tier system is itself a form of this pattern — Directors search and plan, Workers implement

**Anti-pattern:** Putting extensive domain documentation in the system prompt "just in case."

**BeesGo application:** D/W/R tier system. Directors build context via search before planning. Workers search for patterns before implementing. The HindsightRouter is a lightweight pre-search subagent.

---

## Self-Evolution Workflow

When the agent detects that its behavior needs improvement, follow this workflow:

```
1. DETECT  — Observe failure (deep_task exhausted, wrong tool selected, bad output)
2. DIAGNOSE — Search for the pattern:
   → hindsight(action="recall", query="deep_task failed exhausted budget")
   → Read the relevant prompt file
3. IDENTIFY PRINCIPLE — Which of the 6 principles does the failure violate?
   → Tool confusion? → P1 (reshape the tool)
   → Output format broken? → P2 (add structure)
   → Constraint too rigid? → P3 (remove/soften the rule)
   → Missing context? → P4 (add search-first instruction)
   → Too many tool options? → P5 (make some discoverable)
   → Domain knowledge gap? → P6 (create a subagent/skill)
4. EDIT  — Make a minimal, targeted change to the relevant prompt file
5. LOG   — hindsight(action="retain", content="[prompt_change] principle=P{N} ...")
6. TEST  — Run a similar task and observe if the change helped
7. ITERATE — If the change didn't help, REVERT it. What works for one model may not work for another.
```

## Reference

For the full original article, see: [references/original_article.md](references/original_article.md)

---

## Online Resources & Troubleshooting

> **Search-first approach:** When you encounter an issue not covered above, search for solutions before asking the user. Check official docs → GitHub issues → Stack Overflow → web search, in that order.

When applying these principles to agent design, search these resources for deeper understanding:

**Agent Architecture & Design:**
- Search: `"AI agent" design patterns <pattern>` (e.g., tool use, subagent delegation, context management)
- Search: `"Claude Code" architecture agent design` for Claude-specific patterns
- Anthropic research: `https://www.anthropic.com/research` — papers on agent capabilities and safety

**Prompt Engineering:**
- Anthropic prompt engineering docs: `https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview`
- Search: `"prompt engineering" <technique>` (e.g., chain of thought, few-shot, system prompt design)
- Search: `"tool use" prompt design LLM <issue>` for tool-calling prompt patterns

**MCP & Tool Design:**
- Model Context Protocol: `https://modelcontextprotocol.io/` — tool interface specifications
- Search: `MCP tool design best practices` for tool interface patterns
- Search: `"function calling" LLM design <issue>` for general tool-use patterns

**Evaluation & Iteration:**
- Search: `"LLM evaluation" agent performance <metric>` for measuring agent quality
- Search: `"prompt iteration" methodology <approach>` for systematic improvement
- Search: `"A/B testing" LLM prompts <framework>` for comparative evaluation
