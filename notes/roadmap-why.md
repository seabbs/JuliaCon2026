# Roadmap talk, the "why"

Source notes for `roadmap/slides.qmd`.
Everything below is either quoted from a file in `~/code`, read from the
GitHub API, or checked against the Julia General registry.
Anything unverified is flagged in the last section.

## Recommended opener

**The epinowcast story, told as a personal failure.**

I set out in 2021 to build the modular version.
The repository description still says so.

> A modular Bayesian framework for real-time infectious disease
> surveillance. Provides tools for nowcasting, reproduction number
> estimation, delay estimation, and forecasting from data subject to
> reporting delays, right-truncation, missing data, and incomplete
> ascertainment

(`gh repo view epinowcast/epinowcast`, created 2021-10-29, 67 stars.)

It was modular in the sense I meant at the time.
Every component had a regression interface.
It was still not reusable.
From the 40 min composability deck, slide "What happens when you try to be
modular? {subtitle=epinowcast}":

> - Cannot easily be separated into reusable parts
> - Difficult for users to contribute to or adapt beyond supported
>   functionality
> - Limited adoption; large API and documentation for users to get to grips
>   with
> - Remains limited in scope despite ambition

Why this works as an opener for a JuliaCon roadmap talk.
It is first person and it admits failure, which buys the audience's
attention before any claim is made.
It states the actual lesson in one line, that the unit of reuse was the
whole model rather than the epidemiological ideas inside it.
That lesson is the entire premise of the roadmap, so the rest of the talk
follows from it without a separate motivation section.

**The evidence to put next to it, if a second slide is wanted.**
EpiNow2 issue [#122](https://github.com/epiforecasts/EpiNow2/issues/122),
"Functionalise stan code", opened by @seabbs on 2020-10-16.

> The stan code is represented partially in functions and partially within
> the main model. Several sections (like the mapping from infections ->
> reports, the GP, update Rt etc) could be easily rewritten into stan
> functions. This would help support future model developments as adding
> extensions/reusing code will be easier.

EpiNow2 issue [#1345](https://github.com/epiforecasts/EpiNow2/issues/1345),
"Add estimate_joint for joint estimation across model components", opened
2026-04-09, still open.

> The current workflow requires users to estimate components separately
> (e.g. estimate truncation, plug that into `estimate_infections`, then use
> those results in `estimate_secondary`). This sequential approach has
> well-known downsides ... The current `epinow()` wrapper orchestrates
> sequential calls rather than fitting a joint model.

Five and a half years between the two, same package, same request, same
person opening it.
That is the argument for changing the substrate rather than the package.

## Source material

### 1. "Why am I so late?" (2024)

`gh api repos/seabbs/presentations/contents/2024/why-am-i-so-late.pdf`,
linked from `2024/README.md` as
<https://samabbott.co.uk/presentations/2024/why-am-i-so-late.pdf>.
Subtitle "Delays and nowcasting for situational awareness".
A local copy is in the scratchpad for this session only, so re-download it
if slides need the figures.

The deck's structure is the roadmap talk's "why" already written down.
It alternates "Where it started", "What went wrong", "Where it ended", five
times over five years.

Slide sequence, verbatim titles.

1. "A review of work over 5 years of outbreaks. Are we being useful? Are we
   getting better?"
2. "Where it started" — Funk, Abbott, Flasche, reporting delays in China,
   Jan 2020, then the CMMID Rt site, then EpiNow 0.3.0.
3. "What went wrong - back sampling delays" — the backcalculation
   evaluation, and Gostic et al. 2020, "Practical considerations for
   measuring the effective reproductive number, Rt".
4. "Where it ended" — EpiNow2, plus "Reflections on two years estimating
   effective reproduction numbers" (Abbott and Funk, 2022,
   doi:10.59350/8apn9-8h048).
5. "What went wrong - right truncation" — German hospitalisation nowcast
   hub, Wolfram et al., leading to epinowcast.
6. "What went wrong - team work" — the epinowcast community site and forum.
7. "mpox - 2022" — Charniga et al., Overton et al., Ward et al.
8. "What went wrong - delay distributions in outbreaks" — Park et al. 2024
   and Charniga et al. 2024 best practices.
9. "Where it ended? Double censoring and right truncation" —
   primarycensored, then epidist.
10. "Mpox clade 1" — three questions, "Are recent delay distribution
    estimates accounting for double censoring and right truncation?", "Are
    real time considerations like delayed reporting and changing
    ascertainment being incorporated into more complex models that are
    being developed?", "If not why not?"
11. "What went wrong - composable modelling" — EpiAware.jl,
    PrimaryCensored.jl, and Nicholson et al., "Interoperability of
    statistical models in pandemic preparedness: principles and reality".
12. "Where its going" — epidist, epinowcast community, EpiAware modules
    (wastewater, viral load, reporting triangle, ODE infection processes,
    deep learning compatibility).

The usable point for the roadmap talk.
Each cycle found a real problem, fixed it, and produced another package
that could not be taken apart.
The loop never terminates because the fix is always a new package.
The "Mpox clade 1" slide is the sharpest version of the failure, because it
asks whether the fixes actually reached the next outbreak, and the implied
answer is no.

### 2. The composability deck, 40 min version

`ComposableProbabilisticIDModels/presentations/40min/index.qmd` under
`/Users/lshsa2/code/EpiAware/`.

Slide "The $R_t$ estimation ecosystem" (lines 272 to 295).

> - At least seven Stan packages estimate $R_t$ using renewal approaches;
>   none share components
> - Some packages share authors yet still duplicate implementations
> - Wastewater $R_t$ tools built by non-wastewater experts, share no
>   components, unclear which choices matter
> - Efforts to share components (e.g. primarycensored) have largely failed
>   to gain adoption by $R_t$ packages
> - Unit of reuse is the whole model, not the underlying epidemiological
>   concepts

Slide "$R_t$ estimation research" (lines 297 to 314).

> - Each typically represents a year or more of PhD/postdoc work for
>   incremental features
> - Much of this effort is duplicated across groups with shared goals
> - Little research directly uses the tools developed by other groups
> - Difficult to communicate across groups as even shared language is
>   lacking

Slide "This pattern repeats across domains" (lines 340 to 354), callout
titled with three emoji.

> 🥱😭😱
>
> Each subdomain rebuilds the same infrastructure from scratch, just with
> different names. And they do it again and again.

Listed domains: delay estimation, nowcasting, viral load modelling,
severity estimation, forecasting and scenario modelling.

Slide "Following the workflow exposes gaps" (lines 392 to 407).
This is the cleanest statement of what the ecosystem has to solve.

> - How to build model components and combine them into joint models
> - Propagating uncertainty correctly across components
> - Diagnosing failures at interfaces between model components
> - Detecting and resolving conflicts between data sources
> - Hybrid inference methods that combine different algorithms for
>   different model components
> - Staged inference for time-sensitive settings
> - Real-time updating as new data arrives

Slide "For the Turing.jl developers" (lines 1041 to 1058) is useful if the
roadmap talk wants a direct ask of the room.

> - **Performance**: nested submodel dispatch is slow; profiling through
>   PPL layers is hard
> - **Submodel interface**: `@submodel` → `to_submodel` broke us;
>   conditioning on nested submodels is limited
> - **Data dimensions**: `condition`/`fix` assumes fixed length;
>   forecasting needs different sized vectors
> - **AD compatibility**: no standards for what AD support a model
>   component needs
> - **Online learning**: streaming data and sequential updating

### 3. The announcement post, the why in his own voice

`gh api repos/EpiAware/epiaware.github.io/contents/news/posts/\
hello-epiaware.qmd`
Published 2026-07-10, author Sam Abbott.
This is the closest thing to a written version of the roadmap talk's "why",
already in the right register, so lines can be lifted almost unchanged.

Three headed reasons.

> **Good data can be spoiled on the way to the answer.**
> The UK Community Infection Survey ran from 2020 to 2023, tested over four
> million swabs from more than 150,000 households, and cost over half a
> billion pounds. External modellers could not see the underlying
> observations, only summarised prevalence estimates. Those estimates
> became inputs to incidence estimates, which became inputs to reproduction
> number estimates, which in turn fed analyses of how transmissible and how
> severe new variants were. At every step the uncertainty was approximated
> and the previous step's assumptions were inherited, with no way to check
> what they cost.

> **Models do not survive contact with the next outbreak.**
> During COVID-19 there were models bringing together case counts,
> prevalence surveys, severity data, and hospital occupancy. When mpox
> arrived in 2022 the data were similar, but contact structure and
> behaviour now needed representing, and those models could not be adapted.

> **We keep rebuilding the same things.**
> At least seven packages estimate the reproduction number using renewal
> approaches in Stan. None of them share components, despite overlapping
> heavily and in some cases sharing authors. The unit of reuse has become
> the whole model, or the whole codebase, rather than the epidemiological
> ideas inside it. The cost shows up as expertise that never lands.
> Wastewater tools have largely been written by people who are not
> wastewater experts, and a wastewater expert who wants to contribute has
> no way in short of writing an entire model themselves.

The funding paragraph is worth a slide on its own, and it is honest in a
way the audience will respond to.

> We think this is worth doing properly, and we have been applying for
> funding to do it. So far without success.
>
> Rather than wait, we have started the organisation and begun building in
> the open, at whatever pace we can manage alongside other work.

And the framing of the ecosystem as plural rather than singular.

> EpiAware is a set of small, interoperable Julia packages rather than a
> single framework. We are not sure which way of composing models will work
> best, so we are trying more than one and keeping them interoperable.

### 4. The workflow paper

`/Users/lshsa2/code/seabbs/a-workflow-for-infectious-disease-modelling/main.tex`

Section `sec:modularise`, "Modularising DAGs", line 278.
The workflow tells you to break the model into sub-models and validate each
one alone before integrating.

> Each sub-model should be as simple as possible, ideally including the
> process DAG and a single observation DAG, therefore depending on a single
> data source.

The discussion then admits the software does not exist to do that.
Line 1030 onward, future work.

> Future progress requires infrastructure that makes it easier to implement
> methodological best practices. ... such tutorials and tools are likely to
> require advances in software composability, where self-contained
> components can be combined to build complex models, to make them
> feasible. This would enable domain experts to contribute specialised
> components without rebuilding core functionality and make all steps of
> our proposed workflow easier to implement.

Also a stated limitation, useful because it is self-critical.

> A significant limitation is that we have not implemented the workflow in
> practice, providing only a schematic case study that illustrates
> conceptual progression rather than actual code or examples.

The argument for the roadmap talk.
We wrote down the workflow, then found we could not follow it with the
tools we had built.
The ecosystem is the attempt to make the workflow followable.

### 5. EpiNow2 issue tracker

Searched with `gh issue list -R epiforecasts/EpiNow2 --search "..."
--state all`.
The complaints are almost all from the maintainers rather than from users,
which is itself the finding.
Users do not ask for extensibility, they ask for features, and the
maintainers convert those into structural work that never lands.

Relevant issues, all verified via the API.

All at `https://github.com/epiforecasts/EpiNow2/issues/<n>`.

| Issue | Opened | Author | State |
|---|---|---|---|
| #122 Functionalise stan code | 2020-10-16 | seabbs | closed |
| #313 Fit series, fold in secondary | 2022-09-22 | sbfnk | closed |
| #600 Time-varying parameters as latent variables | 2024-03-06 | sbfnk | open |
| #792 Support for time-varying ascertainment | 2024-09-24 | seabbs | open |
| #1070 Refactor stan time vars | 2025-04-04 | jamesmbaazam | open |
| #1268 Vendor primarycensored Stan code | 2026-01-28 | seabbs-bot | open |
| #1345 Add estimate_joint across components | 2026-04-09 | seabbs-bot | open |
| #1346 Centralised named delay infra | 2026-04-09 | seabbs-bot | open |

Two details worth a slide.

**#1268, "Vendor primarycensored Stan code".**
Sharing a component between two Stan packages means copying its source into
the downstream package, because Stan has no package manager and no type
system.
That is the concrete technical reason the R and Stan ecosystem cannot
compose, and it contrasts directly with `CensoredDistributions.jl` being a
dependency you add to a `Project.toml`.

**#1345 references #313 from 2022.**
The joint model has been specified in issue form three times across four
years and has never been implemented, because implementing it in the
existing package means rewriting the package.

### 6. Fellowship and grant material

`/Users/lshsa2/code/seabbs/fellowships/README.md` and
`/Users/lshsa2/code/seabbs/fellowships/ideas/composable-building-blocks.md`.
Private planning repo, so nothing from it should be quoted on a slide, but
two lines shape the framing.

> The big team/platform framing ("composable generative modelling") has been
> rejected repeatedly, most recently the Wellcome Discovery resubmission;
> lead instead with a **scientific question + why me**, with composability
> as means.

> **Note:** the team/platform framing has failed repeatedly; lead with the
> question.

Read across to the talk.
Do not pitch the roadmap as a platform.
Pitch it as a question that has not been answered, which is what the
submitted abstract already does, and which matches the deck's closing
"What I want from you" slide.

The `hello-epiaware` funding paragraph is the public, quotable version of
the same fact, so use that on the slide rather than anything from
`fellowships/`.

Do not use anything from the "strategy in five lines" section.
It leads on citation counts and h-index, which are ruled out.

## Multiple ways to do it

The honest position is that nobody knows which of these wins, and the
EpiAware org is currently running at least two of them in parallel.
Source, `gh api repos/EpiAware/epiaware.github.io/contents/approaches/\
index.qmd`.

> We are not sure yet which of these will work best, so we are trying more
> than one and keeping them interoperable. Both work with the same
> underlying packages, and they can be combined in a single analysis.

### Route A, composable `Distributions.jl` objects

No probabilistic programming language required.
A composed delay is an ordinary `Distributions.jl` distribution, so it
works anywhere a distribution works.

From `ComposedDistributions.jl`'s README.

> - Every leaf is an ordinary Distributions.jl distribution, so nothing
>   needs reimplementing to compose it, and the composed result is itself a
>   distribution that drops into code expecting one.
> - A composed tree is inspectable, editable data — a parameter table, a
>   nested prior, a rendered tree — rather than an opaque function.

Five composers, `sequential`, `parallel`, `resolve`, `compete`, `choose`.
`rand` simulates a case, `logpdf` scores an observed one, from one object.

**Trade-off.**
Strongest where the model is a natural history of one case and the data are
individual level.
It has no story for a time series, a renewal process, or a latent infection
trajectory, because those are not distributions over a record.
`DistributionsInference.jl` exists precisely because this route needs its
own fitting layer once you leave a PPL, and that layer is now a package we
maintain rather than one we borrow.

### Route B, Turing submodels

`ComposableTuringIDModels.jl`.
Three roles, a prior model, an infection model, an observation model.

> Every part is a plain struct with a single method of `as_turing_model`,
> which returns a `DynamicPPL.Model`. There is no deep type hierarchy, and
> a part is identified by the method it implements rather than by its place
> in a tree.

**Trade-off.**
This is the route that gets joint inference for free, and the full Turing
toolchain with it.
It also inherits everything on the "For the Turing.jl developers" slide.
Nested submodel dispatch is slow, profiling through the PPL layers is hard,
the `@submodel` to `to_submodel` change broke the package, and
`condition`/`fix` assume fixed-length data, which forecasting violates.
It ties the ecosystem's fate to one PPL's design decisions.

### Route C, SciML and dynamical systems

`LoweredDistributions.jl` is the bridge, and it is already built.

> A delay distribution and a compartmental model are two views of the same
> thing; `lower` gives you the compartmental view without hand-deriving the
> generator each time.
>
> Four backend extensions (Catalyst, SciMLBase, JumpProcesses,
> AlgebraicPetri) share the same lowering, so switching simulation or
> inference backend does not mean re-deriving the dynamical system.

**Trade-off.**
Gets the whole SciML ecosystem, solvers, sensitivity, GPU, without
rebuilding any of it.
Composition of dynamical systems is not the same problem as composition of
probability models, so the inference story has to be supplied separately.
Lowering is exact only where the maths allows it, and moment matching is a
documented fallback rather than a guarantee.

### Route D, plain hand-written models

Write the Turing or Stan model directly for the problem in front of you.

**Trade-off.**
Fastest to a first answer, and the honest baseline that every alternative
has to beat.
It is what everybody already does, and it is why there are at least seven
renewal packages that share nothing.
The cost is not visible in any single project, only in the aggregate, which
is why it keeps being chosen.

### Route E, the ones we are not doing

From the 40 min deck, slide "Alternative approaches".

> - Category theory / AlgebraicJulia provide formal compositional
>   guarantees but limited support for probabilistic modelling
> - Stan optimised for complete models; Gen.jl lower-level; NumPyro/JAX
>   promising but barriers for epidemiological modellers
> - Declarative graph-based PPLs (JuliaBUGS, RxInfer) trade flexibility for
>   structure
> - Symbolic-numeric frameworks (ModelingToolkit.jl) offer automated
>   optimisation
> - Agent-based approaches (Starsim, EpiABM) have made the most progress
>   toward calibration but challenges remain

### How to present the trade-off

One slide, four rows, no winner declared.
The point is that the roadmap is a bet on Julia, not a bet on any one of
these routes, and that the reason Julia is the bet is that it is the only
place where all of these routes can share the same `Distributions.jl`
objects and the same AD backends.
Ask the room which one they would pick and why.

## Verified facts, safe to use

Checked against the GitHub API or the Julia General registry on
2026-08-10.

- `epinowcast/epinowcast` created 2021-10-29, 67 stars, described as
  "A modular Bayesian framework for real-time infectious disease
  surveillance".
- `epiforecasts/EpiNow2` created 2020-06-17, 140 stars.
- EpiNow2 issue numbers, dates, authors and states in the table above.
- The EpiAware org has 12 public Julia packages plus a private
  `ReproductionNumber.jl`.
  Public: `CensoredDistributions.jl` (created 2024-09-24),
  `ReparameterisedDistributions.jl` (2024-06-04),
  `ModifiedDistributions.jl` (2025-08-14), `LoweredDistributions.jl`
  (2026-02-05), `GenerationTime.jl` (2026-02-05),
  `EpiAwarePackageTools.jl` (2026-06-25), `ComposableTuringIDModels.jl`
  (2026-06-26), `ComposedDistributions.jl` (2026-07-03),
  `ConvolvedDistributions.jl` (2026-07-04), `EpiAwareADTools.jl`
  (2026-07-11), `ScoringRules.jl` (2026-07-15),
  `DistributionsInference.jl` (2026-07-17).
- Ten of those are registered in the Julia General registry.
  `ScoringRules` and `GenerationTime` are not, checked via
  `raw.githubusercontent.com/JuliaRegistries/General`.
- `CensoredDistributions.jl` CI runs six AD configurations, ForwardDiff,
  ReverseDiff tape, Enzyme forward, Enzyme reverse, Mooncake reverse and
  Mooncake forward, each with its own codecov flag.
  That is a concrete answer to "what does a good package in this ecosystem
  look like".
- The talk's own submitted abstract says "So far, we have
  CensoredDistributions.jl ... and an R interface prototype (EpiAwareR)".
  That is out of date by eleven packages.
  Say so on a slide rather than repeating the abstract.

## Do not claim without checking

- "At least seven Stan packages estimate $R_t$ using renewal approaches."
  This appears in the deck, the paper and the announcement post, but the
  seven are never named in any of them.
  Either name them on the slide or say "several".
- The ONS CIS figures, over four million swabs, more than 150,000
  households, over half a billion pounds.
  Taken from the announcement post and the 40 min deck.
  Not independently checked against an ONS source here.
- "Took 3 hours to replicate EpiNow2 by composition."
  From the case study decks.
  Not reproducible from anything in this session.
- Any download, adoption or user count for the R packages.
  The badges in the READMEs are live queries, so the numbers change.
- Anything about citations, h-index or academic metrics.
  Ruled out.
