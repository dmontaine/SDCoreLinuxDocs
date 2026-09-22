Title: Questions on the first document set
Subtitle: Answered 26 Aug 2026. Two are still open — they are first.

***THIS FILE IS NOT PART OF THE TESTER SET.*** It is the review list for the
first document set, with your answers recorded against each question and what
was done about them. Delete or move it before the set goes out.

**Sixteen of the eighteen are answered and applied.** The two below are not.

---

## STILL OPEN

### 7. The `limitssh` question — you said you were not sure what was being proposed

**Here is the whole of it, and then four ways to settle it.**

The installer offers a task, ***ticked by default***, called *"Limit ssh to SD
users and administrators"*. When it runs it adds two lines to
`C:\ProgramData\ssh\sshd_config`, inside its own fenced block:

```
AllowGroups <sdssh> <the administrators group>
ForceCommand "C:\Program Files\SD\usr\bin\sd.exe"
```

The original is copied to `sshd_config.before-sd` first, and uninstalling SD
strips the block again.

***THE PART THAT IS A QUESTION.*** `allow-ssh-groups.ps1` refuses to touch an
`sshd_config` that **already** has an `AllowGroups`, `AllowUsers`, `DenyGroups`
or `DenyUsers` line — that is somebody's policy, and merging into it blind
either widens it or locks its author out. **But a stock `sshd_config` has none
of those lines.** So on a machine where somebody had already installed OpenSSH
and left it at its defaults, the ticked-by-default task reconfigures an ssh
server SD did not install, and every ssh session on that machine — not only
SD's — lands in SD.

**Why it is ticked rather than offered.** The opposite default was tried and
cost a fault: with no `ForceCommand`, an account created as ssh-only got a
**PowerShell prompt** instead of SD. Found on this machine, 21 Aug 2026.

**Four ways to settle it.** No recommendation; the page changes to match
whichever you pick.

| | |
|---|---|
| **a. Leave it** | ticked, and it applies to a stock config. Simplest, and an ssh-only account is always safe. The cost is the one above |
| **b. Tick it only when SD installed the ssh server** | a pre-existing server gets the task unticked. An administrator who wants the lock-down has to notice it |
| **c. Refuse a stock config too** | treat *no policy line* the same as *somebody's policy*: never touch a server SD did not install, and print the two lines for them to add by hand |
| **d. Leave it ticked and say more in the wizard** | the page names scp and sftp today; it could also name the two lines and the backup file, so the tick is an informed one |

### 14. Remote administration over ssh — you did not answer this one

A local account arriving over the network gets a **filtered** token, so an SD
administrator over ssh may be unable to elevate, and so unable to reach SDSYS.
***THIS HAS NEVER BEEN MEASURED.***

Page 12 currently says exactly that, including that it is unmeasured.

**Do you want that stated to testers, or held back until somebody measures
it?** Leaving it in invites a tester to measure it for us, which is the
argument for; the argument against is that an unmeasured caveat in a document
reads as a defect report.

---

## ANSWERED, AND WHAT WAS DONE

| | Your answer | What changed |
|---|---|---|
| **1.** the changelog sends users to an `sd.conf` that does not exist | silent fix | `sdsys/changelog` now reads `C:\ProgramData\SD\sd.conf`. No correction entry. **A second wrong statement in the same entry was fixed with it** — see 8 |
| **2.** *"do not document missing features"* versus *"tell them what is gone"* | the interpretation was correct | Page 14 stays a list of removals with what to use instead, describing none of them |
| **3.** where the set lives | its own GitHub repository, without the no-binaries rule | `SDCoreWindowsDocs`, now at `C:\Users\dmont\Projects\SD Core for Windows 1.0-0 Docs` with `Testing`, `User` and `Technical` sets |
| **4.** three topics not on your list | all three written | Now pages 02, 03 and 10 |
| **5.** `create.account other` | do not document | Left out of the account-types page. Its own header calls it *"maintained for backwards compatibility"*, and it needs the accounts record hand-edited |
| **6.** `batch.jobs` — scheduled jobs | a feature; give it its own page | **New page 04, Scheduled jobs**, and the set renumbered to a flat `00`–`14`. The hardening page keeps a pointer |
| **8.** `sdapi` group wording | *"which an account joins only when you give it API access"* | Changed on page 09 **and in the changelog**, which carried the old wording. The old form contradicted the sentence after it: `create.account user fred api` joins the group for you (`CREATEA:1428`) |
| **9.** product name | confirmed | *SD Core for Windows* in titles and the header bar, *SD Core* in prose |
| **10.** version string | `W1.0-0` | Page 00 now tells a tester to quote `W1.0-0` and says where to find it — the header bar, the installer file name, and `sd --version` |
| **11.** verbs or commands | the methodology was correct | *Verbs* for what a VOC contains, *commands* for what a person types |
| **12.** lower case | **bold lower case for verbs** | 198 verb names across the set are now bold. The list is not hand-written: it is read from `sdsys/newvoc` and the two `TIER.*` records, so it cannot drift from what a VOC holds |
| **13.** the Turkish and Azeri fix | leave as written | Page 12 describes it from the changelog |
| **15.** does the toolchain move | move it — possibly to several machines | `mkdoc.py` and `mkpdf.ps1` are now in `tools\` here, and both are **out of** `assert-current.ps1`'s `$neverShipped`. A clone needs no checkout of `sd4windows` |
| **16.** are the PDFs tracked | generated after a change, and only the ones that changed | `.gitignore` keeps `*.html`, `*.pdf` and `*.zip` out. Two deliverables eventually — a PDF download and the pages on a web site — both built from the Markdown at release time |
| **17.** a release step | a short script | `tools\release.ps1`. It renders only what changed, **refuses to zip if any PDF is older than its Markdown**, and prints the SHA256 |
| **18.** how the client libraries are published | a client installer carrying the DLLs, the documentation and related utilities; no source; source on GitHub, referenced from a `docs` subdirectory the installer creates | Page 10 says that, and says plainly that **it is not what W1.0-0 ships** — it needs an installer change that has not been made |

## Notes on two of those

**On 12, and it is worth knowing before the next set is written.** A verb is
bold only when the whole code span is the verb name. `create.account user fred
api` is a **command** somebody types and is left plain, which is question 11's
distinction made visible. Upper-case spans are left alone too — page 11 is
about case folding and its capitals are the demonstration.

**On 16 and 17 together.** Moving the documentation out of `sd4windows` gave up
the only automatic check that a page still matched the product. `release.ps1`
does not replace that — nothing can, short of a person re-reading the pages —
but it does close the second gap the move opened, which is shipping a PDF
rendered before the last fix to its Markdown.
