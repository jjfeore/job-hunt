---
name: setup
description: Initializes and configures the job-hunt workspace — creates config files from templates, ingests the user's work history into a curated bullet bank, and runs a guided interview to fill in search criteria, applicant profile, and standard application answers. Use when the user says "set up job-hunt", "configure my job search", "help me get started with this plugin", when they want to update their criteria, profile, or bullet bank, or whenever any job-hunt skill detects a fresh or incomplete workspace.
---

# job-hunt: setup

Configure the user's private job-hunt workspace through a guided interview. Work one
topic at a time — never dump a wall of questions.

**The no-fabrication rule governs everything here:** record only facts the user provides
or confirms. Never pad a bullet, guess a metric, or upgrade a title. Where a real number
is unknown, write `[METRIC?]` in its place — the resume-tailor skill knows what that
means and will never print it on a resume.

## Workspace

All mutable data lives in the user's workspace, never inside the plugin directory
(installed plugins are read-only at runtime).

1. Resolve the workspace path: the `JOB_HUNT_HOME` environment variable if set, otherwise
   `~/job-hunt-data/` (`%USERPROFILE%\job-hunt-data` on Windows).
2. If the workspace directory is missing, create it: copy every file from this skill's
   bundled `templates/` directory (it sits inside this skill's folder, next to this
   SKILL.md) into it, dropping `.template` from each filename
   (`search-criteria.template.md` → `search-criteria.md`, `tracker.template.csv` →
   `tracker.csv`).
3. Workspace contents: `search-criteria.md`, `profile.md`, `bullet-bank.md`,
   `resume-template.md`, `tracker.csv`, plus `shortlists/` and `applications/`
   directories created as needed. Never write inside the plugin directory at runtime.

## Procedure

### 0. Take stock

Read every workspace config file. Classify each as unfilled template, partially filled,
or complete, and tell the user what you found. If everything is already complete, ask
which part they want to revise and jump straight there.

### 1. Work history → bullet bank

Goal: a `bullet-bank.md` with 6–12 tagged bullets per significant role, following the
format documented at the top of that file. Offer the user these ingestion paths:

- **LinkedIn via browser** — if a browser tool is available in this session, offer to
  open the user's LinkedIn profile and read roles (company, title, dates, location,
  description), education, skills, and certifications directly. The user may need to be
  logged in; never handle their credentials — let them log in themselves.
- **Document drop** — the user saves a resume or a LinkedIn "Save to PDF" export at
  `<workspace>/linkedin-export.pdf`; read it from there. Any readable resume file works.
- **Interview** — no documents: walk role by role asking for company, title, dates,
  location, what the team did, what the user owned, and what changed because of them.

Then, role by role:

1. Draft bullets from the source material in the bank's format, tagging each from the
   competency taxonomy.
2. Show the user each drafted role block. Ask them to confirm wording, correct anything,
   and supply missing numbers. Mark every plausible-but-unknown quantity `[METRIC?]` —
   never drop the bullet, and never invent the number.
3. Capture education, certifications, and the skills inventory the same way.

### 2. Search criteria

Interview one topic at a time, writing confirmed answers into `search-criteria.md`:

1. Target titles — including variants and borderline titles
2. Seniority — floor and ceiling
3. Domains and keywords
4. Location and remote policy
5. Compensation floor
6. Company stage and size preferences
7. Exclusions and dealbreakers

Push for specificity: vague criteria produce noisy shortlists. Read the finished file
back to the user for confirmation.

### 3. Profile and standard answers

Fill `profile.md`: contact fields first, then the standard application answers one at a
time — work authorization, visa sponsorship, relocation, salary expectation, earliest
start date / notice period, "how did you hear about us", voluntary self-identification
policy, references. Where the user is unsure, leave a clearly marked TODO; the job-apply
skill flags TODOs during applications instead of guessing.

### 4. Completeness report

End with a short report: what is filled in and what remains TODO (file by file), how many
roles and bullets the bank holds, and how many bullets still carry `[METRIC?]`. Suggest
the natural next step — usually running the `job-search` skill.
