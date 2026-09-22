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
> the verb records in `newvoc` plus the ones an administrator account
> adds, which is **147** verbs, and `tools/mktclsyntax.py` refuses to
> write the page if any of them has no line. The shapes come from the
> subject documents, where each verb is described in full.

**The tier column is the VOC, not an opinion.** It is read from
`TIER.OMIT.STANDARD` and `TIER.ADD.ADMINISTRATOR`, the same two lists
the account-creation code uses, so it cannot drift from what an account
actually gets. **A verb your account does not have is not refused — the
name is simply not recognised.**

| | | |
|---|---|---|
| **standard** | 82 verbs | every account has these |
| **programmer** | 42 more | withheld from a standard account |
| **administrator** | 23 more | and several need an elevated session as well |

## The verbs

| | syntax | tier |
|---|---|---|
| **`!`** | **`!`** *command* | A |
| **`abort`** | **`abort`** {*message*} |  |
| **`alias`** | **`alias`** *command* *target* |  |
| **`analyse.file`** | **`analyse.file`** {**`dict`**} *file* {**`statistics`**} {**`lptr`**} | P |
| **`analyze.file`** | **`analyze.file`** — the same verb as **`analyse.file`** | P |
| **`append.sd.path`** | **`append.sd.path`** {**`on`** | **`off`**} | A |
| **`autologout`** | **`autologout`** {*minutes*} |  |
| **`basic`** | **`basic`** {*file*} *record* {*record* …} | P |
| **`bell`** | **`bell on`** | **`off`** |  |
| **`break`** | **`break on`** | **`off`** | **`on user`** *n* |  |
| **`build.index`** | **`build.index`** *file* *field* … | **`all`** | P |
| **`catalog`** | **`catalog`** {*file* {*call.name*}} {*program*} {**`local`** | **`global`** | **`pcode`**} {**`no.xref`**} | P |
| **`catalogue`** | **`catalogue`** — the same verb as **`catalog`** | P |
| **`cd`** | **`cd`** {**`dict`** | **`data`**} *file* {*i-type* …} {**`no.query`**} {**`no.page`**}  ·  **`cd local`**  ·  **`cd all`** | P |
| **`clean.account`** | **`clean.account`** | A |
| **`clear.abort`** | **`clear.abort`** |  |
| **`clear.data`** | **`clear.data`** |  |
| **`clear.file`** | **`clear.file`** {**`data`** | **`dict`**} *file* | P |
| **`clear.input`** | **`clear.input`** |  |
| **`clear.locks`** | **`clear.locks`** {*n*} | A |
| **`clear.prompts`** | **`clear.prompts`** |  |
| **`clear.select`** | **`clear.select`** {*list.no*} |  |
| **`clear.stack`** | **`clear.stack`** |  |
| **`cleardata`** | **`cleardata`** — the same verb as **`clear.data`** |  |
| **`clearinput`** | **`clearinput`** — the same verb as **`clear.input`** |  |
| **`clearprompts`** | **`clearprompts`** — the same verb as **`clear.prompts`** |  |
| **`clearselect`** | **`clearselect`** — the same verb as **`clear.select`** |  |
| **`clr`** | **`clr`** |  |
| **`cname`** | **`cname`** *old.file* **`to`** *new.file* | P |
| **`como`** | **`como on`** {*record*} | **`off`** | **`pause`** | **`resume`** |  |
| **`compile.dict`** | **`compile.dict`** — the same verb as **`cd`** | P |
| **`config`** | **`config`** {**`lptr`** | **`gpl`** | **`contrib`** | *param* *value*} | A |
| **`configure.file`** | **`configure.file`** {**`dict`**} *voc.name* {*parameters*} | **`default`** | P |
| **`copy`** | **`copy from`** {**`dict`**} *src* {**`to`** {**`dict`**} *tgt*} {*id* …} {**`(options`**} | P |
| **`copy.list`** | **`copy.list`** *list* {**`,`***new*} {**`from`** *src*} {**`to`** *tgt*} {*options*} |  |
| **`copyp`** | **`copyp`** {**`dict`**} *file* *id* … {**`(options`**} | P |
| **`count`** | **`count`** {**`dict`**} *file* {*selection*} |  |
| **`create.account`** | **`create.account user`** *name* {**`administrator`** | **`programmer`**} <**`ssh`** | **`api`** | **`both`** | **`none`**> {**`no.query`**}  ·  **`create.account group`** *name*  ·  **`create.account other`** *name* *pathname* | A |
| **`create.file`** | **`create.file`** {**`dict`**} *voc.name* {**`directory`**} {*parameters*} | P |
| **`create.index`** | **`create.index`** *file* *field* … {**`no.nulls`**} {**`pathname`** *path*} | P |
| **`cs`** | **`cs`** — the same verb as **`clr`** |  |
| **`ct`** | **`ct`** {**`dict`**} *file* {*id* … | **`*`**} {**`(options`**} |  |
| **`date`** | **`date`** | **`internal`** | *n* | *date* |  |
| **`date.format`** | **`date.format on`** | **`off`** | **`display`** |  |
| **`debug`** | **`debug`** | P |
| **`delete`** | **`delete`** {**`dict`**} *file* {*id* …} {**`no.query`**} | P |
| **`delete.account`** | **`delete.account`** *account* | A |
| **`delete.catalog`** | **`delete.catalog`** *name* … {**`global`** | **`local`**} | P |
| **`delete.catalogue`** | **`delete.catalogue`** — the same verb as **`delete.catalog`** | P |
| **`delete.common`** | **`delete.common`** *name* | P |
| **`delete.file`** | **`delete.file`** {**`dict`** | **`data`**} *voc.name* {**`force`**} {**`no.query`**} | P |
| **`delete.index`** | **`delete.index`** *file* *field* … | **`all`** | P |
| **`delete.list`** | **`delete.list`** *list* |  |
| **`display`** | **`display`** *text* |  |
| **`dump`** | **`dump`** {**`dict`**} *file* {*id* … | **`*`**} {**`(options`**} | P |
| **`echo`** | **`echo on`** | **`off`** | **`echo`** to toggle |  |
| **`ed`** | **`ed`** {**`dict`**} *file* {*id* …} | P |
| **`edit`** | **`edit`** {**`dict`**} *file* *record* | P |
| **`form.list`** | **`form.list`** {**`dict`**} *file* {*list.no*} |  |
| **`format`** | **`format`** {*file*} {*record*} {**`case`**} |  |
| **`fstat`** | **`fstat`** *file* **`on`** | **`off`** | {**`lptr`**}  ·  **`fstat global`** {**`lptr`**}  ·  **`fstat reset`**  ·  **`fstat`** | P |
| **`generate`** | **`generate`** {**`dict`**} *file* *record* … | P |
| **`get.list`** | **`get.list`** *list* {**`to`** *list.no*} |  |
| **`get.stack`** | **`get.stack`** {*name*} |  |
| **`go`** | **`go`** *label* |  |
| **`grant`** | **`grant`** *account* **`to`** *user* | A |
| **`hsm`** | **`hsm on`** | **`off`** | **`display`** {**`user`** *n*} | P |
| **`hush`** | **`hush on`** | **`off`** | **`hush`** to toggle |  |
| **`if`** | **`if`** *condition* *command* |  |
| **`list`** | **`list`** {**`dict`**} *file* {*selection*} {*fields*} {*options*} |  |
| **`list.common`** | **`list.common`** {**`all`**} |  |
| **`list.diff`** | **`list.diff`** *list.1* {*list.2* {*tgt*}} {**`count.sup`**} |  |
| **`list.files`** | **`list.files`** |  |
| **`list.grants`** | **`list.grants`** *account* | A |
| **`list.index`** | **`list.index`** *file* {*field* …} | P |
| **`list.inter`** | **`list.inter`** *list.1* {*list.2* {*tgt*}} {**`count.sup`**} |  |
| **`list.item`** | **`list.item`** {**`dict`**} *file* {*selection*} |  |
| **`list.label`** | **`list.label`** {**`dict`**} *file* {*selection*} {*fields*} |  |
| **`list.locks`** | **`list.locks`** | A |
| **`list.readu`** | **`list.readu`** {*user.no*} {**`detail`**} {**`wait`**} {**`no.page`**} {**`lptr`** {*n*}} | A |
| **`list.union`** | **`list.union`** *list.1* {*list.2* {*tgt*}} {**`count.sup`**} |  |
| **`list.vars`** | **`list.vars`** {*pattern*} |  |
| **`listu`** | **`listu`** {**`no.page`**} {**`lptr`** {*n*}} | A |
| **`lock`** | **`lock`** *n* {**`no.wait`**} | A |
| **`logmsg`** | **`logmsg`** *text* |  |
| **`logout`** | **`logout`** | *n* … | **`all`** | P |
| **`logto`** | **`logto`** *account* |  |
| **`make.index`** | **`make.index`** *file* *field* … {**`no.nulls`**} {**`pathname`** *path*} | P |
| **`map`** | **`map`** {**`all`**} {**`lptr`** {*n*}} {**`file`** {*name*}} | P |
| **`merge.list`** | **`merge.list`** *list.no* *rel.op* *list.no* {**`to`** *list.no*} {**`count.sup`**} |  |
| **`message`** | **`message`** *user.no* {**`immediate`**} {*text*} |  |
| **`micro`** | **`micro`** {**`dict`**} *file* *record* | P |
| **`modify.account`** | **`modify.account`** *account* **`standard`** | **`programmer`** | **`administrator`** | **`suspended`**  ·  *account* **`ssh`** | **`api`** | **`both`** | **`none`**  ·  *account* **`sh-on`** | **`sh-off`** | **`os-on`** | **`os-off`**  ·  *account* **`add`** | **`delete`** *user* | A |
| **`modify.password`** | **`modify.password`** {*account*} | A |
| **`nselect`** | **`nselect`** *file* {*list.no*} |  |
| **`off`** | **`off`** |  |
| **`option`** | **`option`** *name* {**`on`** | **`off`** | **`display`**}  ·  **`option all off`**  ·  **`option`** |  |
| **`pause`** | **`pause`** {*seconds*} |  |
| **`pdebug`** | **`pdebug`** {*command*} | P |
| **`pdump`** | **`pdump`** *n* | P |
| **`phantom`** | **`phantom`** *command* | P |
| **`printer`** | **`printer`** {*unit*} **`query`** | **`at`** *name* | **`file`** *file* *record* | **`width`** *n* | **`lines`** *n* | **`top.margin`** *n* | **`bottom.margin`** *n* | **`left.margin`** *n* | **`keep.open`** | **`close`** | **`reset`** |  |
| **`pstat`** | **`pstat`** {**`user`** *n*} {**`level`** *n*} {**`no.page`**} {**`lptr`** {*n*}} | P |
| **`pterm`** | **`pterm display`** | **`lptr`** | **`break`** … | **`case`** … | **`newline`** … | **`return`** … | **`binary`** … | **`telnet`** … | **`reset`** *string* | **`prompt`** *p* *c* |  |
| **`qselect`** | **`qselect`** {**`dict`**} *file* {*id* … | **`*`**} {**`(options`**} |  |
| **`quit`** | **`quit`** — the same verb as **`off`** |  |
| **`reformat`** | **`reformat`** {**`dict`**} *file* {*selection*} {*fields*} | P |
| **`release`** | **`release`** *file* *id* …  ·  **`release filelock`** *file* |  |
| **`remote.api`** | **`remote.api`** {**`on`** | **`local`** | **`off`**} | A |
| **`remote.ssh`** | **`remote.ssh`** {**`on`** | **`off`**} | A |
| **`rename`** | **`rename`** — the same verb as **`cname`** | P |
| **`report.src`** | **`report.src on`** | **`off`** | **`report.src`** to toggle |  |
| **`report.style`** | **`report.style`** {*name* | **`off`**} |  |
| **`revoke`** | **`revoke`** *account* **`from`** *user* | A |
| **`run`** | **`run`** {*file*} *record* {*arguments*} | P |
| **`save.list`** | **`save.list`** *list* {**`from`** *list.no*} |  |
| **`save.stack`** | **`save.stack`** {*name*} |  |
| **`search`** | **`search`** {**`dict`**} *file* {*selection*} |  |
| **`select`** | **`select`** {**`dict`**} *file* {*selection*} {*list.no*} |  |
| **`set`** | **`set`** *name* *value* |  |
| **`set.date`** | **`set.date`** *date* | A |
| **`set.exit.status`** | **`set.exit.status`** *n* |  |
| **`set.file`** | **`set.file`** *account* *file* *pointer* |  |
| **`set.trigger`** | **`set.trigger`** *file* *name* {*modes*} | P |
| **`setptr`** | **`setptr`** *unit* | **`default`**`,`*width*`,`*depth*`,`*top*`,`*bottom*`,`*mode* {`,`*options*}  ·  **`setptr display`**  ·  **`setptr`** *unit*`,`**`display`** |  |
| **`sh`** | **`sh`** *command* | A |
| **`show`** | **`show`** {**`dict`**} *file* {*selection*} |  |
| **`sleep`** | **`sleep`** *n* | *hh*`:`*mm*{`:`*ss*} |  |
| **`sort`** | **`sort`** {**`dict`**} *file* {*selection*} {*fields*} {*options*} |  |
| **`sort.item`** | **`sort.item`** {**`dict`**} *file* {*selection*} |  |
| **`sort.label`** | **`sort.label`** {**`dict`**} *file* {*selection*} {*fields*} |  |
| **`sp.close`** | **`sp.close`** |  |
| **`sp.open`** | **`sp.open`** |  |
| **`sp.view`** | **`sp.view`** |  |
| **`spool`** | **`spool`** *file* *id* … {**`lines`** *n* *m*} {**`lnum`**} {**`lptr`** *n*} |  |
| **`sreformat`** | **`sreformat`** {**`dict`**} *file* {*selection*} {*fields*} | P |
| **`sselect`** | **`sselect`** {**`dict`**} *file* {*selection*} {*list.no*} |  |
| **`ssh.server`** | **`ssh.server`** {**`install`** | **`remove`**} | A |
| **`status`** | **`status`** |  |
| **`stop`** | **`stop`** |  |
| **`sum`** | **`sum`** {**`dict`**} *file* {*selection*} *field* |  |
| **`term`** | **`term`** | *width*{`,`*lines*} {*type*} | **`colour`** *bg*{`,`*fg*} | **`default`** | **`display`** |  |
| **`time`** | **`time`** | **`internal`** |  |
| **`unlock`** | **`unlock file`** *n* {**`user`** *n*} *id* … | **`all`** | **`filelock`**  ·  **`unlock tasklock`** *n* … | A |
| **`update.accounts`** | **`update.accounts`** {**`all`**} | A |
| **`who`** | **`who`** |  |
| **`who.am.i`** | **`who.am.i`** |  |

**Blank in the tier column means every account has it**; `P` is a
programmer verb and `A` an administrator one.

