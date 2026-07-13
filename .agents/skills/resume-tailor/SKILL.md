---
name: resume-tailor
description: Builds a job-specific resume from the user's curated bullet bank — selects, reorders, and rewords existing bullets to mirror a job description, renders .docx and .pdf, and logs keyword coverage and gaps. Never fabricates experience. Use when the user says "tailor my resume for <URL or job description>", "prep a resume for this job", "make me a resume for the <company> role", or after the user picks jobs to pursue from a shortlist.
---

# job-hunt: resume-tailor

Produce a resume tailored to one job description, drawn entirely from the user's
bullet bank.

**HARD RULE — NEVER FABRICATE.** Select, reorder, reword, and emphasize existing
bullet-bank content only. Never invent employers, titles, dates, technologies,
credentials, or metrics. Never print a `[METRIC?]` placeholder on a resume: omit that
bullet, rephrase it without the quantitative claim, or ask the user for the real number.
If the job description asks for something the bank doesn't support, record it as a gap in
`notes.md` — do not paper over it. Rewording must preserve truth: mirroring the JD's
vocabulary is good, upgrading a claim to match the JD is fabrication.

## Workspace

All mutable data lives in the user's workspace, never inside the plugin directory
(installed plugins are read-only at runtime).

1. Resolve the workspace path: the `JOB_HUNT_HOME` environment variable if set, otherwise
   `~/job-hunt-data/` (`%USERPROFILE%\job-hunt-data` on Windows).
2. If the workspace directory is missing, create it: copy every file from the plugin's
   `templates/` directory into it, dropping `.template` from each filename
   (`search-criteria.template.md` → `search-criteria.md`, `tracker.template.csv` →
   `tracker.csv`). The plugin root is the directory containing this `skills/` folder.
3. Workspace contents: `search-criteria.md`, `profile.md`, `bullet-bank.md`,
   `resume-template.md`, `tracker.csv`, plus `shortlists/` and `applications/`
   directories created as needed. Never write inside the plugin directory at runtime.

If `bullet-bank.md` is missing or still the unfilled template, stop and tell the user to
run the `setup` skill first — there is nothing truthful to tailor from.

## Procedure

### 1. Obtain the job description

Fetch the posting URL, or use text the user pasted. Extract: company, title, location,
hard requirements, nice-to-haves, and the recurring language the JD uses for its
priorities. Classify the role as senior IC or engineering leadership.

### 2. Read the source material

Read `bullet-bank.md` and `resume-template.md` from the workspace, plus contact details
from `profile.md` for the resume header.

### 3. Select and shape content

- Pick the strongest 3–5 bullets per role that mirror the JD's language and priorities;
  use the bank's competency tags to find candidates fast. Older or less relevant roles
  get fewer bullets — or one line.
- Reword selected bullets to echo the JD's own terms where truthful.
- Choose the summary variant by role type — senior-ic or leadership — per the template's
  `[VARIANT: ...]` markers, and write it using the JD's vocabulary.
- Skills section: the JD-relevant subset of the bank's skills inventory, nothing else.

### 4. Write and render

- Write the tailored resume to
  `<workspace>/applications/<Company>_<Title>/<UserName>_Resume_<Company>.md`, replacing
  spaces with underscores and stripping characters that are unsafe in filenames.
- Render `.docx` and `.pdf` alongside the markdown using available document-generation
  tooling (e.g. a docx/pdf skill), else `pandoc` if installed, else deliver clean
  markdown and tell the user explicitly that they'll need to render it themselves.
- Respect the template's layout rules (single column, no tables or graphics) and page
  targets: one page for IC roles, up to two for leadership when the content earns it.

### 5. Write notes.md

In the same folder, write `notes.md` covering:

- Keyword coverage vs. the JD — covered / partial / missing, term by term
- Gaps: requirements the bullet bank genuinely doesn't support
- Likely screen questions for this role, each with a truthful angle from the bank

### 6. Update the tracker

Set the job's row in `tracker.csv` to `status=tailored` and fill `resume_path` with the
folder path. If the job wasn't already tracked (came directly from the user), add a row
first: `date_found` = today, `source` = direct, `fit_score` left empty or scored against
the criteria if they exist.

### 7. Report

Report the files written, a one-paragraph coverage summary, the gaps, and any bullets
that were held back for carrying `[METRIC?]` — with a nudge to supply real numbers via
the `setup` skill.
