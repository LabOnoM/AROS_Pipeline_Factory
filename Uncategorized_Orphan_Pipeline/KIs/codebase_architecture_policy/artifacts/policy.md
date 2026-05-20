# Codebase Architecture & Deep Modules Policy

This policy governs how Swarm Agents approach architectural refactoring, interface design, and codebase navigation within the AROS environment. It is derived from the principles of "A Philosophy of Software Design" (Ousterhout) and adapted for AI-Native development.

## Core Principles

### 1. Deep Modules over Shallow Modules
The primary goal of refactoring is to create **Deep Modules** — modules that provide significant leverage by hiding complex implementation details behind a very simple interface.
- **Deep = High Leverage:** A lot of behavior hidden behind a small interface.
- **Shallow = Low Leverage:** An interface that is nearly as complex as the implementation it hides. Shallow modules are friction points for AI agents and human developers because they increase cognitive load without reducing complexity.

### 2. Locality of Behavior
Maintainers (and AI agents) benefit when change, bugs, and knowledge are concentrated in one place.
- Avoid extracting pure functions solely for the sake of "testability" if it means the real bugs now hide in how those functions are coordinated (orchestration logic).
- Tightly-coupled modules that leak their internal state across boundaries violate locality. Consolidate them.

### 3. The Deletion Test
To determine if a module or abstraction is earning its keep, imagine deleting it.
- If deleting it causes complexity to vanish (e.g., you just inline the code and it's simpler), the module was a shallow pass-through.
- If deleting it causes complexity to reappear and spread across N callers, the module was earning its keep.

### 4. Seams and Adapters
- **Seam:** A place where behavior can be altered without editing the caller in place. (Avoid the vague term "boundary").
- **Adapter:** A concrete implementation satisfying an interface at a seam.
- **Rule of Thumb:** One adapter = a hypothetical seam. Two adapters = a real seam. Don't over-engineer hypothetical seams unless preparing for imminent replacement.

## Agent Refactoring Workflow

When an agent is tasked with "cleaning up" or "refactoring" a codebase:

1. **Explore organically:** Do not follow rigid line-count heuristics. Look for architectural friction.
   - Where does understanding one concept require bouncing between many small files?
   - Where are the modules shallow?
   - Which parts of the codebase are untested because they lack a proper seam?
2. **Apply the Deletion Test:** If a module is suspected of being shallow, apply the deletion test in thought before proceeding.
3. **Present Deepening Opportunities:** Frame refactors as turning shallow modules into deep ones. Focus on the benefits of Locality and Leverage.
4. **Use Vertical Slices (Tracer Bullets):** When rewriting, do not rewrite horizontal layers. Create a vertical slice that cuts through all layers to prove the new architectural seam works before migrating the rest.
5. **TDD-Based Fixes:** Use the interface as the test surface. Drive fixes and structural changes by writing tests against the new interface first.

## Vocabulary Constraints

Agents MUST use consistent vocabulary to prevent linguistic drift:
- Use **Module**, **Interface**, **Implementation**, **Depth**, **Seam**, **Adapter**, **Leverage**, and **Locality**.
- **Do not use** generic terms like "component," "service," or "boundary" unless they are explicitly defined in the project's `CONTEXT.md` domain language.
