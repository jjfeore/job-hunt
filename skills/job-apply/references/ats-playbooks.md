# ATS playbooks

Platform-specific handling for the job-apply skill. Identify the platform from the URL
pattern, then follow its playbook. Two rules repeat everywhere: **account walls always go
to the user**, and **know where the submit button is so you stop before it**.

## Greenhouse

**URL patterns:** `boards.greenhouse.io/<company>/jobs/<id>`, `job-boards.greenhouse.io/<company>/jobs/<id>`, or embedded in a company careers page (`<iframe>` from `boards.greenhouse.io`).

- Single-page form directly under the job description. No account needed.
- Standard block first: first/last name, email, phone, resume upload, sometimes cover
  letter. Resume upload buttons offer "Attach" (file) vs "Dropbox/Google Drive" — use
  the plain file attach.
- Uploading a resume may auto-parse into fields on some boards; verify parsed values.
- Company-specific custom questions follow the standard block — dropdowns, radio
  buttons, and free-text. Location/school fields are often autocomplete widgets: type,
  then click a suggestion; free text alone doesn't register.
- **EEO / demographic section** ("U.S. Equal Employment Opportunity", "Voluntary
  Self-Identification") sits at the bottom, above submit. Answer from the profile's
  self-ID policy.
- **Submit button:** a single `Submit application` button at the very bottom. Stop
  above it.
- Embedded (iframe) boards: fields live inside the iframe; interact within it.

## Lever

**URL patterns:** `jobs.lever.co/<company>/<uuid>` (posting) and `.../apply` (form).

- Single-page form at the `/apply` URL. No account needed.
- Resume upload sits at the TOP ("ATTACH RESUME/CV") and often auto-fills name/email/
  phone/org fields below — verify every autofilled value.
- Standard fields: name, email, phone, current company, plus links (LinkedIn, GitHub,
  portfolio, other). Custom questions and an "Additional information" free-text box
  follow.
- **EEO section** ("U.S. Equal Employment Opportunity information") appears near the
  bottom for US companies.
- **Submit button:** `Submit application` at the bottom of the single page. Stop
  above it.

## Ashby

**URL patterns:** `jobs.ashbyhq.com/<company>/<uuid>`.

- Single-page React app; the "Application" tab or an "Apply for this job" button
  reveals the form. No account needed.
- Fields render dynamically; give the page a moment before reading it. Autocomplete
  multi-selects (location, pronouns) require clicking an option from the dropdown —
  typed free text that isn't a listed option is silently dropped, so re-read the field
  value after setting it.
- Resume upload is a standard file input; some Ashby boards offer "Autofill from
  resume" — if used, verify every autofilled field.
- Yes/no screeners are usually segmented buttons or dropdowns.
- **Submit button:** `Submit application` at the form's bottom. Stop above it.

## Workday

**URL patterns:** `<company>.wd1.myworkdayjobs.com/...` (wd1/wd2/wd3/wd5 all exist).

- **Account wall first:** "Apply" leads to sign-in / account creation almost
  immediately. Creating accounts and entering passwords is the user's job — hand the
  browser over right away and resume once they're signed in.
- Multi-page flow with a progress bar, typically: Autofill with Resume (or Apply
  Manually) → My Information → My Experience → Application Questions → Voluntary
  Disclosures → Self Identify → Review.
- "Autofill with Resume" parses aggressively and badly. If used, expect to rebuild the
  Experience section: check job titles, dates (fields are picky — usually MM/YYYY via
  their own widget), and descriptions block by block.
- Dropdowns are custom widgets (search boxes with option lists), not native selects:
  click, type, click the matching option.
- Each page has `Save and Continue` — clicking it is fine; it advances, it doesn't
  submit.
- Voluntary Disclosures and Self Identify pages hold the EEO/veteran/disability
  questions; the disability form (CC-305) sometimes requires a name and date even when
  answering "prefer not to answer" — fill from profile policy, flag it in the handoff.
- **Submit button:** on the final Review page, labeled `Submit`. Stop on the Review
  page and hand over there — it conveniently shows everything entered.

## iCIMS

**URL patterns:** `careers-<company>.icims.com/jobs/<id>/...`.

- Frequently gated by a "returning candidate?" login or an email-verification step —
  hand walls to the user.
- The form usually lives inside an **iframe** (`#icims_content_iframe`); if the page
  looks empty, look for the iframe and work inside it.
- Flow: resume upload (or social import — use plain upload) → parsed profile review
  (fix mangled fields) → questionnaires → EEO on a separate step near the end.
- Multi-step "Next"/"Continue" buttons advance pages safely.
- **Submit button:** final step, labeled `Submit`, `Submit Profile`, or `Finish`. Stop
  before it and hand over.

## LinkedIn Easy Apply / Indeed

- Both require the user's logged-in session and both aggressively bot-check. Attended
  sessions only — never in unattended runs, never with stored credentials.
- Easy Apply is a modal wizard (Next → Next → Review → Submit): resume choice, contact
  info, screeners. Stop on the **Review** step; the submit button is labeled
  `Submit application`.
- Indeed applications ("Apply now") are similar wizards; stop at the review step
  (`Submit your application`).
- If either platform interrupts with verification (email codes, CAPTCHA, "are you a
  robot"), hand to the user immediately.

## Cross-platform habits

- After filling any page, re-read it and confirm no validation errors before moving on.
- Confirm file uploads by their displayed filename; a failed upload that goes unnoticed
  wastes the whole handoff.
- Salary fields that force a single number: use the profile's stated single-number
  policy; if the profile only has a range, enter per its policy or flag it.
- Multi-select "skills" pickers: choose only skills present in the bullet bank's
  inventory.
- Screenshot (or otherwise capture) the completed form state for the handoff summary.
