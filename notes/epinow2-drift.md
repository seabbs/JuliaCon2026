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
- **Restore "took 3 hours to replicate".** It is concrete, favourable, and was
  dropped. It appears in the 40 minute deck at
  `presentations/40min/index.qmd:897`, as "Widely used real-time tool
  replicated through composition of DSL components (took 3 hours to
  replicate)". It is not in the paper, and it does not need to be. See the
  ruling below.
- Leave the "seven packages share nothing" slide alone. That framing is in the
  original and is the argument, not drift.

## Ruling: the 40 minute deck is canonical

The author, asked whether the three hours figure was real, said:

> yes everything in 40 minute talk is canonical

So `/Users/lshsa2/code/EpiAware/ComposableProbabilisticIDModels/presentations/40min/index.qmd` is a primary source for this talk.
Anything stated there can be used without further verification, and does not
need a second source in the paper.

Two consequences:

1. Facts that live only in the 40 minute deck are usable. The three hours
   figure is the immediate one. Go and look for others that were dropped on
   the way down to 15 minutes, since the same reasoning will have discarded
   them, and they are the concrete favourable details this deck is short of.
2. Where our deck and the 40 minute deck disagree about anything other than
   length or the author's changed view of Turing, the 40 minute deck wins and
   ours is the thing to correct.

This does NOT extend to the 20 minute deck, which is a cut of the same
material, nor to any claim about a third party's project that has aged since.
Turing's maintenance state in particular has moved, and the author's
scepticism about Turing is deliberate and post-dates both decks.

## Separately: the prototype is not named clearly

`ComposableTuringIDModels.jl` is the proof of concept the whole deck
demonstrates. It currently appears only:

- in a `using` line inside a code block (`03-case-study.qmd:6`)
- in an attribution link (`03-case-study.qmd:36`)
- as one bullet under "Code" on `composable/index.qmd:98`

It is never introduced by name on a slide, and it is not in the button row at
the top of the talk page beside Slides and Code and data. Someone watching the
talk cannot tell what to go and install.
