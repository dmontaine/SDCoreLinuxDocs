#!/usr/bin/env python3
"""Make the 'Generated from XX.md' in each footer a link to the source markdown."""

import os
import re

DOCS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SETS = ["GettingStarted", "User", "Administrator"]

for set_name in SETS:
    html_dir = os.path.join(DOCS_ROOT, set_name, "html")
    md_dir = os.path.join(DOCS_ROOT, set_name, "markdown")

    for fname in os.listdir(html_dir):
        if not fname.endswith('.html') or fname == 'index.html':
            continue
        fpath = os.path.join(html_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find "Generated from XX-xxx.md." and make it a link
        # The markdown files are in ../markdown/ relative to the html dir
        content = re.sub(
            r'Generated from ([\w.-]+\.md)\.',
            r'Generated from <a href="../markdown/\1">\1</a>.',
            content
        )

        with open(fpath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)

    print(f"  {set_name}: linked source markdown in footers")

print("\nDone.")
