#!/usr/bin/env python3
"""
Transcribe a Craftons talking-head clip with word-level timings.

Produces everything the edit needs: word timings for caption cards, silence spans
for cutting, filler-word positions, and a flag on every trade term Whisper is
likely to have mangled.

    pip install faster-whisper imageio-ffmpeg
    python transcribe.py clip.mp4 --out out/clip

Outputs under --out:
    transcript.json   words + timings + silences + vocabulary flags (for the editor)
    transcript.md     readable, for Lee

Runs locally and offline. No API key, nothing uploaded.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
FILLERS = {"um", "uh", "erm", "ah", "like", "you know", "sort of", "kind of", "basically"}
MIN_SILENCE = 0.5   # matches editing.silenceThresholdSec in the style config


def load_style() -> dict:
    p = HERE / "craftons-video-style.json"
    return json.loads(p.read_text()) if p.exists() else {}


def ffmpeg_exe() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def extract_audio(ff: str, src: Path, wav: Path) -> None:
    subprocess.run(
        [ff, "-i", str(src), "-vn", "-ar", "16000", "-ac", "1", "-y", str(wav)],
        check=True, capture_output=True,
    )


def find_silences(words: list[dict], end: float) -> list[dict]:
    """Gaps between spoken words — the cut candidates."""
    spans, prev = [], 0.0
    for w in words:
        if w["start"] - prev >= MIN_SILENCE:
            spans.append({"start": round(prev, 2), "end": round(w["start"], 2),
                          "duration": round(w["start"] - prev, 2)})
        prev = max(prev, w["end"])
    if end - prev >= MIN_SILENCE:
        spans.append({"start": round(prev, 2), "end": round(end, 2),
                      "duration": round(end - prev, 2)})
    return spans


def _squash(s: str) -> tuple[str, list[int]]:
    """Lowercase, strip everything but letters/digits. Keep an index map back to the original."""
    out, idx = [], []
    for i, ch in enumerate(s):
        if ch.isalnum():
            out.append(ch.lower())
            idx.append(i)
    return "".join(out), idx


def flag_vocabulary(text: str, terms: list[str]) -> list[dict]:
    """
    Whisper's real failure on trade vocabulary is splitting or joining compounds —
    'formply' becomes 'form ply', 'Woodtron' becomes 'wood tron', 'set-out' becomes
    'set out'. Comparing on a squashed form (letters and digits only) catches all
    three, which a plain substring search does not.

    KNOWN GAP: purely phonetic errors slip through — 'architrave' heard as
    'arky trave' squashes to 'arkytrave' and won't match. Read the transcript;
    don't trust this to catch everything.
    """
    flags = []
    low = text.lower()
    squashed, idx_map = _squash(text)

    for term in terms:
        if term.lower() in low:
            flags.append({"term": term, "status": "present",
                          "action": "verify capitalisation"})
            continue

        sq_term, _ = _squash(term)
        pos = squashed.find(sq_term)
        if pos != -1:
            # present but written differently — the exact case this exists to catch
            start, end = idx_map[pos], idx_map[pos + len(sq_term) - 1] + 1
            flags.append({
                "term": term, "status": "MIS-TRANSCRIBED",
                "found": text[start:end],
                "action": f"Whisper wrote '{text[start:end]}' — correct to '{term}'",
            })

    # measurements are the highest-cost errors in this pipeline
    for m in re.finditer(r"\b\d+(?:\.\d+)?\s?(?:mm|cm|m|kg|deg|degrees?)\b", text, re.I):
        flags.append({"term": m.group(0), "status": "measurement",
                      "action": "CHECK AGAINST THE JOB — a misheard number is the worst error"})

    # sort so the things needing correction surface first
    order = {"MIS-TRANSCRIBED": 0, "measurement": 1, "present": 2}
    flags.sort(key=lambda f: order.get(f["status"], 3))
    return flags


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="small",
                    help="tiny|base|small|medium|large-v3 (default small; "
                         "use medium if the workshop is loud)")
    args = ap.parse_args()

    src = Path(args.video)
    if not src.exists():
        print(f"No such file: {src}", file=sys.stderr)
        return 1

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    style = load_style()

    ff = ffmpeg_exe()
    wav = out / "audio.wav"
    print("Extracting audio…")
    extract_audio(ff, src, wav)

    print(f"Transcribing with faster-whisper '{args.model}'…")
    from faster_whisper import WhisperModel
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        str(wav), word_timestamps=True, vad_filter=True, language="en"
    )

    words, sentences = [], []
    for seg in segments:
        sentences.append({"start": round(seg.start, 2), "end": round(seg.end, 2),
                          "text": seg.text.strip()})
        for w in (seg.words or []):
            words.append({"word": w.word.strip(), "start": round(w.start, 2),
                          "end": round(w.end, 2)})

    if not words:
        print("No speech detected. Check the audio track.", file=sys.stderr)
        return 1

    full = " ".join(s["text"] for s in sentences)
    duration = words[-1]["end"]
    silences = find_silences(words, duration)
    fillers = [w for w in words if w["word"].lower().strip(".,!?") in FILLERS]
    vocab = flag_vocabulary(full, style.get("vocabulary", {}).get("terms", []))

    payload = {
        "source": str(src),
        "model": args.model,
        "language": info.language,
        "durationSec": duration,
        "text": full,
        "sentences": sentences,
        "words": words,
        "silences": silences,
        "fillerWords": fillers,
        "vocabularyFlags": vocab,
        "hookWindow": {
            "$comment": "First 1.7s decides reach. This is what a viewer hears before deciding.",
            "text": " ".join(w["word"] for w in words if w["start"] < 1.7),
        },
    }
    (out / "transcript.json").write_text(json.dumps(payload, indent=2))

    cut = sum(s["duration"] for s in silences)
    md = [
        f"# Transcript — {src.name}", "",
        f"**{duration:.1f}s** · model `{args.model}` · {len(words)} words", "",
        f"- **{len(silences)} silences** over {MIN_SILENCE}s — **{cut:.1f}s** removable "
        f"({cut / duration * 100:.0f}% of the clip)",
        f"- **{len(fillers)} filler words**",
        f"- **{len(vocab)} vocabulary items to verify**", "",
        "## Hook — the first 1.7 seconds", "",
        f"> {payload['hookWindow']['text'] or '(silence — this is a problem)'}", "",
        "## Full transcript", "", full, "",
    ]
    if vocab:
        md += ["## Verify before export", ""]
        md += [f"- **{v['term']}** — {v['action']}" for v in vocab]
        md.append("")
    (out / "transcript.md").write_text("\n".join(md))

    wav.unlink(missing_ok=True)
    print(f"\n{duration:.1f}s · {cut:.1f}s of silence removable · "
          f"{len(vocab)} items to verify\n→ {out}/transcript.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
