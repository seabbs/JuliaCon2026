# What he has already said in public, about other people's tools

Checked because he asked:

> some of that might be things I have okayed in past slide decks so check on
> that

Searched `how-to-serial-interval`, `how-I-llm`, and both composability decks
for "sloppy", "flaky", "dodgy", "small team", "unmaintained", "abandoned",
"brittle", "one maintainer", "bus factor". **No hits in any delivered deck.**

## The norm his decks actually follow

Blunt about his own work, factual and generous about everyone else's.

**About his own package**, `40min/index.qmd:316`, slide "What happens when you
try to be modular?", on epinowcast:

> - Cannot easily be separated into reusable parts
> - Difficult for users to contribute to or adapt beyond supported
>   functionality
> - Limited adoption; large API and documentation for users to get to grips
>   with
> - Remains limited in scope despite ambition

That is harsher than anything in our three decks, and it is aimed at himself.

**About someone else's package**, same deck, `:665`, "Why Turing.jl as the
modelling backend?": six bullets, all strengths, no criticism at all.

So the rule is not "never criticise". It is "criticism of others is factual
and sourced, criticism of yourself can be blunt".

## Where our decks stand

They already follow this, and no change is needed.

- `roadmap/_partials/02-ad.qmd:112` reads "In my view none of the six is
  reliably best, and each is kept going by a small team". Marked as opinion,
  and "kept going by" is respectful rather than dismissive. The attribution
  beneath carries CI dates and issue numbers.
- `composable/_partials/05-backend.qmd` makes the Turing case by quoting
  Turing's **own documentation** ("not all AD libraries in there are
  thoroughly tested on Turing models"), noting `TuringLang/ADTests` was
  archived on 2026-06-15, and showing a commit count table. Evidence, not
  adjectives.
- The delays deck's autodiff table reports scenarios registered broken per
  backend, counted from the fixtures.

## The one place the blunt register survives

`prompts.qmd`, inside his verbatim brief:

- "Julia standards by default are somewhat sloppy and you need to enforce a
  template."
- "We needed to set up AD testing, as you cannot say which AD backend is best.
  They are all flaky and dodgy, or run by small teams."

These are his own words, in a block clearly marked as his prompt, and he has
said his prompts are fine. There is precedent for publishing a raw prompt: the
how-I-llm deck put its prompt on a slide.

Worth knowing rather than acting on: neither line names a project, but the
second is about other people's autodiff packages, and it reads differently on
a public page than it did in a private prompt. The slides make the same point
with evidence and no adjectives. His call.
