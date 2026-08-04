# Creative strategy — what actually works, and the register mix

_Written 2026-08-03 after Lee reviewed the 33-ad brand-guide batch: **"They're okay. Some of them are
okay."** and questioned whether the Residency guide is an advertising system at all._

---

## 1. Lee was right, and the account proves it

> *"I wonder if that design guide is more for posting on Instagram rather than the ads… I don't think
> just a background with some text on is going to be very engaging."*

**Correct.** `Craftons_BrandGuide_SocialLayouts01.pdf` is titled **"Brand Guidelines - Socials"** and
its examples are organic posts — "HOW TO GUIDE", "Free Melbourne Shipping / SEPTEMBER SPECIAL". It is
a **posting** system. I applied it as an **advertising** system and produced 33 branded cards.

Suby's hack #4 says the same thing from the other direction: *if it reads as an ad, it's dead on
arrival.* A flat colour field with type on it reads as an ad instantly.

---

## 2. Teardown of the ad that actually worked

**`AD5 Chippies | curved wall frame (Lawless)`** — creative `1347855387557688`.
**10.45% CTR · 9,244 landing page views at $0.08 · 132 reactions · 12 saves.** Best hook the account
has ever run.

### The image

**A bare site photo. No overlay text. No logo. No brand furniture. Nothing designed on it at all.**

A curved timber stud wall standing on a real slab, blue sky, other framing around it, a bloke working
in the background. It looks exactly like something a builder posted from site — because it is.

> **This is the finding.** The best-performing creative in the account is the one with *no design on
> it*. My 33 branded typographic cards are the opposite of it.

### The copy — and the uncomfortable part

> *"Any architect can draw a curve. Now any chippy can frame one.*
>
> *The curved feature wall is the bit that looks unreal in the render and then causes you headaches
> on site.*
>
> ***The old way is some maths, a jigsaw, and a day you didn't have. Cutting every curved plate by
> hand, following the line, and binning half a pack of ply when it doesn't go to plan.***
>
> *This one turned up solved. The curved top and bottom plates came cut to the exact radius. 17mm
> Formply, machined, engraved, delivered. **@lawlessconstruction** framed this one up, and the curve
> was never in question.*
>
> *Architects aren't going to stop drawing them. Now they don't have to be your problem. Punch in the
> radius, we cut the plates. Laminate two to 34mm and stand your wall."*

**Maths. Jigsaw. Binning half a pack of ply.** That is Lee's entire product briefing — written in
**July**, three weeks before he gave it to me, in the best-performing ad in the account.

**So the "research" this session did largely rediscovered what the winning ad already said.** The
lesson is the same one this repo keeps learning: *look at what exists before producing something new.*
Next time, the first move on a creative brief is to read the top-performing ad's copy.

### Why it works — five things, reusable

| # | Ingredient | Why it matters |
|---|---|---|
| 1 | **A real job, photographed on site** | Native. Passes as organic. Nothing to design |
| 2 | **A named real customer** (`@lawlessconstruction`) | Social proof, and the tag borrows their audience |
| 3 | **Long-form copy in trade voice** | Meta doesn't punish length when it's read. This is a story, not a slogan |
| 4 | **The pain named precisely** | "a day you didn't have", "binning half a pack of ply" |
| 5 | **A concrete instruction** | *"Laminate two to 34mm and stand your wall."* Only someone who knows the job writes that |

---

## 3. The register mix

Lee: *"don't disregard the brand guidelines… but I don't think that needs to be everything… some
content using that method and some other content with images and AI avatars."*

That is exactly what the `CREATIVE_FAMILIES` gate in `_meta-policy.mjs` was built for — and it also
solves the 2-families-vs-3 failure honestly rather than by relabelling.

| Register | Family | Status | Notes |
|---|---|---|---|
| **Real job photography** | `real_footage` / `before_after` | 🔴 **The proven winner. 1 photo exists** | Highest priority. Every new job photo is a potential winner |
| **The configurator / the tool** | `configurator` | 🟡 Screenshot only | Lee: *"our product is the configurator, is the tool."* Screen capture > static screenshot |
| **The end result** | `real_footage` | 🔴 Blocked on photos | Curved walls, curved concrete, finished work |
| **AI avatar presenter** | `avatar` | ⛔ **Blocked — no API key** | Lee wants tests. Capped at 40% of a batch |
| **Brand-guide typographic** | `static_craft` | ✅ 33 built | **One register, not the system.** Good for spec/number/offer cards |

**The mix is the point.** Andromeda reads family spread as genuine diversity; five registers is
strictly better creative *and* clears the gate.

---

## 4. Blockers, precisely

### 4.1 🔴 Photography — the biggest single lever
One real site photo has out-performed everything else in the account. **There is exactly one.**
Everything else in the repo is a CGI product render on white.

**What to capture, in priority order:**
1. **Curved timber stud walls standing on site** — the proven winner, more angles, more jobs
2. **The pack as delivered** — plates strapped on a pallet, part IDs visible. Proves "cut, labelled"
3. **Curved concrete / off-form after the strip** — the end result for concreters
4. **Nesting on the bed** — parts laid out on the sheet before cutting. The waste argument, made visible
5. **Before/after** — a hand-cut curve next to a machine-cut one

Phone photos from site are *better* than studio here — the winner is a phone photo.

**Also worth doing: ask past customers.** `@lawlessconstruction` already let us use one. The
`CURVED-JOBS-WINLOSS.md` repeat buyers (Perfetto, Invoke, Glenvill, LBA, Frameworks, Montegar) are the
obvious ask.

### 4.2 ⛔ AI avatars — blocked on credentials
`HEYGEN_API_KEY` and `ANTHROPIC_API_KEY` are **in Vercel but NOT in session env.** Verified this
session. Nothing avatar-related can be built or tested until they're mirrored into the session
environment (or the work runs inside a Vercel function).

**ACL constraint, already in code** (`_meta-policy.mjs`): a synthetic presenter may describe the
product, but **must never claim first-person experience of it** — that's an ACL s18/s29(1)(e) breach.
Scripts stay second-person about the product.

### 4.3 🟡 Configurator capture
Lee: *"our product is the configurator, is the tool."* The current proof asset is a static screenshot
showing unrepresentative values (150mm width, qty 1). A **screen capture of someone actually typing a
radius and the price appearing** is a far stronger asset, and it's the single most-converting path on
site (~54 orders / ~$26,800).

---

## 5. What to do next, in order

1. **Get photos.** Nothing else moves the needle as much. One phone photo beat a designed batch.
2. **Mirror `HEYGEN_API_KEY` + `ANTHROPIC_API_KEY`** into session env so avatars can be tested.
3. **Capture the configurator in use** — screen recording, not a screenshot.
4. **Lee + Tim conversation** on where the Residency system applies. Current read: organic posting and
   spec/offer cards yes; cold-traffic hooks no.
5. **Cut the 33 down** to the ones worth keeping as the typographic register, once Lee flags them.
6. **Rewrite the long-form copy pattern** from the winner — it is a proven template and nothing in the
   current batch uses it. Every ad in the new batch has short copy; the winner's is six paragraphs.

---

## 6. What this changes about the batch already built

Not deleted — **re-scoped.** 33 typographic cards are a legitimate register and some will be useful,
especially for offers, specs and retargeting where the viewer already knows Craftons. They are the
wrong tool for a cold-traffic hook, which is what the launch test needs.

**The launch batch should lead with real photography and the configurator, and use the brand-guide
cards as support** — not the other way round, which is what I built.
