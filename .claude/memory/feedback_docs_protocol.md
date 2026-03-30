---
name: Always update all 5 docs per session
description: Never skip SESSION_LOG, ARCHITECTURE, or ROADMAP marks — all 5 docs must be updated every session
type: feedback
---

Every session MUST update ALL 5 documentation files per the CLAUDE.md contract:
1. `docs/CHANGELOG.md` — session entry
2. `docs/MEMORY.md` — test count, progress line, next session pointer
3. `docs/SESSION_LOG.md` — session entry under correct Phase heading
4. `docs/ROADMAP.md` — mark session complete
5. `docs/ARCHITECTURE.md` — new module entries if files were created

**Why:** User caught that S270-S305 (36 sessions) had zero entries in SESSION_LOG and ARCHITECTURE, and only partial ROADMAP updates. This created a false picture of project state for anyone reading the docs.

**How to apply:** The update_docs_s[N].py script must patch all 5 files, not just CHANGELOG + MEMORY + coverage map. Check each file before committing.
