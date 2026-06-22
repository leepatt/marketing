# Client Follow-Up Engine

> **New workstream — sales conversion, not content.** Separate from the content/social engine
> (`SETUP.md`, `CONTENT-PILLARS.md`). This is about converting leads and quotes we've *already
> earned* — plugging the revenue leaks where deals slip away.
>
> **Status: v1 draft (2026-06-22) — for Lee's review.** Nothing here sends until Lee approves the
> copy and the automation level (see *Open decisions*). All email copy below is DRAFT, in Craftons
> voice, awaiting sign-off.

---

## Why this exists — the leak

Most quotes that go quiet were *winnable*. The deal was half-closed; it just needed a chase that
never came. The trigger for this work was a Will Barron (Salesman.com) talk, and the principle is
blunt: **~44% of businesses follow up once and give up, or never follow up at all.** That gap is
the cheapest revenue in the building — you've already done the hard part (won the enquiry, built
the quote); you're just not finishing.

Barron's **Revenue Leak Calculator** is built for exactly our kind of business and names four
leak points. Mapped to Craftons:

| # | Leak | Craftons reality | Where we fix it |
|---|------|------------------|-----------------|
| 1 | **Lead generation** — system to find customers | The content engine feeds this | (content engine — separate) |
| 2 | **Meeting / response** — system to respond + book | Enquiries land in Gmail + form → ClickUp | **Flow B** (Gmail) |
| 3 | **Quote follow-up** — system to chase quotes | **The main gap.** ~15–30 quotes/wk, no chase | **Flow A** (Quotient → own platform) |
| 4 | **Past-customer reactivation** — when did you last reach out | Untapped — they already trust us | **Flow C** (Gmail + Shopify Email) |

You came in for #3. **#4 is the other half** — reactivating past clients is the easiest money in
the building because the trust is already there.

---

## Current state (confirmed 2026-06-22)

- **Leads land in:** Gmail (direct enquiries) + form submissions that drop into **ClickUp**.
- **Quoting:** **Quotient** is live and working — **but** a custom, Craftons-tailored quoting
  platform is on the roadmap to replace it.
- **Volume:** ~**15–30 quotes/week** (~60–120/month).

**Strategic consequence:** because Quotient is being replaced, we **do not** over-invest in deep
Quotient-specific plumbing. We design the follow-up *logic* (cadence + copy) as a **portable
asset**, switch on Quotient's built-in follow-ups as the cheap interim, and **bake the same
sequence into the new platform** when it's built.

---

## Architecture — ClickUp is the spine

```
Enquiry (Gmail) ─┐
Form submission ─┴─► ClickUp (the spine: pipeline + status + reminders)
                          │
          ┌───────────────┼─────────────────────────┐
          ▼               ▼                          ▼
   Flow B (Gmail)   Flow A (Quotient now,      Flow C (Gmail +
   enquiry chase    own platform later)        Shopify Email)
                    quote follow-up            reactivation
```

- **ClickUp = system of record.** It already receives form submissions and is connected here.
  A simple pipeline drives everything: `New enquiry → Quoted → Following up → Won / Lost`.
  ClickUp reminders/automations fire the cadence; status changes are the stop-condition.
- **Quotient** = switch on built-in automatic quote-follow-up emails now (config, not build).
  Interim only.
- **Gmail** = where enquiry + reactivation emails go out (connected; Zapier bridge available).
- **Own quoting platform (future)** = Flow A baked in natively; retire Quotient's version.

### Control model (carried over from the marketing engine)
Craftons' standing rule is **"Claude drafts → Lee approves; nothing auto-publishes."** Follow-ups
test that rule at 15–30/wk. Recommended reconciliation (see *Open decisions* to confirm):
- **Quote follow-ups (Flow A):** templated + low-risk + Quotient auto-stops on accept/decline →
  safe to **automate** once copy is approved.
- **Reactivation + enquiry replies (Flows B/C):** more personal → **Claude drafts, Lee one-click
  sends.**
- **Hard safety rule everywhere:** never send the next touch if the customer has already replied,
  accepted, or paid. Quotient handles this for quotes; the Gmail side must check the thread +
  ClickUp status before each send.

---

## Flow A — Quote follow-up *(the main gap)*

**Trigger:** a quote is sent (Quotient now). **Stop:** reply, accept, or decline.
Five touches over three weeks. Builder-to-builder, low-pressure, each one gives a reason to
re-engage. `[brackets]` = merge fields.

| Touch | When | Intent |
|-------|------|--------|
| 1 | Day 2 | Did it land? open the door |
| 2 | Day 5 | Reassurance — kill the common hesitation |
| 3 | Day 9 | Remove the blocker — make it easy to say what's wrong |
| 4 | Day 14 | Still going ahead? gentle validity deadline |
| 5 | Day 21 | Break-up — close the file, leave the door open |

**DRAFT copy** (Craftons voice — confident, not pushy; trade language; "we" = Craftons, "you" = the builder):

**Touch 1 — Day 2**
> **Subject:** Your Craftons quote — did it land?
>
> Hi [First name], just making sure the quote for [project] came through OK — they occasionally
> catch in spam. Happy to walk through any line item or adjust quantities if the scope's moved.
> Anything you need from us to move it forward?
>
> — [Sender], Craftons

**Touch 2 — Day 5**
> **Subject:** Quick one on the [project] quote
>
> Hi [First name], two things builders usually want nailed down before they commit on a job like
> this: lead time, and knowing the parts land ready to go. Everything's CNC-cut to your spec, so it
> goes straight in — no hand-fitting on site. Want me to jump on a quick call and run through it?
>
> — [Sender]

**Touch 3 — Day 9**
> **Subject:** Anything holding up the [project] job?
>
> Hi [First name], if the quote isn't quite right — price, quantities, timing — tell me what's off
> and I'll sort it. Easier to adjust now than have it sit. What's the hold-up?
>
> — [Sender]

**Touch 4 — Day 14**
> **Subject:** Still going ahead with [project]?
>
> Hi [First name], checking in before this one ages out — the pricing and lead times on the quote
> hold until [date]. If you're still on for it, reply and I'll lock it in.
>
> — [Sender]

**Touch 5 — Day 21**
> **Subject:** Closing this one off
>
> Hi [First name], I'll close the file on the [project] quote for now — no worries if the timing's
> not right. When it comes back around we're here, and the quote's easy to refresh. Good luck with
> the build.
>
> — [Sender]

---

## Flow B — New enquiry *(speed-to-lead + info chase)*

**Speed-to-lead is the single biggest lever** — the faster the first reply, the higher the close.

1. **Instant acknowledgement** (auto, on enquiry/form):
   > Hi [First name], got your enquiry — we'll have [a quote / next steps] back to you by
   > [timeframe]. If it's time-sensitive, call [number] and we'll get straight onto it. — Craftons
2. **Info chase** — when we're waiting on drawings/specs to quote: nudge **Day 2 / Day 5 / Day 10**
   to get what we need ("To get your quote accurate we just need [plans / dimensions / spec] —
   send those through and we'll turn it around fast.").

---

## Flow C — Past-customer reactivation *(the easy money)*

A recurring campaign, **not** a per-lead sequence. Quarterly 1:1-style outreach to past clients.
**Cross-links to the content engine:** this is also where the **#BuiltWithCraftons** mechanic and
the **Shopify Email** newsletter (B8) feed in — ask for finished-job photos and you get content +
reactivation in one touch.

**DRAFT copy:**
> **Subject:** What are you building at the moment?
>
> Hi [First name], been a while since [last job]. What's on the bench at the moment? We've [new:
> e.g. new shapes in the Formwork Builder / Radius Pro updates] — happy to quote anything curved
> you've got coming up. And if you've got photos of how [last job] turned out, we'd love to see it.
>
> — [Sender], Craftons

---

## Open decisions (need Lee)

1. **Automation level** — full auto vs. draft-and-approve vs. hybrid (recommended: hybrid — auto
   the quote chase, draft-and-approve the personal ones). *This gates how we build.*
2. **Sender / signatory** — who do these come from? Lee personally, or a `sales@` inbox?
3. **Cadence numbers** — confirm the Day 2/5/9/14/21 spacing for Flow A (and the validity window
   for Touch 4).
4. **Quotient now vs. wait for the new platform** — confirm we switch Quotient's follow-ups on as
   the interim rather than waiting.

## Phased rollout (once decisions land)

1. **Phase 1 — Quote chase live.** Approve Flow A copy → switch on Quotient's built-in follow-ups;
   stand up the ClickUp pipeline + statuses. *Biggest, fastest win.*
2. **Phase 2 — Enquiry flow.** Gmail speed-to-lead ack + info chase (canned responses / drafts).
3. **Phase 3 — Reactivation.** Quarterly campaign, cross-linked to #BuiltWithCraftons + Shopify Email.
4. **Phase 4 — Own platform.** Bake Flow A into the new quoting tool; retire Quotient's follow-ups.

---

_Sources: Will Barron / Salesman.com — [the video](https://www.youtube.com/watch?v=ltI6fVjNCSk),
[Revenue Leak Calculator](https://calculator.salesman.com/),
[Simple Selling Method](https://salesman.com/simple-selling-method/). Sequence reconstructed from
Barron's published material (the verbatim transcript wasn't retrievable)._
</content>
</invoke>
