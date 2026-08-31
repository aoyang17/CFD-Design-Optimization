#!/bin/bash
#SBATCH -p amd_256
#SBATCH -N 1
#SBATCH -n 64
source /public3/soft/module/module.sh
module load mpi/intel/17.0.5-cjj-public3 hdf5/1.8.13-parallel-icc17-public3
source ~/.bashrc
source activate new-env
export PETSC_DIR=/public3/home/sc71052/repos/petsc-3.14.3
export PETSC_ARCH=real-debug
export CGNS_HOME=/public3/home/sc71052/repos/new/CGNS-4.1.2
export PATH=/public3/home/sc71052/repos/new/CGNS-4.1.2/bin:$PATH
export LD_LIBRARY_PATH=/public3/home/sc71052/repos/new/CGNS-4.1.2/src/install/lib:$LD_LIBRARY_PATH

# git clone https://github.com/OpenMDAO/build_pyoptsparse.git
# python -m pip install ./build_pyoptsparse-master
# build_pyoptsparse
# mpirun -np 64 python mode_based_opt.py
pip install smt
mpirun -np 64 python residualTimeJFK.py

