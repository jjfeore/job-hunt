# job-hunt

A job-application pipeline for AI agents: scheduled search, human-reviewed shortlists,
no-fabrication resume tailoring, and browser-driven applications that always stop before
submit.

`job-hunt` is an agent plugin — a set of portable skills that work in Claude Code,
Claude Cowork, OpenAI Codex, and any other runtime that reads `SKILL.md` files. The
engine lives in this repo; **your personal data never does**. Everything about you —
criteria, work history, applications — lives in a private workspace on your machine.

## How it works

Four stages — three driven by skills, one owned by you:

1. **`job-search`** — reads your saved criteria, scans login-free sources (Greenhouse,
   Lever, and Ashby job boards, company careers pages, web search), dedupes against your
   tracker, and writes a dated shortlist scored 1–5 against *your* criteria. Runs
   great on a schedule.
2. **You review the shortlist** and pick which jobs to pursue. The agent never decides
   this for you.
3. **`resume-tailor`** — builds a per-job resume by selecting and rewording bullets from
   your curated bullet bank. It logs keyword coverage and honest gaps, and renders
   `.docx`/`.pdf` when tooling allows.
4. **`job-apply`** — drives a browser to fill the application from your profile, uploads
   the tailored resume, answers standard screeners — then **stops at the completed form**
   and hands you a field-by-field summary. You review; you click submit.

The fourth skill, **`setup`**, is the guided interview that builds your configuration in
the first place.

## The safety model

- **The agent never clicks submit.** Every application ends with a human review and a
  human click — even if you tell it to "submit my application".
- **The agent never touches credentials.** No account creation, no passwords, no
  CAPTCHAs; login walls are handed back to you.
- **The agent never fabricates.** Resumes are assembled only from bullets you wrote and
  approved. Unknown numbers stay unknown (`[METRIC?]`) rather than becoming lies.
- **You pick the jobs.** The search produces a shortlist; nothing advances without you.

## Quickstart

### Claude Code

Try it for a single session (loads straight from the clone):

```
git clone https://github.com/jjfeore/job-hunt
claude --plugin-dir ./job-hunt
```

For a persistent install, clone into your personal skills directory instead — any
folder under `~/.claude/skills/` containing `.claude-plugin/plugin.json` loads
automatically as `job-hunt@skills-dir` from the next session on, no install step:

```bash
# macOS / Linux
git clone https://github.com/jjfeore/job-hunt "$HOME/.claude/skills/job-hunt"
```

```powershell
# Windows (PowerShell)
git clone https://github.com/jjfeore/job-hunt
```

Then say: *"set up job-hunt"*.

### Claude Cowork

Cowork installs plugins as `.plugin` files (which are plain zip archives of this repo).
Package one from the repo root — `git archive` works identically on Windows, macOS, and
Linux and automatically excludes `.git/` and untracked files (commit changes first):

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force dist | Out-Null
git archive --format=zip -o dist/job-hunt.plugin HEAD
```

```bash
# macOS / Linux
mkdir -p dist
git archive --format=zip -o dist/job-hunt.plugin HEAD
```

Upload `dist/job-hunt.plugin` in Cowork's plugin settings, then say *"set up job-hunt"*.

For a recurring search, create a scheduled task with a prompt like:

> Run the job-hunt job-search skill and tell me where the new shortlist is and how many
> new postings it found.

### OpenAI Codex

Codex discovers repo skills under `.agents/skills`, and this repo ships a committed
mirror of its skills there — so cloning is enough:

```
git clone https://github.com/YOUR_GITHUB/job-hunt   # TODO(James): replace with the real published URL
cd job-hunt
codex
```

Codex also reads the repo-root `AGENTS.md` as project guidance automatically. To make
the skills available in *every* directory (not just this repo), copy the contents of
`skills/` into `~/.agents/skills/` **and** the `templates/` folder to
`~/.agents/templates/` — the skills bootstrap your workspace from a `templates/`
directory near their skills folder, so it must come along.

> **Contributors:** the canonical skills live in `skills/`; `.agents/skills` is a
> generated mirror. After editing any skill, run
> `python3 scripts/sync_codex_skills.py` (Windows: `py scripts/sync_codex_skills.py`).

## Configuration

All of your data lives in one workspace directory **outside this repo**:

- Default location: `~/job-hunt-data/` (`%USERPROFILE%\job-hunt-data` on Windows)
- Override: set the `JOB_HUNT_HOME` environment variable to any path you like.

Any skill will create the workspace from the templates on first run, but the fastest
path is running the `setup` skill and letting it interview you. What each file controls:

| File | Controls |
|---|---|
| `search-criteria.md` | What `job-search` looks for: titles, seniority, domains, location, comp floor, exclusions |
| `profile.md` | What `job-apply` types into forms: contact info + standard screener answers |
| `bullet-bank.md` | The only source `resume-tailor` may draw from: your tagged, truthful accomplishment bullets |
| `resume-template.md` | The ATS-safe layout tailored resumes are rendered into |
| `tracker.csv` | Every job's status: `new → shortlisted → tailored → applied → …` |
| `shortlists/` | Dated search results, one file per day |
| `applications/` | One folder per application: tailored resume, renders, notes |

## Set up with your AI agent

You have an AI agent — let it do the data entry. Paste any of these prompts.

**1. Full guided setup**

```
Use the job-hunt plugin's setup skill. Interview me one topic at a time — don't move on
until we've finished each topic — to fill in my search criteria, my applicant profile,
and my standard application answers. Start by telling me what my workspace already
contains. Then work through: (1) my work history into the bullet bank, (2) my search
criteria, (3) my profile and standard answers. Never invent facts about me; where I
don't know a number, write [METRIC?] instead of guessing. Finish with a completeness
report listing everything still TODO.
```

**2. Build my bullet bank** (attach a resume, or save a LinkedIn "Save to PDF" export
as `linkedin-export.pdf` in your workspace first)

```
I've provided my resume / LinkedIn export. Using the job-hunt plugin's bullet-bank
format, draft my bullet bank from it. Go role by role: show me 6–12 draft bullets per
role, each tagged with the plugin's competency taxonomy, and interview me about each
role — what I owned, what changed because of me, and the numbers behind each claim. Ask
me for every missing metric; if I can't remember one, write [METRIC?] instead of a
guess. Never invent employers, titles, dates, technologies, or accomplishments. When
we're done, save the result to bullet-bank.md in my job-hunt workspace and list every
bullet still carrying [METRIC?].
```

**3. Define my search criteria**

```
Help me define my job search criteria for the job-hunt plugin. Ask me probing questions
one topic at a time: target titles (including variants I might be forgetting),
seniority floor and ceiling, domains and keywords, location and remote policy, my
compensation floor, preferred company stage and size, and my exclusions/dealbreakers.
Challenge vague answers — if I say "senior roles", ask which titles I'd actually accept
and which I'd skip. When we've covered everything, write the result to
search-criteria.md in my job-hunt workspace and read it back to me for confirmation.
```

## Privacy

Your name, contact details, work history, and application record live **only** in your
workspace directory — never in this repo, and never in anything you'd push by
installing, forking, or contributing to it. The templates here contain placeholders and
a fictional example persona; the `.gitignore` guards against a workspace accidentally
landing in the repo. Before publishing a fork, it's still smart to search your tree for
your own name and phone number.

## Responsible use

This tool optimizes for *quality* applications, not volume — a tailored resume and a
human-reviewed form for jobs you actually want. Please keep it that way: review every
application before submitting, don't spray low-effort applications, respect job boards'
terms of service and rate limits, and remember that everything sent under your name is
yours. The plugin's guardrails (no auto-submit, no fabrication, no credential handling)
exist to keep the human accountable for anything a human should be accountable for.

## License

MIT — see [LICENSE](LICENSE).
