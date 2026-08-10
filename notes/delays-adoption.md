# Delays talk: adoption numbers (primarycensored vs CensoredDistributions.jl)

Retrieved 2026-08-10.
All figures below are as returned by the cited API or page on that date.

## Headline (5 lines)

- primarycensored (CRAN): 11,211 downloads all-time (since 2020-01-01),
  7,872 in the last 365 days, 511 in the last month. Badge reads "11K".
- CensoredDistributions.jl (JuliaPkgStats): 116 total requests all-time,
  49 in the last month.
- primarycensored has two confirmed CRAN reverse-imports (EpiNow2,
  distspec) plus two GitHub-only R packages that import it (epidist,
  epinowcast), all epinowcast-ecosystem packages by the same group.
- CensoredDistributions.jl is registered in Julia General but its
  confirmed dependents are EpiAware's own packages plus repos owned by
  Sam Abbott, Sam Brand, and Sebastian Funk. No independent third-party
  adopter found.
- This is not a straight win for Julia: primarycensored is ~100x more
  downloaded and sits under an ecosystem of packages used in public
  health delay-estimation work; CensoredDistributions.jl is used by the
  author and a small circle of close collaborators.

## primarycensored (R, CRAN)

Source: https://cranlogs.r-pkg.org/downloads/total/2020-01-01:2026-08-10/primarycensored
Retrieved 2026-08-10.

- All-time (2020-01-01 to 2026-08-10): 11,211 downloads.
- Last 365 days (2025-08-10 to 2026-08-10): 7,872 downloads.
- Last month (2026-07-10 to 2026-08-08): 511 downloads.
- Grand-total badge (cranlogs.r-pkg.org/badges/grand-total/primarycensored):
  displays "11K", aria-label "CRAN downloads 11K" — consistent with the
  figures above.

Caveat: CRAN download counts include CI runs, mirrors, and automated
package checks, not distinct human users. Same caveat applies in
spirit to the Julia numbers below, so the two are at least
methodologically comparable, but neither is a user count.

CRAN package page (cran.r-project.org/web/packages/primarycensored):
published 2026-06-15, version 1.5.1.

## CensoredDistributions.jl (Julia)

Source: https://juliapkgstats.com/api/v1/total_downloads/CensoredDistributions
and https://juliapkgstats.com/api/v1/monthly_downloads/CensoredDistributions
Retrieved 2026-08-10.

- Total requests (all-time as tracked by JuliaPkgStats): 116.
- Monthly requests (most recent month tracked): 49.

Note: JuliaPkgStats' "requests" metric counts package-server hits
(includes CI resolves), same caveat as CRAN above. No longer-window
(e.g. last-year) endpoint was queried since the total already covers
the package's whole life; the package was created 2024-09-24.

## Reverse dependencies: primarycensored (R)

CRAN page reverse-dependencies field (authoritative for CRAN-listed
packages only):

- Reverse imports: **distspec**, **EpiNow2** (both on CRAN).
- No reverse depends, no reverse suggests listed.

Additional R packages that import primarycensored but are NOT on CRAN
(so do not appear in CRAN's reverse-deps field), confirmed by reading
each package's local DESCRIPTION file:

- **epidist** (epinowcast org): `Imports: primarycensored (>= 1.4.0)`.
  Not on CRAN (cran.r-project.org/web/packages/epidist returns 404).
- **epinowcast** (epinowcast org): `Suggests: primarycensored`
  (not Imports — used in vignettes/tests, not a hard runtime dependency).
  Not on CRAN (404).

So: 4 R packages use primarycensored (EpiNow2, distspec, epidist,
epinowcast). Three of the four (EpiNow2, epidist, epinowcast) are
maintained by the same epinowcast/epiforecasts group as
primarycensored itself; distspec is the one dependency from outside
that immediate circle, and I have not verified who maintains it or
how it uses primarycensored — flag as unverified if it goes in a slide.

## Public health agency use: what the evidence actually is

I looked for independent evidence of public-health-agency adoption
(README claims, papers, citations) and did not find any that is not
traceable back to the epinowcast group itself.

What I did find, and no more than this:

- A slide deck in `epinowcast/GuideToSTLTReportingDelays` (a guide the
  epinowcast group wrote, aimed at US state/tribal/local/territorial
  health department epidemiologists) lists primarycensored, epidist,
  and CensoredDistributions.jl together under "our tools" as part of a
  talk given to that audience.
  This is the epinowcast team describing its own tools to a public
  health audience, not a report of an agency having adopted the tool.
  Source: `~/code/epinowcast/GuideToSTLTReportingDelays/meeting/
  modelling-options-slides.qmd`, lines 152-161.
- primarycensored has a CITATION.cff / Zenodo DOI
  (10.5281/zenodo.13632839), so it is citable, but I did not verify
  any actual third-party citations of it — do not claim citation counts.

Correct framing for the slide: "the epinowcast ecosystem, which
includes packages built for public-health reporting-delay guidance,
says so" — not "public health agencies use primarycensored". Be
precise about this distinction if it goes on a slide.

## GitHub repo stats (context, not a headline number)

Source: `gh api repos/<org>/<repo>` and `.../contributors`,
retrieved 2026-08-10.

| | primarycensored | CensoredDistributions.jl |
|---|---|---|
| Stars | 9 | 15 |
| Forks | 9 | 2 |
| Created | 2024-08-21 | 2024-09-24 |
| Top contributor | seabbs (187 commits) | seabbs (119 commits) |
| Other named contributors | SamuelBrand1 (5), sbfnk (4), athowes (2), jamesmbaazam (2), barbora-sobolova (1), pearsonca (1), kaitejohnson (1), TimTaylor (1) | SamuelBrand1 (5), sbfnk (3), medewitt (9), damonbayer (2), jcblemai (1), Vyshnavi0702 (1) |

CensoredDistributions.jl has slightly more stars but this is a poor
proxy for use; keep it out of the slides or use it only to show the
contributor circle is genuinely small on both sides, which undercuts
any claim that Julia has a bigger community here — it doesn't, it has
roughly the same small circle of people, just far fewer downloads.

## Dependents of CensoredDistributions.jl (Julia General + EpiAware org)

Confirmed via `gh api search/code` for `CensoredDistributions` in
`Project.toml`/`Deps.toml` files, then verified each hit by checking
the file's `[deps]` section directly (not just a text match).

Registered in Julia General: yes
(`JuliaRegistries/General/C/CensoredDistributions/Package.toml`
exists).

Confirmed real dependents (CensoredDistributions listed under
`[deps]` or `[compat]` in a `Project.toml`, not just present in a
Manifest.toml or test-only target):

- `EpiAware/ComposableTuringIDModels.jl` — real dep, compat "0.2.22".
- `EpiAware/EpiAwarePrototype.jl` — real dep, compat "0.2.20".
- `sbfnk/EpiNow2.jl` (Sebastian Funk's Julia port of EpiNow2) —
  real dep, compat "0.2".
- `SamuelBrand1/RenewalExamples` — real dep.
- `SamuelBrand1/julia-inference-for-epi` — real dep.
- `sbfnk/DistributionHazards.jl` — test-only dep (`[targets] test =
  [...]`), not a runtime dependency.
- Several other EpiAware repos (`ComposedDistributions.jl`,
  `ConvolvedDistributions.jl`, `EpiAwareADTools.jl`,
  `LoweredDistributions.jl`, `ReparameterisedDistributions.jl`) use it
  only in `test/Project.toml`, i.e. as a test fixture, not a shipped
  dependency.
- `epiforecasts/BVDOutbreakSize` (the author's own DRC Ebola repo) has
  it in `Project.toml` — another use by the author himself.

No dependent outside the EpiAware org / Sam Abbott / Sam Brand /
Sebastian Funk cluster was found. This matches the brief precisely:
used by the author and a few close collaborators, not by anyone else.

## Sources checked and found empty or not useful

- GitHub code search for `primarycensored` and `CensoredDistributions`
  more broadly returns hundreds/dozens of hits, but the large majority
  are forks/mirrors of the packages themselves, registry snapshot
  repos (e.g. `codedownio/General`, `hyperpolymath/julia-ecosystem`,
  `nhabibi/MSSA` are unofficial or personal mirrors of the General
  registry, not evidence of use), and CI artefacts. I did not count
  these as adoption evidence.
- `epiforecasts/scoringutils` DESCRIPTION does not reference
  primarycensored.
- `epiforecasts/ForecastEnsembles.jl` matched the code search on
  `CensoredDistributions` but the term does not appear in its
  `Project.toml` `[deps]` — likely a stale search index hit or a
  comment/docstring; not counted as a dependent.

## Files/paths consulted

- `~/code/epiforecasts/EpiNow2/DESCRIPTION`
- `~/code/epinowcast/epinowcast/DESCRIPTION`
- `~/code/epinowcast/epidist/DESCRIPTION`
- `~/code/epinowcast/primarycensored/CITATION.cff`
- `~/code/epinowcast/GuideToSTLTReportingDelays/meeting/
  modelling-options-slides.qmd`
- `~/code/EpiAware/ComposableTuringIDModels.jl/Project.toml`
- `~/code/EpiAware/EpiAwarePrototype.jl/Project.toml`
- `https://cranlogs.r-pkg.org/downloads/total/...primarycensored`
- `https://cranlogs.r-pkg.org/badges/grand-total/primarycensored`
- `https://cran.r-project.org/web/packages/primarycensored/index.html`
- `https://juliapkgstats.com/api/v1/total_downloads/CensoredDistributions`
- `https://juliapkgstats.com/api/v1/monthly_downloads/CensoredDistributions`
- `gh api repos/EpiAware/CensoredDistributions.jl`
- `gh api repos/epinowcast/primarycensored`
- `gh api search/code` (multiple queries, see above)
