# sdtcl.ps1 - run TCL commands in a real SD session and print what came back.
# This is how the measured listings in the SD TCL document set were produced:
# type the claim as a command, run it, and quote what SD said.
#
# USAGE
#     sdtcl.ps1 -Commands 'list voc sample 3','count voc'
#     sdtcl.ps1 -File commands.txt [-Account don] [-TimeoutSec 90] [-Raw]
#
# WHY IT EXISTS.  sdprobe.ps1 runs a BASIC probe; there was nothing for a TCL
# command, and the TCL pages need their examples run before they are written
# down.
#
# WHY 'don' AND NOT SDSYS, WHICH IS THE SAME REASON sdprobe.ps1 GIVES AND ONE
# MORE.  A user account needs no elevation.  LOGTO SDSYS does: CPROC's
# logto.authorised admits an already-elevated session, an internal one, or one
# that has JUST OBTAINED privilege - and that last route asks UAC, so every run
# against SDSYS puts a consent prompt in front of whoever is at the machine.
# Six runs, six prompts, and the person clicking them is not necessarily the
# person who started the script.  THE GROUP FALLBACK DOES NOT HELP: the SDSYS
# register entry names a group 'sdsys' that does not exist on Windows.
# Measure in a user account unless the thing being measured is SDSYS.
#
# THE SHAPE IS PROJECT_STATUS section 6's: a whole script ending in OFF, fed
# down a pipe under Start-Job with a timeout, with a blank sacrificial first
# line to absorb the pipe's BOM.  A bare "echo CMD | sd" hangs the session and
# leaves a stray sd.exe that costs an elevation to clear.
#
# IT REFUSES A RUN THAT MEASURED NOTHING.  An empty transcript, or fewer
# command echoes than commands sent, and it says so - an empty transcript
# scored against a set of patterns produces tidy negatives that look like
# findings.
#
# ***THE TIMEOUT PATH COSTS THE INSTALL, NOT JUST THE RUN.  AVOID REACHING
# IT.***  Killing the job kills the sd session, and PROJECT_STATUS.md is
# explicit: "never Stop-Process an sd session on a tree you still want to
# measure."  The dead session keeps its user-table slot; nothing reaps it
# without elevation; LOGOUT n only marks it "(logout pending)" because logout
# signals a process that is gone; and sdwind's five-minute check_lost_users()
# sweep has been observed answering every NEW session "Forced logout" for
# twenty minutes.  Recovery is elevated: sd -cleanup, then a service restart
# if that does not take.
#
# SO THE RULE IS PREVENTION, AND IT IS ONE RULE: NEVER SEND A COMMAND THAT CAN
# PROMPT.  A prompt eats the following lines as its answers and the session
# then waits for ever.  COPY prompts when a select list is active - give it
# explicit record ids, or NO.QUERY.  CREATE.FILE, DELETE.FILE and DELETE all
# take NO.QUERY.  SAVE.LIST and GET.LIST prompt when the name is omitted.
# If a verb has a confirmation, supply the switch that suppresses it.

[CmdletBinding()]
param(
    [string[]]$Commands,
    [string]$File,
    [string]$Account = 'don',
    [int]$TimeoutSec = 90,
    [switch]$Raw
)

$ErrorActionPreference = 'Stop'

$sdExe = Join-Path $env:ProgramFiles 'SD\usr\bin\sd.exe'

if ($File) {
    if (-not (Test-Path -LiteralPath $File)) { Write-Output "sdtcl: no such file $File"; exit 2 }
    $Commands = @(Get-Content -LiteralPath $File | Where-Object { $_.Trim() -ne '' })
}
if (-not $Commands -or $Commands.Count -eq 0) {
    Write-Output 'sdtcl: no commands given - refusing to run an empty session'
    exit 2
}
if (-not (Test-Path -LiteralPath $sdExe)) { Write-Output "sdtcl: no sd.exe at $sdExe"; exit 2 }

Write-Output '--- sdtcl -----------------------------------------------------'
Write-Output ('  sd.exe  : ' + $sdExe)
Write-Output ('  sha256  : ' + (Get-FileHash -LiteralPath $sdExe -Algorithm SHA256).Hash.Substring(0, 16))
Write-Output ('  account : ' + $Account)
Write-Output ('  commands: ' + $Commands.Count)
foreach ($c in $Commands) { Write-Output ('    | ' + $c) }
Write-Output '---------------------------------------------------------------'

$body = "`n" + ((@("LOGTO $Account", 'TERM 200,9999') + $Commands + @('OFF')) -join "`n") + "`n"

# ANYTHING SD's CHILD SHELL WRITES TO stderr ARRIVES HERE AS AN ErrorRecord,
# AND UNDER ErrorActionPreference='Stop' THAT KILLS THIS SCRIPT AND LOSES THE
# WHOLE TRANSCRIPT.  Not theoretical - it happened twice in one session,
# 27 Aug 2026, measuring the SH verb: "SH sd" hits SD's own nested-session
# guard, and "SH echo a && echo b" is a PowerShell 5.1 parse error.  Both wrote
# one line to stderr; both times every command before them was lost and the run
# had to be repeated.
#
# SO Receive-Job RUNS WITH 'Continue' AND THE ERROR STREAM IS KEPT, not
# discarded: what the child shell said on stderr is part of the measurement -
# a refusal is usually the thing being measured - and swallowing it would
# leave a tidy transcript with the answer missing.
$job = Start-Job -ScriptBlock { param($exe, $text) $text | & $exe } -ArgumentList $sdExe, $body
$prevEAP = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
if (Wait-Job $job -Timeout $TimeoutSec) {
    $out = Receive-Job $job 2>&1
    $timedOut = $false
} else {
    Stop-Job $job
    $out = Receive-Job $job 2>&1
    $timedOut = $true
}
$ErrorActionPreference = $prevEAP
$out = $out | ForEach-Object { if ($_ -is [System.Management.Automation.ErrorRecord]) { $_.ToString() } else { $_ } }
Remove-Job $job -Force

# WINDOWS POWERSHELL 5.1 HAS NO `e ESCAPE - it arrived in PowerShell 6, so a
# pattern written "`e\[..." is the literal letter e and strips NOTHING.  This
# is PROJECT_STATUS section 6's trap and it is not theoretical: written that
# way, TERM 200,9999 comes back as TERM<ESC>[7G200,9999 and any check whose
# anchor spans the escape silently misses.  Build it from the code point.
$esc = [string][char]27
$text = (($out -replace ($esc + '\[[0-9;]*[A-Za-z]'), '') -join "`n")

if ($timedOut) {
    Write-Output $text
    Write-Output ''
    Write-Output "*** SD did not finish in $TimeoutSec s - it was waiting for input,"
    Write-Output '*** and the session has now been killed.  A command prompted and ate'
    Write-Output '*** the following lines as its answers; look at the transcript above'
    Write-Output '*** to see which one, and give it NO.QUERY or explicit arguments.'
    Write-Output '***'
    Write-Output '*** THIS HAS COST THE INSTALL, NOT JUST THE RUN.  The dead session'
    Write-Output '*** keeps its user-table slot.  LOGOUT n will only mark it "(logout'
    Write-Output '*** pending)" - logout signals a process that no longer exists - and'
    Write-Output '*** BUILD.INDEX and anything else needing exclusive access will be'
    Write-Output '*** refused while it is there.  RECOVERY IS ELEVATED:'
    Write-Output '***'
    Write-Output '***     & "C:\Program Files\SD\usr\bin\sd.exe" -cleanup'
    Write-Output '***'
    Write-Output '*** The leading & is required.  A quoted path at the start of a'
    Write-Output '*** PowerShell line is an expression, not a command, so without it'
    Write-Output '*** the switch is a parser error and nothing runs.'
    Write-Output '***'
    Write-Output '*** and restart the SD service if that does not take.  Check the'
    Write-Output '*** errlog for "Forced logout": sdwind sweeps every five minutes and'
    Write-Output '*** has been seen refusing healthy sessions after a kill.'
    exit 2
}

$echoes = ([regex]::Matches($text, '(?m)^:')).Count
Write-Output ('  transcript lines: ' + (@($text -split "`n")).Count + ', command echoes: ' + $echoes)
if ($text.Trim().Length -eq 0) {
    Write-Output 'sdtcl: THE SESSION PRODUCED NOTHING - refusing to report it as output.'
    exit 2
}
if ($echoes -lt $Commands.Count) {
    Write-Output ('sdtcl: only ' + $echoes + ' command echo(es) for ' + $Commands.Count +
                  ' commands - the session did not get through the script.')
    Write-Output '       The transcript follows so you can see how far it got.'
}

Write-Output ''
if ($Raw) {
    Write-Output $text
} else {
    $keep = @()
    foreach ($l in ($text -split "`n")) {
        $s = $l.TrimEnd("`r")
        if ($s -match '^\s*$') { continue }
        if ($s -match '^:\s*$') { continue }
        $keep += $s
    }
    Write-Output ($keep -join "`n")
}
exit 0
