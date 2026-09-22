#
# mkdoc.py - render documentation Markdown to single-file HTML
#
# command line: python3 gplbld/mkdoc.py --in DIR|FILE... --out DIR
# eg  python gplbld/mkdoc.py --in docs/sample --out docs/sample
#
# NOTHING CALLS THIS YET, DELIBERATELY.  It is not wired into stage.py or
# sd.iss, because naming a .md in either of those files is what makes
# assert-current watch it (the $shipsAs valve, assert-current.ps1:484), and
# from that moment every documentation edit demands a full cycle before any
# verifier will run.  That is correct once the documentation ships; it is a
# toll nobody should pay while the format is still being judged.  See
# HISTORY.md, "20 Aug 2026 - assert-current demanded a full cycle for a
# markdown file".
#
# WHY HTML AT ALL, AND WHY ONE FILE.  Every Windows machine has a browser, so
# there is nothing to install and no format to explain.  Embedding the CSS
# means there is no asset folder to break, no relative path to get wrong when
# the file is copied off the machine, and nothing to fetch - which matters
# because SD installs on machines that are not on the internet.  The user
# prints to PDF from the browser, so no PDF ships, which the no-binaries rule
# in CLAUDE.md forbids anyway.
#
# WHY A LIBRARY RATHER THAN A HAND-ROLLED CONVERTER.  Markdown looks trivial
# until the first nested list inside a table cell.  python-markdown is pure
# Python, so it installs with pip and adds no binary dependency - which is why
# pandoc was rejected despite being the better converter.
#
# THE CSS IS THE POINT OF THIS SCRIPT, not the conversion.  What makes
# technical documentation look like documentation rather than a rendered
# README is a short list, and it is all here: a measure capped near 72
# characters, a system font stack with no web fonts to fetch or license, real
# table and code-block styling, a table of contents with anchors, and a print
# stylesheet so browser-to-PDF comes out clean.
#

import argparse
import html
import os
import re
import sys

try:
    import markdown
except ImportError:
    sys.stderr.write(
        'mkdoc: the python-markdown library is not installed.\n'
        '       pip install markdown\n'
        '       (setup-devbox.ps1 does not install it yet - the documentation\n'
        '        format has not been ruled on, so nothing depends on it.)\n')
    sys.exit(2)


# ---------------------------------------------------------------------------
# The stylesheet.  Shared by every page; written once, here, and IMPORTED BY
# add_nav.py for the index pages rather than copied into them.
#
# ***THE SCREEN NOW LOOKS LIKE THE PDF.  OWNER'S INSTRUCTION, 5 September
# 2026:*** "Change the formatting of the html pages to look as much like the
# pdfs as possible, no side bar.  Allow the user to navigate forward and
# backward through the pages using controls at both the top and bottom of the
# pages."
#
# WHAT THAT MEANT IN PRACTICE was mostly promoting the @media print block to
# the default rules rather than writing new ones - black on white, one column,
# no sidebar, no masthead - because the browser IS the PDF exporter, so that
# block already WAS the PDF's appearance.  What is left in @media print below
# is only the part that is genuinely print-only: point sizes, page breaks, and
# hiding the navigation controls.
#
# THE DARK PALETTE IS GONE, DELIBERATELY.  A PDF has one appearance and the
# instruction was to match it.  A page that is grey-on-black on one machine and
# black-on-white on another is not "as much like the pdf as possible" on the
# first machine.
#
# THE SIDEBAR TABLE OF CONTENTS IS GONE, AND SPLITTING THE LONG PAGES IS WHAT
# PAID FOR IT.  Dropping it means a reader moves between pages rather than
# within one, which is only tolerable if no page is twenty screens long.  See
# README.md, "A number with a letter after it is the second half of a long
# page": fourteen pages were cut in two in the same change.
#
# THE MEASURE IS THE PRINTED PAGE'S, NOT THE BROWSER'S.  The sheet is sized so
# a line of prose runs about as long as it does in the PDF.  Tables and code
# blocks get the full sheet, because a keyword table squeezed into prose width
# wraps in every cell and a syntax line that wraps stops being a syntax line.
# ---------------------------------------------------------------------------

CSS = '''
:root {
  --ink:        #000000;
  --ink-soft:   #333333;
  --ink-faint:  #555555;
  --bg:         #ffffff;
  --panel:      #f4f4f4;
  --rule:       #999999;
  --rule-firm:  #333333;
  --accent:     #000000;
  --accent-bg:  #f4f4f4;
  /* screen only: the ground the sheet sits on, the way a PDF viewer shows one */
  --ground:     #d9dbdf;
  --sheet-edge: #b6b9be;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--ground);
  color: var(--ink);
  font-family: "Segoe UI", -apple-system, "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  -webkit-text-size-adjust: 100%;
}

.page {
  max-width: 52rem;
  margin: 1.75rem auto;
  padding: 0 3.25rem 1rem;
  background: var(--bg);
  border: 1px solid var(--sheet-edge);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.10);
}
@media (max-width: 54rem) {
  .page { margin: 0; border: 0; box-shadow: none; padding: 0 1.25rem 1rem; }
}

/* --- the prose column -------------------------------------------------- */

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
  font-size: 1.02rem;
  margin: 2rem 0 0.6rem;
  color: var(--ink-soft);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-size: 0.8rem;
}
h4 { font-size: 1rem; margin: 1.5rem 0 0.4rem; }

p { margin: 0 0 1rem; }
ul, ol { margin: 0 0 1rem; padding-left: 1.4rem; }
li { margin: 0.25rem 0; }

/* The PDF prints links as plain black text.  On screen they stay black and
   keep the underline: black with no underline would be faithful and would also
   make every cross-reference invisible, which is a worse page than a slightly
   less faithful one. */
a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 2px; }

.headerlink {
  margin-left: 0.4rem;
  color: var(--ink-faint);
  text-decoration: none;
  opacity: 0;
  font-weight: 400;
}
h2:hover .headerlink, h3:hover .headerlink { opacity: 1; }

/* --- code -------------------------------------------------------------- */

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

/* --- tables ------------------------------------------------------------ */

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

/* --- notes ------------------------------------------------------------- */

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

/* The tag line.  The gap above it is the second of the owner's "two blank
   lines", written the same way as the one under the page header so the two
   cannot drift apart. */
footer {
  margin: calc(2 * 1.5em) 0 0;
  padding: 1rem 0;
  border-top: 1px solid var(--rule);
  color: var(--ink-faint);
  font-size: 0.82rem;
}

/* --- prev/next controls, top and bottom --------------------------------
   OWNER'S INSTRUCTION, 5 September 2026: "controls at both the top and bottom
   of the pages".  tools/add_nav.py inserts both bars AFTER the PDFs are
   printed - a "Next page" link is meaningless inside a PDF - so these rules
   describe elements that exist only in the HTML.  They live here rather than
   in add_nav.py so that the whole appearance of a page is decided in one
   file. */

.pagenav {
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  gap: 0.75rem;
  margin: 0;
  padding: 0.9rem 0;
}
.pagenav-top    { border-bottom: 1px solid var(--rule); margin-bottom: 0.5rem; }
.pagenav-bottom { border-top: 1px solid var(--rule); margin-top: 2.5rem; }

.pagenav a {
  flex: 1 1 0;
  min-width: 0;
  color: var(--ink-soft);
  text-decoration: none;
  font-size: 0.9rem;
  line-height: 1.35;
  padding: 0.5rem 0.85rem;
  border: 1px solid var(--rule);
  border-radius: 3px;
}
.pagenav a:hover { color: var(--ink); border-color: var(--rule-firm); background: var(--panel); }
.pagenav .pn-prev { text-align: left; }
.pagenav .pn-next { text-align: right; }
.pagenav .pn-up   { flex: 0 0 auto; text-align: center; align-self: center; }
.pagenav .pn-label {
  display: block;
  font-size: 0.7rem;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--ink-faint);
  margin-bottom: 0.1rem;
}
.pagenav .pn-spacer { flex: 1 1 0; }
@media (max-width: 34rem) {
  .pagenav { flex-wrap: wrap; }
  .pagenav .pn-up { flex: 1 1 100%; }
}

/* --- the page header -----------------------------------------------------
   The product line, the title and the subtitle.  It used to carry the
   copyright and licence too and be a page of its own; both went on
   5 September 2026 - see the comment above TITLEPAGE for the instruction.

   THE GAP BELOW IT IS THE "two blank lines" THE OWNER ASKED FOR, and it is
   written as a multiple of the body line-height rather than a round number of
   rems so that it stays two blank lines if the type size changes.  The same
   figure separates the body from the footer. */

.titlepage {
  /* ***IT IS THE SAME WIDTH AS THE BODY, AND IT WAS NOT.***  This block was
     "max-width: 40rem; margin: 0 auto" - a centred cover, which is what it was
     when .page was a two-column grid with a sidebar beside it.  In a single
     column it just left the title, the subtitle and the rule under them inset
     by 86px from the text below, and the owner saw it on the User set's first
     page: 640px against the body's 726px, so the longest title in the set
     wrapped to two lines while the paragraphs beneath it ran wider.  Eight of
     the fifty-three wrapped that way.  Nothing here is a cover any more, so
     nothing here gets its own measure. */
  max-width: none;
  margin: 0 0 calc(2 * 1.5em);
  padding: 2.5rem 0 1.25rem;
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
  margin: 0;
}

/* --- the licence block, on one page per set ------------------------------
   Same markup the title page used to carry.  It is rendered into whichever
   page holds the <!--LICENCE-BLOCK--> marker - 00a-copyright-and-licence in
   each set - and nowhere else. */

/* Body width, for the same reason as .titlepage above: it sits among ordinary
   paragraphs and a block indented from them reads as a mistake. */
.licenceblock {
  max-width: none;
  margin: 0 0 2rem;
}

.licenceblock dl.tp-meta {
  margin: 0 0 2.2rem;
  padding: 1.1rem 0;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}

.licenceblock dl.tp-meta > div {
  display: flex;
  gap: 1rem;
  padding: 0.28rem 0;
}

.licenceblock dl.tp-meta dt {
  flex: 0 0 9.5rem;
  font-size: 0.8rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--ink-faint);
  padding-top: 0.15rem;
}

.licenceblock dl.tp-meta dd {
  margin: 0;
  flex: 1;
}

.licenceblock .tp-licence p {
  font-size: 0.94rem;
  line-height: 1.55;
  color: var(--ink-soft);
  margin: 0 0 0.9rem;
  /* 06 Sep 26 - ***FULL WIDTH, LIKE EVERYTHING ELSE ON THE PAGE.***  Owner, on
     the merged set: "the description of the license on that page is not full
     width and causes several unneeded lines".  This was "max-width: 36rem"
     against a body measure of about 45rem, so the licence summary wrapped
     early and ran several lines longer than it needed to, next to paragraphs
     that did not.
     THIS IS THE .titlepage DEFECT AGAIN, one block along - that one was
     "max-width: 40rem; margin: 0 auto", a centred measure left over from the
     two-column layout, and it was corrected to none for the same reason.  A
     narrower measure reads better in isolation and reads WRONG beside text
     that is not narrowed. */
  max-width: none;
}

.licenceblock .tp-url {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.86em;
  /* "break-all" broke it after "htt".  This only breaks when the line really
     cannot hold the URL, which on a 40rem measure it can. */
  overflow-wrap: anywhere;
}

@media (max-width: 34rem) {
  .licenceblock dl.tp-meta > div { display: block; }
  .licenceblock dl.tp-meta dt { margin-bottom: 0.1rem; }
}

/* --- print -------------------------------------------------------------
   The browser IS the PDF exporter, and this block is now SHORT because the
   screen rules above already are the PDF's appearance - that was the point of
   the 5 September 2026 change.  What is left is the part that only makes sense
   on paper: point sizes, page breaks, the sheet's screen chrome removed, and
   the prev/next controls hidden.

   THE PALETTE IS NO LONGER RESET HERE AND DOES NOT NEED TO BE.  It used to be,
   because a machine in dark mode would otherwise print pale grey on white -
   every rule that read a variable kept the dark value.  There is one palette
   now and it is the printed one, so there is nothing to undo. */

@media print {

  body { background: #fff; font-size: 10.5pt; line-height: 1.45; }

  /* The sheet is a screen device: on paper the paper is the sheet. */
  .page {
    max-width: none;
    margin: 0;
    padding: 0;
    border: 0;
    box-shadow: none;
  }

  /* A "Next page" link pointing at an .html file is meaningless in a PDF.
     add_nav.py also runs after mkpdf so they are not usually there at all;
     this is the belt to that braces, for anyone printing from the browser
     after the bars have been inserted. */
  .pagenav { display: none; }

  a { text-decoration: none; }

  /* --- WHAT MUST NOT BE LEFT ALONE AT A PAGE BREAK ----------------------
     Owner, 5 September 2026, pointing at a sheet that began with a rule and
     nothing else: "also try to avoid situations like in the screen shot where
     one line, in this case a horizontal rule, is on the following page".

     THE RULE WAS AN h2's border-top, AND break-after:avoid COULD NOT HELP.
     That property keeps a heading with what FOLLOWS it; the break here fell
     INSIDE the heading's own box, between its border-top plus padding and its
     text, so the border printed at the top of the next sheet and the words
     went further down.  break-inside is the one that forbids that, and it has
     to be on the headings themselves. */
  h1, h2, h3, h4 {
    break-inside: avoid; page-break-inside: avoid;
    break-after: avoid;  page-break-after: avoid;
  }
  /* And the same defect one line at a time: a lone first or last line of a
     paragraph stranded across the break. */
  p, li, dd, dt { orphans: 3; widows: 3; }
  ul, ol, dl { break-before: avoid; page-break-before: avoid; }

  /* 06 Sep 26 - ***A LONG CODE BLOCK IS ALLOWED TO SPAN A PAGE, FOR THE SAME
     REASON THE TABLE ABOVE IS.***  Owner, on the merged Administrator set:
     "page 3 has an orphan and most the page is blank".  This is the table
     defect exactly, one element along: headings are unbreakable AND glued to
     what follows them, so an h2 with a tall pre under it could not fit in what
     was left of a sheet and BOTH moved on, leaving the rest of that page
     empty and whatever preceded them stranded.
     A listing that flows across a break is normal in a printed manual; half a
     blank sheet is not.  blockquote KEEPS the rule - they are a few lines, so
     they always fit somewhere and splitting one reads worse than moving it. */
  pre { break-inside: auto; page-break-inside: auto; }
  blockquote { break-inside: avoid; page-break-inside: avoid; }

  /* ***A TABLE IS ALLOWED TO SPAN A PAGE AND A ROW IS NOT.***  "break-inside:
     avoid" used to be on the table too, and with headings now unbreakable as
     well it produced the opposite of the defect it was there for: a heading
     and its table would not fit in what was left of a sheet, so BOTH moved on
     and left half a page blank.  These are reference tables of thirty rows;
     flowing across a break is what they are supposed to do.  The header row
     repeats at the top of each sheet the table continues onto, so a reader who
     turns the page still knows what the columns are. */
  table { break-inside: auto; page-break-inside: auto; }
  thead { display: table-header-group; }
  tr    { break-inside: avoid; page-break-inside: avoid; }

  pre, code { border-color: #ccc; }
  th { border-bottom: 1.5pt solid #000; }
  td, th { border-bottom: 0.5pt solid #999; }
  footer { border-top: 0.5pt solid #999; padding: 0.5rem 0 0; }

  /* THE PAGE HEADER IS NO LONGER A SHEET OF ITS OWN.  It used to be, and
     break-after:page is what did it; with the licence block gone it is three
     lines, and three lines on an otherwise empty sheet is a gap rather than a
     cover.  The two-line space below it is kept - the em is now the printed
     one, which is the reason it is written as a multiple of line-height. */
  .titlepage {
    max-width: none;
    margin: 0 0 calc(2 * 1.45em);
    padding: 0 0 0.8rem;
    break-inside: avoid;
    page-break-inside: avoid;
  }
  .titlepage h1.tp-title { font-size: 22pt; }
  .titlepage .tp-subtitle { font-size: 11pt; }
  .licenceblock dl.tp-meta { border-color: #999; }
  .licenceblock .tp-licence p { font-size: 9.5pt; }
}
'''


# ---------------------------------------------------------------------------
# The title page.
#
# WHY IT IS GENERATED HERE RATHER THAN WRITTEN INTO EACH MARKDOWN FILE.  There
# are fifty-three documents in the User set alone.  A copyright line pasted into
# each one is fifty-three places to update when the year, the licence or the
# release changes, and fifty-three chances for one of them to say something
# different from the rest.  The Markdown supplies the two things that differ
# per document - Title and Subtitle - and everything else comes from here.
#
# ***THE LICENCE BLOCK CAME OFF EVERY PAGE ON 5 September 2026.  OWNER, LOOKING
# AT A PDF:*** "You can remove this header (shown in the pdf) from every page.
# It should be available once for each set of documents: user, administrator and
# getting started.  After that a tag line at the bottom of each page should
# contain the copyright notices and the license name."
#
# So a page's own header is now the product line, the title and the subtitle,
# and nothing else; the copyright and the licence NAME are the footer tag line
# on every page; and the full block - the metadata table and the three-paragraph
# summary with the licence URL - is rendered ONCE PER SET, into whichever page
# carries the <!--LICENCE-BLOCK--> marker.  That is
# 00a-copyright-and-licence.md in each of the three sets.
#
# ***IT IS STILL GENERATED, WHICH IS THE WHOLE POINT.***  Writing the block into
# three markdown files instead of one template would be three places to update
# rather than fifty-three, which is better and is still wrong.  The marker keeps
# one copy of the words here and lets the set decide where it appears.
# add_nav.py asserts that EXACTLY ONE page per set carries it, so it can neither
# go missing nor appear twice.
#
# THE COVER IS NO LONGER A PAGE OF ITS OWN.  It used to break after itself so
# that browser-to-PDF gave a real page 1.  With the licence block gone it is
# three lines, and a whole sheet holding three lines is not a cover, it is a
# gap.  It now sits at the top of the first page with the two-line gap below it
# that the same instruction asked for.
# ---------------------------------------------------------------------------

COPYRIGHT = 'Copyright © 2026 Donald Montaine'

LICENCE_NAME = ('Creative Commons Attribution-ShareAlike 4.0 International '
                '(CC BY-SA 4.0)')

# 06 Sep 26 - THE SHORT FORMS, FOR THE PER-PAGE WEB FOOTER ONLY.  Owner's
# ruling.  The footer is a tag line repeated on every page and the full licence
# title is clutter there.  THE GRANT IS UNAFFECTED: the full name still appears
# in the two places that actually make it - the licence block's "Licence" row
# below, and 00a-copyright-and-licence, which is a whole page and one per set.
#
# THE MERGED PDF DOES NOT USE THIS FOOTER AT ALL.  One PDF per set carries the
# copyright once in its front matter and a running footer drawn by printToPDF's
# footerTemplate, where the page numbers live - so the two deliverables stopped
# competing over one string.  This one belongs to the WEB page, where each page
# stands alone and a reader may arrive on it from a search engine.
COPYRIGHT_SHORT = '&copy; Donald Montaine'
LICENCE_SHORT   = 'CC BY-SA'

LICENCE_URL = 'https://creativecommons.org/licenses/by-sa/4.0/'

LICENCE_SUMMARY = [
    ('You are free to <strong>share</strong> this document - copy and '
     'redistribute it in any medium or format - and to <strong>adapt</strong> '
     'it - remix, transform and build upon it - for any purpose, including '
     'commercially.'),
    ('Two conditions apply. <strong>Attribution:</strong> you must give '
     'appropriate credit, provide a link to the licence, and indicate if '
     'changes were made. <strong>ShareAlike:</strong> if you remix, transform '
     'or build upon this document, you must distribute what you produce under '
     'the same licence. You may not add legal terms or technological measures '
     'that restrict others from doing anything the licence permits.'),
    ('This is a summary and not a substitute for the licence itself. The '
     'complete text is at <span class="tp-url">' + LICENCE_URL + '</span>.'),
]

TITLEPAGE = '''<section class="titlepage">
<p class="tp-product">@PRODUCT@ <span>@VERSION@</span></p>
<h1 class="tp-title">@TITLE@</h1>
@TP_SUBTITLE@
</section>
'''

# The marker a page puts in its Markdown to ask for the full block.  It is an
# HTML comment so that it is invisible if anything ever renders the Markdown
# without mkdoc, and greppable so "which page has it" is one command.
LICENCE_MARKER = '<!--LICENCE-BLOCK-->'

LICENCE_BLOCK = '''<section class="licenceblock">
<dl class="tp-meta">
<div><dt>Released with</dt><dd>@PRODUCT@ @VERSION@</dd></div>
<div><dt>Copyright</dt><dd>@COPYRIGHT@</dd></div>
<div><dt>Licence</dt><dd>@LICENCE_NAME@</dd></div>
</dl>
<div class="tp-licence">
@LICENCE_SUMMARY@
</div>
</section>
'''


# THE TWO MARKERS ARE WHERE add_nav.py PUTS THE PREV/NEXT BARS, and they are
# comments rather than an anchor guessed from the markup.  add_nav runs AFTER
# mkpdf, deliberately, so the bars are not in the PDFs; that means mkdoc cannot
# write them itself, and add_nav needs somewhere reliable to put them.  Both
# scripts REFUSE a page missing either marker rather than inserting one bar and
# reporting two.
#
# THE BOTTOM MARKER SITS BEFORE <footer>, NOT INSIDE IT.  add_nav used to
# insert before </footer>, which put the page controls UNDERNEATH the copyright
# line - the last thing on the page was the licence and the reader had to scroll
# back up past it to find "Next".
#
# THE MASTHEAD AND THE SIDEBAR ARE GONE.  Both were hidden in @media print
# already, which is to say neither was ever in the PDF; the 5 September 2026
# instruction was to make the screen match, so they are no longer emitted at
# all rather than emitted and hidden.
#
# THE FOOTER IS INSIDE .page NOW.  It used to sit outside, so on screen it was
# a strip below the sheet - and add_nav inserts the bottom bar before
# </footer>, which would have put the page controls off the paper.
#
# ***THE FOOTER IS THE TAG LINE THE OWNER ASKED FOR, AND "Generated from
# <file>.md" HAS GONE FROM IT.***  It is the only place the copyright and the
# licence name now appear on an ordinary page, so it carries both and nothing
# else.  The source file name was the one thing on it a reader could not use.

PAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@TITLE@ - @PRODUCT@</title>
<style>@CSS@</style>
</head>
<body>
<div class="page">
<!--PAGENAV-TOP-->
@TITLEPAGE@
<main>
@BODY@
</main>
<!--PAGENAV-BOTTOM-->
<footer>@PRODUCT@ @VERSION@ &middot; @COPYRIGHT_SHORT@ &middot; License: @LICENCE_SHORT@</footer>
</div>
</body>
</html>
'''


def render(src, product, version):
    """Markdown text -> (title, subtitle, toc html, body html)."""
    md = markdown.Markdown(extensions=['extra', 'meta', 'sane_lists',
                                       'toc'],
                           extension_configs={'toc': {'permalink': '#',
                                                      'toc_depth': '2-3'}})
    body = md.convert(src)
    meta = getattr(md, 'Meta', {}) or {}
    title = ' '.join(meta.get('title', [])) or '(untitled)'
    subtitle = ' '.join(meta.get('subtitle', []))
    return title, subtitle, md.toc, body


def build(path, out_dir, product, version):
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()

    # An editor that saves UTF-8 with a BOM leaves it as the first character
    # of the first heading, where it renders as a stray glyph rather than an
    # error.  It is written as chr() rather than as the character itself so that
    # a byte-scan of THIS file does not report a BOM of its own - it did.
    if src[:1] == chr(0xFEFF):
        src = src[1:]
        sys.stdout.write('  note: stripped a UTF-8 BOM from %s\n'
                         % os.path.basename(path))

    title, subtitle, toc, body = render(src, product, version)

    if not body.strip():
        raise RuntimeError('%s rendered to an empty document' % path)

    # THE TOC IS STILL COMPUTED AND IS NO LONGER RENDERED.  The sidebar went
    # with the 5 September 2026 change; the "toc" extension stays on because it
    # is what puts an id="" on every heading, and checklinks.py verifies every
    # "#..." link against those ids.  Turning the extension off to remove the
    # sidebar would have broken every anchor in the tree silently.  The count is
    # still reported, as the anchors-per-page figure.
    sub_html = ''
    if subtitle:
        sub_html = '<p class="tp-subtitle">%s</p>' % html.escape(subtitle)

    titlepage = TITLEPAGE.replace('@TP_SUBTITLE@', sub_html)

    # THE MARKER SURVIVES THE MARKDOWN CONVERTER AS AN HTML COMMENT, and it is
    # matched against the RENDERED body rather than the source so that a marker
    # the converter swallowed - inside a code fence, say - is not counted.
    wants_licence = LICENCE_MARKER in body
    if wants_licence:
        # SUBSTITUTED HERE, NOT LEFT TO THE PAGE CHAIN BELOW.  The chain
        # replaces @BODY@ LAST, so any @PLACEHOLDER@ arriving inside the body
        # had already missed its turn: the first render of the licence page
        # printed "@PRODUCT@ @VERSION@" and "@COPYRIGHT@" to the screen.  The
        # block is completed before it goes anywhere near the body, so it no
        # longer depends on the order of a list of .replace() calls.
        block = (LICENCE_BLOCK
                 .replace('@LICENCE_SUMMARY@',
                          '\n'.join('<p>%s</p>' % s for s in LICENCE_SUMMARY))
                 .replace('@PRODUCT@', html.escape(product))
                 .replace('@VERSION@', html.escape(version))
                 .replace('@COPYRIGHT@', COPYRIGHT)
                 .replace('@LICENCE_NAME@', LICENCE_NAME))
        body = body.replace(LICENCE_MARKER, block)

    page = (PAGE
            .replace('@CSS@', CSS)
            .replace('@TITLEPAGE@', titlepage)
            .replace('@PRODUCT@', html.escape(product))
            .replace('@VERSION@', html.escape(version))
            .replace('@TITLE@', html.escape(title))
            .replace('@COPYRIGHT_SHORT@', COPYRIGHT_SHORT)
            .replace('@COPYRIGHT@', COPYRIGHT)
            .replace('@LICENCE_SHORT@', LICENCE_SHORT)
            .replace('@LICENCE_NAME@', LICENCE_NAME)
            .replace('@BODY@', body)
            .replace('@SOURCE@', html.escape(os.path.basename(path))))

    # The title page is the one part of this file a reader would notice missing,
    # and a template typo would drop it silently - the page would still render.
    if 'class="titlepage"' not in page:
        raise RuntimeError('%s rendered without a title page' % path)

    # EVERY page carries the copyright and the licence, in the footer tag line.
    # Only the page that asked for the block carries the licence URL, and it
    # must - a licence page with no link to the licence is the one failure this
    # whole arrangement could produce quietly.
    #
    # 06 Sep 26 - THE SHORT FORMS ARE WHAT THE FOOTER HOLDS NOW, so this tests
    # those.  It used to require COPYRIGHT and LICENCE_NAME, and it CAUGHT THE
    # SHORTENING THE MOMENT IT LANDED - which is the guard doing its job, not a
    # nuisance: its own comment above says a template typo would drop the footer
    # silently.  The full LICENCE_NAME is still asserted below, on the one page
    # that makes the grant, which is where it now has to appear.
    if COPYRIGHT_SHORT not in page or LICENCE_SHORT not in page:
        raise RuntimeError('%s rendered without the copyright or the licence '
                           'in its footer' % path)
    if wants_licence and LICENCE_NAME not in page:
        raise RuntimeError('%s asked for the licence block and rendered '
                           'without the full licence name' % path)
    if wants_licence and LICENCE_URL not in page:
        raise RuntimeError('%s asked for the licence block and rendered '
                           'without the licence URL' % path)

    # ***NO @PLACEHOLDER@ MAY SURVIVE, AND THIS IS THE CLASS FIX RATHER THAN
    # THE ONE ABOVE.***  Fixing the licence block's own substitution repairs
    # that block; this catches the next template that is expanded in the wrong
    # order, or a placeholder added to a template and not to the chain.  An
    # unsubstituted @NAME@ renders as visible text and nothing else looks at
    # it - the licence page shipped "@COPYRIGHT@" past two content assertions
    # that both passed, because the real copyright was in the footer.
    left = sorted(set(re.findall(r'@[A-Z][A-Z0-9_]*@', page)))
    if left:
        raise RuntimeError('%s rendered with unsubstituted placeholder(s): %s'
                           % (path, ' '.join(left)))
    # The same argument for the marker add_nav.py needs: a page without it gets
    # no top bar and looks exactly like a page that has one and did not need it.
    for marker in ('<!--PAGENAV-TOP-->', '<!--PAGENAV-BOTTOM-->'):
        if marker not in page:
            raise RuntimeError('%s rendered without the %s marker'
                               % (path, marker))

    stem = os.path.splitext(os.path.basename(path))[0]
    out = os.path.join(out_dir, stem + '.html')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(page)
    return out, title, len(page), toc.count('<a ')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--in', dest='inputs', nargs='+', required=True,
                    metavar='PATH', help='.md files, or directories of them')
    ap.add_argument('--out', required=True, metavar='DIR')
    ap.add_argument('--product', default='SD Core for Windows')
    ap.add_argument('--version', default='W1.0-0')
    args = ap.parse_args()

    sources = []
    for item in args.inputs:
        if os.path.isdir(item):
            sources += [os.path.join(item, n) for n in sorted(os.listdir(item))
                        if n.lower().endswith('.md')]
        else:
            sources.append(item)

    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)

    # An instrument prints what it DID (CLAUDE.md).  The resolved paths matter
    # more than they look: --in docs/sample from the wrong directory finds no
    # .md at all, and a converter that cheerfully writes nothing is exactly
    # the "passes because it did nothing" failure the rule exists to stop.
    sys.stdout.write('mkdoc: markdown %s, python %s\n'
                     % (markdown.__version__, sys.version.split()[0]))
    sys.stdout.write('mkdoc: out  %s\n' % out_dir)
    for s in sources:
        sys.stdout.write('mkdoc: in   %s\n' % os.path.abspath(s))

    if not sources:
        sys.stderr.write('mkdoc: no .md files found - nothing rendered.\n')
        return 1

    for s in sources:
        out, title, size, anchors = build(s, out_dir, args.product,
                                          args.version)
        sys.stdout.write('mkdoc: wrote %s  "%s"  %d bytes, %d anchors\n'
                         % (out, title, size, anchors))
        with open(out, 'r', encoding='utf-8') as f:
            if 'class="licenceblock"' in f.read():
                sys.stdout.write('mkdoc:       ^ carries the licence block\n')

    sys.stdout.write('mkdoc: %d page(s).\n' % len(sources))
    return 0


if __name__ == '__main__':
    sys.exit(main())
