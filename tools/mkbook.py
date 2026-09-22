#!/usr/bin/env python3
"""mkbook.py - assemble one HTML "book" per set, for a single merged PDF.

    python tools\\mkbook.py --set Administrator --out Administrator\\book.html

WHY THIS EXISTS.  The release ships PDF only, and 86 separate PDFs is not a
document - it is a pile of fragments with no continuous page numbers, no
outline, and no search across a set.  Owner's ruling, 6 Sep 2026: "merge per
set".  So each set becomes ONE PDF with a bookmark tree and running page
numbers.

THE FOOTER PROBLEM THIS ALSO SOLVES, and it is the reason the per-page footer
is STRIPPED here rather than kept.  An HTML <footer> is an in-flow block: it
renders once, at the end of the last page's content, so in a printed document
it is either invisible or - as the owner photographed on 6 Sep 2026 - orphaned
alone on a sheet of its own.  A running footer cannot be made from HTML in
Chromium at all: CSS Paged Media margin boxes (@page { @bottom-center }) are
the standard way and Chromium has never implemented them.  The ONLY mechanism
is printToPDF's footerTemplate, which is page furniture rather than content and
therefore cannot be orphaned, split or covered.  mkbookpdf.ps1 supplies it.

So the copyright appears ONCE, on the book's first page - stated by the licence
document that opens every set, which is why the front matter states no licence
of its own - and the running strip is drawn by the printer.

THE OUTLINE IS NOT BUILT HERE EITHER.  printToPDF's generateDocumentOutline
derives it from the heading elements, and every page already carries an
<h1 class="tp-title">.  Keeping the h1s intact is what makes the bookmark tree,
so nothing here may demote them.

WHAT IT REFUSES.  A set with no pages, a page whose shape does not match what
mkdoc.py emits, and a set whose pages disagree about the stylesheet - all three
would otherwise produce a book that renders and is quietly wrong.
"""

import argparse
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS_ROOT = os.path.dirname(HERE)

# The full licence name and the URL belong on the ONE page that makes the
# grant.  In the book that is the front matter, and this is the only place the
# merged PDF states it - the per-page footers are stripped.
COPYRIGHT = 'Copyright © 2026 Donald Montaine'
LICENCE_NAME = ('Creative Commons Attribution-ShareAlike 4.0 International '
                '(CC BY-SA 4.0)')
LICENCE_URL = 'https://creativecommons.org/licenses/by-sa/4.0/'

# Descriptions are the set's own, and a missing one is not fatal - the book
# still reads.  They are here rather than imported from add_nav.py because that
# module runs work at import time.
SET_BLURB = {
    'GettingStarted': 'Installing SD Core for Windows, and finding your way '
                      'around it for the first time.',
    'User':           'Using SD Core for Windows: SD BASIC, TCL, the '
                      'dictionaries and the file system.',
    'Administrator':  'Running an SD Core for Windows installation: accounts, '
                      'security, remote access and the machine.',
}

BOOK_CSS = """
/* --- mkbook.py: what makes a pile of pages into one document ------------- */

/* Every document starts a new sheet - EXCEPT the first, which shares page one
   with the front matter.
   06 Sep 26, owner: "page 1 and 2 of the sample can be merged".  They were
   two half-empty sheets saying the same thing: the front matter announced the
   set and stated the licence, and 00a-copyright-and-licence then stated it
   again in full.  Every set has that page, so the duplication was in the front
   matter and it is the front matter that gave way - see FRONT below. */
.bookpage { break-before: page; }
.bookfront + .bookpage { break-before: auto; }

/* The per-page rule under each title was a separator between documents when
   each was its own file.  Bound together, the page break is the separator and
   the rule is noise at the top of every sheet. */
.bookpage .titlepage { border-bottom: 0; padding-top: 0; }

.bookfront { margin: 0 0 2rem; padding-bottom: 1.25rem;
             border-bottom: 1px solid var(--rule); }
.bookfront h1 { font-size: 2.1rem; margin: 0 0 0.4rem; }
.bookfront .bf-product { text-transform: uppercase; letter-spacing: 0.09em;
                         font-size: 0.8rem; color: var(--ink-faint); }
.bookfront .bf-blurb { font-size: 1.05rem; color: var(--ink-soft); margin: 0; }
"""

# 06 Sep 26 - NO LEGAL BLOCK HERE, deliberately.  Every set opens with
# 00a-copyright-and-licence, which states the copyright and the full grant
# properly, and it now sits on page one directly beneath this - so a legal
# block here said the same thing twice on the same sheet.  The copyright still
# appears once on the first page, which is what was asked for; it just comes
# from the page whose job that is.
#
# THAT SENTENCE WAS TRUE OF ONE SET AND FALSE OF TWO WHEN IT WAS WRITTEN, AND
# THAT IS PRE_RELEASE 181.  "Every set opens with 00a-copyright-and-licence"
# was an assumption about the sort, not a fact: "00-" sorts before "00a-", so
# GettingStarted and User opened with their introduction and the licence page
# landed after it - while the guard below, which only asked whether the
# copyright was in the book ANYWHERE, stayed green.  The two "00-" pages were
# renamed "00b-" on the owner's ruling of 6 Sep 2026 (Administrator's pattern,
# in the HTML and the PDF alike), so the claim is now true of all three; and
# because reasoning that depends on an order must be checked where nothing can
# quietly change it, main()'s guards now assert the POSITION of that document
# rather than trusting the filenames to stay as they are.
FRONT = """<section class="bookfront">
<p class="bf-product">@PRODUCT@ @VERSION@</p>
<h1>@SETNAME@</h1>
<p class="bf-blurb">@BLURB@</p>
</section>
"""

BOOK = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@PRODUCT@ @VERSION@ - @SETNAME@</title>
<style>
@CSS@
@BOOKCSS@
</style>
</head>
<body>
<div class="page">
@FRONT@
@PAGES@
</div>
</body>
</html>
"""

PRETTY = {
    'GettingStarted': 'Getting Started',
    'User': 'User Guide',
    'Administrator': 'Administrator Guide',
}


def pages_of(set_name):
    """The reading order, taken the same way add_nav.py takes it.

    add_nav.py:78 is a plain sorted() over the markdown stems, so '01-' sorts
    before '01a-'.  The book MUST agree with it: a book in a different order
    from the prev/next chain on the website is two documents claiming to be
    one.
    """
    md_dir = os.path.join(DOCS_ROOT, set_name, 'markdown')
    if not os.path.isdir(md_dir):
        sys.exit('mkbook: no such directory: %s' % md_dir)
    stems = sorted(n[:-3] for n in os.listdir(md_dir) if n.endswith('.md'))
    if not stems:
        sys.exit('mkbook: no .md files in %s - refusing' % md_dir)
    return stems


def read(path):
    with open(path, 'r', encoding='utf-8') as fh:
        return fh.read()


def extract_style(page, path):
    m = re.search(r'<style>(.*?)</style>', page, re.S)
    if not m:
        sys.exit('mkbook: no <style> block in %s' % path)
    return m.group(1)


def extract_body(page, path):
    """The content of <div class="page">, minus the nav bars and the footer.

    The shape is mkdoc.py's and is asserted rather than assumed: a page that
    does not match it would otherwise be silently dropped or half-copied.
    """
    m = re.search(r'<div class="page">(.*)</div>\s*</body>', page, re.S)
    if not m:
        sys.exit('mkbook: %s does not have mkdoc\'s <div class="page"> shape'
                 % path)
    body = m.group(1)

    # add_nav.py inserts these AFTER mkdoc has run, so a rendered tree usually
    # has them.  They are prev/next links between .html files and are meaning-
    # less bound into one document.
    body = re.sub(r'<nav class="pagenav.*?</nav>', '', body, flags=re.S)

    # The per-page footer goes.  See this module's header for why it cannot be
    # a running footer and why the printer draws that instead.
    before = body
    body = re.sub(r'<footer>.*?</footer>', '', body, flags=re.S)
    if body == before:
        sys.exit('mkbook: no <footer> found in %s - the page shape has '
                 'changed and this script is stripping the wrong things'
                 % path)
    return body.strip()


def rewrite_ids_and_links(body, stem, stems):
    """Make one document's anchors unique, and point its links inside the book.

    Bound together, two pages that both define id="limits" collide, and every
    href="other.html#frag" leads out of the PDF to a file the reader does not
    have.  Both are rewritten to the book's own namespace.
    """
    body = re.sub(r'\bid="([^"]+)"', lambda m: 'id="%s--%s"' % (stem, m.group(1)),
                  body)

    known = set(stems)

    def fix(m):
        target, frag = m.group(1), m.group(2) or ''
        if target not in known:
            return m.group(0)          # not a page of this set - leave it
        if frag:
            return 'href="#%s--%s"' % (target, frag[1:])
        return 'href="#%s"' % target

    body = re.sub(r'href="([^"#]+)\.html(#[^"]*)?"', fix, body)
    return body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--set', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--product', default='SD Core for Windows')
    ap.add_argument('--version', default='W1.0-0')
    args = ap.parse_args()

    set_name = args.set
    html_dir = os.path.join(DOCS_ROOT, set_name, 'html')
    stems = pages_of(set_name)

    print('mkbook: set      %s' % set_name)
    print('mkbook: html     %s' % html_dir)
    print('mkbook: pages    %d' % len(stems))
    print('mkbook: out      %s' % args.out)

    css = None
    sections = []
    for stem in stems:
        path = os.path.join(html_dir, stem + '.html')
        if not os.path.isfile(path):
            sys.exit('mkbook: %s has no rendered HTML - run mkdoc first' % stem)
        page = read(path)

        this_css = extract_style(page, path)
        if css is None:
            css = this_css
        elif this_css != css:
            # One stylesheet is copied into every page by mkdoc.  If they ever
            # disagree, concatenating them means the last one silently wins for
            # the whole book.
            sys.exit('mkbook: %s has a different <style> block from the first '
                     'page - refusing to guess which one the book should use'
                     % path)

        body = extract_body(page, path)
        body = rewrite_ids_and_links(body, stem, stems)
        sections.append('<section class="bookpage" id="%s">\n%s\n</section>'
                        % (stem, body))

    if not sections:
        sys.exit('mkbook: nothing to assemble - refusing to write an empty book')

    pretty = PRETTY.get(set_name, set_name)
    front = (FRONT
             .replace('@PRODUCT@', html.escape(args.product))
             .replace('@VERSION@', html.escape(args.version))
             .replace('@SETNAME@', html.escape(pretty))
             .replace('@BLURB@', html.escape(SET_BLURB.get(set_name, '')))
             .replace('@COPYRIGHT@', COPYRIGHT)
             .replace('@LICENCE_URL@', LICENCE_URL)
             .replace('@LICENCE_NAME@', LICENCE_NAME))

    book = (BOOK
            .replace('@CSS@', css)
            .replace('@BOOKCSS@', BOOK_CSS)
            .replace('@FRONT@', front)
            .replace('@PAGES@', '\n\n'.join(sections))
            .replace('@PRODUCT@', html.escape(args.product))
            .replace('@VERSION@', html.escape(args.version))
            .replace('@SETNAME@', html.escape(pretty)))

    # The two things a reader would notice missing, and which a template typo
    # would drop without any other symptom.
    if 'bookfront' not in book:
        sys.exit('mkbook: the book rendered without its front matter')
    if COPYRIGHT not in book:
        sys.exit('mkbook: the book rendered without the copyright')

    # WHERE, NOT MERELY WHETHER - PRE_RELEASE 181.  The check above is
    # satisfied by a copyright anywhere in 53 documents, which is how two of
    # the three books shipped with the licence page sitting after the
    # introduction and nothing reporting it.  The front matter carries no legal
    # block of its own precisely because the first document carries one, so if
    # that document is not the licence page the book has no licence on page
    # one at all - and a PDF is read from page one.
    if 'class="licenceblock"' not in sections[0]:
        carrying = [s for s in stems
                    if 'class="licenceblock"' in sections[stems.index(s)]]
        sys.exit('mkbook: %s opens with %s and its licence page is %s - the '
                 'front matter states no licence of its own, so the licence '
                 'page must be the first document.  Rename so it sorts first '
                 '(add_nav.py checks the same thing for the website, and the '
                 'book must not disagree with it)'
                 % (set_name, stems[0],
                    ', '.join(carrying) if carrying else 'nowhere in the set'))

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    with open(args.out, 'w', encoding='utf-8') as fh:
        fh.write(book)

    # An instrument says what it did.  A count of sections is the one number
    # that distinguishes "assembled the set" from "assembled one page".
    print('mkbook: sections %d' % len(sections))
    print('mkbook: bytes    %d' % len(book.encode('utf-8')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
