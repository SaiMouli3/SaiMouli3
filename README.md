<div align="center">

# Sai Mouli

**I build agents that read, fix, and ship code.**

<sub>Python · Go · TypeScript — LangGraph, MCP, Tree-sitter, Kubernetes</sub>

</div>

<br>

Most of my work sits at the point where a language model stops being a chat window and
starts being a process: an isolated sandbox, a real tool surface, retrieval over an
actual repository, and a pull request at the end of it. Lately I've been taking the
same interest upstream, into the libraries that make that possible.

<br>

---

## Selected work

### [xtxt](https://github.com/SaiMouli3/xtxt) · Go

**Plain text that machines can read — without guessing.**

Markdown makes an agent infer structure from prose. XTXT lets the document carry it:
images, tables, charts, and typed records in a file that still opens in any editor and
diffs cleanly in git. A written spec, a reference parser, and seven implementations.

<sub>[Live demo](https://saimouli3.github.io/xtxt/) · [pkg.go.dev](https://pkg.go.dev/github.com/SaiMouli3/xtxt) · [PyPI](https://pypi.org/project/xtxt/) · [npm](https://www.npmjs.com/package/xtxt-js)</sub>

<br>

### [autonomous-code-agent](https://github.com/SaiMouli3/autonomous-code-agent) · Python

**Give it a repo URL and a task. It opens the pull request.**

Clones into an isolated Docker sandbox, chunks the codebase with Tree-sitter, retrieves
the relevant functions by embedding similarity, edits, runs the tests, and pushes a real
PR. Every capability the agent has is exposed through an MCP server — so the tool surface
is inspectable, not buried in a prompt.

<br>

### [AI-Powered-Debugging-Agent](https://github.com/SaiMouli3/AI-Powered-Debugging-Agent) · Python

**A debugging pipeline that remembers.**

Five specialized agents in sequence: log parsing, root-cause analysis, fix generation,
validation against the test suite, then the PR. Past incidents land in a FAISS vector
store, so the system gets sharper on failure modes it has already seen. Works across
OpenAI, Claude, and Gemini.

<br>

### [Federated-Learning-Kube](https://github.com/SaiMouli3/Federated-Learning-Kube) · Python · Kubernetes

**Distributed training where the data never leaves the client.**

Clients train locally and publish only model updates; the server aggregates them into a
shared model. Kubernetes handles orchestration and scaling across the fleet.

<br>

---

## Open source

Contributing back to the infrastructure I build on.

**[chroma-core/chroma#7559](https://github.com/chroma-core/chroma/pull/7559)** — Two API
implementations annotated a return type as the string `"IndexingStatus"` without importing
the name. Because the annotation was a string, the missing import stayed invisible at
import time and only surfaced once something resolved type hints. Traced it to both call
sites, fixed, and added a regression test that needs no cluster to run.

Also working through the trackers at **[pydantic](https://github.com/pydantic/pydantic)**
and **[fastmcp](https://github.com/jlowin/fastmcp)**.

<br>

---

## Elsewhere

Also building **[SecurePass](https://github.com/SaiMouli3/SecurePass)**, a password vault
that encrypts client-side so the server never sees a credential, and
**[BankStatement_Extraction](https://github.com/SaiMouli3/BankStatement_Extraction)** —
template-free statement parsing with OCR fallback, balance-reconciliation checks, and a
per-transaction confidence score.

<br>

<div align="center">
<sub>

[saimouli2023@gmail.com](mailto:saimouli2023@gmail.com)

</sub>
</div>
