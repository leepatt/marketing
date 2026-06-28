# CNC Cut — Client Follow-Up Rules

> **What this is.** The rulebook for writing client follow-ups at CNC Cut — used both by the
> follow-up drafting agent in Claude Cowork (it reads these rules before drafting) and by any
> human writing one by hand. The **system/plumbing** (how follow-ups are triggered and run) lives
> in `followups/README.md`; **this** file is purely *how to write a good one*.
>
> **Source.** A Will Barron / Salesman.com video triggered this work, but its transcript wasn't
> retrievable — so these rules are reconstructed from Barron's **published** method ("Selling Made
> Simple", the Revenue Leak Calculator) plus the specific rules Lee relayed from the video, then
> adapted to CNC Cut. His published material and the video say the same things. Treat it as living —
> tune it as we see what actually converts.
>
> **Status:** draft for review (2026-06-23). Not yet wired into a Routine.

---

## Voice — how CNC Cut sounds

Write like one tradie talking to another — Australian, relaxed, direct, human. We make CNC-cut
components for builders; the reader knows their trade, so respect their time.

- **Australian English and tone.** Plain and friendly, no corporate gloss. Aussie spelling
  (organise, colour, metre).
- **Builder-to-builder.** Concrete and practical. Short sentences. Get to the point.
- **Warm but not gushy; confident, not salesy.** A real person wrote this, not a marketing team.
- **Light vernacular is fine** — "no dramas", "give you a buzz", "keen", "sort it out", "flick it
  through" — but don't lay it on thick. **Mirror the customer's energy:** if they're formal, ease
  off; if they open with "Legend", match it.
- **First person, real.** "I'll", "we'll". Sign off `Cheers,` then the sender's name (blank for
  now), then `CNC Cut`.
- **Banned corporate-speak:** "reach out", "touch base", "circle back", "as per", "kindly", "at
  your earliest convenience" (on top of the banned filler in §2).

## 1. Mindset

- **Most quotes are lost by never following up — not to a competitor.** The follow-up *is* the
  edge. ~44% of businesses follow up once or not at all; simply doing it well wins back deals that
  were already half-closed.
- **Every follow-up must earn its place with a real reason.** If the only reason is "have you
  decided yet," don't send it — find the genuine reason (a lapsed timeline, a question, something
  useful) or wait until there is one.
- **Persistence, not pestering.** Follow up properly *and* know when to stop.

## 2. Banned language — never write these

- "Just following up", "just checking in", "touching base", "circling back", "any update?",
  "bumping this up" — empty filler. **Open with the real reason instead.**
- Needy / apologetic openers: "sorry to bother you", "I know you're busy", "I hate to chase".
  They signal the deal isn't worth pursuing. Be confident and matter-of-fact.
- Manufactured urgency ("prices go up Friday") and reflexive discounting to win a reply. Both
  erode trust. Refreshing pricing because time has *genuinely* passed is fine and honest.
- Broken/placeholder details. Never send "Hi [First name]" or a guessed figure. If a specific is
  missing, write around it cleanly.

## 3. How to write it

- **Direct and short.** Three lines beats three paragraphs. Get in, make the point, get out.
- **One email, one idea, one ask.** Two requests halve the reply rate. Land the single most
  important question; everything else waits for the reply.
- **One clear question** the customer can answer in five seconds (e.g. "Still going ahead?").
- **Give an easy "no."** Permission to close it off releases the pressure and is one of the
  highest-reply moves there is.
- **Lead with their outcome, not our process** — getting their job built/installed, not "our quote
  is expiring."
- **Confident, warm, human** — and **mirror the customer's tone**. If they write casual ("Legend"),
  don't reply corporate. Builder-to-builder.
- **Reason about dates.** Weigh time since the quote *and* the customer's own stated timelines, and
  match the message to where things actually stand (a fresh nudge, a stale re-quote, or a
  window-has-passed reconnect are different emails).

## 4. The sequence

Follow-ups are a short sequence with a **definite end**, and **each touch uses a new angle** —
never re-send the same nudge.

| Touch | Timing (from quote sent) | Angle |
|-------|--------------------------|-------|
| 1 | ~4 business days | The reason-led nudge (e.g. timeline, did it land, one question) |
| 2 | ~2 weeks | The **callback offer** — "reply with a window that suits + a number and I'll call you" (no fixed slot). One ask. |
| 3 | ~4 weeks | The close-off / "break-up" — give permission to say no, then stop |

*(Timings are starting defaults — tune them.)* **All timings are in business days — Monday to
Friday only; never count weekends.** (e.g. the first touch is 4 business days after the quote.)

- **Touch 2 is the callback offer.** Don't propose a fixed time slot — CNC Cut's day is
  unpredictable (walk-ins, moving schedule). Ask the customer for a rough window + a number and call
  them within it. Lower friction for them, and it fits how the day actually runs.
- **The close-off is a deliberate step, not a failure** — it's often the highest-replying email in
  the sequence. Always the ender.
- **Then stop.** After the close-off with no reply, mark it lost. Don't keep going.

## 5. Personalisation & context

- **Use real specifics** — the job description, quote number, value, a detail from the thread.
  Generic follow-ups get ignored; "the seat and planter box setout (Quote #1162, $4,850)" lands.
- **Context comes from two places:** the Gmail thread, and the ClickUp job comments.
- **Internal notes inform, they never leak.** ClickUp comments are internal — use them to
  *understand* the job, but never quote or reveal internal detail (margins, "chase the deposit",
  supplier issues, "client is difficult", CAM complexity) to the customer.
- **Exclude Ravi-tagged comments entirely.** Comments tagging/assigning Ravi are CAM handoff notes
  — drop them before drafting; never use them.
- **Don't fabricate context.** If a job has no comments, work from the email thread alone. Never
  invent detail to fill a gap.

## 6. Operational rules

- **Draft only — a human always sends.** Nothing auto-sends. Drafts sit in Gmail for review.
- **Never write to the repo.** Create Gmail drafts only and report your summary as text in the run.
  Do **not** commit files, create branches, or store customer details (names, emails, quotes) in the
  repo.
- **Delivery — fresh email vs reply.** Quotes go out via **Quotient**, so there's usually **no Gmail
  thread** to reply to. If an existing thread with the customer exists (e.g. their original enquiry),
  reply on it. If not, send a **fresh email** to the customer's address with a clear subject like
  `[Job] – Quote #[number]`. **No thread is NOT a reason to skip.** Get the customer's email from the
  enquiry thread, the Quotient notification, or the ClickUp task.
- **Sender:** `cnc@cnccut.melbourne`, signing off as **CNC Cut**. Don't lead with brand — referencing
  "the quote we sent" avoids confusion for customers with **Craftons** history.
- **Trigger:** quote sent (Quotient) → ClickUp status moves to **AWAITING APPROVAL** → first
  follow-up due ~4 business days later. Runs as a daily Claude Cowork **Routine** that sweeps for
  due jobs (polls; it doesn't get pushed).
- **Pipeline logic:** chase **only** while in **AWAITING APPROVAL**. When the customer accepts,
  Quotient auto-moves the job to **DEPOSIT INVOICE** → chasing stops and **nothing is sent through
  the production stages** (Deposit Invoice → Delivery). At **COMPLETE** (parts in the customer's
  hands), send one **review + photo request**, **2–15 business days** after completion (best Tue–Thu,
  late morning).
- **Match the right thread.** Jobs are named `Client - Job` (e.g. *Concretum - Heartford Entry
  Walls*); a client may have several on the go. Use client + job detail to find the correct Gmail
  thread. Only **skip + flag** if you find *multiple* threads and can't tell which is right — never
  guess. If there's simply **no thread**, that's fine — send a fresh email (see Delivery above).
- **Send during business hours / business days.** Skip weekends; respect the business-day count.
- **Idempotency & stop conditions:** track state in two ClickUp custom fields on the job —
  `Follow-Up Email` (dropdown: `None` / `1st follow-up` / `2nd follow-up` / `Closed off` / `Do not follow up`
  / `Request Email`) and `Last follow-up` (date). Advance `Follow-Up Email` and set `Last follow-up` whenever a draft is
  created, so a job is never drafted twice and the next touch can be timed. **Stop the sequence** the
  moment the customer replies, the quote is accepted/declined, the job changes status, or
  `Follow-Up Email` is set to `Do not follow up`.

## 7. Worked example — "Concretum – Heartford Entry Walls" (illustrative)

A client with several jobs on the go — so we match the thread on client **and** job detail. Quote's
been quiet ~2 weeks → **touch 2 (the callback offer)** is due.

**✗ Wrong** — filler opener, no real reason, two asks:
> Hi [name], just checking in on the Heartford entry walls quote. Also, did you want to send through
> the updated plans? Let me know if you'd like to proceed.

**✓ Right** — reason-led, one ask, dead easy to action:
> Hi [name],
>
> Chasing up the Heartford entry walls quote — easiest might be a quick call to run through it.
>
> Reply with a rough window that suits and a number, and I'll give you a buzz then.
>
> Cheers,
> [Sender]
> CNC Cut
</content>
