#!/bin/bash
set -e

OUTPUT_FILE="${1:-before.mp4}"
DURATION="${2:-15}"

echo "=========================================="
echo " Starting Galaga recording session..."
echo " Output file: $OUTPUT_FILE"
echo " Duration:    $DURATION seconds"
echo " Controls:    Left/Right arrow to move, Space to fire, R to reset"
echo "=========================================="

python3 game.py &
GAME_PID=$!

# Wait for window to appear
WIN_ID=""
for i in {1..40}; do
    WIN_ID=$(xdotool search --onlyvisible --name "Galaga" | head -n 1 || true)
    if [ -n "$WIN_ID" ]; then
        break
    fi
    sleep 0.1
done

if [ -z "$WIN_ID" ]; then
    echo "ERROR: Galaga window not found!"
    kill $GAME_PID 2>/dev/null || true
    exit 1
fi

echo "Galaga window detected (ID: $WIN_ID). Activating window..."
xdotool windowactivate "$WIN_ID" 2>/dev/null || true

echo "Recording $DURATION seconds of gameplay..."
ffmpeg -y -f x11grab -window_id "$WIN_ID" -framerate 30 -i :0.0 -t "$DURATION" -c:v libx264 -pix_fmt yuv420p "$OUTPUT_FILE"

echo "Recording completed successfully: $OUTPUT_FILE"
kill $GAME_PID 2>/dev/null || true
wait $GAME_PID 2>/dev/null || true
echo "Session ended."
