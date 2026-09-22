@echo off
rem ------------------------------------------------------------------
rem  SD Core for Windows - local docs server
rem  Serves the docs tree over http://localhost so Chrome always loads
rem  the current files from disk (avoids Chrome's file:// cache quirks).
rem  Close the server window (titled below) to stop it.
rem ------------------------------------------------------------------
cd /d "%~dp0"
start "SD Core docs server - close this window to stop" cmd /k "python -m http.server 8123 --bind 127.0.0.1"
timeout /t 2 /nobreak >nul
start "" "http://localhost:8123/index.html"
