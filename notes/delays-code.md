# Paired code examples for the delays talk

Three R/Stan versus Julia pairs, taken from
`~/code/epinowcast/primarycensored` and
`~/code/EpiAware/CensoredDistributions.jl`.
All snippets are real code.
Cuts are marked with `# ...` or `// ...`.
Reflowing to fit 62 characters is noted where it happened.

Julia snippets were run against
`--project=/Users/lshsa2/code/EpiAware/CensoredDistributions.jl`
(and `--project=test` where Turing is needed).
Verification output is recorded under each pair.

Package versions checked at time of writing.
CensoredDistributions.jl is v0.2.20 (`Project.toml`).
primarycensored has a `CRAN-SUBMISSION` file in the repo root.

---

## Pair A: a double interval censored, right truncated delay

Caption: the R version takes the pieces as arguments to one function;
the Julia version composes them and hands back a distribution.

### R

```r
dprimarycensored <- function(
    x, pdist, pwindow = 1, swindow = 1,
    L = -Inf, D = Inf,
    dprimary = stats::dunif,
    dprimary_args = list(),
    log = FALSE, ...) {
  # ...
}

# Weibull delay, uniform primary, truncated to [1, 10]
dprimarycensored(1:9, pweibull, L = 1, D = 10,
                 shape = 1.5, scale = 2.0)
```

Source: `primarycensored/R/dprimarycensored.R:71-81` (signature),
`primarycensored/R/dprimarycensored.R:69-70` (the roxygen example).
The call was reflowed onto two lines to fit the width.

### Julia

```julia
using CensoredDistributions, Distributions

original = Gamma(2, 3)
censored = double_interval_censored(
    original; upper = 15, interval = 1
)

pdf(censored, 3.0)        # 0.1274
cdf(censored, 7.0)        # 0.6677
quantile(censored, 0.5)
rand(censored, 10)
```

Source: `CensoredDistributions.jl/README.md:39-40` for the two
constructor lines,
`CensoredDistributions.jl/src/censoring/double_interval_censored.jl:48-54`
for the `pdf`/`cdf`/`quantile`/`rand` lines.

Verified.
Ran and returned
`IntervalCensored{Truncated{PrimaryCensored{Gamma{Float64},
Uniform{Float64}, AnalyticalSolver{...}}}}`,
`pdf = 0.12741255086023234`, `cdf = 0.667710369213006`,
`rand(censored, 5) = [9.0, 6.0, 5.0, 6.0, 1.0]`.
The two comment values in the snippet are those verified numbers
rounded to four decimal places.

If a shorter Julia block is wanted, the first four lines alone carry
the point.

---

## Pair B: the dispatch mechanism

This is the strongest pair.
Caption: Stan has to enumerate every distribution it will ever
support; Julia calls `logcdf` on whatever it was given.

### Stan

```stan
real dist_lcdf(real delay, array[] real params,
               int dist_id) {
  // IDs match pcd_distributions$stan_id in R
  if (dist_id == 1)
    return lognormal_lcdf(delay | params[1], params[2]);
  else if (dist_id == 2)
    return gamma_lcdf(delay | params[1], params[2]);
  // ... 16 more branches ...
  else if (dist_id == 25)
    return von_mises_lcdf(delay | params[1], params[2]);
  else reject("Invalid distribution identifier: ",
              dist_id);
}
```

Source:
`primarycensored/inst/stan/functions/primarycensored_ode.stan:52-77`.
Each `if` was split across two lines to fit the width; the bodies are
unchanged.

Verified count.
There are exactly 18 `dist_id ==` branches in that function
(lines 58-75), plus the `reject`.
Counted with
`awk 'NR>=57 && NR<=76' ... | grep -c "dist_id =="` which returns 18.
The IDs are 1, 2, 3, 4, 9, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22,
23, 24, 25.
The gaps in the numbering are IDs in the R lookup table that have no
Stan `_lcdf`.

There is a second switch of the same shape for the primary event
distribution in the same file, and a third for which pairs have a
closed form, in
`primarycensored/inst/stan/functions/primarycensored_analytical_cdf.stan:10-15`
and `:191-199`.
Mention that they exist; do not show them.

### Julia

```julia
function primarycensored_cdf(
        dist::D1, primary_event::D2,
        x::Real,
        method::NumericSolver
) where {D1 <: UnivariateDistribution,
         D2 <: UnivariateDistribution}
    # ...
    function integrand(u, x)
        return exp(_logcdf_ad_safe(dist, u) +
                   logpdf(primary_event, x - u))
    end
    # ...
end
```

Source:
`CensoredDistributions.jl/src/censoring/primarycensored_cdf.jl:208-229`.
Unmodified apart from two cuts.

The line that answers Stan's 18 branches is
`_logcdf_ad_safe(dist, u)`, which is

```julia
_logcdf_ad_safe(dist::UnivariateDistribution, u::Real) =
    logcdf(dist, u)
```

Source: `CensoredDistributions.jl/src/utils/gamma_ad.jl:112`, wrapped
onto two lines.
There is one further method for `Gamma` at `:114`, an autodiff
workaround, not a dispatch table.

Verified.
`length(methods(CensoredDistributions.primarycensored_cdf))` returns
6 for the whole file, against Stan's 18 branches in one function
alone.
Three of those methods are closed-form specialisations, at
`primarycensored_cdf.jl:351` (`Gamma`, `Uniform`), `:404`
(`LogNormal`, `Uniform`) and `:449` (`Weibull`, `Uniform`).

Verified that the fallback works for distributions Stan never
enumerated.
`cdf(primary_censored(d, Uniform(0,1)), 3.0)` returned

| distribution | value | in Stan's switch? |
| --- | --- | --- |
| `Gamma(2,3)` | 0.20357801828224475 | yes, id 2 |
| `LogNormal(1.5,0.75)` | 0.2183282452603626 | yes, id 1 |
| `Weibull(2,3)` | 0.4988934980445596 | yes, id 3 |
| `Pareto(3,1)` | 0.9305555555555555 | yes, id 21 |
| `Gumbel(2,1)` | 0.5400318623728096 | yes, id 15 |
| `TDist(3)` | 0.9543710516570098 | yes, id 23 |
| `Frechet(2,1)` | 0.8471314136980865 | no |

`Frechet` is the one to say out loud.
It is not in the Stan switch, so in primarycensored it needs a new
branch, a new ID, and a rebuild.
In Julia it already worked.

If a signature-only block reads better on the slide, this is the
same point in fewer characters.

```julia
# Closed form, picked by the argument types
primarycensored_cdf(dist::Gamma,
    primary_event::Uniform, x::Real,
    ::AnalyticalSolver)
# ... same for LogNormal, Weibull ...

# Every other pair, same function name
primarycensored_cdf(dist::D1,
    primary_event::D2, x::Real,
    method::AnalyticalSolver
) where {D1 <: UnivariateDistribution,
         D2 <: UnivariateDistribution}
```

Source: `primarycensored_cdf.jl:351-353` and `:174-178`, signatures
only, reflowed.
Label it as signatures if used, since the bodies are cut entirely.

---

## Pair C: fitting

Caption: the Stan model needs the distribution passed in as data;
the Turing model builds it from the parameters being sampled.

### Stan

```stan
model {
  for (i in 1:n_params) {
    params[i] ~ normal(prior_location[i], prior_scale[i]);
  }
  // ... priors for primary_params ...
  for (i in 1:N) {
    target += n[i] * primarycensored_lpmf(
      d[i] | dist_id, to_array_1d(params),
      pwindow[i], d_upper[i], L[i], D[i],
      primary_id, to_array_1d(primary_params)
    );
  }
}
```

Source: `primarycensored/inst/stan/pcens_model.stan:72-99`.
The `reduce_sum` branch is cut; the loop shown is the `else` branch
at `:93-99`.

### R wrapper

```r
delay_data <- data.frame(
  left = samples, right = samples + swindow,
  pwindow = rep(pwindow, n), D = rep(D, n)
)

fit_norm <- fitdistdoublecens(
  delay_data, distr = "norm",
  start = list(mean = 0, sd = 1)
)
```

Source: `primarycensored/R/fitdistdoublecens.R:93-103` (roxygen
example), reflowed onto fewer lines.
`distr = "norm"` is the string that gets turned into `dist_id` by
`pcd_dist_name()` in `primarycensored/R/utils.R:92-118`.

### Julia

```julia
@model function double_censored_model(values, weights)
    α ~ truncated(Normal(1, 2), 0, Inf)
    θ ~ truncated(Normal(1, 2), 0, Inf)
    censored_dist = double_interval_censored(
        Gamma(α, θ); upper = 15, interval = 1
    )
    values ~ weight(censored_dist, weights)
end

model = double_censored_model(values, weights)
chain = sample(model, NUTS(), MCMCThreads(), 1000, 2)
```

Source: `CensoredDistributions.jl/README.md:71-85`.
The two prior comments were cut and the `double_interval_censored`
call was split across three lines to fit the width.

Verified.
Ran with `--project=test` on 500 draws from
`double_interval_censored(Gamma(2, 3); upper = 15, interval = 1)`,
sampled 300 NUTS iterations, and recovered posterior means
`alpha = 1.69` and `theta = 3.81` against true values 2 and 3.
That is the expected direction of shrinkage for 300 iterations on
one chain and is not worth putting on a slide.
Do not quote the recovery numbers; the point is that it runs.

Nothing needed fixing in the README code.
The only change made to run it was dropping `using StatsBase`, which
is not in the test project, and using `Statistics.mean` on the chain
instead of `summarystats`.

---

## Which pair is strongest

Pair B, clearly.
It is the only one where the two languages are doing something
structurally different rather than spelling the same thing
differently.
Stan enumerates 18 distributions by integer ID inside one function,
and needs a second switch for the primary event and a third for
which pairs have a closed form.
Julia has 6 methods, three of which are closed-form
specialisations, and a fallback that reaches `logcdf(dist, u)` on
anything that is a `UnivariateDistribution`.

The `Frechet` result is the line to build the slide around.
It is a distribution nobody wrote code for, it is not in the Stan
switch, and it returned an answer in Julia without anything being
added.

Pair A is the weakest.
Both versions are short and the difference reads as taste rather
than consequence.
Use it as a warm-up slide or cut it.

Pair C sits in between.
The useful contrast is that `dist_id` has to be data in Stan,
so the distribution is fixed before sampling starts, while the
Turing model constructs `Gamma(α, θ)` from parameters inside the
model.
That contrast is real but takes a sentence to explain, whereas
Pair B lands on sight.

## Things checked and left out

The abstract says the Stan integral solver was unstable and had to
be recast as an ODE.
`primarycensored/inst/stan/functions/primarycensored_ode.stan` is
145 lines and exists, which supports the claim.
There is no snippet here that shows the instability itself, so say
it in prose rather than showing code.

The abstract says tooling was needed to vendor Stan code into
downstream projects.
That is `primarycensored/R/pcd-stan-tools.R`, with `pcd_stan_path()`
at `:8`, `pcd_stan_functions()` at `:243` and
`pcd_load_stan_functions()` at `:339`, the last of which walks
function dependencies.
A one-line mention of the file is enough; the code is not
interesting to look at.

No count of total lines of Stan versus Julia is given here, because
the two repos are not structured comparably and any such number
would be misleading.
