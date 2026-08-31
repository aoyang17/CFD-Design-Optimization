# Tecplot Wing Visualization Templates

This repository collects reusable Tecplot templates for aerodynamic wing visualization. It organizes layout files, Tecplot macros, style presets, and small helper scripts that were originally spread across:

- `plot_wing_Tecplot.zip`
- `wing_compare`

The repository is intended to track the lightweight, editable "code side" only. CFD data, full archives, rendered images/PDFs, and movie frame sequences are kept locally under `large_assets/` and are excluded from Git.

## What Is Included

- `layouts/` - Tecplot `.lay` layout templates.
- `macros/` - Tecplot `.mcr` automation macros.
- `styles/` - Tecplot `.sty` style presets for CRM, BWB, airfoil, and wing comparison views.
- `scripts/` - Python helper scripts for combining or post-processing generated figures.
- `source_snapshots/plot_wing_Tecplot_selected/` - selected editable files extracted from the original zip, excluding data and rendered media.
- `docs/` - inventory and local asset notes.

## What Is Not Tracked

The following local-only content is organized in `large_assets/` and ignored by Git:

- `large_assets/archives/` - original zip and full extracted source archive.
- `large_assets/data/` - CGNS and Tecplot data files.
- `large_assets/outputs/` - PNG/PDF outputs and generated frame sequences.
- `large_assets/source_snapshots/wing_compare/` - complete original `wing_compare` snapshot with data and media.

## Suggested Entry Points

- Wing comparison layouts:
  - `layouts/wing_compare/Wing_compare_main.lay`
  - `layouts/wing_compare/wing_compare.lay`
  - `layouts/wing_compare/tecView/compare.lay`
- CRM/BWB/airfoil layouts:
  - `layouts/crm_bwb_airfoil/show.lay`
  - `layouts/crm_bwb_airfoil/tecView/compare.lay`
- Common macro/style directories:
  - `macros/crm_bwb_airfoil/tecView/`
  - `styles/crm_bwb_airfoil/tecView/`

## Restoring Local Assets

Layouts may reference relative paths from their original directories. If a layout cannot find data, use the matching files under `large_assets/`:

- Full extracted archive: `large_assets/archives/plot_wing_Tecplot/`
- Wing comparison data: `large_assets/data/wing_compare/`
- Full wing comparison snapshot: `large_assets/source_snapshots/wing_compare/`

These assets are intentionally excluded from GitHub to keep the private repository lightweight.
