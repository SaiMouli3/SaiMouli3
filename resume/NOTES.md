# Resume revision notes

## What I checked on GitHub (5 Nov 2026)

| Claim | Source | Result |
|---|---|---|
| fastmcp #4758 merged | GitHub search | Merged 7 Aug 2026 |
| 64 striped locks | `fastmcp_slim/fastmcp/server/event_store.py` on main | `_LOCK_STRIPES = 64`, `asyncio.Lock` keyed by `hash(stream_id)` |
| 4 of 5 events lost | PR #4758 body | Seen in the 5-write `asyncio.gather` reproduction, not in production |
| fastmcp #4705 merged | GitHub search | Merged 4 Aug 2026 |
| chroma #7560 | GitHub search | Open issue, filed by you; no fix PR |
| chroma #7559 | GitHub search | **Open, not merged** |
| XTXT "24-case conformance suite" | `conformance/cases/` | **12 cases** (24 files: one `.xtxt` input and one `.json` expected output each). Changed to "12-case". |
| XTXT "six more SDKs" | `sdk/` + CI | Python, JS, Rust, Java and C run the fixtures in CI. C++ wraps the C parser and only gets a smoke pass. The resume now says so. |
| XTXT adoption | repo | 1 star. I made no adoption claim. |
| Code agent | repo source | Checks below |

The code agent claims I checked in the source:
- Tree-sitter is set up with the **Python grammar only**.
- Embeddings come from Gemini `gemini-embedding-001`. Ranking is in-memory cosine similarity, not FAISS.
- Nothing in the code stops the agent "until the tests pass". The loop has `recursion_limit=50`, and testing comes from the prompt. I worded the bullet to match.
- The safety measures are real: workspace path-containment checks on read/write, shell only via `docker exec` with a timeout, and a fresh container per run.
- The repo has a single commit and no evaluation results, so the resume has none either.

Aamara details came from `SaiMouli3/techno_backend`:
- DRF + MySQL.
- `post_save` signals handle breakdowns, which create a pro-rated `Performs` entry.
- The 2M1P (two machines, one person) split.
- The `Externals` table holds rates and thresholds.
- `unique_together` constraints.

The code has **no** `transaction.atomic` or `select_for_update`, so I didn't add any concurrency or transaction claims for Aamara.

## Changes you asked for that I made
- Go is **not** in the skills list, as you asked. It shows up only where it's a fact: the XTXT Go reference parser.
- Tree-sitter moved out of the AI frameworks list. It now appears only as "Tree-sitter code indexing" in Version B.
- Dropped "microservices" because nothing on the resume backs it up. Added Django REST Framework, which the Aamara code uses.
- The page is A4, single column, about 625 words, and every bullet is at most 2 lines. Links still work.

## I couldn't fill these without inventing them. Please send the real answers.
NatWest (the section the checklist wants strongest):
1. Stack: language/framework, which LLM, which database engine, and how the schema is supplied (whole schema, retrieved subset, embeddings?).
2. What "validates against the schema" means: parse with sqlglot or similar? SELECT-only? A read-only DB user? Row limits or timeouts?
3. What happens on a failed or ambiguous query: retry with the error, ask a clarifying question, or just fail?
4. What the 3 min → 30 s figure measures (end-to-end dashboard response?) and the change that caused it (caching, query rewrites, pagination, async?).
5. Is it in production, and roughly how many users? Any accuracy or success-rate numbers?

Aamara:
6. What does "20,000 people" mean: workforce, registered users, or daily active users? One plant or several?
7. How was the 4 h → 30 min figure measured, and what changed (manual spreadsheet work → automated calculation?).

Pods Studio:
8. What does the 27% measure (repeat purchases, returning users, churn?), and over what period?
9. Payment fixes: which gateway was it, and was the root cause webhooks, transaction state, or something else?

Send these and I'll rewrite the NatWest section with real architecture detail. It's the biggest gap.

## Other things I noticed
- **Security:** the public repo `SaiMouli3/techno_backend` has a production MySQL hostname, username and password in its README. A `db.sqlite3` is committed too. Rotate that password and scrub it from the repo, which means rewriting git history.
- Your GitHub profile README gives a different email (`saimouli2023@`) from the resume (`saimouli12345678@`). Pick one.
- autonomous-code-agent has one commit and no eval. Running it on a few real repos and putting the results in the README (tasks tried, PRs opened, tests passing) would be the most convincing evidence you could add. I didn't push anything to your repos.

Rebuild: `python3 build.py` (writes the HTML, then `render.js` prints the PDFs).
