# Roadmap deck: the structure the author asked for

His verdict:

> For the ecosystem talk it's over indexed on the R stuff.

And the structure he wants, in his words, lightly punctuated:

> it should instead be we want to build this compose thing (brief bit on what
> that is and why, ref to the other talk) then what we wanted, something like
> epinowcast, something like SciML, something like Turing community, i.e.
> epinowcast, but that approach was hard. Multiple approaches possible so want
> to leave space for that. Something like rOpenSci for epi ideally.
>
> Need AD as a first class citizen for fitting. Need PPL support for any real
> world ID modelling. What does that look like, what did we need to do for AD
> testing, what does it mean to support AD? Guides for this in Julia
> ecosystem? All have small teams.
>
> Apart from AD, R has a lot of package quality checks. What does a good
> package look like in Julia? Aqua but need more? So add? Lots of CI needed.
> Maintainability with all the required infra. Need good docs and docstrings,
> Julia not good at that so need to enforce via the template.
>
> We don't have many/any contributors so far and realistically we need to make
> this work with AI going forward, how do we do that well? Package templates,
> but why not i.e. BestieTemplate etc? We need to make it more structured to
> force the shape on the AI I think. We also have our opinionated needs i.e. AD
> testing and benchmarking, we want to look at JET etc, stuff outside template
> support. Probably should have built it with their templating stuff but... We
> get all our CI from a central .github like i.e. SciML, use dependabot to
> update, use EpiAwarePackageTools to enforce structure, has docs for agents to
> look at. ... shape of org.

Read `notes/style.md` first.

## The main fault

The deck spends too long on the R ecosystem: what epinowcast was, what EpiNow2
could not do, the R packages we built. That is context, not the talk. It
should be compressed to the minimum needed to explain why we are here, and the
weight moved to the Julia questions, which are what this audience can actually
answer.

## The structure

### 1. What we are trying to build, briefly

Composable modelling in one or two slides. What it is, why it needs an
ecosystem of reusable components rather than one package. Point at the 16:45
talk for the argument rather than making it here.

### 2. What we wanted, and why the obvious route was hard

We wanted something with the community of **epinowcast**, the technical
coherence of **SciML**, and the ecosystem shape of **Turing**. We had
epinowcast in R, and that approach was hard. Say concretely why, briefly.

Then the two points that open the talk up:

- **Multiple approaches are possible** and we want to leave space for them.
  Composable Distributions, Turing submodels, SciML, hand-written models.
- **Ideally something like rOpenSci, for epidemiology.** That is the shape of
  the thing that does not exist in Julia.

### 3. AD as a first class citizen

- Any real-world infectious disease model needs a PPL, and a PPL needs AD that
  works. So AD support is not a nice-to-have, it is the requirement.
- What does it even mean to say a package "supports AD"? There is no settled
  answer, which is a genuine question for the room.
- What we had to build: per-backend CI, a fixture set, registered broken
  scenarios. `DifferentiationInterfaceTest` is very good and we still needed
  more on top.
- Are there guides for this anywhere in the Julia ecosystem? Every AD backend
  is run by a small team.

### 4. What a good Julia package looks like

- R has a deep stack of package quality checks. `R CMD check`, rOpenSci
  review, CRAN policy. Julia has `Aqua`, and then what?
- So we add: `JET`, benchmarking, docstring coverage, per-backend AD tests.
- All of that is CI, and the CI is itself infrastructure to maintain.
- Julia documentation and docstring culture is weak by default, so the
  template has to enforce it rather than suggest it.

### 5. Contributors, and building for AI

This is the honest bit and it should not be a victory lap. See
`notes/style.md`: this is not a talk about coding agents.

- We have few or no outside contributors so far. Realistically this ecosystem
  has to work with AI doing much of the writing.
- So the template has to be **rigid**, to force a shape on the model. That is
  the argument against a flexible template.
- Why not `BestieTemplate` or the existing community templates? Because they
  are deliberately modular, and we want uniformity. Concede plainly that we
  probably should have built on their templating rather than rolling our own.
- We have opinionated needs the templates do not cover: AD testing,
  benchmarking, JET.
- How it works now: a central `.github` repository supplying CI, as SciML
  does, dependabot to keep it current, and `EpiAwarePackageTools.jl` to
  enforce structure, including documentation written for agents to read.

### 6. The shape of an org, and the questions

Close on the open questions. Keep the existing closing slide, which is good:
smallest viable governance, no rOpenSci for Julia, who tells a user which
backend works for a model built from five packages, releasing eleven packages
that must work together, and whether any Julia ecosystem has users who are
mostly not developers.

## Constraints

- 15 minute slot.
- The R material earns at most two slides, as setup.
- BVDOutbreakSize stays as evidence about the workflow, briefly. It is not a
  story about how clever the agents were.
- Cut the mermaid diagrams added last round unless they show a mechanism.
  Several are box-and-arrow restatements of their own bullets.
