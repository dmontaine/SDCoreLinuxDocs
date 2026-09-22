#!/usr/bin/env python3
"""
Add prev/next navigation to every HTML page in each documentation set,
create a master index page, and create User and Administrator set
index pages.

Works on the rendered HTML files in <set>/html/ directories.
Each page gets a navigation bar inserted before the </footer> with:
  ← Previous page title     Next page title →

Also creates:
  - index.html at the repo root (master index)
  - User/html/index.html (User set index)
  - Administrator/html/index.html (Administrator set index)

Each index entry links to the page and shows its source markdown file.

A SET INDEX DOES NOT LINK BACK TO THE MASTER INDEX, and that is deliberate
rather than an omission.  Each set is handed out on its own, so the master
index is not there for whoever received one set - the link was a 404 in every
delivered copy, and check_all_links.py reported exactly that three times during
the W1.0-0 audit.  The master index is for browsing the tree locally and links
downward only.
"""

import os
import re
import sys
import html as html_mod

# THE PALETTE IS IMPORTED, NOT COPIED.  It used to be written out three times -
# here for the set index, here again for the master index, and in mkdoc.py for
# every content page - so a colour change had to be made in three places and
# was twice made in one.  mkdoc.py defines CSS at module level and guards its
# main() behind __name__, so importing it costs nothing and runs nothing.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mkdoc

DOCS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCT = "SD Core for Windows"
VERSION = "W1.0-0"

# ── Set definitions ──────────────────────────────────────────

SETS = {
    "GettingStarted": {
        "desc": "Installing and running SD Core on Windows, and what differs from OpenQM and SD on Linux.",
    },
    "User": {
        "desc": "For programmers and operators. SDBasic, TCL, the VOC, dictionaries, the file system, and the client API.",
    },
    "Administrator": {
        "desc": "For administrators. Accounts, security, remote access, encryption, configuration, installation, and what an ordinary program may not compile.",
    },
}


# ── The page order is READ, not typed ────────────────────────
#
# THIS LIST USED TO BE THREE HAND-KEPT ARRAYS AND IT HAD ALREADY GONE STALE.
# Administrator/11, Features the Developers Could Not Test, was written on
# 5 Sep 2026 and never added: it had no prev/next bar and no line on its own set
# index, and nothing said so, because a page missing from the list is a page the
# script never looks at.  Splitting fourteen long pages would have added
# fourteen more chances to do the same thing.
#
# The directory sorted is exactly the order that was typed - "01-" sorts before
# "01a" because "-" is 0x2D and "a" is 0x61, and both before "02-" - so reading
# it removes the class rather than checking for it.  A page cannot be missing
# from a list derived from the pages.
#
# It REFUSES A SET IT FOUND NOTHING IN.  A wrong DOCS_ROOT would otherwise leave
# every set empty and every step reporting that it navigated nothing, which is
# the "passes because it did nothing" failure.

def pages_of(set_name):
    md_dir = os.path.join(DOCS_ROOT, set_name, "markdown")
    stems = sorted(n[:-3] for n in os.listdir(md_dir) if n.endswith(".md"))
    if not stems:
        raise SystemExit("add_nav: no .md files in %s - refusing" % md_dir)
    return stems


for _name, _info in SETS.items():
    _info["pages"] = pages_of(_name)
    print("  %-14s %2d page(s): %s ... %s"
          % (_name, len(_info["pages"]), _info["pages"][0], _info["pages"][-1]))

# ── CSS for navigation and index pages ───────────────────────

# THE .pagenav RULES MOVED TO mkdoc.py.  They used to be injected into every
# rendered page from here, which meant the look of a page was decided in two
# files - and the top bar added on 5 September 2026 needed rules the injected
# copy did not have.  mkdoc.CSS now carries them, so a content page needs
# nothing added to its stylesheet at all and this string is only what the two
# index pages need on top of it.

NAV_CSS = """
/* set index page */
.setindex {
  max-width: none;
  margin: 0;
  padding: 2.5rem 0 0;
}
.setindex h1 { margin-bottom: 0.35rem; }
.setindex .si-subtitle {
  font-size: 1.05rem;
  color: var(--ink-soft);
  margin: 0 0 0.5rem;
  max-width: 40rem;
}
.setindex .si-desc {
  color: var(--ink-soft);
  font-size: 0.92rem;
  margin: 0 0 2rem;
  max-width: 40rem;
}
.setindex .si-source {
  font-family: Consolas, "Cascadia Mono", monospace;
  font-size: 0.78rem;
  color: var(--ink-faint);
}
/* THE THREE COLUMNS ARE GIVEN WIDTHS BECAUSE THE SOURCE COLUMN TOOK THEM
   OTHERWISE.  It is monospace and nowrap, so a name like
   05-remote-access-and-the-machine.md demanded about 45% of the table and
   squeezed the description into a two-word-per-line ribbon. */
.setindex table { font-size: 0.92rem; table-layout: fixed; }
.setindex th:nth-child(1), .setindex td:nth-child(1) {
  width: 30%; white-space: normal; padding-right: 1.25rem;
}
.setindex th:nth-child(2), .setindex td:nth-child(2) {
  width: 44%; white-space: normal; padding-right: 1.25rem;
}
.setindex th:nth-child(3), .setindex td:nth-child(3) {
  width: 26%; white-space: normal; overflow-wrap: anywhere;
}
@media print {
  .setindex .si-source { display: none; }
}

/* master index page */
.master-index {
  grid-column: 1 / -1;
  max-width: 40rem;
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
  margin: 0 0 2.5rem;
  max-width: 34rem;
}
.master-index .mi-sets {
  margin: 0 0 2.5rem;
  padding: 1.5rem 0;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}
.master-index .mi-set {
  margin: 0 0 1.5rem;
}
.master-index .mi-set:last-child { margin-bottom: 0; }
.master-index .mi-set h2 {
  font-size: 1.15rem;
  margin: 0 0 0.4rem;
  padding: 0;
  border: 0;
}
.master-index .mi-set h2 a {
  color: var(--ink);
  text-decoration: none;
}
.master-index .mi-set h2 a:hover { color: var(--accent); text-decoration: underline; }
.master-index .mi-set p {
  font-size: 0.92rem;
  color: var(--ink-soft);
  margin: 0 0 0.3rem;
  max-width: 36rem;
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
  max-width: 36rem;
}
"""


# ── Helper: extract title from an HTML page ──────────────────

def get_title(html_path):
    """Extract the document title from a rendered HTML page."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Try <title> tag first
    m = re.search(r'<title>(.+?) - SD Core for Windows</title>', content)
    if m:
        return m.group(1)
    # Fallback: tp-title
    m = re.search(r'<h1 class="tp-title">(.*?)</h1>', content, re.DOTALL)
    if m:
        return html_mod.unescape(m.group(1).strip())
    return os.path.basename(html_path)


def get_subtitle(html_path):
    """Extract the subtitle from a rendered HTML page."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'<p class="tp-subtitle">(.*?)</p>', content, re.DOTALL)
    if m:
        return html_mod.unescape(m.group(1).strip())
    return ""


# ── Add prev/next navigation to all pages ─────────────────────

TOP_MARKER = "<!--PAGENAV-TOP-->"
BOTTOM_MARKER = "<!--PAGENAV-BOTTOM-->"


def nav_bar(where, i, pages, titles, set_name):
    """One prev / set index / next bar.  Same links at both ends of the page."""
    parts = ['<nav class="pagenav pagenav-%s">' % where]

    if i > 0:
        parts.append(
            f'<a class="pn-prev" href="{pages[i-1]}.html">'
            f'<span class="pn-label">&larr; Previous</span>'
            f'{html_mod.escape(titles[i-1])}</a>')
    else:
        parts.append('<span class="pn-spacer"></span>')

    parts.append(f'<a class="pn-up" href="index.html">'
                 f'<span class="pn-label">Contents</span>'
                 f'{html_mod.escape(set_name)}</a>')

    if i < len(pages) - 1:
        parts.append(
            f'<a class="pn-next" href="{pages[i+1]}.html">'
            f'<span class="pn-label">Next &rarr;</span>'
            f'{html_mod.escape(titles[i+1])}</a>')
    else:
        parts.append('<span class="pn-spacer"></span>')

    parts.append('</nav>')
    return '\n'.join(parts)


def add_navigation(set_name, pages):
    """Put a prev/next bar at BOTH ends of every HTML page in a set.

    OWNER'S INSTRUCTION, 5 September 2026: "controls at both the top and bottom
    of the pages".  There was only a bottom bar before, inserted before
    </footer>; the top one goes at the marker mkdoc.py leaves for it.

    IT REFUSES A PAGE WITH NO MARKER rather than inserting one bar and
    reporting two.  A page rendered by an older mkdoc has no marker, and a
    top bar that silently did not appear would look exactly like a page the
    reader had scrolled past."""
    html_dir = os.path.join(DOCS_ROOT, set_name, "html")

    # A NEW MARKDOWN PAGE HAS NO HTML UNTIL ITS OWN SET IS RENDERED, and this
    # script runs over every set while release.ps1 renders one.  So adding a
    # page to set B and releasing set A used to end in a bare FileNotFoundError
    # out of get_title, six frames deep, naming a path and not the cure.
    missing = [p for p in pages
               if not os.path.exists(os.path.join(html_dir, p + ".html"))]
    if missing:
        raise SystemExit(
            'add_nav: %s has %d markdown page(s) with no HTML: %s\n'
            '         render that set first:  python tools/mkdoc.py --in %s '
            '--out %s'
            % (set_name, len(missing), ', '.join(missing),
               os.path.join(set_name, 'markdown'),
               os.path.join(set_name, 'html')))

    titles = {}
    for i, page in enumerate(pages):
        titles[i] = get_title(os.path.join(html_dir, page + ".html"))

    done = 0
    already = 0
    for i, page in enumerate(pages):
        html_path = os.path.join(html_dir, page + ".html")
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Idempotent: release.ps1 runs this on every set, every release.
        #
        # THE CLOSING QUOTE IS NOT IN THIS PATTERN AND THAT IS THE POINT.  It
        # was 'class="pagenav"' until the bars gained a position -
        # class="pagenav pagenav-top" - and then it matched nothing, so a
        # second run treated an already-done page as undone, found its marker
        # consumed, and refused.  A guard that stops matching when the thing it
        # guards changes shape is worse than no guard.
        if 'class="pagenav' in content:
            already += 1
            continue

        for marker in (TOP_MARKER, BOTTOM_MARKER):
            if marker not in content:
                raise SystemExit(
                    'add_nav: %s has no %s - re-render it with mkdoc.py before '
                    'adding navigation' % (html_path, marker))

        content = content.replace(
            TOP_MARKER, nav_bar('top', i, pages, titles, set_name))
        content = content.replace(
            BOTTOM_MARKER, nav_bar('bottom', i, pages, titles, set_name))

        # Both bars, or neither.  A page with one is a page this script got
        # half way through, and it must not be reported as done.
        if content.count('class="pagenav') != 2:
            raise SystemExit('add_nav: %s ended with %d bar(s), expected 2'
                             % (html_path, content.count('class="pagenav')))

        with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        done += 1

    print(f"  {set_name}: top and bottom bars on {done} page(s)"
          f"{f', {already} already had them' if already else ''}")


# ── Exactly one licence block per set ─────────────────────────

def check_licence_block(set_name, pages):
    """One page per set carries the copyright and licence in full - no more.

    OWNER, 5 September 2026: the block comes off every page and is "available
    once for each set of documents".  Once is a number, so it is checked.

    THIS IS THE GUARD FOR A FAILURE NOTHING ELSE CAN SEE.  mkdoc.py can only
    say whether the ONE page it is rendering asked for the block; whether a set
    ends up with a copy - or with two - is a question about the set, and
    add_nav is the only thing that looks at a whole set.  A set that lost its
    licence page would render clean, link clean and ship."""
    html_dir = os.path.join(DOCS_ROOT, set_name, "html")
    carriers = []
    for page in pages:
        with open(os.path.join(html_dir, page + ".html"), 'r',
                  encoding='utf-8') as f:
            if 'class="licenceblock"' in f.read():
                carriers.append(page)

    if len(carriers) != 1:
        raise SystemExit(
            'add_nav: %s has %d page(s) carrying the licence block and must '
            'have exactly 1%s' % (set_name, len(carriers),
                                  (' - ' + ', '.join(carriers)) if carriers else ''))
    # AND IT MUST BE THE FIRST PAGE OF THE SET.  Counting it was not enough:
    # on 6 Sep 2026 all three sets carried the block exactly once and this
    # check was green, yet GettingStarted and User sat it AFTER the
    # introduction because the order is a plain sorted() and "00-" sorts
    # before "00a-".  Administrator was right only by accident - it is the
    # one set with no "00-" file.  The owner's ruling that day was to follow
    # Administrator's pattern in both the HTML and the PDF, so position is
    # now a number too, and it is checked where the order is decided rather
    # than left to whoever next reads a rendered set.  PRE_RELEASE 181.
    if carriers[0] != pages[0]:
        raise SystemExit(
            'add_nav: %s opens with %s and its licence page is %s - the '
            'licence page must sort first.  Rename so it does; do not '
            'special-case the order here, because the book takes this same '
            'order and the two must agree' % (set_name, pages[0], carriers[0]))

    print(f"  {set_name}: licence block on {carriers[0]}, first page of the "
          f"set, and on no other page")


# ── Create set index pages ────────────────────────────────────

def create_set_index(set_name, set_desc, pages):
    """Create an index.html for a documentation set."""
    html_dir = os.path.join(DOCS_ROOT, set_name, "html")
    md_dir = os.path.join(DOCS_ROOT, set_name, "markdown")

    # Build table rows
    rows = []
    for i, page in enumerate(pages):
        html_path = os.path.join(html_dir, page + ".html")
        title = get_title(html_path)
        subtitle = get_subtitle(html_path)
        md_source = page + ".md"
        prev_arrow = "&uarr;" if i > 0 else ""
        rows.append(
            f'<tr>'
            f'<td><a href="{page}.html">{html_mod.escape(title)}</a></td>'
            f'<td>{html_mod.escape(subtitle)}</td>'
            f'<td class="si-source">{md_source}</td>'
            f'</tr>'
        )

    # Count pages
    count = len(pages)
    first_page = pages[0] + ".html"

    # Build the full HTML page using the same template as mkdoc.py
    # but with the set index content instead of a document
    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{set_name} set - {PRODUCT}</title>
<style>
{mkdoc.CSS}
{NAV_CSS}
@media print {{
  .si-source {{ display: none; }}
}}
</style>
</head>
<body>
<div class="page">
<main class="setindex">
<h1>{set_name}</h1>
<p class="si-subtitle">{count} pages. <a href="{first_page}">Start reading &rarr;</a></p>
<p class="si-desc">{set_desc}</p>
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
</main>
<footer>{PRODUCT} {VERSION} &middot; &copy; Donald Montaine &middot; License: CC BY-SA</footer>
</div>
</body>
</html>
"""

    index_path = os.path.join(html_dir, "index.html")
    with open(index_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(page_html)
    print(f"  Created {set_name}/html/index.html ({count} pages)")


# ── Create master index page ──────────────────────────────────

def create_master_index():
    """Create the root index.html listing all sets."""
    set_cards = []
    for set_name, info in SETS.items():
        pages = info["pages"]
        desc = info["desc"]
        count = len(pages)
        first = pages[0] + ".html"
        set_cards.append(f"""<div class="mi-set">
<h2><a href="{set_name}/html/{first}">{set_name}</a></h2>
<p>{desc}</p>
<p class="mi-count">{count} pages &middot; <a href="{set_name}/html/index.html">Set index</a></p>
</div>""")

    sets_html = '\n'.join(set_cards)

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{PRODUCT} - Documentation</title>
<style>
{mkdoc.CSS}
{NAV_CSS}
</style>
</head>
<body>
<div class="page">
<main class="master-index">
<h1>Documentation</h1>
<p class="mi-subtitle">The {PRODUCT} documentation is organised into three sets, each aimed at a different audience. Each page is a self-contained HTML file.</p>
<div class="mi-sets">
{sets_html}
</div>
<div class="mi-licence">
<p>The documentation is licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)</a>.</p>
<p>Copyright &copy; 2026 Donald Montaine.</p>
</div>
</main>
<footer>{PRODUCT} {VERSION} &middot; &copy; Donald Montaine &middot; License: CC BY-SA</footer>
</div>
</body>
</html>
"""

    index_path = os.path.join(DOCS_ROOT, "index.html")
    with open(index_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(page_html)
    print(f"  Created root index.html")


# ── Fix broken links in markdown ──────────────────────────────

def check_and_fix_links(set_name, pages):
    """Check for broken links in the markdown source files and fix them."""
    md_dir = os.path.join(DOCS_ROOT, set_name, "markdown")
    html_dir = os.path.join(DOCS_ROOT, set_name, "html")

    # Build set of valid HTML page names
    valid_pages = set(p + ".html" for p in pages)

    bad = 0
    fixed = 0
    for page in pages:
        md_path = os.path.join(md_dir, page + ".md")
        if not os.path.exists(md_path):
            continue
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all markdown links to .html files
        link_re = re.compile(r'\]\((\d[\w.-]+\.html)(#[\w-]+)?\)')

        for m in link_re.finditer(content):
            target = m.group(1)
            anchor = m.group(2) or ""
            if target not in valid_pages:
                print(f"  BROKEN in {page}.md: links to {target}{anchor}")
                bad += 1

    if bad == 0:
        print(f"  {set_name}: all markdown links resolve")
    else:
        print(f"  {set_name}: {bad} broken links found (see above)")


# ── Main ──────────────────────────────────────────────────────

print("Adding prev/next navigation...")
for set_name, info in SETS.items():
    add_navigation(set_name, info["pages"])

print("\nChecking the licence block...")
for set_name, info in SETS.items():
    check_licence_block(set_name, info["pages"])

print("\nCreating set index pages...")
for set_name, info in SETS.items():
    create_set_index(set_name, info["desc"], info["pages"])

print("\nCreating master index page...")
create_master_index()

print("\nChecking for broken links in markdown...")
for set_name, info in SETS.items():
    check_and_fix_links(set_name, info["pages"])

print("\nDone.")
