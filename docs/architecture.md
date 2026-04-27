# Architecture

```mermaid
flowchart TB
  L[plant pathology<br/>literature] --> A[(host_targets.csv)]
  P[effector + host<br/>protein records] --> E[(effector_host_edges.csv)]
  W[(configs/weights.toml)] --> S[scoring.py]
  A --> S
  S --> AT[atlas.py<br/>process rollup]
  E --> N[novelty.py]
  N --> AT
  S --> R1[funcgenomic rank]
  AT --> R2[funcgenomic processes]
  N --> R3[funcgenomic novelty]
  R2 --> M[memo + shortlist]
  M --> V[validation packet]
  V --> H[partner labs]
```

Inputs on top, data layer in CSVs, three small Python modules in the middle, three CLI commands on the surface, and a memo plus validation packet at the end. That is the whole system.
