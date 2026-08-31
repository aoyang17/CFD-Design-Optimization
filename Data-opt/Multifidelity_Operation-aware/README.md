# Multifidelity Operation-aware

This is the integration configuration for the repository's two main research directions:

1. `../Multifidelity/` supplies aerodynamic data generation, SF/MF training, surrogate inference, and surrogate optimization.
2. `../Operation-aware/` supplies operational-data clustering, representative-condition weighting, and mission evaluation.
3. `../../CFD-opt/Operation-aware/` supplies CFD optimization and validation.

The `configs/` directory uses asset IDs from `assets/manifests/` and must not contain machine-specific paths.
