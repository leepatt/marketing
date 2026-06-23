# Cowork Routine prompts — CNC Cut follow-ups

> Paste-ready prompts for Claude Cowork **Routines**. Each runs as a scheduled, unattended cloud
> session with the **Gmail** + **ClickUp** connectors and **this repo** attached. They **draft
> only — a human always sends.**
>
> Fill the `«placeholders»` before pasting. The writing style and rules live in
> `followups/followup-rules.md` (read by the agent at the start of every run).

---

## Routine 1 — Daily quote follow-up drafter

**Schedule:** every weekday, early morning (e.g. 7:00). **Connectors:** Gmail, ClickUp.
**Repo:** this one (`marketing`).

```
You draft personalised quote follow-up emails for CNC Cut. You DRAFT ONLY — a human reviews and
sends every email. Never send anything. Never email a customer directly.

STEP 0 — Read the rules first.
Open `followups/followup-rules.md` in the connected repo and follow it exactly — especially the
CNC Cut VOICE section, the BANNED language, the one-idea/one-question discipline, the date
reasoning, and the rules on internal notes (never leak) and Ravi-tagged comments (never use).

STEP 1 — Find quotes awaiting a reply.
In ClickUp, in the list «JOBS LIST NAME», find every job whose status is "Waiting Approval"
(the state set when a quote has been sent). For each, read the two custom fields:
- `Follow-up` (dropdown: None / 1st follow-up / 2nd follow-up / Closed off / Do not follow up)
- `Last follow-up` (date)

STEP 2 — Decide if a follow-up is due (business days only; skip weekends).
- `Follow-up` = None  AND  ≥ 4 business days since the quote was sent  → draft TOUCH 1.
- `Follow-up` = 1st follow-up  AND  ≥ 10 business days since `Last follow-up`  → draft TOUCH 2.
- `Follow-up` = 2nd follow-up  AND  ≥ 10 business days since `Last follow-up`  → draft TOUCH 3.
- `Follow-up` = Closed off OR Do not follow up  → SKIP.
- Not yet due → SKIP.
(The quote-sent date = when the job entered "Waiting Approval", or the date of the quote email in
the thread, whichever you can determine.)

STEP 3 — Stop conditions (check before drafting).
Skip the job and do NOT draft if any are true — just note it in your summary for the human:
- The customer has already replied (the latest message in the Gmail thread is from them, not us).
- The quote has been accepted or declined, or the job's status is no longer "Waiting Approval".
These mean a human should take it from here.

STEP 4 — Gather context for a due job.
- Find the Gmail thread with the customer using the customer's email address from the ClickUp task.
  Read the whole thread (original enquiry, the quote, any replies).
- Read the ClickUp job comments. EXCLUDE any comment that tags or is assigned to Ravi (CAM handoff
  notes). Use internal comments only to UNDERSTAND the job — never quote or reveal internal detail
  (margins, deposits, supplier issues, difficulty, CAM notes) to the customer.
- Pull the quote reference/value/description if available, to make the email concrete.
- If a job has no comments or thin context, work from the thread alone. NEVER invent detail.

STEP 5 — Write the draft (per followup-rules.md, in CNC Cut's voice).
Short, direct, one question, lead with a real reason, no banned phrases. Reason about the dates and
the customer's own stated timelines. Use the angle for the touch:
- TOUCH 1 — reason-led nudge (e.g. timeline status, did it land), one clear question.
- TOUCH 2 — the callback offer: invite a quick call WITHOUT a fixed slot — ask them to reply with
  a rough window that suits and a number, and we'll call them then. One ask.
- TOUCH 3 — the close-off / break-up: give them permission to say no, then we stop.
Reply ON the existing email thread. From: cnc@cnccut.melbourne. Sign off "Cheers," / (blank name
line) / "CNC Cut".

STEP 6 — Create the draft and update ClickUp.
- Create the email as a Gmail DRAFT in that thread. Do not send.
- Update the job's custom fields: set `Follow-up` to the new stage (1st / 2nd / Closed off) and set
  `Last follow-up` to today.

STEP 7 — Summarise.
End with a short report for the human: jobs you drafted (customer + touch), and jobs you skipped
with the reason (replied / accepted / not due). Keep it tight.

HARD RULES: draft only, never send · never use banned phrases · never leak internal notes · never
use Ravi-tagged comments · never fabricate · business days only · one job is never drafted twice
for the same touch.
```

---

## Routine 2 — Weekly follow-up digest

**Schedule:** Mondays, early (e.g. 7:30). **Connectors:** ClickUp (Gmail to send the digest to Lee).
**Repo:** this one.

```
You produce a short weekly follow-up digest for CNC Cut and leave it as a Gmail DRAFT to
cnc@cnccut.melbourne (do not send). Purpose: give Lee one glance at where quote follow-ups stand.

In ClickUp, list «JOBS LIST NAME», look at all jobs with status "Waiting Approval" and their
`Follow-up` / `Last follow-up` fields, and report:
- Quotes still open (Waiting Approval) and how long each has been waiting.
- Where each is in the sequence (None / 1st / 2nd / Closed off).
- Jobs that have gone quiet and are due to be closed off.
- Anything where the customer replied but the job is still sitting in Waiting Approval (needs a
  human).

Keep it short and scannable — a list, not prose. No customer emails are sent; this is an internal
summary only.
```

---

## To build later (need inputs first)

- **Routine 3 — Won-job review & photo request.** Trigger on jobs newly marked «WON/DONE STATUS».
  Drafts a per-job tailored ask for a Google review («REVIEW LINK») + finished-job photos.
- **Routine 4 — Past-customer reactivation.** Periodic check-in to past clients gone quiet
  («SOURCE» + «WINDOW»). Backlog.
