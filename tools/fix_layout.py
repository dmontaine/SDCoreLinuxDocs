#!/usr/bin/env python3
"""
Fix all rendered HTML pages:
1. Move the pagenav OUT of the footer and place it prominently after </main>
2. Widen the page layout - increase max-widths significantly
3. Make the pagenav visible and prominent

Works on all HTML files in GettingStarted/html, User/html, Administrator/html.
The set list is SETS below; keep this line in step with it.
"""

import os
import re

DOCS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SETS = ["GettingStarted", "User", "Administrator"]

# ── New CSS for pagenav (placed prominently in the main column) ──

OLD_PAGENAV_CSS = """/* prev/next page navigation */
.pagenav {
  max-width: 46rem;
  margin: 2.5rem 0 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--rule);
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}
.pagenav a {
  color: var(--ink-soft);
  text-decoration: none;
  font-size: 0.92rem;
  line-height: 1.4;
  max-width: 48%;
}
.pagenav a:hover { color: var(--accent); text-decoration: underline; }
.pagenav .pn-prev { text-align: left; }
.pagenav .pn-next { text-align: right; }
.pagenav .pn-label {
  display: block;
  font-size: 0.72rem;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--ink-faint);
  margin-bottom: 0.15rem;
}
.pagenav .pn-spacer { flex: 1; }
@media print { .pagenav { display: none; } }"""

NEW_PAGENAV_CSS = """/* prev/next page navigation - prominent, in main column */
.pagenav {
  margin: 3rem 0 1.5rem;
  padding: 1.25rem 0 0;
  border-top: 2px solid var(--rule-firm);
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
}
.pagenav a {
  color: var(--ink);
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.4;
  max-width: 48%;
  display: inline-flex;
  flex-direction: column;
  gap: 0.2rem;
}
.pagenav a:hover { color: var(--accent); text-decoration: underline; }
.pagenav .pn-prev { text-align: left; }
.pagenav .pn-next { text-align: right; margin-left: auto; }
.pagenav .pn-label {
  font-size: 0.72rem;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--ink-faint);
  font-weight: 400;
}
.pagenav .pn-spacer { flex: 1; }
@media print { .pagenav { display: none; } }"""

# ── Width changes ──
# Old: .page max-width: 66rem, grid 14rem + 1fr, main max-width: 46rem
# New: .page max-width: 90rem, grid 16rem + 1fr, main max-width: none

WIDTH_REPLACEMENTS = [
    # Widen the page container
    (".page {\n  max-width: 66rem;",
     ".page {\n  max-width: 90rem;"),
    # Widen the sidebar slightly
    ("grid-template-columns: 14rem minmax(0, 1fr);",
     "grid-template-columns: 16rem minmax(0, 1fr);"),
    # Remove main max-width constraint
    ("main { max-width: 46rem; }",
     "main { max-width: none; }"),
    # Remove paragraph width constraint
    ("main > p, main > ul, main > ol, main > blockquote { max-width: 72ch; }",
     "main > p, main > ul, main > ol, main > blockquote { max-width: 80ch; }"),
    # Widen masthead
    (".masthead div {\n  max-width: 66rem;",
     ".masthead div {\n  max-width: 90rem;"),
    # Widen footer
    ("footer {\n  max-width: 66rem;",
     "footer {\n  max-width: 90rem;"),
    # Widen responsive breakpoint
    ("@media (max-width: 60rem) {",
     "@media (max-width: 70rem) {"),
    # Widen the pagenav max-width in old CSS if present
    ('.pagenav {\n  max-width: 46rem;',
     '.pagenav {\n  max-width: none;'),
    # Widen titlepage
    (".titlepage {\n  /* .page IS A GRID",
     ".titlepage {\n  /* .page IS A GRID"),
]

def fix_html_file(fpath):
    """Fix a single HTML file."""
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Replace old pagenav CSS with new
    if OLD_PAGENAV_CSS in content:
        content = content.replace(OLD_PAGENAV_CSS, NEW_PAGENAV_CSS)
    elif NEW_PAGENAV_CSS not in content:
        # Page doesn't have pagenav CSS yet (shouldn't happen for non-index pages)
        pass

    # 2. Apply width changes
    for old, new in WIDTH_REPLACEMENTS:
        if old != new and old in content:
            content = content.replace(old, new)

    # 3. Move pagenav out of footer
    # Current structure: ...</main>\n</div>\n<footer>...Generated from...<nav class="pagenav">...</nav>\n<p>set index</p>\n</footer>
    # Target structure:  ...</main>\n<nav class="pagenav">...</nav>\n<p>set index link</p>\n</div>\n<footer>...Generated from...</footer>

    # Extract the pagenav and set-index link from inside the footer
    pagenav_match = re.search(r'(<nav class="pagenav">.*?</nav>\s*<p style="[^"]*"><a href="index\.html">[^<]+</a></p>)', content, re.DOTALL)
    if pagenav_match:
        pagenav_html = pagenav_match.group(1)
        # Remove the pagenav and set-index link from inside the footer
        content = content.replace(pagenav_html + '\n', '')
        # Also clean up any leftover newlines
        # Remove the pagenav from wherever it was in the footer
        content = re.sub(r'<nav class="pagenav">.*?</nav>\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'<p style="margin:0\.5rem[^"]*"><a href="index\.html">[^<]+</a></p>\s*', '', content)

        # Insert the pagenav after </main> but before </div>
        # The structure is: </main>\n</div>\n<footer>
        # We want: </main>\n<pagenav>\n</div>\n<footer>
        content = content.replace('</main>\n</div>',
                                  '</main>\n' + pagenav_html + '\n</div>')

    # 4. Also add a "set index" link at the top of the page, in the masthead area
    # Actually, let's add it to the pagenav area instead - it's already there

    if content != original:
        with open(fpath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        return True
    return False


def fix_set_index(fpath):
    """Fix a set index page - just widen it."""
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    for old, new in WIDTH_REPLACEMENTS:
        if old != new and old in content:
            content = content.replace(old, new)

    # Also widen setindex max-width
    content = content.replace(".setindex {\n  max-width: 46rem;",
                              ".setindex {\n  max-width: none;")

    if content != original:
        with open(fpath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        return True
    return False


# ── Process all files ──

total_fixed = 0
for set_name in SETS:
    html_dir = os.path.join(DOCS_ROOT, set_name, "html")
    set_fixed = 0
    for fname in sorted(os.listdir(html_dir)):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(html_dir, fname)
        if fname == 'index.html':
            if fix_set_index(fpath):
                set_fixed += 1
        else:
            if fix_html_file(fpath):
                set_fixed += 1
    print(f"  {set_name}: fixed {set_fixed} pages")
    total_fixed += set_fixed

# Also fix the root index
root_index = os.path.join(DOCS_ROOT, "index.html")
with open(root_index, 'r', encoding='utf-8') as f:
    content = f.read()
original = content
for old, new in WIDTH_REPLACEMENTS:
    if old != new and old in content:
        content = content.replace(old, new)
# Remove the max-width on master-index
content = content.replace(".master-index {\n  grid-column: 1 / -1;\n  max-width: 40rem;",
                          ".master-index {\n  grid-column: 1 / -1;\n  max-width: 60rem;")
if content != original:
    with open(root_index, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print(f"  Root index: fixed")
    total_fixed += 1

print(f"\nTotal: {total_fixed} pages fixed")
