"""Build both resume versions (A: backend, B: applied AI) as HTML, then A4 PDFs.

Usage: python3 build.py   (writes HTML here, then render.js prints A4 PDFs via Playwright)
Every fact is shared between versions; only title, summary, ordering and emphasis differ.
"""
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent

GH = "https://github.com"
FM = f"{GH}/PrefectHQ/fastmcp/pull"
CH = f"{GH}/chroma-core/chroma"


def link(href, text):
    return f'<a href="{href}">{text}</a>'


HEADER = f"""
<header>
  <h1>A SAI MOULI</h1>
  <p class="title">{{role}}</p>
  <p class="contact">Bengaluru, India &nbsp;|&nbsp; {link("tel:+918919554720", "+91 89195 54720")} &nbsp;|&nbsp;
    {link("mailto:saimouli12345678@gmail.com", "saimouli12345678@gmail.com")}</p>
  <p class="contact">GitHub: {link(f"{GH}/SaiMouli3", "github.com/SaiMouli3")} &nbsp;|&nbsp;
    LinkedIn: {link("https://linkedin.com/in/saimouli036", "linkedin.com/in/saimouli036")} &nbsp;|&nbsp;
    Portfolio: {link("https://sai-mouli-portfolio.vercel.app", "sai-mouli-portfolio.vercel.app")}</p>
</header>"""


def entry(left, right, bullets, cls=""):
    lis = "".join(f'<li><span class="dot">&bull;</span>{b}</li>' for b in bullets)
    return (f'<div class="entry {cls}"><div class="head"><span class="name">{left}</span>'
            f'<span class="meta">{right}</span></div><ul>{lis}</ul></div>')


def line_entry(org, text, right):
    return (f'<div class="entry"><div class="head"><span><span class="name">{org}</span> &nbsp;|&nbsp; {text}</span>'
            f'<span class="meta">{right}</span></div></div>')


def section(name, body):
    return f"<section><h2>{name}</h2>{body}</section>"


# ---------------- summary ----------------
SUMMARY = {
    "backend": ("Backend engineer at NatWest Group, building backend APIs and a natural-language-to-SQL service over a "
                "136-table reporting database. Builds multi-tenant FastAPI/PostgreSQL systems with policy-gated agent "
                "workflows; merged fixes into FastMCP and DSPy."),
    "ai": ("Applied AI engineer at NatWest Group: built a natural-language-to-SQL engine over a 136-table reporting "
           "database, shipped as a dashboard chatbot. Builds policy-gated agent workflows and MCP tooling; merged "
           "fixes into FastMCP and DSPy."),
}

# ---------------- experience ----------------
NW_SQL = ("Built a natural-language-to-SQL engine over a <b>136-table</b> reporting database: it turns a plain-English "
          "question into SQL, validates the query against the schema before it runs, executes it, and returns the answer with a chart.")
NW_BOT = ("Shipped the engine as a chatbot in the analytics dashboard, so stakeholders pull ad-hoc reports themselves.")
NW_PERF = ("Cut large-query dashboard response time from <b>~3 min to under 30 s</b> by reworking the backend "
           "APIs and data path.")

AA_SYS = ("Built the backend of Techno Rings&rsquo; shop-floor operations system, used by <b>20,000 people</b>, on Django "
          "REST Framework and MySQL with a React front end: machine assignment, shift logging and tool-life tracking.")
AA_RULES = ("Implemented payroll exception paths as model-level rules: breakdowns pro-rate shift and target, and workers "
            "move to another machine&rsquo;s job. Daily processing fell from <b>about four hours to under thirty minutes</b>.")

PODS = ("Moved customer email outreach onto event-driven Celery tasks and cron jobs, removing the manual send "
        "step (retention up <b>27%</b>); root-caused and fixed customer-reported failed in-app payments.")


def experience(order):
    nw = [NW_SQL, NW_BOT, NW_PERF] if order == "ai" else [NW_PERF, NW_SQL, NW_BOT]
    return section("Experience",
        entry("Software Engineer | NatWest Group", "Bengaluru, India | Jul 2025 &ndash; Present", nw) +
        entry("Backend Developer Intern | Aamara Technologies", "Bengaluru, India | Mar 2024 &ndash; Aug 2024",
              [AA_SYS, AA_RULES]) +
        entry("Software Development Intern | Pods Studio", "Bengaluru, India | Nov 2023 &ndash; Dec 2023", [PODS]))


# ---------------- open source ----------------
def open_source():
    fastmcp = [
        f"<b>{link(f'{FM}/4758', 'PR #4758')} (merged):</b> fixed a lost-update race in the event store (a "
        "five-concurrent-write reproduction kept 1 of 5 event IDs); after maintainer review, replaced a store-wide "
        "lock with <b>64 striped asyncio locks</b> keyed by stream ID.",
        f"<b>{link(f'{FM}/4705', 'PR #4705')} (merged):</b> stopped the response cache storing is_error "
        "results, which pinned a transient 503 for a full hour.",
    ]
    dspy = (f"<b>{link(f'{GH}/stanfordnlp/dspy/pull/10720', 'PR #10720')} (merged):</b> fixed dspy.majority() "
            "raising TypeError when voting on non-string values")
    chroma = [f"<b>{link(f'{CH}/issues/7560', 'Issue #7560')}:</b> showed the CI lint job could never fail "
              "(continue-on-error plus bash -e meant black, flake8 and prettier never ran). "
              f"<b>{link(f'{CH}/pull/7559', 'PR #7559')} (open)</b> proposes a fix for two undefined-name defects it hid."]
    instructor = (f"<b>{link(f'{GH}/567-labs/instructor/pull/2846', 'PR #2846')} (open):</b> renders context "
                  "placeholders in input_text parts that reached the model raw")
    return section("Open-Source Contributions",
        entry("PrefectHQ/fastmcp", "2 PRs merged", fastmcp) +
        line_entry("stanfordnlp/dspy", dspy, "1 PR merged") +
        entry("chroma-core/chroma", "1 issue, 1 open PR", chroma) +
        line_entry("567-labs/instructor", instructor, "1 open PR"))


# ---------------- projects ----------------
ZIPPYY = entry(
    "Zippyy | Python, FastAPI, PostgreSQL, Redis, Next.js",
    link(f"{GH}/SaiMouli3/zippyy", "github.com/SaiMouli3/zippyy"),
    ["Built a multi-tenant delivery-recovery platform: signed carrier, WhatsApp and voice webhooks are de-duplicated "
     "into an inbox, drive a shipment state machine, and wake durable agent workflows that act only through typed tools.",
     "Every carrier action must pass a deterministic 14-rule policy engine, and the LLM reads only replies the rule "
     "extractor is unsure of. Per-merchant row-level security, SKIP LOCKED job leases; 145 tests pass."])

XTXT = entry(
    "XTXT | Go, Python, JavaScript, Rust, Java, C",
    link(f"{GH}/SaiMouli3/xtxt", "github.com/SaiMouli3/xtxt"),
    ["Designed a plain-text document format where structure is explicit syntax: directives carry images, tables, "
     "charts and typed records that the CLI extracts as JSON, while files still diff cleanly in Git.",
     "Wrote the spec, a Go reference parser and CLI, and a 12-case conformance suite the Python, JS, Rust, Java and "
     "C SDKs run in CI; published to PyPI and npm, with a VS Code extension and MCP server."])


def projects(order):
    return section("Projects", ZIPPYY + XTXT)


# ---------------- skills ----------------
def skills(order):
    backend = ("Backend Engineering", "FastAPI, Django, Django REST Framework, Flask, SQLAlchemy, REST APIs, WebSockets, Celery")
    ai = ("AI Engineering", "LangGraph, LangChain, MCP servers, RAG pipelines, embeddings, FAISS")
    rows = [("Languages", "Python, C++, SQL")]
    rows += [backend, ai] if order == "backend" else [ai, backend]
    rows += [("Databases &amp; Infrastructure", "PostgreSQL, MySQL, Redis, AWS, Docker, Kubernetes, Linux, Git, GitHub Actions"),
             ("Engineering Practices", "asyncio concurrency, database transactions, pytest, API design, performance optimization")]
    body = "".join(f"<p><b>{k}:</b> {v}</p>" for k, v in rows)
    return section("Technical Skills", f'<div class="skills">{body}</div>')


EDUCATION = section("Education",
    '<div class="entry"><div class="head"><span><span class="name">Ramaiah Institute of Technology</span> &nbsp;|&nbsp; '
    'B.Tech, Computer Science and Engineering &nbsp;|&nbsp; CGPA: 9.06/10</span>'
    '<span class="meta">2021 &ndash; 2025</span></div></div>')

CSS = """
@page { size: A4; margin: 0.55in 0.6in; }
:root { --text: #17212B; --head: #16324F; --sub: #505C68; --meta: #687583; --rule: #DCE2E8; }
* { box-sizing: border-box; }
html, body { background: #FFFFFF; }
body { margin: 0; color: var(--text); font-family: Calibri, Carlito, Arial, Helvetica, sans-serif;
       font-size: 9.5pt; line-height: 1.2; }
a { color: inherit; text-decoration: none; }
p { margin: 0; }
b { font-weight: 700; }
header { margin-bottom: 12pt; }
h1 { margin: 0; font-size: 22pt; font-weight: 700; letter-spacing: 0.4pt; line-height: 1; color: var(--text); }
.title { margin: 3pt 0 4pt; font-size: 11pt; color: var(--head); }
.contact { font-size: 9.5pt; color: var(--sub); line-height: 1.25; }
section { margin-top: 9pt; }
section:first-of-type { margin-top: 0; }
h2 { margin: 0 0 4pt; padding-bottom: 1.5pt; border-bottom: 0.5pt solid var(--rule);
     font-size: 10.5pt; font-weight: 700; letter-spacing: 0.8pt; text-transform: uppercase; color: var(--head); }
.entry { margin-bottom: 6pt; }
.entry:last-child { margin-bottom: 0; }
.head { display: flex; justify-content: space-between; align-items: baseline; gap: 12pt; }
.name { font-size: 10pt; font-weight: 700; color: var(--text); }
.meta { font-size: 9.5pt; color: var(--meta); white-space: nowrap; }
ul { margin: 1pt 0 0; padding: 0; list-style: none; }
li { margin-bottom: 2pt; padding-left: 10pt; position: relative; }
.dot { position: absolute; left: 1pt; color: var(--sub); }
li:last-child { margin-bottom: 0; }
.skills p { margin-bottom: 2pt; }
.sub { color: var(--sub); margin-top: 1pt; }
"""


def page(order, role):
    parts = [HEADER.format(role=role),
             section("Professional Summary", f"<p>{SUMMARY[order]}</p>"),
             experience(order), open_source(), projects(order), skills(order), EDUCATION]
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
