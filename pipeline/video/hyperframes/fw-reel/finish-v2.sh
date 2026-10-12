#!/usr/bin/env bash
set -euo pipefail
S=${REEL_WORK:-/tmp/claude-0/-home-user-marketing/11024340-908c-56ba-aa6d-76c2639c3272/scratchpad}
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
export HYPERFRAMES_FFMPEG_PATH=$S/hf/node_modules/@ffmpeg-installer/linux-x64/ffmpeg HYPERFRAMES_FFPROBE_PATH=$S/hf/node_modules/@ffprobe-installer/linux-x64/ffprobe FFMPEG=$S/hf/node_modules/@ffmpeg-installer/linux-x64/ffmpeg
cd $S/hf/fw-reel2
cp $S/take/cut/v2.mp4 assets/take.mp4
"$FFMPEG" -y -loglevel error -i assets/take.mp4 -vn -c:a aac -b:a 192k assets/vo.m4a
python3 ../make-v2.py $S/take/cut/v2.out-words.json . | tee make-v2.log
LEN=$(python3 -c "import json;print(json.loads(open('make-v2.log').readline())['demo_len'])")
python3 ../build-demo.py cues-v2.json assets/demo.mp4 --length "$LEN" --steps ../cap2/steps.json --frames ../cap2/frames 2>&1 | grep -v Fontconfig | grep -E "fit|wrote"
echo "=====CHECK====="; npx hyperframes check 2>&1 | grep -vE "^\[INFO\]|^\s*$" | grep -E "error|warn|⚠|✗|Check" | head -12
echo "=====RENDER====="; mkdir -p out && npx hyperframes render -o out/reel-nocaps.mp4 2>&1 | grep -vE "^\s*$|Render:trace|\[INFO\]" | tail -3
cp $S/take/cut/v2.caps.ass caps.ass
"$FFMPEG" -y -loglevel error -i out/reel-nocaps.mp4 -vf "ass=caps.ass:fontsdir=/home/user/marketing/pipeline/video/fonts" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a copy -movflags +faststart out/formwork-builder-reel-v2.mp4
"$FFMPEG" -y -loglevel error -i out/formwork-builder-reel-v2.mp4 -vf scale=540:960 -c:v libx264 -preset fast -crf 27 -c:a aac -b:a 96k -movflags +faststart out/formwork-builder-reel-v2-preview.mp4
ls -la out/
