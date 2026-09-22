# sdprobe.ps1 - compile and run a BASIC probe inside an SD account and print
# what it said.  This is how every measured value in the User document set was
# produced: write the claim as a program, run it, and quote what came back.
#
# USAGE
#     sdprobe.ps1 -Source <file> [-Account don] [-TimeoutSec 90]
#
# The source file is copied into the account's BP as a record called ZZMATH and
# must print ZZMATH.START and ZZMATH.END.  Anything that does not print both is
# REFUSED with exit 1 - a probe that aborted half way through prints values
# that look like measurements and are not, and that has happened four times.
#
# WHY THE 'don' ACCOUNT AND NOT SDSYS.  C:\ProgramData\SD\sdsys is ACL-locked
# and an ordinary shell cannot write to it; a user account's BP is writable
# without elevation.  Anything needing SDSYS needs an elevated session.
#
# IT DELETES THE PROBE RECORD AFTERWARDS, and any file the probe itself made is
# the probe's own business - the ones in the User set create and DELETE.FILE
# their own work files.
#
# THE SHAPE IS PROJECT_STATUS section 6's: a whole script ending in OFF, fed
# down a pipe under Start-Job with a timeout, with a blank sacrificial first
# line to absorb the pipe's BOM.  A bare "echo CMD | sd" hangs.
param(
    [string]$Source,
    [string]$Account = 'don',
    [int]$TimeoutSec = 90
)

$ErrorActionPreference = 'Stop'

$sdExe = Join-Path $env:ProgramFiles 'SD\usr\bin\sd.exe'
$bp    = Join-Path $env:ProgramData ('SD\user_accounts\' + $Account + '\bp')
$name  = 'ZZMATH'
$dest  = Join-Path $bp $name

Write-Output ('sd.exe   : ' + $sdExe)
Write-Output ('bp dir   : ' + $bp)
Write-Output ('source   : ' + $Source)
Write-Output ('dest     : ' + $dest)

if (-not (Test-Path -LiteralPath $sdExe)) { throw "no sd.exe at $sdExe" }
if (-not (Test-Path -LiteralPath $bp))    { throw "no bp directory at $bp" }
if (-not (Test-Path -LiteralPath $Source)){ throw "no source at $Source" }

$text = [IO.File]::ReadAllText($Source) -replace "`r`n", "`n"
if ($text.Length -lt 200) { throw "source is only $($text.Length) bytes - refusing to run a probe that measures nothing" }
[IO.File]::WriteAllText($dest, $text, (New-Object Text.UTF8Encoding $false))
Write-Output ('wrote    : ' + (Get-Item -LiteralPath $dest).Length + ' bytes')

$commands = @("BASIC BP $name", "RUN BP $name")
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
Write-Output '=== SD SAID ============================================================='
Write-Output $clean

Write-Output '=== NULL-CASE GUARD ====================================================='
$started  = $clean -match 'ZZMATH\.START'
$ended    = $clean -match 'ZZMATH\.END'
$compiled = $clean -match '0 error\(s\)'
Write-Output ("  compiled with 0 errors : {0}" -f $compiled)
Write-Output ("  probe printed START    : {0}" -f $started)
Write-Output ("  probe printed END      : {0}" -f $ended)
if (-not ($started -and $ended -and $compiled)) {
    Write-Output '  REFUSED: the probe did not run end to end - the values above are not a measurement.'
    Remove-Item -LiteralPath $dest -Force -ErrorAction SilentlyContinue
    exit 1
}
Write-Output '  the probe ran end to end.'
Remove-Item -LiteralPath $dest -Force -ErrorAction SilentlyContinue
Write-Output ('  removed  : ' + $dest)
exit 0
