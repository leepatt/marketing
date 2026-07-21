---
name: craftons-dream-buyer
description: Craftons' market-research engine — our in-house build of King Kong's "Dream Buyer Avatar" tool (Kong / getkong.ai). Scrapes the sewers (Reddit, AU trade forums, YouTube, reviews/Q&A, plus any Facebook group threads Lee feeds in) for the market's VERBATIM language, distils it into an "obsessed-stalker" Dream Buyer Avatar (desires, beliefs, fears, pains, goals, emotions, buying triggers, objections + a raw language bank), then drives ads, offers and U-U-S-U headlines from it. Use whenever we need to research the market, build or refresh the buyer avatar, mine what real builders/concretors/architects are actually saying, or generate research-driven ad/offer copy. Triggers on: market research, customer research, dream buyer, buyer avatar, what are builders saying, mine customer language, voice-of-customer, research-driven ad copy, "do the research". Pairs with: direct-response-copy, positioning-angles, craftons-voice, keyword-research. Governed by MARKETING-BIBLE.md (Pillar One).
---

# Craftons Dream Buyer — the market-research engine

Our own version of the tool Sabri Suby (King Kong) sells as **Kong** ($79–299/mo). Kong's pitch is
*"it scrapes the internet, the sewers, gets the raw materials and does all the research in the click of
a button,"* then builds a **Dream Buyer Avatar** and spits out ads + headlines. The scraping is mostly
marketing framing — Kong is really an LLM trained on his ad data. **We do the part Kong only claims**:
real scraping of Craftons' actual AU market, in our buyers' real words, owned by us, for free.

This skill is the doctrine's **Pillar One** made executable (`MARKETING-BIBLE.md` §1). All the money is
in the research. Run it before writing any ad, page, offer or email.

## The pipeline (three stages)

```
  STAGE 1 — SCRAPE            STAGE 2 — AVATAR              STAGE 3 — GENERATE
  the sewers        ──▶       obsessed-stalker    ──▶       ads · offers · U-U-S-U
  (verbatim quotes)           Dream Buyer Avatar            headlines (from the avatar)
```

Outputs live in `research/market-intel/`:
- `QUOTE-BANK.md` — raw verbatim quotes, sorted (Stage 1)
- `DREAM-BUYER-AVATAR.md` — the distilled avatar (Stage 2)
- copy is generated on demand into the relevant campaign/page (Stage 3)

---

## STAGE 1 — Scrape the sewers (get the raw material)

Fan out **parallel research subagents**, one per source cluster. Each returns verbatim quotes tagged by
segment + category with a working source link.

**The source clusters (AU-only market):**
1. **Reddit** — r/AusConstruction, r/concrete, r/Formwork1, r/carpentry, r/woodworking, r/bunnings, AU city subs.
2. **AU trade & reno forums** — renovateforum.com.au, forums.whirlpool.net.au, workshop.bunnings.com.au, homeone.com.au, woodworkforums.com, productreview.com.au.
3. **YouTube** — AU curved-wall / curved-formwork / bench-seat build videos: transcripts + comments.
4. **Architects / specifiers** — architectureau.com, houzz.com.au, LinkedIn, spec/detailing threads.
5. **Reviews · Q&A · competitor complaints** — Google/ProductReview reviews of AU suppliers, Quora AU, StackExchange DIY, hipages/Airtasker job posts. Competitor one-stars = our positioning.
6. **Facebook groups (Lee-fed)** — no API can read private groups (Meta locked the Groups API in 2024).
   Lee pastes/screenshots threads; mine them into the same bank. This is the richest AU source.

**The three segments we care about** (weight per the current brief; default all three):
- **Concrete formwork** (concretors / form carpenters — curved walls, bench seats, firepits)
- **Curved timber framing** (carpenters — curved walls, plates, studwork, bending-ply linings)
- **Architects / specifiers** (buildability, budget, finding a supplier, detailing curves)

### ⚠️ CRITICAL — subagent setup (this is how the tool breaks)
Web tools are **deferred** in this environment. A subagent that doesn't load them does **zero research**
and returns in seconds with nothing (or, worse, fabricates). Every research subagent prompt MUST start with:

> **STEP 0 (do first):** call `ToolSearch` with query exactly `select:WebSearch,WebFetch` to load your
> web tools. You cannot search until you do. Then proceed.

Watch the completion notifications: **0 tool_uses + a few seconds = the agent failed** → re-dispatch it
with the STEP 0 fix. Don't trust its output.

### The three laws of Stage 1 (never break these)
1. **AU-only.** Every quote needs an Australian signal (AU sub/forum/.au, AU spelling, AU terms —
   concretor, chippy, formply, reno, Bunnings, AUD, place names, AU supplier). No signal → exclude.
   If a cluster is genuinely thin, allow a few *clearly-labelled* non-AU quotes in a separate section.
2. **Verbatim.** Copy exact words — slang, typos, swearing. Never paraphrase or "clean up." Their exact
   language IS the deliverable (it's what makes copy read like we hacked their Gmail).
3. **No fabrication.** Real quotes with working links only. 8 real quotes beat 30 invented ones. If a
   quote can't be verified, it doesn't go in.

**Per-quote schema:** `QUOTE` (verbatim) · `WHO` (trade/role) · `AU SIGNAL` · `SEGMENT` · `TAG`
(pain / desire / objection / language / trigger) · `SOURCE` (URL) · `CONTEXT` (one line).

Collate all subagent returns into `research/market-intel/QUOTE-BANK.md`, deduped, sorted by TAG then SEGMENT.

---

## STAGE 2 — Build the Dream Buyer Avatar (distil the raw material)

Synthesise `QUOTE-BANK.md` into `research/market-intel/DREAM-BUYER-AVATAR.md`. **Every claim in the
avatar must be backed by real quotes** from Stage 1 — cite them. No quote to support a trait = it's a
guess, cut it. Mirror Kong's fields (this is the "obsessed-stalker" persona):

- **Who they are** — the one person (not "builders"): trade, context, the job on the board.
- **Deepest desires** — what they actually want (backed by desire-tagged quotes).
- **Fears & pains** — the nightmare (the curve not fitting on site, blown program, rework, cracking).
- **Beliefs** — what they already believe about curved work / suppliers / "doing it myself."
- **Objections** — every reason they hesitate (cost, "will it fit", "is it strong enough", trust).
- **Buying triggers** — the moment they go looking ("got a curved job", "architect specced a radius").
- **Emotions** — how the problem makes them feel (in front of the builder, on a deadline).
- **The verbatim language bank** — their exact words/phrases, grouped, ready to drop into copy. This is
  the single most valuable output. (Confirmed converters already: *"bendy ply"*, *"curved bench seat"*.)

Keep it living — date it, refresh quarterly or when the market shifts. Feed confirmed search terms back
into `brand/keyword-plan.md` and pains/desires back into `brand/audience.md`.

---

## STAGE 3 — Generate (turn the avatar into money)

The avatar drives copy. Hand it to the copy skills — the avatar IS their input:

- **Offers** → build/sharpen the Godfather offer (`MARKETING-BIBLE.md` §4): the desire it fulfils + the
  fear it reverses, in their words. Every ad/page carries the same offer + risk reversal.
- **Ads & headlines** → `direct-response-copy` + the bible's **U-U-S-U gate** (Urgent · Unique ·
  Specific · Useful). Every headline must quote or echo the avatar's verbatim language before it ships.
- **Angles** → `positioning-angles` for the hero-mechanism / category-of-one framing.
- **Pages/emails** → same language bank; social stays value-first (`craftons-voice`), ads go direct-response.

**The one hard rule:** no ad, page, offer or email gets written without a verbatim quote from the avatar
for the problem it addresses. No quote = not ready to write.

---

## Running the tool (quick recipe)

1. **Scope** — confirm segments, geography (default AU-only), and deliverable with Lee if unset.
2. **Scrape** — dispatch the 6 clusters as parallel subagents (STEP 0 fix in every prompt). Re-dispatch any that misfire.
3. **Collate** — merge returns → `QUOTE-BANK.md`, deduped and sorted.
4. **Distil** — write `DREAM-BUYER-AVATAR.md`, every trait cited to a quote.
5. **Generate** — produce a first set of offer angles + U-U-S-U headlines to prove the pipeline end-to-end.
6. **Feed back** — update `audience.md` + `keyword-plan.md`; note coverage gaps (esp. where FB threads would help).
7. **Mirror** — copy the intel to the Drive brain (`…/01 Craftons/Marketing/`).
8. **Refresh** — it's a living document; re-run quarterly. Markets move.
