# Generalizable Multi-Fidelity Design Optimization

## Overview
This repository compiles scripts, surrogate models, and training data for a research workflow that accelerates
aerodynamic shape optimization by combining single- and multi-fidelity neural surrogates. High-fidelity CFD data are
generated with ADflow across multiple meshes, and the
trained surrogates drive multi-point aerodynamic optimizations via pyOptSparse.

For details, please refer to paper:

```bibtex
@article{yang2026multifidelity,
  title     = {{Generalizable Multifidelity Aerodynamic Wing Shape Design Optimization}},
  author    = {Yang, Aobo and Li, Jichao and Liem, Rhea P},
  journal   = {Journal of Aircraft},
  year      = {2026},
  publisher = {American Institute of Aeronautics and Astronautics},
}

````

## Features
- ADflow-based generation of CFD training data with DVGeometry and IDWarp mesh warping.
- Training pipelines for both single-fidelity (SF) and multi-fidelity (MF) neural networks.
- Surrogate wrappers for prediction and sensitivity analysis
- Multi-point, multifidelity data-driven aerodynamic shape optimization developed based on MACH-Aero.
- Curated inputs (bounds, modal shapes, meshes) plus example datasets and pretrained `.h5` models for CL/CD/CM
predictions.

  ## Repository Structure
  ```
  .
  ├── NN_training/
  ├── adflow_create_training_data/
  ├── input/
  ├── models/
  ├── opt/
  ├── surrogate/
  └── training_data/
  ```

  | Folder | Description |
  | --- | --- |
  | `NN_training/` | TensorFlow training scripts for SF and MF surrogate models; outputs logs, plots, and `.h5`
  weights. |
  | `adflow_create_training_data/` | ADflow driver (`CFD_run_train.py`) and coefficient inputs used to generate CFD
  datasets on HPC systems. |
  | `input/` | Shared geometry and design-variable artifacts (bounds, modal bases, mesh files, node lists, twist
  ranges, CRM reference data). |
  | `models/` | Pretrained Keras models (`SF_models/` baseline surrogates, `MF_models/` low-to-high-fidelity
  correction networks). |
  | `opt/` | Surrogate-based aerodynamic optimization driver (`data_driven_mpts_ASO_main_9pts.py`). |
  | `surrogate/` | `AeroSurrogate` implementations for SF and MF surrogates, including finite-difference sensitivities
  for optimizers. |
  | `training_data/` | Example CFD datasets (`L3_training.dat`, `L2_training.txt`) used when training the neural
  networks. |

  ## Key Components

  ### Data Generation (`adflow_create_training_data/CFD_run_train.py`)
  - Uses ADflow, DVGeometry, IDWarp, and multiPointSparse to warp meshes, run RANS analyses, and record CL/CD/CM for
  each sample in `L2_train_coeff_input.dat`.
  - Designed for MPI-enabled HPC environments; outputs concatenated coefficient files (`Data_Gen_L2_validate.txt`).

  ### Neural-Network Training (`NN_training/`)
  - `NN_training_single_fidelity_data.py`: trains SF networks (e.g., lift-to-drag ratio predictors) from high-fidelity
  datasets such as `training_data/L3_training.dat`; produces TensorBoard logs and diagnostic plots.
  - `NN_training_multi_fidelity_data.py`: trains MF residual models by combining normalized low-fidelity inputs
  with baseline predictions from SF models, improving CL/CD/CM accuracy using limited higher-fidelity data. Outputs
  comparison CSVs, error summaries, and updated MF `.h5` weights.

  ### Surrogate APIs (`surrogate/SF_SUR.py`, `surrogate/MF_SUR.py`)
  - Load the pretrained Keras models, normalize inputs according to `input/bounds.txt`, evaluate CL/CD/CM, and provide
  finite-difference sensitivities with respect to angle of attack, twist, and shape modal coefficients.
  - MF version chains SF predictions with correction networks to map low-fidelity outputs to higher-fidelity
  estimates.

  ### Optimization (`opt/data_driven_mpts_ASO_main_9pts.py`)
  - Builds nine flow cases with prescribed Mach numbers, CL targets, and weighting coefficients.
  - Constructs `AeroSurrogate` instances for each case, registers them with multiPointSparse, and minimizes weighted
  drag via pyOptSparse (SLSQP/SNOPT/IPOPT).
  - Requires auxiliary modules (`DVGeometry_FFD_MODE`, `SUR`) and ADflow-compatible installations.

  ## Usage

  1. **Prepare Inputs**
     Populate the `input/` directory with meshes (`rot.xyz`, CGNS files), modal bases (`modes.dat`), bounds, and
  supporting metadata. Adjust hard-coded absolute paths inside scripts to point to your environment.

  2. **Generate CFD Data (optional refresh)**
     ```
     mpirun -np <procs> python adflow_create_training_data/CFD_run_train.py --output l2_runs --task analysis
     ```
     Produces updated coefficient files for downstream training.

  3. **Train Surrogate Models**
     - SF: `python NN_training/NN_training_single_fidelity_data.py` (configure dataset path near lines 104–118).
     - MF: `python NN_training/NN_training_multi_fidelity_data.py` (uses `training_data/L2_training.txt`, baseline SF
  models, writes MF `.h5` files and diagnostics).

  4. **Run Surrogate-Based Optimization**
     ```
     mpirun -np <procs> python opt/data_driven_mpts_ASO_main_9pts.py --opt SNOPT --output history_MF
     ```
     Generates optimizer logs, history files, and `optmum_HF.dat` containing the best design vector.

  ## Data & Models
  - `training_data/L3_training.dat` and `training_data/L2_training.txt` contain aggregated design variables plus CL/
  CD/CM responses (60 + 3 columns inferred from scripts).
  - `models/SF_models/*.h5` supply baseline CL/CD/CM predictions; `models/MF_models/*.h5` provide the low-to-high-
  fidelity correction networks.
  - `surrogate` scripts expect these files in their current relative locations; update paths if relocating or
  regenerating models.

  ## Notes
  - Many scripts currently reference `/home/aobo/MACH-Aero/...`; update these paths to relative locations or
  configurable arguments before public release.
  - CFD scripts assume access to HPC resources with ADflow installations; surrogate training can run locally but
  benefits from GPU acceleration.
  - Ensure required external modules (`DVGeometry_FFD_MODE`, `SUR`) are available in the repository or documented
  for users.
