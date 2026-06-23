# Client Follow-Up Engine — CNC Cut

> **Sales-conversion workstream, not content.** Separate from the Craftons content/social engine
> (`/CONTENT-PILLARS.md` etc.). This is about converting quotes and leads we've *already earned* —
> chasing quotes that go quiet so winnable jobs don't slip away.
>
> **Two docs:** *this* file = the **system** (how follow-ups are triggered and run).
> `followup-rules.md` = **how to write a good follow-up** (the agent reads it before drafting).
>
> **Status:** v2 design (2026-06-23). Proof-of-concept validated; not yet wired into a Routine.

---

## Why this exists — the leak

Most quotes that go quiet were *winnable* — the job was half-closed and just needed a chase that
never came. The trigger for this work was a Will Barron (Salesman.com) video; the principle is
blunt: **~44% of businesses follow up once or never**, and that gap is the cheapest revenue going.
We currently issue **~15–30 quotes/week** with no systematic follow-up. That's the leak we're
plugging.

## Current state (confirmed 2026-06-23)

- **Leads land in:** Gmail (direct enquiries) + form submissions that drop into **ClickUp**.
- **Quoting:** **Quotient** is live, **but** a custom CNC Cut quoting platform is on the roadmap to
  replace it. So we don't over-invest in Quotient-specific plumbing — the follow-up *logic* is a
  portable asset.
- **Volume:** ~15–30 quotes/week (~60–120/month).
- **Sender & brand:** `cnc@cnccut.melbourne`, signing off as **CNC Cut** *(decided 2026-06-23)*.
  - *Caveat to keep in mind:* some customers have history under the **Craftons** brand (the PoC job
    came in to `hello@craftons.com.au` as "Craftons Order #1155"). Referencing "the quote we sent"
    sidesteps any confusion; we don't lead with brand.

## Why Gmail-centred (the key decision)

The goal is **personalise every follow-up as much as possible.** That settles the tool choice:

- **Quotient can't personalise** — its follow-ups are templated merge-fields, capped at 2, and the
  API won't allow per-client bespoke copy.
- **The context lives in email** — the whole conversation (enquiry, quote, back-and-forth) is in
  the Gmail thread. ClickUp only holds the job at the start; Quotient only the quote + enquiry.
- **An agent can read the thread** and draft a genuinely tailored follow-up.

So follow-ups are **written and sent from Gmail**, drafted by an agent that reads the real context.
Quotient still *creates* the quote (and its own auto-follow-ups are turned **off**, so the customer
never gets a robotic Quotient nudge plus our personal one).

## Architecture

```
Quotient: quote sent ──► ClickUp: status → "Waiting Approval"  (state machine, already wired)
                                    │
                       daily Routine sweep: in "Waiting Approval"
                       ≥ 4 business days, no draft yet, no reply
                                    │
                                    ▼
            Agent reads: Gmail thread  +  ClickUp comments [Ravi excluded]
                                    │   (apply followup-rules.md; never leak internal)
                                    ▼
                 Gmail: personalised draft, on-thread ──► human reviews & sends
                                    │
                         mark ClickUp task "drafted" (idempotency)
```

- **ClickUp = trigger / state machine.** It already knows quote status (Quotient tells it). Not the
  content store — just the state + timer.
- **Gmail = context + draft + send.** The thread is the richest context; the draft lands here; a
  human always sends.
- **No separate database.** State (drafted? / stop?) lives on the ClickUp task.

## How it runs — a Claude Cowork Routine

This runs entirely in **Claude Cowork (Claude Code on the web)** as a scheduled **Routine** — no
custom code and no raw API keys needed for v1:

- **Scheduled, unattended** daily run on Anthropic's cloud; the Gmail + ClickUp connectors carry
  over (authenticated once on the account) and execute without per-call prompts.
- **The build is a prompt, not code** — a self-contained instruction set the daily run executes,
  pointed at `followup-rules.md`.
- **Trigger is a poll, not a push:** the daily sweep finds jobs that are *Waiting Approval ≥ 4
  business days, not yet drafted, no customer reply*, and drafts each one.

**Later hardening (optional):** re-implement in **cnccut.app** if/when we want it baked into the
dashboard or the new quoting platform — same logic, more control. Code + secrets live there, never
in this repo (per `/CLAUDE.md`).

## Context & safety

Full rules in **`followup-rules.md`**. The load-bearing ones:

- **Context = Gmail thread + ClickUp job comments.**
- **Exclude Ravi-tagged comments** — they're CAM handoff notes; drop before drafting.
- **Internal notes inform, never leak** — use them to understand the job; never reveal margins,
  "chase deposit," supplier issues, etc. to the customer.
- **Never fabricate** — no comments? Work from the thread alone.
- **Draft only — a human always sends.** Nothing auto-sends.
- **Stop conditions:** customer replied, quote accepted/declined, or status changed → no further
  follow-up. Mark the task once drafted so it's never drafted twice.

## Proof of concept — done ✅

Validated manually on **"Build by the Sea"** (2026-06-23): read the enquiry thread, applied the
date logic (quote ~11 May, install window lapsed), and produced a short, direct, reason-led draft
with no banned filler. Confirmed the no-comments case degrades gracefully. See the worked example
in `followup-rules.md §7`.

## Decisions (resolved 2026-06-23)

1. **Brand/inbox** — ✅ CNC Cut, from `cnc@cnccut.melbourne` (see *Current state*).
2. **Sequence timings** — provisional defaults ~4 days / ~2 weeks / ~4 weeks (`followup-rules.md §4`).
   *Based on Barron's published method, not the verbatim video — tune from real results.*
3. **Signature** — ✅ left blank for now; the human fills it before sending.
4. **ClickUp state marker** — ✅ two **custom fields** on each job task (not a separate task):
   - `Follow-up` (dropdown): `None` · `1st follow-up` · `2nd follow-up` · `Closed off` · `Do not follow up`
   - `Last follow-up` (date)
   The agent reads/updates these for idempotency + timing. *Lee to create the fields in ClickUp.*

## Phased rollout

1. **Phase 1 — Routine live (here).** Finalise the Routine prompt (points at `followup-rules.md`),
   stand up the daily sweep, turn Quotient's auto-follow-ups off. *Biggest, fastest win.*
2. **Phase 2 — Tune.** Watch real drafts, refine the rules + timings.
3. **Phase 3 — Harden into cnccut.app** if/when we want dashboard integration or it's folded into
   the new quoting platform.

## Additional routines (planned)

Each is its own scheduled Cowork Routine, sharing the voice in `followup-rules.md`. Draft-only,
human sends.

- **Weekly digest** *(confirmed)* — Mondays, emails Lee a summary: outstanding quotes, follow-ups
  drafted, jobs gone quiet. Drives adoption + visibility.
- **Won-job review & photo request** *(confirmed)* — when a job is marked Won, drafts a **per-job
  tailored** message asking for a Google review + finished-job photos. Photos feed the Craftons
  `#BuiltWithCraftons` content engine — two birds. *Needs: the Google review link + the exact
  "Won/done" status name.*
- **Past-customer reactivation** *(backlog)* — periodic (≈quarterly) personalised "what are you
  building?" to past clients gone quiet ~3–6 months (Barron's leak #4 — the cheapest revenue).
  1:1 and personal, distinct from a broadcast newsletter. *Needs: the cleanest past-customer source
  (ClickUp / Quotient / Xero / Shopify) + the "gone quiet" window.*
- **Speed-to-lead** — *already handled in ClickUp; no Routine needed.*

---

_Source: Will Barron / Salesman.com — [the video](https://www.youtube.com/watch?v=ltI6fVjNCSk),
[Revenue Leak Calculator](https://calculator.salesman.com/),
[Simple Selling Method](https://salesman.com/simple-selling-method/). Method reconstructed from
Barron's published material (verbatim transcript wasn't retrievable)._
</content>
