# CFD Design Optimization

Unified research framework for CFD-based aerodynamic design optimization, centred on the **Multifidelity Operation-aware** CRM wing workflow.

## Main workflow

`operation data → clustering → multifidelity surrogate → weighted multipoint optimization → CFD validation → mission analysis → visualization`

The end-to-end implementation belongs in [`main_cases/Multifidelity_Operation-aware`](main_cases/Multifidelity_Operation-aware/). The other directories provide reusable components, focused comparison cases, and preserved historical material.

## Repository map

- `src/cfd_design_opt/` — reusable Python interfaces for geometry, CFD, surrogates, optimization, and operations.
- `main_cases/Multifidelity_Operation-aware/` — the flagship reproducible workflow.
- `cases/` — focused CRM, ADODG, BWB, and 2-D reference cases.
- `assets/` — manifests and small shared CRM inputs. Large meshes, datasets, models, and run outputs stay outside Git.
- `Tecplot_visualization/` — editable Tecplot layouts, macros, styles, helper scripts, and documentation.
- `legacy/` — source-preserving historical scripts not yet ported to the unified API.

## Scope of the initial version

This first commit establishes a clean structure, provenance, asset policy, and Tecplot resources. It deliberately does not claim that legacy scripts are immediately runnable: their hard-coded paths and MACH-Aero-version assumptions must be ported case by case.

See [`docs/migration-plan.md`](docs/migration-plan.md) for the staged migration plan and [`assets/manifests/crm-assets.md`](assets/manifests/crm-assets.md) for the canonical CRM assets.
