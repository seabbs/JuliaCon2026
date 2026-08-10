# Composable talk: cutting 40 minutes down to 15

Planning notes for `composable/slides.qmd`.
Source decks are the 40 minute and 20 minute versions in
`~/code/EpiAware/ComposableProbabilisticIDModels/presentations/`.

Target is 17 slides total.
Title, 15 content slides at roughly 50 seconds each, closing.

## Headline decisions

- One case study only, and it is the `EpiNow2` replication.
- Turing.jl moves from "the answer" to "the backend the proof of concept
  happened to use", with an honest slide on why that choice is now less
  settled.
- A new closing arc on the direction of travel, built on composable
  `Distributions.jl` objects rather than on a PPL.

## Slide plan

1. **Title.**
   Title, name, LSHTM, JuliaCon 2026.
   No content.

2. **TL;DR.**
   Evidence must be timely, rigorous, and collaborative; chaining models is
   flexible but loses information, joint models are rigorous but cannot be
   taken apart; composable parts can be both; here is a proof of concept and
   where I now think the implementation should go.
   Five bullets, callout with the paper URL.

3. **What modelling evidence has to be.**
   Whitty set out that evidence for policy must be timely, explicit about its
   methods, as simple as it can be while staying rigorous, and it also has to
   be collaborative; almost nothing we build is all of these at once.
   Two columns, `whitty.png` on the right.

4. **We know it is possible, and we know it does not transfer.**
   COVID-19 models joined cases, prevalence, severity, and bed occupancy and
   informed policy; in 2022 mpox needed a different contact structure and
   those models could not be adapted, so single-source models were built
   instead.
   Merge of two source slides.
   `birrell-results.png` and `endo-results.png` side by side, one attribution
   block with both citations.

5. **Chaining models loses information.**
   The ONS CIS cost over £500 million and tested more than four million
   swabs, external modellers saw only summarised prevalence, and prevalence
   fed incidence fed $R_t$ fed variant severity analyses, with the
   uncertainty approximated and the assumptions inherited at every step.
   Compresses three source slides into one.
   `rt-incidence-ons.jpg` on the right.

6. **Joint models are rigorous but cannot be taken apart.**
   Lison et al. showed the cascade biases are real and that fitting the steps
   together removes them, but such models need expertise across several
   domains and do not survive contact with a new pathogen.
   `lison.png` on the right.
   Callout: this is the trade-off the talk is about.

7. **The duplication this produces.**
   At least seven Stan packages estimate $R_t$ by renewal and none share
   components, some share authors, wastewater tools were written by people
   who are not wastewater experts, and attempts at shared parts have not been
   picked up.
   `epinow2.png` or `epinowcast.png` on the right.
   Callout: the unit of reuse is the whole model, not the epidemiology.

8. **Composable modelling, and what it needs.**
   Definition callout, then the six themes as one line each rather than six
   slides, with the warning that these came from the authors and have had no
   community input.
   `requirements.png` full width beneath, or right column.
   This is the biggest single saving in the deck.

9. **The proof of concept.**
   A thin domain-specific language for epidemiology over a probabilistic
   backend, components carrying their own priors so domain knowledge travels
   with them, model definitions that do not know about the data, and an R
   interface so the choice of Julia is not a wall.
   `fig-composable.png` on the right, cropped if it will not read at size.

10. **What composition looks like in code.**
    `AR`, `MA`, and `DiffLatentModel` are separate objects; `@set` swaps the
    AR innovations for the MA process and the result is an ARIMA(2,1,1) that
    every later model reuses.
    Code block on the left from the 40 minute deck, `fig-case-studies.png`
    ARIMA panel on the right.

11. **Case study: rebuilding EpiNow2 by composition.**
    Reuse the whole ARIMA(2,1,1) and the negative binomial from the previous
    slide, broadcast $R_t$ to weekly, wrap the observation model in
    day-of-week ascertainment, then in an incubation delay, then in a
    reporting delay.
    `fig-case-studies.png`, EpiNow2 panel.
    Callout: nothing here required editing a component that already existed.

12. **Case study: it works.**
    Each part gets its own prior predictive check before anything is
    composed, and the joint posterior accounts for reporting delay while
    still recovering $R_t$.
    `fig-epinow2.png` on the right, panels A-C and E-F called out by letter.

13. **The backend, honestly.**
    Turing.jl gave us submodels, sampler choice, and the rest of Julia, and
    it is why the proof of concept exists at all; it is also still 0.x after
    nine years, ten breaking releases in the last eighteen months, and the
    submodel interface change left our code incompatible with the current
    release.
    Callout: none of this is a criticism of the people doing the work, it is
    a statement about how much of the stack depends on very few of them.
    Verified numbers to use are in the section below.

14. **AD is the part that decided it for me.**
    Turing is tested extensively against four AD backends and everything else
    routes through `DifferentiationInterface.jl`, where the documentation
    itself says a backend may error or silently return the wrong gradient;
    for a model that has to be trusted in an outbreak that is not a footnote.
    Callout: we ended up running our own AD matrix in CI because there was
    nothing to inherit.
    Quote the docs wording exactly, it is stronger than any paraphrase.

15. **So what is the composable unit, if not a PPL model?**
    Turn the question around; a `Distributions.jl` distribution is already a
    shared interface that the whole of Julia understands, so build the
    epidemiology as distributions and the PPL becomes optional rather than
    load-bearing.
    Callout: the DSL was always meant to be backend-agnostic, this is what
    taking that seriously looks like.

16. **Where this is going.**
    `CensoredDistributions.jl` for primary event and interval censoring,
    `ConvolvedDistributions.jl` for sums of arbitrary delays with a
    quadrature fallback, `ComposedDistributions.jl` for chains and branches
    of a natural history, and then compound quantities such as the generation
    time estimated as distributions in their own right.
    Four bullets maximum.
    Attribution block links to the org and to the delays talk earlier in the
    day.

17. **Closing.**
    What I want from the room, then the QR.
    Counter-examples where practice already is timely, rigorous, and
    collaborative; ideas that are not composable models; and, since
    composition needs an ecosystem to compose, build epidemiology tooling in
    Julia and come and talk to me.
    QR to the talk page, not to the slides.

## Which case study, and why

**Recommendation: `EpiNow2`.**

- It is the only one of the three that actually demonstrates the claim.
  Mishra reuses a single `AR(2)` component; Chatzilena swaps the infection
  process for an ODE and reuses least of all; `EpiNow2` reuses the entire
  ARIMA(2,1,1) and the negative binomial observation model from the worked
  example and then adds four layers on top without editing any of them.
- It carries its own motivation. The audience does not need the original
  paper explained, and "I rebuilt a package I wrote and maintain, in Julia,
  by composing parts that already existed" is a sharper claim than "we
  reproduced someone's figure".
- It sets up slides 15 and 16 for free. The layers it adds are reporting
  delay and incubation period, which is exactly the ground
  `CensoredDistributions.jl` and `ConvolvedDistributions.jl` cover, so the
  direction of travel follows from the case study rather than arriving from
  nowhere. It also ties the talk to the delays talk earlier in the day.
- One figure does both jobs. `fig-epinow2.png` has the per-component prior
  predictive checks in A-C and the joint posterior in E-F, so validate the
  parts and compose the parts are one image, not two slides.

Against Chatzilena: the ODE swap is the best argument for supporting more
than one modelling paradigm, but it costs a slide of SIR and SciML setup and
the reuse story is thin.
Keep it as a backup slide for questions.

Against Mishra: simplest to explain, weakest evidence of composition.

## Top three cuts

1. **The six design-consideration slides become one.**
   Lines 433 to 556 of the 40 minute deck are seven slides of themes.
   Replace with one slide, one line per theme, and `requirements.png`.
   Saves about six slides.

2. **Two of the three case studies, and the standalone ARIMA results slide.**
   Keep the ARIMA composition as setup for `EpiNow2` and drop
   `fig-arima.png`, `fig-mishra.png`, and `fig-sir.png`.
   Saves about five slides.

3. **The Turing.jl advocacy.**
   "The Turing.jl ecosystem" (people and institutions), "Why Turing.jl as the
   modelling backend?", the `generate_latent` backend code slide, and "For
   the Turing.jl developers" all go.
   They are replaced by slides 13 and 14, which say something the audience
   cannot get from the paper.
   Saves about three slides and changes the argument of the talk.

Also cut, less structurally: the gap section from five slides to two (drop
`hay.png` and `cramer.png`); the PPL definition callout, which this audience
does not need; the ONS CIS cascade from three slides to one; the alternative
approaches slide (AlgebraicJulia, Gen.jl, NumPyro, JuliaBUGS, RxInfer),
which becomes a backup slide; the workflow slides, which belong in the
roadmap talk; and the bot disclaimer slide.

## Figures to reuse, by path

Both bases sit under
`/Users/lshsa2/code/EpiAware/ComposableProbabilisticIDModels/`.
Base A is that path plus `presentations/figures/`.
Base B is that path plus `figures/`.

Reuse:

| Slide | Path |
|---|---|
| 3 | `A/whitty.png` |
| 4 | `A/birrell-results.png`, `A/endo-results.png` |
| 4 | `A/birrell.png`, `A/endo.png` (small inline thumbnails, optional) |
| 5 | `A/rt-incidence-ons.jpg` |
| 5 | `A/ons-prev.jpg` (alternative if the cascade image reads poorly) |
| 6 | `A/lison.png` |
| 7 | `A/epinow2.png` or `A/epinowcast.png` |
| 8 | `A/requirements.png` |
| 9 | `B/fig-composable.png` |
| 10, 11 | `B/fig-case-studies.png` |
| 12 | `B/fig-epinow2.png` |

Do not reuse:

- `A/hay.png`, `A/cramer.png`, `A/davies.png`. Their slides are cut.
- `A/stan.png`. The PPL slide is cut.
- `A/turing-docs.png`, `A/turing-epi-example.png`. These sell Turing, which
  is the opposite of what slides 13 and 14 do.
- `A/workflow.png`, `A/workflow-schematic.png`. These belong to the roadmap
  talk; using them here duplicates it.
- `B/fig-arima.png`, `B/fig-mishra.png`, `B/fig-sir.png`. Backup slides only.
- `B/visual-abstract.png`. 7 MB and built for print; use it on the poster,
  not in `embed-resources: true` slides.

All of these live outside this repo, so copy the ones we keep into
`JuliaCon2026/figures/composable/` before rendering rather than referencing
across repositories.

## Verified facts

Checked on 2026-08-10 through the GitHub API and the TuringLang docs source.
Anything not in this list should not appear as a number on a slide.

Turing.jl:

- 2,245 stars, 26 open issues, not archived, last push 2026-08-02.
- `DynamicPPL.jl`, where most of the composition machinery lives, has 62 open
  issues.
- First release April 2017. Latest release v0.46.0, 10 July 2026.
  Still 0.x after nine years; the planned 1.0 has not landed.
- Ten breaking releases in the last eighteen months, v0.37.0 through v0.46.0.
- Commits to Turing.jl since 2026-02-10: `penelopeysm` 17, `yebai` 4, every
  other human contributor two or fewer.
  Since 2025-08-10: `penelopeysm` 28 of roughly 42 human commits.
- Commits to DynamicPPL.jl since 2026-02-10: `penelopeysm` 47, `yebai` 9,
  `shravanngoswamii` 7, everyone else three or fewer.
- `mhauru`'s last commit to Turing.jl was 2025-12-04.

Say this as "one person is writing most of the commits", which the record
supports.
Do not say the team was cut, or name funding, or speculate about why.
Neither is verifiable from here.

AD, from `TuringLang/docs/usage/automatic-differentiation/index.qmd`:

- "Turing is most extensively tested with **ForwardDiff.jl** (the default),
  **Enzyme.jl**, **Mooncake.jl**, and **ReverseDiff.jl**."
- Everything else routes through `DifferentiationInterface.jl`, and "not all
  AD libraries in there are thoroughly tested on Turing models. Thus, it is
  possible that some of them will either error ... or maybe even silently
  give incorrect results".

That second quote is the strongest line available and it is theirs, not ours.
Use it verbatim.

From the paper's own limitations, so already on the record:

- The submodel interface changed from `@submodel` to `to_submodel` and the
  DSL is not compatible with the current Turing release.
- Limited handling of numerical instability; large simulated counts error.
- Profiling through the PPL layers is hard.

The direction of travel, all pushed 2026-08-09 or 2026-08-10 unless noted:

- `CensoredDistributions.jl`, 15 stars, 62 open issues, registered, has a
  Zenodo DOI, and runs six AD workflows in CI (ForwardDiff, ReverseDiff tape,
  Enzyme forward and reverse, Mooncake forward and reverse).
- `ConvolvedDistributions.jl`, 29 open issues.
- `ComposedDistributions.jl`, `ModifiedDistributions.jl` (28 open issues),
  `ReparameterisedDistributions.jl` (7), `LoweredDistributions.jl` (21),
  `DistributionsInference.jl`, `EpiAwareADTools.jl`,
  `ComposableTuringIDModels.jl`.
- `EpiAwareADTools.jl` describes itself as a home for AD workarounds that are
  deleted once the upstream fix lands. That is a good one-line illustration
  of the AD point on slide 14.
- `GenerationTime.jl` exists but was last pushed 2026-02-05 and has 3 open
  issues. Present generation time as where this is going, not as something
  that ships today.

Not verified, so keep it off the slides or attribute it as recollection:

- "Three hours to replicate EpiNow2." This appears in both source decks but
  there is no record behind it. Either drop it or say "an afternoon" and own
  it as a recollection.
- Any claim about Turing.jl funding or team size.
