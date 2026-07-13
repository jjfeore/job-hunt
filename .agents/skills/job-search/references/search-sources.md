# Search sources and query recipes

Login-free sources for job postings, with URL patterns and search recipes. Load this
before running searches in the job-search skill.

## Direct ATS job boards

These host thousands of company boards, are publicly readable, and give canonical
application URLs — always prefer capturing these URLs over aggregator links.

| Platform | Board URL pattern | Search recipe |
|---|---|---|
| Greenhouse | `boards.greenhouse.io/<company>` or `job-boards.greenhouse.io/<company>` | web search: `site:boards.greenhouse.io "<title>"` (also try `site:job-boards.greenhouse.io`) |
| Lever | `jobs.lever.co/<company>` | web search: `site:jobs.lever.co "<title>" <keyword>` |
| Ashby | `jobs.ashbyhq.com/<company>` | web search: `site:jobs.ashbyhq.com "<title>" <keyword>` |
| SmartRecruiters | `careers.smartrecruiters.com/<Company>` | web search: `site:careers.smartrecruiters.com "<title>"` |
| Workable | `apply.workable.com/<company>` | web search: `site:apply.workable.com "<title>"` |
| Rippling ATS | `ats.rippling.com/<company>/jobs` | web search: `site:ats.rippling.com "<title>"` |
| Workday | `<company>.wd1.myworkdayjobs.com/...` (wd1/wd2/wd3/wd5 vary) | web search: `site:myworkdayjobs.com "<title>" <keyword>` |
| iCIMS | `careers-<company>.icims.com` | web search: `site:icims.com "<title>"` |

Notes:

- Site-scoped queries return individual postings directly. Vary the title phrasing across
  queries; boards use the company's own titles.
- Greenhouse and Lever board pages list ALL open roles for a company — when a company
  matches the user's stage/size preferences, scan its whole board, not just the one hit.

## Careers pages and aggregators

- Company careers pages: for any company named in the criteria's preferred sources or
  known to match the user's stage/size preference, check `<company site>/careers` directly.
- Hacker News "Who is hiring" monthly threads — search via `hn.algolia.com` for the
  current month's thread plus keyword.
- Remote-focused boards that are publicly readable: We Work Remotely
  (`weworkremotely.com`), RemoteOK (`remoteok.com`). Verify each hit on the company's own
  ATS page before recording it.
- General web search: `"<title>" <domain keyword> job <location or "remote">`, optionally
  restricted to the last month.

## Sources that need the user present

- **LinkedIn** and **Indeed** both require a logged-in browser session and actively wall
  automated access. Use them only in attended sessions where the user is logged in;
  in unattended runs, skip them and say so in the report.
- Never bypass a login wall, rate limit, or CAPTCHA to reach a source.

## Recording hygiene

- Capture the canonical posting URL (the ATS page you'd apply on), not a search-result
  or aggregator redirect.
- US salary-transparency states (CA, CO, NY, WA, and others) force posted ranges — when a
  range is listed, record it; when not, record "comp unlisted" rather than guessing.
- Postings older than ~60 days are often stale; note visible posted dates and prefer
  fresher listings when volume allows.
