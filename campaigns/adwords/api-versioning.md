# Google Ads API — versioning & upgrade policy

_Source: [Upgrade your API version](https://developers.google.com/google-ads/api/docs/upgrade) ·
[Deprecation and sunset](https://developers.google.com/google-ads/api/docs/sunset-dates).
Checked 2026-08-03._

## Current state (2026-08-03)

**The tool already exists — in `cnccut-app`, not here.** `cnccut-app/tools/google-ads.mjs` is built,
live, and calling the API. It powers the Marketing Cockpit's Google Ads module. **The plan docs in
this folder (`api-access.md`, `api-tool-design.md`) describe it as not-yet-built — they are stale.**

**Bumped v22 → v25 on 2026-08-03** (branch `claude/google-ads-api-migration-ofqe83`). Verified: no
field this tool queries was removed or renamed in v23/v24/v25, so it was a one-line change.

### ⚠️ UNRESOLVED: something else is calling v21

Google emailed on ~2026-08-03: the developer token on MCC **275-347-3695** had *recently submitted
requests to v21*, which sunset **2026-08-05**. **That caller has not been found.** What's been ruled
out, conclusively:

| Suspect | Verdict |
|---|---|
| `cnccut-app/tools/google-ads.mjs` | **Not it.** Written 2026-07-08 with `v22`, never changed until the v25 bump. `v21` appears nowhere in 286 commits across all branches. |
| A `GOOGLE_ADS_API_VERSION` env override | **Not it.** The variable is not set in Vercel (confirmed by Lee). |
| `cnccut-website` | **Not it.** No Google Ads code at all. |
| `marketing` (this repo) | **Not it.** No Google Ads code at all. |

So the v21 caller is **outside all three repos**, authenticating with the same developer token.
Leading hypothesis (unverified): a one-off verification call made during the 2026-06-15 setup or the
2026-06-23 credential rotation — a hand-rolled `curl` or throwaway script would plausibly have used
v21, which was current from Aug 2025. If so it's already dead and there is nothing to fix.

**To resolve it:** Cloud Console → APIs & Services → Google Ads API → **METRICS** → **Methods**. That
is the only place that sees every request made with the token, with versions and timestamps. Recurring
v21 traffic = something live that broke on 2026-08-05. A single old spike = the one-off theory, closed.

**Who holds the developer token?** This is the question that actually resolves it, and it's answered
nowhere. The token is one string tied to the MCC, and *anything* holding it calls the API in our
name — Google attributes the request to us regardless of what made it. Known holder: cnccut-app's
Vercel env. Unknown: local `.env` files, one-off scripts, anything it was pasted into during the
2026-06-15 setup. Worth an inventory.

**The correction worth remembering:** the production tool was on **v22** (sunset Oct 2026) and was
never at risk from the Aug 5 deadline. The sunset email named a version nothing in the codebase used
— it was a warning about the *token*, not about the deployed code. Don't assume an API sunset email
refers to your main integration; check which version your code actually pins before acting.

## The versioning contract

- ~5 major versions live at once. Majors last **~12 months**, minors ~10.
- **At most 2 upgrades per year.** This is the real maintenance number.
- Upgrades **do not have to be sequential** — v23 → v25 directly is fine.
- **Deprecated** = not the newest; everything still works, but no new features.
  **Sunset** = requests fail. Different things — don't panic at "deprecated".
- Google guarantees ≥20 weeks between a new client-library release and the old version's sunset.
  **This guarantee covers Google's own libraries only — not community ones.**

## Timetable

| Version | Released | Sunset |
|---|---|---|
| v21 | 2025-08-06 | **Aug 2026 (tentative)** |
| v22 | 2025-10-15 | Oct 2026 (tentative) |
| v23 | 2026-01-28 | Feb 2027 |
| v23.1 | 2026-02-25 | Feb 2027 |
| v23.2 | 2026-03-25 | Feb 2027 |
| v24 | 2026-04-22 | May 2027 |
| v24.1 | 2026-05-13 | May 2027 |
| v24.2 | 2026-06-24 | Jun 2027 |
| **v25** ← latest | **2026-07-22** | **Aug 2027** |

Upcoming: v25.1 (Aug 2026) · v25.2 (Sep 2026) · v26 (Oct 2026) · v26.1 (Nov 2026, optional).

## How to check what you're calling

Cloud Console → **APIs & Services** → **Google Ads API** → **METRICS** tab → **Methods** table.
The version is inside every method name, e.g. `google.ads.googleads.v25.services.GoogleAdsService.Mutate`.
Empty table = nothing is calling the API.

## The Node problem

Google ships **official** client libraries for Java, C#, PHP, Python, Ruby, Perl — **not Node.js**.

The community package `google-ads-api` (Opteo) is at **24.1.0, published 2026-06-15** → tracks
**v24.1, not v25**. Single maintainer, structurally ~1 version behind Google, and outside the
20-week overlap guarantee.

### Decision: call REST directly, no client library — **already implemented**

`cnccut-app/tools/google-ads.mjs` already does exactly this (same reasoning, reached independently:
dependency-light fetch matching the Xero/Gmail OAuth convention, and gRPC bundles poorly for
serverless). Recorded here so it doesn't get re-litigated. The endpoint:

```
POST https://googleads.googleapis.com/v25/customers/{customerId}/googleAds:searchStream
Headers: Authorization: Bearer <access_token>
         developer-token: <GOOGLE_ADS_DEVELOPER_TOKEN>
         login-customer-id: 2753473695
Body:    { "query": "<GAQL>" }
```

Why this wins here:
- **The version is one constant.** Upgrading = bump the string, skim the proto diff, test.
- No dependency between us and Google — never blocked on a maintainer.
- Keeps the Node convention already set by `meta-ads.mjs`.
- Our surface is small: GAQL reports + a handful of mutates. We don't need the codegen.

Define it once, in one place:

```js
const API_VERSION = 'v25';  // sunset Aug 2027 — see table above
```

If we ever outgrow raw REST, the official **Python** library is the fallback (always day-one
current: 31.2.0 supports v25), at the cost of breaking the Node convention.

## The recurring upgrade routine (~2×/year)

When a new major lands, or ~3 months before our version's sunset:

1. **Update the endpoint** — bump `API_VERSION`. On major bumps the endpoint changes; that's the
   whole "update your client libraries" step when calling REST.
2. **Read the [release notes](https://developers.google.com/google-ads/api/docs/release-notes)** for
   every version being skipped, not just the target.
3. **Check the version-specific focus areas** called out for the target version.
4. **Check the proto diff table** (e.g. "Proto differences between v24 and v25") for renamed,
   removed, and changed fields — this is where GAQL queries silently break.
5. Run the report tool read-only against the live account and diff the output before trusting it.

Also worth tracking separately: [feature deprecations and unversioned changes](https://developers.google.com/google-ads/api/docs/sunset-dates)
— some behaviour shifts (e.g. conversion environment, gclid/gbraid handling) land *without* a
version bump, so a pinned version does not make us immune.

Subscribe to the [Google Ads Developer Blog](https://ads-developers.googleblog.com/) for sunset
reminders — that's the only push notification for this.
