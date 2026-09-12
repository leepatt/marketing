# Craftons reel editing — desktop setup

Prompt-driven editing of Jake's talking-head reels. **Lee prompts, Claude edits, CapCut renders.**

> **Runs on Lee's desktop only.** A cloud Claude session cannot reach CapCut — no install, no
> filesystem access, and CapCut ships no public API. Everything here assumes local Claude Code.

> ⚠️ **Untested end to end.** The CapCut half was written without a CapCut install to test
> against. Expect to iterate on the first video. The transcription half **is** verified working.
> Flagging this so a failure on day one reads as expected, not broken.

---

## What this is, and what it isn't

**Is:** a written spec your local Claude Code reads (`CLAUDE.md`), plus transcription, plus a
maintained third-party bridge that writes CapCut project files.

**Isn't:** a CapCut template file. Because you direct by prompt rather than by clicking, the
"template" is instructions Claude can read — brand rules, caption style, safe zones, the trade
vocabulary Whisper mangles. That file is the actual asset here. The tooling is replaceable.

---

## Why this stack

The YouTube walkthrough used Deepgram + Remotion + Kie.ai. Two deliberate changes:

| Their stack | Ours | Why |
|---|---|---|
| Deepgram (API key, paid) | **faster-whisper**, local | Free, no key, no upload. Verified working |
| Kie.ai AI B-roll | **dropped** | Real footage leads. AI footage would waste Craftons' only structural content advantage |
| Custom bridge script | **VectCutAPI** | Someone else maintains the undocumented CapCut draft format. That's the fragile part — don't own it |
| Remotion | **later, if needed** | Heavy. The spec stamp can be a still overlay first. Add motion only once the format is settled |

---

## Setup — once

> **Step-by-step with checkpoints: [`SETUP-DESKTOP.md`](SETUP-DESKTOP.md).** Use that, not the
> summary below, if you're setting this up for the first time.

**Prerequisites:** CapCut desktop installed, Claude Code working locally, Python 3.10+, Node.

```bash
# 1. this repo, on your desktop
git clone -b claude/dreamy-fermi-gfqbdj https://github.com/leepatt/marketing   # BRANCH, not default
cd marketing/pipeline/video-edit

# 2. transcription (free, local, no API key)
pip install faster-whisper imageio-ffmpeg

# 3. the CapCut bridge
git clone https://github.com/sun-guannan/VectCutAPI
cd VectCutAPI
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-mcp.txt                  # MCP, so Claude can drive it
```

Then start it — HTTP server on 9001, or the MCP server for Claude:

```bash
python capcut_server.py        # HTTP API
# or
python mcp_server.py           # MCP — this is the one you want
```

**Register the MCP server with local Claude Code** so Claude can call it directly. VectCutAPI's
own README has the config block; ask your local Claude to wire it up and restart.

**Sanity check before any real work:** ask local Claude to create an empty CapCut draft and open
it. If that works, the hard part is done. If it doesn't, the draft-format version has likely
drifted — check VectCutAPI's issues before debugging yourself.

---

## The loop

```
Jake films (phone + lav mic)
        ↓
footage lands in Drive / a local folder
        ↓
python transcribe.py clip.mp4 --out out/clip     ← verified working
        ↓
you prompt local Claude: "cut the silences, caption it, stamp the R900"
        ↓
Claude drives CapCut via VectCutAPI
        ↓
CapCut opens — you look at it
        ↓
"move the caption up, it's behind the UI"        ← iterate by prompt
        ↓
export → Later.com → approve → post
```

**You can still edit by hand at any point.** That's the main reason CapCut beats a
render-only pipeline: when something takes Claude two minutes and you five seconds, do it
yourself. Ask Claude where to click.

---

## Files here

| File | What it does |
|---|---|
| **`CLAUDE.md`** | **The important one.** Brand, caption style, safe zones, trade vocabulary, the standard edit, when to stop and ask. Local Claude Code reads this automatically |
| `craftons-video-style.json` | Same rules, machine-readable, for tooling that wants values not prose |
| `transcribe.py` | Local transcription with word timings. Free, offline |

---

## Honest limits

- **Claude cannot watch the output.** It can cut, caption and place things from a transcript. It
  cannot tell you whether the result is any good. Your eye is the missing piece and no amount of
  tooling replaces it.
- **The draft format is undocumented and ByteDance can change it.** When CapCut updates, this can
  break. That's the accepted cost — it's why the bridge is a maintained third-party project
  rather than something written here.
- **Budget 8–15 hours to get the first few videos right.** The walkthrough's author says 20–30
  hours from scratch; using VectCutAPI and skipping the AI-footage half should cut that, but it
  is not an afternoon.
- **Do the first batch by hand anyway.** Learn what actually annoys you about the edit before
  automating it. Automating a process you haven't run is how the wrong thing gets built well.
