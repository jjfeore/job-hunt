# Bullet Bank

This file is the single source of truth for resume content. The `resume-tailor` skill
selects, reorders, rewords, and emphasizes bullets from here — and does nothing else.

**The no-fabrication rule:** every fact in this file must be true. The tailor skill never
invents employers, titles, dates, technologies, credentials, or metrics — which means
anything not written here can never appear on a resume. If an accomplishment is missing,
add it here first.

## Format

Each role is one block, newest first:

    ## <Company> — <Title>
    **Dates:** <start> – <end>  |  **Location:** <city or Remote>
    **Context:** one or two lines on the team, product, and scale.

    - [tag, tag] Bullet text with a real number.
    - [tag] Bullet text with a pending number [METRIC?].

Guidelines:

- Write bullets resume-ready: strong verb, what you did, the outcome.
- Write MORE bullets than fit any one resume — 6–12 per significant role. Tailoring
  works by selection; a thin bank produces thin resumes.
- Tag every bullet with one or more competency tags (see taxonomy below).

## The `[METRIC?]` convention

When you know something is quantifiable but don't remember the number, write `[METRIC?]`
where the number belongs — "Cut p95 latency by [METRIC?] by rewriting the cache layer."
The tailor skill never puts a `[METRIC?]` bullet on a resume as-is: it omits the bullet,
rephrases it without the quantitative claim, or asks you for the real number. Never
invent a number to make a bullet look finished.

## Competency taxonomy

Tag bullets with these fixed tags:

`applied-ai` · `llm-agents` · `ml-infra` · `backend` · `systems-architecture` ·
`leadership` · `hiring` · `delivery` · `cross-functional` · `mentorship`

You may extend the taxonomy: add kebab-case tags to the **Custom tags** list below with a
one-line definition each, then use them like any other tag. Don't rename or repurpose the
fixed tags — the skills refer to them by name.

**Custom tags:**

- (none yet)

---

# Roles

<!-- Replace the fictional example below with your real roles, newest first. -->

## Meridian Analytics — Senior Software Engineer (FICTIONAL EXAMPLE — delete)
**Dates:** 2019-03 – 2023-06  |  **Location:** Denver, CO (hybrid)
**Context:** 8-person platform team; real-time analytics product processing ~2B events/day.

- [backend, systems-architecture] Redesigned the ingestion pipeline from batch to streaming (Kafka + Flink), cutting data freshness from 4 hours to under 90 seconds.
- [backend, delivery] Led the migration of 40+ services to Kubernetes with zero customer-facing downtime.
- [leadership, mentorship] Mentored four engineers to senior promotions; ran the team's design-review process.
- [cross-functional, delivery] Partnered with product and sales engineering to ship usage-based billing, unlocking [METRIC?] in new ARR.
- [hiring] Built the team's take-home exercise and interview rubric; interviewed ~60 candidates over two years.

# Education

<!-- Degree, institution, year — one per line. Certifications too: name, issuer, year. -->

-

# Skills inventory

<!-- Flat list of languages, frameworks, and tools you're genuinely comfortable defending
     in an interview. The tailor skill picks the JD-relevant subset from this list only. -->

-
