# sddebug.ps1 - compile a program in debug mode, run it, and drive SD's
# debugger from a script.  This is how the examples in User document 17 were
# produced.
#
# USAGE
#     sddebug.ps1 -Source <file> -Commands 'STACK','/N','S','R' [-Account don]
#
# WHY IT WORKS AT ALL, which is not obvious.  $DEBUG is a full screen program
# and a piped session has no screen - but its own test is
# "full.screen = TERMINFO('sreg') # ''" (DEBUG:522), and 'sreg' is an SD client
# capability that the 'windows' terminal definition does not carry.  So on this
# port the debugger runs in its LINE mode, prompting with ">" and reading a
# command line, and a pipe can answer it.  Measured: a four command drive
# completed in 0.8 s.
#
# THE PROGRAM IS COMPILED WITH THE 'DEBUGGING' KEYWORD.  Without it BCOMP emits
# no per line debug opcodes, the DEBUG statement compiles to a warning, and the
# debugger is never entered - the program simply runs to the end and every
# debugger command is then fed to the command processor instead, where each is
# a verb that does not exist.  That failure looks like a working run with odd
# output, so the guard below tests for the debugger's own prompt.
param(
    [string]$Source,
    [string[]]$Commands = @('R'),
    [string]$Account = 'don',
    [int]$TimeoutSec = 60
)

$ErrorActionPreference = 'Stop'

$sdExe = Join-Path $env:ProgramFiles 'SD\usr\bin\sd.exe'
$bp    = Join-Path $env:ProgramData ('SD\user_accounts\' + $Account + '\bp')
$name  = 'ZZDBG'
$dest  = Join-Path $bp $name

Write-Output ('sd.exe   : ' + $sdExe)
Write-Output ('source   : ' + $Source)
Write-Output ('dest     : ' + $dest)

if (-not (Test-Path -LiteralPath $sdExe))  { throw "no sd.exe at $sdExe" }
if (-not (Test-Path -LiteralPath $bp))     { throw "no bp directory at $bp" }
if (-not (Test-Path -LiteralPath $Source)) { throw "no source at $Source" }

$text = [IO.File]::ReadAllText($Source) -replace "`r`n", "`n"
[IO.File]::WriteAllText($dest, $text, (New-Object Text.UTF8Encoding $false))
Write-Output ('wrote    : ' + (Get-Item -LiteralPath $dest).Length + ' bytes')

$cmds = @('TERM 200,9999', "BASIC BP $name DEBUGGING", "RUN BP $name") + $Commands + @('OFF')
Write-Output ('commands : ' + ($cmds -join ' ; '))

$body = "`n" + ($cmds -join "`n") + "`n"
$job = Start-Job -ScriptBlock { param($exe, $t) $t | & $exe } -ArgumentList $sdExe, $body
if (Wait-Job $job -Timeout $TimeoutSec) {
    $out = Receive-Job $job
    $finished = $true
} else {
    Stop-Job $job
    $out = Receive-Job $job
    $finished = $false
}
Remove-Job $job -Force

$esc = [char]27
$clean = (($out -replace "$esc\[[0-9]*[A-Za-z]", '') | Out-String)

Write-Output ''
Write-Output '=== SD SAID ============================================================='
Write-Output $clean

Write-Output '=== NULL-CASE GUARD ====================================================='
$compiled = $clean -match '0 error\(s\)'
$prompted = ([regex]::Matches($clean, '(?m)^>')).Count
Write-Output ("  session finished on its own : {0}" -f $finished)
Write-Output ("  compiled with 0 errors      : {0}" -f $compiled)
Write-Output ("  debugger prompts seen       : {0} (commands given: {1})" -f $prompted, $Commands.Count)
$ok = $finished -and $compiled -and ($prompted -gt 0)
if (-not $ok) {
    if (-not $prompted) {
        Write-Output '  REFUSED: no ">" prompt - the debugger was never entered, so the output'
        Write-Output '           above is the command processor rejecting debugger commands.'
    }
    Remove-Item -LiteralPath $dest -Force -ErrorAction SilentlyContinue
    exit 1
}
Write-Output '  the debugger was entered and answered.'
Remove-Item -LiteralPath $dest -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath (Join-Path $bp ('..\bp.out\' + $name)) -Force -ErrorAction SilentlyContinue
exit 0
