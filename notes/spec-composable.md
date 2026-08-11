# Composable deck: remix the canonical 40 minute talk

His words:

> for our composability talk we have a great 40 minute talk to draw content
> from so it should be mostly remixing that with some concerns about small
> teams and future direction. Question at back of mind is JAX actually the
> right way forward, is Julia the place to build serious tools.

Read `notes/style.md` and `notes/epinow2-drift.md` first.

## The instruction

This deck should be a **remix of the 40 minute deck**, not a fresh
composition. That deck is canonical (see `notes/epinow2-drift.md`), it is
good, and it is the author's own voice. Where our version has invented its own
framing, replace it with the original's.

Source:
`/Users/lshsa2/code/EpiAware/ComposableProbabilisticIDModels/presentations/40min/index.qmd`

Work by selecting and compressing its slides, keeping its wording where the
wording is fine. Do not paraphrase for the sake of it. Paraphrasing is how the
EpiNow2 justification framing got in, and how the deck drifted from his voice.

Its figures are in
`/Users/lshsa2/code/EpiAware/ComposableProbabilisticIDModels/figures/`.
Prefer them over anything newly drawn.

## What to keep from the original

- The Whitty framing: modelling evidence must be timely, rigorous and
  collaborative, and current approaches struggle to be all three.
- The gap slides, compressed: COVID showed what is possible, flexibility for
  new contexts, integrating diverse data, multi-model efforts.
- Chaining versus joint modelling, and what each costs.
- What composable modelling is.
- One case study, worked properly, with the three hours to replicate figure.
- The design considerations, heavily compressed. There are eight in the
  original and there is room for the two or three that matter.

## What to add, which the original does not have

The author's position has moved since the paper. This is the honest part and
it belongs near the end.

- Turing.jl as the backend is less obviously right than it was: reduced team
  size, stability, incomplete AD backend support. State it fairly and with
  evidence. The original could not say this and it is the main reason this is
  not simply a cut-down of the original.
- Small teams across the tools we depend on.
- The direction now: composable `Distributions.jl` objects,
  `CensoredDistributions.jl`, `ConvolvedDistributions.jl`.
- **The question at the back of his mind, which should be asked out loud:**
  is JAX actually the way forward, and is Julia the place to build serious
  tools? This is a real question to a room of Julia developers, and asking it
  honestly is more interesting than any answer the deck could give. It should
  not be buried in an attribution.

`ComposableTuringIDModels.jl` is the prototype the talk demonstrates and must
be named clearly, on a slide and in the talk page button row.

## Do not link the Zenodo archive

The author:

> Don't like to link this: https://zenodo.org/records/18274166. Remove from
> project page and slides.
>
> paper in CDC clearance is the bullet
>
> composabeturing and epiaware.org have what we mostly need, the latter has an
> approaches page we can link to with i.e. requirements

`https://doi.org/10.5281/zenodo.17884675` resolves to that record. Every
reference to it comes out of the talk page and the deck, and nothing should
put it back.

What replaces it:

- **The paper's status is a bullet, not a link.** It is in CDC clearance. Say
  that plainly and do not link anything.
- **[ComposableTuringIDModels.jl](https://github.com/EpiAware/ComposableTuringIDModels.jl)**
  for the prototype itself.
- **[epiaware.org/approaches](https://epiaware.org/approaches/)** for the
  argument. That page carries "Why we need this", "What we want from any
  approach" as twelve design considerations, and the two current approaches,
  [composed distributions](https://epiaware.org/approaches/composed-distributions.html)
  and
  [composable Turing models](https://epiaware.org/approaches/composable-turing-models.html).

The design considerations section of the deck should point at the approaches
page rather than the paper. It is public, it is maintained, and it is the
same content.

## Constraints

- 15 minute slot, and the counted slide budget has oscillated badly across
  rounds: 21, then 13, then 20. Do not simply promote backup slides to fill
  time. Decide the talk, then let the length follow.
- Backup slides after the close are fine and useful for questions.
- The two poster slides in `_partials/90-summary.qmd` must still work in print
  with no speaker.
