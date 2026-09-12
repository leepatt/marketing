#!/usr/bin/env python3
"""
Turn a screen recording of Instagram reels into a transcript + frame grabs.

Built because Instagram is unreachable from the Claude session environment:
Firecrawl refuses the site (403), direct fetch 302s to login, the web profile
API 401s, headless Chromium gets ERR_CONNECTION_RESET, and the Meta token on
hand is a Conversions API system user without `instagram_basic`. A screen
recording routed through Drive is the working path.

Usage:
    python3 pipeline/transcribe-reels.py RECORDING.mp4 --out research/reels/jade
    python3 pipeline/transcribe-reels.py RECORDING.mp4 --out ... --model small

Outputs, under --out:
    transcript.md       timestamped transcript, split into segments
    transcript.json     same, machine-readable, for later analysis
    frames/*.jpg        one frame per detected segment (for on-screen text)

Requires (installed on demand, both pip-only, no apt needed):
    pip install faster-whisper imageio-ffmpeg
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SILENCE_DB = "-32dB"        # what counts as "quiet" between reels
SILENCE_MIN_SEC = 0.6       # a gap this long is treated as a reel boundary


def ffmpeg_exe() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def extract_audio(ff: str, video: Path, wav: Path) -> None:
    """16 kHz mono — what Whisper wants, and small on disk."""
    subprocess.run(
        [ff, "-i", str(video), "-vn", "-ar", "16000", "-ac", "1", "-y", str(wav)],
        check=True, capture_output=True,
    )


def find_boundaries(ff: str, wav: Path) -> list[float]:
    """Detect silences; their midpoints are where one reel likely ends."""
    proc = subprocess.run(
        [ff, "-i", str(wav), "-af",
         f"silencedetect=noise={SILENCE_DB}:d={SILENCE_MIN_SEC}", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    starts, ends = [], []
    for line in proc.stderr.splitlines():
        if "silence_start:" in line:
            starts.append(float(line.split("silence_start:")[1].strip()))
        elif "silence_end:" in line:
            ends.append(float(line.split("silence_end:")[1].split("|")[0].strip()))
    return [round((s + e) / 2, 2) for s, e in zip(starts, ends)]


def grab_frame(ff: str, video: Path, at: float, dest: Path) -> None:
    """One frame, for reading on-screen text and judging the visual style."""
    subprocess.run(
        [ff, "-ss", str(at), "-i", str(video), "-frames:v", "1",
         "-q:v", "3", "-y", str(dest)],
        check=True, capture_output=True,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="small",
                    help="tiny|base|small|medium|large-v3 (default small — good "
                         "accuracy/speed balance on CPU for trade vocabulary)")
    ap.add_argument("--no-frames", action="store_true")
    args = ap.parse_args()

    video = Path(args.video)
    if not video.exists():
        print(f"No such file: {video}", file=sys.stderr)
        return 1

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    frames_dir = out / "frames"

    ff = ffmpeg_exe()
    wav = out / "audio.wav"

    print("Extracting audio…")
    extract_audio(ff, video, wav)

    print("Finding reel boundaries…")
    boundaries = find_boundaries(ff, wav)
    print(f"  {len(boundaries)} candidate boundaries")

    print(f"Transcribing with faster-whisper '{args.model}' (CPU)…")
    from faster_whisper import WhisperModel
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(wav), vad_filter=True, language="en")

    # Group Whisper segments into reels, cutting at each detected boundary.
    reels: list[dict] = [{"index": 1, "start": 0.0, "lines": []}]
    nxt = 0
    for seg in segments:
        while nxt < len(boundaries) and seg.start > boundaries[nxt]:
            nxt += 1
            reels.append({"index": len(reels) + 1, "start": seg.start, "lines": []})
        reels[-1]["lines"].append(
            {"start": round(seg.start, 2), "end": round(seg.end, 2),
             "text": seg.text.strip()}
        )

    reels = [r for r in reels if r["lines"]]
    for r in reels:
        r["end"] = r["lines"][-1]["end"]
        r["text"] = " ".join(l["text"] for l in r["lines"])

    if not args.no_frames:
        print("Grabbing one frame per reel…")
        frames_dir.mkdir(exist_ok=True)
        for r in reels:
            # A second in, so the hook overlay is up but the cut has settled.
            dest = frames_dir / f"reel-{r['index']:02d}.jpg"
            try:
                grab_frame(ff, video, r["start"] + 1.0, dest)
                r["frame"] = str(dest.relative_to(out))
            except subprocess.CalledProcessError:
                pass

    (out / "transcript.json").write_text(
        json.dumps({"source": str(video), "language": info.language,
                    "model": args.model, "reels": reels}, indent=2)
    )

    def ts(s: float) -> str:
        return f"{int(s // 60):02d}:{int(s % 60):02d}"

    md = [f"# Reel transcripts — {video.name}", ""]
    md.append(f"_{len(reels)} segments · model `{args.model}` · language `{info.language}`_")
    md.append("")
    md.append("> Segments are split on silence gaps and **are not guaranteed to match reel")
    md.append("> boundaries exactly**. Check against the frame grabs before relying on the split.")
    md.append("")
    for r in reels:
        md.append(f"## Segment {r['index']}  ·  {ts(r['start'])}–{ts(r['end'])}")
        if r.get("frame"):
            md.append(f"![frame]({r['frame']})")
        md.append("")
        md.append(r["text"])
        md.append("")
    (out / "transcript.md").write_text("\n".join(md))

    wav.unlink(missing_ok=True)   # it's big and reproducible
    print(f"\nDone. {len(reels)} segments → {out}/transcript.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
