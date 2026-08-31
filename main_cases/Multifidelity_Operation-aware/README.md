# Multifidelity Operation-aware CRM wing design optimization

This is the repository's flagship workflow. It will optimize a CRM wing at representative operating conditions derived from operational data, use a multifidelity aerodynamic surrogate during optimization, validate selected designs with CFD, and assess them at mission level.

The directories map directly to the pipeline stages:

- `data_preparation/`: operation-data ingestion and cleaning.
- `clustering/`: representative conditions and weights.
- `multifidelity_surrogate/`: SF/MF model configuration, training, and inference.
- `optimization/`: weighted multipoint design optimization.
- `mission_analysis/`: performance and fuel assessment.
- `configs/`: portable case configurations; no machine-specific absolute paths.

Implementation begins by porting the established operation-aware and multifidelity scripts into these stages.
