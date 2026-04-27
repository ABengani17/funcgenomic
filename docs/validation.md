# Validation handoff

The hardest part of this project is not generating a plausible target list. It is producing a list that survives contact with agronomy. The ranking is upstream of validation. Validation is where the real cost lives.

## Four questions every candidate has to clear

```mermaid
flowchart TD
  C[candidate target] --> Q1{does perturbing it<br/>reduce disease burden}
  Q1 -- no --> X1[drop]
  Q1 -- yes --> Q2{does the effect<br/>generalise across<br/>strains or pathogen classes}
  Q2 -- no --> X2[narrow scope only]
  Q2 -- yes --> Q3{is the yield or<br/>growth penalty<br/>acceptable}
  Q3 -- no --> X3[interesting biology only]
  Q3 -- yes --> Q4{is there a realistic<br/>route to deployment<br/>in this crop}
  Q4 -- no --> X4[orphaned]
  Q4 -- yes --> Pass[validation handoff package]
```

Most plausible looking targets fail one of the inner questions. The ranker can rank well and still produce a list where two thirds of the rows drop out at question 2 or 3.

## Minimum viable validation per target

For each target on the short list:

- a relevant infection assay in an established model system
- effect size measurement, not just present or absent
- a parallel growth and fitness readout, so the disease answer does not hide the yield answer
- some attempt to separate `interesting mechanism` from `field plausible intervention`

The goal of the handoff is to make this small package easy to start, not to design the full study.

## What the partner needs from us

- the row level evidence behind the ranking, not just the final score
- the assumptions behind each weight in the rubric
- the failure modes the curator is worried about (these are usually the most useful part of the conversation)
- a list of candidate edits at the locus with at least one fallback if the first is hard to make

## Partner types worth approaching first

- plant pathology labs that already run infection assays in the relevant model
- crop genetics groups with established CRISPR or base editing pipelines in the target crop
- public sector breeding programmes with regulatory experience for edited crops in the target geography
- a small number of biosecurity oriented funders who care about cross pathogen defense

The right first conversation is rarely the most senior person. It is the postdoc who already has the assay running.

## What a no looks like

A clean negative is more valuable than a noisy positive. The handoff has to make it easy to say `we tried, it did not work, here is what we learned`. That includes:

- writing down failure modes ahead of time
- pre committing to what would change the ranking and how
- making the data and weights available so others can rerun the comparison without us
