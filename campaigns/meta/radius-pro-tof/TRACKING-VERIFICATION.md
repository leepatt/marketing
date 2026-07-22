# Paste-back to the calculator session: review sign-off + verification checklist

Copy everything below the line back into the `craftons-curves-calculator` session.

---

Reviewed the tracking implementation. It matches the spec and is built correctly. One confirmation, then
a verification checklist to run during the phone plus Test Events pass before you merge.

**CONFIRMATION (do not change this):**
The increment-value approach for AddToCart is correct. Keep sending the increase in the cart total per
AddToCart so the values sum to the cart total. Do NOT switch to sending the full running total each
time. Running total would make Meta add 172 + 173 = 345 and inflate value for optimisation and ROAS.
The current behaviour is the right one.

**VERIFY IN META EVENTS MANAGER DURING THE TEST (these cannot be seen from local stubs):**

1. **AddToCart deduplication.** The browser AddToCart (with `eventID`) and the CAPI AddToCart must send
   the **same** `event_id` so Meta merges them into one. In Events Manager the browser and server pair
   should show as deduplicated / counted once. Confirm the CAPI POST reuses the exact `eventID` generated
   for the browser event. If the two ids differ, every AddToCart is double counted.

2. **One Purchase per order.** The Meta Shopify app fires Purchase at checkout. Confirm exactly one
   Purchase per test order in Events Manager, not two (theme and app firing duplicates). If Shopify data
   sharing is set to Maximum it dedupes server-side, but eyeball it.

3. **Remove `META_TEST_EVENT_CODE` after testing.** While it is set, events route only to Test Events and
   do NOT count as live conversions. Do not deploy to production with it still set.

**GO-LIVE SEQUENCE (confirming the steps you listed):**
1. Paste the updated liquid section into the Shopify theme (browser events need it; CAPI works without it).
2. Generate the CAPI access token in Events Manager, Craftons Web pixel, Settings, Conversions API. Set
   `META_CAPI_ACCESS_TOKEN` in Vercel. Optionally set `META_TEST_EVENT_CODE` while testing, then remove it.
3. Merge and push to main.
4. Walk the flow on a phone with Test Events open and confirm: ViewContent on load, AddToCart with the AUD
   value on add-to-list, a second AddToCart on a second part, InitiateCheckout at checkout, one Purchase on
   completion, no duplicate AddToCart on the cart push, and AddToCart showing deduplicated between browser
   and CAPI.

**REPORT BACK:** confirm each walk-through event fired correctly, that AddToCart shows as deduplicated, and
that only one Purchase fired. Then this is done and I will start using the AddToCart signal on the ads side.

---
