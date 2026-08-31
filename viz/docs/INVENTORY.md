# Inventory

Created on 2026-05-28.

## Repository Content

The Git-tracked side contains only lightweight editable files:

- `.lay`: Tecplot layout files
- `.mcr`: Tecplot macro files
- `.sty`: Tecplot style files
- `.py`: helper scripts
- `.md`: documentation
- `.txt`: small notes/configuration files

Large rendered media, CFD data, and compressed archives are excluded by `.gitignore`.

## Local Asset Layout

Large files are organized under `large_assets/`:

- `large_assets/archives/plot_wing_Tecplot.zip` - original compressed archive.
- `large_assets/archives/plot_wing_Tecplot/` - full extracted archive, about 16 GB.
- `large_assets/data/wing_compare/` - CGNS and Tecplot data copied from `wing_compare`.
- `large_assets/data/selected_examples/` - selected data examples moved out of the code tree.
- `large_assets/outputs/images/` - rendered PNG outputs.
- `large_assets/outputs/pdfs/` - rendered PDF outputs.
- `large_assets/outputs/frame_sequences/` - reserved for generated movie frames.
- `large_assets/source_snapshots/wing_compare/` - complete original wing comparison snapshot.

## Notes

Some Tecplot layouts may use original relative paths. Keep `large_assets/` next to this repository when using layouts interactively in Tecplot.
