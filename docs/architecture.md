# Architecture

## System view

```mermaid
flowchart TB
  subgraph inputs[inputs]
    L[plant pathology<br/>literature]
    P[effector and host<br/>protein records]
    D[domain expert<br/>review]
  end
  subgraph data[data layer]
    A[(host_targets.csv<br/>14 rows, 12 columns)]
    E[(effector_host_edges.csv<br/>23 edges)]
    W[(configs/weights.toml)]
  end
  subgraph compute[compute layer]
    S[scoring.py<br/>five axis rule]
    AT[atlas.py<br/>process rollup]
    N[novelty.py<br/>structural promiscuity]
  end
  subgraph cli[cli surface]
    R1[funcgenomic rank]
    R2[funcgenomic processes]
    R3[funcgenomic novelty]
  end
  subgraph downstream[downstream artifacts]
    M[memo + shortlist]
    V[validation packet]
    H[partner labs]
    F[funder pitch]
  end
  L --> A
  P --> E
  D --> A
  D --> W
  A --> S
  W --> S
  E --> N
  S --> AT
  N --> AT
  S --> R1
  AT --> R2
  N --> R3
  R2 --> M
  M --> V
  V --> H
  V --> F
```

## Module view

```mermaid
classDiagram
  class TargetRow {
    +crop
    +pathogen
    +pathogen_class
    +host_target
    +host_process
    +evidence_score
    +breadth_classes
    +tractability_score
    +deployability_score
    +fitness_risk
    +structural_novelty_flag
    +primary_reference
    +convergence_score
  }
  class ProcessScore {
    +host_process
    +breadth_classes
    +evidence_score
    +tractability_score
    +deployability_score
    +fitness_risk
    +novelty_flag
    +crops_covered
    +pathogen_classes
    +convergence_score
  }
  class NoveltySignal {
    +host_module
    +pathogen_classes
    +effector_families
    +flagged
  }
  TargetRow --> ProcessScore : aggregated by host_process
  NoveltySignal --> ProcessScore : feeds novelty_flag
```

## Data flow on a single query

```mermaid
sequenceDiagram
  participant U as user
  participant CLI as funcgenomic CLI
  participant Sc as scoring.py
  participant At as atlas.py
  participant No as novelty.py
  U->>CLI: processes --top 5
  CLI->>Sc: load_targets(host_targets.csv)
  Sc-->>CLI: list[TargetRow]
  CLI->>No: load_edges + signal()
  No-->>CLI: novelty_modules
  CLI->>At: rollup_processes(rows, edges, novelty)
  At-->>CLI: list[ProcessScore]
  CLI-->>U: ranked process table
```

## State across the 12 weeks

```mermaid
stateDiagram-v2
  [*] --> setup
  setup --> curation: schema locked
  curation --> ranking: rows + provenance
  ranking --> memo: weights frozen with reasons
  memo --> handoff: shortlist written
  handoff --> [*]: validation packet shipped
  ranking --> curation: rubric review found row gaps
  memo --> ranking: reviewer changed a weight
```

The two reverse arrows are the part that matters. Curation, ranking, and memo phases all loop back when a domain reviewer finds something. The artifact gets better when the curator and the reviewer disagree productively.
