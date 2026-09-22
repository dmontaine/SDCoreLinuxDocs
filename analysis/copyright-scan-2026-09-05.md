Title: Copyright scan — our documentation against the OpenQM 2.6-6 help
Subtitle: Whether the "reference only, do not quote extensively" rule was followed. Measured, with a positive control.

This file is the record of a copyright compliance scan run on 5 Sep 2026. It
is not part of any set and does not ship. It exists so the question does not
have to be re-answered from scratch, and so that the next person can re-run the
measurement rather than trust this page.

**Why it was asked.** Some of this documentation was originally drafted by a
different AI, working with the OpenQM 2.6-6 help as a reference. The company
behind that documentation is gone and its copyright status is ambiguous, so the
owner set a rule at the time: **use it as a reference, do not quote it
extensively.** This scan asks whether that rule was actually followed.

**It is a compliance check on our own work**, not an assessment of anyone
else's rights. Nothing here is legal advice, and the ambiguity of the source's
status is unchanged by it.

---

## What was compared

| | |
|---|---|
| Reference corpus | OpenQM 2.6-6 help, local copy, **495 pages / 149,334 words** |
| Our documentation | **77 markdown pages** — GettingStarted, User, Administrator, and the `analysis/` working files |
| Coverage | every one of our pages against every reference page |

The reference copy is the same material published at `scarl.cdmiweb.com`. That
site was tried first and its TLS chain does not verify, so a local copy was
used instead; the local copy is what the numbers below describe.

## The method, and why it is shaped this way

Seed on an exact **N-word window**, then extend each match greedily in both
directions, so what is reported is the **full length** of a shared run rather
than the window that found it. Comparison is on lower-cased words with runs of
whitespace collapsed. **Punctuation is kept** — dropping it manufactures
matches that are not in either text.

Two passes, because they answer different questions:

- **Prose** (default). Fenced code blocks and inline code are stripped from our
  side. A shared command example is not copied prose, and leaving it in buries
  the finding that matters.
- **With code** (`withcode`). Everything kept. This asks whether *syntax*
  matches, which is a different question with a different answer — see below.

### The positive control is the part that makes the result mean anything

***A SCAN THAT REPORTS ZERO AND A SCAN THAT LOADED NOTHING PRINT THE SAME
THING.*** Before believing any zero, a real 25-word passage was taken **from
the reference corpus** and planted in a file shaped like one of ours. The
matcher was required to find it.

It did: 25 words, at full length, naming the source page it came from. The
zeros below are therefore measurements rather than silence.

---

## Result — prose

| Seed | Runs found | Longest run |
|---|---|---|
| 8 words | **0** | — |
| 6 words | 28 | 7 words |
| 5 words | 127 | 7 words |

***NO EIGHT-WORD SEQUENCE OF PROSE IS SHARED ANYWHERE.*** The longest run in
the whole corpus is **seven words**, and every run at that length is
unavoidable technical English — the shape of *"is greater than or equal to"*,
or a phrase naming a field in a dictionary record. These are not copyrightable
expression: they are the only natural way to say the thing, and several are
domain terms with no synonym available.

At a five-word seed the count rises to 127 and the longest run does not move.
That is the signature of independent writing about the same subject: many short
collisions, no long ones.

## Result — including code

Four runs of eight words or more, and **all four are functional rather than
expressive**:

| Length | What it is |
|---|---|
| 10 words | a canonical SD Basic type-forcing idiom, with its trailing comment |
| 10 words | the paired idiom for the other direction |
| 9 words | a client-API function signature |
| 8 words | the standard `READNEXT` select-list loop |

The signature **must** match: SD implements the same API, so an identical
declaration is compatibility, not copying. The `READNEXT` loop is the idiomatic
form in every MultiValue dialect. Neither is a choice anyone made.

### The one judgment call, and why it resolves

The two idiom lines share a **four-word trailing comment** as well as the code.
That is the only place in 77 pages where shared wording sits next to shared
code, so it was read in context rather than counted.

The surrounding explanation in
`User/markdown/40-sd-programming-tutorial.md` — why conversion happens on use
rather than on assignment, and what each line changes — **scored zero
overlap**. The same language behaviour is documented, because it is real; the
canonical example is the canonical example; and the prose around it was written
independently. ***THAT IS THE RULE WORKING, NOT A BREACH OF IT.***

---

## Conclusion

**The rule was followed.** There is no extensive quotation, and nothing that
reads as borderline. The documentation describes the same product family as its
reference and shares almost none of its wording.

## What this does NOT establish

***IT DETECTS VERBATIM REUSE AND NOTHING ELSE.*** It cannot see close
paraphrase, and it cannot see structural copying — the same section order with
the same worked examples reworded.

Nothing in the results *suggests* either: a paraphrased page normally still
leaks some eight-word runs, and none did. But that is an inference from an
absence, not a measurement, and it should not be quoted as one. A paraphrase
check is a different and much fuzzier exercise, and it has not been done.

## Re-running it

The two scripts are in `analysis/copyright-scan/`, and need only Python and a
local copy of the reference help.

```
python analysis/copyright-scan/control.py <qmhelp-dir> ./ctlfixture
python analysis/copyright-scan/overlap.py <qmhelp-dir> ./ctlfixture 8
```

The control must report a found run before any real result is believed. Then:

```
python analysis/copyright-scan/overlap.py <qmhelp-dir> . 8
python analysis/copyright-scan/overlap.py <qmhelp-dir> . 8 withcode
```

`overlap.py` refuses and exits 2 if either side is empty, because a comparison
that examined nothing must not report that it found nothing.

**This page does not match itself, and that was checked rather than assumed.**
It quotes a few of the short generic phrases it reports, so it is a candidate
for matching the reference corpus on its own account. Re-running with it in
place gives **78 pages, 0 runs at seed 8, and 28 at seed 6 — the same 28 as
before it existed.** Keeping punctuation is what does it: a phrase quoted here
carries its quotation marks into the comparison and stops matching. Had it
matched, the honest fix would be to exclude this file by name and say so, not
to drop the punctuation rule that keeps the rest of the result truthful.
