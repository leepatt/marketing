# Google Ads module — the first cockpit module (spec)

_Draft 2026-06-30. Planning only. The first module of the Craftons Marketing Cockpit (`PLAN.md`).
Built on the engine we already have: `tools/google-ads.mjs` (read) + `tools/google-ads-launch.mjs`
(gated writes) + the live campaign `23983924746`._

> Goal: pull Google Ads data, show it cleanly, and let Claude propose changes that Lee applies with a
> click — with a chat bar to talk to the brain. This is the template every other channel copies.

---

## 1. Screen layout (the thing Lee looks at)

```
┌───────────────────────────────────────────────────────────────────────────────┐
│  CRAFTONS COCKPIT · Google Ads        Marketing Score 720 ▲28   🔥 4-day streak │
│  [ Ads ] Sales  Social  Email  Newsletter  LinkedIn  Content                    │
├───────────────────────────────────────────────────────────────────────────────┤
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────────┐        │
│  │ SPEND  │ │ CLICKS │ │ LEADS  │ │ $/LEAD │ │  CTR   │ │ HEALTH       │        │
│  │ $48/day│ │  32    │ │   2    │ │ $24 ▼  │ │ 5.1% ▲ │ │  82 🟢       │        │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └──────────────┘        │
│  ┌──────────────────────────────────────────┐ ┌─────────────────────────────┐  │
│  │ Spend vs Leads — 14 days                  │ │ 🧠 RECOMMENDATIONS (3)       │  │
│  │   ▁▂▃▅▆▇▆▅▅▆▇█▇                            │ │ ① Add negative "guitar"      │  │
│  │                                            │ │    6 clicks · $17 · 0 leads  │  │
│  │ ── Campaigns / Ad groups / Keywords ──     │ │    [ Apply ]  [ Dismiss ]    │  │
│  │  Radius Pro       $19  12clk  1 lead  $19  │ │ ② Pause kw [curved ply panel]│  │
│  │  Formwork         $17  11clk  1 lead  $17  │ │    22 clk · $41 · 0 leads     │  │
│  │  Architraves      $12   9clk  0 lead   –   │ │    [ Apply ]  [ Dismiss ]    │  │
│  │                                            │ │ ③ Shift +$10/day → Formwork  │  │
│  │ [Campaigns][Ad groups][Keywords][Terms][Ads]│ │   (best $/lead this week)    │  │
│  │  💧 Wasted-spend leak meter:  $58 ▼         │ │    [ Apply ]  [ Dismiss ]    │  │
│  └──────────────────────────────────────────┘ └─────────────────────────────┘  │
├───────────────────────────────────────────────────────────────────────────────┤
│  💬  Ask the brain…   e.g. "why did leads drop yesterday?"            [ Send ]   │
└───────────────────────────────────────────────────────────────────────────────┘
```

- **Top tiles** = the headline numbers, each with a trend arrow vs the prior period.
- **Left main** = chart + drill-down tabs (Campaigns → Ad groups → Keywords → Search terms → Ads),
  plus the **A/B panel** for our pinned-vs-unpinned RSA test (see §5).
- **Right rail** = the **recommendations feed** — Claude's proposed changes as click-to-apply cards.
- **Bottom** = the **chat bar** — talk to the brain; it can answer *and* drop new action cards inline.

## 2. Data the module pulls (from Google Ads API v21)

- **Account/campaign:** name, status, serving status, budget, bidding strategy.
- **Metrics** (by day, campaign, ad group, keyword, search term, ad): impressions, clicks, cost,
  conversions, conversions value, CTR, avg CPC, cost-per-conversion, conversion rate, impression
  share + lost-IS-to-budget/rank.
- **Entities:** keywords (+ match type), negatives, search terms, RSAs (+ ad strength, policy/approval
  status), extensions/assets.
- **Refresh:** scheduled snapshot (the existing daily monitor) + an on-demand "Refresh now" button.
  Store daily snapshots in the DB so trends/streaks work without re-pulling history.

## 3. KPI tiles (top row)

| Tile | Definition | Why it's here |
|------|-----------|---------------|
| **Spend** | cost, today + 7-day avg/day | are we within budget |
| **Clicks** | clicks, period | traffic volume |
| **Leads** | conversions (form_submit + purchase) | the actual goal |
| **$/Lead** | cost ÷ conversions | the real scoreboard (vs job value) |
| **CTR** | clicks ÷ impressions | ad relevance |
| **Health** | 0–100 composite (see §6) | one-glance "are we ok" |

## 4. Actions Claude can propose (each = a click-to-apply card → a gated tool call)

Every card maps to a **CONFIRM-gated** write (the `google-ads-launch.mjs` pattern, extended). The card
shows the *evidence* (why) + the *change* (what) + **[Apply] / [Dismiss]**. On Apply: backend runs the
write, logs to audit, refreshes the view.

| Action | Trigger (what Claude looks for) | Underlying write |
|--------|-------------------------------|------------------|
| **Add negative keyword(s)** | search term ≥5 clicks, 0 conv, irrelevant | add campaign/ad-group negative |
| **Pause keyword** | keyword ≥20 clicks, ~$40, 0 conv | set keyword PAUSED |
| **Pause / enable ad** | ad disapproved, or clear A/B loser | set ad status |
| **Adjust bid (cap)** | keyword over/under cost-per-lead target | set cpc_bid_micros (within cap) |
| **Shift / change budget** | one ad group clearly best $/lead | change campaign budget (≤ ceiling) |
| **Add keyword** | strong converting search term not yet a keyword | add keyword (phrase/exact) |
| **Create / edit RSA** | ad strength low, or new angle to test | create/update RSA |
| **Pause / enable campaign** | emergency stop / go-live | set campaign status |

**Action card schema (what the brain emits so the UI can render a button):**
```json
{
  "id": "rec_2026-07-01_001",
  "type": "add_negative",
  "title": "Add negative \"guitar\"",
  "evidence": { "searchTerm": "guitar", "clicks": 6, "cost": 17.0, "conversions": 0, "window": "7d" },
  "change": { "level": "campaign", "keyword": "guitar", "matchType": "PHRASE" },
  "impact": "Stops ~$17/wk of hobbyist waste",
  "risk": "low",
  "status": "pending"   // pending | applied | dismissed
}
```

## 5. A/B panel (our live test)
A dedicated card tracks the **pinned vs unpinned RSA** test per ad group: impressions, CTR, $/lead for
each ad, and once there's enough data, a **"Pin wins / Unpinned wins"** verdict with a one-click
"pause the loser" action. This is the gamified "experiment" surfaced as a mini-scoreboard.

## 6. Gamification for this module — **LIGHT** (per `PLAN.md` §6)

Two signals only:
- **Ads Health (0–100):** blends $/lead vs target, CTR, % budget not wasted, all-ads-approved, has
  conversions. Green/amber/red.
- **Leak meter 💧:** running total of spend on 0-conversion search terms in the window. Applying
  negatives visibly drops it — instant feedback.

_(Score/streaks/quests/badges are intentionally out of scope for now — can revisit later.)_

> **Autonomy (per `PLAN.md` §4):** start with every action a click. Later, `add_negative` cards with
> `risk:"low"` may auto-apply (with an "auto-applied (undo)" entry in the feed); budget/bid/pause/ad
> changes always wait for Lee's click.

## 7. Build phases (this module)

1. **Read-only view** — connector (port `google-ads.mjs`) → KPI tiles + 14-day chart + drill-down
   tables. Just see it. *No writes.*
2. **Recommendations feed** — the daily/weekly brain writes action cards to the DB; UI renders them
   read-only (advice, no buttons yet).
3. **Click-to-apply** — wire [Apply] to the gated writes + audit log + auto-refresh. Start with the
   safest action (add negative), expand outward.
4. **Chat bar** — embed the conversational brain; it answers questions and can emit cards inline.
5. **Gamify** — health score, leak meter, quests, streak.

## 8. Reuse / not-from-scratch
- `tools/google-ads.mjs` → the **connector** (reports, search terms, identity).
- `tools/google-ads-launch.mjs` → the **write/action handlers** (already does atomic, validated,
  all-or-nothing mutations with a CONFIRM gate — exactly what Apply needs).
- The **daily monitor routine** → the engine that **populates the feed**.
- The **propose→approve law** → the **Apply/Dismiss** UX.

> Net: Phase 1–2 are mostly **UI over data we already pull**; the risky write-path is already built and
> battle-tested by this week's launch. That's why Google Ads is the right first module.
