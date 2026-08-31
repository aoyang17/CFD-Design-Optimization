# CFD Design Optimization

Unified research repository for CFD-based aerodynamic shape optimization of aircraft wings. The repository contains two related, but distinct, research directions:

1. **Multifidelity aerodynamic shape optimization** — learning and optimization with single- and multi-fidelity aerodynamic data.
2. **Operation-aware aerodynamic shape optimization** — clustering flight-operational data into representative conditions and optimizing the wing over a weighted multipoint mission envelope.

The two directions share geometry, CFD, optimization, and visualization infrastructure, but their main cases and scientific contributions should be treated independently. The combined workflow is a later integration of these components, not a replacement for either case.

## Main research cases

### Multifidelity aerodynamic shape optimization

This case develops a generalizable, gradient-based data-driven workflow for high-dimensional wing optimization. It uses compact modal geometry parameterization, CFD data at multiple fidelity levels, single-fidelity neural surrogates, and residual-learning multifidelity models. The surrogate provides aerodynamic predictions and sensitivities to a multipoint optimizer, reducing the CFD evaluations required during the optimization stage.

Implementation: [`Data-opt/Multifidelity`](Data-opt/Multifidelity/).

### Operation-aware aerodynamic shape optimization

This case incorporates real flight-operational data into aerodynamic design. Operational variables are cleaned and clustered into representative flight conditions with weights; the resulting conditions define a cluster-based multipoint CFD optimization. The optimized designs are then evaluated with mission-level performance and fuel-burn analysis.

Implementation: [`Data-opt/Operation-aware`](Data-opt/Operation-aware/) and [`CFD-opt/Operation-aware`](CFD-opt/Operation-aware/).

### Integrated workflow

`operation data → clustering → multifidelity surrogate → weighted multipoint optimization → CFD validation → mission analysis → visualization`

The integration configuration belongs in [`Data-opt/Multifidelity_Operation-aware`](Data-opt/Multifidelity_Operation-aware/). It combines the two cases above for future end-to-end studies; it should not be confused with the standalone multifidelity or operation-aware research cases.

## Major work and architecture

| Research work / layer | Main responsibility | Repository location | Inputs → outputs |
| --- | --- | --- | --- |
| Multifidelity optimization | Generate multi-level CFD data, train SF/MF neural surrogates, and perform gradient-based aerodynamic optimization | `Data-opt/Multifidelity/` | CFD samples + geometry variables → aerodynamic surrogate + optimized wing |
| Operation-aware optimization | Process operational data, identify representative conditions, and formulate weighted multipoint design optimization | `Data-opt/Operation-aware/`; `CFD-opt/Operation-aware/` | flight-operation data → clusters, weights, and operation-aware design |
| CFD layer | Run FFD/mode-based CFD optimization, ADflow analysis, adjoint, MPhys, ADODG, BWB, and 2-D examples | `CFD-opt/` | geometry + operating condition → CFD forces and coefficients |
| Geometric parameterization | Maintain FFD definitions, mode-based geometry classes, compatibility variants, and reference inputs | `Geometric_parameterization/` | design variables → deformed geometry |
| Mission and performance layer | Evaluate optimized designs over representative flight missions and estimate fuel/performance impact | `Data-opt/Operation-aware/mission/` | aerodynamic model + mission segments → mission metrics |
| Visualization and assets | Provide Tecplot macros/layouts and track portable CRM inputs while keeping large assets external | `viz/`; `assets/`; `docs/` | CFD/optimization results → plots, layouts, and reproducible asset references |

## Repository map

- `CFD-opt/` — CFD-based optimization, analysis, validation, and benchmark workflows.
- `Data-opt/` — single-fidelity, multifidelity, operation-aware, and EGO data-driven workflows.
- `Geometric_parameterization/` — FFD and mode-based parameterization implementations and inputs.
- `src/cfd_design_opt/` — shared portable utilities, including external-asset resolution.
- `assets/` — manifests and small shared CRM inputs. Large meshes, datasets, models, and run outputs stay outside Git.
- `viz/` — editable Tecplot layouts, macros, styles, helper scripts, and documentation.

## Scope of the initial version

The repository is organized by technical method. Some research scripts still require replacement of hard-coded paths and MACH-Aero-version assumptions before they are portable entry points.

See [`docs/migration-plan.md`](docs/migration-plan.md) for the staged migration plan, [`docs/assets.md`](docs/assets.md) for setup and use, and [`assets/manifests/crm-v1.json`](assets/manifests/crm-v1.json) for the canonical CRM asset registry.

## Citation

For work based on this repository as a whole, please cite the PhD thesis. For work specifically using one of the two main research cases, please also cite the corresponding paper:

- **All repository projects:** [*Scalable Operation-aware Aerodynamic Design*](https://researchportal.hkust.edu.hk/en/studentTheses/scalable-operation-aware-aerodynamic-design/) ([Google Scholar](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=lbQ5y9RPZxkC&citation_for_view=lbQ5y9RPZxkC:WF5omc3nYNoC)).
- **Multifidelity case:** [*Generalizable Multifidelity Aerodynamic Wing Shape Design Optimization*](https://doi.org/10.2514/1.C038587) ([Google Scholar](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=lbQ5y9RPZxkC&citation_for_view=lbQ5y9RPZxkC:zYLM7Y9cAGgC)).
- **Operation-aware case:** [*Operation-Aware Aircraft Wing Design Using Cluster-Based Multipoint Aerodynamic Shape Optimization*](https://doi.org/10.2514/1.C038291) ([Google Scholar](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=lbQ5y9RPZxkC&citation_for_view=lbQ5y9RPZxkC:u5HHmVD_uO8C)).

### BibTeX

The following entries are ready to copy:

```bibtex
@phdthesis{yang2026scalable,
  author      = {Yang, Aobo},
  title       = {{Scalable Operation-aware Aerodynamic Design}},
  school      = {The Hong Kong University of Science and Technology},
  year        = {2026},
  type        = {Doctoral thesis},
  doi         = {10.14711/thesis-hdl171519}
}

@article{yang2026generalizable,
  author      = {Yang, Aobo and Li, Jichao and Liem, Rhea P.},
  title       = {{Generalizable Multifidelity Aerodynamic Wing Shape Design Optimization}},
  journal     = {Journal of Aircraft},
  year        = {2026},
  publisher   = {American Institute of Aeronautics and Astronautics},
  doi         = {10.2514/1.C038587}
}

@article{yang2025operationaware,
  author      = {Yang, Aobo and Lyu, Yuan and Li, Jichao and Liem, Rhea P.},
  title       = {{Operation-Aware Aircraft Wing Design Using Cluster-Based Multipoint Aerodynamic Shape Optimization}},
  journal     = {Journal of Aircraft},
  volume      = {62},
  number      = {6},
  pages       = {1531--1547},
  year        = {2025},
  publisher   = {American Institute of Aeronautics and Astronautics},
  doi         = {10.2514/1.C038291}
}
```
