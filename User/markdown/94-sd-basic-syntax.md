Title: SD Basic - Syntax
Subtitle: Every statement and function, alphabetically, with its syntax and nothing else.

A lookup card, and nothing else. If you know what you want and have forgotten
how to spell it, it is here. If you want to know what it *does*, the other
seventeen documents in this set are where that lives.

*Italics* mark something you supply, **bold** a word typed as it stands, and
braces an optional part. SD folds case, so any of this may be written in
either case.

> **This page is generated, and it is checked for completeness rather than
> proof-read for it.** The roster comes from `BCOMP`'s own tables — the same
> extraction the rest of this set uses — and `tools/mksyntax.py` refuses to
> write the page if a single name that belongs on it has no line. Argument
> counts for functions are read out of `BCOMP`'s dispatch table, which is
> positional against the name list and carries each name in a comment; the
> script asserts the two agree before it uses either. The shapes that a count
> cannot express — every statement, and about twenty functions — come from
> documents 01 to 17, where each one is described in full.

**What is not here, and where it went.** Everything on this card is something
an application may use. Names that an ordinary program **cannot** compile are
in the administrator documentation, under *SD Basic - Restricted Commands*: the
restricted statements, the internal-only functions, and the one name that is in
the compiler's table with nothing behind it. **If you are looking for something
and it is not here, that is where to look before concluding it does not
exist.**

***ONE THING IS MARKED, AND IT IS THE ONE THAT WASTES TIME.***

| | |
|---|---|
| ***(clause word)*** | not a statement — a word that belongs inside another one's syntax |


## A

| | |
|---|---|
| **`abort`** | `abort` {*message*} |
| **`abs`** | `abs(`*a*`)` |
| **`abss`** | `abss(`*a*`)` |
| **`accept.socket.connection`** | `accept.socket.connection(`*a*, *b*`)` |
| **`acos`** | `acos(`*a*`)` |
| **`alpha`** | `alpha(`*a*`)` |
| **`ands`** | `ands(`*a*, *b*`)` |
| **`append`** | clause of `openseq`, and of `edit` ***(clause word)*** |
| **`arg`** | `arg(`*a*`)` |
| **`arg.count`** | `arg.count()` |
| **`ascii`** | `ascii(`*a*`)` |
| **`asin`** | `asin(`*a*`)` |
| **`assigned`** | `assigned(`*a*`)` |
| **`atan`** | `atan(`*a*`)` |

## B

| | |
|---|---|
| **`before`** | clause of `ins`: `ins` *value* `before` *arr*`<`*f*`>` ***(clause word)*** |
| **`begin`** | `begin case` … `end case`   ·   `begin transaction` … `end transaction` |
| **`bindkey`** | `bindkey(`*a*, *b*`)` |
| **`bitand`** | `bitand(`*a*, *b*`)` |
| **`bitnot`** | `bitnot(`*a*`)` |
| **`bitor`** | `bitor(`*a*, *b*`)` |
| **`bitreset`** | `bitreset(`*a*, *b*`)` |
| **`bitset`** | `bitset(`*a*, *b*`)` |
| **`bittest`** | `bittest(`*a*, *b*`)` |
| **`bitxor`** | `bitxor(`*a*, *b*`)` |
| **`break`** | `break on`   ·   `break off`   ·   `break` *n* |
| **`by`** | clause of `locate` and `sselect` — `by` `'AL'`, `'AR'`, `'DL'`, `'DR'` ***(clause word)*** |

## C

| | |
|---|---|
| **`call`** | `call` *name*`(`*arg*, …`)`   ·   `call @`*var*`(`*arg*, …`)` |
| **`capturing`** | clause of `execute` and `os.execute` — take the output ***(clause word)*** |
| **`case`** | `case` *condition*, inside `begin case` … `end case` |
| **`catalogued`** | `catalogued(`*a*`)` |
| **`cats`** | `cats(`*a*, *b*`)` |
| **`ccall`** | `ccall(`*a*, *b*`)` |
| **`chain`** | `chain` *command* |
| **`change`** | `change(`*string*, *from*, *to* {, *occurrences* {, *start*}}`)` |
| **`char`** | `char(`*a*`)` |
| **`checksum`** | `checksum(`*a*`)` |
| **`chgphant`** | `chgphant()` |
| **`class`** | `class` *name* |
| **`clear`** | `clear` — zeroes every variable |
| **`clearcommon`** | `clearcommon` {*name*} |
| **`cleardata`** | `cleardata` |
| **`clearfile`** | `clearfile` *file.var* {`on error` …} |
| **`clearinput`** | `clearinput` |
| **`clearselect`** | `clearselect` {*list.no*} |
| **`close`** | `close` *file.var* {`on error` …} |
| **`close.socket`** | `close.socket` *socket* |
| **`closeseq`** | `closeseq` *file.var* |
| **`col1`** | `col1()` |
| **`col2`** | `col2()` |
| **`com`** | `com` `/`*name*`/` *var*, … — synonym of `common` |
| **`commit`** | `commit`, inside `begin transaction` … `end transaction` |
| **`common`** | `common` `/`*name*`/` *var*, *matrix*`(`*n*`)`, … |
| **`compare`** | `compare(`*a*, *b* {, *justification*}`)` |
| **`config`** | `config(`*a*`)` |
| **`continue`** | `continue` — next iteration of the enclosing `loop` or `for` |
| **`convert`** | `convert(`*a*, *b*, *c*`)` |
| **`cos`** | `cos(`*a*`)` |
| **`count`** | `count(`*a*, *b*`)` |
| **`counts`** | `counts(`*a*, *b*`)` |
| **`create`** | `create` *file.var* `then` … `else` … |
| **`create.file`** | `create.file` *name* {`directory`} {`on error` …} |
| **`create.server.socket`** | `create.server.socket(`*addr*, *port* {, *flags*}`)` |
| **`crop`** | `crop(`*a*`)` |
| **`crt`** | `crt` *expr* {`:` …} {`:`} |
| **`csvdq`** | `csvdq(`*line* {, *delimiter*}`)` |
| **`current.level`** | clause of `enter` — run at the current command level ***(clause word)*** |

## D

| | |
|---|---|
| **`data`** | `data` *expr*, … |
| **`date`** | `date()` |
| **`dcount`** | `dcount(`*a*, *b*`)` |
| **`debug`** | `debug` — needs `basic` *file* *record* `debugging` |
| **`deffun`** | `deffun` *name*`(`*arg*, …`)` {`calling` *"cat.name"*} {`local`} |
| **`del`** | `del` *arr*`<`*f* {, *v* {, *sv*}}`>` |
| **`delete`** | `delete` *file.var*, *id* {`on error` …}   ·   `delete(`*arr*, *f* {, *v* {, *sv*}}`)` |
| **`deletelist`** | `deletelist` *name* `then` … `else` … |
| **`deleteseq`** | `deleteseq` *path* {`on error` …} `then` … `else` … |
| **`deleteu`** | `deleteu` *file.var*, *id* {`on error` …} |
| **`dim`** | `dim` *name*`(`*rows* {, *cols*}`)`, … |
| **`dimension`** | `dimension` *name*`(`*rows* {, *cols*}`)`, … — synonym of `dim` |
| **`dir`** | `dir(`*a*`)` |
| **`disinherit`** | `disinherit` *object* |
| **`display`** | `display` *expr* {`:` …} {`:`} |
| **`div`** | `div(`*a*, *b*`)` |
| **`do`** | `loop` … `do` … `repeat` |
| **`downcase`** | `downcase(`*a*`)` |
| **`dparse`** | `dparse` *string*, *delimiter*, *var*, … |
| **`dparse.csv`** | `dparse.csv` *line*, *delimiter*, *var*, … |
| **`dquote`** | `dquote(`*a*`)` |
| **`dtx`** | `dtx(`*n* {, *digits*}`)` |

## E

| | |
|---|---|
| **`ebcdic`** | `ebcdic(`*a*`)` |
| **`echo`** | `echo on`   ·   `echo off`   ·   `echo` *expr* |
| **`edit`** | clause of `keyedit`, and the `edit` verb at the command prompt ***(clause word)*** |
| **`else`** | clause of `if`, and of every statement that has a `then` |
| **`end`** | `end` — closes a program, a `then`, an `else`, a `case`, a transaction |
| **`enter`** | `enter` *name*   ·   `enter @`*var* |
| **`env`** | `env(`*a*`)` |
| **`eqs`** | `eqs(`*a*, *b*`)` |
| **`equ`** | `equ` *name* `to` *value* — synonym of `equate` |
| **`equate`** | `equate` *name* `to` *value* {, *name* `to` *value*} … |
| **`execute`** | `execute` *cmd* {`capturing` *v*} {`returning` *v*} {`passlist` {*l*}} {`rtnlist` {*v*}} |
| **`exit`** | `exit` — leave the enclosing `loop` or `for` |
| **`exp`** | `exp(`*a*`)` |
| **`extract`** | `extract(`*arr*, *f* {, *v* {, *sv*}}`)` |

## F

| | |
|---|---|
| **`field`** | `field(`*string*, *delimiter*, *occurrence* {, *count*}`)` |
| **`fields`** | `fields(`*arr*, *delimiter*, *occurrence* {, *count*}`)` |
| **`fieldstore`** | `fieldstore(`*a*, *b*, *c*, *d*, *e*`)` |
| **`file`** | `file` *name* — names a file at compile time |
| **`fileinfo`** | `fileinfo(`*file.var*, *key*`)` |
| **`filelock`** | `filelock` *file.var* {`locked` …} {`on error` …} — ***no `then`/`else`*** |
| **`fileunlock`** | `fileunlock` *file.var* {`on error` …} |
| **`findstr`** | `findstr` *x* `in` *arr* {, *occ*} `setting` *f* {, *v* {, *sv*}} `then` … `else` … |
| **`flush`** | `flush` *file.var* `then` … `else` … |
| **`fmt`** | `fmt(`*a*, *b*`)` |
| **`fmts`** | `fmts(`*a*, *b*`)` |
| **`fold`** | `fold(`*string*, *width* {, *delimiter*}`)` |
| **`folds`** | `folds(`*arr*, *width* {, *delimiter*}`)` |
| **`footing`** | `footing` *expr* |
| **`for`** | `for` *var* `=` *start* `to` *end* {`step` *n*} … `next` *var* |
| **`formlist`** | `formlist` *arr* {, *delimiter*} {`to` *list.no*} |
| **`from`** | clause of `read`, `readnext`, `matbuild`, `matparse`, `remove`, `readcsv` ***(clause word)*** |
| **`function`** | `function` *name*`(`*arg*, …`)` |

## G

| | |
|---|---|
| **`ges`** | `ges(`*a*, *b*`)` |
| **`get`** | `get` *var* `from` *object* |
| **`get.messages`** | `get.messages()` |
| **`get.port.params`** | `get.port.params(`*a*`)` |
| **`getlist`** | `getlist` *name* {`to` *list.no*} `then` … `else` — ***the `then`/`else` is not optional*** |
| **`getnls`** | `getnls(`*a*`)` |
| **`getpu`** | `getpu(`*a*, *b*`)` |
| **`getrem`** | `getrem(`*a*`)` |
| **`go`** | `go` *label* — synonym of `goto` |
| **`gosub`** | `gosub` *label* {, *arg*, …} |
| **`goto`** | `goto` *label* |
| **`gts`** | `gts(`*a*, *b*`)` |

## H

| | |
|---|---|
| **`heading`** | `heading` *expr* |
| **`hidden`** | clause of `input` — do not echo what is typed ***(clause word)*** |
| **`hush`** | `hush on`   ·   `hush off`   ·   `hush` *expr* |

## I

| | |
|---|---|
| **`iconv`** | `iconv(`*a*, *b*`)` |
| **`iconvs`** | `iconvs(`*a*, *b*`)` |
| **`idiv`** | `idiv(`*a*, *b*`)` |
| **`if`** | `if` *condition* `then` … `else` … |
| **`ifs`** | `ifs(`*a*, *b*, *c*`)` |
| **`in`** | clause of `find`, `findstr` and `locate` |
| **`include`** | `$include` *record*   ·   `$include` *file* *record* |
| **`index`** | `index(`*a*, *b*, *c*`)` |
| **`indexs`** | `indexs(`*a*, *b*, *c*`)` |
| **`indices`** | `indices(`*file.var* {, *index*}`)` |
| **`inherit`** | `inherit` *object* |
| **`inmat`** | `inmat()`   ·   `inmat(`*matrix*`)` |
| **`input`** | `input` *var* {, *length*} {`:`} {`_`} {`hidden`} {`overlay`} {`upcase`} {`waiting` *n*} |
| **`inputblk`** | `inputblk(`*a*`)` |
| **`inputclear`** | `inputclear` |
| **`inputcsv`** | `inputcsv` *var*, … |
| **`inputerr`** | `inputerr` *message* |
| **`inputfield`** | `inputfield` *var*, *length* {, *mask*} |
| **`ins`** | `ins` *value* `before` *arr*`<`*f* {, *v* {, *sv*}}`>` |
| **`insert`** | `insert(`*arr*, *f* {, *v* {, *sv*}}, *value*`)` |
| **`int`** | `int(`*a*`)` |
| **`itype`** | `itype(`*compiled.i.type*`)` |

## K

| | |
|---|---|
| **`keycode`** | `keycode(`{*timeout*}`)` |
| **`keyedit`** | `keyedit` *key*, *action* |
| **`keyexit`** | `keyexit` *key*, *action* |
| **`keyin`** | `keyin(`{*timeout*}`)` |
| **`keyinc`** | `keyinc(`{*timeout*}`)` |
| **`keyinr`** | `keyinr(`{*timeout*}`)` |
| **`keyready`** | `keyready()` |
| **`keytrap`** | `keytrap` *key*, *action* |

## L

| | |
|---|---|
| **`len`** | `len(`*a*`)` |
| **`lens`** | `lens(`*a*`)` |
| **`les`** | `les(`*a*, *b*`)` |
| **`listindex`** | `listindex(`*a*, *b*, *c*`)` |
| **`ln`** | `ln(`*a*`)` |
| **`local`** | `local` *var*, … — inside a `deffun` declared `local` |
| **`locate`** | `locate` *x* `in` *arr*`<`*f* {, *v*}`>` {`by` *order*} `setting` *pos* `then` … `else` … |
| **`lock`** | `lock` *n* `then` … `else` … — ***with no `else` it retries for ever*** |
| **`locked`** | clause of `readu`, `readl`, `readvu`, `readvl`, `matreadu`, `matreadl`, `filelock`, `recordlocku`, `recordlockl` ***(clause word)*** |
| **`logmsg`** | `logmsg` *text* |
| **`loop`** | `loop` … {`while` *c*} {`until` *c*} … `repeat` |
| **`lower`** | `lower(`*a*`)` |
| **`lts`** | `lts(`*a*, *b*`)` |

## M

| | |
|---|---|
| **`mark.mapping`** | `mark.mapping` *file.var*, *state* |
| **`mat`** | `mat` *matrix* `=` *value*   ·   `mat` *a* `=` `mat` *b* |
| **`matbuild`** | `matbuild` *var* `from` *matrix* {, *start* {, *end*}} — ***no `using`*** |
| **`matchfield`** | `matchfield(`*a*, *b*, *c*`)` |
| **`matparse`** | `matparse` *matrix* `from` *string* {, *delimiter*} |
| **`matread`** | `matread` *matrix* `from` *file.var*, *id* {`on error` …} `then` … `else` … |
| **`matreadcsv`** | `matreadcsv` *matrix* `from` *file.var* `then` … `else` … |
| **`matreadl`** | `matreadl` *matrix* `from` *file.var*, *id* {`locked` …} `then` … `else` … |
| **`matreadu`** | `matreadu` *matrix* `from` *file.var*, *id* {`locked` …} `then` … `else` … |
| **`matwrite`** | `matwrite` *matrix* `to` *file.var*, *id* {`on error` …} |
| **`matwriteu`** | `matwriteu` *matrix* `to` *file.var*, *id* {`on error` …} |
| **`max`** | `max(`*a*, *b*`)` |
| **`maximum`** | `maximum(`*a*`)` |
| **`min`** | `min(`*a*, *b*`)` |
| **`minimum`** | `minimum(`*a*`)` |
| **`mod`** | `mod(`*a*, *b*`)` |
| **`mods`** | `mods(`*a*, *b*`)` |

## N

| | |
|---|---|
| **`nap`** | `nap` *milliseconds* |
| **`neg`** | `neg(`*a*`)` |
| **`negs`** | `negs(`*a*`)` |
| **`nes`** | `nes(`*a*, *b*`)` |
| **`next`** | `next` *var* — closes a `for` |
| **`nobuf`** | `nobuf` *file.var* `then` … `else` … |
| **`nocaseinvert`** | clause of `input` — do not invert the case of typed letters ***(clause word)*** |
| **`not`** | `not(`*a*`)` |
| **`nots`** | `nots(`*a*`)` |
| **`null`** | `null` — does nothing; the empty statement |
| **`num`** | `num(`*a*`)` |
| **`nums`** | `nums(`*a*`)` |

## O

| | |
|---|---|
| **`object`** | `object(`*class* {, *arg*, …}`)` |
| **`objinfo`** | `objinfo(`*a*, *b*`)` |
| **`oconv`** | `oconv(`*a*, *b*`)` |
| **`oconvs`** | `oconvs(`*a*, *b*`)` |
| **`on`** | `on` *n* `goto` *label*, … — ***clamps, it does not fall through*** |
| **`open`** | `open` {*dict*`,`} *name* `to` *file.var* {`readonly`} {`on error` …} `then` … `else` … |
| **`open.socket`** | `open.socket(`*addr*, *port*, *flags* {, *context*}`)` |
| **`openpath`** | `openpath` *path* `to` *file.var* {`readonly`} {`on error` …} `then` … `else` … |
| **`openseq`** | `openseq` *path* `to` *file.var* {`append`} {`overwrite`} {`readonly`} `then` … `else` … — ***`then` = it existed, `else` = it was created*** |
| **`ors`** | `ors(`*a*, *b*`)` |
| **`os.error`** | `os.error()` |
| **`os.execute`** | `os.execute` *command* {`capturing` *var*} |
| **`outerjoin`** | `outerjoin(`*a*, *b*, *c*`)` |
| **`overlay`** | clause of `input` — type over what is already there ***(clause word)*** |
| **`overwrite`** | clause of `openseq` ***(clause word)*** |

## P

| | |
|---|---|
| **`page`** | `page` {*n*} |
| **`panning`** | clause of `input` — pan a field wider than the screen ***(clause word)*** |
| **`passlist`** | clause of `execute` — hand the active select list to the command ***(clause word)*** |
| **`pause`** | `pause` {*seconds*} |
| **`perform`** | `perform` *command* |
| **`precision`** | `precision` *n* |
| **`print`** | `print` *expr* {`:` …} {`:`}   ·   `print on` *unit* *expr* |
| **`printcsv`** | `printcsv` {`on` *unit*} *value*, … {`:`} |
| **`printer`** | `printer on`   ·   `printer off`   ·   `printer close`   ·   `printer file on` *unit* *file*, *record* |
| **`printer.setting`** | `printer.setting(`*a*, *b*, *c*`)` |
| **`printerr`** | `printerr` *message* |
| **`private`** | `private` *var*, … |
| **`procread`** | `procread` *var* `then` … `else` … |
| **`procwrite`** | `procwrite` *var* |
| **`program`** | `program` *name* |
| **`public`** | `public` *var*, … |
| **`pwr`** | `pwr(`*a*, *b*`)` |

## Q

| | |
|---|---|
| **`quote`** | `quote(`*a*`)` |

## R

| | |
|---|---|
| **`raise`** | `raise(`*a*`)` |
| **`randomize`** | `randomize`   ·   `randomize(`*seed*`)` |
| **`rdiv`** | `rdiv(`*a*, *b*`)` |
| **`read`** | `read` *var* `from` *file.var*, *id* {`on error` …} `then` … `else` … |
| **`read.socket`** | `read.socket(`*a*, *b*, *c*, *d*`)` |
| **`readblk`** | `readblk` *var* `from` *file.var*, *length* `then` … `else` … |
| **`readcsv`** | `readcsv` `from` *file.var* `to` *var*, … `then` … `else` … |
| **`readl`** | `readl` *var* `from` *file.var*, *id* {`locked` …} {`on error` …} `then` … `else` … |
| **`readlist`** | `readlist` *var* {`from` *list.no*} `then` … `else` … |
| **`readnext`** | `readnext` *id* {, *vm*} {`from` *list.no*} {`on error` …} `then` … `else` … |
| **`readonly`** | clause of `open`, `openpath` and `openseq` ***(clause word)*** |
| **`readseq`** | `readseq` *var* `from` *file.var* {`on error` …} `then` … `else` … — `else` is end of file |
| **`readu`** | `readu` *var* `from` *file.var*, *id* {`locked` …} {`on error` …} `then` … `else` … |
| **`readv`** | `readv` *var* `from` *file.var*, *id*, *field* {`on error` …} `then` … `else` … |
| **`readvl`** | `readvl` *var* `from` *file.var*, *id*, *field* {`locked` …} `then` … `else` … |
| **`readvu`** | `readvu` *var* `from` *file.var*, *id*, *field* {`locked` …} `then` … `else` … |
| **`recordlocked`** | `recordlocked(`*file.var*, *id*`)` — ***-3 -2 -1 0 1 2 3*** |
| **`recordlockl`** | `recordlockl` *file.var*, *id* {`locked` …} {`on error` …} |
| **`recordlocku`** | `recordlocku` *file.var*, *id* {`locked` …} {`on error` …} |
| **`release`** | `release` {*file.var* {, *id*}} {`on error` …} — bare `release` releases everything |
| **`rem`** | `rem(`*a*, *b*`)` |
| **`remark`** | `remark` *text* — synonym of `rem` |
| **`remove`** | `remove` *value* `from` *arr* `setting` *delimiter.code* |
| **`remove.break.handler`** | `remove.break.handler` |
| **`repeat`** | `repeat` — closes a `loop` |
| **`replace`** | `replace(`*arr*, *f* {, *v* {, *sv*}}, *value*`)` |
| **`restore.screen`** | `restore.screen` *image*, *restore.cursor* |
| **`return`** | `return` {`to` *label*}   ·   `return(`*value*`)` from a function |
| **`returning`** | clause of `execute` — take the command's error text ***(clause word)*** |
| **`reuse`** | `reuse(`*a*`)` |
| **`rnd`** | `rnd(`*a*`)` |
| **`rollback`** | `rollback`, inside `begin transaction` … `end transaction` |
| **`rqm`** | `rqm` {*seconds*} |
| **`rtnlist`** | clause of `execute` — take the list the command left ***(clause word)*** |
| **`rtrans`** | `rtrans(`*file.var*, *id*, *field*, *action*`)` |

## S

| | |
|---|---|
| **`save.screen`** | `save.screen(`*a*, *b*, *c*, *d*`)` |
| **`savelist`** | `savelist` *name* {`from` *list.no*} `then` … `else` — ***the `then`/`else` is not optional*** |
| **`sddecrypt`** | `sddecrypt(`*a*, *b*, *c*`)` |
| **`sdencrypt`** | `sdencrypt(`*a*, *b*, *c*`)` |
| **`seek`** | `seek` *file.var*, *offset* {, *relative.to*} `then` … `else` … |
| **`select`** | `select` {*file.var*} {`to` *list.no*} |
| **`selecte`** | `selecte` {`to` *var*} |
| **`selectindex`** | `selectindex` *index* {, *value*} `from` *file.var* {`to` *list.no*} |
| **`selectinfo`** | `selectinfo(`*a*, *b*`)` |
| **`selectleft`** | `selectleft` *index* `from` *file.var* `setting` *var* `to` *list.no* — ***no `then`/`else`*** |
| **`selectn`** | `selectn` {*file.var*} `to` *list.no* |
| **`selectright`** | `selectright` *index* `from` *file.var* `setting` *var* `to` *list.no* — ***no `then`/`else`*** |
| **`selectv`** | `selectv` {*file.var*} `to` *var* — read it back with `readnext … from` |
| **`sendmail`** | `sendmail` *to*, *from*, *subject*, *body* {, *attachments*} `then` … `else` … |
| **`sentence`** | `sentence()` — the same value as `@sentence` |
| **`seq`** | `seq(`*a*`)` |
| **`server.addr`** | `server.addr(`*a*`)` |
| **`set`** | `set` *var* `on` *object* `to` *value* |
| **`set.arg`** | `set.arg` *n*, *value* |
| **`set.break.handler`** | `set.break.handler` *subroutine.name* |
| **`set.exit.status`** | `set.exit.status` *n* |
| **`set.port.params`** | `set.port.params(`*a*, *b*`)` |
| **`set.socket.mode`** | `set.socket.mode(`*a*, *b*, *c*`)` |
| **`setleft`** | `setleft` *index* `from` *file.var* — ***no `then`/`else`*** |
| **`setnls`** | `setnls` *key*, *value* |
| **`setpu`** | `setpu` `on` *unit*, *key*, *value* |
| **`setrem`** | `setrem` *position* `on` *var* |
| **`setright`** | `setright` *index* `from` *file.var* — ***no `then`/`else`*** |
| **`setting`** | clause of `find`, `findstr`, `locate`, `remove`, `selectleft`, `selectright` ***(clause word)*** |
| **`shift`** | `shift(`*a*, *b*`)` |
| **`sin`** | `sin(`*a*`)` |
| **`sleep`** | `sleep` {*seconds*}   ·   `sleep` *hh:mm:ss* |
| **`socket.info`** | `socket.info(`*a*, *b*`)` |
| **`soundex`** | `soundex(`*a*`)` |
| **`soundexs`** | `soundexs(`*a*`)` |
| **`space`** | `space(`*a*`)` |
| **`spaces`** | `spaces(`*a*`)` |
| **`splice`** | `splice(`*a*, *b*, *c*`)` |
| **`sqrt`** | `sqrt(`*a*`)` |
| **`squote`** | `squote(`*a*`)` |
| **`sselect`** | `sselect` {*file.var*} {`by` *field*} {`to` *list.no*} |
| **`status`** | `status()` |
| **`step`** | clause of `for`: `for` *v* `=` *a* `to` *b* `step` *n* ***(clause word)*** |
| **`stop`** | `stop` {*message*} |
| **`str`** | `str(`*a*, *b*`)` |
| **`strs`** | `strs(`*a*, *b*`)` |
| **`sub`** | `sub` *name*`(`*arg*, …`)` — synonym of `subroutine` |
| **`subr`** | `subr(`*"name"* {, *arg*, …}`)` |
| **`subroutine`** | `subroutine` *name*`(`*arg*, …`)` |
| **`substitute`** | `substitute(`*arr*, *from*, *to*, *delimiter*`)` |
| **`substrings`** | `substrings(`*a*, *b*, *c*`)` |
| **`sum`** | `sum(`*a*`)` |
| **`summation`** | `summation(`*a*`)` |
| **`swap`** | `swap(`*string*, *from*, *to* {, *occurrences* {, *start*}}`)` |
| **`swapcase`** | `swapcase(`*a*`)` |
| **`sysmsg`** | `sysmsg(`*number* {, *substitution*, …}`)` |
| **`system`** | `system(`*a*`)` |

## T

| | |
|---|---|
| **`tan`** | `tan(`*a*`)` |
| **`tclread`** | `tclread` *var* |
| **`terminfo`** | `terminfo(`*capability* {, *arg*, …}`)` |
| **`then`** | clause of `if`, and of every statement that has an `else` ***(clause word)*** |
| **`time`** | `time()` |
| **`timedate`** | `timedate()` |
| **`timeout`** | `timeout` *file.var*, *seconds* |
| **`to`** | clause of `open`, `for`, `equate`, `readcsv`, `select`, `savelist`, `writecsv` ***(clause word)*** |
| **`trans`** | `trans(`{*dict*`,`} *file.name*, *id*, *field*, *action*`)` |
| **`transaction`** | `transaction start`   ·   `transaction commit`   ·   `transaction abort` |
| **`trapping`** | clause of `execute` — trap the break key ***(clause word)*** |
| **`trim`** | `trim(`*string* {, *character* {, *option*}}`)` |
| **`trimb`** | `trimb(`*a*`)` |
| **`trimbs`** | `trimbs(`*a*`)` |
| **`trimf`** | `trimf(`*a*`)` |
| **`trimfs`** | `trimfs(`*a*`)` |
| **`trims`** | `trims(`*arr* {, *character* {, *option*}}`)` |

## U

| | |
|---|---|
| **`umask`** | `umask(`*a*`)` |
| **`unassigned`** | `unassigned(`*a*`)` |
| **`unlock`** | `unlock` {*n*} |
| **`until`** | clause of `loop`: `loop` … `until` *condition* … `repeat` |
| **`upcase`** | `upcase(`*a*`)` |

## V

| | |
|---|---|
| **`vartype`** | `vartype(`*a*`)` |
| **`void`** | `void` *function.call* — call a function and discard its value |
| **`vslice`** | `vslice(`*a*, *b*`)` |

## W

| | |
|---|---|
| **`waiting`** | clause of `input`: `input` *var* `waiting` *seconds* ***(clause word)*** |
| **`wake`** | `wake` *user.no* |
| **`weofseq`** | `weofseq` *file.var* {`on error` …} |
| **`while`** | clause of `loop`: `loop` … `while` *condition* … `repeat` |
| **`write`** | `write` *var* `to` *file.var*, *id* {`on error` …} — ***inside a transaction the lock must already be held*** |
| **`write.socket`** | `write.socket(`*a*, *b*, *c*, *d*`)` |
| **`writeblk`** | `writeblk` *var* `to` *file.var* {`on error` …} |
| **`writecsv`** | `writecsv` *value*, … `to` *file.var* `then` … `else` … |
| **`writeseq`** | `writeseq` *var* `to` *file.var* {`on error` …} `then` … `else` … |
| **`writeseqf`** | `writeseqf` *var* `to` *file.var* {`on error` …} `then` … `else` … |
| **`writeu`** | `writeu` *var* `to` *file.var*, *id* {`on error` …} |
| **`writev`** | `writev` *var* `to` *file.var*, *id*, *field* {`on error` …} |
| **`writevu`** | `writevu` *var* `to` *file.var*, *id*, *field* {`on error` …} |

## X

| | |
|---|---|
| **`xlate`** | `xlate(`{*dict*`,`} *file.name*, *id*, *field*, *action*`)` |
| **`xtd`** | `xtd(`*a*`)` |

## See also

[SD Basic - Program Structure](01-sd-basic-program-structure.html) ·
[SD Basic - Program Control](02-sd-basic-program-control.html) ·
[SD Basic - File Handling](07-sd-basic-file-handling.html) ·
[SD Basic - System and Environment](16-sd-basic-system-and-environment.html).
