#!/bin/sh
# ------------------------------------------------------------------
#  SD Core for Linux - local docs server
#  Serves the docs tree over http://localhost so a browser always loads
#  the current files from disk (avoids the browser's file:// cache quirks).
#  Ctrl-C stops the server.
#  Ported from SD Core for Windows's start-docs.cmd (same result: a local
#  server plus a browser tab), the mechanism Linux's own - no "start" or
#  "timeout", a background job and whichever browser opener exists.
# ------------------------------------------------------------------
cd "$(dirname "$0")" || exit 1

python3 -m http.server 8123 --bind 127.0.0.1 &
server_pid=$!
trap 'kill "$server_pid" 2>/dev/null' EXIT INT TERM

sleep 1

url="http://localhost:8123/index.html"
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$url" >/dev/null 2>&1
elif command -v open >/dev/null 2>&1; then
  open "$url" >/dev/null 2>&1
else
  echo "Open $url in a browser."
fi

wait "$server_pid"
