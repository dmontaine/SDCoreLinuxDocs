<#
    release.ps1 - render what has changed, prove nothing is stale, and zip the
    deliverable with a checksum.

    command line:
        tools\release.ps1 [-Set GettingStarted] [-Version W1.0-0] [-OutDir <dir>]
                          [-Force] [-NoZip]

    WHY THIS EXISTS, and it is not the ten minutes it saves.  Moving the
    documentation into its own repository gave up the only automatic check
    that a page still matched the product (assert-current never sees it now).
    Zipping by hand adds a SECOND way to drift: shipping a PDF that was
    rendered before the last Markdown fix.  Nothing would catch it, and it
    looks exactly like a correct release.  So the staleness test below is the
    point of the script and the zip is the convenience.

    WHAT IT RENDERS.  Only what changed - owner's ruling, 26 Aug 2026,
    question 16.  A page is rendered when its .html or .pdf is missing or
    older than the .md beside it.  -Force renders everything.

    IT REFUSES RATHER THAN SHIPPING A DOUBT.  No .md found, a generated file
    with no source, or any .pdf still older than its .md after the render, and
    it stops with a non-zero exit.  A release step that passes because it did
    nothing is the failure this is shaped to avoid.
#>

[CmdletBinding()]
param(
    [string]$Set     = 'GettingStarted',
    [string]$Version = 'W1.0-0',
    [string]$OutDir,
    [switch]$Force,
    [switch]$NoZip
)

$ErrorActionPreference = 'Stop'

function Say($m) { Write-Output ("release: " + $m) }

# --- resolve everything, and say what was resolved -------------------------
$tools = $PSScriptRoot
$root  = Split-Path -Parent $tools
$setDir = Join-Path $root $Set
$mdDir   = Join-Path $setDir 'markdown'
$htmlDir = Join-Path $setDir 'html'
$pdfDir  = Join-Path $setDir 'pdf'
if (-not $OutDir) { $OutDir = $root }

Say ("repository  " + $root)
Say ("set         " + $Set + "   version " + $Version)
Say ("markdown    " + $mdDir)
Say ("html        " + $htmlDir)
Say ("pdf         " + $pdfDir)

# 06 Sep 26 - THE SOURCE MUST EXIST; THE GENERATED DIRECTORIES GET CREATED.
# PRE_RELEASE_FIXES 179.
#
# This loop tested all three the same way and refused on any one of them, so
# A FRESH CLONE COULD NOT RENDER AT ALL: .gitignore tracks only markdown\, and
# neither html\ nor pdf\ comes with the repository.  Measured 6 Sep 2026 on a
# second machine - "no such directory: ...\GettingStarted\html", exit 1, with
# nothing rendered.
#
# NOBODY MET IT BECAUSE THE MACHINE THE DOCUMENTATION WAS WRITTEN ON HAD BOTH
# DIRECTORIES LEFT OVER from earlier renders.  That is the same shape as
# PRE_RELEASE 173 and 177 in the other repository: a state the development box
# had accumulated, hiding a gap from every run made on it.
#
# It was also inconsistent with the tool this script drives - mkpdf.ps1 creates
# its own -Out directory with New-Item -Force and always has.
if (-not (Test-Path -LiteralPath $mdDir)) {
    Write-Error ("no such directory: " + $mdDir)
}
foreach ($d in @($htmlDir, $pdfDir)) {
    if (-not (Test-Path -LiteralPath $d)) {
        Say ("creating    " + $d + "   (generated, not in the repository)")
        $null = New-Item -ItemType Directory -Path $d -Force
    }
}

$sources = @(Get-ChildItem -LiteralPath $mdDir -Filter '*.md' | Sort-Object Name)
Say ("sources     " + $sources.Count + " markdown page(s)")
if ($sources.Count -eq 0) {
    Write-Error "no .md files - refusing to report a release"
}

# --- a generated file with no source is a renumbering left half-done -------
#
# THE SET INDEX IS THE ONE LEGITIMATE EXCEPTION, and it is exempt by name
# rather than by pattern.  html\index.html is written by tools\add_nav.py from
# the set's page list, not rendered from a Markdown file, so it has no source
# and never will.
#
# It is recorded here because this script REFUSED THE WHOLE TREE over it during
# the W1.0-0 audit.  release.ps1 was written before the set indexes existed, so
# the first release run after they were added could not complete - two halves of
# one toolchain, each correct, that had never been run together.  A pattern
# exemption would have hidden the next real orphan; a named one cannot.
$exemptStems = @('index')
$stems = @($sources | ForEach-Object { [IO.Path]::GetFileNameWithoutExtension($_.Name) })
$orphans = @()
$generated = @(Get-ChildItem -LiteralPath $htmlDir -Filter '*.html') +
             @(Get-ChildItem -LiteralPath $pdfDir  -Filter '*.pdf')
foreach ($g in $generated) {
    $stem = [IO.Path]::GetFileNameWithoutExtension($g.Name)
    if ($exemptStems -contains $stem) { continue }
    if ($stems -notcontains $stem) { $orphans += $g.FullName }
}
if ($orphans.Count -gt 0) {
    Say "GENERATED FILES WITH NO MARKDOWN SOURCE:"
    $orphans | ForEach-Object { Say ("    " + $_) }
    Write-Error ("" + $orphans.Count + " orphan(s) - delete them or restore the source, then run again")
}

# --- DOES THIS DOCUMENTATION STILL MATCH THE PRODUCT? ----------------------
#
# PRE_RELEASE 55, wired in 5 September 2026 on the owner's ruling.  Until now
# this script rendered, printed, navigated and link-checked, and NOTHING in
# either repository automatically asked whether the pages still describe the
# product.  These four do: each computes a roster from sd4windows and exits
# non-zero when the typed lists in this repository disagree.
#
# ***IT IS NOT HYPOTHETICAL.***  tclmap.py sat red from 30 Aug 2026 until the
# W1.0-0 audit found it - a verb was added in sd4windows and the checker lives
# HERE, where no check in that repository runs it.  Entry 80's own conclusion
# was "the answer was more checkers, not more diligence", and then the wiring
# was left out.  Measured 5 Sep 2026: all four together cost 3.6 s.
#
# ***scriptmap.py IS DELIBERATELY NOT ONE OF THEM.  OWNER, 5 September 2026:
# "wire in the four only - documentation may not be updated on the same cycle
# as the project."***  It reads the INSTALLED tree at C:\Program Files\SD
# rather than the source, by design - entry 80's rule is that every claim is
# checked against what a user actually receives.  Requiring one here would tie
# a documentation release to the product's install cycle, and the two are
# deliberately separate.  Measured: with no install it exits 1 on
# "scriptmap: no install at ...", which would have failed releases for a reason
# that is nothing to do with the documentation.  Run it by hand when there is a
# current install; the line below says so rather than letting it be forgotten.
#
# THEY READ THE SIBLING TREE, which is the layout setup-devbox.ps1 builds.  A
# missing sibling REFUSES rather than skipping: this script's whole purpose is
# to stop a doubtful release, and "the checks did not run" is a doubt.
$sd64 = Join-Path (Split-Path -Parent $root) 'sd4windows\sdb_ai\sd64'
if (-not (Test-Path -LiteralPath $sd64)) {
    Write-Error ("no sd4windows beside this repository at " + $sd64 +
                 " - the roster checks cannot run, and a release is not made without them")
}

$rosterChecks = @(
    @{ Name = 'docmap';     Script = 'docmap.py';     Arg = (Join-Path $sd64 'sdsys\gpl.bp\BCOMP') }
    @{ Name = 'tclmap';     Script = 'tclmap.py';     Arg = (Join-Path $sd64 'sdsys\newvoc') }
    @{ Name = 'confmap';    Script = 'confmap.py';    Arg = $sd64 }
    @{ Name = 'verbcounts'; Script = 'verbcounts.py'; Arg = (Join-Path $sd64 'sdsys\newvoc') }
)

Say ("rosters     " + $rosterChecks.Count + " check(s) against " + $sd64)
$rosterBad = @()
foreach ($c in $rosterChecks) {
    # A native exe on stderr terminates the script under ErrorActionPreference
    # Stop, so the exit code is read explicitly - the same reason mkdoc.py is
    # invoked the way it is below.
    $out = & python (Join-Path $tools $c.Script) $c.Arg 2>&1
    if ($LASTEXITCODE -ne 0) {
        $rosterBad += $c.Name
        Say ("  " + $c.Name + " REFUSED (exit " + $LASTEXITCODE + '):')
        $out | ForEach-Object { Say ("    " + $_) }
    } else {
        Say ("  " + $c.Name.PadRight(11) + " ok")
    }
}
if ($rosterBad.Count -gt 0) {
    Write-Error ("" + $rosterBad.Count + " roster check(s) refused - " +
                 ($rosterBad -join ', ') + ". Nothing was rendered and no zip was written")
}
Say '  scriptmap   not run here - it needs a current install; run it by hand:'
Say ('              python ' + (Join-Path $tools 'scriptmap.py') + ' "C:\Program Files\SD"')

# --- what needs rendering --------------------------------------------------
function Needs($generated, $source) {
    if (-not (Test-Path -LiteralPath $generated)) { return $true }
    return ((Get-Item -LiteralPath $generated).LastWriteTimeUtc -lt $source.LastWriteTimeUtc)
}

$toHtml = @()
foreach ($s in $sources) {
    $stem = [IO.Path]::GetFileNameWithoutExtension($s.Name)
    if ($Force -or (Needs (Join-Path $htmlDir ($stem + '.html')) $s)) { $toHtml += $s }
}

Say ("to render   " + $toHtml.Count + " of " + $sources.Count + " page(s) to HTML" +
     $(if ($Force) { "   (-Force)" } else { "" }))

if ($toHtml.Count -gt 0) {
    # A native exe writing to stderr terminates the script under
    # ErrorActionPreference Stop, so the exit code is read explicitly.
    # NOT $args.  That is a PowerShell automatic variable: naming a parameter
    # or a local $args gets it clobbered, and the command runs with nothing
    # after it.  This project has paid for that once already.
    $mkdoc = Join-Path $tools 'mkdoc.py'
    $mkdocArgs = @('--in') + @($toHtml | ForEach-Object { $_.FullName }) +
                 @('--out', $htmlDir, '--product', 'SD Core for Windows',
                   '--version', $Version)
    Say ("python " + $mkdoc + " " + ($mkdocArgs -join ' '))
    if ($mkdocArgs.Count -lt 5) { Write-Error 'mkdoc argument list is too short to be right' }
    & python $mkdoc @mkdocArgs 2>&1 | ForEach-Object { Write-Output ("  " + $_) }
    if ($LASTEXITCODE -ne 0) { Write-Error ("mkdoc.py exited " + $LASTEXITCODE) }
}

# THE PDF IS COMPARED AGAINST THE MARKDOWN, NOT AGAINST THE HTML, and README.md
# already said so about the hand check while this script did the opposite:
# "Re-rendering the HTML touches every file's mtime, so comparing those two
# reports the whole set as stale and tells you nothing."
#
# IT WAS WORSE THAN WASTEFUL HERE, because add_nav.py runs at the END of this
# script and rewrites every HTML file to insert the prev/next bars.  So the HTML
# was ALWAYS newer than the PDF by the time the next release looked, every run
# re-printed all 83 pages, and - the part that matters - each of those reprints
# was taken from HTML THAT ALREADY HAD THE NAV BARS IN IT.  The bars stayed out
# of the PDFs only because mkdoc.py's stylesheet hides .pagenav in @media print.
# That rule is the belt; this is the braces it was supposed to be backing up.
$toPdf = @()
foreach ($s in $sources) {
    $stem = [IO.Path]::GetFileNameWithoutExtension($s.Name)
    $html = Join-Path $htmlDir ($stem + '.html')
    if (-not (Test-Path -LiteralPath $html)) { Write-Error ("no HTML for " + $s.Name) }
    if ($Force -or (Needs (Join-Path $pdfDir ($stem + '.pdf')) $s)) {
        $toPdf += $html
    }
}

Say ("to print    " + $toPdf.Count + " of " + $sources.Count + " page(s) to PDF")

foreach ($html in $toPdf) {
    & (Join-Path $tools 'mkpdf.ps1') -In $html -Out $pdfDir | ForEach-Object { Write-Output ("  " + $_) }
}

# --- THE CHECK THIS SCRIPT EXISTS FOR --------------------------------------
# Every deliverable must be newer than the source it was made from.  This runs
# whether or not anything was rendered, so a run that rendered nothing still
# has to prove the set is current.
$stale = @()
foreach ($s in $sources) {
    $stem = [IO.Path]::GetFileNameWithoutExtension($s.Name)
    foreach ($ext in @('html', 'pdf')) {
        $g = Join-Path (Join-Path $setDir $ext) ($stem + '.' + $ext)
        if (-not (Test-Path -LiteralPath $g)) { $stale += ($stem + '.' + $ext + '  MISSING'); continue }
        $gi = Get-Item -LiteralPath $g
        if ($gi.LastWriteTimeUtc -lt $s.LastWriteTimeUtc) {
            $stale += ($stem + '.' + $ext + '  ' + $gi.LastWriteTimeUtc.ToString('s') +
                       '  older than  ' + $s.LastWriteTimeUtc.ToString('s'))
        }
    }
}

if ($stale.Count -gt 0) {
    Say "STALE OR MISSING DELIVERABLES:"
    $stale | ForEach-Object { Say ("    " + $_) }
    Write-Error ("" + $stale.Count + " stale - the zip was NOT written")
}
Say ("current     all " + $sources.Count + " page(s): html and pdf both newer than their markdown")

# --- NAVIGATION, WHICH IS HTML-ONLY AND MUST RUN AFTER THE PDFs -----------
#
# add_nav.py inserts the prev/next bar into every rendered page and writes the
# set index.  IT IS DELIBERATELY AFTER mkpdf: a "Next page" link pointing at an
# .html file is meaningless inside a PDF, so the PDFs are printed from the
# pages before the bar goes in.
#
# IT WAS NOT WIRED IN AT ALL UNTIL THE W1.0-0 AUDIT.  add_nav.py arrived with
# the second author's work and release.ps1 predates it, so navigation existed
# only when somebody remembered to run the script by hand - and a -Force render
# silently removed it again.  Two correct halves of one toolchain that had
# never been run in sequence.
#
# It works on every set at once rather than the one being released, which is
# harmless: it is idempotent and takes under a second.
$nav = Join-Path $tools 'add_nav.py'
if (Test-Path -LiteralPath $nav) {
    & python $nav 2>&1 | ForEach-Object { Write-Output ("  " + $_) }
    if ($LASTEXITCODE -ne 0) { Write-Error "add_nav.py failed - the zip was NOT written" }
}

# --- AND EVERY CROSS-PAGE LINK LANDS SOMEWHERE ----------------------------
# The markdown alone can only prove a page exists.  An anchor is generated by
# the renderer's own slugify - "OS.EXECUTE" becomes "osexecute", not
# "os-execute" - so a "#..." link can only be checked against the rendered
# pages.  One wrong anchor was written on 26 Aug 2026 and shipped past a
# markdown-side check that had no way to see it.
$check = Join-Path $tools 'checklinks.py'
& python $check $mdDir $htmlDir 2>&1 | ForEach-Object { Write-Output ("  " + $_) }
if ($LASTEXITCODE -ne 0) {
    Write-Error "broken link(s) - the zip was NOT written"
}

# --- THE BOUND SET: one PDF, page numbers, and a bookmark tree -------------
# Owner's ruling, 6 Sep 2026: "merge per set".  The release ships PDF only, and
# 86 separate PDFs is not a document - no continuous numbering, no outline, no
# search across a set, and 53 files to keep for the User guide alone.
#
# IT GOES IN ITS OWN DIRECTORY, AND THAT IS NOT TIDINESS.  The orphan check at
# the top of this script refuses any .pdf in pdf\ whose stem is not a markdown
# source, so a merged book dropped in beside the per-page PDFs would be
# reported as an orphan and refuse the whole set - the same way html\index.html
# had to be exempted by name during the W1.0-0 audit.  book\ sidesteps both
# that check and the staleness walk, which are per-page by design.
#
# AFTER add_nav ON PURPOSE.  mkbook.py strips the prev/next bars either way,
# but running last means the book is assembled from exactly the HTML that
# shipped, rather than from an intermediate state.
$bookDir = Join-Path $setDir 'book'
if (-not (Test-Path -LiteralPath $bookDir)) {
    Say ("creating    " + $bookDir + "   (generated, not in the repository)")
    $null = New-Item -ItemType Directory -Path $bookDir -Force
}
$bookHtml = Join-Path $bookDir ($Set + '.html')
$bookPdf  = Join-Path $bookDir ("SD-Core-for-Windows-" + $Version + "-" + $Set + ".pdf")

$mkbook = Join-Path $tools 'mkbook.py'
Say ("python " + $mkbook + " --set " + $Set)
& python $mkbook --set $Set --out $bookHtml --product 'SD Core for Windows' `
                 --version $Version 2>&1 | ForEach-Object { Write-Output ("  " + $_) }
if ($LASTEXITCODE -ne 0) { Write-Error "mkbook.py failed - the zip was NOT written" }

& (Join-Path $tools 'mkbookpdf.ps1') -In $bookHtml -Out $bookPdf `
    -FooterText ('SD Core for Windows ' + $Version) |
    ForEach-Object { Write-Output ("  " + $_) }

# VERIFY, DO NOT ASSUME - and do not rest it on the exit code alone.  A script
# invoked with "&" reports through $LASTEXITCODE, which is easy to read from
# the wrong statement; the file either exists at a plausible size or it does
# not.  PROJECT_STATUS.md records an exit code being trusted here before.
if (-not (Test-Path -LiteralPath $bookPdf)) {
    Write-Error "the bound $Set PDF was not written - the zip was NOT written"
}
$bookInfo = Get-Item -LiteralPath $bookPdf
Say ("book        " + $bookPdf)
Say ("book bytes  " + $bookInfo.Length)
if ($bookInfo.Length -lt 20000) {
    Write-Error "the bound $Set PDF is too small to be the set - the zip was NOT written"
}

if ($NoZip) { Say 'no zip written (-NoZip)'; exit 0 }

# --- the deliverable -------------------------------------------------------
$zip = Join-Path $OutDir ("SD-Core-for-Windows-" + $Version + "-" + $Set + "-docs.zip")
if (Test-Path -LiteralPath $zip) { Remove-Item -LiteralPath $zip -Force }

Compress-Archive -Path @($pdfDir, $htmlDir, $bookDir) -DestinationPath $zip
$item = Get-Item -LiteralPath $zip
$sha  = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash

Say ("zip         " + $item.FullName)
Say ("size        " + $item.Length + " bytes")
Say ("sha256      " + $sha)
Say ("contents    " + $sources.Count + " page(s), html and pdf, plus the bound set")
exit 0
