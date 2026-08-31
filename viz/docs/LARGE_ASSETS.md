# Large Assets

The data and rendered media for these templates are kept locally and are not uploaded to GitHub.

## Local Directories

- `large_assets/archives/` contains original archives and the full extraction of `plot_wing_Tecplot`.
- `large_assets/data/` contains CFD and Tecplot data files such as `.cgns` and `.dat`.
- `large_assets/outputs/` contains rendered images, PDFs, and frame sequence outputs.
- `large_assets/source_snapshots/` contains full source snapshots that include data and media.

## Git Policy

`.gitignore` excludes `large_assets/`, CFD data formats, rendered media, and archives. Commit only source templates, macros, styles, scripts, and documentation unless a specific small fixture is intentionally added later.
