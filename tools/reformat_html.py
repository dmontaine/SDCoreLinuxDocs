#!/usr/bin/env python3
"""
Reformat all HTML documentation pages to look more like the PDF documents:
1. Remove the two-column grid layout (no sidebar)
2. Remove the "On this page" table of contents sidebar (nav.toc)
3. Move prev/next navigation links to the TOP of each page (right after masthead, before titlepage)
4. Full-width header and body - no narrow constraints
5. Keep the title page section but render it full-width

Transforms the page structure from:
  <masthead>
  <div class="page">          (grid: sidebar + main)
    <titlepage>
    <nav class="toc">         (sidebar TOC - REMOVE)
    <main>...</main>
    <nav class="pagenav">     (bottom nav - MOVE TO TOP)
    <p>set index link</p>
  </div>
  <footer>

To:
  <masthead>
  <nav class="pagenav">       (top nav - MOVED HERE)
  <div class="page">          (now single-column, full-width)
    <titlepage>
    <main>...</main>
    <p>set index link</p>
  </div>
  <footer>
"""

import os
import re

DOCS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETS = ["GettingStarted", "User", "Administrator"]


# ─── New CSS block ─────────────────────────────────────────────────────
# Replaces the entire <style> content with a clean, full-width, no-sidebar layout

NEW_STYLE = """<style>
:root {
  --ink:        #1a1c1f;
  --ink-soft:   #555c66;
  --ink-faint:  #767d87;
  --bg:         #ffffff;
  --panel:      #f5f7f9;
  --rule:       #dde1e6;
  --rule-firm:  #b9c0c8;
  --accent:     #1a5fa8;
  --accent-bg:  #eef4fb;
}
@media (prefers-color-scheme: dark) {
  :root {
    --ink:       #dfe3e8;
    --ink-soft:  #aab2bd;
    --ink-faint: #868f9b;
    --bg:        #16181c;
    --panel:     #1e2127;
    --rule:      #2c3038;
    --rule-firm: #3d434d;
    --accent:    #6fa8e0;
    --accent-bg: #1b2530;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: "Segoe UI", -apple-system, "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  line-height: 1.62;
  -webkit-text-size-adjust: 100%;
}

/* --- masthead: full-width header bar --- */
.masthead {
  border-bottom: 1px solid var(--rule);
  background: var(--panel);
}
.masthead div {
  max-width: 60rem;
  margin: 0 auto;
  padding: 0.7rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 1rem;
  font-size: 0.85rem;
  color: var(--ink-soft);
}
.masthead strong { color: var(--ink); font-weight: 600; }

/* --- top navigation bar (prev/next/set-index) --- */
.navbar {
  max-width: 60rem;
  margin: 0 auto;
  padding: 0.6rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid var(--rule);
  font-size: 0.88rem;
}
.navbar a {
  color: var(--ink-soft);
  text-decoration: none;
}
.navbar a:hover { color: var(--accent); text-decoration: underline; }
.navbar .nav-prev { text-align: left; }
.navbar .nav-next { text-align: right; }
.navbar .nav-home {
  font-size: 0.82rem;
  color: var(--ink-faint);
}

/* --- page container: single column, centered, readable width --- */
.page {
  max-width: 60rem;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
}

/* --- prose --- */
main { max-width: none; }
main > p, main > ul, main > ol, main > blockquote { max-width: none; }

h1, h2, h3, h4 { line-height: 1.25; font-weight: 600; }
h1 {
  font-size: 2rem;
  margin: 0 0 0.35rem;
  letter-spacing: -0.01em;
}
h2 {
  font-size: 1.4rem;
  margin: 2.75rem 0 0.9rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--rule);
}
h3 {
  font-size: 0.8rem;
  margin: 2rem 0 0.6rem;
  color: var(--ink-soft);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
h4 { font-size: 1rem; margin: 1.5rem 0 0.4rem; }

p { margin: 0 0 1rem; }
ul, ol { margin: 0 0 1rem; padding-left: 1.4rem; }
li { margin: 0.25rem 0; }

a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 2px; }

.headerlink {
  margin-left: 0.4rem;
  color: var(--ink-faint);
  text-decoration: none;
  opacity: 0;
  font-weight: 400;
}
h2:hover .headerlink, h3:hover .headerlink { opacity: 1; }

/* --- code --- */
code, pre, kbd {
  font-family: Consolas, "Cascadia Mono", "DejaVu Sans Mono", monospace;
}
code {
  background: var(--panel);
  border: 1px solid var(--rule);
  border-radius: 3px;
  padding: 0.05em 0.3em;
  font-size: 0.88em;
}
pre {
  background: var(--panel);
  border: 1px solid var(--rule);
  border-left: 3px solid var(--rule-firm);
  border-radius: 3px;
  padding: 0.85rem 1.1rem;
  margin: 0 0 1.25rem;
  overflow-x: auto;
  font-size: 0.875rem;
  line-height: 1.5;
}
pre code { background: none; border: 0; padding: 0; font-size: inherit; }

/* --- tables --- */
table {
  border-collapse: collapse;
  width: 100%;
  margin: 0 0 1.5rem;
  font-size: 0.94rem;
}
th, td {
  text-align: left;
  vertical-align: baseline;
  padding: 0.5rem 0.9rem 0.5rem 0;
  border-bottom: 1px solid var(--rule);
}
th {
  border-bottom: 2px solid var(--rule-firm);
  font-weight: 600;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ink-soft);
}
td:first-child { white-space: nowrap; padding-right: 1.5rem; }
td:first-child code { white-space: nowrap; }

/* --- notes --- */
blockquote {
  margin: 0 0 1.25rem;
  padding: 0.8rem 1.1rem;
  border: 1px solid var(--rule);
  border-left: 3px solid var(--accent);
  border-radius: 3px;
  background: var(--accent-bg);
}
blockquote p:last-child { margin-bottom: 0; }
blockquote code { background: var(--bg); }

/* --- footer --- */
footer {
  max-width: 60rem;
  margin: 0 auto;
  padding: 1.5rem;
  border-top: 1px solid var(--rule);
  color: var(--ink-faint);
  font-size: 0.82rem;
}

/* --- set index link --- */
.set-link {
  margin: 1.5rem 0 0;
  font-size: 0.82rem;
  color: var(--ink-faint);
}
.set-link a { color: var(--ink-soft); }

/* --- title page --- */
.titlepage {
  max-width: none;
  margin: 0 auto 3.5rem;
  padding: 2rem 0 2.5rem;
  border-bottom: 1px solid var(--rule);
}
.titlepage .tp-product {
  font-size: 0.78rem;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--ink-faint);
  margin: 0 0 1.6rem;
}
.titlepage .tp-product span {
  display: inline-block;
  margin-left: 0.5rem;
  padding: 0.1rem 0.45rem;
  border: 1px solid var(--rule-firm);
  border-radius: 3px;
  letter-spacing: 0.04em;
}
.titlepage h1.tp-title {
  font-size: 2.35rem;
  line-height: 1.15;
  margin: 0 0 0.85rem;
  border: 0;
  padding: 0;
}
.titlepage .tp-subtitle {
  font-size: 1.08rem;
  line-height: 1.5;
  color: var(--ink-soft);
  margin: 0 0 3.9rem;
  max-width: 34rem;
}
.titlepage dl.tp-meta {
  margin: 0 0 2.2rem;
  padding: 1.1rem 0;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}
.titlepage dl.tp-meta > div {
  display: flex;
  gap: 1rem;
  padding: 0.28rem 0;
}
.titlepage dl.tp-meta dt {
  flex: 0 0 9.5rem;
  font-size: 0.8rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--ink-faint);
  padding-top: 0.15rem;
}
.titlepage dl.tp-meta dd {
  margin: 0;
  flex: 1;
}
.titlepage .tp-licence p {
  font-size: 0.9rem;
  line-height: 1.55;
  color: var(--ink-soft);
  margin: 0 0 0.7rem;
  max-width: 36rem;
}
.titlepage .tp-url {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.86em;
  word-break: break-all;
}
@media (max-width: 34rem) {
  .titlepage dl.tp-meta > div { display: block; }
  .titlepage dl.tp-meta dt { margin-bottom: 0.1rem; }
}

/* --- set index page --- */
.setindex {
  max-width: none;
  margin: 0;
  padding: 0;
}
.setindex h1 { margin-bottom: 0.35rem; }
.setindex .si-subtitle {
  font-size: 1.05rem;
  color: var(--ink-soft);
  margin: 0 0 2rem;
}
.setindex .si-desc {
  color: var(--ink-soft);
  font-size: 0.92rem;
  margin: 0 0 2rem;
}
.setindex .si-source {
  font-family: Consolas, "Cascadia Mono", monospace;
  font-size: 0.78rem;
  color: var(--ink-faint);
}
.setindex table { font-size: 0.92rem; }
.setindex td:nth-child(2) { white-space: normal; }
.setindex td:nth-child(3) { white-space: nowrap; }

/* --- master index page --- */
.master-index {
  max-width: none;
  margin: 0 auto;
  padding: 3rem 0 2.5rem;
}
.master-index h1 {
  font-size: 2.35rem;
  line-height: 1.15;
  margin: 0 0 0.85rem;
  border: 0;
  padding: 0;
}
.master-index .mi-subtitle {
  font-size: 1.08rem;
  line-height: 1.5;
  color: var(--ink-soft);
  margin: 0 0 4rem;
  max-width: 34rem;
}
.master-index .mi-sets {
  margin: 0 0 2.5rem;
  padding: 1.5rem 0;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}
.master-index .mi-set { margin: 0 0 1.5rem; }
.master-index .mi-set:last-child { margin-bottom: 0; }
.master-index .mi-set h2 {
  font-size: 1.15rem;
  margin: 0 0 0.4rem;
  padding: 0;
  border: 0;
}
.master-index .mi-set h2 a { color: var(--ink); text-decoration: none; }
.master-index .mi-set h2 a:hover { color: var(--accent); text-decoration: underline; }
.master-index .mi-set p {
  font-size: 0.92rem;
  color: var(--ink-soft);
  margin: 0 0 0.3rem;
}
.master-index .mi-set .mi-count {
  font-size: 0.78rem;
  color: var(--ink-faint);
}
.master-index .mi-licence p {
  font-size: 0.9rem;
  line-height: 1.55;
  color: var(--ink-soft);
  margin: 0 0 0.7rem;
}

/* --- print --- */
@media print {
  :root {
    --ink: #000;      --ink-soft: #333;   --ink-faint: #555;
    --bg:  #fff;      --panel: #f4f4f4;
    --rule: #999;     --rule-firm: #333;
    --accent: #000;   --accent-bg: #f4f4f4;
  }
  body { background: #fff; color: #000; font-size: 10.5pt; line-height: 1.45; }
  .masthead, .navbar { display: none; }
  .page { display: block; max-width: none; padding: 0; }
  main { max-width: none; }
  a { color: #000; text-decoration: none; }
  h2 { break-after: avoid; page-break-after: avoid; }
  h3, h4 { break-after: avoid; page-break-after: avoid; }
  pre, table, blockquote { break-inside: avoid; page-break-inside: avoid; }
  pre, code { border-color: #ccc; }
  th { border-bottom: 1.5pt solid #000; }
  td, th { border-bottom: 0.5pt solid #999; }
  footer { border-top: 0.5pt solid #999; padding: 0.5rem 0; }
  .set-link { display: none; }
  .titlepage {
    max-width: none;
    margin: 0;
    padding: 0 0 1rem;
    border-bottom: 0;
    break-after: page;
    page-break-after: always;
  }
  .titlepage h1.tp-title { font-size: 26pt; margin-top: 2.5cm; }
  .titlepage .tp-subtitle { font-size: 12pt; }
  .titlepage dl.tp-meta { border-color: #999; }
  .titlepage .tp-licence p { font-size: 9.5pt; }
  .setindex .si-source { display: none; }
}
</style>"""


def extract_pagenav(content):
    """Extract the prev/next nav and set-index link from their current position."""
    # Find the pagenav block
    pagenav_match = re.search(
        r'<nav class="pagenav">(.*?)</nav>',
        content, re.DOTALL
    )
    pagenav_html = pagenav_match.group(0) if pagenav_match else None

    # Extract prev/next links
    prev_match = re.search(
        r'<a class="pn-prev" href="([^"]+)"><span class="pn-label">([^<]+)</span>(.*?)</a>',
        content, re.DOTALL
    )
    next_match = re.search(
        r'<a class="pn-next" href="([^"]+)"><span class="pn-label">([^<]+)</span>(.*?)</a>',
        content, re.DOTALL
    )

    prev_link = prev_match.group(1) if prev_match else None
    prev_label = prev_match.group(2).strip() if prev_match else None
    prev_title = prev_match.group(3).strip() if prev_match else None

    next_link = next_match.group(1) if next_match else None
    next_label = next_match.group(2).strip() if next_match else None
    next_title = next_match.group(3).strip() if next_match else None

    return {
        'prev_link': prev_link,
        'prev_label': prev_label,
        'prev_title': prev_title,
        'next_link': next_link,
        'next_label': next_label,
        'next_title': next_title,
    }


def build_navbar(nav_info, set_index_href):
    """Build the top navbar HTML."""
    parts = []
    if nav_info['prev_link']:
        parts.append(
            f'<a class="nav-prev" href="{nav_info["prev_link"]}">'
            f'&larr; {nav_info["prev_title"]}</a>'
        )
    else:
        parts.append('<span class="nav-prev"></span>')

    if nav_info['next_link']:
        parts.append(
            f'<a class="nav-next" href="{nav_info["next_link"]}">'
            f'{nav_info["next_title"]} &rarr;</a>'
        )
    else:
        parts.append('<span class="nav-next"></span>')

    nav_items = ' | '.join(parts)
    return (
        f'<div class="navbar">'
        f'{nav_items}'
        f' <a class="nav-home" href="{set_index_href}">Set index</a>'
        f'</div>'
    )


def reformat_content_page(content, set_index_href="index.html"):
    """Reformat a content HTML page."""
    nav_info = extract_pagenav(content)

    # Build the navbar
    navbar_html = build_navbar(nav_info, set_index_href)

    # Find <body> and masthead
    body_start = content.find('<body>')
    masthead_end = content.find('</div>\n<div class="page">')
    if masthead_end == -1:
        masthead_end = content.find('</div>\n<section class="titlepage">') - 1 + len('</div>')
        if masthead_end == -1:
            masthead_end = content.find('</div>\n<div class="page">')

    # Extract masthead.  The regex stops at the inner header-row </div>, so
    # re-close the outer .masthead div when the capture is unbalanced.
    masthead_match = re.search(r'(<div class="masthead">.*?</div>)', content, re.DOTALL)
    masthead_html = masthead_match.group(0) if masthead_match else '<div class="masthead"><div><strong>SD Core for Windows</strong><span>W1.0-0</span></div></div>'
    if masthead_html.count('<div') > masthead_html.count('</div>'):
        masthead_html += '</div>'

    # Find title after the titlepage section
    title_match = re.search(r'<title>(.*?)</title>', content)
    title_text = title_match.group(1) if title_match else "SD Core for Windows"

    # Remove the old <style>...</style> block
    content_no_style = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)

    # Build the new body content:
    # 1. Remove nav.toc (sidebar)
    # 2. Remove old pagenav
    # 3. Remove old set-index link paragraph
    # 4. Extract the inner content (titlepage + main)

    # Find the content between <div class="page"> and </div>\n<footer
    page_match = re.search(
        r'<div class="page">(.*?)</div>\s*<footer',
        content_no_style, re.DOTALL
    )
    if not page_match:
        # Try alternative pattern
        page_match = re.search(
            r'<div class="page">(.*?)</div>\s*<footer',
            content_no_style, re.DOTALL
        )

    if page_match:
        inner = page_match.group(1)
    else:
        inner = ""

    # Remove nav.toc block entirely
    inner = re.sub(r'<nav class="toc">.*?</nav>', '', inner, flags=re.DOTALL)

    # Remove old pagenav
    inner = re.sub(r'<nav class="pagenav">.*?</nav>', '', inner, flags=re.DOTALL)

    # Remove old set-index link paragraph
    inner = re.sub(
        r'<p style="grid-column:1/-1[^"]*"[^>]*><a href="index\.html">[^<]+</a></p>',
        '',
        inner
    )
    inner = re.sub(
        r'<p style="[^"]*"[^>]*><a href="index\.html">[^<]+</a></p>',
        '',
        inner
    )

    # Add set-index link at the bottom of the content
    set_link = f'\n<p class="set-link"><a href="{set_index_href}">&larr; Set index</a></p>'

    # Build the new page
    new_body = (
        f'{masthead_html}\n'
        f'{navbar_html}\n'
        f'<div class="page">\n'
        f'{inner.strip()}\n'
        f'{set_link}\n'
        f'</div>'
    )

    # Find footer
    footer_match = re.search(r'(<footer>.*?</footer>)', content_no_style, re.DOTALL)
    footer_html = footer_match.group(1) if footer_match else ''

    # Reassemble
    new_html = (
        f'<!DOCTYPE html>\n'
        f'<html lang="en">\n'
        f'<head>\n'
        f'<meta charset="utf-8">\n'
        f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>{title_text}</title>\n'
        f'{NEW_STYLE}\n'
        f'</head>\n'
        f'<body>\n'
        f'{new_body}\n'
        f'{footer_html}\n'
        f'</body>\n'
        f'</html>\n'
    )

    return new_html


def reformat_index_page(content, page_class="setindex"):
    """Reformat a set index or master index page."""
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title_text = title_match.group(1) if title_match else "SD Core for Windows"

    # Find masthead.  The regex stops at the inner header-row </div>, so
    # re-close the outer .masthead div when the capture is unbalanced.
    masthead_match = re.search(r'(<div class="masthead">.*?</div>)', content, re.DOTALL)
    masthead_html = masthead_match.group(0) if masthead_match else '<div class="masthead"><div><strong>SD Core for Windows</strong><span>W1.0-0</span></div></div>'
    if masthead_html.count('<div') > masthead_html.count('</div>'):
        masthead_html += '</div>'

    # Remove old style
    content_no_style = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)

    # Find the content between <div class="page"> and </div>\s*<footer
    page_match = re.search(
        r'<div class="page">(.*?)</div>\s*<footer',
        content_no_style, re.DOTALL
    )
    if page_match:
        inner = page_match.group(1)
    else:
        inner = ""

    # Clean up any inline style overrides on the main element
    inner = re.sub(
        r'<main class="(setindex|master-index)"[^>]*>',
        r'<main class="\1">',
        inner
    )

    # Find footer
    footer_match = re.search(r'(<footer>.*?</footer>)', content_no_style, re.DOTALL)
    footer_html = footer_match.group(1) if footer_match else ''

    new_html = (
        f'<!DOCTYPE html>\n'
        f'<html lang="en">\n'
        f'<head>\n'
        f'<meta charset="utf-8">\n'
        f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>{title_text}</title>\n'
        f'{NEW_STYLE}\n'
        f'</head>\n'
        f'<body>\n'
        f'{masthead_html}\n'
        f'<div class="page">\n'
        f'{inner.strip()}\n'
        f'</div>\n'
        f'{footer_html}\n'
        f'</body>\n'
        f'</html>\n'
    )

    return new_html


def process_set(set_name):
    """Process all HTML files in a set."""
    html_dir = os.path.join(DOCS_ROOT, set_name, "html")
    if not os.path.isdir(html_dir):
        print(f"  {set_name}: no html directory, skipping")
        return 0

    count = 0
    for fname in sorted(os.listdir(html_dir)):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(html_dir, fname)

        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        if fname == 'index.html':
            new_content = reformat_index_page(content)
        else:
            new_content = reformat_content_page(content)

        with open(fpath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)
        count += 1

    print(f"  {set_name}: reformatted {count} pages")
    return count


# ─── Process all sets ───

total = 0
for set_name in SETS:
    total += process_set(set_name)

# Process root index
root_index = os.path.join(DOCS_ROOT, "index.html")
if os.path.exists(root_index):
    with open(root_index, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = reformat_index_page(content)
    with open(root_index, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_content)
    print(f"  Root index: reformatted")
    total += 1

print(f"\nTotal: {total} pages reformatted")
