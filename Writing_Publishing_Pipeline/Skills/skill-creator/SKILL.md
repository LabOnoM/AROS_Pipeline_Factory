---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
original-source: mattpocock/skills/write-a-skill
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process of creating a skill goes like this:

- **Phase 1: Knowledge Consolidation & Scoping**
    - **Identify and Synthesize:** Before writing any code or documentation, ensure all relevant information from disparate sources is identified and synthesized. This may involve reviewing existing skills, KIs, workflow logs, or external documentation to build a coherent structure for the new skill.
    - **Define Scope:** Clearly decide what the skill should do and roughly how it should do it.

- **Phase 2: Drafting & Implementation**
    - Write a draft of the skill.

- **Phase 3: Evaluation & Refinement**
    - Create a few test prompts and run claude-with-access-to-the-skill on them.
    - Help the user evaluate the results both qualitatively and quantitatively.
        - While the runs happen in the background, draft some quantitative evals if there aren't any (if there are some, you can either use as is or modify if you feel something needs to change about them). Then explain them to the user (or if they already existed, explain the ones that already exist).
        - Use the `eval-viewer/generate_review.py` script to show the user the results for them to look at, and also let them look at the quantitative metrics.
    - Rewrite the skill based on feedback from the user's evaluation of the results (and also if there are any glaring flaws that become apparent from the quantitative benchmarks).
    - Repeat until you're satisfied.
    - Expand the test set and try again at larger scale.

Your job when using this skill is to figure out where the user is in this process and then jump in and help them progress through these stages. So for instance, maybe they're like "I want to make a skill for X". You can help narrow down what they mean, write a draft, write the test cases, figure out how they want to evaluate, run all the prompts, and repeat.

On the other hand, maybe they already have a draft of the skill. In this case you can go straight to the eval/iterate part of the loop.

Of course, you should always be flexible and if the user is like "I don't need to run a bunch of evaluations, just vibe with me", you can do that instead.

Then after the skill is done (but again, the order is flexible), you can also run the skill description improver, which we have a whole separate script for, to optimize the triggering of the skill.

Cool? Cool.

## Communicating with the user

The skill creator is liable to be used by people across a wide range of familiarity with coding jargon. If you haven't heard (