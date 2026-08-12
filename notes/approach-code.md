# Approach code, and the Enzyme record

Collected for the roadmap rebuild.
Sources and retrieval dates are given for every block.

## Approach one: composable Turing models

Source: <https://epiaware.org/approaches/composable-turing-models.html>,
retrieved 2026-08-12.

The page block runs to 22 lines and does not fit a slide.
Trimmed below to 14 lines by removing the blank lines and the two source
comments, and by moving `NegativeBinomialError()` onto the
`Ascertainment(` line.
No code was changed.

```julia
# trimmed: blank lines and source comments
using ComposableTuringIDModels, Distributions, Turing
data = IDData(gen_distribution = Gamma(1.4, 1 / 0.38))
model = IDModel(
    Renewal(data;
        rt = AR(; ϵ_t = HierarchicalNormal(
            std_prior = HalfNormal(0.1))),
        initialisation_prior = Normal(log(1.0), 1.0)),
    LatentDelay(
        Ascertainment(NegativeBinomialError(),
            Intercept(Normal(log(0.4), 0.1))),
        truncated(Normal(5.0, 2.0), 0.0, Inf)))
chain = sample(as_turing_model(model, cases, length(cases)),
               NUTS(), MCMCThreads(), 1_000, 2)
```

14 lines, widest line 60 characters.

The comments removed from the source block were
"Renewal infections with an inline prior model",
"Multiple observation layers:",
"delay → ascertainment → negative-binomial noise" and
"Fit to case data with Turing's NUTS".

## Approach two: composed distributions

Source: <https://epiaware.org/approaches/composed-distributions.html>,
retrieved 2026-08-12.

The page block runs to 24 lines.
Trimmed below to 14 lines by removing the blank lines, the source
comments, and the three inspection calls `event_tree(tree)`,
`params_table(tree)` and `priors = param_priors(tree)`.
The closing `))` was folded onto the `:lost` line.

```julia
# trimmed: blank lines, source comments and the inspect calls
using ComposedDistributions, Distributions
tree = @uncertain compose((
    clinical = sequential(
        :onset_admit => Gamma(Normal(1.2, 0.2), 3.0),
        :admit_resolve => resolve(
            :death => (Gamma(2.0, 3.5), 0.3),
            :discharge => (Gamma(1.0, 8.0), 0.7))),
    surveillance = sequential(
        :onset_notif => Gamma(0.7, 20.0),
        :notif_compete => compete(
            :confirmed => Gamma(2.0, 1.0),
            :lost => Gamma(5.0, 0.5))),))
case = rand(tree); logpdf(tree, case)
```

14 lines, widest line 61 characters.

The source comments removed were
"BDBV-inspired delay tree: parallel pathways with sequential, resolve,
and compete nested together",
"Inspect tree, params, and default priors" and
"Draw a synthetic case, or evaluate a real one's likelihood".

## Enzyme on BVDOutbreakSize

All references are to `/Users/lshsa2/code/seabbs/BVDOutbreakSize`,
read 2026-08-12.

### Mooncake is the default, Enzyme is opt-in

`Project.toml` lists `Mooncake` under `[deps]` and `Enzyme` under
`[weakdeps]`, with the extension `BVDOutbreakSizeEnzymeExt = "Enzyme"`.
Compat bounds are `Mooncake = "0.5"` and `Enzyme = "0.13"`.

`src/sampling.jl:8`:

```julia
default_adtype() = AutoMooncake(; config = Mooncake.Config())
```

`src/sampling.jl:277` passes `adtype = default_adtype()` as the
`nuts_sample` default, so every fit in the repo uses Mooncake unless the
caller opts out.
`enzyme_adtype()` is only a stub in `src/sampling.jl` and raises a
`MethodError` until `Enzyme` is loaded.

`scripts/fit_joint_stream.jl:18` takes the AD backend as the third
positional argument and defaults it to `"mooncake"`.
Its comment on line 20 claims Enzyme is "~3x faster than the Mooncake
default on the joint".
No timing output in the repo backs that number, so do not put it on a
slide.

### Enzyme works on a single stream and fails on the joint

`test/enzyme/runtests.jl` keeps Enzyme in its own sub-environment and
compares its gradient to Mooncake at a fixed prior draw.
The single-stream `exports_only_model` test passes.
The `bvd_joint` test is recorded as `@test_broken`.

The file header gives the reasons Enzyme is kept out of the main test
environment: a native access violation on Windows, an
`EnzymeInternalError` LLVM compile failure on the joint on some Linux
runners, and a wrong gradient from mishandling the Gauss-Legendre
quadrature in the censored-delay path on Julia LTS.
Loading it in the main environment also tripped Aqua's persistent-task
check and broke precompilation on Windows.

### Issue 445 is the record of the failure

`epiforecasts/BVDOutbreakSize` issue #445, "Enzyme cannot differentiate
bvd_joint: boxed map(do) closures (fixable) then upstream
nodecayed_phis! LLVM bug", opened 2026-07-20, still open at 2026-08-12.

Reported run of `test/enzyme/runtests.jl`:

```
Test Summary:    | Pass  Broken  Total      Time
Enzyme extension |    4       1      5  24m41.4s
```

On the single stream, Enzyme against Mooncake gives
`maxabsdiff = 4.44e-15`, `relerr = 2.28e-16`.

Two failures on the joint:

1. Enzyme's reverse mode cannot build a shadow for the anonymous
   closures made by `map(collection) do x … end` when the captures are
   boxed in a `Base.RefValue`.
   Mooncake tolerates the box.
2. After the closures are de-boxed, Enzyme reaches its own LLVM pass
   `nodecayed_phis!` and fails there with an `EnzymeInternalError`.
   That is an upstream Enzyme bug, not model code.

Versions in the issue: Julia 1.12.6, Enzyme 0.13.190, Mooncake 0.5.39,
Turing 0.46, CensoredDistributions 0.2.22, ADTypes 1.22.2.

The de-box was merged as PR #446, "refactor(models): de-box map(do)
closures on the joint AD path", merged 2026-07-20.
It clears the first failure and exposes the second.
`docs/src/news.md` records the same change and notes the Mooncake
gradient is bit-identical after it.

### The git history of the attempt

`git log --grep=Enzyme -i` returns 39 commits.
They include a long-running `enzyme-joint-explore` branch, repeated
merges from `renewal` into it, three separate de-box commits
(`9c03679b`, `ec933ed1`, `85dcf9db`), a benchmark commit
"bench(docs): build docs with Enzyme AD to time vs Mooncake"
(`954a15ff`), and dependabot bumps for the `test/enzyme` environment
alone.

Issue #445 records that an older, smaller joint, before
`treatment_flow_model` existed, did once differentiate under Enzyme on
macOS aarch64.
The current joint does not.

### What the opener can safely say

- The model fits with Mooncake.
- Enzyme is wired up as an opt-in extension and differentiates the
  single-stream models to 4e-15 of Mooncake.
- Enzyme cannot differentiate the joint.
  One layer was model code and was fixed.
  The layer underneath is an LLVM compile failure inside Enzyme.
