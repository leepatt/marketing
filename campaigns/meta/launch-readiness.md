# Launch readiness — what's left before test ads

_Written 2026-08-03, verified against the live account rather than from notes._

---

## 🔴 First: two things the repo believes that are wrong

### 1. The account is NOT paused. It is spending right now.

`STATUS.md` and the agent bible both say *"currently paused (0 live ad sets)."* Not true:

| Campaign | Status | Last 3 days | IC | Purchases |
|---|---|---:|---:|---:|
| **Retargeting — Bottom Of Funnel** | **ACTIVE** ($15/day) | **$124.83** | 3 | **1** |
| RadiusPro \| TOF \| Ardreagh \| Jul26 | now paused | $132.69 | 0 | 0 |

Retargeting spent **$15.28 yesterday and $1.10 today**. One live ad set: `Retargeting Campaign -
Bottom Of Funnel – Purchase`, `120233074187690186`.

**Why this matters for the test:**

- **We do not start from zero.** A live retargeting ad set will convert people the new TOF ads warm
  up, and last-click will credit retargeting — the exact attribution trap identified in the July
  post-mortem. **Read the test blended at account level, not per-campaign.**
- **Retargeting is working.** 1 purchase on $124.83 over 3 days is inside the $322 break-even. Don't
  switch it off to "clean up" the test — that would cost real money to buy a tidier read.
- **The TOF Ardreagh campaign repeated July exactly**: $132.69 over 3 days, zero IC, zero purchases,
  before it was paused. Same signature. It was optimising on the old setup.

### 2. `META_PAGE_ID` was never actually missing — it just wasn't discoverable the usual way

`me/accounts` returns `{"data":[]}` for this SYSTEM_USER token, which is why it read as absent.
It resolves via the business:

```
GET /1006792137511423/owned_pages  →  611852278682648  "Craftons"
```

**`META_PAGE_ID=611852278682648`** — needs adding to the session env and Vercel. `create-creative`
cannot publish without it, so this was a genuine hard blocker and is now unblocked.

⚠️ **No Instagram account is linked to the ad account** (`instagram_accounts` is empty). Ads will run
Facebook-only placements unless that's connected. Worth checking whether an IG account should be
attached before launch.

---

## ✅ Verified ready

| Item | Evidence |
|---|---|
| Ad account active, no restrictions | `account_status: 1`, `disable_reason: 0` |
| Currency + timezone correct | AUD, `Australia/Melbourne` |
| No spend cap blocking | `spend_cap: 0` |
| Pixel healthy | `Craftons Web`, `is_unavailable: false` |
| **Advanced Matching ON, 11 fields** | `em, fn, ln, ge, ph, ct, st, zp, db, country, external_id` |
| First-party cookie | `first_party_cookie_enabled` |
| **Custom conversion live** | `27686282527680441` — Sales Intent, IC OR Purchase |
| Purchase carries AUD value | Confirmed in earlier pass |
| Copy written from product truth | 24 creatives, `radius-pro-ad-copy.md` |
| Guardrails in code | $2k/mo ceiling · one ad set · always PAUSED · rung 0 |

---

## 🔴 Hard blockers — cannot run a test without these

### B1. The creative is still the wrong product
**The single biggest item.** Copy is v2; the images are v0. They show a **900mm decorative
quarter-arc**. The product is **90mm plates at multi-metre radii in runs of 16–60**.

A true headline over a misleading image is still a misleading ad. Requires `leepatt/cnccut-app` @
`claude/marketing-agents-setup-qamq2f` to re-render.

### B2. The re-render brief is bigger than "fix the arc" — hack #4
Suby's #4 (*don't make ads look like ads*) is the weakest part of the build, and the current renders
are catalogue cards. Our version of native is **a real part on a real site, a plan with a radius
marked on it, a stack of plates on a ute tray** — not a product-on-white card with a logo.

Doing B1 without B2 wastes the re-render. **Do them in one pass.**

### B3. Wire the ad set to the custom conversion
`promoted_object` → `27686282527680441`. The object exists; nothing points at it. Without this the
test optimises on the old event and reproduces July.

### B4. `META_PAGE_ID` into env
`611852278682648`. Needed by `create-creative`.

---

## 🟠 Should fix — will damage the test if skipped

| # | Item | Why |
|---|---|---|
| S1 | **Run `brand-check` live on the new batch** | Built, never run against a real image. First live run should not be on a batch we're about to publish |
| S2 | **Check EMQ > 7** | Not readable until ~2026-08-04/05. Phase 0 wants it above 7 before spend |
| S3 | **Scent-match `/products/radius-online`** | Hack #6, worth +15–20%, and free. At minimum the page's opening line shouldn't contradict the ads |
| S4 | **Decide on the Instagram placement** | No IG account linked. Facebook-only halves the inventory |
| S5 | **Confirm the ad set is broad AU, no interests** | The one setting July got right. Don't lose it |

---

## ⬜ Explicitly NOT blocking

- **Fit guarantee** — deferred by Lee, reassess after month one
- **Lead magnet / capture** — the biggest *structural* gap (July put ~13,000 people on the page and
  captured zero), but a test can run without it. It determines whether the test *compounds*, not
  whether it's valid
- **Plan Scan** — in beta, can't be advertised
- **Before/after photography** — in progress, `before_after` family stays empty

---

## Setting expectations on what the test can prove

**It will not exit Meta's learning phase, and no budget we'd sensibly spend would get it there.**

Learning needs ~50 conversions/week *for the ad set*. The whole site produces ~26 sales-intent
events/week. At a $322 break-even CAC, buying 50/week would cost ~$16,000/week. Not happening, and
that's fine — plenty of low-volume accounts run Learning Limited profitably.

**So judge the test on true CAC vs the $322 break-even, not on learning status or ROAS %.**

Rough shape of a readable test:

| | |
|---|---|
| Budget | $50–100/day, inside the $2k/mo ceiling already in code |
| Structure | **One ad set**, broad AU, no interests, optimising the new custom conversion |
| Duration | **3–4 weeks.** At $150–320 CAC that's a conversion every 2–3 days; ~10 conversions is the minimum readable sample |
| Read | Blended account-level CAC, because retargeting is live and will take last-click credit |
| Kill rules | Already coded: ≥72h AND ≥$25 AND 0 results; max 50% killed per run |

**Don't read it at 7 days.** A week at $75/day is ~$525 — one to three conversions. That's noise, and
reacting to it is how July's budget got scaled 13× in one step.

---

## The shortest path to live

1. Add `META_PAGE_ID=611852278682648` to env _(minutes)_
2. Re-render creative — right product **and** native, not catalogue cards _(the real work)_
3. Run `brand-check` live on the batch, then `check-batch`
4. Check EMQ > 7 _(2026-08-04/05)_
5. Build the ad set: broad AU, one ad set, `promoted_object` = `27686282527680441`
6. `propose` → Cockpit batch approval → `apply` with `CONFIRM=1`
7. Leave retargeting running. Read blended.

**Steps 1, 3, 4, 5 are quick. Step 2 is the whole job.**
