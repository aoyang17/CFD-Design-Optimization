#!MC 1410
$!FrameLayout Width = 3
$!FrameLayout Height = 2.5
$!FrameLayout XYPos{X = 0}
$!CreateNewFrame 
$!FrameLayout XYPos{X = 0}
$!FrameLayout Width = 3
$!FrameLayout Height = 2.5
$!FrameLayout XYPos{Y = 0.25}
$!FrameLayout ShowBorder = No
$!FrameLayout IsTransparent = Yes
$!ReadDataSet  '"STANDARDSYNTAX" "1.0" "FILELIST_CGNSFILES" "1" "C:\Users\aobo\Desktop\plot_wing\tecView\circle_2_airfoil_surf\surface\circle_2d5_iter_20_000_surf.cgns" "LoadBCs" "Yes" "AssignStrandIDs" "Yes" "UniformGridStructure" "Yes" "LoaderVersion" "V3" "CgnsLibraryVersion" "4.1.2"'
  DataSetReader = 'CGNS Loader'
  ReadDataOption = New
  ResetStyle = No
  AssignStrandIDs = Yes
  InitialPlotType = Cartesian3D
  InitialPlotFirstZoneOnly = No
  AddZonesToExistingStrands = No
  VarLoadMode = ByName
$!ReadStyleSheet  "C:\Users\aobo\Desktop\plot_wing\tecView\circle_airfoil.sty"
  IncludePlotStyle = Yes
  IncludeText = Yes
  IncludeGeom = Yes
  IncludeAuxData = Yes
  IncludeStreamPositions = Yes
  IncludeContourLevels = Yes
  Merge = No
  IncludeFrameSizeAndPosition = No
$!FrameLayout IsTransparent = No

$!ExportSetup ExportFName = 'C:/Users/aobo/Desktop/plot_wing/tecView/circle_airfoil.png'
$!Export 
  ExportRegion = AllFrames
