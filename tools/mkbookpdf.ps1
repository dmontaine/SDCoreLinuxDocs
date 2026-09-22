# mkbookpdf.ps1 - print one assembled book to a single PDF, over DevTools.
#
#   powershell -File tools\mkbookpdf.ps1 -In Administrator\book.html `
#                                        -Out Administrator\pdf\Administrator.pdf
#
# Exit 0 the PDF was written and checked, 1 it was not.
#
# WHY NOT --print-to-pdf, WHICH IS WHAT mkpdf.ps1 USES.  The command line is
# all-or-nothing: --no-pdf-header-footer removes Edge's date, title and URL and
# TAKES THE PAGE NUMBERS WITH IT, which is why the shipped PDFs have none.
# Measured 5 Sep 2026: that switch gave 163,942 bytes against 193,113 with the
# furniture.  There is no CLI flag that keeps the numbers and drops the rest.
#
# Page.printToPDF over the DevTools protocol takes a footerTemplate, so the
# strip carries exactly what we put in it.  Two things follow from that and
# both matter:
#
#   * THE RUNNING FOOTER IS PAGE FURNITURE, NOT CONTENT.  An HTML <footer> is
#     an in-flow block: it renders once at the end of the document and, as the
#     owner photographed on 6 Sep 2026, is orphaned alone on a trailing sheet.
#     CSS Paged Media margin boxes would be the standard answer and CHROMIUM
#     HAS NEVER IMPLEMENTED THEM.  This is the only mechanism there is.
#   * generateDocumentOutline gives the PDF a bookmark tree built from the
#     heading elements - the navigation a bound document needs, which no link
#     inside the HTML could provide across separate files.
#
# NO NEW DEPENDENCY.  System.Net.WebSockets.ClientWebSocket ships with .NET
# Framework, so Windows PowerShell 5.1 can speak DevTools without pypdf,
# reportlab, or a websocket package.  That was the recorded objection to this
# route ("might not be worth the websocket client it needs") and it is wrong.

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)] [string] $In,
    [Parameter(Mandatory = $true)] [string] $Out,
    [string] $FooterText = 'SD Core for Windows W1.0-0',
    [int]    $TimeoutSec = 180
)

$ErrorActionPreference = 'Stop'

function Say([string]$t) { Write-Output ("mkbookpdf: " + $t) }

# --- resolve, and say what was resolved -------------------------------------
if (-not (Test-Path -LiteralPath $In)) { Say ("no such file: " + $In); exit 1 }
$inPath  = (Resolve-Path -LiteralPath $In).Path
$outDir  = Split-Path -Parent $Out
if ($outDir -and -not (Test-Path -LiteralPath $outDir)) {
    $null = New-Item -ItemType Directory -Path $outDir -Force
}

$browsers = @(
    (Join-Path $env:ProgramFiles 'Microsoft\Edge\Application\msedge.exe'),
    (Join-Path ${env:ProgramFiles(x86)} 'Microsoft\Edge\Application\msedge.exe'),
    (Join-Path $env:ProgramFiles 'Google\Chrome\Application\chrome.exe'),
    (Join-Path ${env:ProgramFiles(x86)} 'Google\Chrome\Application\chrome.exe')
)
$browser = $browsers | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $browser) { Say 'no Edge or Chrome found'; exit 1 }

Say ("browser  " + $browser)
Say ("in       " + $inPath)
Say ("out      " + $Out)
Say ("footer   " + $FooterText)

# A port nobody else is on.  Asking the OS for a free one and then handing that
# number to the browser is a race, but a narrow and self-correcting one: if the
# browser cannot bind it, the endpoint below never answers and this refuses.
$listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, 0)
$listener.Start()
$port = $listener.LocalEndpoint.Port
$listener.Stop()

$profileDir = Join-Path $env:TEMP ('mkbookpdf-' + [guid]::NewGuid().ToString('N').Substring(0, 8))
$null = New-Item -ItemType Directory -Path $profileDir -Force

# NOT $args.  That is a PowerShell AUTOMATIC variable, and naming a list of
# switches after it means Start-Process silently receives none of them - the
# process still starts, so nothing looks wrong.  Recorded in CLAUDE.md as
# having cost a session in the sd4windows repository, on a probe that then
# "passed" while measuring nothing.
$browserArgs = @(
    '--headless=new',
    ('--remote-debugging-port=' + $port),
    ('--user-data-dir=' + $profileDir),
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-gpu',
    '--disable-extensions',
    'about:blank'
)

$proc = $null
$ws   = $null
try {
    Say ("port     " + $port)
    # The argument list is echoed because a switch list that silently arrived
    # empty is the failure this shape is known for - see $browserArgs above.
    Say ("argv     " + ($browserArgs -join ' '))
    if ($browserArgs.Count -lt 5) { Say 'the browser argument list is too short to be right'; exit 1 }
    $proc = Start-Process -FilePath $browser -ArgumentList $browserArgs -PassThru -WindowStyle Hidden

    # --- find the DevTools endpoint -----------------------------------------
    $wsUrl = $null
    $deadline = (Get-Date).AddSeconds(30)
    while ((Get-Date) -lt $deadline) {
        Start-Sleep -Milliseconds 250
        try {
            $targets = Invoke-RestMethod -Uri ("http://127.0.0.1:$port/json/list") -TimeoutSec 5
            $page = $targets | Where-Object { $_.type -eq 'page' } | Select-Object -First 1
            if ($page -and $page.webSocketDebuggerUrl) { $wsUrl = $page.webSocketDebuggerUrl; break }
        } catch { }
    }
    if (-not $wsUrl) { Say 'the browser never answered on its debugging port'; exit 1 }

    # --- connect -------------------------------------------------------------
    # NO Origin HEADER.  Chromium's DevTools endpoint REFUSES a websocket that
    # carries an Origin it did not expect - a deliberate defence against a web
    # page hijacking the debugging protocol.  Setting one here produced
    # "Unable to connect to the remote server" with the browser running and the
    # endpoint answering, which reads like a dead port and is not one.
    Say ("connect  " + $wsUrl)
    $ws = [System.Net.WebSockets.ClientWebSocket]::new()
    # $null = on EVERY await.  A Task's GetResult() puts a VoidTaskResult on the
    # output stream, and in PowerShell everything a function writes to that
    # stream is part of what it RETURNS - so Send-Cdp below returned an array of
    # [VoidTaskResult, id] and its caller was handed System.Object[] where it
    # wanted an int.  CLAUDE.md records the same shape costing a session in the
    # sd4windows repository.
    $null = $ws.ConnectAsync([Uri]$wsUrl, [Threading.CancellationToken]::None).GetAwaiter().GetResult()

    $script:msgId = 0
    function Send-Cdp([string]$method, $params) {
        $script:msgId++
        $obj = @{ id = $script:msgId; method = $method }
        if ($params) { $obj.params = $params }
        $json  = $obj | ConvertTo-Json -Depth 10 -Compress
        $bytes = [Text.Encoding]::UTF8.GetBytes($json)
        $seg   = [ArraySegment[byte]]::new($bytes)
        $null = $ws.SendAsync($seg, [Net.WebSockets.WebSocketMessageType]::Text, $true,
                              [Threading.CancellationToken]::None).GetAwaiter().GetResult()
        return $script:msgId
    }

    # A CDP reply can be far larger than one frame - a 2 MB PDF arrives as ~2.7
    # MB of base64 - so this reads until the message is complete rather than
    # assuming one buffer holds it.
    function Receive-Cdp([int]$timeoutSec) {
        $buf = [byte[]]::new(65536)
        $sb  = [Text.StringBuilder]::new()
        $cts = [Threading.CancellationTokenSource]::new([TimeSpan]::FromSeconds($timeoutSec))
        while ($true) {
            $seg = [ArraySegment[byte]]::new($buf)
            $r = $ws.ReceiveAsync($seg, $cts.Token).GetAwaiter().GetResult()
            [void]$sb.Append([Text.Encoding]::UTF8.GetString($buf, 0, $r.Count))
            if ($r.EndOfMessage) { break }
        }
        return $sb.ToString() | ConvertFrom-Json
    }

    function Wait-Reply([int]$id, [int]$timeoutSec) {
        $deadline = (Get-Date).AddSeconds($timeoutSec)
        while ((Get-Date) -lt $deadline) {
            $msg = Receive-Cdp $timeoutSec
            if ($msg.PSObject.Properties.Name -contains 'id' -and $msg.id -eq $id) { return $msg }
        }
        throw "no reply to message $id within $timeoutSec s"
    }

    function Wait-Event([string]$method, [int]$timeoutSec) {
        $deadline = (Get-Date).AddSeconds($timeoutSec)
        while ((Get-Date) -lt $deadline) {
            $msg = Receive-Cdp $timeoutSec
            if ($msg.PSObject.Properties.Name -contains 'method' -and $msg.method -eq $method) { return $msg }
        }
        throw "$method never arrived within $timeoutSec s"
    }

    [void](Wait-Reply (Send-Cdp 'Page.enable' $null) 30)

    $uri = ([Uri]$inPath).AbsoluteUri
    Say ("navigate " + $uri)
    [void](Wait-Reply (Send-Cdp 'Page.navigate' @{ url = $uri }) 60)
    [void](Wait-Event 'Page.loadEventFired' $TimeoutSec)

    # Fonts and layout settle after load; printing too early yields a document
    # whose pagination does not match what a reader sees.
    Start-Sleep -Milliseconds 1500

    # --- the footer ----------------------------------------------------------
    # Chromium renders the templates in their own document with NO inherited
    # styling, and a template with no explicit font-size prints at nothing.
    # The two spans are what Chromium substitutes into.
    # Escaped by hand: System.Web is not loaded in Windows PowerShell 5.1 by
    # default, so HttpUtility::HtmlEncode would throw here rather than escape.
    $ft = $FooterText -replace '&', '&amp;' -replace '<', '&lt;' -replace '>', '&gt;'
    $footer = @"
<div style="font-family:'Segoe UI',Arial,sans-serif;font-size:8pt;color:#555;width:100%;margin:0 12mm;">
  <table style="width:100%;border:0;"><tr>
    <td style="text-align:left;">$ft</td>
    <td style="text-align:right;"><span class="pageNumber"></span> of <span class="totalPages"></span></td>
  </tr></table>
</div>
"@

    $printParams = @{
        printBackground       = $true
        displayHeaderFooter   = $true
        headerTemplate        = '<span></span>'
        footerTemplate        = $footer
        generateDocumentOutline = $true
        marginTop             = 0.5
        marginBottom          = 0.6
        marginLeft            = 0.6
        marginRight           = 0.6
        preferCSSPageSize     = $false
    }

    Say 'printing...'
    $reply = Wait-Reply (Send-Cdp 'Page.printToPDF' $printParams) $TimeoutSec
    if (-not $reply.result -or -not $reply.result.data) {
        Say 'printToPDF returned no data'
        if ($reply.error) { Say ("  " + ($reply.error | ConvertTo-Json -Compress)) }
        exit 1
    }

    $bytes = [Convert]::FromBase64String($reply.result.data)
    [IO.File]::WriteAllBytes($Out, $bytes)

    # --- VERIFY, DO NOT ASSUME ----------------------------------------------
    # A zero-byte or truncated write looks like success to everything upstream.
    $fi = Get-Item -LiteralPath $Out
    Say ("bytes    " + $fi.Length)
    if ($fi.Length -lt 10000) { Say 'that is too small to be the document'; exit 1 }
    $head = [Text.Encoding]::ASCII.GetString($bytes[0..4])
    if ($head -ne '%PDF-') { Say ("not a PDF - starts with '" + $head + "'"); exit 1 }
    Say 'ok'
    exit 0
}
finally {
    if ($ws) {
        try { $ws.Dispose() } catch { }
    }
    if ($proc -and -not $proc.HasExited) {
        try { $proc.Kill() } catch { }
    }
    # The browser writes a profile per run; leaving them behind is the litter
    # PRE_RELEASE 178 was filed over in the other repository.
    if (Test-Path -LiteralPath $profileDir) {
        try { Remove-Item -LiteralPath $profileDir -Recurse -Force -ErrorAction SilentlyContinue } catch { }
    }
}
