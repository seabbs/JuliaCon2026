# Style, corrected

The author's verdict on the decks as they stood:

> the slides honestly kind of suck. In general content is not my style. how I
> llm is not a good ref as all bots, other talks are a better ref. new dags are
> high level not very good, lots of text all over the place. Slides have become
> very cluttered.

Read this before touching any slide. It overrides earlier guidance.

## The reference decks changed

**DO NOT use `/Users/lshsa2/code/seabbs/how-I-llm` as a style reference.**
Earlier rounds of this project used it. That was wrong. It was itself written
by agents, so copying it compounds the problem rather than fixing it.

Use these instead, in this order:

1. `/Users/lshsa2/code/seabbs/how-to-serial-interval/_partials/` — the closest
   thing to what these decks should look like. Study
   `02-censoring.qmd` in particular.
2. `/Users/lshsa2/code/EpiAware/ComposableProbabilisticIDModels/presentations/40min/index.qmd`
   — canonical for the composable talk, and a good model generally.

## What the good decks actually do

Take `how-to-serial-interval/_partials/02-censoring.qmd` apart. Every content
slide there is the same shape:

- A 40% column of **three or four short bullets**. Not five. Not sub-bullets.
- A 60% column holding **one purpose-built diagram** that carries the idea,
  and where there is maths, the one equation that matters.
- One `::: {.attribution}` line saying where the figure or claim came from.
- At most one `::: {.callout-note}`, holding a single sentence.

The bullets do not describe the figure. The figure does the explaining and the
bullets say the things the figure cannot.

That is the target. Slides in our decks that carry two columns of prose, or a
table plus bullets plus a callout plus an attribution, are the problem.

## Specific faults to fix

1. **Clutter.** Too many words per slide, and too many elements per slide. If
   a slide has a figure, a table, four bullets, a callout and a two-line
   attribution, cut until one idea is left.
2. **The mermaid diagrams added in the last round are weak.** They are
   high-level box-and-arrow sketches that restate the bullets. A diagram earns
   its place only if it shows something the words cannot: a mechanism, a
   timeline, a distribution being deformed. If a mermaid block is just three
   labelled boxes, delete it and let the slide breathe.
3. **Prefer reusing the real diagrams.** `how-to-serial-interval/figures/`
   contains purpose-built figures that are exactly right and already match the
   author's hand: `fig-double-censoring.png`, `fig-primary-censoring.png`,
   `fig-secondary-censoring.png`, `fig-truncation.png`,
   `fig-charniga-flowchart.png`, `fig-si-compose.png`. Copy the ones you need
   into `figures/` and use them.
4. **Voice.** Match the serial interval deck. Plain, specific, unhurried. No
   slogans, no summarising the point, no telling the audience what to think.

## The test

Put a slide from our deck next to a slide from `02-censoring.qmd`. If ours
looks busier, it is wrong.
