#!/usr/bin/env python3
"""
mkbookpdf.py - print mkbook.py's merged HTML to one PDF with a running
footer and a bookmark outline, driving Chrome's DevTools Protocol directly.

    python3 tools/mkbookpdf.py <book.html> <book.pdf> [--footer TEXT]

22 Sep 2026 - Linux port of the Windows docs repo's tools/mkbookpdf.ps1.
That script opens a raw websocket to Chrome/Edge's remote-debugging port
(via .NET's built-in ClientWebSocket) and drives Page.printToPDF with
footerTemplate - the only mechanism that can draw a running footer without
orphaning it, because Chromium has never implemented CSS Paged Media's
@page margin boxes (see mkbook.py's own note) - and generateDocumentOutline,
which builds the PDF's bookmark tree from the book's own <h1>s.  mkpdf.sh's
plain --print-to-pdf command line cannot reach either.

WHY THIS IS PYTHON WITH A HAND-ROLLED WEBSOCKET CLIENT, NOT A LIBRARY.
There is no stdlib websocket client in Python the way ClientWebSocket is
built into .NET, and reaching for one (websocket-client, websockets) would
be a new dependency this exact toolchain has otherwise avoided - mkdoc.py's
own header explains why pandoc was rejected for being a binary dependency
and python-markdown was chosen for being pure Python.  The WebSocket
handshake and frame format (RFC 6455) are a few dozen lines against the
stdlib (socket, hashlib, base64, json) and CDP itself is JSON over that
connection, so nothing here needs anything mkdoc.py does not already need:
Python 3 itself.
"""

import argparse
import base64
import json
import os
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
import uuid


def find_browser():
    for name in ('google-chrome', 'google-chrome-stable', 'chromium',
                 'chromium-browser', 'microsoft-edge', 'microsoft-edge-stable'):
        found = shutil.which(name)
        if found:
            return found
    return None


class CDP:
    """A minimal, blocking WebSocket client speaking just enough of RFC 6455
    to drive Chrome DevTools Protocol - stdlib only, see the module docstring
    for why this exists instead of a library."""

    def __init__(self, ws_url, timeout=30):
        assert ws_url.startswith('ws://'), ws_url
        host_port, _, path = ws_url[len('ws://'):].partition('/')
        path = '/' + path
        host, _, port = host_port.partition(':')
        port = int(port or 80)
        self.sock = socket.create_connection((host, port), timeout=timeout)
        key = base64.b64encode(uuid.uuid4().bytes).decode()
        req = ('GET %s HTTP/1.1\r\nHost: %s:%d\r\nUpgrade: websocket\r\n'
               'Connection: Upgrade\r\nSec-WebSocket-Key: %s\r\n'
               'Sec-WebSocket-Version: 13\r\n\r\n') % (path, host, port, key)
        self.sock.sendall(req.encode())
        status = self._recv_http_headers().split(b'\r\n', 1)[0]
        if b'101' not in status:
            raise RuntimeError('WebSocket handshake failed: %r' % status)
        self._next_id = 1

    def _recv_http_headers(self):
        data = b''
        while b'\r\n\r\n' not in data:
            chunk = self.sock.recv(4096)
            if not chunk:
                break
            data += chunk
        return data

    def _recvn(self, n):
        out = bytearray()
        while len(out) < n:
            chunk = self.sock.recv(n - len(out))
            if not chunk:
                raise RuntimeError('connection closed mid-frame')
            out += chunk
        return bytes(out)

    def _send_frame(self, opcode, payload):
        header = bytearray([0x80 | opcode])
        mask_bit = 0x80
        length = len(payload)
        if length <= 125:
            header.append(mask_bit | length)
        elif length <= 0xFFFF:
            header.append(mask_bit | 126)
            header += struct.pack('>H', length)
        else:
            header.append(mask_bit | 127)
            header += struct.pack('>Q', length)
        mask = os.urandom(4)
        header += mask
        masked = bytearray(payload)
        for i in range(len(masked)):
            masked[i] ^= mask[i % 4]
        self.sock.sendall(bytes(header) + bytes(masked))

    def _recv_frame(self):
        first2 = self._recvn(2)
        fin = first2[0] & 0x80
        opcode = first2[0] & 0x0F
        masked = first2[1] & 0x80
        length = first2[1] & 0x7F
        if length == 126:
            length = struct.unpack('>H', self._recvn(2))[0]
        elif length == 127:
            length = struct.unpack('>Q', self._recvn(8))[0]
        payload = self._recvn(length)
        if masked:
            mask = payload[:4]
            payload = payload[4:]
            payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        return fin, opcode, payload

    def _recv_message(self, timeout=None):
        if timeout is not None:
            self.sock.settimeout(timeout)
        parts = []
        while True:
            fin, opcode, payload = self._recv_frame()
            if opcode == 0x8:
                raise RuntimeError('server closed the connection')
            if opcode == 0x9:
                self._send_frame(0xA, payload)  # pong
                continue
            if opcode in (0x1, 0x0):
                parts.append(payload)
            if fin:
                break
        return b''.join(parts).decode('utf-8')

    def call(self, method, params=None, timeout=90):
        """Send a CDP command and wait for ITS response, discarding any
        event notifications that arrive first - both share this socket."""
        my_id = self._next_id
        self._next_id += 1
        self._send_frame(0x1, json.dumps(
            {'id': my_id, 'method': method, 'params': params or {}}).encode())
        deadline = time.time() + timeout
        while time.time() < deadline:
            msg = json.loads(self._recv_message(timeout=max(1, deadline - time.time())))
            if msg.get('id') == my_id:
                if 'error' in msg:
                    raise RuntimeError('%s: %s' % (method, msg['error']))
                return msg.get('result', {})
        raise RuntimeError('%s: no response within %ds' % (method, timeout))

    def wait_for_event(self, method_name, timeout=90):
        deadline = time.time() + timeout
        while time.time() < deadline:
            msg = json.loads(self._recv_message(timeout=max(1, deadline - time.time())))
            if msg.get('method') == method_name:
                return msg
        raise RuntimeError('%s never arrived within %ds' % (method_name, timeout))

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass


def wait_for_debug_port(port, timeout=15):
    deadline = time.time() + timeout
    last_err = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(
                    'http://127.0.0.1:%d/json/version' % port, timeout=1):
                return
        except OSError as e:
            last_err = e
            time.sleep(0.2)
    raise RuntimeError('Chrome never opened its debugging port: %s' % last_err)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('html', help="mkbook.py's merged HTML file")
    ap.add_argument('pdf', help='where to write the PDF')
    ap.add_argument('--footer', default='SD Core for Linux L1.1-0',
                    help='text drawn at the bottom-left of every printed page')
    ap.add_argument('--timeout', type=int, default=120)
    args = ap.parse_args()

    html_path = os.path.abspath(args.html)
    pdf_path = os.path.abspath(args.pdf)
    if not os.path.isfile(html_path):
        sys.stderr.write('mkbookpdf: no such file: %s\n' % html_path)
        return 1

    browser = find_browser()
    if not browser:
        sys.stderr.write(
            'mkbookpdf: no Chrome, Chromium or Edge found on this machine.\n'
            'mkbookpdf: looked for: google-chrome google-chrome-stable '
            'chromium chromium-browser microsoft-edge microsoft-edge-stable\n')
        return 1

    sys.stdout.write('mkbookpdf: browser %s\n' % browser)
    sys.stdout.write('mkbookpdf: in      %s\n' % html_path)
    sys.stdout.write('mkbookpdf: out     %s\n' % pdf_path)

    profile_dir = tempfile.mkdtemp(prefix='mkbookpdf-')
    # A port derived from our own pid, not a fixed number, so two runs of
    # this script never collide on the same machine.
    debug_port = 9200 + (os.getpid() % 300)
    proc = None
    tab_id = None
    cdp = None
    try:
        proc = subprocess.Popen(
            [browser, '--headless=new', '--disable-gpu', '--no-first-run',
             '--no-default-browser-check', '--user-data-dir=' + profile_dir,
             '--remote-debugging-port=%d' % debug_port, 'about:blank'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        wait_for_debug_port(debug_port)

        # 22 Sep 2026 - Chrome refuses this endpoint as a plain GET (405):
        # newer versions require PUT.  urlopen defaults to GET for a
        # Request with no data, so the method is set explicitly.
        file_url = 'file://' + urllib.parse.quote(html_path)
        req = urllib.request.Request(
            'http://127.0.0.1:%d/json/new?%s' % (debug_port, file_url),
            method='PUT')
        with urllib.request.urlopen(req, timeout=10) as r:
            tab = json.loads(r.read().decode())
        tab_id = tab['id']

        cdp = CDP(tab['webSocketDebuggerUrl'])
        cdp.call('Page.enable')
        # The tab was opened AT the target URL already (json/new took it),
        # so wait for that initial load rather than navigating a second time.
        cdp.wait_for_event('Page.loadEventFired', timeout=args.timeout)

        footer_text = (args.footer.replace('&', '&amp;').replace('<', '&lt;')
                      .replace('>', '&gt;'))
        footer_template = (
            '<div style="width:100%;font-size:9px;color:#555;'
            'padding:0 8mm;display:flex;justify-content:space-between;'
            'font-family:Arial,sans-serif;">'
            '<span>' + footer_text + '</span>'
            '<span><span class="pageNumber"></span> / '
            '<span class="totalPages"></span></span>'
            '</div>')
        result = cdp.call('Page.printToPDF', {
            'printBackground': True,
            'displayHeaderFooter': True,
            'headerTemplate': '<span></span>',
            'footerTemplate': footer_template,
            'generateDocumentOutline': True,
            'marginTop': 0.4, 'marginBottom': 0.5,
            'marginLeft': 0.4, 'marginRight': 0.4,
            'preferCSSPageSize': False,
        }, timeout=args.timeout)

        data = base64.b64decode(result['data'])
        with open(pdf_path, 'wb') as f:
            f.write(data)
    finally:
        if cdp:
            cdp.close()
        if tab_id:
            try:
                urllib.request.urlopen(
                    'http://127.0.0.1:%d/json/close/%s' % (debug_port, tab_id),
                    timeout=5)
            except OSError:
                pass
        if proc:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
        shutil.rmtree(profile_dir, ignore_errors=True)

    # BEFORE AND AFTER, NOT JUST A CONCLUSION (CLAUDE.md).  "the file exists"
    # is also true of a stale PDF an earlier, failed run left behind.
    if not os.path.isfile(pdf_path):
        sys.stderr.write('mkbookpdf: no PDF written.\n')
        return 1
    size = os.path.getsize(pdf_path)
    if size < 20000:
        sys.stderr.write(
            'mkbookpdf: PDF is only %d bytes - almost certainly wrong.\n' % size)
        return 1
    if open(pdf_path, 'rb').read(5) != b'%PDF-':
        sys.stderr.write('mkbookpdf: output does not start with %PDF- .\n')
        return 1
    sys.stdout.write('mkbookpdf: wrote %s (%d bytes)\n' % (pdf_path, size))
    return 0


if __name__ == '__main__':
    sys.exit(main())
