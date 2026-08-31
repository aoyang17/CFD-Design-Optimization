#!MC 1410
$!VarSet |MFBD| = 'C:\Users\aobo\Downloads\bwb_surfaces'
$!VarSet |NumLoop| = 1000
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
$!FRAMELAYOUT HEIGHT = 4.5
$!FRAMELAYOUT SHOWBORDER = NO

$!READDATASET  '"STANDARDSYNTAX" "1.0" "FILELIST_CGNSFILES" "1" "C:\Users\aobo\Downloads\bwb_surfaces\bwb_iter_|num|_000_surf.cgns" "LoadBCs" "Yes" "AssignStrandIDs" "Yes" "LoaderVersion" "V3" "CgnsLibraryVersion" "3.1.4"'
  DATASETREADER = 'CGNS Loader'
  READDATAOPTION = NEW
  RESETSTYLE = YES
  ASSIGNSTRANDIDS = NO
  INITIALPLOTTYPE = CARTESIAN3D
  INITIALPLOTFIRSTZONEONLY = NO
  ADDZONESTOEXISTINGSTRANDS = NO

$!ReadStyleSheet  "C:\Users\aobo\Desktop\plot_wing\bwb_result_aviation.sty"
  IncludePlotStyle = Yes
  IncludeText = Yes
  IncludeGeom = Yes
  IncludeAuxData = Yes
  IncludeStreamPositions = Yes
  IncludeContourLevels = Yes
  Merge = No
  IncludeFrameSizeAndPosition = No

$!CreateMirrorZones 
  SourceZones =  [1-23]
  MirrorVars =  [3]

$!PRINTSETUP PALETTE = COLOR
$!EXPORTSETUP EXPORTREGION = ALLFRAMES
$!EXPORTSETUP IMAGEWIDTH = 3000
$!EXPORTSETUP EXPORTFNAME = 'C:\Users\aobo\Desktop\plot_wing\BWB_ouput_figure\|num|.png'
$!EXPORT 
  EXPORTREGION = ALLFRAMES
$!EndLoop
$!RemoveVar |MFBD|
