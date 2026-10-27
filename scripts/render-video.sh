#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
node scripts/render-video-frames.cjs
ffmpeg -y -framerate 1/9 -start_number 1 -i video/frames/frame-%03d.png -t 45 -r 15 -c:v libx264 -preset medium -crf 24 -pix_fmt yuv420p -movflags +faststart video/demo.mp4
cp video/frames/frame-001.png video/poster.png
