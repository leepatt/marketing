# Desktop setup — step by step

**For Lee, on the Windows desktop.** Roughly 45–60 minutes if nothing fights you.

Work through it in order. **Each step has a checkpoint — don't move on until it passes.**
If a checkpoint fails, that's the thing to fix; carrying on makes it harder to find.

---

## Before you start

| Need | Check it | If missing |
|---|---|---|
| CapCut desktop | Open it once | capcut.com — get the **desktop** app, not mobile |
| Claude Code | `claude --version` | You said it's installed |
| Python 3.10+ | `python --version` | python.org — **tick "Add Python to PATH"** during install |
| Node | `node --version` | nodejs.org |
| Git | `git --version` | git-scm.com |

Open **Command Prompt** (not PowerShell — the activate command below differs).

---

## Step 1 — Get the repo

```cmd
cd %USERPROFILE%\Documents
git clone https://github.com/leepatt/marketing
cd marketing\pipeline\video-edit
```

If you already have it cloned elsewhere, just `cd` there and `git pull`.

**✅ Checkpoint:** `dir` shows `CLAUDE.md`, `transcribe.py`, `craftons-video-style.json`.

---

## Step 2 — Transcription

```cmd
pip install faster-whisper imageio-ffmpeg
```

**✅ Checkpoint:**

```cmd
python -c "import faster_whisper, imageio_ffmpeg; print('ok')"
```

Prints `ok`. First real transcription downloads a model (~500MB) — one time only.

---

## Step 3 — The CapCut bridge

```cmd
cd %USERPROFILE%\Documents\marketing\pipeline\video-edit
git clone https://github.com/sun-guannan/VectCutAPI
cd VectCutAPI

python -m venv venv-capcut
venv-capcut\Scripts\activate

pip install -r requirements.txt
pip install -r requirements-mcp.txt
```

Your prompt now shows `(venv-capcut)`. That means the virtual environment is active — packages
install into this folder rather than system-wide.

**✅ Checkpoint:** both installs finish without red errors.

---

## Step 4 — config.json ⚠️ THE ONE THAT BREAKS

```cmd
copy config.json.example config.json
notepad config.json
```

Find **`draft_profile`** and set it to match your CapCut:

| Your app | Value |
|---|---|
| **CapCut International (English)** | `capcut_legacy` |
| Jianying (Chinese) | `jianying_legacy` |
| Jianying Pro 10+ | `jianying_pro_10` |

**You almost certainly want `capcut_legacy`.**

> **If nothing else works later, come back here first.** A wrong `draft_profile` writes a draft
> CapCut cannot open, and the error you get won't point at this.

Also check whether the file has a draft-folder path. On Windows CapCut usually keeps drafts at:

```
C:\Users\<you>\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft
```

**Verify that folder actually exists** before trusting it — paths move between versions. Make a
throwaway project in CapCut and see where it lands if you're unsure.

**✅ Checkpoint:** `config.json` exists, `draft_profile` is set, and any path in it is real.

---

## Step 5 — Register the bridge with Claude Code

Point Claude at the **venv's** python, not system python, or it won't find the packages.

```cmd
cd %USERPROFILE%\Documents\marketing\pipeline\video-edit\VectCutAPI

claude mcp add --scope user --transport stdio capcut -- "%CD%\venv-capcut\Scripts\python.exe" "%CD%\mcp_server.py"
```

The `--` matters: everything after it is the server command, passed through untouched.

**✅ Checkpoint:**

```cmd
claude mcp list
```

Shows `capcut`. Start Claude Code, type `/mcp`, and confirm **✔ Connected**.

If it says failed: run that python path and script manually in the terminal and read the error.
Usually a missing dependency or a bad path.

---

## Step 6 — Motion graphics (Remotion)

This is what makes the spec stamp possible. **Verified working** — unlike the CapCut half, every
composition here has been rendered and checked.

```cmd
cd %USERPROFILE%\Documents\marketing\pipeline\video-edit\remotion
npm install
```

**✅ Checkpoint:**

```cmd
npm run still
```

`out\spec-stamp.png` appears, showing **R900** in the Craftons green with the specs beneath.
Open it — the type should be tall and condensed, not a generic sans. If it looks generic, the
fonts in `public\fonts` didn't load; say so rather than shipping off-brand video.

Render one with alpha:

```cmd
npm run spec
```

`out\spec-stamp.mov` is a transparent overlay you drop on a track **above** your footage in
CapCut.

**For a real job**, pass the actual numbers:

```cmd
npx remotion render SpecStamp out/job.mov --codec=prores --prores-profile=4444 --pixel-format=yuva444p10le --props="{\"radius\":\"R1450\",\"specs\":[\"3600mm\",\"19mm bendy ply\"]}"
```

> ⚠️ **`--pixel-format=yuva444p10le` is not optional.** Without it the file renders with no alpha
> and the overlay shows up in CapCut as a **solid black box**. The npm scripts include it.

`npm run studio` opens a live preview if you want to see changes as you make them.

---

## Step 7 — Smoke test ⚠️ DO THIS BEFORE ANY REAL VIDEO

**Close CapCut completely first.** The bridge writes project files on disk; CapCut can overwrite
them if it's holding the folder open.

Start Claude Code in the `video-edit` folder and ask:

> Create an empty CapCut draft called `smoke-test` using the capcut MCP server, then save it.

Then open CapCut and look for a `smoke-test` project.

**✅ Checkpoint: the project exists and opens without error.**

**This is the real go/no-go.** If it works, the hard part is done. If it doesn't:
1. `draft_profile` in Step 4 — most likely
2. The draft folder path — is it the one CapCut actually uses?
3. VectCutAPI's GitHub issues — the format may have drifted with a CapCut update

Don't debug past this on your own for long. Bring me the error.

---

## Step 8 — First real clip

Get one of Jake's clips onto the desktop, then:

```cmd
cd %USERPROFILE%\Documents\marketing\pipeline\video-edit
python transcribe.py "C:\path\to\jake-clip.mp4" --out out\clip01
```

Read `out\clip01\transcript.md` — check the **Verify before export** section. It flags where
Whisper split trade words ("form ply" for `formply`) and every measurement. **Fix any wrong
numbers now.** A misheard radius is the worst thing this pipeline can produce.

Then prompt Claude Code:

> Read CLAUDE.md. Using out/clip01/transcript.json, create a CapCut draft: cut the silences and
> filler words, add captions in the Craftons style, keep them out of the bottom unsafe band.
> Don't export — I'll look at it in CapCut first.

**✅ Checkpoint:** a CapCut project you can open, with cuts and captions roughly right.

Then iterate by prompt: *"captions are too low, move them up"*, *"that cut at 12s is too tight"*.

---

## Working rules

- **Close CapCut before Claude writes to a draft.** Reopen to look. It's clunky and it's normal.
- **Some things are faster by hand.** If it takes Claude two minutes and you five seconds, do it
  yourself — ask Claude where to click.
- **Claude can't see the output.** It cuts and places from the transcript. It cannot tell you
  whether the result is good. That's your job and it doesn't get automated.
- **Nothing publishes itself.** Export, look, approve, then Later.com.

---

## Expect friction

The CapCut half of this has **never been run** — it was written without a CapCut install to test
against. The transcription half is verified.

Budget **8–15 hours across the first few videos**, not one afternoon. The walkthrough author says
20–30 hours from scratch; using VectCutAPI and dropping the AI-footage half should cut that, but
it's not a quick job.

**Do your first batch by hand in CapCut anyway.** You'll learn what actually annoys you about the
edit — and that's what tells you what's worth automating.
