import os
import argparse
import numpy as np
from mpi4py import MPI

import openmdao.api as om
from mphys.multipoint import Multipoint
from multipoint import multiPointSparse
from mphys.scenario_aerodynamic import ScenarioAerodynamic
from adflow.mphys import ADflowBuilder
from baseclasses import AeroProblem
from pygeo.mphys import OM_DVGEOCOMP

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="output_L3")
parser.add_argument("--gridFile", type=str, default="./input/L3_peter_rotat_mirror_bc.cgns")
parser.add_argument("--FFDFile", type=str, default="./input/rot.xyz")
parser.add_argument("--task", default="opt")
parser.add_argument("--level", type=str, default="L1")
args = parser.parse_args()

MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet("cruise", nMembers=1, memberSizes=MPI.COMM_WORLD.size)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()
 
if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)
        
class Top(Multipoint):
    def setup(self):

        ################################################################################
        # ADflow options
        ################################################################################
        aero_options = {
            # I/O Parameters
            "gridFile": args.gridFile,
            "outputDirectory": args.output,
            # Common Parameters
            'monitorVariables':["resrho", "cl", "cd", "cmz"],
            'volumeVariables':['cp','mach'],
            'isoSurface':{'shock':1.0},     
            # Physics Parameters
            'equationType':'RANS',#args.mode,
            'smoother':'DADI',#gridops[args.level]['s'],
            'frozenturbulence':False,
            # Solver Parameters
            'CFL':1.0,
            'CFLCoarse':1.0,
            'MGCycle':'sg',
            'MGStartLevel':-1,
            'nCyclesCoarse':5000,
            'nCycles':10000,
            'nsubiterturb':7,
            'useNKSolver':True,
            'useANKSolver':True,
            'nkswitchtol':1e-7,
            'rkreset': True,
            'nrkreset': 200,
            'liftIndex': 2,
            'writeVolumeSolution':True,
            'writeSurfaceSolution':True,
            #'ANKmaxIter' : 40,
            #'ANKsecondordswitchtol' : 1e-16,
            #'ANKcoupledswitchtol' : 1e-12,
            'useanksolver' : True,
            #'nsubiterturb' : 10,
            'useNKSolver':True,
            'ankstepfactor' : 0.5,
            # 'ankstepinit' : 0.1,
            # 'ankstepexponent' : 0.5,
            'ANKCFLExponent' : 0.5,
            'anklinearsolvetol' : 0.05,

            # Convergence Parameters
            'L2Convergence':1e-10,
            'adjointL2Convergence':1e-12,
            'ADPC':True,
            'adjointMaxIter': 500,
            'adjointSubspaceSize':150,
            'ILUFill':2,
            'ASMOverlap':1,
            'outerPreconIts':3,
        }

        adflow_builder = ADflowBuilder(aero_options, scenario="aerodynamic")
        adflow_builder.initialize(self.comm)

        ################################################################################
        # MPHYS setup
        ################################################################################

        # ivc to keep the top level DVs
        self.add_subsystem("dvs", om.IndepVarComp(), promotes=["*"])

        # create the mesh component
        self.add_subsystem("mesh", adflow_builder.get_mesh_coordinate_subsystem())

        # add the geometry component, we dont need a builder because we do it here.
        self.add_subsystem("geometry", OM_DVGEOCOMP(ffd_file=args.FFDFile))

        self.mphys_add_scenario("cruise", ScenarioAerodynamic(aero_builder=adflow_builder))

        self.connect("mesh.x_aero0", "geometry.x_aero_in")
        self.connect("geometry.x_aero0", "cruise.x_aero")

    def configure(self):
        # create the aero problems for both analysis point.
        # this is custom to the ADflow based approach we chose here.
        # any solver can have their own custom approach here, and we don't
        # need to use a common API. AND, if we wanted to define a common API,
        # it can easily be defined on the mp group, or the aero group.
        aoa = 2.3
        ap0 = AeroProblem(
            name="fc" ,
            alpha=aoa,
            mach=0.85,
            altitude=11740,
            # reynolds=5e6,
            # reynoldsLength=1.0,
            # T=326.45,
            areaRef= 3.407014,
            xRef=1.20777,
            yRef=0.0,
            zRef=.007669,
            chordRef=1.0,
            evalFuncs=["cl", "cd", "cmz"],
        )
        ap0.addDV("alpha", value=aoa, name="aoa", units="deg")

        self.cruise.coupling.mphys_set_ap(ap0)
        self.cruise.aero_post.mphys_set_ap(ap0)

        # create geometric DV setup
        points = self.mesh.mphys_get_surface_mesh()

        # add pointset
        self.geometry.nom_add_discipline_coords("aero", points)

        # add these points to the geometry object
        # self.geo.nom_add_point_dict(points)
        # create constraint DV setup
        tri_points = self.mesh.mphys_get_triangulated_surface()
        self.geometry.nom_setConstraintSurface(tri_points)

        # geometry setup

        # Create reference axis
        nRefAxPts = self.geometry.nom_addRefAxis(name="wing", xFraction=0.25, alignIndex="k")
        nTwist = nRefAxPts - 1

        # Set up global design variables
        def twist(val, geo):
            for i in range(1, nRefAxPts):
                geo.rot_z["wing"].coef[i] = val[i - 1]

        self.geometry.nom_addGeoDVGlobal(dvName="twist", value=np.array([0] * nTwist), func=twist)
        nLocal = self.geometry.nom_addGeoDVLocal(dvName="thickness", axis="y")

        LE_pt = np.array([.01, 0.0,0.01])
        break_pt = np.array([.8477, 0.0, 1.11853])
        tip_pt = np.array([2.85680, 0.0, 3.75816])
        root_chord = 1.689
        break_chord = 1.03628
        tip_chord = .3902497

        x_le = np.array([[LE_pt[0] + 0.01*root_chord, LE_pt[1], LE_pt[2]],
                            [break_pt[0] + 0.01*break_chord, break_pt[1], break_pt[2]],
                            [tip_pt[0] + 0.01*tip_chord, tip_pt[1], tip_pt[2]]])

        x_te = np.array([[LE_pt[0] + 0.99*root_chord, LE_pt[1], LE_pt[2]],
                            [break_pt[0] + 0.99*break_chord, break_pt[1], break_pt[2]],
                            [tip_pt[0] + 0.99*tip_chord, tip_pt[1], tip_pt[2]]])
        
        self.geometry.nom_addThicknessConstraints2D("thickcon", x_le, x_te, nSpan=25, nChord=30)
        self.geometry.nom_addVolumeConstraint("volcon", x_le, x_te, nSpan=25, nChord=30)
        self.geometry.nom_add_LETEConstraint("lecon", 0, "iLow")
        self.geometry.nom_add_LETEConstraint("tecon", 0, "iHigh")
        # add dvs to ivc and connect
        self.dvs.add_output("aoa", val=aoa, units="deg")
        self.dvs.add_output("local", val=np.array([0] * nLocal))
        self.dvs.add_output("twist", val=np.array([0] * nTwist))

        self.connect("aoa", ["cruise.coupling.aoa", "cruise.aero_post.aoa"])
        self.connect("local", "geometry.thickness")
        self.connect("twist", "geometry.twist")

        # define the design variables
        self.add_design_var("aoa", lower=0.0, upper=10.0, scaler=0.1, units="deg")
        self.add_design_var("local", lower=-0.5, upper=0.5, scaler=0.01)
        self.add_design_var("twist", lower=-10.0, upper=10.0, scaler=0.01)

        # add constraints and the objective
        self.add_constraint("cruise.aero_post.cl", equals=0.5, scaler=10.0)
        self.add_constraint("geometry.thickcon", lower=1.0, scaler=1.0)
        self.add_constraint("geometry.volcon", lower=1.0, scaler=1.0)
        self.add_constraint("geometry.tecon", equals=0.0, scaler=1.0, linear=True)
        self.add_constraint("geometry.lecon", equals=0.0, scaler=1.0, linear=True)
        self.add_objective("cruise.aero_post.cd", scaler=100.0)


################################################################################
# OpenMDAO setup
################################################################################
prob = om.Problem()
prob.model = Top()

prob.driver = om.pyOptSparseDriver()
prob.driver.options["optimizer"] = "IPOPT"
# prob.driver.opt_settings = {
#     "Major feasibility tolerance": 1e-4,  # 1e-4,
#     "Major optimality tolerance": 1e-3,  # 1e-8,
#     "Verify level": 0,
#     "Major iterations limit": 200,
#     "Minor iterations limit": 1000000,
#     "Iterations limit": 1500000,
#     "Nonderivative linesearch": None,
#     "Major step limit": 0.01,
#     "Function precision": 1.0e-8,
#     # 'Difference interval':1.0e-6,
#     # 'Hessian full memory':None,
#     "Hessian frequency": 200,
#     # 'Linesearch tolerance':0.99,
#     "Print file": "SNOPT_print.out",
#     "Summary file": "SNOPT_summary.out",
#     "Problem Type": "Minimize",
#     # 'New superbasics limit':500,
#     "Penalty parameter": 1.0,
# }

prob.driver.opt_settings = {
    "limited_memory_max_history": 1000,
    "print_level": 5,
    "tol": 1e-6,
    "acceptable_tol": 1e-5,
    "max_iter": 300,
    "start_with_resto": "yes",
}

# prob.driver.options['debug_print'] = ['totals', 'desvars']

prob.setup(mode="rev")
om.n2(prob, show_browser=False, outfile="mphys_aero.html")

if args.task == "run":
    prob.run_model()
    # prob.model.list_outputs(print_arrays=True)
    # prob.check_partials(compact_print=True, includes='*geometry*')
    # prob.check_totals(compact_print=True)
elif args.task == "opt":
    prob.run_driver()

prob.model.list_inputs(units=True)
prob.model.list_outputs(units=True)

if prob.model.comm.rank == 0:
    print("Scenario 0")
    print("cl =", prob["cruise.aero_post.cl"])
    print("cd =", prob["cruise.aero_post.cd"])