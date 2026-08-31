#!MC 1410
$!VarSet |MFBD| = 'C:\Users\aobo\Desktop\plot_wing\tecView\circle_2_airfoil_surf\noCNN'
$!VarSet |NumLoop| = 20
$!Loop |NumLoop|
$!Varset |num| = (|Loop|)

$!Varset |num| = (|Loop|)
$!PICK ADDATPOSITION
  X = 1.00749464668
  Y = 1.0465738758
  CONSIDERSTYLE = YES
$!FRAMECONTROL ACTIVATEBYNUMBER
  FRAME = 1
$!FRAMELAYOUT WIDTH = 8
$!FRAMELAYOUT HEIGHT = 6
$!FRAMELAYOUT SHOWBORDER = NO
$!READDATASET  '"STANDARDSYNTAX" "1.0" "FILELIST_CGNSFILES" "1" "C:\Users\aobo\Desktop\plot_wing\tecView\circle_2_airfoil_surf\surface\circle_2d5_iter_|num|_000_surf.cgns" "LoadBCs" "Yes" "AssignStrandIDs" "Yes" "LoaderVersion" "V3" "CgnsLibraryVersion" "3.1.4"'
  DATASETREADER = 'CGNS Loader'
  READDATAOPTION = NEW
  RESETSTYLE = YES
  ASSIGNSTRANDIDS = NO
  INITIALPLOTTYPE = CARTESIAN3D
  INITIALPLOTFIRSTZONEONLY = NO
  ADDZONESTOEXISTINGSTRANDS = NO
$!ReadStyleSheet  "C:\Users\aobo\Desktop\plot_wing\tecView\circle_2_airfoil_surf\circle_airfoil_dmm.sty"
  IncludePlotStyle = Yes
  IncludeText = Yes
  IncludeGeom = Yes
  IncludeAuxData = Yes
  IncludeStreamPositions = Yes
  IncludeContourLevels = Yes
  Merge = No
  IncludeFrameSizeAndPosition = No
$!PRINTSETUP PALETTE = COLOR
$!EXPORTSETUP EXPORTREGION = ALLFRAMES
$!EXPORTSETUP IMAGEWIDTH = 3000
$!EXPORTSETUP EXPORTFNAME = 'C:\Users\aobo\Desktop\plot_wing\tecView\circle_2_airfoil_surf\output_dmm\|num|.png'
$!EXPORT 
  EXPORTREGION = ALLFRAMES
$!EndLoop
$!RemoveVar |MFBD|
