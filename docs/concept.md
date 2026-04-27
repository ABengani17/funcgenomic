# Concept

Crop pathogens from different kingdoms (bacteria, fungi, viruses, oomycetes) often need the same host machinery to infect successfully. Sucrose transporters, translation factors, salicylate signalling, callose deposition, a few metabolic gates. If you map which host nodes are repeatedly used, you can prioritise broad spectrum defenses instead of chasing one pathogen at a time.

This repo is the smallest honest version of that map plus a transparent rule for ranking which host nodes to defend first.

## Why it matters

- Plant pests and disease still cause roughly 20 to 40 percent crop losses depending on the system.
- Classical R gene breeding targets pathogen recognition. Pathogens evolve around it in 3 to 7 years.
- Host side defense is durable when the host process is something the pathogen actually needs (`mlo` in barley has held for over 40 years).
- Frontier protein design models can produce effectors with no sequence match to anything in databases. That weakens homology based DNA synthesis screening. A functional map of host bottlenecks does not lose value when sequence space stops being the right index.

## What already works

- `MLO` in barley, wheat, tomato. Loss of function gives durable powdery mildew resistance.
- `eIF4E` and `eIF(iso)4E` across rice, tomato, pepper, cassava. Recessive resistance to dozens of potyvirus species.
- `SWEET` promoter edits in rice. Block bacterial blight without losing the transporter function.
- `DMR6` and `DLO1` in tomato, potato, banana. Simultaneous resistance to bacteria, fungi, oomycetes.

## What is missing

- A structured atlas of host dependency factors across systems.
- A scoring layer for breadth, tractability, deployability, fitness cost.
- A ready to use validation handoff for top candidates.

## Why a transparent rule and not a model

Not enough labelled data to train a model that does not memorise. A simple weighted rule with the assumptions written out is honest, easy to argue with, and easy to revise. Editable weights are in `configs/weights.toml`.

## Honest limits

- The atlas is small. Several rows lean on a single primary paper.
- Ranking output is not directly actionable. It is an input to a wet lab conversation.
- The fitness risk axis is the most underreported in the literature and the one most likely to be wrong.
