# Original Article: Designing Tools for AI Agents

**Author:** Thariq (@trq212), Claude Code team at Anthropic
**Date:** February 28, 2026
**Source:** https://x.com/trq212/article/2027463795355095314

---

## Introduction

If you're building an agent today you're probably thinking a lot about its tools.
Tools are the levers of the agent: they define how it can interact with the world
and are where most of the complexity of an agent system lies.

What is a tool, really? It's just a function: it takes some inputs and produces a
useful output. Similar to a hammer, it's not useful by itself. A great hammer
left on a table won't build a house. Give that hammer to a skilled carpenter and
it becomes invaluable. An LLM is like a very smart person who has never used a
computer, but you would have to know how to use it to write and execute code.

This is a useful framework for designing your agent. You want to give it tools
that are shaped to its own abilities. But how do you know what those abilities
are? You pay attention, read its outputs, experiment. You learn to see like an
agent.

## Lesson 1: Improving Elicitation & the AskUserQuestion Tool

When building the AskUserQuestion tool, our goal was to improve Claude's
ability to ask questions (often called elicitation).

While Claude could just ask questions in plain text, we found answering
those questions felt like they took an unnecessary amount of time. How
could we lower this friction and increase the bandwidth of communication
between the user and Claude?

**Attempt #1 - Editing the ExitPlanTool:**
The first thing we tried was adding a parameter to the ExitPlanTool to have an
array of questions alongside the plan. This was the easiest thing to
implement, but it confused Claude because we were simultaneously asking
for a plan and a set of questions about the plan. What if the user's answers
conflicted with what the plan said? Would Claude need to call the
ExitPlanTool twice? We needed another approach.

**Attempt #2 - Changing Output Format:**
Next we tried modifying Claude's output instructions to serve a slightly
modified markdown format that it could use to ask questions. While this was
the most general change we could make and Claude even seemed to be okay at
outputting this, it was not guaranteed. Claude would append extra sentences,
omit options, or use a different format altogether.

**Attempt #3 - The AskUserQuestion Tool:**
Finally, we landed on creating a tool that Claude could call at any point, but it
was particularly prompted to do so during plan mode. This tool allowed us to
prompt Claude for a structured output and it helped us ensure that Claude gave
the user multiple options. Most importantly, Claude seemed to like calling this
tool and we found its outputs worked well. Even the best designed tool doesn't
work if Claude doesn't understand how to call it.

## Lesson 2: Updating with Capabilities — Tasks & Todos

When we first launched Claude Code, we realized that the model needed a
Todo list to keep it on track. To do this we gave Claude the TodoWrite tool.

But even then we often saw Claude forgetting what it had to do. To adapt, we
inserted system reminders every 5 turns that reminded Claude of its goal.

But as models improved, they not only did not need to be reminded of the
Todo List but could find it limiting. Being sent reminders of the todo list made
Claude think that it had to stick to the list instead of modifying it.

Seeing this, we replaced TodoWrite with the Task Tool. Whereas Todos were about
keeping the model on track, Tasks were more about helping agents communicate
with each other. Tasks could include dependencies, share updates across subagents
and the model could alter and delete them.

**Key insight:** As model capabilities increase, the tools that your models once
needed might now be constraining them. It's important to constantly revisit
previous assumptions on what tools are needed.

## Lesson 3: Designing a Search Interface

When Claude Code first came out, we used a RAG vector database to find
context for Claude. While RAG was powerful and fast it required indexing and
setup and could be fragile. More importantly, Claude was given this context
instead of finding the context itself.

But if Claude could search on the web, why not search your codebase? By
giving Claude a Grep tool, we could let it search for files and build context
itself.

This is a pattern we've seen as Claude gets smarter: it becomes increasingly
good at building its context if it's given the right tools.

When we introduced Agent Skills we formalized the idea of **progressive
disclosure**, which allows agents to incrementally discover relevant context
through exploration. Claude could read skill files and those files could then
reference other files that the model could read recursively.

Over the course of a year Claude went from not really being able to build its
own context, to being able to do nested search across several layers of files
to find the exact context it needed.

## Lesson 4: Progressive Disclosure — The Claude Code Guide Agent

Claude Code currently has ~20 tools, and we are constantly asking ourselves
if we need all of them. The bar to add a new tool is high, because this gives
the model one more option to think about.

We could have put all information about Claude Code in the system prompt, but
given that users rarely asked about this, it would have added context rot and
interfered with Claude Code's main job: writing code.

Instead, we tried a form of progressive disclosure. We gave Claude a link to its
docs which it could then load to search for more information. But Claude would
load a lot of results into context. So we built the Claude Code Guide subagent
which has extensive instructions on how to search docs well and what to return.

We were able to add things to Claude's action space without adding a tool.

## Conclusion: An Art, not a Science

Designing the tools for your models is as much an art as it is a science. It
depends heavily on the model you're using, the goal of the agent and the
environment it's operating in.

Experiment often, read your outputs, try new things. **See like an agent.**
