# Host node network

The atlas as a bipartite graph. Pathogens on the left coloured by class. Host modules on the right. Edges are documented exploit relationships.

```mermaid
flowchart LR
  Xoo[Xanthomonas oryzae]:::bact
  Pst[Pseudomonas syringae]:::bact
  Mo[Magnaporthe oryzae]:::fung
  Bgh[powdery mildew]:::fung
  Fg[Fusarium graminearum]:::fung
  Pi[Phytophthora infestans]:::oom
  Hpa[Hyaloperonospora a.]:::oom
  Cbsv[cassava brown streak v.]:::vir
  Rtv[rice tungro virus]:::vir
  Pb[Plasmodiophora brassicae]:::prot

  SWEET((SWEET))
  MLO((MLO))
  eIF((eIF4E))
  DMR((DMR6))
  SnRK((SnRK1))
  CALL((callose))
  COREC((coreceptor))
  PHOS((phospholipid))
  FHB((FHB1))

  Xoo --> SWEET
  Mo --> SWEET
  Mo --> SnRK
  Pst --> SnRK
  Bgh --> MLO
  Pi --> DMR
  Hpa --> DMR
  Pst --> DMR
  Pst --> COREC
  Mo --> COREC
  Pi --> COREC
  Cbsv --> eIF
  Rtv --> eIF
  Pb --> CALL
  Pi --> CALL
  Pi --> PHOS
  Mo --> PHOS
  Fg --> FHB

  classDef bact fill:#e74c3c,stroke:#922,color:#fff
  classDef fung fill:#27ae60,stroke:#164,color:#fff
  classDef oom  fill:#2980b9,stroke:#125,color:#fff
  classDef vir  fill:#8e44ad,stroke:#522,color:#fff
  classDef prot fill:#f39c12,stroke:#742,color:#fff
```

## Cross class convergence

```
                 bact  fung  virus oom   prot   classes
SWEET             X     X           X            3
DMR6              X     X           X            3
coreceptor        X     X           X            3
SnRK1             X     X                        2
phospholipid            X           X            2
callose                             X     X      2
MLO                     X                        1
FHB1                    X                        1
eIF4E                         X                  1
```

`>= 3` is the structural novelty zone. Those are the modules engaged by very different effectors and the most useful to defend ahead of time.
