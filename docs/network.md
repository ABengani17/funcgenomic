# The host node network

The atlas is a small bipartite graph. One set of nodes is pathogens. The other set is host modules. Edges are documented exploit relationships from the literature. Defending an exploited host node breaks all the edges going into it at once. The whole project is a way of turning that picture into a ranked list.

## Pathogens to host nodes

```mermaid
flowchart LR
  Xoo[Xanthomonas oryzae]:::bact
  Xao[Xanthomonas axonopodis]:::bact
  Pst[Pseudomonas syringae]:::bact
  Mo[Magnaporthe oryzae]:::fung
  Bgh[Bgh powdery mildew]:::fung
  En[Erysiphe necator]:::fung
  Fg[Fusarium graminearum]:::fung
  Pi[Phytophthora infestans]:::oom
  Hpa[Hyaloperonospora a.]:::oom
  Ps[Phytophthora sojae]:::oom
  Tlcv[tomato leaf curl virus]:::vir
  Cbsv[cassava brown streak v.]:::vir
  Rtv[rice tungro virus]:::vir
  Pvmv[pepper veinal mottle v.]:::vir
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
  Xao --> SWEET
  Mo --> SWEET
  Ps --> SWEET
  Mo --> SnRK
  Pst --> SnRK
  Bgh --> MLO
  Pi --> DMR
  Hpa --> DMR
  Pst --> DMR
  En --> DMR
  Pst --> COREC
  Mo --> COREC
  Pi --> COREC
  Tlcv --> eIF
  Cbsv --> eIF
  Rtv --> eIF
  Pvmv --> eIF
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

## The same network, collapsed to classes and modules

What it looks like once you stop caring about which species and only care about which class.

```mermaid
flowchart LR
  bacterium:::bact
  fungus:::fung
  oomycete:::oom
  virus:::vir
  protist:::prot

  bacterium --> SWEET
  fungus --> SWEET
  oomycete --> SWEET
  bacterium --> DMR6
  fungus --> DMR6
  oomycete --> DMR6
  bacterium --> coreceptor
  fungus --> coreceptor
  oomycete --> coreceptor
  bacterium --> SnRK1
  fungus --> SnRK1
  fungus --> MLO
  fungus --> phospholipid
  oomycete --> phospholipid
  fungus --> FHB1
  virus --> eIF4E
  oomycete --> callose
  protist --> callose

  classDef bact fill:#e74c3c,stroke:#922,color:#fff
  classDef fung fill:#27ae60,stroke:#164,color:#fff
  classDef oom  fill:#2980b9,stroke:#125,color:#fff
  classDef vir  fill:#8e44ad,stroke:#522,color:#fff
  classDef prot fill:#f39c12,stroke:#742,color:#fff
```

## Convergence heatmap

A coarse heatmap of which classes are documented to engage which host module in the atlas plus edges file.

```
                 bact  fung  virus oom   prot   sum
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

`sum >= 3` is the structural novelty zone. Those are the modules that show up in the literature as functionally promiscuous attractors and are the most useful to defend ahead of time.

## Reading the network

Three things to notice that the score table alone does not show:

1. **Hubs are sparse.** Most pathogens hit one or two modules in the atlas. Three modules (SWEET, DMR6, coreceptor) catch many. That is the convergence pattern.
2. **Class diversity matters more than edge count.** SWEET has more edges than DMR6 in absolute terms, but DMR6 reaches three classes too. Both are broad spectrum candidates. The ranker treats them as comparable.
3. **eIF4E is tall and narrow.** It looks like a hub but it only collects virus edges. Still very valuable, but the right framing is `viral broad spectrum` not `kingdom broad spectrum`.
