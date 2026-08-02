# Meta Ads — change log

_Account: `act_1650412872259063` (Craftons, AUD) · Pixel: `677437638374055`_

Every change made to the live Meta ad account gets recorded here, with the API response that
confirmed it. This exists because the Jul 22 campaign build was never written down — the next
session had no idea it existed. Don't repeat that.

---

## 2026-08-02 — Emergency stop after audit

Context: `meta-ads-audit-2026-08-02.md`. Sales fell after the Jul 22 launch (orders/day −42%,
conversion rate 1.49% → 0.066%) and the TOF campaign was poisoning the retargeting audience.

Authorised by Lee in-session. Both changes verified against the API after execution.

| # | Change | Object | Before | After |
|---|---|---|---|---|
| 1 | Paused campaign | `RadiusPro \| TOF \| Ardreagh \| Jul26` (`120247183657950186`) | ACTIVE, $70.00/day | **PAUSED** |
| 2 | Cut daily budget | ad set `Retargeting — BOF - Add To Cart` (`120232888615720186`) | $60.00/day | **$15.00/day** |

**Daily exposure: ~$130/day → $15.00/day.**

Verified account-wide after the changes — exactly one ad set still delivering:

```
Retargeting Campaign - Bottom Of Funnel | ...- Add To Cart   $15.00/day
TOTAL DAILY EXPOSURE: $15.00/day
```

TOF ad set `TOF | Broad AU | AddToCart` reads `effective_status: CAMPAIGN_PAUSED` — nothing beneath
the paused campaign is delivering. Final TOF spend on its last day (Aug 2): $85.97, 1,281 clicks,
15 add-to-carts, **0 purchases**. Campaign lifetime: $1,277 → 0 purchases.

### Deliberately NOT changed

- **`Retargeting — BOF – Purchase` ad set (`120233074187690186`) is still PAUSED** ($12.50/day).
  The live ad set optimises for Add-To-Cart, not Purchase. Recommended in the audit (§5.2), not yet
  authorised. **Open decision.**
- Nothing else in the account was touched. All other campaigns were already paused before today.

### Reversal

Both changes undo in seconds if wanted:
`POST /120247183657950186 status=ACTIVE` · `POST /120232888615720186 daily_budget=6000`

---

## Watch list (next review)

1. **Does retargeting recover at $15/day?** It produced 9 purchases / $12,797 on ~$15/day in
   Jul 8–21, then 1 purchase on a scaled-up budget once the pool was flooded. If it does **not**
   recover within ~2 weeks, the audience pool is the cause, not the budget — the 30-day visitor
   pool needs until roughly **2026-09-01** to clear the Jul 22 – Aug 2 junk cohort, and the
   180-day pools until **2027-01-29**.
2. **Cross-check Shopify before making any performance claim.** Meta claimed 2 purchases / $3,637
   from retargeting over Jul 22 – Aug 2; Shopify attributed 2 orders / $398 to all of
   Facebook + Instagram across 30 days. Never report on Meta's numbers alone.
3. **Before any relaunch:** confirm ViewContent *and* AddToCart are firing into the campaign in
   Events Manager on day one, before spend starts. The Jul 22–29 blind spend is exactly what that
   check prevents.
