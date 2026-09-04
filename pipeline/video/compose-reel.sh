#!/usr/bin/env bash
# compose-reel.sh LAYOUT SCREEN_CUT.mp4 AVATAR_CUT.mp4 OUT.mp4 [caps.ass]
# LAYOUT:
#   white9x16  1080x1920, white ground (matches the app page), screen recording full-width at top,
#              9:16 avatar PiP bottom-left (36,1113). Captions: ink style, ML=400 MR=40 MV=340.
#   full4x5    1080x1350, screen recording at full viewport width (848 px, no side trim so wide pages like the
#              quote sheet are not clipped), white pad top/bottom, avatar PiP 300x533 bottom-left (30,787).
#              Captions: white style, centred, ML=40 MR=40 MV=70, PlayResY 1350.
# Env FREEZE: optional ffmpeg filter prefix for the screen input, e.g. "freezeframes=first=4044:last=4086:replace=4043,"
#              to hold a frame over a page-loading flash (find frames with signalstats YAVG).
#   green9x16  1080x1920, Craftons-green ground, screen at y=60, avatar PiP bottom-left. Captions as white9x16.
# Screen source: 902x1128 Chrome window (tab/address/bookmark bars + side panel cropped: crop=806:976:21:152).
# Avatar source: 742x1320 (jumpcut.py output + crop=742:1320:249:600 on the 1080x1920 phone clip).
set -euo pipefail
L=$1; S=$2; A=$3; O=$4; CAPS=${5:-}
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())" 2>/dev/null || echo ffmpeg)
HERE=$(cd "$(dirname "$0")" && pwd)
R=28; RR=$((R*R)); R1=$((R+1))
MASK="if(lt(X,$R)*lt(Y,$R)*gt(pow(X-$R,2)+pow(Y-$R,2),$RR)+lt(X,$R)*gt(Y,H-$R1)*gt(pow(X-$R,2)+pow(Y-(H-$R1),2),$RR)+gt(X,W-$R1)*lt(Y,$R)*gt(pow(X-(W-$R1),2)+pow(Y-$R,2),$RR)+gt(X,W-$R1)*gt(Y,H-$R1)*gt(pow(X-(W-$R1),2)+pow(Y-(H-$R1),2),$RR),0,255)"
PIP="format=yuva420p,geq=lum='p(X,Y)':cb='p(X,Y)':cr='p(X,Y)':a='$MASK'"
SCR="crop=806:976:21:152"
FREEZE=${FREEZE:-}
case "$L" in
  white9x16) FC="color=c=white:s=1080x1920:r=30[bg];[0:v]$SCR,scale=1080:1308:flags=lanczos[scr];[1:v]scale=330:587,$PIP[pip];[bg][scr]overlay=0:0:shortest=1[a];[a][pip]overlay=36:1113[v0]";;
  full4x5)   FC="[0:v]${FREEZE}crop=848:976:0:152,scale=1080:1243:flags=lanczos,pad=1080:1350:0:53:color=white,setsar=1[scr];[1:v]scale=300:533,$PIP[pip];[scr][pip]overlay=30:787[v0]";;
  green9x16) FC="color=c=0x194431:s=1080x1920:r=30[bg];[0:v]$SCR,scale=1080:1308:flags=lanczos[scr];[1:v]scale=330:587,$PIP[pip];[bg][scr]overlay=0:60:shortest=1[a];[a][pip]overlay=36:1113[v0]";;
  *) echo "unknown layout $L" >&2; exit 2;;
esac
if [ -n "$CAPS" ]; then FC="$FC;[v0]ass=$CAPS:fontsdir=$HERE/fonts[v]"; else FC="$FC;[v0]null[v]"; fi
"$FF" -y -loglevel error -stats -i "$S" -i "$A" -filter_complex "$FC" -map "[v]" -map 1:a \
  -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$O"
