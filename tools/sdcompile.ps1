# sdcompile.ps1 - compile a BASIC probe inside an SD account and print exactly
# what BCOMP said about it.  The companion to sdprobe.ps1: that one measures
# what a program DOES, this one measures what the compiler REFUSES.
#
# USAGE
#     sdcompile.ps1 -Source <file> [-Account don] [-ExpectErrors] [-TimeoutSec 90]
#
# WHY IT IS A SEPARATE TOOL.  sdprobe.ps1's null-case guard requires "0
# error(s)" and the probe's own START/END markers, so a probe whose whole point
# is that it does not compile can only ever be REFUSED by it.  Half of what the
# User document set records is a refusal - errmsg, MATBUILD ... USING, the
# internal-only intrinsics, the restricted statements - and each one needs an
# instrument that treats the compiler's complaint as the result rather than as
# a failure.
#
# ITS OWN NULL-CASE GUARD, because a compile that never happened prints nothing
# and nothing is easy to read as "no errors":
#   * the source is copied in and its byte count echoed;
#   * "Compiling BP ZZCOMP" must appear - otherwise BASIC never reached it;
#   * the "N error(s)" summary must appear - that line is BCOMP's own, and it
#     is the only proof the compiler ran to the end;
#   * -ExpectErrors demands N > 0 and REFUSES N = 0, so a probe that was meant
#     to be rejected and quietly compiled is a failure, not a pass.
#
# The pipe shape is PROJECT_STATUS section 6's, as in sdprobe.ps1: a whole
# script ending in OFF, fed under Start-Job with a timeout, with a blank
# sacrificial first line to absorb the pipe's BOM.
# -Options is appended to the BASIC command line, e.g. -Options 'DEBUGGING'.
# It is echoed in the "commands" line above, because a compiler option that was
# meant to be passed and was not produces a perfectly ordinary listing.
param(
    [string]$Source,
    [string]$Account = 'don',
    [string]$Options = '',
    [switch]$ExpectErrors,
    [int]$TimeoutSec = 90
)

$ErrorActionPreference = 'Stop'

$sdExe = Join-Path $env:ProgramFiles 'SD\usr\bin\sd.exe'
$bp    = Join-Path $env:ProgramData ('SD\user_accounts\' + $Account + '\bp')
$name  = 'ZZCOMP'
$dest  = Join-Path $bp $name

Write-Output ('sd.exe   : ' + $sdExe)
Write-Output ('bp dir   : ' + $bp)
Write-Output ('source   : ' + $Source)
Write-Output ('dest     : ' + $dest)

if (-not (Test-Path -LiteralPath $sdExe)) { throw "no sd.exe at $sdExe" }
if (-not (Test-Path -LiteralPath $bp))    { throw "no bp directory at $bp" }
if (-not (Test-Path -LiteralPath $Source)){ throw "no source at $Source" }

$text = [IO.File]::ReadAllText($Source) -replace "`r`n", "`n"
if ($text.Length -lt 100) { throw "source is only $($text.Length) bytes - refusing to compile a probe that says nothing" }
[IO.File]::WriteAllText($dest, $text, (New-Object Text.UTF8Encoding $false))
Write-Output ('wrote    : ' + (Get-Item -LiteralPath $dest).Length + ' bytes')

$line = "BASIC BP $name"
if ($Options -ne '') { $line = $line + ' ' + $Options }
$commands = @($line)
Write-Output ('options  : [' + $Options + ']')
Write-Output ('commands : ' + ($commands -join ' ; '))

$body = "`n" + ((@('TERM 200,9999') + $commands + @('OFF')) -join "`n") + "`n"
$job = Start-Job -ScriptBlock { param($exe, $t) $t | & $exe } -ArgumentList $sdExe, $body
if (Wait-Job $job -Timeout $TimeoutSec) {
    $out = Receive-Job $job
} else {
    Stop-Job $job
    $out = Receive-Job $job
    $out += "*** SD did not finish in $TimeoutSec s - it is waiting for input."
    $out += "*** Kill the sdwind PID or cycle.ps1 will refuse to start."
}
Remove-Job $job -Force

$esc = [char]27
$clean = (($out -replace "$esc\[[0-9]*[A-Za-z]", '') | Out-String)

Write-Output ''
Write-Output '=== BCOMP SAID =========================================================='
Write-Output $clean

Write-Output '=== NULL-CASE GUARD ====================================================='
$reached = $clean -match ('Compiling BP ' + $name)
$m       = [regex]::Match($clean, '(?m)^\s*(\d+)\s+error\(s\)')
$summary = $m.Success
$errors  = if ($summary) { [int]$m.Groups[1].Value } else { -1 }
Write-Output ("  BASIC reached the source : {0}" -f $reached)
Write-Output ("  BCOMP printed a summary  : {0}" -f $summary)
Write-Output ("  errors reported          : {0}" -f $errors)
Write-Output ("  -ExpectErrors            : {0}" -f [bool]$ExpectErrors)

$ok = $reached -and $summary
if ($ok -and $ExpectErrors -and $errors -eq 0) {
    Write-Output '  REFUSED: -ExpectErrors was given and the probe compiled cleanly - the'
    Write-Output '           thing being measured did not happen.'
    $ok = $false
}
if (-not $ok) {
    if (-not $reached) { Write-Output '  REFUSED: BASIC never reached the source - nothing was measured.' }
    elseif (-not $summary) { Write-Output '  REFUSED: no "N error(s)" summary - BCOMP did not run to the end.' }
    Remove-Item -LiteralPath $dest -Force -ErrorAction SilentlyContinue
    exit 1
}
Write-Output '  the compiler ran to the end and said what is printed above.'
Remove-Item -LiteralPath $dest -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath (Join-Path $bp ('..\bp.out\' + $name)) -Force -ErrorAction SilentlyContinue
Write-Output ('  removed  : ' + $dest)
exit 0
