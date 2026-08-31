#!MC 1410
$!VarSet |MFBD| = 'C:\Users\aobo\Desktop\plot_wing\circle_airfoil_volume'
$!VarSet |NumLoop| = 820
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

$!READDATASET  '"STANDARDSYNTAX" "1.0" "FILELIST_CGNSFILES" "1" "C:\Users\aobo\Desktop\plot_wing\circle_airfoil_volume\circle_2d5_iter_|num|_000_vol.cgns" "LoadBCs" "Yes" "AssignStrandIDs" "Yes" "UniformGridStructure" "Yes" "LoaderVersion" "V3" "CgnsLibraryVersion" "4.1.2"'
  DataSetReader = 'CGNS Loader'
  ReadDataOption = New
  ResetStyle = Yes
  AssignStrandIDs = Yes
  InitialPlotType = Cartesian3D
  InitialPlotFirstZoneOnly = No
  AddZonesToExistingStrands = No
  VarLoadMode = ByName

$!PlotType = Cartesian2D
$!ExtendedCommand 
  CommandProcessorID = 'CFDAnalyzer4'
  Command = 'SetFieldVariables ConvectionVarsAreMomentum=\'F\' UVarNum=5 VVarNum=6 WVarNum=7 ID1=\'Pressure\' Variable1=8 ID2=\'Density\' Variable2=4'
$!ExtendedCommand 
  CommandProcessorID = 'CFDAnalyzer4'
  Command = 'Calculate Function=\'SHADOWGRAPH\' Normalization=\'None\' ValueLocation=\'Nodal\' CalculateOnDemand=\'T\' UseMorePointsForFEGradientCalculations=\'F\''
$!FieldLayers ShowMesh = Yes
$!GlobalRGB RedChannelVar = 10
$!GlobalRGB GreenChannelVar = 3
$!GlobalRGB BlueChannelVar = 3
$!SetContourVar 
  Var = 3
  ContourGroup = 1
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 4
  ContourGroup = 2
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 5
  ContourGroup = 3
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 6
  ContourGroup = 4
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 7
  ContourGroup = 5
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 8
  ContourGroup = 6
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 9
  ContourGroup = 7
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 10
  ContourGroup = 8
  LevelInitMode = ResetToNice
$!FieldLayers ShowContour = Yes
$!ActiveFieldMaps += [3]
$!ActiveFieldMaps += [4]
$!ActiveFieldMaps += [5]
$!View NiceFit
  ConsiderBlanking = Yes
$!SetContourVar 
  Var = 11
  ContourGroup = 1
  LevelInitMode = ResetToNice
$!ContourLevels New
  ContourGroup = 1
  RawData
11
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1

$!FieldLayers ShowMesh = No
$!TwoDAxis XDetail{ShowAxis = No}
$!TwoDAxis YDetail{ShowAxis = No}
$!View NiceFit
  ConsiderBlanking = Yes
$!View DataFit
  ConsiderBlanking = Yes
$!Pick SetMouseMode
  MouseMode = Select
$!Pick AddAtPosition
  X = 7.9181724316
  Y = 2.34808982963
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 8.05859576665
  Y = 2.17049561177
  ConsiderStyle = Yes
$!GlobalContour 1  Legend{IsVertical = No}
$!GlobalContour 1  Legend{Box{BoxType = None}}
$!Pick DeselectAll
$!Pick AddAllInRect
  SelectText = Yes
  SelectGeoms = Yes
  SelectZones = Yes
  ConsiderStyle = Yes
  X1 = 7.57537429014
  X2 = 7.87274135261
  Y1 = 2.83957150232
  Y2 = 4.78484770263
$!Pick AddAtPosition
  X = 7.94708311822
  Y = 3.35170366546
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 8.23205988642
  Y = 1.1421011874
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 7.81078988126
  Y = 2.28613835829
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 6.95172947858
  Y = 4.28923593185
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 8.28988125968
  Y = 3.39713474445
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 9.5826019618
  Y = 4.41726897264
  ConsiderStyle = Yes

$!ReadStyleSheet  "C:\Users\aobo\Desktop\plot_wing\airfoil_shadowgraph_3.sty"
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
$!EXPORTSETUP EXPORTFNAME = 'C:\Users\aobo\Desktop\plot_wing\airfoil_shadowgraph\|num|.png'
$!EXPORT 
  EXPORTREGION = ALLFRAMES
$!EndLoop
$!RemoveVar |MFBD|
