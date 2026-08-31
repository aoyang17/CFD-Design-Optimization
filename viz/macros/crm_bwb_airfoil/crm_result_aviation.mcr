#!MC 1410
$!VarSet |MFBD| = 'C:\Users\aobo\Desktop\plot_wing\volume\volume'
$!VarSet |NumLoop| = 300
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
$!FRAMELAYOUT HEIGHT = 9
$!FRAMELAYOUT SHOWBORDER = NO

$!READDATASET  '"STANDARDSYNTAX" "1.0" "FILELIST_CGNSFILES" "1" "C:\Users\aobo\Desktop\plot_wing\volume\volume\ADODG4_iter_|num|_000_vol.cgns" "LoadBCs" "Yes" "AssignStrandIDs" "Yes" "LoaderVersion" "V3" "CgnsLibraryVersion" "3.1.4"'
  DATASETREADER = 'CGNS Loader'
  READDATAOPTION = NEW
  RESETSTYLE = YES
  ASSIGNSTRANDIDS = NO
  INITIALPLOTTYPE = CARTESIAN3D
  INITIALPLOTFIRSTZONEONLY = NO
  ADDZONESTOEXISTINGSTRANDS = NO

$!ReadStyleSheet  "C:\Users\aobo\Desktop\plot_wing\CRM_visualize.sty"
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
$!EXPORTSETUP EXPORTFNAME = 'C:\Users\aobo\Desktop\plot_wing\CRM_visualization_output_vol\|num|.png'
$!EXPORT 
  EXPORTREGION = ALLFRAMES
$!EndLoop
$!RemoveVar |MFBD|
