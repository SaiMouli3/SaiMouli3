<div align="center">

# Sai Mouli

**I build agents that read, fix, and ship code.**

<sub>Python · Go · TypeScript — LangGraph, MCP, Tree-sitter, Kubernetes</sub>

<br><br>

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)

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

[![Live demo](https://img.shields.io/badge/live-demo-1f6feb?style=flat-square)](https://saimouli3.github.io/xtxt/)
[![pkg.go.dev](https://img.shields.io/badge/pkg.go.dev-reference-00ADD8?style=flat-square&logo=go&logoColor=white)](https://pkg.go.dev/github.com/SaiMouli3/xtxt)
[![PyPI](https://img.shields.io/pypi/v/xtxt?style=flat-square&logo=pypi&logoColor=white&label=PyPI)](https://pypi.org/project/xtxt/)
[![npm](https://img.shields.io/npm/v/xtxt-js?style=flat-square&logo=npm&logoColor=white&label=npm)](https://www.npmjs.com/package/xtxt-js)
[![License](https://img.shields.io/github/license/SaiMouli3/xtxt?style=flat-square)](https://github.com/SaiMouli3/xtxt/blob/main/LICENSE)

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

[![fastmcp#4705](https://img.shields.io/badge/PrefectHQ%2Ffastmcp%234705-merged-8957e5?style=flat-square&logo=github&logoColor=white)](https://github.com/PrefectHQ/fastmcp/pull/4705)

`ResponseCachingMiddleware` cached every result it saw, including ones a tool returned with
`is_error=True`. A transient 503 or a rate-limit got pinned for the full hour-long TTL, so
every later call replayed the stale failure and the tool never ran again. Added the guard
alongside the passthroughs that already encode the same idea — some results describe a
moment, not an answer — plus tests covering the retry path.

[![chroma#7559](https://img.shields.io/badge/chroma--core%2Fchroma%237559-open-2da44e?style=flat-square&logo=github&logoColor=white)](https://github.com/chroma-core/chroma/pull/7559)

Two API implementations annotated a return type as the string `"IndexingStatus"` without importing
the name. Because the annotation was a string, the missing import stayed invisible at
import time and only surfaced once something resolved type hints. Traced it to both call
sites, fixed, and added a regression test that needs no cluster to run.

Two more up at fastmcp: [#4706](https://github.com/PrefectHQ/fastmcp/pull/4706) adds RFC
6570 explode support for list-typed query parameters, and
[#4758](https://github.com/PrefectHQ/fastmcp/pull/4758) serializes a read-modify-write race
in the event store's stream list. Also reading the tracker at
**[pydantic](https://github.com/pydantic/pydantic)**.

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
