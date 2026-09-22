# Client DLL documentation — salvaged for review

**Placed here 4 Sep 2026, for review and inclusion by PRE_RELEASE task 80
where appropriate.** Owner's instruction, the same day: *"documentation can be
added to our documentation library for review and inclusion by task 80 where
appropriate."*

Nothing here is a finished document set. It is the client-library
documentation that existed in the two client repositories, kept because those
repositories were deleted.

## Why it moved

`sd4windows` PRE_RELEASE **161**: one source produced five client DLLs and the
build made only one of them, so the other four were hand-built in two sibling
repositories — `winsdclilib` (64-bit) and `sdclilib32` (32-bit). When that was
measured they were **fifteen days stale**, with the older copy winning on
`PATH`.

`make sd` now builds all four, and the installer ships them in
`C:\Program Files\SD\usr\clients\client64` and `...\client32`. The two client
installers went with the ruling, and on 4 Sep 2026 the owner ruled the two
repositories deleted as well: *"delete both ..\winsdclilib and ..\sdclilib32 —
I will delete the github repositories."*

## What each file is

| file | provenance |
|---|---|
| `USER_GUIDE.md` | the **current** copy, from `sd4windows/sdb_ai/sd64/gplsrc/sdclilib/`. That copy stays in `sd4windows`; this is a duplicate for review, not a rescue |
| `README-client-64bit.md` | likewise the current `gplsrc/sdclilib/README.md` |
| `README-client-32bit-qm.md` | `sdclilib32/README.md`, 248 lines. ***UNIQUE — it existed nowhere else***, and is the only written account of the 32-bit/QMClient build: why the export table answers to both name sets, why the DLL is `-static-libgcc`, and why `qmclilib.dll` is a name that must not move |
| `SDCLILIB_Windows_DLL_Documentation.pdf` | ***UNIQUE.*** Rendered from the 64-bit `USER_GUIDE.md` on 20 Aug 2026, so it is **older than the guide beside it** — treat the Markdown as authoritative |
| `generate_pdf.py` | ***UNIQUE.*** What rendered that PDF. `sd4windows/sdb_ai/sd64/gplbld/mkdoc.py` is this repository's own renderer; whether either survives is task 80's call |
| `sd_connect.c` | ***UNIQUE, AND NOT DOCUMENTATION.*** A command-line diagnostic that opens a session through the 32-bit DLL. Kept only because deleting the repository would have destroyed it; if it is wanted it belongs in `sd4windows`, not here |

## The one thing a reviewer must not miss

***THE TWO GUIDES CONTRADICTED EACH OTHER ABOUT `SDConnectLocal`, AND AFTER 161
BOTH ARE WRONG.***

- `gplsrc/sdclilib/USER_GUIDE.md:11` — *"connects to SD on this machine and
  **is** provided"*
- `winsdclilib/USER_GUIDE.md:11` (the deleted mirror) — *"The Windows DLL does
  not provide `SDConnectLocal`"*

The mirror's sentence was written before the function was implemented, so it
was stale rather than considered — but it is accidentally closer to what a
reader needs.

**What is actually true, measured:** `sdclilib.c:1409-1421` takes the DLL's own
module path and appends `\sd.exe`, so `SDConnectLocal()` works **only from a
directory that also holds `sd.exe`**. After 161 that is `usr\bin` and nowhere
else — a DLL copied out of `usr\clients\client64` to an application directory
or to `windows\system32` can do everything **except** connect locally. The
32-bit pair never had it: `QMConnectLocal` is a stub that always fails.

It costs nothing in practice — owner, 4 Sep 2026: *"windows applications
written for sd are always going to use the API to connect, so will be logging
in to localhost or 127.0.0.1"* — but the sentence in the guide has to say so.
`sd4windows` PRE_RELEASE **163** carries this, and also asks whether
`SDConnectLocal` should be removed from the API outright.
