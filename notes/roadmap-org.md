# EpiAware org: factual state for the roadmap talk

Checked 2026-08-10.
All counts below were taken from the GitHub API (as `seabbs-bot`), the local
General registry cache (`~/.julia/registries/General.tar.gz`, downloaded
2026-08-10 11:35), and the local clones under `/Users/lshsa2/code/EpiAware/`.
Anything I could not check against one of those is under "Claimed, not
verified".

---

## 1. Repos versus registered packages

### Verified

`gh repo list EpiAware --limit 200` returns **22 repositories**.
19 are public and 3 are private (`ComposableProbabilisticIDModels`,
`EpiAwareAgentReports`, `ReproductionNumber.jl`).

Of those 22, **11 contain a Julia package** (a `Project.toml` with a `uuid`).
**10 of the 11 are in the General registry.**
The gap is `ScoringRules.jl`, which has code and CI but no registry entry and
no git tag.

Two repos exist in name only.
`GenerationTime.jl` and `ReproductionNumber.jl` both return
`"Git Repository is empty"` from the commits API.
They were created on 2026-02-05 and have never been pushed to.

The remaining 9 repos are not packages: `.github`, `epiaware.github.io`,
`tutorials`, `EpiAwareAgents`, `ProjectProposals`, `talks`, `JuliaForIDM`,
`ComposableProbabilisticIDModels`, `EpiAwareAgentReports`.

So the honest headline is **22 repos, 11 Julia packages, 10 registered, 2
empty placeholders**.

Registry state, from `General.tar.gz` `Versions.toml` files:

| Package | Registered versions | Latest registered | GitHub releases | Tags |
|---|---|---|---|---|
| CensoredDistributions | 25 | 0.2.22 | 25 | yes |
| ConvolvedDistributions | 5 | 0.4.0 | 4 | yes |
| EpiAwarePackageTools | 3 | 0.3.0 | 3 | yes |
| EpiAwareADTools | 3 | 0.1.2 | 3 | yes |
| ComposableTuringIDModels | 2 | 0.1.1 | 2 | yes |
| ComposedDistributions | 2 | 0.1.1 | 2 | yes |
| ReparameterisedDistributions | 2 | 0.2.0 | 2 | yes |
| DistributionsInference | 1 | 0.1.0 | 0 | none |
| LoweredDistributions | 1 | 0.1.0 | 1 | v0.1.0 |
| ModifiedDistributions | 1 | 0.1.0 | 0 | none |
| ScoringRules | **0 (not registered)** | — | 0 | none |

`DistributionsInference` and `ModifiedDistributions` are registered but carry
no git tag or GitHub release yet.

`EpiAwarePrototype.jl` no longer appears in the org listing.
`gh api repos/EpiAware/EpiAwarePrototype.jl` redirects to
`EpiAware/ComposableTuringIDModels.jl`, and both share the UUID
`cbebd14a-101c-4997-a79f-d008ad7c07b2`, so the prototype was renamed.
A stale clone of the old name still sits in `/Users/lshsa2/code/EpiAware/`.

Approximate commit counts on `main` (GitHub pagination, so nearest 100 is
exact only where shown):

| Package | Commits on main |
|---|---|
| EpiAwarePackageTools.jl | ~319 |
| ConvolvedDistributions.jl | ~301 |
| CensoredDistributions.jl | ~277 |
| ComposedDistributions.jl | ~259 |
| ComposableTuringIDModels.jl | ~237 |
| DistributionsInference.jl | ~138 |
| ModifiedDistributions.jl | ~103 |
| ReparameterisedDistributions.jl | ~97 |
| EpiAwareADTools.jl | ~67 |
| LoweredDistributions.jl | 66 |
| ScoringRules.jl | 45 |

### Claimed, not verified

Nothing here is claimed.

---

## 2. EpiAwarePackageTools.jl

### Verified

Registered, at v0.3.0, created 2026-06-25.
Roughly 8,600 lines of Julia in `src/`, of which `scaffold.jl` alone is 3,367
lines and `docs_build.jl` is 2,228.

Two entry points.
`scaffold(pkgdir(MyPackage))` writes the standard tooling into a package once.
`EpiAwarePackageTools.update(pkgdir(MyPackage))` re-applies the managed files
later and reports drift, and a scheduled `template-sync.yaml` workflow runs
that automatically, so a change made once in the kit reaches every adopting
package.

**Adoption.**
10 of the 11 Julia packages carry `.github/workflows/template-sync.yaml` on
`main` (checked one repo at a time via the contents API).
The single exception is `CensoredDistributions.jl`, which is the package the
tooling was generalised out of and which is still migrating.
It has the same workflow set by hand (`ad.yaml`, `test.yaml`, `document.yaml`,
`pre-commit.yaml`, `codecoverage.yaml`, `TagBot.yaml`, `try-this-pr.yaml`,
`version-on-demand.yaml`, `auto-version-increment.yaml`,
`docpreviewcleanup.yaml`, `benchmark.yaml`, `claude.yml`,
`claude-code-review.yml`) but no `template-sync.yaml` and no dependency on the
kit.
Open issue `EpiAware/CensoredDistributions.jl#881`, "Adopt the
EpiAwarePackageTools quality.jl/build_docs scaffold generation (reference is
behind the kit)", is the tracking issue.

**What the template writes.**
`templates/` holds 76 files.
`SCAFFOLD_TEMPLATES` in `src/scaffold.jl` lists them with a managed flag; most
are marked force-managed, meaning `update` overwrites them on every sync and a
package cannot drift.
The GitHub Actions callers written into every adopting package are:

`test.yaml`, `ad.yaml`, `document.yaml`, `pre-commit.yaml`,
`codecoverage.yaml`, `docpreviewcleanup.yaml`, `TagBot.yaml`, `Register.yml`,
`downstream.yaml`, `registrability.yaml`, `release-nudge.yaml`,
`cancel-on-close.yaml`, `try-this-pr.yaml`, `claude.yml`,
`claude-code-review.yml`, `template-sync.yaml`, `benchmark.yaml` (opt-in),
`benchmark-history.yaml` (opt-in), `auto-version-increment.yaml`,
`version-on-demand.yaml`, plus a composite action
`.github/actions/increment-version/action.yaml`.

These are thin callers into 23 reusable workflows in `EpiAware/.github`
(`ad.yml`, `ad-backend.yml`, `tests.yml`, `documentation.yml`, `coverage.yml`,
`downgrade.yml`, `downstream.yml`, `format-check.yml`, `runic-check.yml`,
`register.yml`, `registrability.yml`, `release-nudge.yml`, `tagbot.yml`,
`major-version-tag.yml`, `template-sync.yml`, `try-this-pr.yml`,
`version-increment.yml`, `benchmark.yml`, `benchmark-history.yml`,
`cancel-on-close.yml`, `docs-preview-cleanup.yml`, `claude.yml`,
`claude-code-review.yml`).
Each caller pins the reusable to a commit SHA held as a constant in
`scaffold.jl` (e.g. `_DOWNGRADE_SEED_REF`, `_REGISTRABILITY_SEED_REF`).

**What is enforced, concretely.**
Formatting is SciML style, pinned.
`templates/.JuliaFormatter.toml` is two lines, `style = "sciml"`, marked
"MANAGED — do not edit by hand", and JuliaFormatter is pinned to 2.10.1 by
`_JULIAFORMATTER_VERSION`, which feeds the pre-commit hook `rev`, the isolated
formatter test environment, and the CI input together.

Julia support is pinned by `_JULIA_FLOOR = v"1.11"`, `_JULIA_COMPAT =
"1.11, 1.12"`, and a CI matrix of `["1", "pre"]`.

`.pre-commit-config.yaml` is managed and runs large-file, YAML, TOML, JSON,
merge-conflict, debug-statement, end-of-file, mixed-line-ending and
trailing-whitespace checks, a local hook forbidding the `|||||||` diff3 base
marker, the JuliaFormatter hook, and `detect-secrets` against a
`.secrets.baseline`.

The managed `test/package/quality.jl` runs nine test items, all tagged
`:quality`: Aqua, ExplicitImports, import centralisation, docstring format,
**README sections**, doctest, formatting, JET linting, and extension
ambiguities.
JET and the formatter each run in their own isolated environment
(`test/jet/`, `test/formatter/`) so the checked version cannot drift with
whatever the shared test environment resolves.

The README check is the clearest evidence of rigidity.
`STANDARD_README_SECTIONS` requires, in order, a Why/Overview section, a
Getting started section, **Related packages**, Documentation, Contributing, and
a Citing/License section, and `update` re-renders a managed block of standard
sections between `<!-- standard-sections:start -->` markers in every package's
README.
There is also `BANNED_README_WORDS`, a test that fails a package's README if
its prose contains any of: comprehensive, cornerstone, current approaches,
facilitate, foster, framework, harness, landscape, leverage, multifaceted,
novel, nuanced, overarching, pivotal, practitioner, robust, streamline,
synergy, utilise, utilize.
Regex inflection handling is written out for the awkward ones
(`novel(?:s|ly|ty|ties)?`, `synerg(?:y|ies|...)`).
So the org's writing style is a failing test, not a guideline.

The managed/package-owned split is explicit in each file's header comment.
Managed files say "MANAGED by EpiAwarePackageTools.scaffold — do not edit by
hand".
Package-owned files say "PACKAGE-OWNED — scaffold writes this once and never
overwrites it".
`test/ad/scenarios.jl`, `test/ADFixtures/`, and `test/package/qa_config.jl`
are package-owned; `test/ad/setup.jl`, `test/ad/runtests.jl` and
`test/package/quality.jl` are managed.

### Claimed, not verified

The author's view that "Julia's default standards are sloppy and most
templates are modular where mine is rigid" is a position, not a fact.
The verifiable part is the force-managed file list and the failing-test
enforcement above.

---

## 3. EpiAwareADTools.jl

### Verified

Registered, v0.1.2, created 2026-07-11, ~67 commits.
About 1,450 lines across `src/` and `ext/`.
Source files: `ad_safe.jl`, `beta_ad.jl`, `gamma_ad.jl`, `primal.jl`,
`nondifferentiable.jl`, `logsumexp_stream.jl`.
Seven package extensions: ChainRulesCore, Enzyme, ForwardDiff,
LogExpFunctions+Mooncake, Mooncake, ReverseDiff, SurvivalDistributions.

It is **not** a wrapper around DifferentiationInterfaceTest.
It is the library of AD workarounds; the gradient-testing machinery lives in
EpiAwarePackageTools (`src/ad_harness.jl`, 225 lines).
Framing in its own README is "fixes we host while we try to fix things
upstream", with each entry documented against the upstream issue it should
move to and deleted when that lands.

Three families of workaround:

1. `primal` and `primal_distribution` strip an AD wrapper back to the
   underlying value, keeping a non-differentiable hyperparameter off the AD
   path on every backend.
2. `cdf_ad_safe`, `logcdf_ad_safe`, `ccdf_ad_safe`, `logccdf_ad_safe`,
   `pdf_ad_safe`, which are extension points other packages overload.
   The `Gamma` methods route through an analytic gamma-CDF derivative because
   `SpecialFunctions.gamma_inc` is not differentiable; the `Beta` methods do
   the same for `beta_inc`'s missing shape-parameter derivatives.
3. Correct upstream `ChainRulesCore` rules lifted into a backend that lacks
   them, currently `LogExpFunctions.xlogy`/`xlog1py` under Mooncake, which
   otherwise returns a wrong shape gradient for a Gamma log density at
   `shape == 1`.

That last one is the strongest example of the argument: a wrong gradient, not
an error.

Five packages depend on it in their `Project.toml` on `main`:
CensoredDistributions, ConvolvedDistributions, ComposedDistributions,
ModifiedDistributions, DistributionsInference.
ReparameterisedDistributions, LoweredDistributions, ComposableTuringIDModels
and ScoringRules do not.

**What EpiAwarePackageTools adds on top of DifferentiationInterfaceTest**
(this is the "more" in the brief, and it is in `src/ad_harness.jl`):

- An `ADRegistry` duck-typed contract, so the run logic lives once in the kit
  and only the scenarios stay in each package.
- Optional per-backend bookkeeping accessors `broken_scenario_names`,
  `backend_broken_scenarios`, `backend_skip_scenarios`, absent means none.
- `check_broken`, which runs a scenario through plain
  `DifferentiationInterface.gradient` and records `@test_broken` rather than a
  failure, so a partly working backend is not all-or-nothing.
  A scenario declared broken that starts passing is flagged, so declarations
  cannot go stale.
- `test_working_backend` splits the scenarios into the ones a backend handles
  (hard-tested through `DIT.test_differentiation`, correctness only,
  `type_stability = :none`, `rtol = 5e-2`, `atol = 1e-6`) and the declared
  broken ones (routed to `check_broken`).
  It defaults `scenario_intact = false` because a `Missing`-bearing context
  trips DIT's post-run equality check while the gradients themselves are
  correct.
- `test_partial_backend` for a backend that cannot survive a full
  `test_differentiation` sweep at all.
- `ad_backend_support_table`, which renders the per-backend supported/broken/
  skipped table at docs-build time from the same registry the tests read, so
  the published table cannot drift from what CI marks broken.
- One list, `_AD_BACKENDS` in `scaffold.jl`, generates the CI matrix, the
  codecov flags, the README coverage badge table, the starter test items and
  the AD dependency list, and the matrix is passed to the reusable workflow
  explicitly rather than defaulted, so CI cannot drift from the badges.
- Per-backend `@testitem` tags, so a transiently unstable backend reds only
  its own job, and `TAG=enzyme_reverse task test-ad-backend` reproduces one CI
  job locally.

ForwardDiff doubles as the reference gradient for every scenario.

### Claimed, not verified

"No AD backend is reliably best, all are flaky or run by small teams" is the
author's judgement.
The supporting facts available are the broken-scenario declarations and the CI
states below.

---

## 4. AD backends in CI, and current state

### Verified

Six backends across four AD packages, from `_AD_BACKENDS`:
ForwardDiff, ReverseDiff (tape), Enzyme forward, Enzyme reverse,
Mooncake reverse, Mooncake forward.

`CensoredDistributions.jl`, latest `ad.yaml` run on `main`
(run 31051815344, 2026-08-05), per job:

| Backend | Job conclusion |
|---|---|
| ForwardDiff | success |
| ReverseDiff (tape) | success |
| Enzyme forward | success |
| Enzyme reverse | success |
| Mooncake reverse | success |
| Mooncake forward | success |

All six are green, but that is green **because two failures are declared**.
`test/ADFixtures/src/ADFixtures.jl` on `main` declares:

```julia
"Enzyme reverse" => Set{String}([
    "convolve_series IntervalCensored LogNormal daily grid"]),
"Enzyme forward" => Set{String}([
    "convolve_series IntervalCensored LogNormal daily grid"])
```

with the comment that both Enzyme directions fail that scenario on the stacked
`IntervalCensored{Truncated{PrimaryCensored}}` type, every other backend
passes, and it was investigated and unresolved, tracked as issue #889.
`broken_backends()` and `broken_scenario_names()` are both empty, and the
docstring records the history: `IntervalCensored Gamma arbitrary` used to fail
on every backend because it routed through `Distributions.cdf(Gamma, x)` into
`gamma_inc`, and now routes through a `_gamma_cdf` helper.

Latest `ad.yaml` run on `main` across the org:

| Package | Latest AD run on main | Date |
|---|---|---|
| CensoredDistributions.jl | success | 2026-08-05 |
| ModifiedDistributions.jl | success | 2026-08-05 |
| ComposableTuringIDModels.jl | success | 2026-08-07 |
| EpiAwareADTools.jl | success | 2026-08-08 |
| DistributionsInference.jl | success | 2026-08-10 |
| ScoringRules.jl | success | 2026-07-23 |
| **ComposedDistributions.jl** | **failure (all six jobs)** | 2026-08-07 |
| LoweredDistributions.jl | cancelled | 2026-08-04 |
| ConvolvedDistributions.jl | in progress | 2026-08-10 |
| ReparameterisedDistributions.jl | in progress | 2026-08-10 |

`ComposedDistributions.jl` fails on all six backends at once, which reads as
an environment or load failure rather than a per-backend gradient problem.
I did not open the logs to confirm which.

`ScoringRules.jl` has open AD issues that make the same point from the other
direction: #11 "Gamma, GEV and Poisson crps are not ForwardDiff-differentiable
(gamma_inc has no Dual method)" and #6 "Student-t CRPS (and Beta/LogLogistic)
aren't AD-differentiable — beta_inc/cdf(TDist) don't propagate dual numbers".

### Claimed, not verified

I did not read CI logs, so I cannot say why ComposedDistributions fails.
Do not put a cause on a slide.

---

## 5. The planned package set, mapped to what exists

### Verified

**Distribution extensions** (all registered, all with docs):

| Package | Reg. | Rel. | Commits |
|---|---|---|---|
| CensoredDistributions.jl | 0.2.22 | 25 | ~277 |
| ConvolvedDistributions.jl | 0.4.0 | 4 | ~301 |
| ComposedDistributions.jl | 0.1.1 | 2 | ~259 |
| ModifiedDistributions.jl | 0.1.0 | 0 | ~103 |
| ReparameterisedDistributions.jl | 0.2.0 | 2 | ~97 |
| LoweredDistributions.jl | 0.1.0 | 1 | 66 |

What each does, in one line.
CensoredDistributions covers primary and interval censoring and truncation.
ConvolvedDistributions gives `convolved`, `difference`, `product`, `ratio`
and `convolve_series`.
ComposedDistributions gives chains, branches and `one_of` natural histories.
ModifiedDistributions gives weighted, rescaled and hazard-shifted wrappers.
ReparameterisedDistributions gives mean/sd and other parameterisations.
LoweredDistributions gives `lower`, a delay as a compartmental generator.

`CensoredDistributions.jl` is by some way the most mature: 15 stars, 25
registered versions, and it is the only package with `docs-stable` published
under the old `epiaware.github.io/CensoredDistributions.jl/` path.

**Delay and generation time estimation.**
`DistributionsInference.jl` (registered 0.1.0, ~138 commits, no tag yet) is
the fit protocol.
Its stated position is that a distribution declares its scalar parameters as
a table of rows carrying name, value, prior and support, and
`distribution_to_logdensity` turns that plus data into a `LogDensityProblems`
problem any sampler can drive.
`GenerationTime.jl` **is an empty repository** and has been since 2026-02-05.

**Disease dynamics.**
`ComposableTuringIDModels.jl` (registered 0.1.1, ~237 commits), renamed from
`EpiAwarePrototype.jl`, is the composable infection plus observation model
layer on Turing.
`ReproductionNumber.jl` **is an empty private repository**, created
2026-02-05, never pushed to.

**Forecast evaluation.**
`ScoringRules.jl` (~45 commits, **not registered**, no tags) is a port of the
R `scoringRules` package by Jordan, Krüger, Lerch and Allen, distributed under
GPL-2.0-or-later to match, with the test suite checked against reference
values generated from R.
Note there is a second `ScoringRules.jl` on GitHub (`jcm-sci/ScoringRules.jl`,
0 stars, last pushed 2026-04-08) with the same intent, and neither is in the
General registry.

So the four planned areas map to: distribution extensions, six packages, all
registered; delay/generation time, one registered package plus one empty repo;
disease dynamics, one registered package plus one empty private repo; forecast
evaluation, one unregistered package.

### Claimed, not verified

Whether `GenerationTime.jl` and `ReproductionNumber.jl` are still intended, or
are leftovers from February, is not something I can establish from the repos.
Treat them as placeholders on a slide, honestly labelled.

---

## 6. epiaware.github.io / epiaware.org

### Verified

`epiaware.github.io` is a Quarto site, not a Julia docs build.
Its `CNAME` is `epiaware.org` and `https://epiaware.org` returns 200.

Pages: `index.qmd`, `packages/`, `docs.qmd`, `tutorials.qmd`, `gallery.qmd`,
`team.qmd`, `funding.qmd`, `get-involved.qmd`, `community.qmd`,
`using-julia.qmd`, `faq.qmd`, `contributing.qmd`, `developer.qmd`, plus light
and dark SCSS themes.

`docs.qmd` is a documentation browser that loads each package's own site in an
iframe from an `EPIAWARE_DOCS` list.
That list currently has **four** entries: CensoredDistributions,
ConvolvedDistributions, ComposedDistributions, EpiAwarePackageTools.
`packages/` has **five** package pages plus a `_template.qmd`
(censoreddistributions, composeddistributions, convolveddistributions,
epiawarepackagetools, reparameteriseddistributions).
So the site is well behind the 11 packages that exist.

Per-package docs are served under subdomains of `epiaware.org` and are live.
Checked, all 200:
`censoreddistributions.epiaware.org/stable/`,
`epiawarepackagetools.epiaware.org/stable/`,
`epiawareadtools.epiaware.org/stable/`,
`convolveddistributions.epiaware.org/stable/`.

`EpiAware/tutorials` is a separate Quarto site on `tutorials.epiaware.org`
(200), and its `tutorials/` directory currently contains a single `index.qmd`,
so it is a shell.

Adding a package is documented as copying `packages/_template.qmd` and adding
a one-line entry to `EPIAWARE_DOCS`.

### Claimed, not verified

Nothing.

---

## 7. EpiAwareR

### Verified

It is not in the EpiAware org.
It is `sbfnk/EpiAwareR`, public, described as "R interface to EpiAware.jl".
Created 2025-10-22.
Last commit 2026-05-05, repo last pushed 2026-06-22.
Over 100 commits (first page of the commits API is full).

It has the shape of a real R package: `DESCRIPTION`, `NAMESPACE`, `R/`, `man/`,
`tests/`, `vignettes/`, `inst/`, `NEWS.md`, `CITATION.cff`, `.Rbuildignore`,
`.github/`.
It is not on CRAN as far as I checked, and I did not check r-universe.
It targets "EpiAware.jl", a package name that no longer exists in the org, so
it predates the split into the current package set.

### Claimed, not verified

Whether it currently works against the present packages.
I did not run it.
Describe it as a prototype by Sebastian Funk, roughly three months stale, and
predating the current package layout.

---

## 8. Other org context

### Verified

`EpiAwareAgents` (~Python, last push 2026-07-30) holds the configuration for
an agent fleet meant to run routine org maintenance.
Its README says explicitly **"Status: design phase. Nothing here runs yet."**
Design principle 1 is "Assume every prompt injection succeeds; make the damage
boring anyway".
`EpiAwareAgentReports` is the private repo the reports would go to.

`JuliaForIDM` is a teaching repo, last pushed 2025-12-05.
Star counts, highest first: CensoredDistributions.jl 15, JuliaForIDM 9,
ComposableProbabilisticIDModels 5 (private), ReparameterisedDistributions.jl 3,
ComposableTuringIDModels.jl 3, and everything else 0 or 1.

`ProjectProposals` and `talks` exist but `ProjectProposals` has not been
pushed to since it was created on 2026-02-05.

### Note on avoiding a metrics slide

Star counts are in this file for context only.
Per the brief, do not put them on a slide.

---

## Sources

- `gh repo list EpiAware --limit 200 --json ...`
- `gh api repos/EpiAware/<repo>/...` for contents, releases, tags, commits
- `gh run list -R EpiAware/<repo> --workflow ad.yaml --branch main`
- `gh run view <id> --json jobs`
- `~/.julia/registries/General.tar.gz` (fetched 2026-08-10 11:35)
- Local clones under `/Users/lshsa2/code/EpiAware/`
- `curl -I` against the `epiaware.org` docs subdomains
