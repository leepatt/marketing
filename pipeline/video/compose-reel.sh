#!/usr/bin/env bash
# compose-reel.sh SCREEN_CUT.mp4 AVATAR_CUT.mp4 OUT.mp4 [caps.ass]
# 1080x1920 Reel: Craftons-green ground, browser screen recording (Chrome chrome + side panel cropped)
# full-width at y=100, 9:16 avatar PiP (330x587, rounded corners) bottom-right at (714,1073), optional ASS captions.
# Screen source assumed 902x1128 browser window; avatar source assumed 742x1320 (see jumpcut.py + crop=742:1320:249:600).
set -euo pipefail
S=$1; A=$2; O=$3; CAPS=${4:-}
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())" 2>/dev/null || echo ffmpeg)
HERE=$(cd "$(dirname "$0")" && pwd)
R=28; RR=$((R*R)); R1=$((R+1))
MASK="if(lt(X,$R)*lt(Y,$R)*gt(pow(X-$R,2)+pow(Y-$R,2),$RR)+lt(X,$R)*gt(Y,H-$R1)*gt(pow(X-$R,2)+pow(Y-(H-$R1),2),$RR)+gt(X,W-$R1)*lt(Y,$R)*gt(pow(X-(W-$R1),2)+pow(Y-$R,2),$RR)+gt(X,W-$R1)*gt(Y,H-$R1)*gt(pow(X-(W-$R1),2)+pow(Y-(H-$R1),2),$RR),0,255)"
FC="color=c=0x194431:s=1080x1920:r=30[bg];
[0:v]crop=848:976:0:152,scale=1080:1243:flags=lanczos[scr];
[1:v]scale=330:587,format=yuva420p,geq=lum='p(X,Y)':cb='p(X,Y)':cr='p(X,Y)':a='$MASK'[pip];
[bg][scr]overlay=0:100:shortest=1[a];
[a][pip]overlay=714:1073[v0]"
if [ -n "$CAPS" ]; then FC="$FC;[v0]ass=$CAPS:fontsdir=$HERE/fonts[v]"; else FC="$FC;[v0]null[v]"; fi
"$FF" -y -loglevel error -stats -i "$S" -i "$A" -filter_complex "$FC" -map "[v]" -map 1:a \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$O"
