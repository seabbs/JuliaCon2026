# LLM-driven org running: material for the roadmap talk

Gathered 2026-08-10. Covers the "very heavy LLM use for org" section:
figure, EpiAware-specific numbers, EpiAwareAgents status, Chris
Rackauckas cross-reference, and the contribution question.

## 1. The how-I-llm bot PR figure (verified numbers, as that repo
   settled on them)

Source: `~/code/seabbs/how-I-llm/figures/bot-prs-by-month.png`, built by
`figures/make_figures.py`. The numbers were wrong once and fixed in
commit `69e6236` ("fix: correct seabbs-bot pull request figures"),
which explains why the API needs total_count, not a paginated list:

> The previous numbers read 400+ PRs in 17 days, which was an artefact
> of the GitHub search API's 400-result cap. Uses search total_count
> instead: 1,643 PRs since January 2026, 84% merged, 11% closed
> unmerged.

The figure this settled on (snapshot taken end of July 2026, across
all of Sam's orgs, `seabbs-bot` only):

- **1,643** pull requests opened since January 2026, across **23**
  repositories
- **84%** merged, **11%** closed unmerged
- Monthly count: Jan 17, Feb 92, Mar 78, Apr 61, May 124, Jun 531,
  **Jul 740**
- Line to use with it (from `05-scale.qmd`): "Ten times the throughput
  at ten times the review load is not a win." About half of the closed
  unmerged were superseded by a later PR rather than rejected outright.

The figure file itself
(`~/code/seabbs/how-I-llm/figures/bot-prs-by-month.png`) can be reused
or rebuilt directly; it is a bar chart by month with the summary line
"1,643 total · 84% merged · 11% closed unmerged" printed on it.

## 2. EpiAware-org-specific numbers, re-verified today (2026-08-10)

Used `gh api search/issues` with `total_count`, not `gh search prs
--limit N`, for the same reason the how-I-llm repo had to fix its
figure (the plain search endpoint caps at 400/1000 results and a
`--limit` list undercounts silently).

**EpiAware org only, `author:seabbs-bot is:pr`, all time:**

- Total opened: **1,138**
- Merged: **966** (84.9%)
- Closed unmerged: **119** (10.5%)
- Still open: **53**
- (966 + 119 + 53 = 1,138, checks out)

Distinct repos with at least one `seabbs-bot` PR: **at least 16** (from
a sample capped at 400 results, so a lower bound, not exhaustive):
`.github`, `CensoredDistributions.jl`, `ComposableProbabilisticIDModels`,
`ComposableTuringIDModels.jl`, `ComposedDistributions.jl`,
`ConvolvedDistributions.jl`, `DistributionsInference.jl`,
`EpiAwareADTools.jl`, `EpiAwareAgents`, `EpiAwarePackageTools.jl`,
`LoweredDistributions.jl`, `ModifiedDistributions.jl`,
`ReparameterisedDistributions.jl`, `ScoringRules.jl`,
`epiaware.github.io`, `tutorials`. The org has 22 repos total (`gh repo
list EpiAware`), so this is close to the full set once inactive/admin
repos (e.g. `ProjectProposals`, `JuliaForIDM`) are excluded.

**Overall across all of Sam's orgs, re-verified today (grows daily, so
higher than the how-I-llm snapshot from end of July):**

- Total opened: **1,814**
- Merged: **1,541** (84.9%)
- Closed unmerged: **204** (11.2%)

So the EpiAware-specific rate (84.9% merged / 10.5% closed unmerged) is
consistent with the org-wide figure quoted in how-I-llm (84% / 11%).
Safe to say on stage: "the same ratio holds inside EpiAware specifically
— it's not an artefact of one easy repo."

I looked for genuine revert PRs (a PR that reverts a prior bot PR) as a
proxy for "the agent shipped something wrong that had to be undone."
Searching `org:EpiAware author:seabbs-bot is:pr in:title revert` returns
3 hits, but all three are the same title —
`fix: auto-detect docs_subdomain on update so hosting is not reverted
(#123)` — which contains the word "reverted" describing a bug being
fixed, not an actual revert-a-PR PR. **I found no evidence of an actual
revert rate in the org.** Do not claim a revert-rate number on stage;
say instead that a title-text search for reverts found nothing, which
is itself worth a line if useful ("I went looking for a revert-rate
number and couldn't find one — that's a gap I'd like to fix, not a
claim of zero").

Review turnaround (proxy for human review load): last 30 merged
EpiAware bot PRs, `created_at` to `closed_at`:

- Median: **~3.0 hours**
- Mean: **~10.1 hours**
- Range: 6 minutes to 71 hours

This is a small, recent sample (last 30 merged, not the full 966), so
treat as illustrative, not a claimed org-wide average.

## 3. EpiAwareAgents — what it is, and what is actually running

Local path: `~/code/EpiAware/EpiAwareAgents`.

**Status, stated plainly in its own README:** "Status: design phase.
Nothing here runs yet." I checked this against the evidence rather than
just trusting the README:

- The paired private reports repo, `EpiAware/EpiAwareAgentReports`
  (which the design says gets a daily push once the fleet runs), has
  exactly **one commit** ("Create README.md"), dated 2026-07-26, and
  `pushed_at` is also 2026-07-26. No daily reports have landed. This
  confirms the README: the fleet is not live.
- `deploy/epiaware-agent@.timer` is a systemd timer **template with no
  `OnCalendar` in it** by design — the design doc explains the real
  jittered schedule is host-local and deliberately not committed to the
  public repo (so a prompt-injection attacker can't read the org's
  schedule off GitHub). So "is there a cron schedule" has a real answer
  either way: there is no committed schedule, and the intended
  mechanism is systemd timers (not cron), specifically because
  `Persistent=true` lets a sleeping desktop catch up on wake.

**What it is, in one paragraph** (from the repo's own README): a
GitHub App identity (`epiaware-agent[bot]`) that would act across the
EpiAware org with per-job, per-repo, 1-hour tokens. Jobs run on systemd
timers on Sam's own desktop, one fresh container per work unit, with
all behaviour defined in the repo (not the host's personal Claude
setup). Nightly jobs are designed to triage issues, draft designs,
implement a review-debt-gated trickle of easy PRs (always opened as
draft, and the agent **never merges**), and unstick stalled PRs. A
weekly retrospective is designed to feed cross-package patterns back
into shared org tooling — this is the closest thing to "runs as public
standards enforcement," per the author's framing, though it is not
live. A private, tailnet-only daily report plus an off-host dead-man's
switch is the intended safety net if the desktop goes quiet.

Nine job stages are fully built out in code (`00-sync` through
`70-report`, including `20-design`, `40-unstick`, `45-deps`,
`50-implement`, `55-retro`, `60-escalate`), with a harness, host-side
push guard, and token broker — so this is a complete, reviewed design
and implementation, just not switched on. `DESIGN.md` records that the
org lead (Sam) made explicit decisions during design review, including
keeping reports private (not public Pages) and a hard "never merge"
rule enforced in the harness, not just documented.

**Line for the talk:** "The design is done and the code is written.
What isn't done is turning it on. That's deliberately the last step,
not an accident."

## 4. Chris Rackauckas at JuliaCon 2026

**Confirmed, from JuliaCon's own keynotes page
(`juliacon.org/2026/keynotes/`): Rackauckas is NOT one of the four
confirmed keynote speakers.** The confirmed keynotes are Julia
Kowalski (RWTH Aachen), Zoë Holmes (EPFL), Paul Tiede (Black Hole
Initiative, Harvard), and Simon Peyton Jones (Epic Games). So "keynote"
in the author's framing is not correct — if he is speaking, it is a
regular talk slot, not a keynote.

**Not independently confirmed, single source only:** a JuliaHub company
blog post (`juliahub.com/blog/juliahub-at-juliacon-global-2026`) lists
three Rackauckas sessions at JuliaCon 2026, including one that matches
the author's framing exactly:

- **"The Agentic AI Maintenance Bots of the SciML Organization"**
  — long talk — Wednesday 12 August, 10:00-10:30 CEST — Muschel — N2

  (plus two unrelated SciML/ODE-solver talks the same day, same
  building, different room — not relevant here)

I could not corroborate this specific title, time, or room on a second
source: a direct web search for the exact title returns zero hits, and
the JuliaCon pretalx schedule/speaker-search pages either 404'd or
returned no results for "Rackauckas" when fetched directly (the
official schedule is still marked "preliminary and subject to change"
as of today). **Treat this as unconfirmed** — plausible (JuliaHub's own
blog naming its own VP's session titles is a reasonably strong signal)
but not verified against JuliaCon's own schedule data. If it holds up,
it is a strong on-stage reference: same building (Muschel) as this
talk's room (N3), one day earlier, and directly on-topic — "an agentic
maintenance-bot talk happened in this building yesterday; here's the
Julia-ecosystem, infectious-disease-modelling version of that
question." Recommend the author check the live schedule at
`juliacon.org/2026/schedule/` or `pretalx.com/juliacon-2026/schedule/`
before the talk, since today (10 August) is day one of the conference
and the schedule may firm up over the week.

## 5. The contribution question: what does agent-authored-majority mean
   for an open source org?

What I found, concretely, in EpiAware repos:

- **No CONTRIBUTING.md or AGENTS.md in the package repos I checked**
  (`CensoredDistributions.jl`, `ComposableProbabilisticIDModels`,
  `EpiAwarePackageTools.jl`, `EpiAwareADTools.jl`) — 404 on all of
  them. `ComposableProbabilisticIDModels` has a `CLAUDE.md`, the others
  don't have any agent-facing policy file at all.
- The **only** CONTRIBUTING.md addressing agent contribution in the org
  lives in the not-yet-live `EpiAwareAgents` repo, and it isn't aimed
  at human contributors at all — it's instructions for how a *human*
  directs the *bot* (`@epiaware-agent <request>`, comment-only, no
  edited comments, numeric-ID authorization, tiered refusals for
  unauthorized org members). There is currently no public document in
  the org explaining to a human contributor what changes when most PRs
  are agent-authored.
- The `EpiAwareAgents/CLAUDE.md` "agent constitution" is explicit that
  the agent **never merges, never approves, never enables auto-merge** —
  every change ends at a PR a human merges — and has a "no-debate rule"
  (the bot may push commits addressing review feedback and post one
  neutral summary, but never argues with a reviewer; disagreement goes
  to a human as an attention item, not into the PR thread). That's a
  policy answer to "what changes for reviewers," even though the system
  implementing it isn't running yet.
- Review-turnaround evidence (section 2 above): median ~3 hours from
  PR open to merge on a recent sample. That's fast, and consistent with
  small, single-purpose PRs rather than slow deliberate review — worth
  pairing with the "review gate working" framing rather than "review is
  being skipped."
- I found **53 currently-open** EpiAware-org PRs authored by
  `seabbs-bot` — a live number for "how much review debt is
  outstanding right now," if useful, though I have not classified how
  many are stale vs. awaiting review vs. blocked on CI.
- No revert-rate evidence either way (see section 2) — an honest gap,
  not a zero.

Suggested framing for the slide, staying inside what's verified: most
PRs in this org are now agent-opened, review remains 100% human-gated
by policy and in practice (never-merge is enforced in the harness for
the *next* system, and is simply true today because there is no
autonomous merge path at all), turnaround is fast, and the org has no
public-facing document yet that tells a new human contributor what any
of this means for them. That absence is itself a finding worth putting
in front of a JuliaCon audience — a live "what should exist"
question rather than a claimed answer.

## Sources

- `~/code/seabbs/how-I-llm/_partials/05-scale.qmd`,
  `_partials/06-money.qmd`, `_partials/03-tooling.qmd`
- `~/code/seabbs/how-I-llm/figures/make_figures.py`,
  `figures/bot-prs-by-month.png`
- `~/code/seabbs/how-I-llm` git log, commit `69e6236`
- `gh api search/issues` queries against `org:EpiAware` and global,
  run 2026-08-10 (see counts above; re-run before the talk if the
  numbers need to be current on the day)
- `~/code/EpiAware/EpiAwareAgents`: README.md, DESIGN.md, CLAUDE.md,
  CONTRIBUTING.md, jobs/README.md, deploy/epiaware-agent@.timer
- `gh api repos/EpiAware/EpiAwareAgentReports` and its commit history
- `juliacon.org/2026/keynotes/` (confirmed keynote list)
- `juliahub.com/blog/juliahub-at-juliacon-global-2026` (single-source,
  unconfirmed Rackauckas session details)
