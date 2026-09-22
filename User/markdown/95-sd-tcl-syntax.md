Title: SD TCL - Syntax
Subtitle: Every verb you can type, alphabetically, with its syntax and nothing else.

A lookup card, and nothing else. If you know which verb you want and
have forgotten its arguments, it is here. If you want to know what it
*does*, the subject documents are where that lives.

*Italics* mark something you supply, **bold** a word typed as it stands,
braces an optional part, and a vertical bar separates alternatives. SD
folds case, so any of this may be typed in either case.

> **This page is generated, and it is checked for completeness rather
> than proof-read for it.** The roster is computed from SD's own VOC:
> every verb record in `newvoc`, plus the ones only `voc_template`
> has, which is **144** verbs, and `tools/mktclsyntax.py` refuses to
> write the page if any of them has no line. The shapes come from the
> subject documents, where each verb is described in full.

**The "who" column is the VOC, not an opinion.** It is computed by
reading `newvoc` and `voc_template` directly, so it cannot drift from
what an account actually gets. **A verb your account does not have is
not refused — the name is simply not recognised.**

| | | |
|---|---|---|
| **every account** | 129 verbs | `newvoc`, identical for every ordinary account |
| **SDSYS only** | 15 more | in `voc_template` but not `newvoc` |

## The verbs

| | syntax | who |
|---|---|---|
| **`!`** | **`!`** *command* |  |
| **`abort`** | **`abort`** {*message*} |  |
| **`alias`** | **`alias`** *command* *target* |  |
| **`analyse.file`** | **`analyse.file`** {**`dict`**} *file* {**`statistics`**} {**`lptr`**} |  |
| **`analyze.file`** | **`analyze.file`** — the same verb as **`analyse.file`** |  |
| **`autologout`** | **`autologout`** {*minutes*} |  |
| **`basic`** | **`basic`** {*file*} *record* {*record* …} |  |
| **`bell`** | **`bell on`** | **`off`** |  |
| **`break`** | **`break on`** | **`off`** | **`on user`** *n* |  |
| **`build.index`** | **`build.index`** *file* *field* … | **`all`** |  |
| **`catalog`** | **`catalog`** {*file* {*call.name*}} {*program*} {**`local`** | **`global`** | **`pcode`**} {**`no.xref`**} |  |
| **`catalogue`** | **`catalogue`** — the same verb as **`catalog`** |  |
| **`cd`** | **`cd`** {**`dict`** | **`data`**} *file* {*i-type* …} {**`no.query`**} {**`no.page`**}  ·  **`cd local`**  ·  **`cd all`** |  |
| **`clean.account`** | **`clean.account`** | S |
| **`clear.abort`** | **`clear.abort`** |  |
| **`clear.data`** | **`clear.data`** |  |
| **`clear.file`** | **`clear.file`** {**`data`** | **`dict`**} *file* |  |
| **`clear.input`** | **`clear.input`** |  |
| **`clear.locks`** | **`clear.locks`** {*n*} | S |
| **`clear.prompts`** | **`clear.prompts`** |  |
| **`clear.select`** | **`clear.select`** {*list.no*} |  |
| **`clear.stack`** | **`clear.stack`** |  |
| **`cleardata`** | **`cleardata`** — the same verb as **`clear.data`** |  |
| **`clearinput`** | **`clearinput`** — the same verb as **`clear.input`** |  |
| **`clearprompts`** | **`clearprompts`** — the same verb as **`clear.prompts`** |  |
| **`clearselect`** | **`clearselect`** — the same verb as **`clear.select`** |  |
| **`clr`** | **`clr`** |  |
| **`cname`** | **`cname`** *old.file* **`to`** *new.file* |  |
| **`como`** | **`como on`** {*record*} | **`off`** | **`pause`** | **`resume`** |  |
| **`compile.dict`** | **`compile.dict`** — the same verb as **`cd`** |  |
| **`config`** | **`config`** {**`lptr`** | **`gpl`** | **`contrib`** | *param* *value*} | S |
| **`configure.file`** | **`configure.file`** {**`dict`**} *voc.name* {*parameters*} | **`default`** |  |
| **`copy`** | **`copy from`** {**`dict`**} *src* {**`to`** {**`dict`**} *tgt*} {*id* …} {**`(options`**} |  |
| **`copy.list`** | **`copy.list`** *list* {**`,`***new*} {**`from`** *src*} {**`to`** *tgt*} {*options*} |  |
| **`copyp`** | **`copyp`** {**`dict`**} *file* *id* … {**`(options`**} |  |
| **`count`** | **`count`** {**`dict`**} *file* {*selection*} |  |
| **`create.account`** | **`create.account user`** *name* {**`ssh`** | **`api`** | **`both`** | **`none`**} {**`no.query`**}  ·  **`create.account group`** *name* {**`no.query`**}  ·  **`create.account other`** *name* *pathname* {**`no.query`**} | S |
| **`create.file`** | **`create.file`** {**`dict`**} *voc.name* {**`directory`**} {*parameters*} |  |
| **`create.index`** | **`create.index`** *file* *field* … {**`no.nulls`**} {**`pathname`** *path*} |  |
| **`cs`** | **`cs`** — the same verb as **`clr`** |  |
| **`ct`** | **`ct`** {**`dict`**} *file* {*id* … | **`*`**} {**`(options`**} |  |
| **`date`** | **`date`** | **`internal`** | *n* | *date* |  |
| **`date.format`** | **`date.format on`** | **`off`** | **`display`** |  |
| **`debug`** | **`debug`** |  |
| **`delete`** | **`delete`** {**`dict`**} *file* {*id* …} {**`no.query`**} |  |
| **`delete.account`** | **`delete.account`** *account* | S |
| **`delete.catalog`** | **`delete.catalog`** *name* … {**`global`** | **`local`**} |  |
| **`delete.catalogue`** | **`delete.catalogue`** — the same verb as **`delete.catalog`** |  |
| **`delete.common`** | **`delete.common`** *name* |  |
| **`delete.file`** | **`delete.file`** {**`dict`** | **`data`**} *voc.name* {**`force`**} {**`no.query`**} |  |
| **`delete.index`** | **`delete.index`** *file* *field* … | **`all`** |  |
| **`delete.list`** | **`delete.list`** *list* |  |
| **`display`** | **`display`** *text* |  |
| **`dump`** | **`dump`** {**`dict`**} *file* {*id* … | **`*`**} {**`(options`**} |  |
| **`echo`** | **`echo on`** | **`off`** | **`echo`** to toggle |  |
| **`ed`** | **`ed`** {**`dict`**} *file* {*id* …} |  |
| **`edit`** | **`edit`** {**`dict`**} *file* *record* |  |
| **`form.list`** | **`form.list`** {**`dict`**} *file* {*list.no*} |  |
| **`format`** | **`format`** {*file*} {*record*} {**`case`**} |  |
| **`fstat`** | **`fstat`** *file* **`on`** | **`off`** | {**`lptr`**}  ·  **`fstat global`** {**`lptr`**}  ·  **`fstat reset`**  ·  **`fstat`** |  |
| **`generate`** | **`generate`** {**`dict`**} *file* *record* … |  |
| **`get.list`** | **`get.list`** *list* {**`to`** *list.no*} |  |
| **`get.stack`** | **`get.stack`** {*name*} |  |
| **`go`** | **`go`** *label* |  |
| **`hsm`** | **`hsm on`** | **`off`** | **`display`** {**`user`** *n*} |  |
| **`hush`** | **`hush on`** | **`off`** | **`hush`** to toggle |  |
| **`if`** | **`if`** *condition* *command* |  |
| **`list`** | **`list`** {**`dict`**} *file* {*selection*} {*fields*} {*options*} |  |
| **`list.common`** | **`list.common`** {**`all`**} |  |
| **`list.diff`** | **`list.diff`** *list.1* {*list.2* {*tgt*}} {**`count.sup`**} |  |
| **`list.files`** | **`list.files`** |  |
| **`list.index`** | **`list.index`** *file* {*field* …} |  |
| **`list.inter`** | **`list.inter`** *list.1* {*list.2* {*tgt*}} {**`count.sup`**} |  |
| **`list.item`** | **`list.item`** {**`dict`**} *file* {*selection*} |  |
| **`list.label`** | **`list.label`** {**`dict`**} *file* {*selection*} {*fields*} |  |
| **`list.locks`** | **`list.locks`** | S |
| **`list.readu`** | **`list.readu`** {*user.no*} {**`detail`**} {**`wait`**} {**`no.page`**} {**`lptr`** {*n*}} | S |
| **`list.union`** | **`list.union`** *list.1* {*list.2* {*tgt*}} {**`count.sup`**} |  |
| **`list.vars`** | **`list.vars`** {*pattern*} |  |
| **`listu`** | **`listu`** {**`no.page`**} {**`lptr`** {*n*}} | S |
| **`lock`** | **`lock`** *n* {**`no.wait`**} | S |
| **`logmsg`** | **`logmsg`** *text* |  |
| **`logout`** | **`logout`** | *n* … | **`all`** |  |
| **`logto`** | **`logto`** *account* |  |
| **`make.index`** | **`make.index`** *file* *field* … {**`no.nulls`**} {**`pathname`** *path*} |  |
| **`map`** | **`map`** {**`all`**} {**`lptr`** {*n*}} {**`file`** {*name*}} |  |
| **`merge.list`** | **`merge.list`** *list.no* *rel.op* *list.no* {**`to`** *list.no*} {**`count.sup`**} |  |
| **`message`** | **`message`** *user.no* {**`immediate`**} {*text*} |  |
| **`micro`** | **`micro`** {**`dict`**} *file* *record* |  |
| **`modify.account`** | **`modify.account`** *account* **`add`** | **`delete`** *user*  ·  *account* **`ssh`** | **`api`** | **`both`** | **`none`**  ·  *account* **`sh-on`** | **`sh-off`** | **`os-on`** | **`os-off`**  ·  *account* **`suspended`** | **`unsuspended`** | S |
| **`modify.password`** | **`modify.password`** {*account*} |  |
| **`nano`** | **`nano`** {**`dict`**} *file* *record* |  |
| **`nselect`** | **`nselect`** *file* {*list.no*} |  |
| **`off`** | **`off`** |  |
| **`option`** | **`option`** *name* {**`on`** | **`off`** | **`display`**}  ·  **`option all off`**  ·  **`option`** |  |
| **`pause`** | **`pause`** {*seconds*} |  |
| **`pdebug`** | **`pdebug`** {*command*} |  |
| **`pdump`** | **`pdump`** *n* |  |
| **`phantom`** | **`phantom`** *command* |  |
| **`printer`** | **`printer`** {*unit*} **`query`** | **`at`** *name* | **`file`** *file* *record* | **`width`** *n* | **`lines`** *n* | **`top.margin`** *n* | **`bottom.margin`** *n* | **`left.margin`** *n* | **`keep.open`** | **`close`** | **`reset`** |  |
| **`pstat`** | **`pstat`** {**`user`** *n*} {**`level`** *n*} {**`no.page`**} {**`lptr`** {*n*}} |  |
| **`pterm`** | **`pterm display`** | **`lptr`** | **`break`** … | **`case`** … | **`newline`** … | **`return`** … | **`binary`** … | **`telnet`** … | **`reset`** *string* | **`prompt`** *p* *c* |  |
| **`qselect`** | **`qselect`** {**`dict`**} *file* {*id* … | **`*`**} {**`(options`**} |  |
| **`quit`** | **`quit`** — the same verb as **`off`** |  |
| **`reformat`** | **`reformat`** {**`dict`**} *file* {*selection*} {*fields*} |  |
| **`release`** | **`release`** *file* *id* …  ·  **`release filelock`** *file* |  |
| **`remote.api`** | **`remote.api`** {**`on`** | **`local`** | **`off`**} | S |
| **`remote.ssh`** | **`remote.ssh`** {**`on`** | **`off`**} | S |
| **`rename`** | **`rename`** — the same verb as **`cname`** |  |
| **`report.src`** | **`report.src on`** | **`off`** | **`report.src`** to toggle |  |
| **`report.style`** | **`report.style`** {*name* | **`off`**} |  |
| **`run`** | **`run`** {*file*} *record* {*arguments*} |  |
| **`save.list`** | **`save.list`** *list* {**`from`** *list.no*} |  |
| **`save.stack`** | **`save.stack`** {*name*} |  |
| **`search`** | **`search`** {**`dict`**} *file* {*selection*} |  |
| **`select`** | **`select`** {**`dict`**} *file* {*selection*} {*list.no*} |  |
| **`set`** | **`set`** *name* *value* |  |
| **`set.date`** | **`set.date`** *date* | S |
| **`set.exit.status`** | **`set.exit.status`** *n* |  |
| **`set.file`** | **`set.file`** *account* *file* *pointer* |  |
| **`set.trigger`** | **`set.trigger`** *file* *name* {*modes*} |  |
| **`setptr`** | **`setptr`** *unit* | **`default`**`,`*width*`,`*depth*`,`*top*`,`*bottom*`,`*mode* {`,`*options*}  ·  **`setptr display`**  ·  **`setptr`** *unit*`,`**`display`** |  |
| **`sh`** | **`sh`** *command* |  |
| **`show`** | **`show`** {**`dict`**} *file* {*selection*} |  |
| **`sleep`** | **`sleep`** *n* | *hh*`:`*mm*{`:`*ss*} |  |
| **`sort`** | **`sort`** {**`dict`**} *file* {*selection*} {*fields*} {*options*} |  |
| **`sort.item`** | **`sort.item`** {**`dict`**} *file* {*selection*} |  |
| **`sort.label`** | **`sort.label`** {**`dict`**} *file* {*selection*} {*fields*} |  |
| **`sp.close`** | **`sp.close`** |  |
| **`sp.open`** | **`sp.open`** |  |
| **`sp.view`** | **`sp.view`** |  |
| **`spool`** | **`spool`** *file* *id* … {**`lines`** *n* *m*} {**`lnum`**} {**`lptr`** *n*} |  |
| **`sreformat`** | **`sreformat`** {**`dict`**} *file* {*selection*} {*fields*} |  |
| **`sselect`** | **`sselect`** {**`dict`**} *file* {*selection*} {*list.no*} |  |
| **`status`** | **`status`** |  |
| **`stop`** | **`stop`** |  |
| **`sum`** | **`sum`** {**`dict`**} *file* {*selection*} *field* |  |
| **`term`** | **`term`** | *width*{`,`*lines*} {*type*} | **`colour`** *bg*{`,`*fg*} | **`default`** | **`display`** |  |
| **`time`** | **`time`** | **`internal`** |  |
| **`umask`** | **`umask`** {*mask*} |  |
| **`unlock`** | **`unlock file`** *n* {**`user`** *n*} *id* … | **`all`** | **`filelock`**  ·  **`unlock tasklock`** *n* … | S |
| **`update.accounts`** | **`update.accounts`** {**`all`**} | S |
| **`who`** | **`who`** |  |
| **`who.am.i`** | **`who.am.i`** |  |

**Blank in the who column means every account has it**; `S` is SDSYS
alone.

