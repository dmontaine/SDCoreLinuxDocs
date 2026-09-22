# sdprobe2.ps1 - run TWO SD sessions at once and measure what one does to the
# other.  Record locking, task locks and file locks cannot be measured from a
# single session: a lock you hold yourself answers a different question from a
# lock somebody else holds, and every RECORDLOCKED() code above zero is the
# self-answer.  This is the instrument for User document 14.
#
# USAGE
#     sdprobe2.ps1 -Holder <file> -Contender <file> [-Account don] [-TimeoutSec 150]
#
# THE TWO PROGRAMS RENDEZVOUS THROUGH A FILE, NOT THROUGH A SLEEP.  The holder
# takes its locks and writes a HOLDING record; the contender polls for it,
# measures, writes DONE; the holder sees DONE and releases.  Timing-based
# staggering was rejected because a slow compile or a busy box turns it into a
# measurement of nothing that still prints numbers.
#
# BOTH PROGRAMS ARE COMPILED IN A THIRD, EARLIER SESSION.  Compiling inside the
# timed pair would put a variable-length step inside the window being measured.
#
# ==== THE NULL-CASE GUARD IS THE WHOLE POINT OF THIS TOOL ====
# Two sessions that never overlapped produce exactly the numbers a reader would
# expect from a working test - RECORDLOCKED() 0, a lock granted, no contention
# anywhere - so "it printed values" is not evidence.  Five things must hold or
# the run is REFUSED:
#   1. both programs compiled with 0 errors;
#   2. both printed their own START and END markers;
#   3. both printed USERNO, and THE TWO USER NUMBERS DIFFER - one session
#      running twice would satisfy everything else;
#   4. the contender printed SAW.USERNO, and it EQUALS the holder's USERNO -
#      so the lock it met was that session's lock and not a leftover;
#   5. the contender printed at least one CONTENDED line - if nothing
#      conflicted, nothing was measured.
#
# The pipe shape is PROJECT_STATUS section 6's, as in sdprobe.ps1: a whole
# script ending in OFF, fed under Start-Job with a timeout, with a blank
# sacrificial first line to absorb the pipe's BOM.  PHANTOM is deliberately not
# used - a phantom child inherits the pipe and the job never completes.
param(
    [string]$Holder,
    [string]$Contender,
    [string]$Account = 'don',
    [int]$TimeoutSec = 150
)

$ErrorActionPreference = 'Stop'

$sdExe = Join-Path $env:ProgramFiles 'SD\usr\bin\sd.exe'
$bp    = Join-Path $env:ProgramData ('SD\user_accounts\' + $Account + '\bp')

Write-Output ('sd.exe    : ' + $sdExe)
Write-Output ('bp dir    : ' + $bp)
Write-Output ('holder    : ' + $Holder)
Write-Output ('contender : ' + $Contender)

if (-not (Test-Path -LiteralPath $sdExe))     { throw "no sd.exe at $sdExe" }
if (-not (Test-Path -LiteralPath $bp))        { throw "no bp directory at $bp" }
if (-not (Test-Path -LiteralPath $Holder))    { throw "no holder source at $Holder" }
if (-not (Test-Path -LiteralPath $Contender)) { throw "no contender source at $Contender" }

# NOTE: this function returns a value, so it must not Write-Output anything -
# PowerShell would join the message onto the return value and the caller would
# get a two element array where it expected a path.  The caller does the
# printing.
function Install-Probe([string]$src, [string]$name) {
    $dest = Join-Path $bp $name
    $text = [IO.File]::ReadAllText($src) -replace "`r`n", "`n"
    if ($text.Length -lt 200) { throw "$name source is only $($text.Length) bytes - refusing to run a probe that measures nothing" }
    [IO.File]::WriteAllText($dest, $text, (New-Object Text.UTF8Encoding $false))
    return $dest
}

$holdDest = Install-Probe $Holder    'ZZHOLD'
$contDest = Install-Probe $Contender 'ZZCONT'
Write-Output ('wrote     : ' + $holdDest + '  ' + (Get-Item -LiteralPath $holdDest).Length + ' bytes')
Write-Output ('wrote     : ' + $contDest + '  ' + (Get-Item -LiteralPath $contDest).Length + ' bytes')

function Invoke-SDScript([string[]]$commands) {
    $body = "`n" + ((@('TERM 200,9999') + $commands + @('OFF')) -join "`n") + "`n"
    $job = Start-Job -ScriptBlock { param($exe, $t) $t | & $exe } -ArgumentList $sdExe, $body
    return $job
}

function Get-JobText($job, [int]$timeout, [string]$label) {
    if (Wait-Job $job -Timeout $timeout) {
        $out = Receive-Job $job
    } else {
        Stop-Job $job
        $out = Receive-Job $job
        $out += "*** $label did not finish in $timeout s - it is waiting for input."
        $out += "*** Kill the sdwind PID or cycle.ps1 will refuse to start."
    }
    Remove-Job $job -Force
    $esc = [char]27
    return (($out -replace "$esc\[[0-9]*[A-Za-z]", '') | Out-String)
}

# ---- pass 1: compile both, in one session, before anything is timed --------
Write-Output ''
Write-Output '=== COMPILE ============================================================='
$cjob  = Invoke-SDScript @('BASIC BP ZZHOLD', 'BASIC BP ZZCONT')
$ctext = Get-JobText $cjob 60 'compile'
Write-Output $ctext
$clean = [regex]::Matches($ctext, '(?m)^\s*0 error\(s\)').Count
Write-Output ("  clean compiles : {0} (2 required)" -f $clean)

if ($clean -ne 2) {
    Write-Output '  REFUSED: both programs must compile with 0 errors before anything runs.'
    Remove-Item -LiteralPath $holdDest, $contDest -Force -ErrorAction SilentlyContinue
    exit 1
}

# ---- pass 2: the two sessions, started together ---------------------------
Write-Output ''
Write-Output '=== TWO SESSIONS ========================================================'
$hjob = Invoke-SDScript @('RUN BP ZZHOLD')
Start-Sleep -Milliseconds 1500     # the holder gets its locks first; the
                                   # contender polls for HOLDING anyway, so
                                   # this only shortens the poll, it is not
                                   # what makes the order right
$tjob = Invoke-SDScript @('RUN BP ZZCONT')

$htext = Get-JobText $hjob $TimeoutSec 'holder'
$ttext = Get-JobText $tjob $TimeoutSec 'contender'

Write-Output '--- HOLDER SAID ---------------------------------------------------------'
Write-Output $htext
Write-Output '--- CONTENDER SAID ------------------------------------------------------'
Write-Output $ttext

# ---- the guard ------------------------------------------------------------
function Get-Marked([string]$text, [string]$key) {
    $m = [regex]::Match($text, [regex]::Escape($key) + '=(-?\d+)')
    if ($m.Success) { return [int]$m.Groups[1].Value }
    return $null
}

$hStart = $htext -match 'ZZHOLD\.START'
$hEnd   = $htext -match 'ZZHOLD\.END'
$tStart = $ttext -match 'ZZCONT\.START'
$tEnd   = $ttext -match 'ZZCONT\.END'
$hUser  = Get-Marked $htext 'ZZHOLD.USERNO'
$tUser  = Get-Marked $ttext 'ZZCONT.USERNO'
$tSaw   = Get-Marked $ttext 'ZZCONT.SAW.USERNO'
$contended = ([regex]::Matches($ttext, 'CONTENDED')).Count

Write-Output '=== NULL-CASE GUARD ====================================================='
Write-Output ("  holder START / END       : {0} / {1}" -f $hStart, $hEnd)
Write-Output ("  contender START / END    : {0} / {1}" -f $tStart, $tEnd)
Write-Output ("  holder user number       : {0}" -f $hUser)
Write-Output ("  contender user number    : {0}" -f $tUser)
Write-Output ("  user numbers differ      : {0}" -f ($hUser -ne $null -and $tUser -ne $null -and $hUser -ne $tUser))
Write-Output ("  contender saw user       : {0}" -f $tSaw)
Write-Output ("  saw == holder            : {0}" -f ($tSaw -ne $null -and $tSaw -eq $hUser))
Write-Output ("  CONTENDED lines          : {0}" -f $contended)

$ok = $hStart -and $hEnd -and $tStart -and $tEnd `
      -and ($hUser -ne $null) -and ($tUser -ne $null) -and ($hUser -ne $tUser) `
      -and ($tSaw -ne $null) -and ($tSaw -eq $hUser) `
      -and ($contended -gt 0)

Remove-Item -LiteralPath $holdDest, $contDest -Force -ErrorAction SilentlyContinue

if (-not $ok) {
    Write-Output '  REFUSED: the two sessions did not demonstrably contend - the values above'
    Write-Output '           are not a measurement of two sessions.'
    exit 1
}
Write-Output '  two distinct sessions ran at once and one met the other''s locks.'
Write-Output ('  removed  : ' + $holdDest + ' , ' + $contDest)
exit 0
