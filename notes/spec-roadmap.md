# Roadmap deck: full rebuild

This replaces the earlier spec entirely. Read `notes/style.md` first.

The author has given a slide-by-slide running order. Follow it. Where he names
a slide, that is a slide.

## 0. Opener: we are already doing this

> Somewhere I want "we are already using Julia for outbreak modelling in the
> DRC" (full name of the virus and country), supported by LLMs pulling data
> directly from PDF sitreps, fitting to multiple data sources with Mooncake
> AD (despite best efforts and many tokens Enzyme continues to be a failure).
> BVDOutbreakSize repo has some slides with plots. I think as an exciting wow
> we might want that as an opener slide? We want it to have "wow why cool
> Julia helps us" elements but also "wow so much code and jank" elements. Only
> 5 bullets max and ideally several figures.

Open on the real outbreak, not on an agenda. Use the full names: **Bundibugyo
virus disease**, **Democratic Republic of the Congo**.

Both halves must land. The wow: real time, multiple data streams fitted
jointly, sitrep PDFs read automatically, Mooncake gradients through the whole
thing. The jank: a great deal of generated code, hard to review, and Enzyme
still failing after a lot of effort and tokens.

Five bullets maximum. Several figures. Candidates already on disk in
`/Users/lshsa2/code/seabbs/BVDOutbreakSize/slides/figures/`:
`outbreak_streams.png`, `rt-over-time.png`, `size-trajectory.png`,
`insp_sitreps.png` (the sitrep ingestion), `generative-process.svg`,
`validation-mccabe.png`. Copy what you use into `figures/`.

This may need a two or three panel layout rather than the usual 40/60 split.
That is allowed here.

## 1. What we need, one slide

Start from `epiaware.org` needs. One slide only, linking to the 16:45 talk for
the argument. Do not re-run the case for composability here.

## 2. Approach one, with code

`ComposableTuringIDModels.jl`. Include the code example from
<https://epiaware.org/approaches/composable-turing-models.html>.

## 3. Approach two, with code

The distributions extension approach. Code example from
<https://epiaware.org/approaches/composed-distributions.html>.

## 4. Maybe other approaches

Briefly. SciML lowering, and a model written by hand as the baseline.

## 5. Some inspiration

Replace the current four-way comparison and its table. Three bullets, nothing
else:

- Turing, one bullet
- SciML, one bullet
- rOpenSci, one bullet

> no additional test needed

means do not add the R versus Julia forum and seminar counts table. Cut it.

## 6. I tried in R

Replace "We had that in R, and it does not come apart".

> I tried in R, then list the packages (with GitHub stars and downloads).
> "Reused as" is weird, not sure we need it.

So: a table of the R packages with **GitHub stars and download counts**, and
**drop the "Reused as" column**. Verify every number from the GitHub API and
CRAN, with a retrieval date.

Keep the point that epinowcast was started in 2021 to be the modular one and
still cannot be taken apart, and the four EpiNow2 issues.

## 7. What do we need to implement this?

A transition slide. Then, before the agents slide:

- **Funding.** We have tried several times for grants of a few million, and
  met a lot of Julia scepticism.
- **A small team.** At least a few people.
- **Buy-in from others.**

## 8. The agents slide

The existing one. Keep the pull request plot over time. Add a **Claude Max
subscription** as the honest answer to how it is being done now, and end on a
bullet saying we still need funding, any ideas.

## 9. Transition: our current approach

A bullet slide listing five things, then **at least one slide for each**:

1. As much infrastructure as possible
2. Automatic differentiation as a first class citizen
3. Good to great docs, and making sure they work
4. A community of contributors
5. Good governance

### 9.1 Infrastructure

- A central `.github` supplying CI.
- `EpiAwarePackageTools.jl` as its own package slide.
- Trying to replace R's `CRAN check` in Julia. Aqua and the rest, with a
  subtitle about going beyond it.
- No reverse dependency checks in Julia. SciML does some internally. How we
  avoid endless breaking.

### 9.2 Automatic differentiation

- Standardised AD testing and benchmarking via `DifferentiationInterfaceTest`.
- `EpiAwareADTools.jl` for AD fixes, for example the `SpecialFunctions`
  problems. Keep the `xlogy` wrong-gradient example, it is the best evidence
  in the deck.

### 9.3 Docs

Keep the existing documentation-as-a-failing-test slide.

### 9.4 Community, in the age of robots

- How does a community work now? Talking to robots is dispiriting.
- It is unclear which repositories want robot-filed issues at all.
- `EpiAwareAgents` as one possible answer: a community bot available to any
  maintainer. **Say plainly that it does not work and is still a sketch.**

### 9.5 Governance

- What does good governance look like?
- How do we manage whale contributors? Every previous project he has worked on
  has had this problem. He started epinowcast in 2021 partly to avoid what
  happened with EpiNow2, and it did not work.
- Is Julia's composability magic enough on its own? Julia still has whales.
  **Use emojis here.** His instruction.
- How do you attract users who do not care about multiple dispatch, or any
  other Julia magic? They want things to work, and they usually have little
  time and less resource, especially in R and in outbreak settings.

## 10. Close

Keep the four questions slide.

## Explicit removals

Cut these, by his instruction:

- "Eleven packages, three ways to compose them" (backup slide)
- "Eleven packages, and four questions"
- "What ships next"
- "What the language buys us"
- "Nobody can tell you which backend a model needs"

## Constraints

- 15 minute slot. The deck currently runs 8 to 10 minutes, so this rebuild has
  room, but it is adding a lot of slides. Count at the end and report.
- No editorial asides in attribution blocks. See `notes/style.md`.
- Every number verified, with a retrieval date.
