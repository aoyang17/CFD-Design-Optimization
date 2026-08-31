# Canonical CRM assets

The following files occur as identical copies across the predecessor repositories. The `crm-v1` manifest is the authoritative registry. Its first four small geometry assets reside beneath Aobo's external asset root; large assets are intentionally not copied into Git.

| Asset | Role | Seen in |
| --- | --- | --- |
| `rot.xyz` | CRM FFD definition | CFD-based, DataCRM, generalizable multifidelity |
| `modes.dat` | CRM modal geometry basis | CFD-based, DataCRM, MF_data_aero, generalizable multifidelity |
| `L3_peter_rotat_mirror_bc.cgns` | CRM CFD volume mesh | CFD-based, DataCRM |
| `model_cl.h5`, `model_cd.h5`, `model_cm.h5` | low-fidelity NN baselines | DataCRM, MF_data_aero |
| `validating.dat` | CRM surrogate validation data | DataCRM, MF_data_aero |

## Storage policy

- The first canonical files are installed below `/mnt/data2/aobo/CFD-Design-Optimization/assets/crm-v1/geometry/`; their paths and checksums are in `crm-v1.json`.
- Small, redistributable input files may be tracked beneath `assets/CRM/` when a portable Git copy is specifically needed.
- Large datasets, CGNS meshes, and model checkpoints belong in durable storage outside Git and are referenced by a versioned manifest containing path/URI, checksum, source, license or access restriction, and intended case.
- Generated CFD data, optimization histories, rendered images, and model-training outputs must never be committed.
