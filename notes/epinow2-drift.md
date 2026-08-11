# EpiNow2 framing drift in the composable deck

The author's steer:

> The composability paper has weird EpiNow2 justification vibes in the slides
> we have here that weren't in the original.

This note records the comparison so the fix is targeted rather than a rewrite.

## How the original framed EpiNow2

Source:
`/Users/lshsa2/code/EpiAware/ComposableProbabilisticIDModels/presentations/40min/index.qmd`,
slides at lines 850, 867 and 891.

EpiNow2 appears in two distinct roles, and both are matter of fact.

1. **As one of seven Stan packages that share nothing** (line 272, "The $R_t$
   estimation ecosystem"). It is evidence for the problem. No apology, no
   ownership disclaimer.
2. **As a replication target** (line 850, "Real-time nowcasting (EpiNow2)").
   Cited normally as Abbott et al. (2020) with a DOI in a callout, then
   straight into what was reused and how. The only editorial line is a
   concrete one: it "took 3 hours to replicate".

There is no passage defending the choice of EpiNow2, no disclosure that the
author wrote it, and no list of ways the replication differs from EpiNow2's
defaults.

## What our deck added

`composable/_partials/00-tldr.qmd`

> We rebuilt a common `EpiNow2` configuration, **from a package I wrote and
> help maintain**, in Julia, out of components that already existed

The clause is an ownership disclaimer. The original never makes one. It reads
as pre-empting an accusation nobody has made, and it costs the TL;DR its
punch.

`composable/_partials/03-case-study.qmd`, attribution block

> We put an ARIMA(2,1,1) on weekly $R_t$ rather than `EpiNow2`'s default
> differenced Matern Gaussian process, and there is no side-by-side against
> `EpiNow2` itself.

Two hedges in one sentence, both about not having done right by EpiNow2. The
honest caveat worth keeping is that this is a replication of a configuration
rather than a benchmark against the package. It does not need two clauses and
it does not belong in the same breath as the data provenance.

`composable/_partials/03-case-study.qmd`, callout

> No component was edited and no new component code was written. Parts
> validated separately, composition fitted together. **That is the whole
> claim.**

The last sentence is the "X is the point" pattern from `llmisms.md`. The two
sentences before it already make the claim.

## What to do

- Cut the ownership disclaimer from the TL;DR. If EpiNow2's provenance is
  worth stating, the citation already carries it.
- Reduce the attribution to one caveat, plainly: a configuration was
  replicated, not benchmarked.
- Delete "That is the whole claim."
- "Took 3 hours to replicate" appears in the 40 minute deck and is concrete
  and favourable, but grepping the paper (`index.qmd`, `case-studies.qmd`)
  finds no source for it. Do NOT restore it without the author confirming the
  number. Ask him rather than guessing.
- Leave the "seven packages share nothing" slide alone. That framing is in the
  original and is the argument, not drift.

## Separately: the prototype is not named clearly

`ComposableTuringIDModels.jl` is the proof of concept the whole deck
demonstrates. It currently appears only:

- in a `using` line inside a code block (`03-case-study.qmd:6`)
- in an attribution link (`03-case-study.qmd:36`)
- as one bullet under "Code" on `composable/index.qmd:98`

It is never introduced by name on a slide, and it is not in the button row at
the top of the talk page beside Slides and Code and data. Someone watching the
talk cannot tell what to go and install.
