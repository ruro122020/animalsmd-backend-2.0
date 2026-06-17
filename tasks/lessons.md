# Lessons

## Commit granularity and message style

**Correction (2026-06-17):** On issue #10 the work was squashed into one commit of 17 files. Commits should be made incrementally as the work progresses, not batched at the end. A dispatched agent also failed to commit because it was blocked on tooling; the commit rule must be passed into agent dispatch prompts, since subagents do not inherit it.

**Rules:**
- Commit one logical step at a time, as each step completes. Do not bundle an entire multi-part issue into a single commit. Each commit should leave the code in a working/importable state.
- For a multi-part issue, the natural seams are separate commits (e.g. "add the base abstraction" then "migrate callers onto it"), as long as each is self-consistent.
- Match the existing log's message style:
  - Imperative mood, capitalized first word, no trailing period.
  - Concise subject (~50-72 chars). Add a short "why" clause when it clarifies intent.
  - No conventional-commit prefixes (no `feat:`, `fix:`).
  - No issue number in the subject line. Reference the issue in the PR body, not the commit subject.
  - Examples from the log: "Drop stale comment about the old _password_hash validator", "Guard login against a missing body or credentials to avoid a 500", "Rename ic to illness_classification for readability".
- When dispatching an agent to implement, include these commit rules in its prompt.
