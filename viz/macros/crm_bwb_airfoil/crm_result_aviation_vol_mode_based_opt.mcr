#!MC 1410
$!VarSet |MFBD| = 'C:\Users\aobo\Desktop\plot_wing\CRM_L3_1_pt_mode_based'
$!VarSet |NumLoop| = 500
$!Loop |NumLoop|
$!Varset |num| = (|Loop|)

$!Varset |num| = (|Loop|+9)
$!PICK ADDATPOSITION
  X = 1.00749464668
  Y = 1.0465738758
  CONSIDERSTYLE = YES
$!FRAMECONTROL ACTIVATEBYNUMBER
  FRAME = 1
$!FRAMELAYOUT WIDTH = 9
$!FRAMELAYOUT HEIGHT = 6
$!FRAMELAYOUT SHOWBORDER = NO

$!ReadDataSet  '"STANDARDSYNTAX" "1.0" "FILELIST_CGNSFILES" "1" "C:/Users/aobo/Desktop/plot_wing/CRM_L3_1_pt_mode_based/ADODG40_0|num|_surf.cgns" "LoadBCs" "Yes" "AssignStrandIDs" "Yes" "UniformGridStructure" "Yes" "LoaderVersion" "V3" "CgnsLibraryVersion" "4.1.2"'
  DataSetReader = 'CGNS Loader'
  ReadDataOption = New
  ResetStyle = Yes
  AssignStrandIDs = Yes
  InitialPlotType = Cartesian3D
  InitialPlotFirstZoneOnly = No
  AddZonesToExistingStrands = No
  VarLoadMode = ByName

$!ReadStyleSheet  "C:\Users\aobo\Desktop\plot_wing\crm_mirror_visualize.sty"
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
$!EXPORTSETUP EXPORTFNAME = 'C:\Users\aobo\Desktop\plot_wing\Figure_crm_L3_mode_opt\|num|.png'
$!EXPORT 
  EXPORTREGION = ALLFRAMES
$!EndLoop
$!RemoveVar |MFBD|
