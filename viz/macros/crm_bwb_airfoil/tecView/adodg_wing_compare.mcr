#!MC 1410
$!FrameLayout XYPos{X = 0.800000000000000044}
$!FrameLayout Width = 4.5
$!FrameLayout XYPos{Y = 0.5}
$!FrameLayout Height = 3.89999999999999991
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
$!FrameLayout XYPos{X = 5.29999999999999982}
$!FrameLayout Width = 4.5
$!FrameLayout XYPos{Y = 0.5}
$!FrameLayout Height = 3.89999999999999991
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
$!FrameLayout XYPos{X = 0.800000000000000044}
$!FrameLayout Width = 4.5
$!FrameLayout XYPos{Y = 4.40000000000000036}
$!FrameLayout Height = 1
$!CreateNewFrame 
  XYPos
    {
    X = 5.3038
    Y = 4.4173
    }
  Width = 4.4894
  Height = 1.4827
$!FrameLayout XYPos{X = 5.29999999999999982}
$!FrameLayout Width = 4.5
$!FrameLayout Height = 1
$!FrameLayout XYPos{Y = 4.40000000000000036}
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
$!ReadDataSet  '"STANDARDSYNTAX" "1.0" "FILELIST_CGNSFILES" "1" "C:\Users\aobo\Desktop\plot_wing\tecView\CFD\surf.cgns" "LoadBCs" "Yes" "AssignStrandIDs" "Yes" "UniformGridStructure" "Yes" "LoaderVersion" "V3" "CgnsLibraryVersion" "4.1.2"'
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
$!ReadStyleSheet  "C:\Users\aobo\Desktop\plot_wing\tecView\wing_left.sty"
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
$!ReadDataSet  '"STANDARDSYNTAX" "1.0" "FILELIST_CGNSFILES" "1" "C:\Users\aobo\Desktop\plot_wing\tecView\NN\surf.cgns" "LoadBCs" "Yes" "AssignStrandIDs" "Yes" "UniformGridStructure" "Yes" "LoaderVersion" "V3" "CgnsLibraryVersion" "4.1.2"'
  DataSetReader = 'CGNS Loader'
  ReadDataOption = New
  ResetStyle = No
  AssignStrandIDs = Yes
  InitialPlotType = Cartesian3D
  InitialPlotFirstZoneOnly = No
  AddZonesToExistingStrands = No
  VarLoadMode = ByName
$!ReadStyleSheet  "C:\Users\aobo\Desktop\plot_wing\tecView\wing_right.sty"
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
  Y = 4.91288074342
$!Pick AddAtPosition
  X = 3.4494062984
  Y = 4.91288074342
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 2.85054207537
  Y = 5.22263810015
  ConsiderStyle = Yes
$!ReadDataSet  '"STANDARDSYNTAX" "1.0" "FILELIST_CGNSFILES" "1" "C:\Users\aobo\Desktop\plot_wing\tecView\CFD\surf.cgns" "LoadBCs" "Yes" "AssignStrandIDs" "Yes" "UniformGridStructure" "Yes" "LoaderVersion" "V3" "CgnsLibraryVersion" "4.1.2"'
  DataSetReader = 'CGNS Loader'
  ReadDataOption = New
  ResetStyle = No
  AssignStrandIDs = Yes
  InitialPlotType = Cartesian3D
  InitialPlotFirstZoneOnly = No
  AddZonesToExistingStrands = No
  VarLoadMode = ByName
$!ReadStyleSheet  "C:\Users\aobo\Desktop\plot_wing\tecView\wing_bottom_left.sty"
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
  Y = 5.06156427465
$!Pick AddAtPosition
  X = 7.88513164688
  Y = 5.06156427465
  ConsiderStyle = Yes
$!ReadDataSet  '"STANDARDSYNTAX" "1.0" "FILELIST_CGNSFILES" "1" "C:\Users\aobo\Desktop\plot_wing\tecView\NN\surf.cgns" "LoadBCs" "Yes" "AssignStrandIDs" "Yes" "UniformGridStructure" "Yes" "LoaderVersion" "V3" "CgnsLibraryVersion" "4.1.2"'
  DataSetReader = 'CGNS Loader'
  ReadDataOption = New
  ResetStyle = No
  AssignStrandIDs = Yes
  InitialPlotType = Cartesian3D
  InitialPlotFirstZoneOnly = No
  AddZonesToExistingStrands = No
  VarLoadMode = ByName
$!ReadStyleSheet  "C:\Users\aobo\Desktop\plot_wing\tecView\wing_bottom_right.sty"
  IncludePlotStyle = Yes
  IncludeText = Yes
  IncludeGeom = Yes
  IncludeAuxData = Yes
  IncludeStreamPositions = Yes
  IncludeContourLevels = Yes
  Merge = No
  IncludeFrameSizeAndPosition = No
$!FrameControl ActivateAtPosition
  X = 1.10351058338
  Y = 1.00993804853
$!Pick SetMouseMode
  MouseMode = Select
$!AttachText 
  AnchorPos
    {
    X = 3
    Y = 60
    }
  TextShape
    {
    FontFamily = 'Times'
    IsBold = No
    Height = 16
    }
  Color = Red
  Text = 'CFD-based optimization\n\nC<sub>D</sub> = 229.0 counts\nC<sub>L</sub> = 0.500\nC<sub>M</sub> = -0.170'
$!FrameControl ActivateAtPosition
  X = 8.54181724316
  Y = 1.37751677852
$!Pick SetMouseMode
  MouseMode = Select
$!AttachText 
  AnchorPos
    {
    X = 70
    Y = 60
    }
  TextShape
    {
    FontFamily = 'Times'
    IsBold = No
    Height = 16
    }
  Color = Blue
  Text = 'Data-based optimization\n\nC<sub>D</sub> = 229.0 counts\nC<sub>L</sub> = 0.497\nC<sub>M</sub> = -0.170	'
$!FrameControl ActivateAtPosition
  X = 9.14894166236
  Y = 2.00942178627
$!Pick SetMouseMode
  MouseMode = Select
$!Pick AddAtPosition
  X = 8.99612803304
  Y = 1.59228187919
  ConsiderStyle = Yes
$!Pick Clear
$!AttachText 
  AnchorPos
    {
    X = 70
    Y = 60
    }
  TextShape
    {
    FontFamily = 'Times'
    IsBold = No
    Height = 16
    }
  Color = Blue
  Text = '    Data-based optimization\n\n              C<sub>D</sub> = 229.0 counts\n              C<sub>L</sub> = 0.497\n              C<sub>M</sub> = -0.170'
$!Pick AddAtPosition
  X = 8.92591636551
  Y = 1.87725864739
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 8.92591636551
  Y = 1.87725864739
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 9.00025813113
  Y = 2.01355188436
  ConsiderStyle = Yes
$!Pick Clear
$!AttachText 
  AnchorPos
    {
    X = 40
    Y = 60
    }
  TextShape
    {
    FontFamily = 'Times'
    IsBold = No
    Height = 16
    }
  Color = Blue
  Text = '    Data-based optimization\n\n              C<sub>D</sub> = 229.0 counts\n              C<sub>L</sub> = 0.497\n              C<sub>M</sub> = -0.170'
$!FrameControl ActivateAtPosition
  X = 9.28523489933
  Y = 5.21024780589
$!Pick AddAtPosition
  X = 9.28523489933
  Y = 5.21024780589
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 10.3962312855
  Y = 3.3351832731
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 10.2599380485
  Y = 1.71618482189
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 9.99974186887
  Y = 1.61706246773
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 10.2640681466
  Y = 2.22418688694
  ConsiderStyle = Yes
$!FrameControl ActivateAtPosition
  X = 9.13655136809
  Y = 2.74044914817
$!Pick AddAtPosition
  X = 9.13655136809
  Y = 2.74044914817
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 9.16133195663
  Y = 2.80240061951
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 8.75245224574
  Y = 2.13332472896
  ConsiderStyle = Yes
$!Pick Clear
$!AttachText 
  AnchorPos
    {
    X = 45
    Y = 60
    }
  TextShape
    {
    FontFamily = 'Times'
    IsBold = No
    Height = 16
    }
  Color = Blue
  Text = '    Data-based optimization\n\n              C<sub>D</sub> = 229.0 counts\n              C<sub>L</sub> = 0.497\n              C<sub>M</sub> = -0.170'
$!Pick AddAtPosition
  X = 7.14997418689
  Y = 6.18908105318
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 10.8546721735
  Y = 5.35893133712
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 10.1029943211
  Y = 2.33569953536
  ConsiderStyle = Yes
$!FrameControl ActivateAtPosition
  X = 5.63009808983
  Y = 2.84370160041
$!Pick SetMouseMode
  MouseMode = Select
$!AttachText 
  AnchorPos
    {
    X = 50.6043
    Y = 36.6569
    }
  TextShape
    {
    FontFamily = 'Times'
    IsBold = No
    Height = 16
    }
  Text = 'A\n2.35%'
$!Pick SetMouseMode
  MouseMode = Select
$!Pick AddAtPosition
  X = 7.53820340733
  Y = 2.78175012907
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 7.7116675271
  Y = 2.78175012907
  ConsiderStyle = Yes
$!Pick Shift
  X = -2.2771935
  Y = 0.111512648425
$!Pick AddAtPosition
  X = 7.1871450697
  Y = 3.26084150749
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 7.68688693856
  Y = 2.79414042334
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 7.78600929272
  Y = 2.89326277749
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 7.59602478059
  Y = 2.94282395457
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 7.14171399071
  Y = 3.48799690243
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 5.63835828601
  Y = 3.24019101704
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 5.53097573567
  Y = 3.07911719153
  ConsiderStyle = Yes
$!Pick Shift
  X = 0
  Y = -0.0413009808983
$!Pick AddAtPosition
  X = 5.83660299432
  Y = 3.31453278265
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 7.78187919463
  Y = 2.81479091378
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 7.69927723283
  Y = 2.96347444502
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 7.92230252969
  Y = 3.99599896748
  ConsiderStyle = Yes
$!SliceAttributes 1  EdgeLayer{Show = Yes}
$!SliceAttributes 1  SliceSource = SurfaceZones
$!SliceLayers Show = Yes
$!SliceAttributes 1  SliceSurface = YPlanes
$!SliceAttributes 1  PrimaryPosition{Y = 7.81575636210618541E-06}
$!SliceAttributes 1  SliceSurface = ZPlanes
$!SliceAttributes 1  PrimaryPosition{Z = -3.93139051452722154E-18}
$!SliceAttributes 1  EdgeLayer{Show = No}
$!SliceAttributes 1  SliceSource = VolumeZones
$!SliceAttributes 1  SliceSurface = XPlanes
$!SliceAttributes 1  PrimaryPosition{X = -0.212861910462379456}
$!FrameControl ActivateAtPosition
  X = 5.22121837894
  Y = 3.83492514197
$!Pick AddAtPosition
  X = 5.22121837894
  Y = 3.83492514197
  ConsiderStyle = Yes
$!AttachGeom 
  GeomType = GeomImage
  PositionCoordSys = Frame
  AnchorPos
    {
    X = 25
    Y = 45.45541523153464
    }
  ImageFileName = 'C:\Users\aobo\Pictures\cp.PNG'
  PixelAspectRatio = 1
  RawData
50 9.08916953693 
$!FrameControl ActivateAtPosition
  X = 5.32034073309
  Y = 4.04143004646
$!Pick AddAtPosition
  X = 5.32034073309
  Y = 4.04143004646
  ConsiderStyle = Yes
$!FrameControl ActivateByNumber
  Frame = 2
$!FrameControl ActivateAtPosition
  X = 3.56091894682
  Y = 2.55872483221
$!Pick DeselectAll
$!Pick AddAllInRect
  SelectText = Yes
  SelectGeoms = Yes
  SelectZones = Yes
  ConsiderStyle = Yes
  X1 = 3.56091894682
  X2 = 3.77155394941
  Y1 = 2.55872483221
  Y2 = 2.8065307176
$!Pick AddAtPosition
  X = 3.56091894682
  Y = 2.43069179143
  ConsiderStyle = Yes
$!Pick Shift
  X = 2.12700051626
  Y = 1.37532266391
$!Pick AddAtPosition
  X = 4.7503871967
  Y = 3.89274651523
  CollectingObjectsMode = HomogeneousAdd
  ConsiderStyle = Yes
$!FrameControl ActivateByNumber
  Frame = 1
$!FrameControl MoveToTopByNumber
  Frame = 1
$!FrameControl ActivateAtPosition
  X = 5.9274651523
  Y = 4.61551368095
$!Pick AddAtPosition
  X = 5.9274651523
  Y = 4.61551368095
  ConsiderStyle = Yes
$!FrameControl ActivateAtPosition
  X = 5.44424367579
  Y = 3.88035622096
$!Pick AddAtPosition
  X = 5.44424367579
  Y = 3.88035622096
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 5.3575116159
  Y = 3.77297367062
  ConsiderStyle = Yes
$!FrameControl ActivateByNumber
  Frame = 4
$!Pick AddAtPosition
  X = 3.59808982963
  Y = 3.92991739804
  ConsiderStyle = Yes
$!FrameControl ActivateAtPosition
  X = 6.78239545689
  Y = 3.77297367062
$!Pick AddAtPosition
  X = 6.78239545689
  Y = 3.77297367062
  ConsiderStyle = Yes
$!Pick AddAtPosition
  X = 5.68791946309
  Y = 3.67385131647
  ConsiderStyle = Yes
$!FrameControl ActivateAtPosition
  X = 4.70082601962
  Y = 3.98360867321
$!Pick AddAtPosition
  X = 4.70082601962
  Y = 3.98360867321
  ConsiderStyle = Yes
$!Pick Clear
$!ExportSetup ExportFName = 'C:/Users/aobo/Desktop/plot_wing/tecView/wing_aaaa.png'
$!Export 
  ExportRegion = AllFrames