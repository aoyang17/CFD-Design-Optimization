# Operation-aware Aircraft Wing Design Optimization

This repository contains the code base for the **operation-aware aircraft design optimization** project.

It is associated with the following paper. If you use this repository in your research, please cite:

```bibtex
@article{Yang.JoA.2025,
  title   = {{Operation-Aware Aircraft Wing Design Using Cluster-Based Multipoint Aerodynamic Shape Optimization}},
  author  = {Yang, Aobo and Lyu, Yuan and Li, Jichao and Liem, Rhea P.},
  journal = {Journal of Aircraft},
  volume  = {62},
  number  = {6},
  pages   = {1531--1547},
  month   = nov,
  year    = {2025},
  doi     = {10.2514/1.C038291}
}
````

## Repository Overview

The repository is organized into the following folders:

### `cfd_analyze`

This folder contains scripts for CFD-based analysis of wing volume meshes and warped volume meshes using **ADflow**.

### `cfd_opt`

This folder contains the main sample codes for **clustering-based operation-aware design optimization**.

Different cases may require adjusting the selected operating points and their corresponding weights.

### `clustering`

This folder contains scripts for data engineering and clustering analysis used in the operation-aware design framework.

### `mission`

This folder contains the mission analysis code. For the related methodology, please refer to the following paper:

```bibtex
@article{lyu2020flight,
  author    = {Lyu, Y. and Liem, R. P.},
  title     = {Flight Performance Analysis with Data-Driven Mission Parameterization: Mapping Flight Operational Data to Aircraft Performance Analysis},
  journal   = {Transportation Engineering},
  volume    = {2},
  pages     = {100035},
  year      = {2020},
  month     = {December},
  doi       = {10.1016/j.treng.2020.100035},
  publisher = {Elsevier}
}
```

### `viz`

This folder contains scripts for visualization and figure generation.

## Contact

If you have any questions, please contact:

**Aobo Yang**
`cubeyang17@gmail.com`
