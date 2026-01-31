# Splitting guide (v2 Content PROMPT)

## Mental model

You are not “making slides” yet — you are planning **pages** and their information density so a later styling step can render them cleanly.

Treat each page as:

- one key message
- one dominant representation (bullets, diagram, table, code, screenshot)
- plus optional supporting items

## When to split

Split a page when any of these are true:

- **Multiple intents**: the page is doing both “explain” and “compare” and “teach a workflow”.
- **Too many primitives**: >6 bullets, >2 diagrams, >1 table, >1 code block, or mixed forms that compete.
- **Narrative jump**: topic boundary or a new “phase” (setup → execution → results → lessons).
- **Long sequences**: more than ~5 steps in a process without a visual.

Preferred split strategies:

1. **Phase split**: `Setup`, `Execution`, `Failure`, `Fix`, `Results`, `Takeaways`
2. **Example split**: `Concept` → `Example` → `Pitfalls`
3. **Before/after split**: `Old approach` → `New approach`
4. **Zoom split**: `Overview` → `Details` (continuation slide)

## When to merge

Merge adjacent pages when:

- they share the same intent and representation
- each page would be too sparse alone
- the reader would lose context if separated

## Density checklist (self-review)

For each page in `prompts/content/<deck>.md`:

- Title says the takeaway (not a topic label).
- “Must include” contains all facts/code/images that matter.
- “Suggested representation” is clear and singular.
- If there is a table/diagram requirement, the input data is specified (or a TODO is marked).

