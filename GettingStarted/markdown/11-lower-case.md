Title: Lower case
Subtitle: Commands, file names, record ids and account names are lower case now — and nothing you type has to change.

**Everything that can be lower case is lower case.** SD used to be inconsistent
about it: BASIC source is free-form and usually written lower case, while file
names, field names and account names were forced up.

**What you type does not change.** `LIST`, `list` and `List` all run the same
verb, and so does every keyword — `with`, `by`, `no.page` and the rest.

## The lookup rule

SD tries a name **as you typed it, then in lower case, then in upper case**.

```
as typed  →  lower  →  upper
```

A name that matches exactly still wins, so nothing that works today changes. A
name that exists in **no** case is still reported as not found.

This order is used everywhere: the parser, the query processor, `RUN`,
multifile resolution, the `LOGIN` paragraph lookup, and `SET.FILE`'s default
`qfile` pointer.

> **The change was additive, not a flip.** A `downcase` attempt was inserted
> into a chain that already tried as-typed and then upper. On a tree whose ids
> are all upper case the new attempt can never hit, so it changed no behaviour
> and could not break anything.

## What is spelled in lower case now

| | |
|---|---|
| Commands in the VOC | **`list`**, `count`, **`select`**, **`create.file`**, **`setptr`** … and that is how they appear in `list voc`, `listv` and `ct voc` |
| System files on disk | `accounts`, `bp`, `bp.out`, `gpl.bp`, `messages`, `newvoc`, `pcode.out`, `syscom`, `voc`, `voc.dic`, `voc_template` and the rest |
| The `BP` and `GPL.BP` VOC entries | `bp` and `gpl.bp` |
| The hold file | `$hold` |
| The saved select list file | `$savedlists` |
| The command stack record | `$command.stack` |
| Account names on disk | `sdsys\accounts\don`, matching the account's own directory in `user_accounts` |
| Files in a new account | created with lower-case names on disk |

**Renaming these is cosmetic for resolution** — NTFS matches without being
asked — but the stored path text is user-visible through `listf` and the
current-directory reporting, which is the point.

## Record ids in directory files are no longer case sensitive

Two changes that go together:

- **Record ids in directory files** are matched case insensitively.
- **Queries against a directory file** match ids the same way.

**`create.file`** also takes a `no.case` option, which creates a file whose record
ids are treated as case insensitive: SD writes records preserving the casing
given by whatever performs the write, and reads locate records regardless of
casing.

## One correction worth reading

**`LIST` and `CT` used to disagree about the same name.** `list voc $HOLD`
answered *"'$HOLD' not found"* on the very record `ct voc $HOLD` had just shown
you. `LIST`, `SORT`, `SELECT` and the rest of the query language now use the
same as-typed → lower → upper order as everything else.

## Account names

**Account names have never been case sensitive and still are not.**
**`create.account`**, **`logto`** and the rest accept whatever case you type.

What changed is only how the register file is named on disk: new accounts are
recorded in lower case, so `sdsys\accounts\don` matches the account's own
directory. **Existing accounts keep the names they already have.**

## Existing accounts are not touched

**An account created before this keeps the upper-case names in its VOC and goes
on working. there is nothing to migrate.** An account you create now, or one
you refresh with **`update.accounts`**, gets the new spelling.

Because SD only ever *adds* VOC records at an update, an old account will end
up holding both spellings after **`update.accounts`**. That is harmless — they
dispatch to the same programs.

## The Turkish and Azeri fix

The installer creates an SD account for whoever authorises the install, and to
do that it matches your Windows user name against SD's copy of it — which means
changing both to the same case.

**Windows and SD did not change case the same way everywhere.** On a Turkish
or Azeri system Windows turns `I` into a dotless `ı`, and SD does not. A user
name containing that letter did not match itself, and the install finished
**without giving you an SD account at all.**

Both sides now use the same rule, which does not vary by locale. Nothing
changes on a system whose locale was never affected.

> If you are testing on a Turkish or Azeri locale, this is worth exercising
> specifically — it is the kind of fault that only appears on the machine you
> do not have.

## Two related refusals that no longer depend on case

**`delete.file`**'s refusal to delete `voc` and `$acc` no longer depends on the
case you type. It could not be got round before, because those names were upper
case — **it could have been, once they are not.**
