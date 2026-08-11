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

Much of the current material survives, but it moves. The Stan work is no
longer what the talk is mainly about. It sits inside the `primarycensored`
section, where it explains what the packages after it are built on.

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

Rungs 5 to 7 all fit with Stan. `primarycensored` ships Stan functions,
`epidist` fits through `brms` to Stan, and `epinowcast` is Stan. Each package
inherits the constraints of the one backend. So moving to Julia changes the
backend, not just the language, and the deck should say so directly.

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
   How do you extend the model? `brms` gets you the regression machinery, and
   that leads to **`epidist`**.

   The author's framing, which is the substance of this rung:

   > brms is a nice way to metaprogram Stan but is limited in terms of being
   > extensible. In epidist we try hard to extend it but it took a lot of
   > effort. If Julia had something like brms (which a few people, maybe here,
   > have been talking about) it would very likely be a lot more extensible
   > and flexible.

   So the rung has three beats:
   - `brms` is genuinely good. It metaprograms Stan and gives you the whole
     regression apparatus for free. Say so without hedging.
   - Extending it is hard. `epidist` does extend it, and that took a lot of
     effort. Get a concrete example of what was hard from the `epidist`
     repository and its git history rather than asserting it in general.
   - A Julia equivalent would very likely be more extensible, because the
     metaprogramming is not fighting a separate language with no user types.
     This connects back to the Stan constraints from rung 5.
   - **But for many use cases you would not need one.** His follow-up:

     > we might not need one for a lot of use cases, people can more easily
     > reuse i.e. censoreddistributions in any model

     This is the point the rung should end on, and it is the more interesting
     claim. `brms` exists partly because in R you cannot easily drop the
     delay machinery into a model you wrote yourself, so you need something to
     generate the model for you. In Julia the censored distribution is an
     ordinary `Distributions.jl` object, so it goes into any Turing model
     somebody writes, without a formula interface, without code generation,
     and without asking permission from a package author.

     So the honest position is not "Julia needs a brms". It is that a Julia
     brms would be more extensible if someone built it, and that a good deal
     of what brms is *for* stops being necessary once components compose.
     Say both.

   **The invitation to the room, framed accordingly.** A few people here may
   well be working on something like this. Say that, and ask the real
   question rather than making a request: where is a formula interface
   actually needed, once the components compose on their own? No call to
   action, and no names.

   This beat is also where the delays talk touches the composability argument
   from the 16:45 talk. One clause pointing at it is enough.

   **Do not name any candidate Julia package on this slide.** The author was
   asked whether he meant specific projects and said:

   > we just don't need to note those. I meant a few people in the room might
   > be working on something like this

   So the gesture is to the room, warmly and vaguely. No package list, no
   named individuals, no pointers to other talks in the programme.

   For the record, so nobody helpfully adds it back: `TuringGLM.jl` is not the
   answer. The author's view is that it is very narrow, not extensible, and
   dead, and the repository supports that. Its last release was v2.14.2 on 31
   August 2025, nearly a year before this talk, and commits since are
   dependency bumps, CI configuration and dependabot. It is not a `brms`.
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
