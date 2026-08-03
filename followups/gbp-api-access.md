# Google Business Profile API — Basic access application

> **Assumption:** "the direct API" = the **Google Business Profile API** (the one with an application
> and an approval queue), not the Gmail API. Gmail has no application process, and replies to Google
> reviews never travel through Gmail. If you actually meant Gmail API send access, say so — that's a
> different (and much shorter) job, sketched at the bottom.
>
> Companion to `google-reviews.md` (the research). This is the **application package**: what to
> click, what to paste, in what order. Same shape as `campaigns/adwords/api-access.md`.
>
> **Prepared 2026-08-03. Not yet submitted.**

---

## Eligibility — we pass (checked, not assumed)

| Requirement | Status |
|---|---|
| GBP verified and **active 60+ days** | ✅ Craftons profile has been live since **at least July 2025** — review from Joel 16 Jul 2025, monthly performance reports every month since Aug 2025 |
| **Website** listed on the profile | ✅ `craftons.com.au` |
| Applying account is an **owner** on the profile | ⚠️ **Confirm** — `cnc@cnccut.melbourne` receives all notifications, but notifications go to managers too. Must be **Owner**, not Manager |
| Google Cloud project exists | ✅ Reuse the existing project from the Google Ads work (B7) |
| Legitimate use case | ✅ Managing our own four profiles, not reselling |

**The one real risk is the owner check.** The most common rejection is applying from a
manager-level account. Verify at [business.google.com](https://business.google.com) → Craftons →
**Users** → confirm `cnc@cnccut.melbourne` shows as **Owner** (or **Primary owner**) before
submitting.

---

## Step 1 (Lee) — get the Cloud project number

1. [console.cloud.google.com](https://console.cloud.google.com) → select the **existing project**
   used for Google Ads (B7).
2. From the dashboard, copy the **Project number** (the long digit string, not the project ID).
3. Send it to me — it goes on the form, and it must be **the same project** where the APIs get
   enabled later. Access is granted **per project**, so mixing projects means re-applying.

## Step 2 (Lee) — submit the form

Go to **[support.google.com/business/contact/api_default](https://support.google.com/business/contact/api_default)**
and select **"Application for Basic API Access"** from the dropdown.

> Pick that exact option. The other dropdown entries route to general product support, not the API
> team, and the request dies there.

Sign in as the **owner** account (`cnc@cnccut.melbourne`) before opening the form.

### Drafted answers — paste these

**Business name:** Craftons
**Website:** https://craftons.com.au
**Contact email:** cnc@cnccut.melbourne
**Google Cloud project number:** `[from Step 1]`
**Number of locations managed:** 4 — Craftons, CNC Cut Melbourne, CNC Cut Geelong, Cavity Battens
(all our own; we are not managing profiles for third parties)

**What is your use case / what are you building?**

> We manufacture customised building products in Melbourne and Geelong and manage four of our own
> verified Business Profiles. We want an internal tool that reads new reviews and posts our replies,
> so that every customer review gets a timely, personal response instead of being missed in the
> notification inbox.
>
> Specifically we need `accounts.locations.reviews.list` and
> `accounts.locations.reviews.updateReply` on the Google My Business API (v4), plus
> `accounts.list` / `locations.list` from the Account Management and Business Information APIs to
> resolve our own location IDs. Replies are drafted internally and approved by a staff member before
> posting.
>
> This is an internal tool for our own business only. We are not building a product for other
> businesses and will not access profiles we do not own. Expected volume is low: roughly 2 to 5
> reviews per month across all four locations, so a handful of API calls per day.

**Volume / QPS expectations:** minimal — a daily poll plus a few writes; well inside the default
300 requests/minute.

### Why this wording

Google approves **modest, specific, internal** applications and rejects generic ones. So it names
the actual endpoints, states the real location count, keeps the volume honest, and explicitly rules
out multi-tenant use. Do not upgrade it into an "AI-powered reputation platform" pitch — that
framing is what gets applications rejected.

## Step 3 — wait

- Auto-confirmation email arrives within about an hour, usually with a case number.
- Google states **7 to 10 business days**; real-world reports range from **4 days to 6 weeks**, and
  Google's own help text says up to 2 weeks. Assume a fortnight and start now.
- They may email a follow-up question. Answer it fast — that thread is the whole review.

**How to check approval without waiting for the email:** Cloud Console → **APIs & Services → Quotas**
for the Business Profile APIs. **0 QPM = not approved yet. 300 QPM = approved.** Before approval,
calls return HTTP 429 — that's a denial dressed up as a rate limit, not a bug in our code.

## Step 4 (after approval) — enable + authorise

Enable all eight in the Cloud project (they interlock; enabling only one causes confusing 403s):

1. Google My Business API ← **the one that carries reviews**
2. My Business Account Management API
3. My Business Business Information API
4. My Business Notifications API
5. My Business Q&A API
6. My Business Place Actions API
7. My Business Verifications API
8. My Business Lodging API

Then OAuth, exactly as we did for Google Ads (B7):

- **Credentials → Create credentials → OAuth client ID → Web application**
- Redirect URI: `https://developers.google.com/oauthplayground`
- Mint a refresh token via the OAuth Playground using our own credentials, offline + force-consent
- **Scope:** `https://www.googleapis.com/auth/business.manage`

**Env vars** (into the same places as the Google Ads creds — never into git, never into the Drive
brain):

```
GBP_CLIENT_ID
GBP_CLIENT_SECRET
GBP_REFRESH_TOKEN
GBP_ACCOUNT_ID        # from accounts.list, once authorised
```

## Step 5 (Claude, after access) — build the tool

`tools/gbp-reviews.mjs`, mirroring the `google-ads.mjs` / `meta-ads.mjs` guardrail pattern:

- **Read mode (default, safe):** list new reviews across all four locations, resolve which brand
  each belongs to, output them with drafted replies for approval.
- **Write mode (behind a `CONFIRM=1` gate):** post a reply via `reviews.updateReply`.

**Guardrail — non-negotiable:** a review reply is **public and instant**; there is no draft state in
the API. Claude drafts, a human approves, then it posts. Never auto-reply to anything below 4 stars.

## Status

- [ ] Confirm `cnc@cnccut.melbourne` is **Owner** (not Manager) on the Craftons profile — *Lee*
- [ ] Get the Cloud project number — *Lee*
- [ ] Submit the form with the drafted answers — *Lee*
- [ ] Log the case number + submission date here — *Lee → Claude*
- [ ] Check quota flips 0 → 300 QPM
- [ ] Enable the 8 APIs + create OAuth client + mint refresh token
- [ ] Place `GBP_*` env vars
- [ ] Build `tools/gbp-reviews.mjs`
- [ ] Wire the review-reply routine (drafts for approval)

---

## If you did mean the Gmail API

Different thing, much shorter, no application. Today's Gmail connector is **read + draft + label
only — it cannot send**, which is why every follow-up ends with Lee pressing send. Direct Gmail API
access would let the engine send.

To do it: same Cloud project → enable the **Gmail API** → OAuth client → scope
`https://www.googleapis.com/auth/gmail.send` (or `gmail.modify` for drafts + send) → refresh token
via the Playground. **No allowlist, no approval queue** — internal use within our own Workspace
domain doesn't need Google's app verification, though the consent screen will warn about an
unverified app unless we mark it Internal.

**Worth pausing on before we do it:** `CLAUDE.md`, `followups/README.md` and `followup-rules.md` all
rest on *"drafts only — a human always sends."* Send access removes the one hard brake in that
system. Recommend keeping it draft-only unless there's a specific job that needs autonomous sending,
and if so, gating it the same way as ads changes.

---

**Sources:** [Prerequisites](https://developers.google.com/my-business/content/prereqs) ·
[Basic setup](https://developers.google.com/my-business/content/basic-setup) ·
[Applying for API access](https://support.google.com/business/workflow/16726127) ·
[updateReply](https://developers.google.com/my-business/reference/rest/v4/accounts.locations.reviews/updateReply) ·
[Usage limits](https://developers.google.com/my-business/content/limits)
