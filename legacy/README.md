# Legacy source preservation

Each subdirectory preserves the small, versionable part of one predecessor repository as it was reviewed on 2026-08-31. These files are historical reference material, not supported entry points.

Excluded during import: Git metadata, CGNS/Tecplot data, Keras checkpoints, rendered media, archives, and individual files exceeding 1 MiB. The exclusions avoid duplicating large research assets in the source repository; their existence and canonical ownership are recorded in [`../assets/manifests/crm-assets.md`](../assets/manifests/crm-assets.md).

| Legacy directory | Original repository | Intended successor |
| --- | --- | --- |
| `CFD-based-optimization` | CRM FFD/mode CFD optimization | `cases/CRM_CFD_FFD`, `cases/CRM_CFD_Mode` |
| `CFD-FFD-Optimization` | early FFD, ADODG, BWB, and 2-D cases | benchmark/teaching cases |
| `DataCRM` | data-driven CRM inputs and NN baseline | `cases/CRM_Data-driven` |
| `MF_data_aero` | adjoint, MPhys, EGO, and data-driven prototypes | reusable method candidates |
| `Generalizable-multifidelity-wing-design-optimization` | MF data generation, training, and optimization | flagship surrogate stages |
| `Operation-aware-aircraft-wing-design-optimization` | clustering, CFD, and mission workflow | flagship operation and mission stages |
| `Tecplot_wing_visualization_templates` | original Tecplot collection | `Tecplot_visualization/` |
