# Schema

## host_targets.csv

One row per crop x pathogen x host target line.

| field | type | range | meaning |
|---|---|---|---|
| crop | string | | rice, wheat, tomato, etc. |
| pathogen | string | | full pathogen name |
| pathogen_class | string | bacterium, fungus, virus, oomycete, protist, mixed | broad class for breadth counting |
| host_target | string | | gene or locus the row is about |
| host_process | string | | shared host process the target sits in (this is the rollup key) |
| evidence_score | float | 1.0 to 5.0 | how strong the published support is for this target being a real susceptibility lever |
| breadth_classes | int | 1 to 5 | curator estimate of how many pathogen classes are known in the literature to engage this process |
| tractability_score | float | 1.0 to 5.0 | how edit friendly is the locus today |
| deployability_score | float | 1.0 to 5.0 | how realistic is field deployment |
| fitness_risk | float | 1.0 to 5.0 | likelihood of yield or growth penalty |
| structural_novelty_flag | int | 0 or 1 | 1 if effectors hitting this target are structurally promiscuous across classes |
| primary_reference | string | | one citation, abbreviated |

## effector_host_edges.csv

One row per pathogen effector family x host module pair.

| field | type | meaning |
|---|---|---|
| pathogen | string | full pathogen name |
| pathogen_class | string | broad class |
| effector_family | string | name of the effector family or molecule |
| host_module | string | host process the effector engages (matches host_process from the atlas) |
| evidence | string | strong, medium, weak |
| note | string | one line note on the interaction |

## Rollup keys

The link between the two tables is `host_process` in `host_targets.csv` matching `host_module` in `effector_host_edges.csv`. The rollup uses both. Atlas rows give the substantive evidence per crop. Edges give the cross class breadth and feed the structural novelty signal.
