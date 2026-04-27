# Crop Host Atlas

This repo is a first pass at a practical project: assemble a small, inspectable atlas of host dependency factors for important crop pathogens, then use a simple ranking rule to decide which targets look worth validating first.

The motivation is straightforward. Crop disease work is still highly fragmented across pathogen-specific literatures, while the more interesting intervention opportunities may sit at the level of shared host processes: sugar transport, membrane trafficking, phospholipid metabolism, immune-metabolic control, and similar nodes that multiple pathogens exploit.

I am using this repo as an application artifact, but the goal is to keep it honest:

- a short project memo rather than a manifesto
- a small dataset rather than a fake platform
- a ranking prototype with explicit assumptions
- a concrete 12-week work plan

## Repo layout

- [docs/project-note.md](docs/project-note.md): concise project framing
- [docs/plan.md](docs/plan.md): twelve-week execution plan
- [docs/validation.md](docs/validation.md): what a real handoff to wet-lab partners would require
- [docs/sources.md](docs/sources.md): key sources
- [data/host_factor_candidates.csv](data/host_factor_candidates.csv): starter table of candidate targets
- [src/crop_host_atlas/scoring.py](src/crop_host_atlas/scoring.py): simple prioritization logic

## Current scope

The current dataset is deliberately narrow. It covers a few examples that are useful because they anchor different intervention styles:

- promoter editing in rice bacterial blight
- host-factor editing for broad resistance in rice
- susceptibility-factor perturbation with explicit fitness tradeoffs
- one viral crop example where the biology is less clean and the uncertainty is higher

That is enough to demonstrate the structure of the project without pretending the hard work is done.

## Running the prototype

The code has no external dependencies.

```bash
PYTHONPATH=src python3 -m crop_host_atlas.scoring
```

## If this were extended

The next useful step would be to expand the table into a real comparative atlas across a handful of crop-pathogen systems, add provenance at the row level, and make the ranking rubric easier to challenge and revise.
