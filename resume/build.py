"""Build both resume versions (A: backend, B: applied AI) as HTML, then A4 PDFs.

Usage: python3 build.py   (writes HTML here, then render.js prints A4 PDFs via Playwright)
Every fact is shared between versions; only ordering and emphasis differ.
"""
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent

HEADER = """
<header>
  <h1>A SAI MOULI</h1>
  <div class="role">{role}</div>
  <div class="contact">Bengaluru, India &middot; <a href="tel:+918919554720">+91 89195 54720</a> &middot;
  <a href="mailto:saimouli12345678@gmail.com">saimouli12345678@gmail.com</a></div>
  <div class="contact"><a href="https://github.com/SaiMouli3">github.com/SaiMouli3</a> &middot;
  <a href="https://linkedin.com/in/saimouli036">linkedin.com/in/saimouli036</a> &middot;
  <a href="https://sai-mouli-portfolio.vercel.app">sai-mouli-portfolio.vercel.app</a></div>
</header>"""


def job(title, org, dates, bullets):
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    return (f'<div class="item"><div class="row"><span><b>{title}</b> | {org}</span>'
            f'<span class="date">{dates}</span></div><ul>{lis}</ul></div>')


def heading(left, right):
    return f'<div class="row"><span>{left}</span>{right}</div>'


def section(name, body):
    return f"<section><h2>{name}</h2>{body}</section>"


# ---------------- experience ----------------
NW_SQL = ("Built a natural-language-to-SQL engine over a <b>136-table</b> reporting database: it turns a plain-English "
          "question into SQL, validates it against the schema before it runs, executes it, and returns the answer with a chart.")
NW_BOT = ("Shipped it as a chatbot in the analytics dashboard; stakeholders pull ad-hoc reports without an engineering ticket.")
NW_PERF = ("Cut dashboard response time on large queries from <b>~3 min to under 30 s</b> by reworking the backend "
           "APIs and data-processing path.")

AA_SYS = ("Built the backend of Techno Rings&rsquo; shop-floor operations system, used by <b>20,000 people</b> (Django REST "
          "Framework, MySQL, React): worker&ndash;machine assignment, shift logging, tool-life tracking, shift reports.")
AA_RULES = ("Implemented the payroll exception paths as model-level rules: a breakdown pro-rates shift and target, the worker "
            "moves to another machine&rsquo;s job, and a day with every machine already staffed records no wage.")
AA_DATA = ("Moved pay rates and thresholds into a config table and enforced assignment uniqueness with DB constraints; "
           "daily processing fell from <b>about four hours to under thirty minutes</b>.")

PODS_EMAIL = ("Replaced the manual customer-email send step with event-driven Celery tasks and cron jobs; "
              "retention improved <b>27%</b>.")
PODS_PAY = "Reproduced, root-caused and fixed customer-reported failed in-app payments, owning each from report to patch."


def experience(order):
    nw = [NW_SQL, NW_BOT, NW_PERF] if order == "ai" else [NW_PERF, NW_SQL, NW_BOT]
    return section("Experience",
        job("Software Engineer", "NatWest Group, Bengaluru", "July 2025 &ndash; Present", nw) +
        job("Backend Developer Intern", "Aamara Technologies, Bengaluru", "March &ndash; August 2024",
            [AA_SYS, AA_RULES, AA_DATA]) +
        job("Software Development Intern", "Pods Studio, Bengaluru", "Nov &ndash; Dec 2023",
            [PODS_EMAIL, PODS_PAY]))


# ---------------- open source ----------------
FM_4758 = ("<b>#4758 (merged):</b> fixed a lost-update race where two tasks read-modify-wrote one stream&rsquo;s event list; "
           "a five-concurrent-write repro kept 1 of 5 IDs. Fixed the race, not the <code>FileNotFoundError</code> it surfaced.")
FM_LOCK = ("After maintainer review, replaced the store-wide lock with <b>64 striped asyncio locks</b> keyed by stream ID, "
           "so unrelated sessions don&rsquo;t serialize; the regression test forces the interleave.")
FM_4705 = ("<b>#4705 (merged):</b> the response cache stored <code>is_error=True</code> results, replaying a transient 503 "
           "for the full one-hour TTL. Added a no-cache guard for error results, with retry-path tests.")
CH_7560 = ("<b>Issue #7560:</b> showed the CI lint job could never fail: the step set <code>continue-on-error</code> and "
           "hooks ran under <code>bash -e</code>, so the first failure skipped the rest; black, flake8, prettier never ran.")
CH_7559 = ("<b>PR #7559 (open):</b> proposes a fix for two undefined-name (F821) defects that step hid, a missing import "
           "raising <code>NameError</code> under <code>typing.get_type_hints()</code>; with a regression test.")


def open_source():
    return section("Open Source",
        '<div class="item">' + heading("<b>PrefectHQ/fastmcp</b> | Python framework for MCP servers and clients",
                                       '<span class="date">2 PRs merged</span>') +
        f"<ul><li>{FM_4758}</li><li>{FM_LOCK}</li><li>{FM_4705}</li></ul></div>"
        '<div class="item">' + heading("<b>chroma-core/chroma</b> | open-source vector database",
                                       '<span class="date">1 issue, 1 open PR</span>') +
        f"<ul><li>{CH_7560}</li><li>{CH_7559}</li></ul></div>")


# ---------------- projects ----------------
XTXT = ('<div class="item">' + heading(
    "<b>XTXT</b> | plain-text document format | Go reference parser + SDKs",
    '<a class="date" href="https://github.com/SaiMouli3/xtxt">github.com/SaiMouli3/xtxt</a>') +
    "<ul><li>Structure is explicit syntax, not inferred from prose: <code>@name</code> directives carry images, tables, "
    "charts and typed records, and <code>xtxt extract</code> returns them as JSON. Files stay plain text and diff cleanly in Git.</li>"
    "<li>Wrote the spec, a Go parser and CLI, and a 12-case conformance suite (expected AST + diagnostics) that the Python, "
    "JS, Rust, Java and C SDKs run in CI. Published to PyPI and npm; VS Code extension and MCP server.</li></ul></div>")

AGENT = ('<div class="item">' + heading(
    "<b>Autonomous Code Agent</b> | LangGraph, MCP, Tree-sitter, Docker",
    '<a class="date" href="https://github.com/SaiMouli3/autonomous-code-agent">github.com/SaiMouli3/autonomous-code-agent</a>') +
    "<ul><li>Given a repo URL and a task, runs a LangGraph ReAct agent in a fresh Docker container per run; it edits, runs "
    "the tests, then branches, commits, pushes and opens a PR through GitHub&rsquo;s MCP server.</li>"
    "<li>Built its MCP tool server: file access is path-checked to the workspace, shell runs only in the container, and code "
    "search ranks Tree-sitter function/class chunks by embedding similarity, returning file:line ranges.</li></ul></div>")


def projects(order):
    return section("Projects", XTXT + AGENT if order == "backend" else AGENT + XTXT)


# ---------------- skills ----------------
BACKEND = ("Backend", "FastAPI, Django, Django REST Framework, Flask, REST APIs, WebSockets, Celery")
DATA = ("Data &amp; Infra", "PostgreSQL, MySQL, Redis, AWS, Docker, Kubernetes, Linux, Git, GitHub Actions")
PRACTICE = ("Practices", "asyncio concurrency, pytest regression tests, API design, performance optimization")


def skills(order):
    ai = ("AI Engineering", "LangGraph, LangChain, MCP servers, RAG pipelines, embeddings, FAISS"
          + (", Tree-sitter code indexing" if order == "ai" else ""))
    rows = [("Languages", "Python, C++, SQL")]
    rows += [BACKEND, DATA, ai, PRACTICE] if order == "backend" else [ai, BACKEND, DATA, PRACTICE]
    body = "".join(f"<div><b>{k}:</b> {v}</div>" for k, v in rows)
    return section("Technical Skills", f'<div class="skills">{body}</div>')


EDUCATION = section("Education", heading(
    "<b>Ramaiah Institute of Technology</b> | B.Tech, Computer Science and Engineering | CGPA 9.06/10",
    '<span class="date">2021 &ndash; 2025</span>'))

CSS = """
@page { size: A4; margin: 10mm 13mm; }
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif; font-size: 8.8pt;
       line-height: 1.36; color: #1a1a1a; background: #fff; }
a { color: inherit; text-decoration: none; }
header { text-align: center; margin-bottom: 6pt; }
h1 { font-size: 17pt; letter-spacing: 1.5pt; margin: 0; font-weight: 700; }
.role { font-size: 10pt; font-weight: 500; margin: 1pt 0 3pt; color: #333; }
.contact { font-size: 8.5pt; color: #333; }
h2 { font-size: 9.5pt; letter-spacing: 1pt; text-transform: uppercase; margin: 8pt 0 3pt;
     padding-bottom: 1.5pt; border-bottom: 0.8pt solid #1a1a1a; font-weight: 700; }
.item { margin-bottom: 5pt; }
.row { display: flex; justify-content: space-between; gap: 10pt; }
.date { white-space: nowrap; color: #333; }
ul { margin: 1.5pt 0 0; padding-left: 12pt; }
li { margin-bottom: 1.8pt; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 7.9pt; }
.skills div { margin-bottom: 1.5pt; }
"""


def page(order, role):
    parts = [HEADER.format(role=role), experience(order)]
    parts += [open_source(), projects(order)] if order == "backend" else [projects(order), open_source()]
    parts += [skills(order), EDUCATION]
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>A Sai Mouli Resume</title>'
            f"<style>{CSS}</style></head><body>{''.join(parts)}</body></html>")


VERSIONS = {
    "Sai_Mouli_Resume_A_Backend": ("backend", "Backend Software Engineer"),
    "Sai_Mouli_Resume_B_Applied_AI": ("ai", "Applied AI Engineer"),
}

if __name__ == "__main__":
    for name, (order, role) in VERSIONS.items():
        (OUT / f"{name}.html").write_text(page(order, role), encoding="utf-8")
    subprocess.run(["node", str(OUT / "render.js")], check=True)
