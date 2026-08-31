# Migration plan

## Flagship: Multifidelity Operation-aware

The primary case combines operational-data clustering from `Operation-aware-aircraft-wing-design-optimization` with the multifidelity training and surrogate workflow from `Generalizable-multifidelity-wing-design-optimization`.

| Stage | Deliverable | Source material |
| --- | --- | --- |
| 1 | Config schema and asset resolver | common CRM bounds, modes, mesh/FFD references |
| 2 | Operational data preparation and representative-point clustering | operation-aware repository |
| 3 | SF/MF data loading, model training, and inference API | generalizable multifidelity repository; DataCRM baseline models |
| 4 | Weighted multipoint surrogate optimization | operation-aware and multifidelity drivers |
| 5 | ADflow validation and mission-level evaluation | operation-aware CFD/mission modules |
| 6 | Tecplot and publication-figure recipes | Tecplot visualization templates |

## Comparison cases

- `CRM_CFD_FFD`: single- and nine-point FFD optimization.
- `CRM_CFD_Mode`: mode-based CRM parameterization and optimization.
- `CRM_Data-driven`: single-fidelity data-driven optimization.
- `CRM_Multifidelity`: multifidelity surrogate optimization without operational clustering.
- `CRM_Operation-aware`: operation-aware CFD optimization without multifidelity surrogate modelling.
- `ADODG_Benchmarks`, `BWB`, and `Airfoil_2D`: benchmark and teaching cases.

## Migration rule

Port a legacy script only after replacing absolute paths with configuration, declaring its external MACH-Aero/ADflow requirements, and adding a small smoke test or documented dry-run. Until then retain it under `legacy/` with source provenance rather than exposing it as a supported case.
