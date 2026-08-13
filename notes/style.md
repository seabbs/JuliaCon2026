# Style, corrected

The author's verdict on the decks as they stood:

> the slides honestly kind of suck. In general content is not my style. how I
> llm is not a good ref as all bots, other talks are a better ref. new dags are
> high level not very good, lots of text all over the place. Slides have become
> very cluttered.

Read this before touching any slide. It overrides earlier guidance, and the
"Density" section at the end overrides any numeric limit you have been given
anywhere else in your instructions.

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

## His humour is content, not decoration

> my humour is being stripped out

Rebuild passes keep flattening the jokes into correct, dry statements. That is
a fault, not a tidy-up.

Specifically, and these are not negotiable:

- The **before skynet** and **after skynet** framing on the roadmap deck is
  his. Keep the words.
- **Emojis** where he asked for them, for example the whale contributors
  slide.
- Wry section titles like "Unfortunately, biases" stay exactly as written.
- "In sad confusion" stays.

If a line reads as a correct summary of something that was funny, you have
broken it. Put it back.

## Write less

> stop writing so much
>
> take my steer and ape my style

Two related faults keep coming back. Slides carry more prose than he would
write, and the prose is a paraphrase of his steer rather than his steer.

When he gives you a line, use his line. Do not improve it, expand it into two
sentences, or add the clause that explains why it matters. His steers are
often already the bullet.

Signs you are doing this: a bullet that restates its own first clause, a
sentence that ends by telling the audience what to conclude, a slide where
half the words are yours and half are his and the joins show.

## No editorial asides dressed as references

> In all the decks I also see lots of little tiny aside comments in the same
> style the refs are. I don't think we want any of those.

An `::: {.attribution}` block is for **sources**. A citation, a repository, an
issue or PR number, a data provenance line, a figure credit, a retrieval date.

It is not for editorial remarks, second thoughts, caveats the slide did not
have room for, or cross-references to his other talks. Those have crept in
across all three decks because the attribution block is a convenient place to
put a sentence you could not fit. It reads as footnoting yourself.

Example of the fault, from `composable/_partials/06-direction.qmd`:

> The alternative approaches, including NumPyro and JAX, are in the paper's
> discussion. The paper is in CDC clearance · The six autodiff configurations
> were the 14:30 talk in this room, samabbott.co.uk/JuliaCon2026/roadmap

Only the first clause is a source. The rest is commentary and a signpost.

Go through every attribution block in all three decks. Keep the source. Delete
the commentary, or promote it to a bullet if it is worth saying. Cross-talk
pointers stay only where an earlier steer explicitly asked for one, and there
is at most one per deck.

## Talk pages carry the abstract, and nothing arguing with it

The author, on a note that had been added under the delays abstract:

> This: "One correction since submission. Multiple dispatch removes the
> integer distribution tables and ecosystem composability removes the
> vendoring tool, but neither removes the numerical problem underneath..."
> should not be on the project page or similar

Two such notes existed, one on the delays page and one on the composable page
("One change of view since submission..."). Both are gone. Do not write
another.

The rule. A talk page carries the submitted abstract, the links, and the
resources. It does not carry errata, corrections, changes of view, or an
argument with what was submitted. If the position has moved, that belongs in
the talk, where he can say it himself and be asked about it. A written
correction on a web page reads as apologising to a reader who has not
complained.

This applies to all three pages and to anything that behaves like one.

This section takes precedence over any numeric limit you have been given
elsewhere in this task, including counts of elements, bullets or words. The
author's correction:

> it can be a little busier, let's not be so binary

So `02-censoring.qmd` is the register to aim for, not a ceiling. Some slides
carry more and should. A comparison table, a code slide, the autodiff backend
table in the delays deck, a figure with the equation beside it. Density is
fine when the density is the content.

The fault being fixed is clutter without purpose. Ask of each element on a
slide: is it doing work nothing else on this slide is already doing? Cut what
fails that.

Concretely, still wrong:
- Bullets that narrate the figure sitting next to them.
- A bullet that runs to three or four lines. That is a paragraph, and it
  should be two short bullets or one shorter one.
- Sub-bullets, nearly always.
- A callout carrying an argument rather than a single line.
- A diagram whose boxes are the bullet list redrawn.
- Two slides making the same point.

Fine, and do not strip these out:
- A dense table where the comparison is the argument.
- Code, when the code is the point.
- A figure plus the one equation it illustrates plus three bullets, which is
  what `02-censoring.qmd` itself does.
- A slide that is fuller than its neighbours because it is carrying the
  section's main idea.

If you are unsure whether a slide is too busy, leave it and say so in your
return value. Over-cutting is now the bigger risk. Earlier rounds already cut
one deck from 21 slides to 13 and then back to 20, and the author has said
these decks read as thin and cluttered at once, which is what happens when
words are trimmed everywhere instead of ideas being removed somewhere.
