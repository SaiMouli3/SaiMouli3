# Resume revision notes

## Design (per the template spec)
- A4, one page, single column, white background. Margins 0.55 in (top/bottom) and 0.6 in (sides).
- Font: Calibri. The embedded font is Carlito, which has the same metrics as Calibri. Name 22 pt, title 11 pt, section headings 10.5 pt, entry titles 10 pt, body and dates 9.5 pt.
- Colours: #17212B text, #16324F headings, #505C68 secondary text, #687583 dates, #DCE2E8 dividers. It still reads correctly in black and white.
- Section order: Summary, Experience, Open-Source Contributions, Projects, Technical Skills, Education.
- No tables, icons, text boxes or header/footer content. Bullets are a real "•" character in the text.

Three spec items I compressed to keep the page to one page without dropping body text below 9.5 pt:
- Location and dates sit right-aligned on the title line, not on a line of their own.
- Education is one line.
- Databases and Infrastructure share one skills row.

ATS check: `pdftotext` extraction gives the correct reading order with readable headings and dates. Both fonts are embedded TrueType with Unicode maps. All 13 links survive: email, phone, GitHub, LinkedIn, portfolio, 2 repos and 6 PR/issue links. This doesn't guarantee that every ATS will parse the PDF correctly.

## Open-source status, checked on GitHub (5 Nov 2026)
| Contribution | Status | On resume |
|---|---|---|
| PrefectHQ/fastmcp #4758 | Merged 7 Aug 2026 | Yes |
| PrefectHQ/fastmcp #4705 | Merged 4 Aug 2026 | Yes |
| stanfordnlp/dspy #10720 | Merged 27 Oct 2026 | Yes (new) |
| chroma-core/chroma issue #7560 | Open | Yes |
| chroma-core/chroma #7559 | Open, not merged | Yes, as "open" |
| 567-labs/instructor #2846 | Open | Yes, as "open" (new) |
| PrefectHQ/fastmcp #4706 | Closed, not merged | No |
| modelcontextprotocol/python-sdk #3749, #3750 | Closed, not merged | No |

## Projects
- **Removed:** Autonomous Code Agent.
- **Added: Zippyy** (`SaiMouli3/zippyy`). All 15 commits are yours. I ran the backend suite: **145 passed, 5 skipped**. The skipped tests need a real Postgres.
  - The resume uses only what's in the code and README: webhook inbox with de-duplication and signature checks, durable agent workflows that act through typed tools, a 14-rule deterministic policy engine, LLM calls only for replies the rules are unsure about, row-level security, and SKIP LOCKED job leases.
  - The README says live WhatsApp and voice providers are untested and the carriers are mocks, so the resume claims no users and no production use.
  - The repo is **private**, so recruiters will get a 404 on the link. Make it public, or remove the link.
- **Not used:** `jarvis` ("Mai"). It's a fork of Slopedrop's MIT-licensed Contop: 57 of the 70 commits are by another author.
- **Not used:** `switch`. It's a copy of sandbox-quantum/switch.

## Still needs your input (nothing invented)
1. NatWest: the stack, how the SQL is checked (parser? SELECT-only? read-only user?), how failed or ambiguous questions are handled, what the 3 min → 30 s figure measures, and whether it's in production and with how many users.
2. Aamara: what "20,000 people" means, and how the 4 h → 30 min figure was measured.
3. Pods: what the 27% measures and over what period, and the payment gateway or root cause.
4. XTXT: the original resume said "24-case"; the repo has **12** cases (24 files). The resume says 12.

## Security
- `SaiMouli3/techno_backend` (public) has a production MySQL hostname, username and password in its README. Rotate the password, then scrub it from the git history.

Rebuild: `python3 build.py` (writes the HTML, then `render.js` prints the PDFs).
