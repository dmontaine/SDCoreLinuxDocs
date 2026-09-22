#!/usr/bin/env python3
"""Make pagenav span the full page width by adding grid-column: 1 / -1."""

import os
import re

DOCS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETS = ["GettingStarted", "User", "Administrator"]

# The pagenav is inside the .page grid, so it needs grid-column: 1 / -1
# to span both the sidebar and main columns

OLD = """.pagenav {
  margin: 3rem 0 1.5rem;
  padding: 1.25rem 0 0;
  border-top: 2px solid var(--rule-firm);
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
}"""

NEW = """.pagenav {
  grid-column: 1 / -1;
  margin: 3rem 0 1.5rem;
  padding: 1.25rem 0 0;
  border-top: 2px solid var(--rule-firm);
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
  max-width: none;
}"""

# Also need to make the set-index-link span full width
SET_LINK_OLD = '<p style="margin:0.5rem 0 0;font-size:0.82rem;color:var(--ink-faint)"><a href="index.html">'
SET_LINK_NEW = '<p style="grid-column:1/-1;margin:0.5rem 0 0;font-size:0.82rem;color:var(--ink-faint)"><a href="index.html">'

total = 0
for set_name in SETS:
    html_dir = os.path.join(DOCS_ROOT, set_name, "html")
    for fname in os.listdir(html_dir):
        if not fname.endswith('.html') or fname == 'index.html':
            continue
        fpath = os.path.join(html_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        changed = False
        if OLD in content:
            content = content.replace(OLD, NEW)
            changed = True
        if SET_LINK_OLD in content:
            content = content.replace(SET_LINK_OLD, SET_LINK_NEW)
            changed = True
        if changed:
            with open(fpath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
            total += 1

print(f"Fixed {total} pages - pagenav now spans full grid width")
