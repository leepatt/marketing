# Replying to Google reviews — what's possible and how to wire it

> **Researched 2026-08-03.** The other half of the review loop: `README.md` Routine 1 Part B *asks*
> for reviews; this doc covers *replying* to the ones that come in.
>
> **Short answer:** yes, replies can be posted programmatically — but **not through Gmail**. Gmail
> only carries the notification. The reply is written to the **Google Business Profile** (GBP), via
> the Google Business Profile API or the Zapier bridge. Neither is wired up yet.

---

## The Gmail misconception (worth being explicit about)

`businessprofile-noreply@google.com` emails us when a review lands. That email is a **notification,
not a thread** — there is nothing to reply *to*. Replying to it goes to a no-reply address and the
customer never sees it. The reply has to be written against the review object on the Business
Profile itself.

Also worth knowing: this session's **Gmail connector is read + draft + label only — it has no send
tool**. So even for real email, the engine drafts and a human sends. That matches the control model
in `CLAUDE.md` and is not a limitation we want to remove.

## Current state (confirmed from the mailbox, 2026-08-03)

- **Craftons has its own Business Profile**, and its review notifications land in
  `cnc@cnccut.melbourne` — e.g. *"Jordan left a review for Craftons"* (2 Aug 2026), *"Jack left a
  review for Craftons"* (22 Jul 2026), plus a monthly performance report (*61 profile views in
  June*).
- **The same Google account manages at least four profiles:** Craftons · CNC Cut Melbourne ·
  CNC Cut Geelong · Cavity Battens. CNC Cut Melbourne notifications also copy
  `cnccutmelbourne@gmail.com`.
- That matters: **one API integration covers all four locations**, and any access request should be
  framed as "we manage our own multi-location business", which is the use case Google approves.
- Nothing is wired: no GBP connector in this session, no `business.manage` credentials in the env,
  no Zapier GBP action enabled.

---

## Path A — Zapier bridge (fast, no approval wait) ✅ recommended first

The Zapier MCP is **already connected to this session** and Zapier ships a Google Business Profile
app with exactly the two pieces we need:

- **Trigger:** *New Review*
- **Action:** *Reply to Review* — creates the reply, or updates it if one already exists

Zapier holds its own approved Google API access, so **we skip the Google Cloud approval queue
entirely**. In this session `discover_zapier_actions` shows the app with 1 read + 3 write actions
available to enable.

**To stand it up:**
1. Enable the Google Business Profile action in Zapier (`enable_zapier_action`,
   `selected_api: GoogleMyBusinessCLIAPI`) — *needs Lee's go-ahead; it changes the shared Zapier
   config.*
2. Authorise Zapier against the Google account that owns the profiles (`cnc@cnccut.melbourne`).
3. Confirm all four locations are visible, then reply to one real review end-to-end as a test.

**Cost:** covered by the existing Zapier plan. **Lead time:** same day.
**Trade-off:** less control than raw API — no bulk history pull, no custom quota, dependent on
Zapier's field mapping.

## Path B — Google Business Profile API direct (full control, approval-gated)

The real thing. Reviews were **never migrated** to the newer v1 Business Profile APIs, so this is
still the legacy v4 surface — that's expected, not a sign it's dead.

```
PUT https://mybusiness.googleapis.com/v4/accounts/{accountId}/locations/{locationId}/reviews/{reviewId}/reply
Body: { "comment": "…the reply text…" }
Scope: https://www.googleapis.com/auth/business.manage
```

- `reviews.list` / `reviews.get` / `locations.batchGetReviews` — read reviews across locations
- `reviews.updateReply` — upsert: posts a reply, or **replaces** the existing one (one reply per
  review, attributed publicly to the business)
- `reviews.deleteReply` — remove a reply
- **Only works on verified locations.**

**The gate (the part with lead time):** take a Google Cloud project's **project number** and submit
the **Basic API access application** at
[support.google.com/business/contact/api_default](https://support.google.com/business/contact/api_default)
— access is granted per project, and the project's quota sits at **0 QPM until approved** (every
call 429s), flipping to 300 QPM on approval. Only then is enabling the eight APIs useful. Google
states 7–10 business days; assume up to a fortnight. Thin or grandiose applications get rejected,
and the application must come from an **Owner** of the profile, not a Manager. A verified profile
active 60+ days and a real business website are required; both are true for us.

**→ The full application package, with drafted answers, is in `gbp-api-access.md`.**

**Real-time notifications (optional, Path B only):** the Notifications API v1
(`accounts.updateNotificationSetting`) pushes `NEW_REVIEW` events to a Cloud Pub/Sub topic, so a
routine can react the moment a review lands instead of polling. Requires granting
`mybusiness-api-pubsub@system.gserviceaccount.com` publish rights on the topic. Not needed for v1 of
this — a daily sweep is plenty at our volume.

---

## Control model — the important caveat

**A review reply is public and instant.** There is no draft state in the API, unlike Gmail. Posting
*is* publishing, to the single most-read surface a local business has.

So the default stays what `CLAUDE.md` sets out — **Claude drafts, Lee approves and posts**:

1. Routine sweeps for new reviews (via Zapier's trigger, or `reviews.list`).
2. Claude drafts a tailored reply — reading the job context the same way follow-ups do.
3. Draft goes somewhere Lee can approve (Gmail draft to self, or a ClickUp task).
4. **Lee posts it** — or approves and lets the routine post it, once the drafting has earned trust.

Auto-replying to negative reviews should stay off permanently. A 1-star review is a phone call, not
an API call.

## Drafting rules (proposed — for review)

Review replies are public brand surface, so they inherit the discipline in `followup-rules.md`:
**no em/en dashes, one idea, no filler, no AI tells.** Plus:

- Name the actual job ("the curved bench seat frames") — specificity is what reads human.
- Thank once, briefly. Never gush, never repeat the customer's name twice.
- No keyword stuffing. Google doesn't reward it and customers can smell it.
- Two to three sentences. Longer reads defensive.
- Negative reviews: acknowledge, take it offline with a real contact, never argue publicly, never
  reveal job details.
- Which brand voice applies depends on the profile — Craftons replies use the Craftons voice
  (`SOCIAL-VOICE.md` / the `craftons-voice` skill); CNC Cut replies sign as CNC Cut.

---

## Recommended sequence

1. **Lee decides:** Zapier bridge first (fast) or wait for direct API access.
2. If Zapier: give the go-ahead to enable the GBP action + authorise
   `cnc@cnccut.melbourne`. Test on one live review.
3. In parallel, **start the direct API access request anyway** — it costs nothing but time to
   apply, and the approval clock runs while the Zapier path does the work. Same lesson as the Google
   Ads dev token: apply early.
4. Lock the drafting rules above, then wire a routine that drafts replies for approval.

## What's needed from Lee

- [ ] Confirm which Google account owns the Craftons profile (assumed `cnc@cnccut.melbourne` — the
      notifications land there, but ownership vs management access should be confirmed).
- [ ] Go-ahead to enable the Zapier Google Business Profile action + authorise it.
- [ ] Decision: draft-for-approval only (default), or auto-post for 4–5 star reviews once trusted?
- [ ] Whether replies should cover all four profiles or Craftons only to start.

---

**Sources:**
[updateReply reference](https://developers.google.com/my-business/reference/rest/v4/accounts.locations.reviews/updateReply) ·
[Work with review data](https://developers.google.com/my-business/content/review-data) ·
[Usage limits](https://developers.google.com/my-business/content/limits) ·
[Real-time notifications](https://developers.google.com/my-business/content/notification-setup) ·
[Zapier: Reply to Review](https://zapier.com/apps/google-business-profile/integrations) ·
[Zapier: auto-reply to reviews](https://zapier.com/blog/reply-to-google-my-business-reviews/)
