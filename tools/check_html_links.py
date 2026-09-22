#!/usr/bin/env python3
"""Check all HTML files for broken local href links."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
bad = 0
checked = 0

for dirpath, dirs, files in os.walk(ROOT):
    # skip tools directory
    if 'tools' in dirpath:
        continue
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        for m in re.finditer(r'href="([^"]+)"', content):
            href = m.group(1)
            if href.startswith('http') or href.startswith('#') or href == '':
                continue
            checked += 1
            # resolve relative to the file's directory
            target = os.path.normpath(os.path.join(dirpath, href))
            if not os.path.exists(target):
                rel = os.path.relpath(fpath, ROOT)
                print(f'BROKEN: {rel} -> {href}')
                bad += 1

print(f'\nChecked {checked} local links, {bad} broken')
if bad == 0 and checked == 0:
    print('No local links found at all')
sys.exit(1 if bad else 0)
