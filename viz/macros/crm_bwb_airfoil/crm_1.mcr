#!MC 1410
$!ReadDataSet  '"STANDARDSYNTAX" "1.0" "FILELIST_CGNSFILES" "1" "C:/Users/aobo/Desktop/plot_wing/volume/volume/ADODG4_iter_11_000_vol.cgns" "LoadBCs" "Yes" "AssignStrandIDs" "Yes" "UniformGridStructure" "Yes" "LoaderVersion" "V3" "CgnsLibraryVersion" "4.1.2"'
  DataSetReader = 'CGNS Loader'
  ReadDataOption = New
  ResetStyle = Yes
  AssignStrandIDs = Yes
  InitialPlotType = Cartesian3D
  InitialPlotFirstZoneOnly = No
  AddZonesToExistingStrands = No
  VarLoadMode = ByName
$!ExtendedCommand 
  CommandProcessorID = 'CFDAnalyzer4'
  Command = 'Calculate Function=\'SHOCK\' Normalization=\'None\' ValueLocation=\'Nodal\' CalculateOnDemand=\'T\' UseMorePointsForFEGradientCalculations=\'F\''
$!ExtendedCommand 
  CommandProcessorID = 'CFDAnalyzer4'
  Command = 'Calculate Function=\'PRESSURECOEF\' Normalization=\'None\' ValueLocation=\'Nodal\' CalculateOnDemand=\'T\' UseMorePointsForFEGradientCalculations=\'F\''
$!GlobalRGB RedChannelVar = 10
$!GlobalRGB GreenChannelVar = 4
$!GlobalRGB BlueChannelVar = 4
$!SetContourVar 
  Var = 4
  ContourGroup = 1
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 5
  ContourGroup = 2
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 6
  ContourGroup = 3
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 7
  ContourGroup = 4
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 8
  ContourGroup = 5
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 9
  ContourGroup = 6
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 10
  ContourGroup = 7
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 11
  ContourGroup = 8
  LevelInitMode = ResetToNice
$!FieldLayers ShowContour = Yes
$!SetContourVar 
  Var = 12
  ContourGroup = 1
  LevelInitMode = ResetToNice
$!IsoSurfaceLayers Show = Yes
$!IsoSurfaceAttributes 1  ShowGroup = No
$!IsoSurfaceAttributes 2  ShowGroup = Yes
$!IsoSurfaceAttributes 2  DefinitionContourGroup = 8
$!IsoSurfaceAttributes 2  Isovalue1 = 1
