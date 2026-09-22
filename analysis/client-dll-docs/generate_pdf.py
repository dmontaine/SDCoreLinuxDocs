#!/usr/bin/env python3
# generate_pdf.py - renders USER_GUIDE.md to the shipped PDF.
#
# Modifications Copyright (c) 2026 Donald Montaine
#
# This library is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser
# General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library.  If not, see <https://www.gnu.org/licenses/>.
#
# Linking exception (additional permission under GNU LGPL version 3
# section 7): as a special exception, the copyright holders give you
# permission to link this library with independent modules to produce an
# executable, regardless of the license terms of these independent modules,
# and to copy and distribute the resulting executable under terms of your
# choice, provided that you also meet, for each linked independent module,
# the terms and conditions of the license of that module.  An independent
# module is a module which is not derived from or based on this library.

"""Regenerate SDCLILIB_Windows_DLL_Documentation.pdf from USER_GUIDE.md.

Pure-Python pipeline (no pandoc / wkhtmltopdf needed):
    Markdown --(python-markdown)--> HTML --(xhtml2pdf)--> PDF

Dependencies (one-time):
    python -m pip install markdown xhtml2pdf

Usage:
    python generate_pdf.py            # USER_GUIDE.md -> SDCLILIB_Windows_DLL_Documentation.pdf
    python generate_pdf.py in.md out.pdf
"""
import sys
from pathlib import Path

import markdown
from xhtml2pdf import pisa

HERE = Path(__file__).resolve().parent
DEFAULT_SRC = HERE / "USER_GUIDE.md"
DEFAULT_OUT = HERE / "SDCLILIB_Windows_DLL_Documentation.pdf"

CSS = """
@page { size: letter; margin: 2.0cm 1.8cm 2.0cm 1.8cm; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 10.5pt;
       line-height: 1.35; color: #1a1a1a; }
h1 { font-size: 20pt; color: #14315c; margin: 0 0 10pt 0;
     padding-bottom: 4pt; border-bottom: 2px solid #14315c; }
h2 { font-size: 15pt; color: #14315c; margin: 16pt 0 6pt 0;
     padding-bottom: 2pt; border-bottom: 1px solid #b9c6d8;
     -pdf-keep-with-next: true; }
h3 { font-size: 12.5pt; color: #1f4e79; margin: 12pt 0 4pt 0;
     -pdf-keep-with-next: true; }
h4 { font-size: 11pt; color: #1f4e79; margin: 10pt 0 4pt 0; }
p  { margin: 0 0 6pt 0; }
a  { color: #1f4e79; text-decoration: none; }
ul, ol { margin: 0 0 6pt 0; }
li { margin: 0 0 2pt 0; }
strong { color: #111; }

code { font-family: "Courier New", Courier, monospace; font-size: 9pt;
       background-color: #f0f2f5; color: #9b1c1c; padding: 0 2px; }
pre { font-family: "Courier New", Courier, monospace; font-size: 8.5pt;
      background-color: #f4f6f8; border: 1px solid #d9dee5;
      padding: 6pt 8pt; margin: 0 0 8pt 0; color: #17242f; }
pre code { background-color: transparent; color: #17242f; padding: 0; }

table { border: 1px solid #c2cbd6; margin: 0 0 8pt 0; width: 100%; }
th { background-color: #e8edf3; color: #14315c; font-size: 9pt;
     border: 1px solid #c2cbd6; padding: 3pt 5pt; text-align: left; }
td { border: 1px solid #d9dee5; padding: 3pt 5pt; font-size: 9pt;
     vertical-align: top; }
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{css}</style></head>
<body>{body}</body></html>"""


def build(src: Path, out: Path) -> None:
    text = src.read_text(encoding="utf-8")
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "toc", "attr_list"],
        output_format="html5",
    )
    html = HTML_TEMPLATE.format(css=CSS, body=body)
    with out.open("wb") as fh:
        result = pisa.CreatePDF(html, dest=fh, encoding="utf-8")
    if result.err:
        raise SystemExit(f"PDF generation reported {result.err} error(s)")
    print(f"Wrote {out} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUT
    build(src, out)
