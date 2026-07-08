# Meta TOF ad — "Form-Strip Reveal" (Concept A)

_Brief locked with Lee 2026-07-08: Concept A, $40/day. First top-of-funnel campaign for Craftons on Meta.
Companion docs: `briefs/craft-macro-shoot-brief.md` (the shoot — this ad IS Shot 1), `SOCIAL-VOICE.md`,
`CONTENT-PILLARS.md` (Craft Macro lane), `.claude/skills/craftons-design/BRAND.md`._

## Why this ad exists (the funnel job)

This is **not a sales ad.** Its job is to **refill the warm pool** that the bottom-of-funnel retargeting
campaign harvests at ~25× ROAS. That campaign is supply-constrained (14k reach, ~$14/day, nothing feeding
it). This TOF ad puts the most scroll-stopping thing Craftons makes — the form-strip reveal — in front of
cold builders/specifiers, drives a site visit + a video view, and **both actions drop them into the
retargeting audience.** TOF grows the pool; retargeting converts it. Judge this ad on pool growth, not on
its own ROAS (see Measurement).

## Campaign structure

- **Objective:** Traffic → optimise for **Landing Page Views** (LPV).
  - Rationale: a site visit makes a cold viewer retargetable via the existing pixel pool — that's what the
    25× campaign eats. LPV feeds it directly; pure video-views wouldn't.
- **Budget:** **$40/day** (CBO/campaign-level), one ad set. Leave the existing retargeting campaign as-is
  (~$14–20/day) — do NOT move its budget.
- **Landing page:** Formwork Builder — `/products/craftons-formwork-builder-custom-online-formwork`
  ("design yours"). It's the off-form/formwork product this reveal is literally showing.
- **Ad set (one, don't fragment the budget):**
  - **Audience:** start **broad / Advantage+ audience** (strong creative + Meta's algo beats hand-picked
    interests at this budget). Seed suggestions: Carpentry, Construction, Formwork, Concrete, Plywood,
    Cabinetry, Shopfitting, Residential construction, Building material, Architecture, Interior design.
    Fallback: if broad under-delivers after ~7 days, clone to a defined-interest ad set from that seed list.
  - **Location:** Greater Melbourne + Geelong + Mornington Peninsula + Surf Coast (match the AdWords
    footprint; metro-Melbourne delivery, broader by arrangement).
  - **Age/gender:** 25–55, all genders (specifiers + female tradies count).
  - **Placements:** Advantage+ placements. Creative is 9:16, so it leads in Reels / Stories / Feed.
- **Compounding setup (do once):** create two custom audiences to reinforce retargeting —
  (a) **Video viewers ≥25%** of this ad, (b) LP visitors (already in the pixel pool). Make sure the
  retargeting ad set includes them.

## The creative — video (hero)

The money shot from `craft-macro-shoot-brief.md`: **Shot 1 — the form-strip reveal.** Peel the plywood form
away to reveal a flawless curved off-form concrete face. Studio-clean rules still apply even on site — no
shed, no mess in frame; big-company polish.

- **Length:** 8–12s, vertical 9:16, designed to loop, **sound on** (the crack/suction of the form
  releasing is the premium cue — capture it clean).
- **Structure (3 beats):**
  1. **Tight on the form** (0–2s) — hand starts the peel. On-screen text lands the hook.
  2. **The peel** (2–7s) — slow reveal; let the concrete "arrive." Raking light grazes the curve.
  3. **The finished curve** (7–12s) — hold on the smooth arc; subtle logo end-frame.
- **Best version:** shoot Shot 6 (the pour) → Shot 1 (the strip) → Shot 2 (light across the curve) on one
  pour day and cut the mini-sequence "pour → strip → reveal." One shoot, a complete ad.

**On-screen text** (minimal, no emoji, sentence case; text-as-hook does the scroll-stop with the visual):
- Primary: `Flat form in.` → (on reveal) `Perfect curve out.`
- Alt (pain-led, more click intent): `Still bog-and-sanding your curves?` → (reveal) `There's a cleaner way.`
- End-frame line (subtle, paired with logo): `Off-form curves, cut to your set-out.`

## Caption (value-first, soft CTA — per SOCIAL-VOICE)

> Off-form curve, straight off the form. No bog, no sand, no three days of fairing a radius by hand.
>
> The formwork's cut to your set-out and turns up ready to pour — so the concrete comes out smooth and
> true the first time.
>
> Design yours in the Formwork Builder — link below.

- **Hashtags (tight):** `#offform #formwork #curvedwalls #concrete #building #construction #BuiltWithCraftons`
- Dial-up option (if we want more directness for paid): swap line 1 for the pain hook
  *"Still bog-and-sanding a radius on site? There's a faster way."*

## The static test variant (cheap A/B, same ad set)

Add as a **second ad in the same ad set** so Meta A/Bs them under the one budget (don't build a separate
campaign — it'd starve learning). Cut a single frame from the reveal — the finished curved concrete face,
raking light — with the `Flat form in. / Perfect curve out.` text baked in. This is the direct test of Lee's
"still images work best" question against the video, on cold traffic. (In-account so far: video is winning
2.10% vs 0.59% CTR — this confirms it on TOF, cheaply.)

## Measurement — how we judge it (don't misread TOF)

- **Run 10–14 days before any call.** Cold audiences + a new pixel signal need time to settle.
- **Primary (creative health):** link CTR **>1%**, cost per **LPV < ~$1.50**, 3-sec/hook rate **>30%**,
  ThruPlay rate healthy. Video vs static: compare CTR + cost/LPV directly.
- **The real KPI (funnel effect):** the **retargeting campaign's reach + purchase volume should climb** as
  the pool fills. That's where this ad's ROAS actually shows up — TOF itself will NOT print 25×, and that's
  correct. If retargeting reach grows and its conversions hold, the TOF spend is working.
- **Kill/scale rule:** if broad under-delivers by day 7, switch to the interest ad set. If creative health
  is good and retargeting volume rises, scale TOF budget in ~20–30% steps.

## Production dependency (the one blocker)

The form-strip reveal is a **pour-day, on-site shot** — it needs a real job pouring an off-form curve.
- **If a pour is imminent:** Tia shoots 6→1→2 per the Craft Macro brief; we cut the ad from that.
- **If pour day is weeks out:** we can launch an interim TOF video from **Session A studio shots**
  (Shot 3 flat-sheet→curve flex, or Shot 5 the seam) to start filling the pool now, then swap in the
  form-strip hero once it's shot. Flag to Lee which path — don't let the pour-day dependency stall the $40/day.

## Status

- [x] Concept + budget locked (A, $40/day) — 2026-07-08
- [ ] Confirm shoot path (imminent pour vs interim studio ad) — **Lee**
- [ ] Tia shoots Shot 1 (+ 6, 2 for the sequence) — depends on pour day
- [ ] Build campaign in Meta (Traffic/LPV, broad, $40/day) + 2 custom audiences — Claude/Lee once footage lands
- [ ] Static test frame cut + added as 2nd ad
- [ ] Launch → 10–14 day read → scale or switch to interest ad set
