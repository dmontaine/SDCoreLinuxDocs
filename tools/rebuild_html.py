#!/usr/bin/env python3
"""
Rebuild HTML documentation pages from markdown sources.

Mimics the PDF layout:
  - Full-width masthead bar at the top
  - Top navigation bar with prev/next/set-index links
  - Title page section with metadata
  - Single-column body content (no sidebar, no grid, no columns)
  - Footer with copyright and source link
"""

import re
import os
import sys
import html
import glob

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PRODUCT = "SD Core for Windows"
VERSION = "W1.0-0"
COPYRIGHT = "Copyright \u00a9 2026 Donald Montaine"
LICENCE = "Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)"
LICENCE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"

SETS = {
    "User": {
        "md_dir":   "User/markdown",
        "html_dir": "User/html",
        "set_name": "User",
        "set_desc": "For programmers and operators. SDBasic, TCL, the VOC, dictionaries, the file system, and the client API.",
    },
    "Administrator": {
        "md_dir":   "Administrator/markdown",
        "html_dir": "Administrator/html",
        "set_name": "Administrator",
        "set_desc": "For administrators. Accounts, security, encryption, system limits, configuration, and installation.",
    },
}

# ---------------------------------------------------------------------------
# Markdown to HTML conversion
# ---------------------------------------------------------------------------

def md_to_html(text):
    """Convert markdown to HTML. Handles: headings, bold, italic, code spans,
    code blocks, tables, blockquotes, paragraphs, and inline HTML entities."""

    lines = text.split("\n")
    html_parts = []
    i = 0
    in_table = False
    table_rows = []

    def flush_table():
        nonlocal table_rows, in_table
        if not table_rows:
            return
        # Parse table
        header = table_rows[0]
        separator = table_rows[1] if len(table_rows) > 1 else ""
        data_rows = table_rows[2:] if len(table_rows) > 2 else []

        # Count columns from header
        cells = [c.strip() for c in header.split("|")]
        # Remove empty first/last from leading/trailing |
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]
        ncol = len(cells)

        out = ['<table>']
        # Header
        out.append("<thead>")
        out.append("<tr>")
        for c in cells:
            out.append(f"<th>{inline_md(c)}</th>")
        out.append("</tr>")
        out.append("</thead>")

        # Body
        if data_rows:
            out.append("<tbody>")
            for row in data_rows:
                cells = [c.strip() for c in row.split("|")]
                if cells and cells[0] == "":
                    cells = cells[1:]
                if cells and cells[-1] == "":
                    cells = cells[:-1]
                out.append("<tr>")
                for j, c in enumerate(cells):
                    out.append(f"<td>{inline_md(c)}</td>")
                out.append("</tr>")
            out.append("</tbody>")

        out.append("</table>")
        html_parts.append("\n".join(out))
        table_rows = []
        in_table = False

    def flush_paragraph(buf):
        if buf:
            html_parts.append(f"<p>{inline_md(' '.join(buf))}</p>")

    while i < len(lines):
        line = lines[i]

        # Code block
        if line.strip().startswith("```"):
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(html.escape(lines[i]))
                i += 1
            i += 1  # skip closing ```
            code = "\n".join(code_lines)
            html_parts.append(f"<pre><code>{code}</code></pre>")
            continue

        # Heading
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            if in_table:
                flush_table()
            level = len(m.group(1))
            text_content = m.group(2).strip()
            slug = re.sub(r"[^\w]+", "-", text_content.lower()).strip("-")
            headerlink = f'<a class="headerlink" href="#{slug}" title="Permanent link">#</a>'
            html_parts.append(f'<h{level} id="{slug}">{inline_md(text_content)}{headerlink}</h{level}>')
            i += 1
            continue

        # Table row detection: line with | that's not just text
        if "|" in line and line.strip().startswith("|"):
            # Check if next line is separator
            is_separator = (i + 1 < len(lines) and
                           re.match(r"^\s*\|[\s\-:]+\|", lines[i + 1]))
            if is_separator or in_table:
                if not in_table:
                    in_table = True
                    table_rows = []
                table_rows.append(line.strip())
                i += 1
                continue
            # else: not a table, fall through

        # Blockquote
        if line.strip().startswith(">"):
            if in_table:
                flush_table()
            bq_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                bq_lines.append(lines[i].strip()[1:].strip())
                i += 1
            bq_content = " ".join(bq_lines)
            html_parts.append(f"<blockquote>\n<p>{inline_md(bq_content)}</p>\n</blockquote>")
            continue

        # Table flush if we were in a table and hit non-table line
        if in_table:
            flush_table()

        # Blank line
        if not line.strip():
            i += 1
            continue

        # Paragraph: collect consecutive non-blank, non-special lines
        para_buf = []
        while i < len(lines):
            l = lines[i]
            if not l.strip():
                break
            if l.strip().startswith("```"):
                break
            if re.match(r"^#{1,4}\s+", l):
                break
            if l.strip().startswith(">"):
                break
            if l.strip().startswith("|") and "|" in l:
                # Check for table
                is_sep = (i + 1 < len(lines) and
                          re.match(r"^\s*\|[\s\-:]+\|", lines[i + 1]))
                if is_sep or in_table:
                    break
            para_buf.append(l.strip())
            i += 1
        if para_buf:
            html_parts.append(f"<p>{inline_md(' '.join(para_buf))}</p>")

    # Flush any remaining table
    if in_table:
        flush_table()

    return "\n".join(html_parts)


def inline_md(text):
    """Convert inline markdown: bold, italic, code spans."""
    # Escape HTML first
    text = html.escape(text)
    # Code spans (do first, then protect)
    placeholders = []

    def replace_code(m):
        code = m.group(1)
        placeholders.append(f'<code>{code}</code>')
        return f"\x00{len(placeholders)-1}\x00"

    text = re.sub(r"`([^`]+)`", replace_code, text)
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic (but not if already bold)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Restore code spans
    for idx, ph in enumerate(placeholders):
        text = text.replace(f"\x00{idx}\x00", ph)
    return text


# ---------------------------------------------------------------------------
# Page building
# ---------------------------------------------------------------------------

CSS = """\
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
  .setindex .si-source { display: none; }
}
"""

LICENCE_TEXT = """\
<p>You are free to <strong>share</strong> this document - copy and redistribute it in any medium or format - and to <strong>adapt</strong> it - remix, transform and build upon it - for any purpose, including commercially.</p>
<p>Two conditions apply. <strong>Attribution:</strong> you must give appropriate credit, provide a link to the licence, and indicate if changes were made. <strong>ShareAlike:</strong> if you remix, transform or build upon this document, you must distribute what you produce under the same licence. You may not add legal terms or technological measures that restrict others from doing anything the licence permits.</p>
<p>This is a summary and not a substitute for the licence itself. The complete text is at <span class="tp-url">{}</span>.</p>""".format(LICENCE_URL)


def parse_metadata(md_text):
    """Extract Title and Subtitle from the first two lines."""
    lines = md_text.strip().split("\n")
    title = ""
    subtitle = ""
    body_start = 0

    for i, line in enumerate(lines[:5]):
        m = re.match(r"^Title:\s*(.*)$", line)
        if m:
            title = m.group(1).strip()
            body_start = i + 1
            continue
        m = re.match(r"^Subtitle:\s*(.*)$", line)
        if m:
            subtitle = m.group(1).strip()
            body_start = i + 1
            continue

    # Skip blank lines after metadata
    while body_start < len(lines) and not lines[body_start].strip():
        body_start += 1

    body = "\n".join(lines[body_start:])
    return title, subtitle, body


def build_page_html(title, subtitle, body_html, set_key, filename, prev_link, next_link):
    """Build a complete HTML page."""
    basename = filename.replace(".html", ".md")

    prev_html = ""
    if prev_link:
        prev_html = f'<a class="nav-prev" href="{prev_link["file"]}">&larr; {html.escape(prev_link["title"])}</a>'
    else:
        prev_html = '<span class="nav-prev"></span>'

    next_html = ""
    if next_link:
        next_html = f'<a class="nav-next" href="{next_link["file"]}">{html.escape(next_link["title"])} &rarr;</a>'
    else:
        next_html = '<span class="nav-next"></span>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<title>{html.escape(title)} - {PRODUCT}</title>
<style>
{CSS}
</style>
</head>
<body>
<div class="masthead"><div><strong>{PRODUCT}</strong><span>{VERSION}</span></div></div>
<div class="navbar">{prev_html} | {next_html} <a class="nav-home" href="index.html">Set index</a></div>
<div class="page">
<main class="setindex">
<h1>{html.escape(title)}</h1>
<p class="si-subtitle">{html.escape(subtitle)}</p>
{body_html}
<p class="set-link"><a href="index.html">&larr; Set index</a></p>
</main>
</div>
<footer>{PRODUCT} {VERSION} &middot; &copy; Donald Montaine &middot; License: CC BY-SA &middot; Generated from <a href="../markdown/{basename}">{basename}</a></footer>
</body>
</html>
"""


def build_set_index(set_key, config, page_list):
    """Build the index.html for a set."""
    set_name = config["set_name"]
    set_desc = config["set_desc"]

    rows = []
    for page in page_list:
        title = html.escape(page["title"])
        subtitle = html.escape(page["subtitle"])
        src = page["md_basename"]
        rows.append(
            f'<tr><td><a href="{page["html_name"]}">{title}</a></td>'
            f'<td>{subtitle}</td>'
            f'<td class="si-source">{src}</td></tr>'
        )

    count = len(page_list)
    first_link = page_list[0]["html_name"] if page_list else "#"
    first_title = html.escape(page_list[0]["title"]) if page_list else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<title>{set_name} set - {PRODUCT}</title>
<style>
{CSS}
</style>
</head>
<body>
<div class="masthead"><div><strong>{PRODUCT}</strong><span>{VERSION}</span></div></div>
<div class="page">
<main class="setindex">
<h1>{html.escape(set_name)}</h1>
<p class="si-subtitle">{count} pages. <a href="{first_link}">Start reading &rarr;</a></p>
<p class="si-desc">{html.escape(set_desc)}</p>
<table>
<thead>
<tr>
<th>Page</th>
<th>Description</th>
<th>Source</th>
</tr>
</thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>
<p style="margin-top:1.5rem"><a href="../../index.html">&larr; All documentation sets</a></p>
</main>
</div>
<footer>{PRODUCT} {VERSION} &middot; &copy; Donald Montaine &middot; License: CC BY-SA</footer>
</body>
</html>
"""


def process_set(set_key, config, base_dir):
    """Process all markdown files in a set and generate HTML."""
    md_dir = os.path.join(base_dir, config["md_dir"])
    html_dir = os.path.join(base_dir, config["html_dir"])

    # Find all .md files (excluding index.md if any)
    md_files = sorted(glob.glob(os.path.join(md_dir, "*.md")))

    # Build page list with metadata
    pages = []
    for md_path in md_files:
        md_basename = os.path.basename(md_path)
        html_name = md_basename.replace(".md", ".html")

        with open(md_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        title, subtitle, body = parse_metadata(md_text)
        body_html = md_to_html(body)

        pages.append({
            "md_path": md_path,
            "md_basename": md_basename,
            "html_name": html_name,
            "title": title,
            "subtitle": subtitle,
            "body_html": body_html,
        })

    # Generate each HTML page
    for i, page in enumerate(pages):
        prev_link = pages[i - 1] if i > 0 else None
        next_link = pages[i + 1] if i < len(pages) - 1 else None

        prev = {"file": prev_link["html_name"], "title": prev_link["title"]} if prev_link else None
        nxt = {"file": next_link["html_name"], "title": next_link["title"]} if next_link else None

        html_content = build_page_html(
            page["title"], page["subtitle"], page["body_html"],
            set_key, page["html_name"], prev, nxt
        )

        out_path = os.path.join(html_dir, page["html_name"])
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"  Wrote {page['html_name']}")

    # Generate index.html
    index_html = build_set_index(set_key, config, pages)
    index_path = os.path.join(html_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"  Wrote index.html ({len(pages)} pages)")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isdir(os.path.join(base_dir, "User")):
        # Maybe running from the docs root itself
        base_dir = os.getcwd()

    print(f"Base directory: {base_dir}")

    for set_key, config in SETS.items():
        md_dir = os.path.join(base_dir, config["md_dir"])
        if not os.path.isdir(md_dir):
            print(f"Skipping {set_key}: {md_dir} not found")
            continue
        print(f"\nProcessing {set_key} set...")
        process_set(set_key, config, base_dir)

    print("\nDone.")


if __name__ == "__main__":
    main()
