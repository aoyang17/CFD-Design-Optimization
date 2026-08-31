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

## Method organization

- `CFD-opt/` contains CFD-based CRM FFD/mode optimization, ADflow analysis, ADODG, BWB, airfoil, adjoint, MPhys, and operation-aware CFD workflows.
- `Data-opt/` contains single-fidelity and multifidelity surrogate workflows, operation-data clustering and mission analysis, EGO, and the integrated Multifidelity Operation-aware configuration.
- `Geometric_parameterization/` contains FFD setup helpers and distinct mode-based implementations retained for their required MACH-Aero/pyGeo compatibility.
- `viz/` contains all Tecplot visualization resources.

## Porting rule

Before presenting a script as a portable entry point, replace absolute paths with configuration and asset IDs, declare its MACH-Aero/ADflow requirements, and add a smoke test or documented dry-run.
