# JuliaCon 2026

Talk pages and slides for three talks at JuliaCon 2026, Thursday 14 August
2026, Muschel — N3.

Sam Abbott, London School of Hygiene & Tropical Medicine.

Rendered: [samabbott.co.uk/Juliacon2026](https://samabbott.co.uk/Juliacon2026)

## The talks

| Time | Talk | Page |
|---|---|---|
| 14:30–14:45 | Building a composable Julia ecosystem for infectious disease modelling | `roadmap/` |
| 14:45–15:00 | Estimating epidemiological delay distributions: from R/Stan to Julia | `delays/` |
| 16:45–17:00 | Composable probabilistic models can lower barriers to rigorous infectious disease modelling | `composable/` |

## Building

Requires [Quarto](https://quarto.org/) and, optionally,
[Task](https://taskfile.dev/) and [uv](https://docs.astral.sh/uv/) for QR
codes.

```sh
task          # render the site and all decks to _site/
task preview  # live-reloading preview
task qr       # regenerate QR codes
```

## Layout

- `index.qmd` — about me and links to the three talks
- `{roadmap,delays,composable}/index.qmd` — one page per talk: abstract,
  slides link, and resources
- `{roadmap,delays,composable}/slides.qmd` — the deck, with sections in
  `_partials/`
- `prompts.qmd` — the brief that made this, and the steers that followed
- `figures/` — shared figures and the QR codes, one per talk page

The QR code on each deck points at that talk's page here, not at the slides.

These pages and slides were drafted by coding agents; `prompts.qmd` describes
how.
