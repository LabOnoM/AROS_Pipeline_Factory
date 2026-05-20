# Long-running Work Management

## Problem

Without a structured work management layer, concurrent agent work collides in shared state: two sub-agents writing to the same in-memory buffer corrupt each other's output, there is no canonical signal for "this work is done and will not change," and the parent coordinator has no safe window to evict completed work from memory. Untyped work identifiers make it impossible to route kill signals or status queries to the right handler at scale.

These problems emerge in any agent runtime that supports concurrent or background work — they are not specific to a single implementation.

## Golden Rules

### Every work unit gets a typed identity

Assign each unit of async work a prefixed, typed ID at creation time. The type prefix encodes what kind of work it is (shell command, agent, remote worker, teammate, etc.), making log filtering, routing, and kill dispatch unambiguous without parsing additional fields. Use a collision-resistant random suffix — the ID space should be large enough that brute-force collisions are infeasible even across hostile environments.

### Strict state machine with permanent terminal states

Every work unit follows the same lifecycle: it starts (most register directly as "running," skipping any "pending" phase), it runs, and it ends in exactly one terminal state — completed, failed, or killed. Terminal states are permanent. Encode this invariant in a single canonical check function, and use that function everywhere instead of inlining status comparisons. If a new terminal state is ever added, inline copies will silently diverge.

### Output goes to disk; memory holds only an offset

Keeping full transcripts in memory for every concurrent sub-agent is unbounded. Instead, write output to a per-work-unit file on disk. The in-memory state only stores a read offset. On each poll cycle, read the delta since the last offset and advance atomically. This keeps the in-memory footprint constant regardless of how long a work unit runs.

### Eviction is two-phase, gated by notification

When work reaches a terminal state:

1. **Disk cleanup** happens eagerly — output files are removed at the terminal transition.
2. **Memory cleanup** happens lazily — the in-memory record is only removed after the parent has been notified of the result.

The notification gate is critical. Without it, the framework would delete the work record before the parent could read the result, creating a race between eviction and result retrieval.

### Decompose complex tasks into logical, coherent, and sequentially flowing sub-tasks.

## When To Use

- Your agent spawns concurrent sub-agents or background tasks.
- You need to track the lifecycle of work that outlives a single turn.
- You need to display task status in a UI or route kill signals to specific work units.
- Long-running agents produce output that would be too large to keep in memory.
- You need a clean GC strategy that doesn't race with result consumption.

## Tradeoffs

| Decision | Benefit | Cost |
|---|---|---|
| Typed prefixed IDs | Unambiguous routing, easy log grep | One more field to generate and propagate |
| Skip "pending" in practice | Simpler, faster registration | UIs that assume "pending" as a required phase will break |
| Disk-backed output | Constant memory, survives interruption | I/O latency per poll, disk cleanup obligations |
| Two-phase eviction | No race between GC and result retrieval | More complex lifecycle — both phases must happen |
| Notification-gated GC | Parent always sees the result | Un-notified terminal tasks leak memory indefinitely |
| Retain flag for UI | Users can view completed work | Must be explicitly cleared or the task leaks |

## Implementation Patterns

- Mint a typed, prefixed ID before allocating any state. The ID is the work unit's identity for its entire lifecycle.
- Initialize shared base fields (status, output file path, read offset) via a factory function. The factory sets a safe default status; the concrete constructor overrides to "running" if the work starts immediately.
- Register work through a single entry point into shared state. Never write directly to the task store — the registration function is the chokepoint for validation and deduplication.
- For agent-type work, initialize the output file as a symlink to the agent's existing transcript. This avoids copying and lets the output file resolve immediately.
- Transition to "running" at or before registration. The "pending" state from the base factory is a safe default, not a required phase — most work starts immediately.
- Use a generic, type-parameterized update function for all mutations. Skip the state spread when the updater returns the same reference to prevent spurious re-renders.
- On every terminal transition: set the end timestamp, clean up the disk output, and set an eviction deadline (unless the work is being actively viewed).
- Enqueue a parent notification exactly once per terminal transition. Use a "notified" flag inside the update function to make the enqueue idempotent.
- Register a cle