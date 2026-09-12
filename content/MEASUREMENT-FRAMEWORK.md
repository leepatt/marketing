# Craftons content — measurement framework

**Purpose:** make the next 8 weeks of content produce *learning*, not just posts.
**Status:** draft for Lee/Jake sign-off, 2026-09-12.
**Companion:** `content/post-log.csv` (the data), `CONTENT-PILLARS.md` (the lanes), `SOCIAL-VOICE.md` (the voice).

> **The failure mode this exists to prevent:** Jake films for two months, 50 videos go out,
> nobody tags them, and at the end we have a feed and no answers. Tagging takes 60 seconds
> per post. Skipping it wastes the whole experiment.

---

## 1. What we are actually testing

Not "does content work". Too vague to answer. We're testing **five specific variables**, one
at a time, so the results mean something:

| # | Variable | Levels we'll test |
|---|---|---|
| 1 | **Source** | Jake self-shot · Tia shoot · customer-supplied · how-to series · machine/workshop |
| 2 | **Format** | talking head · process/making · finished reveal · before-after · macro detail |
| 3 | **Hook type** | question · problem statement · bold claim · number · cold visual open · POV |
| 4 | **Opening frame** | Jake's face · the machine · the finished product · the job site |
| 5 | **Length** | <15s · 15–30s · 30–60s · 60s+ |

Everything else (voice, pillars, posting cadence) stays **fixed** for 8 weeks. If we change
everything at once we learn nothing.

---

## 2. The metrics that matter, in order

Instagram's own ranking behaviour as of 2026 — this order is not arbitrary:

| Rank | Metric | Why |
|---|---|---|
| 1 | **Average watch time** | The #1 Reels ranking signal (Mosseri, Apr 2026) |
| 2 | **Completion rate** | Predicts reach better than any engagement metric |
| 3 | **Sends (DM shares)** | Carry **3–5× the algorithmic weight of likes** |
| 4 | **Saves** | Intent signal — especially strong for how-to content |
| 5 | **3-second skip rate** | Diagnoses the hook specifically |
| 6 | Shares, comments | Useful, noisier |
| 7 | **Likes** | Nearly useless. Track it, never decide on it. |

**Derived metrics we'll actually rank on:**
- `watch_ratio` = avg watch time ÷ video length *(format quality)*
- `save_rate` = saves ÷ reach *(usefulness)*
- `send_rate` = sends ÷ reach *(word-of-mouth)*
- `hook_hold` = 100 − skip_rate_3s *(hook quality, isolated)*

**Business metrics (the only ones that pay):** enquiries that mention content, "how did you
hear about us" answers, quotes issued, orders. Logged separately in `post-log.csv` notes and
cross-checked against ClickUp/Quotient monthly.

---

## 3. Measure at a fixed age

**Log every post at 7 days, then again at 28 days.** A post measured at day 2 and one measured
at day 20 are not comparable, and this is the single most common way content data gets ruined.

Reels keep accumulating views for weeks. Day-7 is the decision number; day-28 catches the
slow burners (which matter — a post still earning at day 28 is a format worth repeating).

---

## 4. Honesty rules — hold me to these

I will find patterns in this data whether or not the patterns are real. Social metrics are
extremely high-variance; the noise is bigger than most effects. So:

1. **No claim from fewer than 5 posts per variant.** Below that I say "not enough data" and
   we keep collecting. This is not hedging, it's the correct answer.
2. **Report the spread, not just the average.** One viral post drags a mean anywhere.
3. **Flag single-outlier results explicitly.** "Talking heads win" off the back of one hit is
   not a finding.
4. **Effect size before significance.** A 5% difference in watch ratio is noise. A 2× difference
   is worth acting on.
5. **Business metrics override engagement metrics.** A post with 400 views that produced a
   quote beats one with 40,000 that produced nothing. Always.
6. **Say when I'm guessing.** Distinguish "the data shows" from "my read is".

---

## 5. The weekly loop

**Friday (Jake or Lee, ~15 min):** log the week's posts into `post-log.csv` at their 7-day
numbers. Re-log any post hitting 28 days.

**Friday (Claude):** read the log and produce:
- What moved, with effect sizes and honest confidence
- What to stop doing
- **5 specific video ideas for next week** — each with a hook line, a shot list, and which
  variable it's testing
- Any "not enough data yet" calls

**Monthly:** bigger review. Kill the bottom formats, double the top two, re-check against
quotes and orders. Update `CONTENT-PILLARS.md` if a pillar is clearly dead.

---

## 6. Getting the data out of Instagram

**Option A — manual (start here).** Instagram Professional Dashboard → each post → Insights.
Type the numbers into `post-log.csv`. ~60 seconds per post. At ~26 posts/month that's 25
minutes a month. Start here; don't build anything yet.

**Option B — Instagram Graph API (later, if volume justifies it).** Business/Creator account
linked to a Facebook Page. Exposes plays, reach, saves, shares, `ig_reels_avg_watch_time`,
completion rate and `reels_skip_rate`. **Requires 1,000+ followers for engagement insights —
confirm Craftons is over the line before building anything.** Note Meta deprecated
`video_views`, `profile_views` and `website_clicks` from Graph API v21 (Jan 2025), so don't
design around those.

Build Option B only once manual logging has proven the habit sticks. Automating a habit
nobody has yet is how tooling gets built and abandoned.

---

## 7. Tooling costs

| Tool | Cost | Notes |
|---|---|---|
| Submagic Starter | $19/mo ($12 annual) | Captions, silence removal, auto-zoom |
| Submagic Pro | $39/mo ($23 annual) | More exports/features |
| **Submagic Business + API** | **$69/mo ($41 annual)** | 100 API min/mo, then $0.15/min (≤2,000), $0.10/min high volume |
| Instagram Graph API | Free | Needs FB Page link + 1,000 followers |

**Start on Starter or Pro.** The API tier only pays for itself once we're automating a
pipeline, and we shouldn't automate before the format is settled.

---

## 8. The 8-week plan (Lee's structure)

Fixed cadence, mixed sources so no single bottleneck stops the feed:

| Source | Per week | Per 8 weeks | Who |
|---|---|---|---|
| Jake self-shot (phone + Submagic) | 2 | 16 | Jake |
| Tia shoot (finished product on site) | ~3 videos from 1 shoot, fortnightly | ~12 | Tia films + edits |
| Customer-supplied content | ~1 | 8 | Lee to collect |
| How-to series episodes | ~0.5 | 4 | existing storyboards |
| **Total** | **~5/week** | **~40** | |

**~40 posts over 8 weeks** — enough for 5+ posts per variant on the main tests, which clears
the honesty bar in §4. It does *not* clear it for subtle interactions; expect format-level
answers, not fine-grained ones.

**The real test is week 5–8, not week 1.** Everyone films in week one. Sustaining two a week
while running production is the actual experiment, and the honest thing to do at week 4 is
re-baseline the plan against what Jake actually managed rather than what we hoped.

---

## 9. One caution on "quantity over quality"

Right call for learning — you cannot find the format without volume, and polish is the enemy
of frequency. But there is a floor.

Rough-and-useful is fine: phone footage, natural light, Jake explaining a real problem.
**Genuinely bad is not fine** — inaudible audio, no hook, nothing learned. Weak posts don't
just underperform, they teach the algorithm the account is low-quality and can suppress
reach on later posts.

The bar isn't production value. It's: **does this post say one useful thing to a builder in
the first three seconds.** If yes, ship it rough.
