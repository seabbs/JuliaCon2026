# Delays deck: the structure the author asked for

His words:

> For the delays talk we need what is a epidem delay, biases, doublecensoring,
> truncation with i.e. a diagram as we had in our recent serial interval talk.
> Then need software for this.. primary censored what is it etc, then well we
> need partial pooling blah blah well how extend brms okay epidist bt but. then
> but what about population level (i.e. nowcasting) epinowcast... What about in
> Julia... censoreddistibutions.

This replaces the deck's current structure. Read `notes/style.md` first.

## What is wrong with the deck as it stands

It is built as an R versus Julia implementation comparison: two
implementations, what Stan cost us, the honest scorecard, where this goes.
That is a talk about porting a package. The author wants a talk about a
problem and the software that grew up around it, ending in Julia.

Much of the current material survives, but it moves and it shrinks. The Stan
pain is no longer the spine of the talk. It is one honest aside inside the
`primarycensored` section.

## The structure

Two acts. The problem, then the software ladder.

### Act 1: the problem

1. **What is an epidemiological delay.** Infection to onset, onset to
   hospitalisation, onset to death. Why anyone cares: these feed forecasting,
   nowcasting and transmission models, so their biases propagate.
2. **The biases.** What goes wrong when you estimate one naively. Use
   `fig-charniga-flowchart.png` from the serial interval deck if it fits, and
   cite Charniga et al. (2024).
3. **Double interval censoring.** Both events are known only to a window.
   Reuse `fig-double-censoring.png`, and `fig-primary-censoring.png` and
   `fig-secondary-censoring.png` if there is room for the build-up.
4. **Right truncation.** In real time you only see pairs whose secondary event
   has happened. Reuse `fig-truncation.png`. The author asked for this
   diagram by name. The deck already has a generated
   `delays-right-truncation.png`; keep whichever is clearer, and prefer the
   serial interval one if they duplicate each other.

Carry the equations from `02-censoring.qmd` where they earn their place. They
are short and they are the actual content.

### Act 2: the software ladder

Each rung is a need, and the package that answers it. The rhetorical shape is
"that works, but now I want X", which is how the ecosystem actually grew.

**Stan is the through-line.** `primarycensored` ships Stan functions,
`epidist` fits through `brms` to Stan, and `epinowcast` is Stan. So rungs 5 to
7 are all one backend, and the constraints of that backend accumulate down the
ladder. The Julia rung is therefore not a change of language, it is a change
of backend, and that is what makes it worth the audience's attention. Make
that visible rather than leaving it implied.

5. **`primarycensored`.** What it is. The adjustment, the analytic solutions
   where they exist, numerical fallback otherwise.

   **Then what it took to make it work for fitting.** The author's
   correction:

   > we can still have what we needed to make it work for fitting. Stan is
   > what is used in i.e. epidist and i.e. epinowcast

   So the Stan work is not an aside about porting. Stan is the backend of the
   next two rungs, so the work to make these adjustments usable inside a Stan
   model is what makes `epidist` and `epinowcast` possible at all. That is
   why it belongs here, before them, rather than being cut.

   Keep it concrete: reimplementing distribution functions Stan does not
   have, the integral solver that would not hold and the recast as an ODE,
   the tooling to vendor the Stan code into downstream packages, and integer
   distribution identifiers standing in for types. Two slides, and it is
   earning them, because each one is a constraint the downstream packages
   inherit.

   The evidence is in `notes/delays-stan-pain.md`, with commit and PR
   references, and it was verified in an earlier round.
6. **But I want partial pooling.** Delays vary by setting, by age, by wave.
   How do you extend the model? `brms` gets you the regression machinery.
   That leads to **`epidist`**, which is that idea done properly. Then the
   "but": say plainly what is still awkward about it.
7. **But what about the population level.** Individual line list data is not
   always what you have, and nowcasting is a different problem. That leads to
   **`epinowcast`**. Again, say what it does and where it stops.
8. **What about in Julia.** **`CensoredDistributions.jl`**. Composable
   `Distributions.jl` wrappers, multiple dispatch picking closed forms,
   Turing.jl for fitting. Show the code, since the composition is the
   argument. This is the payoff of the whole ladder.

### Close

Where it goes next: modularisation into `ConvolvedDistributions.jl`, compound
distributions such as the generation time, and a composed Julia `epidist`.

Keep the honest adoption slide. "R wins this, by about a hundred to one" is
one of the best lines in the three decks and the author has said so. It fits
naturally just before or after the Julia rung.

## Constraints

- 15 minute slot. Aim for the same slide budget the deck has now, not more.
- Act 1 should be roughly half the talk. It is the part the audience needs to
  follow anything else, and it is the part with the good diagrams.
- Every package named gets a link in an attribution.
- Do not let Act 2 become a list of logos. Each rung must state the need
  first, in one line, before naming the package.
