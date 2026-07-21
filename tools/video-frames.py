#!/usr/bin/env python3
"""
video-frames.py — turn reel/screen-recording videos into a deduped set of
reference frames for the Craftons inspiration library.

Pulls one frame every 0.5s (default), then drops near-identical consecutive
frames with a perceptual hash so a 30s reel yields ~8-12 distinct structure
shots instead of 60 near-copies.

Usage:
    python3 tools/video-frames.py INPUT [-o OUTDIR] [--interval 0.5] [--threshold 6]

INPUT may be a single video file or a directory of videos
(.mp4 .mov .m4v .mkv .webm). Frames land in OUTDIR named
<video-stem>_t<seconds>.jpg.

Designed for the workflow: screen-record @account -> upload to Drive ->
this script extracts frames -> Claude reads the frames visually to write
image-gen prompt notes. Reference/mood use only (third-party content).
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG = "ffmpeg"  # fall back to a system ffmpeg on PATH

from PIL import Image
import imagehash

VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi"}


def extract_raw_frames(video: Path, tmp: Path, interval: float) -> list[Path]:
    """Grab one frame every `interval` seconds into tmp, return them in order."""
    fps = 1.0 / interval
    out_pattern = str(tmp / "f_%05d.jpg")
    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-i", str(video),
           "-vf", f"fps={fps}", "-q:v", "2", out_pattern]
    subprocess.run(cmd, check=True)
    return sorted(tmp.glob("f_*.jpg"))


def dedupe(frames: list[Path], threshold: int) -> list[Path]:
    """Keep a frame only if it differs from the last kept one by >= threshold
    (Hamming distance on a perceptual hash). Lower threshold = stricter = more
    frames kept; higher = fewer, more distinct frames."""
    kept, last_hash = [], None
    for f in frames:
        h = imagehash.phash(Image.open(f))
        if last_hash is None or (h - last_hash) >= threshold:
            kept.append(f)
            last_hash = h
    return kept


def process(video: Path, outdir: Path, interval: float, threshold: int) -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        raw = extract_raw_frames(video, tmp, interval)
        kept = dedupe(raw, threshold)
        outdir.mkdir(parents=True, exist_ok=True)
        for f in kept:
            idx = int(f.stem.split("_")[1]) - 1  # f_00001 -> 0
            seconds = idx * interval
            dest = outdir / f"{video.stem}_t{seconds:06.1f}.jpg"
            dest.write_bytes(f.read_bytes())
        print(f"  {video.name}: {len(raw)} raw -> {len(kept)} kept")
        return len(kept)


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract deduped reference frames from videos.")
    ap.add_argument("input", help="video file or directory of videos")
    ap.add_argument("-o", "--outdir", default="frames", help="output directory (default: ./frames)")
    ap.add_argument("--interval", type=float, default=0.5, help="seconds between frames (default 0.5)")
    ap.add_argument("--threshold", type=int, default=6,
                    help="perceptual-hash distance to treat frames as distinct (default 6)")
    args = ap.parse_args()

    src = Path(args.input)
    if src.is_dir():
        videos = sorted(p for p in src.iterdir() if p.suffix.lower() in VIDEO_EXTS)
    elif src.is_file():
        videos = [src]
    else:
        sys.exit(f"input not found: {src}")
    if not videos:
        sys.exit(f"no videos ({', '.join(sorted(VIDEO_EXTS))}) found in {src}")

    outdir = Path(args.outdir)
    print(f"ffmpeg: {FFMPEG}")
    print(f"{len(videos)} video(s) -> {outdir}/  (every {args.interval}s, dedupe threshold {args.threshold})")
    total = sum(process(v, outdir, args.interval, args.threshold) for v in videos)
    print(f"done: {total} reference frames in {outdir}/")


if __name__ == "__main__":
    main()
