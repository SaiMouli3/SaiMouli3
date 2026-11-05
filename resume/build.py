"""Build both resume versions (A: backend, B: applied AI) as HTML, then A4 PDFs.

Usage: python3 build.py   (writes HTML here, then render.js prints A4 PDFs via Playwright)
Every fact is shared between versions; only title, summary, ordering and emphasis differ.
"""
import re
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent

GH = "https://github.com"
FM = f"{GH}/PrefectHQ/fastmcp/pull"
CH = f"{GH}/chroma-core/chroma"


def link(href, text):
    return f'<a href="{href}">{text}</a>'


def icon(name):
    """Inline SVG icon (vector graphic, not text, so ATS text extraction is unaffected)."""
    svg = (OUT / "icons" / f"{name}.svg").read_text()
    svg = re.sub(r"<!--.*?-->|<title>.*?</title>", "", svg, flags=re.S)
    head, rest = svg.split(">", 1)  # strip sizing only from the root <svg> tag, not from child shapes
    svg = re.sub(r"\s(class|width|height|role)=\"[^\"]*\"", "", head) + ">" + rest
    filled = "simple" if 'fill="none"' not in svg else "line"
    return svg.replace("<svg", f'<svg class="ic {filled}" aria-hidden="true"', 1)


def logo(slug):
    """Company logo from resume/logos/<slug>.(svg|png|jpg), embedded as a data URI. Empty if the file is absent."""
    import base64
    for ext, mime in (("svg", "image/svg+xml"), ("png", "image/png"), ("jpg", "image/jpeg")):
        f = OUT / "logos" / f"{slug}.{ext}"
        if f.exists():
            data = base64.b64encode(f.read_bytes()).decode()
            return f'<img class="logo" alt="" src="data:{mime};base64,{data}">'
    return ""


def contact(name, href, text):
    inner = f"{icon(name)}{text}"
    return f'<span class="ci">{link(href, inner) if href else inner}</span>'


HEADER = f"""
<header>
  <h1>A SAI MOULI</h1>
  <p class="title">{{role}}</p>
  <p class="contact">{contact("map-pin", None, "Bengaluru, India")}{contact("phone", "tel:+918919554720", "+91 89195 54720")}{contact("mail", "mailto:saimouli12345678@gmail.com", "saimouli12345678@gmail.com")}</p>
  <p class="contact">{contact("github", f"{GH}/SaiMouli3", "github.com/SaiMouli3")}{contact("linkedin", "https://linkedin.com/in/saimouli036", "linkedin.com/in/saimouli036")}{contact("globe", "https://sai-mouli-portfolio.vercel.app", "sai-mouli-portfolio.vercel.app")}</p>
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
    "backend": ("Software engineer at NatWest Group building backend APIs and data pipelines for an observability "
                "platform and an AI analytics engine over a 136-table database. Builds policy-gated agent systems on "
                "FastAPI/PostgreSQL; merged fixes into FastMCP and DSPy."),
    "ai": ("Applied AI engineer at NatWest Group: built a text-to-SQL analytics engine over a 136-table database, "
           "shipped as a dashboard chatbot, plus observability data pipelines. Builds policy-gated agents and MCP "
           "tooling; merged fixes into FastMCP and DSPy."),
}

# ---------------- experience ----------------
NW_OBS = ("Developed backend APIs and data pipelines for the <b>SCO Observability Platform</b>, letting internal "
          "banking teams monitor applications and track customer journeys end to end across interconnected systems.")
NW_EVT = ("Built data processing for application lifecycle events and technical observability data, giving analytics "
          "and quality-control teams visibility into application status and workflow progress to investigate issues.")
NW_SQL = ("Built an AI natural-language analytics engine over a <b>136-table</b> reporting database: a text-to-SQL "
          "workflow generates SQL from plain English, validates it against the schema, executes it and charts the result.")
NW_BOT = ("Integrated the engine into the dashboard as a chatbot for self-service reporting, replacing ad-hoc query "
          "requests to engineers.")
NW_PERF = ("Optimized backend APIs and data-processing workflows, cutting large dashboard queries from "
           "<b>~3 minutes to under 30 seconds</b>.")

AA_SYS = ("Built the backend of Techno Rings&rsquo; shop-floor operations system, used by <b>20,000 people</b>, on Django "
          "REST Framework and MySQL with a React front end: machine assignment, shift logging and tool-life tracking.")
AA_RULES = ("Implemented payroll exception paths as model-level rules: breakdowns pro-rate shift and target, and workers "
            "move to another machine&rsquo;s job. Daily processing fell from <b>about four hours to under thirty minutes</b>.")

PODS = ("Moved customer email onto event-driven Celery/cron triggers (retention up <b>27%</b>); debugged and "
        "fixed failed in-app payments.")


def experience(order):
    nw = ([NW_SQL, NW_BOT, NW_OBS, NW_EVT, NW_PERF] if order == "ai"
          else [NW_OBS, NW_EVT, NW_PERF, NW_SQL, NW_BOT])
    return section("Experience",
        entry(f"{logo('natwest')}Software Engineer | NatWest Group", "Bengaluru, India | Jul 2025 &ndash; Present", nw) +
        entry("Backend Developer Intern | Aamara Technologies", "Bengaluru, India | Mar 2024 &ndash; Aug 2024",
              [AA_SYS, AA_RULES]) +
        entry(f"{logo('pods-studio')}Software Development Intern | Pods Studio", "Bengaluru, India | Nov 2023 &ndash; Dec 2023", [PODS]))


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
    chroma = (f"<b>{link(f'{CH}/issues/7560', 'Issue #7560')}:</b> showed CI lint could never fail; "
              f"<b>{link(f'{CH}/pull/7559', 'PR #7559')} (open)</b> fixes two hidden bugs")
    instructor = (f"<b>{link(f'{GH}/567-labs/instructor/pull/2846', 'PR #2846')} (open):</b> renders context "
                  "placeholders in input_text parts that reached the model raw")
    return section("Open-Source Contributions",
        entry("PrefectHQ/fastmcp", "2 PRs merged", fastmcp) +
        line_entry("stanfordnlp/dspy", dspy, "1 PR merged") +
        line_entry("chroma-core/chroma", chroma, "1 issue, 1 open PR") +
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
    ["Designed a plain-text format whose directives carry images, tables, charts and typed records as JSON-extractable data.",
     "Wrote the spec, Go reference parser and a 12-case conformance suite run in CI by 5 SDKs; published to PyPI and npm."])


def projects(order):
    return section("Projects", ZIPPYY + XTXT)


# ---------------- skills ----------------
def skills(order):
    backend = ("Backend Engineering", "FastAPI, Django, Django REST Framework, Flask, SQLAlchemy, REST APIs, data pipelines, WebSockets, Celery")
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
.contact { font-size: 9.5pt; color: var(--sub); line-height: 1.38; }
.ci { white-space: nowrap; margin-right: 13pt; }
.ci:last-child { margin-right: 0; }
.ic { width: 9pt; height: 9pt; vertical-align: -1.3pt; margin-right: 3.5pt; color: var(--head); }
.ic.simple { fill: var(--head); }
.ic.line { stroke: var(--head); stroke-width: 2.2; }
section { margin-top: 9pt; }
section:first-of-type { margin-top: 0; }
h2 { margin: 0 0 4pt; padding-bottom: 1.5pt; border-bottom: 0.5pt solid var(--rule);
     font-size: 10.5pt; font-weight: 700; letter-spacing: 0.8pt; text-transform: uppercase; color: var(--head); }
.entry { margin-bottom: 6pt; }
.entry:last-child { margin-bottom: 0; }
.head { display: flex; justify-content: space-between; align-items: baseline; gap: 12pt; }
.name { font-size: 10pt; font-weight: 700; color: var(--text); }
.logo { height: 10pt; width: auto; max-width: 40pt; vertical-align: -2pt; margin-right: 5pt; }
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
