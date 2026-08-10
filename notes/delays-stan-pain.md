# Delays talk: evidence base

Maintaining `primarycensored` (R + Stan) and building
`CensoredDistributions.jl` (Julia).
Every claim below has a commit SHA, PR number, issue number or `file:line`.
Anything I could not confirm is under [Unverified](#unverified).

Repos read:

- `/Users/lshsa2/code/epinowcast/primarycensored` (310 commits, main at
  `2ec4f402`, 2026-06-25)
- `/Users/lshsa2/code/EpiAware/CensoredDistributions.jl` (513 commits, main at
  `acb9e39b`, 2026-06-18)
- `/Users/lshsa2/code/epinowcast/epidist` (downstream consumer of the Stan code)

The headline is not "Stan bad, Julia good".
Both languages hit the same wall, which is that the integral at the centre of
primary event censoring has to be differentiated.
Stan solved it by turning the integral into an ODE.
Julia solved it by replacing adaptive quadrature with a fixed-node rule.
Same compromise, made twice, for the same reason.

---

## 1. The Stan integral solver instability and the recast as an ODE

**Issue:** epinowcast/primarycensored#34, "Stability issues in the numerical
integral solver".
Opened 2024-09-04, closed 2024-09-13.

**PR:** #64, "Issue 34: rephrase integral as an ODE", merged 2024-09-13.

**Commit:** `1c4e6f120c49ee372998851951ee8f03314c4535`.

**Function:** `primary_censored_integrand` was deleted and replaced by
`primary_censored_ode` in `inst/stan/primary_censored_dist.stan`.
The call site changed from `integrate_1d` to `ode_rk45`.
The current file is `inst/stan/functions/primarycensored_ode.stan` and the
function is now `primarycensored_ode` (renamed in #130, `fae7af3`).

The one-line mechanism, from the diff of `1c4e6f1`:

```stan
// before
result = integrate_1d(
  primary_censored_integrand, lower_bound, d, theta, {d, pwindow}, ids, 1e-2
);

// after
result = ode_rk45(
  primary_censored_ode, y0, lower_bound, {d}, theta, {d, pwindow}, ids
)[1, 1];
```

### What the failure actually looked like

This is the part worth putting on a slide, because it is not a wrong number, it
is a dead chain.
Quoted from issue #34, 2024-09-05.

```
Error in function tanh_sinh<double>::integrate: The tanh_sinh quadrature
evaluated your function at a singular point and got -inf. Please narrow the
bounds of integration or check your function for singularities.
Warning: 243 chain(s) finished unexpectedly!
```

The failures were post-warmup, during sampling, not at initialisation.
Sam's own words in the issue, 2024-09-05:

> Ideally `integrate_1d` would reject on error but it looks like it instead just
> errors and causes things to crash.
> If we had a try catch or similar here that would be perfect but as far as I am
> aware we don't.

### The measured failure rates (all from issue #34, all verified)

| State | Chains | Failed | Rate |
|---|---|---|---|
| First reproduction | 256 | 243 | 95% |
| Relative tolerance dropped 1e-6 to 1e-2 | 256 | 47 | 18% |
| Tolerance dropped further to 1e-1 | - | all | near-instant, in warmup |
| Boundary tuning at `0.3 * pwindow` | 600 | 135 | 22.5% |
| Boundary tuning at `0.1 * pwindow` | 600 | 160 | 26% |
| Truncation adjustment removed (wrong model) | 600 | 33 | 5.5% |
| Best tuned state on main, `e800dfd` | 600 | 88 | 15% |
| After dropping redundant `xc` args, `8fb2c03` | 600 | 70 | 12% |
| **Recast as ODE** | **600** | **0** | **0%** |

The ODE was also "4 to 5 times faster" (issue #34, 2024-09-12) with "no apparent
impact on the estimated values".

Two details that make the story honest rather than triumphal.
The nine days between opening and closing were spent on things that did not
work, including the `xc` high-precision-distance argument, moving `d` from
parameter to data, reparameterising the integral in terms of delay rather than
censoring window, and midpoint approximations.
The removal of the truncation adjustment dropping failures from 15% to 5.5% told
Sam the interaction between the delay CDF and the observation-time CDF was the
real problem, not the quadrature scheme on its own.

**Slide-safe framing:** the integral was mathematically fine.
It was the interaction with Stan's autodiff and its inability to reject inside
a quadrature call that made it unusable.

---

## 2. Reimplementing distribution CDFs in Stan

**Where:** `inst/stan/functions/primarycensored_ode.stan:52-77`, function
`dist_lcdf`.

**Count (verified by counting branches in the file):**

- **18** `dist_id` branches in `dist_lcdf`
- **2** `primary_id` branches in `primary_lpdf`
- **25** distributions named in the R lookup table (`data-raw/distributions.R`)
- **7** named in R but with no Stan branch, because Stan has no CDF for them:
  `gengamma`, `nbinom`, `pois`, `bern`, `binom`, `cat`, `dirich`

The shape of the code, from `primarycensored_ode.stan:57-77`:

```stan
if (dist_id == 1) return lognormal_lcdf(delay | params[1], params[2]);
else if (dist_id == 2) return gamma_lcdf(delay | params[1], params[2]);
else if (dist_id == 3) return weibull_lcdf(delay | params[1], params[2]);
...
else if (dist_id == 25) return von_mises_lcdf(delay | params[1], params[2]);
else reject("Invalid distribution identifier: ", dist_id);
```

A second hand-maintained table sits next to it,
`dist_has_positive_support(dist_id)` at `primarycensored_ode.stan:38-51`, which
is 10 more integer branches encoding which distributions have support on the
non-negative reals.

The Julia equivalent of both tables is zero lines.
`src/censoring/primarycensored_cdf.jl:207-211` takes
`D1 <: UnivariateDistribution` and calls `cdf` on it.
Any distribution in Distributions.jl works without the package knowing it
exists.

**Genuinely hand-written in both languages.**
The exponential-growth primary distribution is not in either standard library.
Stan has `expgrowth_pdf`, `expgrowth_lpdf`, `expgrowth_cdf`, `expgrowth_lcdf`
and `expgrowth_rng` in `inst/stan/functions/expgrowth.stan`, 5 functions and 47
code lines.
Julia has `src/distributions/ExponentiallyTilted.jl`, 193 code lines.
Julia is longer here.
Do not claim this one as a win.

**Analytical solutions are at parity.**
Both implement exactly 3 closed forms, all against a uniform primary.
Stan, `inst/stan/functions/primarycensored_analytical_cdf.stan`, has
`primarycensored_gamma_uniform_lcdf`, `primarycensored_lognormal_uniform_lcdf`
and `primarycensored_weibull_uniform_lcdf`.
Julia, `src/censoring/primarycensored_cdf.jl:351,404,449`, dispatches on
`(::Gamma, ::Uniform)`, `(::LogNormal, ::Uniform)` and `(::Weibull, ::Uniform)`.

---

## 3. Tooling built to vendor Stan code into downstream projects

**What it is called:** the `pcd_stan_*` family in
`/Users/lshsa2/code/epinowcast/primarycensored/R/pcd-stan-tools.R`, 453 lines.

Exported functions, confirmed against `NAMESPACE`:

- `pcd_stan_path()` returns the installed path of the `.stan` files
- `pcd_stan_functions()` lists the function names available
- `pcd_stan_files()` maps functions to files
- `pcd_load_stan_functions()` returns Stan source **as an R string**, optionally
  wrapping it in a `functions{}` block and writing it to disk
- `pcd_stan_function_deps()` returns a function's dependencies in topological
  order
- `pcd_stan_dist_id()` converts a distribution name to its integer id

**Why it was needed.**
Stan has no package manager and no import statement.
A downstream model cannot depend on `primarycensored`, it has to physically
contain the text of the functions.
The generated bundle is checked in at the repo root as `pcd_functions.stan`,
1081 lines, whose first line reads
`// Stan functions from primarycensored version 1.3.0.9000`.
That version string in a comment is the entire dependency-management story.

**The dependency resolver came from a downstream need.**
Issue #171, "Import all function dependency of Stan function", says:

> In working on epinowcast/epidist#426 I've wanted a way to get a
> `primarycensored` Stan function and all its dependencies.
> We don't think this is easy / possible but if it were it would be good.

Shipped in PR #262, commit `d7d710f` (2026-01-23), and released in 1.4.0 as the
`dependencies` argument to `pcd_load_stan_functions()` plus the new
`pcd_stan_function_deps()`.
A hand-rolled call-graph parser and topological sort, in R, over Stan source
text, to do what `using` does.

**Confirmed in use downstream.**
`epidist/R/marginal_model.R:377`:

```r
pcd_stanvars_functions <- brms::stanvar(
  block = "functions",
  scode = primarycensored::pcd_load_stan_functions()
)
```

---

## 4. Integer distribution identifiers, because Stan has no user types

**The mechanism, and it is worse than a switch statement.**
Because Stan has no user-defined types and no generics, `epidist` builds its
model by **string substitution into Stan source before compilation**.

`epidist/R/marginal_model.R:339-368`:

```r
dist_id <- primarycensored::pcd_stan_dist_id(family_name)

# Replace the dist_id passed to primarycensored
stanvars_functions[[1]]$scode <- gsub(
  "dist_id", dist_id, stanvars_functions[[1]]$scode, fixed = TRUE
)
```

with `gsub` also replacing `family`, `dpars_A`, `dpars_B` and `primary_id`.
The template it edits is `epidist/inst/stan/marginal_model/functions.stan`,
whose own docstring says the quiet part out loud:

```
* This function is designed to be read into R where:
* - 'family' is replaced with the target distribution (e.g., 'lognormal')
* - 'dpars_A' is replaced with multiple distribution parameters ...
```

So the type parameter is a string, the substitution happens in another language,
and the type error surfaces as a Stan compile error at best.

**The bug this caused, which is the slide.**
Issue and PR epinowcast/primarycensored#277, merged 2026-02-27, commit
`4aaf249876b59b03fd460b257cc8293c27aaeca1`.
The Stan integer ids and the R lookup table had drifted apart.
From the PR body:

> Stan's `dist_lcdf` function used a completely different distribution ID
> numbering from the R `pcd_distributions` data frame.
> Most notably, `dist_id = 3` was **Normal** in Stan but **Weibull** in R, so
> `pcd_stan_dist_id("weibull")` returned 3 which then called `normal_lcdf` in
> the ODE integration path.

> The mismatch affected all distributions except lognormal (1), gamma (2), and
> exponential (4).

Ask for a Weibull, fit a normal, get numbers back.
No error, no warning.
It only showed up in the ODE numerical path, because the analytical path already
used R's numbering, so it was invisible for the uniform-primary cases people
used most.
The fix added `tests/testthat/test-stan-dist_lcdf.R`, 228 lines, that exists
solely to check two integer tables agree.

In Julia the equivalent bug is not expressible.
`primary_censored(Weibull(2, 1), Uniform(0, 1))` carries the type.
There is no second table to disagree with.

---

## 5. What was genuinely painful on the Julia side

The "it just worked with AD" line does not survive contact with the issue
tracker.
`CensoredDistributions.jl` has 396 issues and, separately, 533 pull requests.
Of the 396 issues, **48** have AD, autodiff, gradient, numerical, quadrature,
precision or performance in the title.
Counting rule, so it can be re-run: fetch every issue title with
`gh api --paginate 'repos/EpiAware/CensoredDistributions.jl/issues?state=all&per_page=100'`,
drop anything carrying a `pull_request` key, then count word-boundary matches
with `grep -icE '\b(AD|autodiff|gradient|numerical|quadrature|precision|performance)\b'`.
Checked 2026-08-10.
There is a dedicated `test/ad/` sub-environment, a `test/ADFixtures` path
package, a separate CI job per backend, and a hand-maintained registry of
known-broken backend and scenario combinations.
That machinery does not get built for something that just worked.

### 5.1 The Julia analogue of the ODE recast

This is the strongest honest parallel in the whole talk.

From `NEWS.md`, under Breaking:

> `primary_censored(...; solver)` defaults to `GaussLegendre(; n = 64)` (was
> `QuadGKJL()`).
> The fixed-node solver traces cleanly through every AD backend, where adaptive
> quadrature does not.

PR #250, "feat: AD-safe gamma CDF + Mooncake-compatible default integrator",
merged 2026-05-26, commit `04963539`.

`src/integration/integration.jl:14-20` states the reason directly.

> The constant control flow and the accumulator type being seeded from the
> integrand make this the AD-safe default: every supported AD backend can
> differentiate through it, unlike adaptive schemes whose node count depends on
> integrand values.

Stan gave up adaptive quadrature for an ODE solver.
Julia gave up adaptive quadrature for a fixed 64-node dot product.
Both were forced by the differentiator, not by the mathematics.

There is a second-order version of the same problem in the same file,
`integration.jl:79-88`.
The quadrature nodes had to be stored on the solver object rather than in a
global cache, because "a mutated global cache here would be written inside the
traced region and crash Enzyme reverse".

### 5.2 Four of six AD backends were broken

Issue #225, opened 2026-04-14, closed 2026-05-29, measured on Julia 1.12.

| Backend | State |
|---|---|
| `AutoForwardDiff()` | Full, 154/154 pass |
| `AutoReverseDiff(compile=false)` | Full, 154/154 pass |
| `AutoReverseDiff(compile=true)` | 40 pass / 48 fail / 3 error per 91 assertions |
| `AutoEnzyme(Forward)` | Broken, 7/7 scenarios error |
| `AutoEnzyme(Reverse)` | Broken, 7/7 scenarios error |
| `AutoMooncake()` | Broken, 7/7 scenarios error |

Issue #218 adds Zygote, which failed on **every** censored logpdf tested,
including all three analytical paths, both interval-censoring paths and
`DoubleIntervalCensored`.

The README carried a per-backend badge row reflecting this
(`NEWS.md`): "ForwardDiff full; ReverseDiff tape, Mooncake reverse, and Mooncake
forward partial; Enzyme forward/reverse broken."

### 5.3 Silently wrong gradients, not just crashes

Issue #259, "Enzyme.@import_rrule produces wrong k-partial for `_gamma_cdf`
rrule", 2026-05-27.
Lifting a correct `ChainRulesCore.rrule` into Enzyme returned a wrong shape
partial while the other two partials were right.

```
Enzyme forward  -> [-0.21736, -0.21296, 0.19054]   # k partial wrong
ForwardDiff     -> [-0.23692, -0.21296, 0.19054]   # matches finite differences
```

Issue #249, 2026-05-24, is a gradient **regression** introduced by the package's
own fix.
Removing `try/catch` (PR #230) and adding NaN guards made
`AutoReverseDiff(compile=false)` produce an incorrect gradient on
`PrimaryCensored LogNormal+Uniform numerical`, 12 of 22 correctness sub-tests
failing.
Root cause per `NEWS.md` was evaluating `cdf(dist, lower)` at the distribution
boundary, tripping degenerate `0·(-Inf)` reverse rules in Distributions.jl and
"contaminating the ReverseDiff tape with NaN".

This is the same failure mode as Stan.
Wrong or absent gradients from a mathematically correct integrand.

### 5.4 Defensive code had to be removed to make AD work

Issue #220, "Remove try/catch in CDF helpers to unblock Mooncake", 2026-04-14.
Mooncake cannot differentiate through `try/catch`, so error handling in
`src/censoring/IntervalCensored.jl:374` and
`src/censoring/primarycensored_cdf.jl:483` blocked reverse-rule compilation
entirely.

```
MooncakeRuleCompilationError: Mooncake failed to differentiate the following
method: _interval_cdf(d::IntervalCensored, x::Real, f::Function)
```

Note the symmetry with Stan.
In Stan the complaint (issue #34) was that there is **no** try/catch.
In Julia the problem was that there **is** one and it has to be taken out again.

### 5.5 Hand-written derivative code, in Julia

Distributions.jl does not give the Gamma CDF shape-parameter derivative.
`src/utils/gamma_ad.jl`, 153 lines, contains `_grad_p_a_series`, a hand-rolled
series expansion for the partial of the regularised incomplete gamma with
respect to its shape.
Around it sit `ext/CensoredDistributionsForwardDiffExt.jl` (75 lines, **7
explicit `Dual` method overloads** covering every non-trivial `Dual` subset of
`(k, θ, x)`), `ext/CensoredDistributionsEnzymeExt.jl` (75),
`ext/CensoredDistributionsMooncakeExt.jl` (102),
`ext/CensoredDistributionsReverseDiffExt.jl` (33) and
`ext/CensoredDistributionsChainRulesCoreExt.jl` (42).

Those 7 hand-written `Dual` overloads later produced their own bug, issue #672,
"ForwardDiff extension has 6 method ambiguities in `_gamma_cdf` Dual overloads
(invisible to Aqua)".

The upstream gap that started it is issue #217, where
`logpdf(interval_censored(Gamma(θ...), boundaries), x)` failed with
`MethodError: no method matching _gamma_inc(::Dual, ::Float64, ::Int64)`.

### 5.6 The package finite-differences its own density

`src/censoring/PrimaryCensored.jl:262-263`:

```julia
# Use central difference for numerical differentiation
h = 1e-8  # Small step size for differentiation
```

`logpdf(::PrimaryCensored, x)` is a central difference of `logcdf` with a
hardcoded step.
`NEWS.md` records the consequence.
Finite-difference reference baselines such as `central_fdm(5, 1)` "disagree with
every AD backend by ~10% on Weibull analytical scenarios" because of this, so
the test suite had to adopt ForwardDiff rather than finite differences as its
gradient reference.

### 5.7 Early correctness and performance problems

Issue #31, 2024-10-08, "Incorrect implementation of numerical `cdf`", against
the package's earlier name `PrimaryCensored.jl`.
The numerical CDF did not reproduce the analytical `Exp(1)` with `Uniform(0,1)`
primary result.
Fixed in a day.

Issue #42, "Improve performance to match the `EpiAware` version", opened
2024-10-22 and **not closed until 2025-09-26**, roughly eleven months.
The Julia rewrite was initially slower than the code it replaced.

Issue #111, 2025-08-01, `interval_censored` worked for `pdf` and `cdf` and under
`Prior()` sampling but failed under NUTS with "failed to find valid initial
parameters in 1000 tries", across LogNormal, Normal, Gamma and Exponential.

### 5.8 Still open

- #749, "Performance: joint andv fit too slow, reverse-AD of
  `cdf(Convolved(...), window)` completeness per leapfrog"
- #889, "Enzyme fails on `convolve_series` through a stacked
  `IntervalCensored{Truncated{PrimaryCensored}}` delay"
- #834, reverse-mode AD over a CTMC path errors on `foreigncall`
- #674, research whether to replace the hand-maintained broken-backend list with
  a trait-based capability system

The hand-maintained registry itself is `backend_broken_scenarios()` at
`test/ADFixtures/src/ADFixtures.jl:177`, with `backend_skip_scenarios()` at
:291 for scenarios that "crash a compiled backend UNCATCHABLY (an abort /
`signal 6`) that a `try`/`catch` cannot recover".

**Suggested slide line, and it is true:** Julia did not remove the problem.
It moved it from "my chains die" to "this backend is on a list".

---

## 6. How much code each implementation is

Counted with comments, docstrings and blank lines stripped, on 2026-08-10.
Raw line counts including documentation are in brackets.

### Stan, `primarycensored/inst/stan/`

| File | Code lines | (with docs) |
|---|---|---|
| `functions/primarycensored.stan` | 263 | (591) |
| `functions/primarycensored_analytical_cdf.stan` | 122 | (266) |
| `functions/primarycensored_ode.stan` | 63 | (145) |
| `functions/expgrowth.stan` | 47 | (100) |
| `pcens_model.stan` | 100 | (113) |
| **Total** | **595** | (1215) |

The Stan code cannot be used on its own.
It needs the R package to drive it, which is **1252** code lines across
`R/*.R`, of which 453 are the vendoring tooling from section 3.

**Two languages, roughly 1850 code lines.**

### Julia, `CensoredDistributions.jl/src/`, equivalent surface only

| File | Code lines |
|---|---|
| `censoring/primarycensored_cdf.jl` | 366 |
| `censoring/IntervalCensored.jl` | 324 |
| `censoring/PrimaryCensored.jl` | 236 |
| `distributions/ExponentiallyTilted.jl` | 193 |
| `censoring/truncation.jl` | 175 |
| `integration/integration.jl` | 102 |
| `censoring/double_interval_censored.jl` | 28 |
| **Total** | **1424** |

**One language, 1424 code lines.**

### Read this carefully before putting it on a slide

Julia is **larger** than the Stan half alone, 1424 against 595.
The honest comparison is against Stan plus its R driver, and even then the
scopes are not identical.
The Julia version supports arbitrary interval boundaries, several truncation
combinations, a pluggable solver interface and any Distributions.jl leaf.
The Stan version supports 18 hardcoded distributions and 2 primaries.

The safe claim is about **where** the lines go, not how many there are.
Roughly 200 of the Stan-plus-R total exist only to work around missing types
and missing imports, being the 18-branch and 10-branch integer tables, the 228
line test that checks two integer tables agree, and the 453 line vendoring
toolkit.
None of that has a Julia counterpart.
Julia's extra lines are in `ext/`, 2304 lines total across 10 extensions, of
which about 327 are AD glue for a single Gamma CDF derivative.

**The most defensible one-liner:** in Stan the workarounds are for the
language, in Julia they are for the autodiff backends.

---

## 7. Other verified facts worth having in reserve

**A 30% Stan slowdown from a no-op branch.**
`primarycensored` 1.5.1 release notes.
Relaxing a truncation guard in 1.5.0 meant every likelihood evaluation for
positive-support delays entered a normalisation block that "cancels to a no-op
but still adds gradient calculations (an `exp`/`log_diff_exp` per call), giving
a roughly 30% slowdown on the likelihood block".
Reported by @sbfnk, issue #323.
In Stan you pay for a branch you do not take, because the autodiff tape does not
know it is a no-op.

**Stan reserved keywords.**
Commits `b13dab8` and `c0efad0` (2026-01-23), epinowcast/primarycensored#259,
"Fix Stan reserved keyword errors in function parameter names".
Not to be confused with EpiAware/CensoredDistributions.jl#259 in section 5.3.

**The Julia AD test suite is a real artefact.**
`test/ad/` plus `test/ADFixtures/src/` come to 2724 lines across roughly 16
files.
Issue #444 records a full sweep result of "6454 passed, 0 failed, 1 errored,
7 broken".

**Two `dist_id` tables in Stan, not one.**
`dist_lcdf` (18 branches) and `dist_has_positive_support` (10 branches), both in
`primarycensored_ode.stan`, both hand-maintained, both must agree with the R
data frame.

---

## Unverified

Things I could not confirm and which should stay off the slides unless checked.

1. **Total distributions available in Distributions.jl.** I did not count them,
   so do not put a number against "Julia gets N distributions for free". Say
   "any `UnivariateDistribution`", which is verified at
   `primarycensored_cdf.jl:207-211`.
2. **The 4-5x ODE speedup.** This is Sam's own comment in issue #34 on
   2024-09-12, from a single run. It is a reported observation, not a benchmark.
   Attribute it, do not present it as measured.
3. **Whether the 95% chain failure rate is representative.** Issue #34 says the
   simulated scenario was deliberately made harder in the same PR that landed
   the ODE (`1c4e6f1` includes "make the simulated scenario harder"). The
   before-and-after numbers in the table are not all on an identical dataset.
   The 0%-versus-12% comparison on 600 chains is the most like-for-like pair.
4. **Current AD backend status.** The #225 table is from 2026-04-14 and much of
   it has since been fixed. Do not present it as the state today. Present it as
   what the first proper measurement found.
5. **Wall-clock timings for Julia versus Stan on the same fit.** I found no
   benchmark comparing them directly. `benchmark/` exists in
   `CensoredDistributions.jl` but I did not run it, and no cross-language
   comparison is recorded.
6. **Whether the #277 `dist_id` bug affected any published result.** The PR says
   it only manifested in the ODE path with non-uniform primary distributions. I
   found no downstream impact assessment.
