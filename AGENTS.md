# job-hunt — agent guidance

This repo is the `job-hunt` plugin: a job-application pipeline (search → human
shortlist review → tailor → apply) delivered as four portable skills — `setup`,
`job-search`, `resume-tailor`, and `job-apply`. The
plugin directory is generic and read-only at runtime; every user's personal data lives
in an external workspace. This file is loaded as project context by agent runtimes
(Codex reads it natively); the rules below bind even when no skill is loaded.

## The skills

| Skill | Use when |
|---|---|
| `skills/setup` | First run, or the user wants to (re)configure criteria, profile, or bullet bank |
| `skills/job-search` | "Run my job search" / scheduled runs — produces a scored, dated shortlist |
| `skills/resume-tailor` | The user picked a job — builds a per-job resume from their bullet bank |
| `skills/job-apply` | The user wants an application filled — browser-driven, stops before submit |

Each skill's `SKILL.md` is the authoritative procedure; skill-local `references/` files
hold platform playbooks and search recipes.

## Workspace convention

- Workspace path: the `JOB_HUNT_HOME` environment variable if set, otherwise
  `~/job-hunt-data/` (`%USERPROFILE%\job-hunt-data` on Windows).
- If the workspace is missing, create it by copying the `setup` skill's bundled
  templates (`skills/setup/templates/*`) into it, dropping `.template` from filenames;
  then direct the user to the `setup` skill.
- Workspace contents: `search-criteria.md`, `profile.md`, `bullet-bank.md`,
  `resume-template.md`, `tracker.csv`, plus `shortlists/` and `applications/` created
  as needed.
- Never write inside this repo/plugin directory at runtime, and never copy user data
  into it. This repo must stay publishable at any moment.

## Hard safety rules — always in force

1. **Never click a final submit button on a job application.** Fill the form, summarize
   it field by field, and wait for the user to review and submit.
2. **Never create accounts, enter or store passwords, or attempt CAPTCHAs.** Hand the
   browser to the user at any such wall and resume once they clear it.
3. **Never fabricate resume or application content.** Only material from the user's
   bullet bank and profile may appear; unknown quantities are marked `[METRIC?]`, never
   invented. Gaps between a job's requirements and the user's real history are reported,
   not papered over.
4. Update `tracker.csv` to `applied` only after the user confirms they submitted.

## Notes for Codex

- Skills are auto-discovered from the committed mirror at `.agents/skills/`. The
  canonical source is `skills/` — edit there, then regenerate the mirror with
  `python3 scripts/sync_codex_skills.py` (Windows: `py scripts/sync_codex_skills.py`).
  CI-style check: add `--check`.
- For user-level (all-repos) availability, copy `skills/*` into `~/.agents/skills/`
  (or `npx skills@latest add jjfeore/job-hunt -g`) — the workspace templates ship
  inside the `setup` skill, so they travel with any skill-level install.

## For contributors

- Portability rules: SKILL.md frontmatter is `name` + `description` only; skill bodies
  never reference runtime-specific variables (no `${CLAUDE_PLUGIN_ROOT}`) or
  product-locked tool names — say "your browser tool", with products only as
  parenthetical examples. Paths are expressed relative to the plugin root ("the
  directory containing this `skills/` folder").
- Templates stay generic: placeholders and fictional personas only. No real personal
  data anywhere in this repo — run a PII search before releasing.
- `tracker.csv` schema is load-bearing across skills:
  `date_found,company,title,url,location,source,fit_score,status,resume_path,date_applied,notes`
  with `status` ∈ `new | shortlisted | tailored | applied | rejected | interviewing | offer | closed`.
