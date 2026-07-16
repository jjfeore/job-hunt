---
name: job-search
description: Runs the user's job search — reads their saved search criteria, scans login-free sources (Greenhouse/Lever/Ashby job boards, company careers pages, web search) for matching postings, dedupes against the application tracker, scores fit 1–5, and writes a dated shortlist. Use when the user says "run my job search", "find new job postings", "check for new roles", "any new jobs today", or when a scheduled or unattended task invokes the job search.
---

# job-hunt: job-search

Find new postings that match the user's saved criteria and produce a scored, dated
shortlist. Quality over volume: five genuine matches beat twenty maybes.

## Workspace

All mutable data lives in the user's workspace, never inside the plugin directory
(installed plugins are read-only at runtime).

1. Resolve the workspace path: the `JOB_HUNT_HOME` environment variable if set, otherwise
   `~/job-hunt-data/` (`%USERPROFILE%\job-hunt-data` on Windows).
2. If the workspace directory is missing, create it: copy every file from the templates
   bundled with the `setup` skill — the `setup/templates/` directory that sits alongside
   this skill's folder — into it, dropping `.template` from each filename
   (`search-criteria.template.md` → `search-criteria.md`, `tracker.template.csv` →
   `tracker.csv`). If `setup/templates/` isn't installed next to this skill, tell the
   user to install the `setup` skill: it carries the templates.
3. Workspace contents: `search-criteria.md`, `profile.md`, `bullet-bank.md`,
   `resume-template.md`, `tracker.csv`, plus `shortlists/` and `applications/`
   directories created as needed. Never write inside the plugin directory at runtime.

If `search-criteria.md` is missing or still an unfilled template, stop and tell the user
to run the `setup` skill first — searching without criteria produces noise.

## Procedure

### 1. Read the criteria

Read `search-criteria.md` in full: titles, seniority, domains, location, compensation
floor, company stage, exclusions, preferred sources. Treat exclusions as hard filters.

### 2. Search

Load `references/search-sources.md` from this skill's directory for source URL patterns
and query recipes, then search. Prefer sources that need no login:

- Direct ATS job boards: Greenhouse, Lever, Ashby company boards.
- Careers pages of companies matching the stage/size preferences, plus any preferred
  sources listed in the criteria.
- General web search combining target titles, domain keywords, and location terms.

LinkedIn and Indeed require a logged-in browser session with the user present; skip them
in unattended runs and note the skip in the final report.

Run several query variations — different title phrasings, different domain keywords.
Favor postings from roughly the last 30 days when age is visible.

### 3. Dedupe against the tracker

Read `tracker.csv`. Drop any posting whose URL already appears. Then drop postings that
match an existing row on normalized company + title (lowercase, punctuation and
whitespace collapsed). A previously seen job is never "new", whatever its status.

### 4. Evaluate each new posting

For each posting that survives dedupe, capture:

- Company, title, location / remote status
- Salary if listed (mark "comp unlisted" when absent)
- URL (the canonical posting URL, not a search-results redirect)
- Posted date if visible
- A 2–3 line fit rationale referencing the criteria
- A fit score 1–5 tied explicitly to the criteria file:
  - **5** — title, domain, location, and compensation all match; no flags
  - **4** — strong match with one soft gap (e.g. comp unlisted, borderline title)
  - **3** — genuine match on domain and seniority but two or more soft gaps
  - **2** — plausible stretch; record it in `tracker.csv` but leave it off the shortlist
  - **1** — barely relevant; discard (no tracker row, no shortlist entry)
- Anything matching an exclusion or dealbreaker: discard it entirely, whatever the score.

### 5. Record

- Append one row per new posting to `tracker.csv` with `status=new`, `date_found` =
  today (YYYY-MM-DD), and `source` = where it was found. Follow the existing header
  exactly; quote any field containing commas; leave unknown fields empty.
- Write the shortlist to `<workspace>/shortlists/YYYY-MM-DD.md` (today's date), sorted by
  fit score descending, with each entry's rationale underneath it. If the file already
  exists from an earlier run today, merge into it rather than overwriting.

### 6. Report

Report the count of new postings found, the shortlist path, and anything skipped
(e.g. LinkedIn/Indeed in an unattended run). If there were zero genuine matches, say
exactly that — never pad the shortlist with weak matches to look productive.
