#!/bin/bash
#
# mkpdf.sh - render mkdoc.py's HTML pages to PDF with headless Chrome.
#
# usage: mkpdf.sh -in <dir-or-file> [-out <dir>] [-timeout <seconds>]
#
# Linux port of the Windows docs repo's tools/mkpdf.ps1, same technique:
# headless Chrome's own --print-to-pdf, not a PDF library, so the PDF cannot
# drift from what a reader's browser shows - mkdoc.py's page IS the PDF
# source, print stylesheet and all.  22 Sep 2026.
#
# WHY NO PDF STILL SHIPS.  Same reasoning as the Windows port's: the
# no-binaries rule (this project's own CLAUDE.md) forbids tracking one, and
# start-docs.sh already serves the HTML a browser can print from directly.
# This script writes PDFs outside the repository's tracked paths (they are
# gitignored, same as the HTML) for whoever wants a delivered copy.
#
# WHY CHROME AND NOT A PDF LIBRARY.  Same argument as the Windows script's:
# wkhtmltopdf and weasyprint are each a new dependency; pandoc was already
# rejected there for being a binary dependency.  Chrome/Chromium take the
# identical --headless=new --print-to-pdf switches on both platforms, so the
# only real port is which binary name to look for.
#
# WHERE THIS DIVERGES FROM WINDOWS, AND WHY.  There is no single browser every
# supported Linux distribution ships the way every Windows machine ships Edge
# - Chrome, Chromium and Edge-for-Linux are all real possibilities and none is
# guaranteed.  So "no browser found" is a real, expected outcome here in a way
# it never is on Windows, and this script says so in words rather than
# treating it as a bug to route around.

set -u

in_path=""
out_dir=""
timeout_sec=90

usage() {
    echo "usage: mkpdf.sh -in <dir-or-file> [-out <dir>] [-timeout <seconds>]" 1>&2
    exit 2
}

while [ $# -gt 0 ]; do
    case "$1" in
        -in) in_path=$2; shift 2 ;;
        -out) out_dir=$2; shift 2 ;;
        -timeout) timeout_sec=$2; shift 2 ;;
        *) usage ;;
    esac
done
[ -n "$in_path" ] || usage

say() { echo "mkpdf: $1"; }

# --- find a browser --------------------------------------------------------
# Order is a judgement call, not a fact the way Edge-then-Chrome is on
# Windows: prefer a real Chrome/Chromium build (matches what mkdoc.py's CSS
# was tuned against) over Edge-for-Linux, which is rarer.
browser=""
for candidate in google-chrome google-chrome-stable chromium chromium-browser microsoft-edge microsoft-edge-stable; do
    if command -v "$candidate" >/dev/null 2>&1; then
        browser=$(command -v "$candidate")
        break
    fi
done
if [ -z "$browser" ]; then
    echo "mkpdf: no Chrome, Chromium or Edge found on this machine." 1>&2
    echo "mkpdf: looked for: google-chrome google-chrome-stable chromium chromium-browser microsoft-edge microsoft-edge-stable" 1>&2
    exit 1
fi

# --- resolve the inputs -----------------------------------------------------
if [ ! -e "$in_path" ]; then
    echo "mkpdf: no such path: $in_path" 1>&2
    exit 1
fi

sources=()
if [ -d "$in_path" ]; then
    while IFS= read -r -d '' f; do sources+=("$f"); done \
        < <(find "$in_path" -maxdepth 1 -name '*.html' -print0 | sort -z)
    [ -n "$out_dir" ] || out_dir=$(cd "$in_path" && pwd)
else
    sources=("$in_path")
    [ -n "$out_dir" ] || out_dir=$(cd "$(dirname "$in_path")" && pwd)
fi

mkdir -p "$out_dir"
out_dir=$(cd "$out_dir" && pwd)

# AN INSTRUMENT PRINTS WHAT IT DID (CLAUDE.md).  The resolved paths and the
# count matter: -in pointed at a directory with no .html renders nothing, and
# a converter that cheerfully writes nothing is the "passes because it did
# nothing" failure - refused out loud, below.
say "browser $browser"
say "in      $(cd "$(dirname "$in_path")" 2>/dev/null && pwd)/$(basename "$in_path")"
say "out     $out_dir"
say "sources ${#sources[@]}"

if [ "${#sources[@]}" -eq 0 ]; then
    echo "mkpdf: no .html files found - nothing rendered." 1>&2
    exit 1
fi

# --- print -------------------------------------------------------------
made=0
failed=()
for s in "${sources[@]}"; do
    base=$(basename "$s")
    pdf="$out_dir/${base%.html}.pdf"
    before=0
    [ -f "$pdf" ] && before=$(stat -c%s "$pdf" 2>/dev/null || echo 0)

    # A dedicated profile directory keeps this from touching, or being
    # blocked by, the user's own running browser.
    profile=$(mktemp -d "${TMPDIR:-/tmp}/mkpdf-XXXXXXXX")

    echo "  [run] $(basename "$browser") --headless=new --disable-gpu --no-first-run --no-default-browser-check --user-data-dir=$profile --no-pdf-header-footer --print-to-pdf=$pdf $s"

    timeout "${timeout_sec}s" "$browser" \
        --headless=new \
        --disable-gpu \
        --no-first-run \
        --no-default-browser-check \
        --user-data-dir="$profile" \
        --no-pdf-header-footer \
        --print-to-pdf="$pdf" \
        "$s" >/dev/null 2>&1
    status=$?
    rm -rf "$profile"

    if [ "$status" -eq 124 ]; then
        failed+=("$base (timed out after ${timeout_sec}s)")
        continue
    fi
    if [ ! -f "$pdf" ]; then
        failed+=("$base (browser exited $status, no PDF written)")
        continue
    fi
    # BEFORE AND AFTER, NOT JUST A CONCLUSION.  "the file exists" would also
    # be true of a stale PDF from an earlier run this one failed to replace.
    after=$(stat -c%s "$pdf" 2>/dev/null || echo 0)
    if [ "$after" -lt 1000 ]; then
        failed+=("$base (PDF is only $after bytes - almost certainly empty)")
        continue
    fi
    echo "  [ok]  $base -> $(basename "$pdf")  $before -> $after bytes"
    made=$((made + 1))
done

echo
say "$made of ${#sources[@]} page(s) written."
if [ "${#failed[@]}" -gt 0 ]; then
    for f in "${failed[@]}"; do echo "  [FAIL] $f"; done
    exit 1
fi
exit 0
