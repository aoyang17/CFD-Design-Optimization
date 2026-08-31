# Canonical CRM assets

The following files occur as identical copies across the predecessor repositories. This repository will maintain one authoritative copy per asset after data storage is selected; no large asset is copied in this initial commit.

| Asset | Role | Seen in |
| --- | --- | --- |
| `rot.xyz` | CRM FFD definition | CFD-based, DataCRM, generalizable multifidelity |
| `modes.dat` | CRM modal geometry basis | CFD-based, DataCRM, MF_data_aero, generalizable multifidelity |
| `L3_peter_rotat_mirror_bc.cgns` | CRM CFD volume mesh | CFD-based, DataCRM |
| `model_cl.h5`, `model_cd.h5`, `model_cm.h5` | low-fidelity NN baselines | DataCRM, MF_data_aero |
| `validating.dat` | CRM surrogate validation data | DataCRM, MF_data_aero |

## Storage policy

- Small, redistributable input files may be tracked beneath `assets/CRM/`.
- Large datasets, CGNS meshes, and model checkpoints belong in durable storage outside Git and are referenced by a versioned manifest containing path/URI, checksum, source, license or access restriction, and intended case.
- Generated CFD data, optimization histories, rendered images, and model-training outputs must never be committed.
