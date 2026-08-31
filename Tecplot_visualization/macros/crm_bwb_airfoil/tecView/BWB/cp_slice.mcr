#!MC 1410
$!FrameLayout XYPos{Y = 0.5}
$!FrameLayout Height = 5
$!FrameLayout ShowBorder = No
$!ReadDataSet  '"C:\Users\aobo\Desktop\plot_wing\tecView\BWB\BWB_non_optimized\fc_000_slices.dat" '
  ReadDataOption = New
  ResetStyle = No
  VarLoadMode = ByName
  AssignStrandIDs = Yes
  VarNameList = '"CoordinateX" "CoordinateY" "CoordinateZ" "XoC" "YoC" "ZoC" "VelocityX" "VelocityY" "VelocityZ" "CoefPressure" "Mach"'
$!ReadStyleSheet  "C:\Users\aobo\Desktop\plot_wing\tecView\BWB_slice_up.sty"
  IncludePlotStyle = Yes
  IncludeText = Yes
  IncludeGeom = Yes
  IncludeAuxData = Yes
  IncludeStreamPositions = Yes
  IncludeContourLevels = Yes
  Merge = No
  IncludeFrameSizeAndPosition = No
$!ReadDataSet  '"C:\Users\aobo\Desktop\plot_wing\tecView\BWB\BWB_FFD\no_TELE\fc_311_slices.dat" '
  ReadDataOption = Append
  ResetStyle = No
  VarLoadMode = ByName
  AssignStrandIDs = Yes
  VarNameList = '"CoordinateX" "CoordinateY" "CoordinateZ" "XoC" "YoC" "ZoC" "VelocityX" "VelocityY" "VelocityZ" "CoefPressure" "Mach"'
$!ReadDataSet  '"C:\Users\aobo\Desktop\plot_wing\tecView\BWB\BWB_dmm\L2\fc_000_slices.dat" '
  ReadDataOption = Append
  ResetStyle = No
  VarLoadMode = ByName
  AssignStrandIDs = Yes
  VarNameList = '"CoordinateX" "CoordinateY" "CoordinateZ" "XoC" "YoC" "ZoC" "VelocityX" "VelocityY" "VelocityZ" "CoefPressure" "Mach"'
$!CreateLineMap 
$!LineMap [1]  Name = 'Map 0'
$!LineMap [1]  Assign{Zone = 1}
$!ActiveLineMaps += [1]
$!CreateLineMap 
$!LineMap [2]  Name = 'Map 1'
$!LineMap [2]  Assign{Zone = 9}
$!LineMap [2]  Assign{YAxisVar = 10}
$!ActiveLineMaps += [2]
$!CreateLineMap 
$!LineMap [3]  Name = 'Map 2'
$!LineMap [3]  Assign{YAxisVar = 10}
$!LineMap [3]  Assign{Zone = 17}
$!ActiveLineMaps += [3]
$!LineMap [1]  Lines{Color = Black}
$!LineMap [2]  Lines{Color = Blue}
$!LineMap [3]  Lines{Color = Red}
$!LineMap [1]  Lines{LineThickness = 1.0}
$!LineMap [2]  Lines{LineThickness = 1.0}
$!LineMap [3]  Lines{LineThickness = 1.0}
$!LineMap [1]  Lines{LinePattern = Solid}
$!LineMap [2]  Lines{LinePattern = Dashed}
$!LineMap [3]  Lines{LinePattern = LongDash}
$!FrameLayout ShowBorder = No
$!View Fit
$!ExportSetup ImageWidth = 2179
$!ExportSetup ExportFName = 'C:\Users\aobo\Desktop\plot_wing\tecView\BWB\cp_slice\A_cp.png'
$!Export 
  ExportRegion = AllFrames

$!CreateLineMap 
$!LineMap [1]  Name = 'Map 0'
$!LineMap [1]  Assign{Zone = 2}
$!ActiveLineMaps += [1]
$!CreateLineMap 
$!LineMap [2]  Name = 'Map 1'
$!LineMap [2]  Assign{Zone = 10}
$!LineMap [2]  Assign{YAxisVar = 10}
$!ActiveLineMaps += [2]
$!CreateLineMap 
$!LineMap [3]  Name = 'Map 2'
$!LineMap [3]  Assign{YAxisVar = 10}
$!LineMap [3]  Assign{Zone = 18}
$!ActiveLineMaps += [3]
$!LineMap [1]  Lines{Color = Black}
$!LineMap [2]  Lines{Color = Blue}
$!LineMap [3]  Lines{Color = Red}
$!LineMap [1]  Lines{LineThickness = 1.0}
$!LineMap [2]  Lines{LineThickness = 1.0}
$!LineMap [3]  Lines{LineThickness = 1.0}
$!LineMap [1]  Lines{LinePattern = Solid}
$!LineMap [2]  Lines{LinePattern = Dashed}
$!LineMap [3]  Lines{LinePattern = LongDash}
$!FrameLayout ShowBorder = No
$!View Fit
$!ExportSetup ImageWidth = 2179
$!ExportSetup ExportFName = 'C:\Users\aobo\Desktop\plot_wing\tecView\BWB\cp_slice\B_cp.png'
$!Export 
  ExportRegion = AllFrames

$!CreateLineMap 
$!LineMap [1]  Name = 'Map 0'
$!LineMap [1]  Assign{Zone = 3}
$!ActiveLineMaps += [1]
$!CreateLineMap 
$!LineMap [2]  Name = 'Map 1'
$!LineMap [2]  Assign{Zone = 11}
$!LineMap [2]  Assign{YAxisVar = 10}
$!ActiveLineMaps += [2]
$!CreateLineMap 
$!LineMap [3]  Name = 'Map 2'
$!LineMap [3]  Assign{YAxisVar = 10}
$!LineMap [3]  Assign{Zone = 19}
$!ActiveLineMaps += [3]
$!LineMap [1]  Lines{Color = Black}
$!LineMap [2]  Lines{Color = Blue}
$!LineMap [3]  Lines{Color = Red}
$!LineMap [1]  Lines{LineThickness = 1.0}
$!LineMap [2]  Lines{LineThickness = 1.0}
$!LineMap [3]  Lines{LineThickness = 1.0}
$!LineMap [1]  Lines{LinePattern = Solid}
$!LineMap [2]  Lines{LinePattern = Dashed}
$!LineMap [3]  Lines{LinePattern = LongDash}
$!FrameLayout ShowBorder = No
$!View Fit
$!ExportSetup ImageWidth = 2179
$!ExportSetup ExportFName = 'C:\Users\aobo\Desktop\plot_wing\tecView\BWB\cp_slice\C_cp.png'
$!Export 
  ExportRegion = AllFrames

$!CreateLineMap 
$!LineMap [1]  Name = 'Map 0'
$!LineMap [1]  Assign{Zone = 4}
$!ActiveLineMaps += [1]
$!CreateLineMap 
$!LineMap [2]  Name = 'Map 1'
$!LineMap [2]  Assign{Zone = 12}
$!LineMap [2]  Assign{YAxisVar = 10}
$!ActiveLineMaps += [2]
$!CreateLineMap 
$!LineMap [3]  Name = 'Map 2'
$!LineMap [3]  Assign{YAxisVar = 10}
$!LineMap [3]  Assign{Zone = 20}
$!ActiveLineMaps += [3]
$!LineMap [1]  Lines{Color = Black}
$!LineMap [2]  Lines{Color = Blue}
$!LineMap [3]  Lines{Color = Red}
$!LineMap [1]  Lines{LineThickness = 1.0}
$!LineMap [2]  Lines{LineThickness = 1.0}
$!LineMap [3]  Lines{LineThickness = 1.0}
$!LineMap [1]  Lines{LinePattern = Solid}
$!LineMap [2]  Lines{LinePattern = Dashed}
$!LineMap [3]  Lines{LinePattern = LongDash}
$!FrameLayout ShowBorder = No
$!View Fit
$!ExportSetup ImageWidth = 2179
$!ExportSetup ExportFName = 'C:\Users\aobo\Desktop\plot_wing\tecView\BWB\cp_slice\D_cp.png'
$!Export 
  ExportRegion = AllFrames

$!CreateLineMap 
$!LineMap [1]  Name = 'Map 0'
$!LineMap [1]  Assign{Zone = 5}
$!ActiveLineMaps += [1]
$!CreateLineMap 
$!LineMap [2]  Name = 'Map 1'
$!LineMap [2]  Assign{Zone = 13}
$!LineMap [2]  Assign{YAxisVar = 10}
$!ActiveLineMaps += [2]
$!CreateLineMap 
$!LineMap [3]  Name = 'Map 2'
$!LineMap [3]  Assign{YAxisVar = 10}
$!LineMap [3]  Assign{Zone = 21}
$!ActiveLineMaps += [3]
$!LineMap [1]  Lines{Color = Black}
$!LineMap [2]  Lines{Color = Blue}
$!LineMap [3]  Lines{Color = Red}
$!LineMap [1]  Lines{LineThickness = 1.0}
$!LineMap [2]  Lines{LineThickness = 1.0}
$!LineMap [3]  Lines{LineThickness = 1.0}
$!LineMap [1]  Lines{LinePattern = Solid}
$!LineMap [2]  Lines{LinePattern = Dashed}
$!LineMap [3]  Lines{LinePattern = LongDash}
$!FrameLayout ShowBorder = No
$!View Fit
$!ExportSetup ImageWidth = 2179
$!ExportSetup ExportFName = 'C:\Users\aobo\Desktop\plot_wing\tecView\BWB\cp_slice\E_cp.png'
$!Export 
  ExportRegion = AllFrames

$!CreateLineMap 
$!LineMap [1]  Name = 'Map 0'
$!LineMap [1]  Assign{Zone = 6}
$!ActiveLineMaps += [1]
$!CreateLineMap 
$!LineMap [2]  Name = 'Map 1'
$!LineMap [2]  Assign{Zone = 14}
$!LineMap [2]  Assign{YAxisVar = 10}
$!ActiveLineMaps += [2]
$!CreateLineMap 
$!LineMap [3]  Name = 'Map 2'
$!LineMap [3]  Assign{YAxisVar = 10}
$!LineMap [3]  Assign{Zone = 22}
$!ActiveLineMaps += [3]
$!LineMap [1]  Lines{Color = Black}
$!LineMap [2]  Lines{Color = Blue}
$!LineMap [3]  Lines{Color = Red}
$!LineMap [1]  Lines{LineThickness = 1.0}
$!LineMap [2]  Lines{LineThickness = 1.0}
$!LineMap [3]  Lines{LineThickness = 1.0}
$!LineMap [1]  Lines{LinePattern = Solid}
$!LineMap [2]  Lines{LinePattern = Dashed}
$!LineMap [3]  Lines{LinePattern = LongDash}
$!FrameLayout ShowBorder = No
$!View Fit
$!ExportSetup ImageWidth = 2179
$!ExportSetup ExportFName = 'C:\Users\aobo\Desktop\plot_wing\tecView\BWB\cp_slice\F_cp.png'
$!Export 
  ExportRegion = AllFrames

$!CreateLineMap 
$!LineMap [1]  Name = 'Map 0'
$!LineMap [1]  Assign{Zone = 7}
$!ActiveLineMaps += [1]
$!CreateLineMap 
$!LineMap [2]  Name = 'Map 1'
$!LineMap [2]  Assign{Zone = 15}
$!LineMap [2]  Assign{YAxisVar = 10}
$!ActiveLineMaps += [2]
$!CreateLineMap 
$!LineMap [3]  Name = 'Map 2'
$!LineMap [3]  Assign{YAxisVar = 10}
$!LineMap [3]  Assign{Zone = 23}
$!ActiveLineMaps += [3]
$!LineMap [1]  Lines{Color = Black}
$!LineMap [2]  Lines{Color = Blue}
$!LineMap [3]  Lines{Color = Red}
$!LineMap [1]  Lines{LineThickness = 1.0}
$!LineMap [2]  Lines{LineThickness = 1.0}
$!LineMap [3]  Lines{LineThickness = 1.0}
$!LineMap [1]  Lines{LinePattern = Solid}
$!LineMap [2]  Lines{LinePattern = Dashed}
$!LineMap [3]  Lines{LinePattern = LongDash}
$!FrameLayout ShowBorder = No
$!View Fit
$!ExportSetup ImageWidth = 2179
$!ExportSetup ExportFName = 'C:\Users\aobo\Desktop\plot_wing\tecView\BWB\cp_slice\G_cp.png'
$!Export 
  ExportRegion = AllFrames

$!CreateLineMap 
$!LineMap [1]  Name = 'Map 0'
$!LineMap [1]  Assign{Zone = 8}
$!ActiveLineMaps += [1]
$!CreateLineMap 
$!LineMap [2]  Name = 'Map 1'
$!LineMap [2]  Assign{Zone = 16}
$!LineMap [2]  Assign{YAxisVar = 10}
$!ActiveLineMaps += [2]
$!CreateLineMap 
$!LineMap [3]  Name = 'Map 2'
$!LineMap [3]  Assign{YAxisVar = 10}
$!LineMap [3]  Assign{Zone = 24}
$!ActiveLineMaps += [3]
$!LineMap [1]  Lines{Color = Black}
$!LineMap [2]  Lines{Color = Blue}
$!LineMap [3]  Lines{Color = Red}
$!LineMap [1]  Lines{LineThickness = 1.0}
$!LineMap [2]  Lines{LineThickness = 1.0}
$!LineMap [3]  Lines{LineThickness = 1.0}
$!LineMap [1]  Lines{LinePattern = Solid}
$!LineMap [2]  Lines{LinePattern = Dashed}
$!LineMap [3]  Lines{LinePattern = LongDash}
$!FrameLayout ShowBorder = No
$!View Fit
$!ExportSetup ImageWidth = 2179
$!ExportSetup ExportFName = 'C:\Users\aobo\Desktop\plot_wing\tecView\BWB\cp_slice\H_cp.png'
$!Export 
  ExportRegion = AllFrames