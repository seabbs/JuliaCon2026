# Julia ecosystems: research notes for the roadmap talk

Research for the closing section of the roadmap talk.
Everything with a number below was checked against the GitHub API, a
repository file, or a primary web page, and the source is given.
Where I could not verify something I have said so.

API counts were taken on 2026-08-10.
They are counts of GitHub repositories, not registered packages.
Org repo counts include documentation repos, meta repos and forks, so
they run ahead of package counts.

- SciML 218 repos
- jump-dev 66 repos
- CliMA 66 repos
- JuliaGraphs 44 repos
- JuliaStats 43 repos
- TuringLang 26 repos
- MakieOrg 22 repos
- SpeedyWeather 16 repos

---

## Q1. What does a good Julia org look like?

### The pattern that repeats

Three of the largest Julia orgs have written governance, and all three
have the same shape.
A small technical core with final say, a slightly larger body that
handles money and legal standing, and a fiscal sponsor.

**JuMP** (<https://jump.dev/pages/governance/>) is the most explicit.
Miles Lubin is named Benevolent Dictator For Life "due to his role in
the creation of JuMP".
Five core contributors "lead the technical development of the JuMP
project, and they are the ultimate authority on the direction".
Below them sit repository maintainers, "trusted members of the
community who help the core contributors by managing a limited number
of repositories", appointed by any core contributor.
A separate five-member Steering Committee exists mainly to face
outward, representing JuMP to NumFOCUS, approving expenditure and
signing contractor agreements.
"JuMP is a fiscally sponsored project of NumFOCUS, a 501(c)(3) public
charity in the United States."
The route in is stated plainly.
Before becoming a core contributor you are expected to have been a
repository maintainer of several repositories in the org.

JuMP separates user channels from developer channels and says so.
Community forum for questions, developer chatroom for technical
discussion, monthly developer calls, workshops.
That split is the concrete answer to "how do you onboard users versus
developers", and it is cheap to copy.

**SciML** (<https://sciml.ai/governance/>) uses a five-member Steering
Council drawn from contributors whose work is "substantial in quality
and quantity" and "sustained over at least one year".
Council decisions are by simple majority.
There is also an eight-member Advisory Committee that meets annually
and exists to "break deadlocks or serious disagreements in the
Council".
Notably the governance document does not say how a new package joins
the org.
That is the thing we most need to know and it is not written down.

**Turing** is the least formal of the three.
The contributing guidance says proposals for new features should be
submitted first so the TuringLang team can indicate whether they fit,
and that "reviewer privileges are reserved for those with a sustained
record of substantive contributions to TuringLang, or for individuals
explicitly invited by a team member".
There is no published steering council or council election process
that I could find.

The pattern worth saying out loud is that all three formalised
governance *after* the code was already widely used.
JuMP's own page notes the project formalised governance as it
approached 1.0, "having come a long way since its creation as a
side-project of two graduate students at MIT".
None of them documents how to set up an org before you have users,
which is exactly our position.

### Scale and funding, with numbers

SciML's own State of the Ecosystem post, June 2025
(<https://sciml.ai/news/2025/06/26/state_of_sciml/>) gives figures.

- "Over 100 GitHub repositories, many containing 10+ packages
  themselves"
- "Totals ~200 Julia packages, all MIT open source licensed"
- "20,000+ GitHub stars across the package ecosystem"
- "~100+ unique contributors monthly (variable month to month)"
- "~20 core maintainers owning specific aspects of the project"
- "~5-10 summer students and other trainees per year"
- "~10 grant applications per year related to expanding the SciML
  organization"

They also state that spinoff companies (PumasAI, JuliaHub, Neuroblox)
employ full-time maintainers, and that many maintainers come from the
MIT Julia Lab and its alumni.
That is the honest answer to how SciML is sustained.
It is grant funding plus company payroll, not donations.

SciML also runs a Small Grants Program, and published a two-year
update in May 2026
(<https://sciml.ai/news/2026/05/26/sciml_small_grants_two_year_update/index.html>).
Lifetime spend is roughly $8,400 to $8,600.
$5,950 went out over the most recent ten months across eight completed
projects, with individual grants from $100 to $2,250.
The work funded is benchmarks, bug fixes, performance work,
architecture migration and GPU acceleration.
Two findings are useful for us.
Repeat contributors do most of the high-value work, and open-ended
per-unit bounties (for example $100 per benchmark problem) attract more
people than single large projects.
They also have an AI usage policy requiring disclosure, noting that
"projects on offer have already been attempted with state-of-the-art AI
tooling, so a contributor relying on AI alone without expert guidance
is unlikely to succeed".

This is a very small amount of money for a very large ecosystem.
Worth saying in the talk if funding comes up.

**Makie** is worth a mention as a different model.
Makie has a JOSS paper (<https://joss.theoj.org/papers/10.21105/joss.03349>)
and lists supporters including NumFOCUS, PumasAI, JuliaHub, MIT, LANL
and ORNL on <https://makie.org>.
Search results reported that Makie work has been funded by the
Sovereign Tech Agency, and GPU work on Raycore by Muon Space.
I could not confirm either from a primary Makie source, so do not put
those on a slide.
Makie also does not publish a governance document that I could find,
which is itself notable given how widely used it is.

### Domain-specific ecosystems

These are the closest analogues to what EpiAware wants to be.

**SpeedyWeather.jl** (<https://joss.theoj.org/papers/10.21105/joss.06323>,
JOSS 2024, Klöwer et al.).
Small org, 16 repos.
Described as "a research playground with an everything-flexible
attitude", easy to extend, and designed for interactive use in the
terminal or a notebook.
Current work is on differentiability with Enzyme, GPU support via
KernelAbstractions and Reactant, and rewriting parametrisations.
There is a JuliaCon 2026 talk on exactly this
(<https://pretalx.com/juliacon-2026/talk/GB8WXW/>).
Copyright is held by Milan Klöwer and "The SpeedyWeather.jl
Contributors", which is the whole of the governance.

**Oceananigans.jl** under CliMA is the better example of adoption
beyond the core team.
Development is described as community-driven with contributors from
academia and industry, and there is a dedicated `#oceananigans` Julia
Slack channel used as the store of institutional knowledge.
They published a short JOSS paper first and later a full model
description paper in JAMES, "High-level, high-resolution ocean
modeling at all scales with Oceananigans".
The two-paper pattern (short software paper early, detailed methods
paper once the model is stable) is worth copying.

### Where the answer genuinely does not exist

There is no Julia equivalent of rOpenSci.
I searched for one and found nothing.
JuliaHealth and BioJulia are domain communities, but neither runs
software peer review, neither publishes a package development guide of
rOpenSci's depth, and neither curates a reviewed suite.
rOpenSci's model, "peer review to curate a suite of high quality
packages and a community of developers and users to support the
long-term development and maintenance of scientific software"
(<https://ropensci.org/software-review/>), has no counterpart in Julia.
This is the biggest genuine gap I found and it is directly relevant to
the ecosystem we want to build.

Second gap.
Nobody has published an account of a Julia ecosystem reaching users
who are not themselves developers.
SciML, Turing and JuMP are all used mostly by technically strong users.
Oceananigans and SpeedyWeather come closest to a domain audience but
are both still small.
The author's instinct here is correct and I could not find a
counterexample.

---

## Q2. How do you depend on minimally maintained packages?

### What the data says

The median Julia package has two contributors, and the effective
bus factor is probably one.
Source is Eric Hanson's "Bus factor 0" post, 2025
(<https://ericphanson.com/blog/2025/bus-factor-0/>), which cites his
2021 work with Mosè Giordano, alongside a 2016 study finding 65% of
repositories had a bus factor of two or less.
Hanson's post is mostly about LLM-generated code that no human has
read, but the Julia contributor figures are the useful part for us.

The Discourse thread on package fragmentation
(<https://discourse.julialang.org/t/fixing-package-fragmentation/98712>)
has the community's own diagnosis.
Fragmentation is called "the only really bad thing of the Julia
ecosystem".
Users report that "sometimes it's hard to impossible to understand
what's different between similar packages", and that old unmaintained
packages remain discoverable years after they stopped being updated.
Proposed fixes included monolithic documentation spanning many
packages (SciML's model, and the one that got the most support), a
"discoverability czar", a higher registration bar, and consolidation
sessions at JuliaCon.
No consensus was reached.

### What the community actually does

There is no adopted policy.
The registry disputes question was raised in
JuliaRegistries/General#25367 in November 2020, comparing Julia to
npm's disputes procedure, and was never resolved into a documented
process.
In practice people email the existing owner, wait, and fork if there is
no reply.
Snappy.jl is a documented example of that route
(<https://discourse.julialang.org/t/forking-of-unmaintained-package-snappy-jl/77431>).

The one large case study is **LightGraphs.jl to Graphs.jl**.
LightGraphs was archived in October 2021 after its maintainer objected
to Julia Computing's telemetry and code redistribution practices and
proposed relicensing away from MIT
(<https://github.com/JuliaGraphs/LightGraphs.jl/issues/1506>).
JuliaGraphs responded by rebooting the package as Graphs.jl, keeping
the full LightGraphs git history inside it, so most of the diff was
module names, documentation and CI.
It was still a breaking upgrade for every downstream package.
The relevant lesson is that a package with hundreds of dependents can
become unmaintained for reasons that have nothing to do with technical
health, and the ecosystem's only recovery mechanism was a volunteer
fork under a new name.

### What is in progress

There is a live effort to define maintenance status labels.
Kosuri-Indu opened a Discourse thread on 21 January 2026
(<https://discourse.julialang.org/t/seeking-community-input-on-package-maintenance-status-labels-criteria/135177>)
as part of an ecosystem-wide audit of the JuliaHealth org, funded by a
NumFOCUS Small Development Grant.
The starting complaint is that "inactive" is misleading for a mature,
stable package with a low commit rate.
Suggestions in the thread include adopting the RepoStatus.org
vocabulary (Concept, WIP, Suspended, Abandoned, Active, Inactive,
Unsupported, Moved), and judging health by issue resolution time,
time-to-PR-merge, download counts and a named maintainer list rather
than commit frequency.
Discussion ran to April 2026.
Nothing has been adopted.

### The registry's only real lever

General's AutoMerge guidelines
(<https://juliaregistries.github.io/RegistryCI.jl/stable/guidelines/>)
require upper-bounded `[compat]` entries for all non-JLL dependencies,
and an upper-bounded `[compat]` for `julia` itself.
Whether to extend that to JLL dependencies is still open
(JuliaRegistries/RegistryCI.jl#394).
The guidelines describe themselves as "deliberately conservative" and
exist only to provide a fast path so manual review is not needed for
every package.
So the registry constrains version ranges and nothing else.
It has no view on whether a package is maintained.

### Genuinely unanswered

There is no accepted answer to "should I take this dependency".
No maintenance signal in the registry, no adopted status vocabulary, no
disputes procedure, no norm about vendoring versus forking versus
taking the risk.
This one is worth putting to the room.

---

## Q3. What does treating AD like a first-class citizen look like?

### The interface layer is settled

DifferentiationInterface.jl is now the answer.
It has a JMLR paper, "A Common Interface for Automatic
Differentiation" (<https://www.jmlr.org/papers/v27/25-1024.html>,
preprint at <https://arxiv.org/abs/2505.05542>).
It supports 15 dense backends declared through ADTypes.jl
(<https://juliadiff.org/DifferentiationInterface.jl/DifferentiationInterface/stable/explanation/backends/>):
ChainRules, Diffractor, Enzyme, FastDifferentiation, FiniteDiff,
FiniteDifferences, ForwardDiff, GTPSA, HyperHessians, Mooncake and
MooncakeForward, PolyesterForwardDiff, ReverseDiff, Symbolics,
Tracker, Zygote.
Its preparation mechanism amortises one-time setup per backend.

Turing has fully switched to DifferentiationInterface for AD of models
(<https://turinglang.org/news/posts/2025-02-28-newsletter-1/>).
Turing's own documentation says its preferred backends are ForwardDiff
and Mooncake, supported natively through their public APIs, with other
backends reached through DifferentiationInterface.
It also says Turing is "most extensively tested with ForwardDiff.jl
(the default), ReverseDiff.jl, and Mooncake.jl" and runs "a smaller set
of tests with Enzyme.jl".
That is the closest thing to a production-readiness statement anyone
publishes, and it is a sentence in a docs page rather than a policy.

### Known rough edges, stated by the maintainers

The DI documentation is candid.

- Enzyme: "Enzyme.jl's handling of activities and multiple arguments
  is not fully supported here, which can cause slowdowns or errors."
  Users are told to consider Enzyme's native API instead if
  differentiation fails or is slow.
- Diffractor: "The latest releases of Diffractor broke
  DifferentiationInterface."
- ReverseDiff with compilation risks "silently wrong results whenever
  it takes new branches that were not taken during preparation".
- Second-order AD: "Second-order AD is tricky, and many backend
  combinations will fail (even if you combine a backend with itself)."

The backends with the widest operator support in DI's own feature
matrix are ForwardDiff, FastDifferentiation, Symbolics and Enzyme.

### Does anyone else run a per-backend CI matrix?

Yes, two, and it is worth naming both.

**DifferentiationInterface.jl itself** runs one CI job per backend.
Verified from `.github/workflows/Test.yml` via the GitHub API.
The `test-DI-Backend` job matrixes 16 groups (ChainRules,
DifferentiateWith, Enzyme, FastDifferentiation, FiniteDiff,
FiniteDifferences, ForwardDiff, GTPSA, HyperHessians, Mooncake,
PolyesterForwardDiff, ReverseDiff, SparsityDetector, Symbolics,
Tracker, Zygote, with Diffractor commented out) across Julia 1.10,
1.11 and 1.12, each with its own test environment.
This is the reference implementation of the idea.

**TuringLang/ADTests** did the same thing at the model level, running
one job per model against every backend and publishing a compatibility
table at turinglang.org/ADTests.
It was built on `DynamicPPL.TestUtils.AD.run_ad`.
It was archived on 15 June 2026 and is read-only.
The published intent was that the utilities move into DynamicPPL so AD
package authors can test against a fixed set of Turing models.
Worth saying plainly in the talk that the one public per-backend
compatibility table for a probabilistic programming stack was
retired this year and has not been replaced with an equivalent public
view.

**CensoredDistributions.jl** does a third variant, verified from the
repo.
`.github/workflows/ad-backend.yaml` is a reusable workflow taking a
display name, a test-item tag and a Codecov flag.
Six thin caller workflows invoke it, one each for ForwardDiff,
ReverseDiff, Enzyme forward, Enzyme reverse, Mooncake forward and
Mooncake reverse.
The comment in the file gives the reason.
Each backend gets its own status badge while the test code stays in one
place, and each backend gets its own Codecov flag so you can see which
lines that backend actually exercises.
The per-backend Codecov flag is the part I did not find anywhere else.

**DifferentiationInterfaceTest.jl** is the tool for the correctness
side.
It offers custom scenarios, correctness checks, type stability checks,
call counting, and runtime and allocation benchmarks, with the stated
aim of making it easy to know "for a given function: which AD backends
can differentiate it [and] how fast they can do it".

### Genuinely unanswered

Nobody publishes AD compatibility for a *stack* of packages.
DI tells you which backends work for a function.
DIT lets you test your own package.
Turing tells you which backends it tests.
There is no mechanism, and no convention, for telling a user which
backend will work for a model assembled from five packages that each
tested independently.
That is the version of the question worth asking the room.

---

## Q4. Ecosystem-level release management

### SciML has the most developed answer, in workflow files

Verified from `SciML/OrdinaryDiffEq.jl/.github/workflows` via the
GitHub API.
The repo carries `Downstream.yml`, `Downgrade.yml`,
`DowngradeSublibraries.yml` and `SublibraryCI.yml` alongside the usual
CI, docs, format and TagBot workflows.

`Downstream.yml` (job name `IntegrationTest`) checks out each
downstream repo, `Pkg.develop`s the current package and all its
sublibraries into that repo's environment, runs `Pkg.update()`, and
runs the downstream test suite.
The matrix lists twelve (repo, test group) pairs, including
DiffEqCallbacks.jl, five groups of SciMLSensitivity.jl and four groups
of ModelingToolkit.jl.
Two entries are repos outside the SciML org,
`nathanaelbosch/ProbNumDiffEq.jl` and `SKopecz/PositiveIntegrators.jl`.
That last detail is the important one.
SciML runs its reverse dependency CI against packages it does not own.

The stated policy from the SciML style guide is that tests "should
include downstream tests to major packages which use the
functionality", and that any update breaking the downstream tests
should be followed by a notification to the downstream package
explaining why, "preferably in the form of a PR that fixes it"
(<https://docs.sciml.ai/SciMLStyle/dev/>).

### Downgrade CI

`julia-actions/julia-downgrade-compat`
(<https://github.com/julia-actions/julia-downgrade-compat>) tests a
package against the oldest versions its `[compat]` entries allow.
Recent versions use Resolver.jl's SAT-based resolver to find a real
minimal resolution rather than rewriting `Project.toml` entries.
Three modes: `deps` (direct dependencies only, the recommended
default), `alldeps` (adds weak dependencies), and `forcedeps` (asserts
the resolved versions match the declared lower bounds exactly).
The problem it solves is stated well.
Compat entries get set once and forgotten, tests run against the
newest versions by default, so a package can quietly start requiring
features from a newer dependency than it declares.
The Discourse PSA is
<https://discourse.julialang.org/t/psa-add-downgrade-ci-to-better-check-version-compatibility/110063>.
CensoredDistributions.jl already has this.

### Centralised documentation

MultiDocumenter.jl (<https://github.com/JuliaComputing/MultiDocumenter.jl>)
aggregates Documenter.jl output from many packages into one site with
a single global search bar.
SciML uses it to build docs.sciml.ai from the SciMLDocs repo
(<https://github.com/SciML/SciMLDocs>), which is listed as depending on
MultiDocumenter 0.8.0.
SciMLDocs describes itself as pooling the docs of the SciML libraries
to "paint the overarching picture, establish development norms, and
document the shared/common functionality".
Note that phrase for what the site is for.
It is not just a search box over many docs, it is where the shared
interface and the development norms live.

SciML also publishes a maturity classification per package
(High, Medium, Low, Research) precisely to manage expectations across
a heterogeneous set of packages.
That is a cheap idea to copy and it partly answers Q2 within an org,
even though the registry does not offer it ecosystem-wide.

### Genuinely unanswered

How to release many packages that must work together is solved in
SciML's CI configuration but is not written down as guidance anywhere.
There is no Julia-wide convention for coordinated releases, no
ecosystem version number, no tool that answers "which versions of
these eight packages are known to work together".
Downstream CI catches breakage before you tag, but nothing records the
answer for a user afterwards.

---

## Things I could not verify, so keep off the slides

- Exact package counts per org. The API gives repo counts and SciML's
  own figure of ~200 packages is self-reported in a 2025 blog post.
- Makie funding from the Sovereign Tech Agency or Muon Space. Reported
  in search summaries, no primary source found.
- Download or user numbers for any of these packages.
- Any claim that a particular AD backend is "production ready". Nobody
  makes that claim in those words. Turing's phrasing about what it
  tests most extensively is the strongest available statement.

---

## The four questions for the closing slide

These are the author's four questions, sharpened to the point where the
research showed there is no published answer.
Each one is a real gap, not a rhetorical device.

1. **Every large Julia org wrote its governance after it was already
   big. What is the smallest governance you can start with?**
   JuMP, SciML and Turing all formalised as they approached 1.0 or
   later. None of them documents how a new org should start, or how a
   package joins one.

2. **Julia has no rOpenSci. Should it, and would a domain ecosystem be
   the right place to try?**
   The median Julia package has two contributors. There is no software
   peer review, no adopted maintenance status vocabulary, and no
   registry disputes procedure. How should I decide whether to take a
   dependency on a package with one maintainer?

3. **Who tells a user which AD backend works for a model built from
   five packages?**
   DifferentiationInterface tells you about a function.
   DifferentiationInterfaceTest lets you test your own package.
   Turing's ADTests published the only stack-level compatibility table
   I found and it was archived in June 2026. Nothing composes.

4. **How do you release twenty packages that have to work together,
   without a monorepo?**
   SciML's downstream CI, downgrade CI and MultiDocumenter site are the
   best answer available, and they exist as workflow files rather than
   as guidance. There is no way to record, for a user, which versions
   of a set of packages are known to work together.

An alternative to swap in for (1) if the room is more applied than
infrastructural.

- **Is there a Julia ecosystem whose users are mostly not developers?**
  SciML, Turing and JuMP are used by technically strong people.
  Oceananigans and SpeedyWeather come closest to a domain audience and
  are both still small. I could not find a counterexample, and this is
  the audience an infectious disease ecosystem has to reach.
