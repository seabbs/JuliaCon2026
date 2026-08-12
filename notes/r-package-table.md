# R package table: verified numbers

For the roadmap deck's "I tried in R" slide (spec section 6).
All figures retrieved 2026-08-12.
Do not edit any deck from this file; hand the numbers to whoever builds
the slide.

## Table

| Package | GitHub stars | CRAN downloads, all-time | CRAN downloads, last month | Repo created |
|---|---|---|---|---|
| EpiNow2 | 141 | 58,073 | 739 | 2020 |
| epinowcast | 67 | not on CRAN | not on CRAN | 2021 |
| epidist | 16 | not on CRAN | not on CRAN | 2023 |
| primarycensored | 9 | 11,294 | 538 | 2024 |
| CensoredDistributions.jl | 15 | 122 (all-time, JuliaHub) | 6 (last month, JuliaHub) | 2024 |

CensoredDistributions.jl is a Julia package, not CRAN. Its download
column uses juliapkgstats.com (JuliaHub download-server logs) in place
of CRAN, as the spec asks.

## Sources, by figure

**GitHub stars** (`gh api repos/<owner>/<repo>`, field
`stargazers_count`, retrieved 2026-08-12):

- EpiNow2: 141. `gh api repos/epiforecasts/EpiNow2`.
- epinowcast: 67. `gh api repos/epinowcast/epinowcast`.
- epidist: 16. `gh api repos/epinowcast/epidist`.
- primarycensored: 9. `gh api repos/epinowcast/primarycensored`.
- CensoredDistributions.jl: 15. `gh api
  repos/EpiAware/CensoredDistributions.jl`. Found via `gh search repos
  CensoredDistributions`; the package lives in the EpiAware org, not
  epinowcast.

**Repo created** (`created_at` from the same `gh api` calls, retrieved
2026-08-12):

- EpiNow2: 2020-06-17 -> 2020.
- epinowcast: 2021-10-29 -> 2021.
- epidist: 2023-07-28 -> 2023.
- primarycensored: 2024-08-21 -> 2024.
- CensoredDistributions.jl: 2024-09-24 -> 2024.

**CRAN status** (`https://cran.r-project.org/package=<pkg>` and
`https://cran.r-project.org/web/packages/<pkg>/index.html`, retrieved
2026-08-12):

- EpiNow2: on CRAN. First published 2020-09-01, per
  `https://crandb.r-pkg.org/EpiNow2/all` (earliest timeline entry,
  version 1.1.0).
- primarycensored: on CRAN. First published 2024-10-28, per
  `https://crandb.r-pkg.org/primarycensored/all` (earliest timeline
  entry, version 1.0.0).
- epinowcast: **not on CRAN**. `cran.r-project.org/package=epinowcast`
  returns "Object not found!"; `cranlogs.r-pkg.org` returns 0
  downloads for every window. Not guessed.
- epidist: **not on CRAN**. Same check, same result.

**CRAN downloads, all-time**
(`https://cranlogs.r-pkg.org/downloads/total/<from>:<to>/<pkg>`,
retrieved 2026-08-12, window = first CRAN publish date to 2026-08-11,
the last complete day cranlogs had data for):

- EpiNow2: 58,073. Window 2020-09-01 to 2026-08-11.
- primarycensored: 11,294. Window 2024-10-28 to 2026-08-11.

**CRAN downloads, last month**
(`https://cranlogs.r-pkg.org/downloads/total/last-month/<pkg>`,
retrieved 2026-08-12, window 2026-07-13 to 2026-08-11 as returned by
the API):

- EpiNow2: 739.
- primarycensored: 538.

**Julia downloads** (juliapkgstats.com API, retrieved 2026-08-12):

- All-time: `total_requests` = 122, from
  `https://juliapkgstats.com/api/v1/total_downloads/CensoredDistributions`.
- Last month: `total_requests` = 6, from
  `https://juliapkgstats.com/api/v1/monthly_downloads/CensoredDistributions`.
- juliapkgstats.com's own docs (`/api` page) confirm `total_downloads`
  is all-time and `monthly_downloads` is the trailing month, both
  counted as unique-IP download-server requests, not CRAN-style
  install events, so the two count different things and should not be
  read as directly comparable to the CRAN figures.

## Not verified / flagged

None. Every cell above traces to a live API call made 2026-08-12,
listed with the exact endpoint. The only substitutions are the
explicit "not on CRAN" cells for epinowcast and epidist, which are a
verified absence, not a guess.

## Note for whoever builds the slide

CensoredDistributions.jl's download count (122 all-time, 6 last
month) is two to three orders of magnitude below the CRAN packages.
That is expected: it is a new package on a much smaller registry, not
a like-for-like comparison. State that plainly on the slide if the
number is shown next to the CRAN ones, rather than implying it is a
small share of a comparable pool.
