# BVDOutbreakSize: material for the roadmap talk

Source repo: `~/code/seabbs/BVDOutbreakSize`, remote
`epiforecasts/BVDOutbreakSize`.
Verified against `origin/main` at commit `536fa1a`
(2026-08-08), which the local clone is checked out to exactly
(no stale branch involved).
Cross-checked against `~/code/seabbs/how-I-llm`, which already
ran a review pass on the same claims (commit `1fceb9a`, "fix:
correct claims the review workflow could not support").
Numbers below are all newer than that pass, re-pulled today,
so they move slightly from the how-I-llm slides.

## What it does, and for which outbreak

A joint Bayesian renewal-process model (Julia, Turing) for the
2026 Bundibugyo virus (BVD) Ebola outbreak in DRC, with exports
to Uganda.
Authors: Sam Abbott, Kath Sherratt, Samuel Brand, Sebastian
Funk.
It is a re-analysis and extension of an Imperial College
London report (McCabe et al., 18 May 2026), built with and
alongside that group, not a competitor to it.
Imperial ran two separate analyses (geographic spread from
Uganda cases, backcalculation from deaths) with fixed nuisance
parameters swept over a grid.
BVDOutbreakSize instead conditions every stream jointly in one
forward-generative model with priors on those nuisance
parameters, giving a single posterior over the latent
cumulative case count.
It is a live report: it re-runs on every push to `main`, tags
a GitHub Release each time with the fitted draws, and the
report changes as new situation reports (SitReps) land.
120 tags exist as of 2026-08-08, i.e. roughly 120 refits since
19 May.

This matches the author's framing: it is squarely a live,
adaptive, multi-source epi model, which is the composable-org
story (EpiAware-style joint modelling), not primarily a Julia
package headline in itself.

## The French sitrep / image-scraping claim: concrete evidence

This holds up, with specifics.

- DRC source is the INSP (Institut National de Santé Publique)
  SitReps for the "17th Ebola epidemic", published in French
  (`https://insp.cd/ebola-17eme-epidemie/`).
  Field names throughout the data files are French: "date de
  rapportage", "cumul cas confirmes", "par date de debut des
  symptomes", etc.
- `scripts/download_sitreps.jl` fetches the SitRep PDFs into
  `data/sitrep_pdfs/`.
- `scripts/confirm_insp_data.jl` regenerates the confirmed-case
  and confirmed-death series from an upstream transcription
  mirror (INRB-UMIE/BDBV2026-Data) and cross-checks them
  against the project's own scan, exiting non-zero on
  disagreement.
- Every other stream (suspected totals, lab cumulatives, daily
  new suspects, isolation occupancy, bed capacity, recoveries)
  is read directly from the SitRep PDFs by an LLM agent, with a
  second agent independently re-scanning, and recorded in
  `data/insp_sitrep_scanned.csv` (70 rows, one per SitRep, up
  to SitRep 082 / 4 August).
- The most striking piece: `scripts/digitize_onset_curve.jl`
  (dependency-free Julia) and `scripts/digitize_onset_curve.py`
  (byte-identical Python port for an automated updater without
  Julia access) digitise a raster bar chart, "courbe
  épidémique par date de début des symptômes", that has no
  underlying data table in the PDF at all, using poppler to
  extract the embedded image and recovering counts from pixel
  colour and axis-tick geometry.
  It writes `data/onset_curve_scanned.csv` (1,781 lines across
  21 scanned vintages, 16 distinct snapshots once reprints are
  collapsed).
  `data/README.md` documents its own error rate against the
  printed total: roughly -5.0% to +1.6% per vintage, and
  documents two concrete pipeline breaks (SitRep 080's caption
  landing on the wrong page and pulling in an unrelated map
  image; SitRep 081's JPEG compression flattening the axis
  ticks so ~10 of 19 were found, undercounting by 54%) that
  were each caught and fixed with a stated diagnosis and a
  stated fix.
  This is unusually good evidence for "with little effort
  ourselves": the doc is explicit that both fixes were verified
  to reproduce every previously-committed block unchanged
  before being accepted, i.e. there was a self-check step, not
  just a patch and move on.

## How many data streams, and how it adapts

`data/observations.toml` has 32 top-level entries: three
Uganda export series (cases, deaths, first-detection date), a
genetic TMRCA bound, and the rest are DRC history series
(reported cases, suspected daily counts and deaths, isolation,
bed capacity, recoveries, treatment admissions/deaths/
ruleout/absconded, tests received/analysed, confirmed cases and
deaths, plus regime-change "break" dates for when INSP changed
its reporting format).
The core joint model (`bvd_joint` in `src/models/joint.jl`)
takes eight count/stream arguments (exports, export deaths,
reported/suspected cases, confirmed cases, tests analysed,
confirmed deaths, recovered cases) plus roughly a dozen more
`*_history` keyword streams, the digitised onset-curve stream,
and explicit breakpoint days for known reporting-format
changes.
There are also eight single-stream composer models (exports
only, deaths only, cases only, confirmed only, treatment only,
onsets only, confirmed-deaths only, exports-deaths only) used
for the "how do the streams compare" sensitivity analysis, so
the same generative core can be run against any one stream in
isolation.

Adaptation to new data is structural, not a rerun with new
numbers bolted on: `as_of_date` in `observations.toml` sets the
cut-off and the literate picks it up with no code change; the
model has an explicit `breakpoint` mechanism for known
regime changes in what INSP publishes (it stopped publishing
national suspected/lab totals after SitRep 013, later resumed
in a different "analytique" format from SitRep 059); and the
news log (`docs/src/news.md`) shows priors being revised in
response to new external evidence mid-outbreak, e.g. v1.13.0
widened the growth-rate prior after a BEAST X genomic
reanalysis (139 genomes) and a field-epidemiology finding
motivated an earlier prior change in v1.12.0.
The model checks itself against its own past releases (refit
at frozen cut-offs and compare to now), against its own past
forecasts (score a week-back projection against what happened),
and against both external groups (McCabe et al., Chamla et
al.).

## Size and authorship (re-verified against origin/main today)

Commits on `main`, 19 May 2026 to 8 August 2026 (442 commits
total):

| Identity | Commits | Share |
|---|---|---|
| Bot identities (`Sam Abbott (bot)` + `seabbs-bot`, both `signin@samabbott.co.uk`) | 336 | 76% |
| `Claude <noreply@anthropic.com>` | 3 | 1% |
| `Sebastian Funk - robot edition` (bot) | 6 | 1% |
| Dependabot | 43 | 10% |
| Sam Abbott, by hand (two personal identities) | 50 | 11% |
| Sebastian Funk / Samuel Brand, by hand | 4 | 1% |

So 345 of 442 commits (78%) are from agent/bot identities, 43
(10%) from Dependabot, and 54 (12%) are human hand-commits.

Pull requests, same window: 367 total, 298 merged, 65 closed
unmerged (18%), 4 open.
By author: `seabbs-bot` 282, `app/dependabot` 47, `seabbs`
(human) 22, `sbfnk-bot` 8, `sbfnk` 4, `sdwfrost` 2,
`kathsherratt` 1, `SamuelBrand1` 1.
Bot identities (`seabbs-bot` + `sbfnk-bot`) opened 290 of 367
PRs (79%).

These are close to, but not identical to, the how-I-llm slide
numbers (390 commits / 291 bot as of 29 July; 353 PRs as of 30
July): the project kept moving in the intervening ten days, as
expected for a live report.
Use today's numbers, not the how-I-llm slide's, if this appears
on its own in the roadmap talk; if reusing the how-I-llm
`bvd-authorship.png` figure directly, keep its own caption
numbers (390 commits / 291 bot, dated 29 July) rather than
relabelling it with today's count.

## The honest downside: long, hard to check, hard to steer

Also holds up, with numbers.

- Code size: `src/` is 12,347 lines across 17 files, `test/` is
  10,548 lines across 64 files, the literate analysis walkthrough
  (`docs/examples/analysis.jl`, which is itself "the main
  artifact" per the repo's own CLAUDE.md) is 3,989 lines, and
  the top-level `scripts/` add another 3,970 lines across 15
  files.
  Over 30,000 lines total for one outbreak model.
- Review burden: 18% of PRs (65 of 367) were closed without
  merging, i.e. proposed and rejected at review.
  AGENTS.md documents that "the full test suite takes a long
  time and a full docs build fits every model, which has hit
  GitHub's six-hour ceiling", and instructs against waiting on
  a local full run, opening PRs early instead and letting CI
  carry the long jobs.
  That is direct evidence the project is slow enough to check
  that the workflow had to be redesigned around it.
- Fit caches go stale on any Turing dependency bump ("Refit
  rather than debugging a `KeyError` on a stale chain"), and
  "any change to the model, the priors or the data needs a
  refit before its results mean anything": there is no cheap
  partial-check path, only a full refit.
- Concrete near-miss: the SitRep 081 onset-curve digitiser
  silently undercounted by 54% (JPEG compression flattened the
  axis ticks) before it was caught, a magnitude far outside the
  stated few-percent noise band; caught because the pipeline
  checks its own output against the printed total on every
  scan, not because someone happened to notice.
- One counterpoint worth being honest about in the other
  direction: test coverage on `main` is 93.93% (3,254 of 3,464
  lines, via the Codecov API, commit `536fa1a`), which is high.
  Worth stating plainly rather than only citing the size
  numbers: the tests were largely written by the same agents
  writing the code, so high coverage is evidence the code does
  what it was told to do, not evidence that what it was told to
  do is correct.
  The failure mode this project has actually hit is silent
  wrong answers (the 081 undercount) rather than crashes, so
  coverage is the wrong metric to lean on for "hard to check".

## Figures worth using on a slide

Two places to look: this repo's own `slides/figures/`, and the
figures already built and reviewed for how-I-llm.

- `~/code/seabbs/BVDOutbreakSize/slides/figures/` — from the
  10 June WHO collaboratory talk, so an early vintage (fit to
  data as of ~7 June).
  `generative-process.svg` (model schematic) and
  `outbreak_streams.png` (per-stream vs joint comparison) are
  vintage-independent enough to reuse; `rt-over-time.png`,
  `size-trajectory.png`, `validation-*.png` are all stale
  (early-outbreak Rt/size numbers that have since moved a lot,
  per the news log).
  Do not use the numbers on the slide deck itself
  (`bdbv_collaboratory_20260610.qmd`, e.g. "2,900-3,800
  infections") without re-checking against the latest release;
  they are ten weeks old.
- `~/code/seabbs/BVDOutbreakSize/output/` on disk is a stale
  local cache (20 May), not the current state.
  Do not pull figures from there.
  The current output lives in the GitHub Release
  (`results-1479`, published 2026-08-08, tag matches
  `536fa1a`) and on the live docs site
  (`epiforecasts.io/BVDOutbreakSize`), not in this local clone.
- `~/code/seabbs/how-I-llm/figures/fig-bvd-model.png` — a
  custom schematic made for that talk, already reviewed, safe
  to reuse as-is.
- `~/code/seabbs/how-I-llm/figures/rt-over-time.png` — carries
  an explicit attribution noting it is a fit to 29 June data
  and that "the live version runs to the latest situation
  report"; reuse the image but keep or adapt that caveat if it
  goes on a slide.
- `~/code/seabbs/how-I-llm/figures/bvd-authorship.png` — the
  reviewed authorship chart (390 commits / 291 bot, 29 July).
  Reuse directly rather than rebuilding from today's numbers
  under time pressure; the two are close enough that relabelling
  risks introducing a new unverified claim.

## Recommendation

Two slides, not one, but tightly scoped.

Slide 1: what it is and why it fits the composable-org story.
Model schematic (`fig-bvd-model.png` or
`generative-process.svg`), the live-report framing (adapts on
every SitRep, 120 releases so far), and the concrete "reads
French PDFs, digitises a chart with no data table" pipeline
detail, which is the single most vivid, checkable claim here
and worth its own bullet rather than folding into a generic
"handles multiple data sources" line.

Slide 2: the honest cost, paired directly against slide 1's
benefit, matching the author's own framing ("hard to check,
hard to steer, but... much better than what we had before").
Authorship chart, the >30,000-line size, the 18%
closed-unmerged rate, and the SitRep 081 near-miss as the
concrete "confident, plausible, wrong" example, closing on why
the composable org (shared standards, shared review tooling
across packages) is the answer to that cost rather than a
reason to avoid this way of working.

Splitting it also avoids diluting the roadmap talk's own
argument: slide 1 is a motivating example for the ecosystem,
slide 2 is a proof point for why the roadmap (standards,
tooling, review workflow) matters, and conflating them onto one
slide would blur which point is being made.
