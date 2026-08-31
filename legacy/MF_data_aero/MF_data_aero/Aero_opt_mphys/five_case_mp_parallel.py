import ast
import numpy as np
from mpi4py import MPI
import os

import openmdao.api as om
from mphys.multipoint import MultipointParallel
from multipoint import multiPointSparse
from mphys.solver_builders.mphys_adflow import ADflowBuilder
from baseclasses import AeroProblem
from mphys.scenario_aerodynamic import ScenarioAerodynamic
from mphys.solver_builders.mphys_dvgeo import OM_DVGEOCOMP
import numpy as np
from mpi4py import MPI

import argparse

baseDir = os.path.dirname(os.path.abspath(__file__))

class ParallelCruises(MultipointParallel):
    def setup(self):

        ################################################################################
        # ADflow options
        ################################################################################
        aero_options = {
            # I/O Parameters
            # "gridFile": "wing_vol_coarse.cgns",
            "gridFile": os.path.join(baseDir, "/home/aobo/Documents/aso_om/ADODG4_Multiblock_Structured_Mesh.cgns"),
            "outputDirectory": os.path.join(baseDir, "/home/aobo/Documents/aso_om/output_mp_files/"),
            "monitorvariables": ["resrho", "resturb", "cl", "cd"],
            #lift direction
            "liftIndex":3,
            # "useZipperMesh":True,
            # Physics Parameters
            "equationType": "RANS",
            # Solver Parameters
            "smoother": "Runge-Kutta",
            "CFL":1.7,
            "CFLCoarse":1.0,
            "MGCycle": "sg",
            "MGStartLevel":-1,
            'nCyclesCoarse':250,
            'nCycles':100000,   
            'nsubiterturb':5,
            'useblockettes':False, 
            'useNKsolver':True,
            'useANKsolver':True,

            # "infchangecorrection": True,

            'usematrixfreedrdw':True,
            # nk
            'nkadpc':True,
            'nkswitchtol':1.0e-4,
            'liftIndex': 3,

            # Convergence Parameters
            'L2Convergence':1e-12,
            'L2ConvergenceCoarse':1e-2,

            # Adjoint Parameters
            'adjointL2Convergence':1e-12,
            'ADPC':True,
            'adjointMaxIter': 1500,
            'adjointSubspaceSize':150,
            'ILUFill':2,
            'ASMOverlap':2,
            'outerPreconIts':3,
        }

        adflow_builder = ADflowBuilder(aero_options, scenario="aerodynamic")
        adflow_builder.initialize(self.comm)

        self.mphys_add_scenario(
            "cruise0",
            ScenarioAerodynamic(aero_builder=adflow_builder, in_MultipointParallel=True),
        )

        self.mphys_add_scenario(
            "cruise1",
            ScenarioAerodynamic(aero_builder=adflow_builder, in_MultipointParallel=True),
        )

        self.mphys_add_scenario(
            "cruise2",
            ScenarioAerodynamic(aero_builder=adflow_builder, in_MultipointParallel=True),
        )

        self.mphys_add_scenario(
            "cruise3",
            ScenarioAerodynamic(aero_builder=adflow_builder, in_MultipointParallel=True),
        )

        self.mphys_add_scenario(
            "cruise4",
            ScenarioAerodynamic(aero_builder=adflow_builder, in_MultipointParallel=True),
        )


class Top(om.Group):
    def setup(self):

        ################################################################################
        # mphys setup
        ################################################################################
        self.add_subsystem("dvs", om.IndepVarComp(), promotes=["*"])
        self.add_subsystem("mp", ParallelCruises())
        self.add_subsystem("mesh", adflow_builder.get_mesh_coordinate_subsystem())
        self.add_subsystem("geometry", OM_DVGEOCOMP(ffd_file="/home/aobo/Documents/aso_om/ADODG4_FFD.xyz"))
        self.add_subsystem("drag", om.ExecComp(
            "cd_out= 0.475 * cd0 + 0.166 * cd1 + 0.356 * cd2 + 0.104 * cd3 + 0.230 * cd4 "))

    def configure(self):
        # create the aero problems for both analysis point.
        # this is custom to the ADflow based approach we chose here.
        # any solver can have their own custom approach here, and we don't
        # need to use a common API. AND, if we wanted to define a common API,
        # it can easily be defined on the mp group, or the aero group.
        nflowcase = 5
        aoa = 2.1789
        alpha = [2.17, 2.2, 2.3, 2.5, 3]
        alt = 10000
        mach = [0.85, 0.84, 0.85, 0.86, 0.85]
        w = [0.144, 0.166, 0.356, 0.104, 0.230]
        cl = [0.475, 0.500, 0.500, 0.5000, 0.525]

        ap0 = AeroProblem(
            name="ap0", mach=0.8, altitude=10000, alpha=aoa, areaRef=45.5, chordRef=3.25, evalFuncs=["cl", "cd"]
        )
        ap0.addDV("alpha", value=aoa, name="aoa", units="deg")

        ap1 = AeroProblem(
            name="ap1", mach=0.7, altitude=10000, alpha=1.5, areaRef=45.5, chordRef=3.25, evalFuncs=["cl", "cd"]
        )
        ap1.addDV("alpha", value=aoa, name="aoa", units="deg")

        ap2 = AeroProblem(name="ap2", alpha=aoa, mach=mach[2], altitude=alt, reynolds=5e6, \
                reynoldsLength=1.0, T=326.45, areaRef= 3.407014, chordRef=1.0, \
                xRef=1.20777, yRef=0, zRef=.007669, evalFuncs=["cl", "cd"])        
        ap2.addDV("alpha", value=alpha[2], name="aoa2", units="deg")

        ap3 = AeroProblem(name="ap3", alpha=aoa, mach=mach[3], altitude=alt, reynolds=5e6, \
                reynoldsLength=1.0, T=326.45, areaRef= 3.407014, chordRef=1.0, \
                xRef=1.20777, yRef=0, zRef=.007669, evalFuncs=["cl", "cd"])        
        ap3.addDV("alpha", value=alpha[3], name="aoa3", units="deg")

        ap4 = AeroProblem(name="ap4", alpha=aoa, mach=mach[4], altitude=alt, reynolds=5e6, \
                reynoldsLength=1.0, T=326.45, areaRef= 3.407014, chordRef=1.0, \
                xRef=1.20777, yRef=0, zRef=.007669, evalFuncs=["cl", "cd"])  
        ap4.addDV("alpha", value=alpha[4], name="aoa4", units="deg")

        # here we set the aero problems for every cruise case we have.
        # this can also be called set_flow_conditions, we don't need to create and pass an AP,
        # just flow conditions is probably a better general API
        # this call automatically adds the DVs for the respective scenario
        try:
            self.mp.cruise0.coupling.mphys_set_ap(ap0)
            self.mp.cruise0.aero_post.mphys_set_ap(ap0)
        except AttributeError:
            pass

        try:
            self.mp.cruise1.coupling.mphys_set_ap(ap1)
            self.mp.cruise1.aero_post.mphys_set_ap(ap1)
        except AttributeError:
            pass

        try:
            self.mp.cruise1.coupling.mphys_set_ap(ap2)
            self.mp.cruise1.aero_post.mphys_set_ap(ap2)
        except AttributeError:
            pass

        try:
            self.mp.cruise1.coupling.mphys_set_ap(ap3)
            self.mp.cruise1.aero_post.mphys_set_ap(ap3)
        except AttributeError:
            pass

        try:
            self.mp.cruise1.coupling.mphys_set_ap(ap4)
            self.mp.cruise1.aero_post.mphys_set_ap(ap4)
        except AttributeError:
            pass

        points = self.mesh.mphys_get_surface_mesh()
        self.geometry.nom_add_discipline_coords("aero", points)

        # add these points to the geometry object
        # self.geo.nom_add_point_dict(points)
        # create constraint DV setup
        tri_points = self.mesh.mphys_get_triangulated_surface()
        self.geometry.nom_setConstraintSurface(tri_points)

        # geometry setup

        # Create reference axis
        tri_points = self.mesh.mphys_get_triangulated_surface()
        self.geometry.nom_setConstraintSurface(tri_points)

        nRefAxPts = self.geometry.nom_addRefAxis(name="wing", xFraction=0.25, alignIndex="j")
        nTwist = nRefAxPts - 1  

        def twist(val, geo):
            for i in range(1, nTwist):
                geo.rot_y["wing"].coef[i] = val[i - 1]

        self.geometry.nom_addGeoDVGlobal(dvName="twist", value=np.array([0] * nTwist), func=twist)

        # add dvs to ivc and connect
        self.dvs.add_output("aoa0", val=aoa, units="deg")
        self.dvs.add_output("aoa1", val=aoa, units="deg")
        self.dvs.add_output("aoa2", val=aoa, units="deg")
        self.dvs.add_output("aoa3", val=aoa, units="deg")
        self.dvs.add_output("aoa4", val=aoa, units="deg")

        self.dvs.add_output("twist", val=np.array([0] * nTwist))

        # TODO this is working but not the correct way to do it. the sensitivities are also wrong now.
        self.connect("aoa0", ["mp.cruise0.coupling.aoa", "mp.cruise0.aero_post.aoa"], src_indices=[0])
        self.connect("aoa1", ["mp.cruise1.coupling.aoa", "mp.cruise1.aero_post.aoa"], src_indices=[0])
        self.connect("aoa2", ["mp.cruise2.coupling.aoa", "mp.cruise2.aero_post.aoa"], src_indices=[0])
        self.connect("aoa3", ["mp.cruise3.coupling.aoa", "mp.cruise3.aero_post.aoa"], src_indices=[0])
        self.connect("aoa4", ["mp.cruise4.coupling.aoa", "mp.cruise4.aero_post.aoa"], src_indices=[0])


        self.connect("twist", "geometry.twist")

        # define the design variables
        self.add_design_var("aoa0", lower=0.0, upper=10.0, scaler=1.0, units="deg")
        self.add_design_var("aoa1", lower=0.0, upper=10.0, scaler=1.0, units="deg")
        self.add_design_var("aoa2", lower=0.0, upper=10.0, scaler=1.0, units="deg")
        self.add_design_var("aoa3", lower=0.0, upper=10.0, scaler=1.0, units="deg")
        self.add_design_var("aoa4", lower=0.0, upper=10.0, scaler=1.0, units="deg")

        self.add_design_var("twist", lower=-10.0, upper=10.0, scaler=1.0)

        # add constraints and the objective
        self.add_constraint("mp.cruise0.aero_post.cl", equals=cl[0], scaler=1.0)
        self.add_constraint("mp.cruise1.aero_post.cl", equals=cl[1], scaler=1.0)
        self.add_constraint("mp.cruise2.aero_post.cl", equals=cl[2], scaler=1.0)
        self.add_constraint("mp.cruise3.aero_post.cl", equals=cl[3], scaler=1.0)
        self.add_constraint("mp.cruise4.aero_post.cl", equals=cl[4], scaler=1.0)

        # connect the two drags to drag average
        self.connect("mp.cruise0.aero_post.cd", "drag.cd0")
        self.connect("mp.cruise1.aero_post.cd", "drag.cd1")
        self.connect("mp.cruise2.aero_post.cd", "drag.cd2")
        self.connect("mp.cruise3.aero_post.cd", "drag.cd3")
        self.connect("mp.cruise4.aero_post.cd", "drag.cd4")
        self.add_objective("drag.cd_out", scaler=1.0)



################################################################################
# OpenMDAO setup
################################################################################
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="output_mp_files")
parser.add_argument("--opt", type=str, default="SLSQP", choices=["IPOPT", "SLSQP", "SNOPT"])
parser.add_argument("--gridFile", type=str, default="ADODG4_Multiblock_Structured_Mesh.cgns")

parser.add_argument("--optOptions", type=ast.literal_eval, default={}, help="additional optimizer options to be added")
args = parser.parse_args() 

MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet("cruise", nMembers=1, memberSizes=MPI.COMM_WORLD.size)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()

if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)


prob = om.Problem()
prob.model = Top()

prob.driver = om.pyOptSparseDriver()
prob.driver.options["optimizer"] = "SLSQP"
prob.driver.opt_settings = {
        "ACC":1.0e-7,
        "MAXIT":50,
        "IFILE": os.path.join(baseDir, "SLSQP.out"),
}

# prob.driver.options['debug_print'] = ['totals', 'desvars']

prob.setup(mode="rev")
om.n2(prob, show_browser=False, outfile="aero_5pt_parallel.html")

# prob.run_model()
# prob.run_driver()
prob.run()


# TODO list i/o did not work for parallel multipoint
# prob.model.list_inputs(units=True)
# prob.model.list_outputs(units=True)

# prob.model.list_outputs()

cl0 = prob.get_val("cruise0.aero_post.cl", get_remote=True)
cd0 = prob.get_val("cruise0.aero_post.cd", get_remote=True)

cl1 = prob.get_val("cruise1.aero_post.cl", get_remote=True)
cd1 = prob.get_val("cruise1.aero_post.cd", get_remote=True)

cl2 = prob.get_val("cruise2.aero_post.cl", get_remote=True)
cd2 = prob.get_val("cruise2.aero_post.cd", get_remote=True)

cl3 = prob.get_val("cruise3.aero_post.cl", get_remote=True)
cd3 = prob.get_val("cruise3.aero_post.cd", get_remote=True)

cl4 = prob.get_val("cruise4.aero_post.cl", get_remote=True)
cd4 = prob.get_val("cruise4.aero_post.cd", get_remote=True)

cd = prob.get_val("drag.cd_out", get_remote=True)


if MPI.COMM_WORLD.rank == 0:
    print("Cruise 0")
    print("cl =", cl0)
    print("cd =", cd1)

    print("Cruise 1")
    print("cl =", cl1)
    print("cd =", cd1)

    print("Cruise 2")
    print("cl =", cl2)
    print("cd =", cd2)

    print("Cruise 3")
    print("cl =", cl3)
    print("cd =", cd3)

    print("Cruise 4")
    print("cl =", cl4)
    print("cd =", cd4)

    print("Cd_out")
    print("cd_out = ", cd)                  
