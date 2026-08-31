#!MC 1410
$!FrameLayout XYPos{X = 0.8}
$!FrameLayout Width = 4.5
$!FrameLayout XYPos{Y = 0.5}
$!FrameLayout Height = 4.9
$!Pick AddAtPosition
  X = 10.8464119773
  Y = 5.35893133712
  ConsiderStyle = Yes
$!CreateNewFrame 
  XYPos
    {
    X = 5.2914
    Y = 0.50194
    }
  Width = 4.316
  Height = 3.9029
$!FrameLayout XYPos{X = 5.3}
$!FrameLayout Width = 4.5
$!FrameLayout XYPos{Y = 0.5}
$!FrameLayout Height = 4.9
$!Pick SetMouseMode
  MouseMode = Select
$!Pick AddAtPosition
  X = 5.66726897264
  Y = 1.92268972638
  ConsiderStyle = Yes
$!FrameLayout ShowBorder = No
$!Pick AddAtPosition
  X = 3.4081053175
  Y = 5.0822147651
  ConsiderStyle = Yes
$!CreateNewFrame 
  XYPos
    {
    X = 0.79788
    Y = 4.4049
    }
  Width = 4.4977
  Height = 1.4249
$!FrameLayout XYPos{X = 0.8}
$!FrameLayout Width = 4.5
$!FrameLayout XYPos{Y = 5.4}
$!FrameLayout Height = 1
$!FrameLayout ShowBorder = No
$!CreateNewFrame 
  XYPos
    {
    X = 5.3038
    Y = 4.4173
    }
  Width = 4.4894
  Height = 1.4827
$!FrameLayout XYPos{X = 5.3}
$!FrameLayout Width = 4.5
$!FrameLayout Height = 1
$!FrameLayout XYPos{Y = 5.4}
$!FrameLayout ShowBorder = No
$!Pick SetMouseMode
  MouseMode = Select
$!FrameControl ActivateAtPosition
  X = 3.09008776458
  Y = 5.03678368611
$!Pick AddAtPosition
  X = 3.09008776458
  Y = 5.03678368611
  ConsiderStyle = Yes
$!FrameLayout ShowBorder = No
$!FrameControl ActivateAtPosition
  X = 7.37712958183
  Y = 3.07911719153
$!Pick AddAtPosition
  X = 7.37712958183
  Y = 3.07911719153
  ConsiderStyle = Yes
$!FrameControl ActivateAtPosition
  X = 1.91300980898
  Y = 3.42191533299
$!Pick AddAtPosition
  X = 1.91300980898
  Y = 3.42191533299
  ConsiderStyle = Yes
$!FrameLayout ShowBorder = No
$!Pick AddAtPosition
  X = 4.84950955085
  Y = 5.99909654104
  ConsiderStyle = Yes
$!ReadDataSet  '"STANDARDSYNTAX" "1.0" "FILELIST_CGNSFILES" "1" "C:\Users\aobo\Desktop\plot_wing\tecView\BWB_wz\L3\L3_wei_nonopt_000_surf.cgns" "LoadBCs" "Yes" "AssignStrandIDs" "Yes" "UniformGridStructure" "Yes" "LoaderVersion" "V3" "CgnsLibraryVersion" "4.1.2"'
  DataSetReader = 'CGNS Loader'
  ReadDataOption = New
  ResetStyle = No
  AssignStrandIDs = Yes
  InitialPlotType = Cartesian3D
  InitialPlotFirstZoneOnly = No
  AddZonesToExistingStrands = No
  VarLoadMode = ByName
$!Pick AddAtPosition
  X = 2.8381517811
  Y = 2.17462570986
  ConsiderStyle = Yes
$!ReadStyleSheet  "C:\Users\aobo\Desktop\plot_wing\tecView\bwb_wing_left.sty"
  IncludePlotStyle = Yes
  IncludeText = Yes
  IncludeGeom = Yes
  IncludeAuxData = Yes
  IncludeStreamPositions = Yes
  IncludeContourLevels = Yes
  Merge = No
  IncludeFrameSizeAndPosition = No
$!FrameControl ActivateAtPosition
  X = 6.70805369128
  Y = 2.38526071244
$!Pick AddAtPosition
  X = 6.70805369128
  Y = 2.38526071244
  ConsiderStyle = Yes
$!ReadDataSet  '"STANDARDSYNTAX" "1.0" "FILELIST_CGNSFILES" "1" "C:\Users\aobo\Desktop\plot_wing\tecView\BWB_wz\L3\L3_wei_opt_000_surf.cgns" "LoadBCs" "Yes" "AssignStrandIDs" "Yes" "UniformGridStructure" "Yes" "LoaderVersion" "V3" "CgnsLibraryVersion" "4.1.2"'
  DataSetReader = 'CGNS Loader'
  ReadDataOption = New
  ResetStyle = No
  AssignStrandIDs = Yes
  InitialPlotType = Cartesian3D
  InitialPlotFirstZoneOnly = No
  AddZonesToExistingStrands = No
  VarLoadMode = ByName
$!ReadStyleSheet  "C:\Users\aobo\Desktop\plot_wing\tecView\bwb_wing_right.sty"
  IncludePlotStyle = Yes
  IncludeText = Yes
  IncludeGeom = Yes
  IncludeAuxData = Yes
  IncludeStreamPositions = Yes
  IncludeContourLevels = Yes
  Merge = No
  IncludeFrameSizeAndPosition = No
$!FrameControl ActivateAtPosition
  X = 3.4494062984
  Y = 5.91288074342
$!Pick AddAtPosition
  X = 3.4494062984
  Y = 5.91288074342
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 2.85054207537
  Y = 5.22263810015
  ConsiderStyle = Yes
$!ReadDataSet  '"STANDARDSYNTAX" "1.0" "FILELIST_CGNSFILES" "1" "C:\Users\aobo\Desktop\plot_wing\tecView\BWB_wz\L3\L3_wei_nonopt_000_surf.cgns" "LoadBCs" "Yes" "AssignStrandIDs" "Yes" "UniformGridStructure" "Yes" "LoaderVersion" "V3" "CgnsLibraryVersion" "4.1.2"'
  DataSetReader = 'CGNS Loader'
  ReadDataOption = New
  ResetStyle = No
  AssignStrandIDs = Yes
  InitialPlotType = Cartesian3D
  InitialPlotFirstZoneOnly = No
  AddZonesToExistingStrands = No
  VarLoadMode = ByName
$!ReadStyleSheet  "C:\Users\aobo\Desktop\plot_wing\tecView\bwb_bottom_left.sty"
  IncludePlotStyle = Yes
  IncludeText = Yes
  IncludeGeom = Yes
  IncludeAuxData = Yes
  IncludeStreamPositions = Yes
  IncludeContourLevels = Yes
  Merge = No
  IncludeFrameSizeAndPosition = No
$!FrameControl ActivateAtPosition
  X = 7.88513164688
  Y = 5.66156427465
$!Pick AddAtPosition
  X = 7.88513164688
  Y = 5.66156427465
  ConsiderStyle = Yes
$!ReadDataSet  '"STANDARDSYNTAX" "1.0" "FILELIST_CGNSFILES" "1" "C:\Users\aobo\Desktop\plot_wing\tecView\BWB_wz\L3\L3_wei_opt_000_surf.cgns" "LoadBCs" "Yes" "AssignStrandIDs" "Yes" "UniformGridStructure" "Yes" "LoaderVersion" "V3" "CgnsLibraryVersion" "4.1.2"'
  DataSetReader = 'CGNS Loader'
  ReadDataOption = New
  ResetStyle = No
  AssignStrandIDs = Yes
  InitialPlotType = Cartesian3D
  InitialPlotFirstZoneOnly = No
  AddZonesToExistingStrands = No
  VarLoadMode = ByName
$!ReadStyleSheet  "C:\Users\aobo\Desktop\plot_wing\tecView\bwb_bottom_right.sty"
  IncludePlotStyle = Yes
  IncludeText = Yes
  IncludeGeom = Yes
  IncludeAuxData = Yes
  IncludeStreamPositions = Yes
  IncludeContourLevels = Yes
  Merge = No
  IncludeFrameSizeAndPosition = No
$!ExportSetup ExportFName = 'C:/Users/aobo/Desktop/plot_wing/tecView/bwb.png'
$!Export 
  ExportRegion = AllFrames