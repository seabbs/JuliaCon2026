# Delays deck: the structure the author asked for

> I think you are working from a spec you wrote not my prompts

WARNING TO ANY AGENT READING THIS. This file is a paraphrase, and it has
been wrong. It has previously invented a 14 line code limit, a generation
time section and a `ConvolvedDistributions.jl` section that the author never
asked for, and they were then applied as if they were his instructions.

`notes/steers.md` is the record of what he actually said. Where this file and
his words differ, his words win. If a requirement here is not traceable to a
quote, treat it as a suggestion.

This replaces the earlier version of this spec. Read `notes/style.md` first.

His outline, lightly punctuated, which is close to a running order:

> In the delays talk we need a slide introducing what an epidemiological delay
> is (this audience won't know), then we need "unfortunately, biases" as a
> title slide, and then censoring and right truncation as we have.
>
> We resolved we could solve this problem numerically and in some cases
> analytically. We first wrote primarycensored. This is modelled after base R
> distributions. However we needed fitting, so we added two extensions,
> fitdistrplus (show some of its horrible code) and Stan (a complete
> duplication of the code base). Unfortunately numerical integration in Stan
> didn't work so we had to recast as an ODE (show the nice things we tried).
> To share the Stan code to our ecosystem and others we had to write the
> copying code. To get partial pooling and time varying we had to extend brms
> into epidist, ick, hard.
>
> What about Julia, can we do better? The good: multiple dispatch,
> Distributions integration in Turing. The bad: AD backend support, which and
> how? Turned out some of our analytical solutions weren't AD compatible.
> Numerical integration also wasn't. Had to write a testing infrastructure,
> had to work out how to do this for AD, had to find
> DifferentiationInterfaceTest (nice). Had to try and understand how to
> recommend different AD backends. Had to write rules for our analytical
> solutions. Had to hack around the integral in sad confusion.
>
> No brms in Julia, so, maybe fine to let people hand-roll, but none of our
> users know Julia, so? Show R vs Julia version usage numbers. In my view the
> Julia version is clearly better, but how to get people to shift?

## The running order

### Act 1: the problem

1. **What an epidemiological delay is.** A new slide. This audience is Julia
   developers, not epidemiologists, and will not know. Infection to symptom
   onset, onset to hospitalisation, onset to death. Where the estimate ends
   up: forecasting, nowcasting, transmission models.
2. **A section divider titled "Unfortunately, biases".** His words. Keep the
   wry register, it is his.
3. **Censoring**, as the deck already has it, using the serial interval
   diagrams.
4. **Right truncation**, as the deck already has it.

### Act 2: what we built, and what each step cost

5. **We can solve this.** Numerically always, analytically in some cases.
   This is the hinge between the problem and the software.
6. **`primarycensored`.** Modelled on base R's distribution functions,
   `d`/`p`/`q`/`r`. Say that explicitly, it explains the shape of the API.
7. **But we needed fitting, so two extensions.**
   - `fitdistrplus`. **Show some of its horrible code.** Find a real,
     unflattering snippet and show it. This is the author being rude about a
     tool he chose to use, which is allowed, but it must be a real excerpt
     with a source line, not a caricature.
   - Stan. **A complete duplication of the code base.** The point is that the
     same maths exists twice, in two languages.
8. **Numerical integration in Stan did not work.** Recast as an ODE.
   **Show the nice things we tried** before that: the approaches that were
   attempted and abandoned. `notes/delays-stan-pain.md` has the PR trail.
9. **Sharing the Stan code meant writing the copying code.** The vendoring
   tooling, so downstream packages could use it.
10. **Partial pooling and time-varying meant extending brms into `epidist`.**
    "Ick, hard" is the register. Concrete evidence of the difficulty from the
    epidist repository, not a general assertion.

### Act 3: Julia

11. **Can we do better? The good.** Multiple dispatch. Distributions.jl
    integration, so it drops straight into Turing.
12. **The bad: automatic differentiation.** Which backend, and how?
    - Some of our analytical solutions were not AD compatible.
    - The numerical integration was not either.
13. **What that cost us.** A testing infrastructure. Working out how to test
    AD at all. Finding `DifferentiationInterfaceTest`, which is genuinely
    good, and say so. Working out how to recommend a backend to a user.
    Writing rules for the analytical solutions. Hacking around the integral.
    "In sad confusion" is his phrase and the honesty is the point of the
    slide.
14. **No brms in Julia.** Maybe it is fine to let people hand-roll, since a
    composed distribution drops into any model. But none of our users know
    Julia. So? Ask the room, no packages named, no names.
15. **R versus Julia usage numbers.** Keep the existing adoption slide. It is
    one of the best in the three decks.
16. **In my view the Julia version is clearly better. How do I get people to
    shift?** Close on that question.

## Notes

- **epinowcast.** An earlier steer asked for a population-level rung leading
  to `epinowcast`. This outline does not mention it. Treat it as dropped
  unless he says otherwise, but keep one clause if it fits naturally, since
  it is the other place `primarycensored.stan` is vendored.
- The Stan work is not an aside. `primarycensored` ships Stan functions,
  `epidist` fits through `brms` to Stan. Each package inherits the constraints
  of the one backend, so moving to Julia changes the backend, not just the
  language.
- Every package named gets a link.
- 15 minute slot. The deck currently runs 8 to 11 minutes, so there is room
  for the new material without cutting elsewhere.
