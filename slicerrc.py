# Python commands in this file are executed on Slicer startup

# Examples:
#
# Load a scene file
# slicer.util.loadScene('c:/Users/SomeUser/Documents/SlicerScenes/SomeScene.mrb')
#
# Open a module (overrides default startup module in application settings / modules)
# slicer.util.mainWindow().moduleSelector().selectModule('SegmentEditor')
#

################################################################################

def infoSlicerRC(s):
    import logging
    logging.info(".slicerrc.py: " + s) 



################################################################################

# set the default model save format to .stl (defautl: .vtk)
def setModelStorageFormat(ext):
    defaultModelStorageNode = slicer.vtkMRMLModelStorageNode()
    defaultModelStorageNode.SetUseCompression(0)
    defaultModelStorageNode.SetDefaultWriteFileExtension( ext )
    slicer.mrmlScene.AddDefaultNode(defaultModelStorageNode)



################################################################################

# enable/disable volume interpolation 
def setVolumeInterpolation(v):
    def setInterpolationAll(v):
      for node in slicer.util.getNodes('*').values():
        if node.IsA('vtkMRMLScalarVolumeDisplayNode'):
          node.SetInterpolate( v )
    def interpolator(caller,event):
      setInterpolationAll(v) # ^ TODO: use Node in 'event'
    # set value for all current nodes:
    setInterpolationAll( v )
    # observe new volumes 
    slicer.mrmlScene.AddObserver(slicer.mrmlScene.NodeAddedEvent, interpolator)

################################################################################

# set overwrite mode for all segmentation 
# (it looks like a singleton so we can actually do it once (at some point)
def setSegmentationOverwriteMode(v):
    def setMode(v):
      for node in slicer.util.getNodes('*').values():
        if node.IsA('vtkMRMLSegmentEditorNode'):
          node.SetOverwriteMode( v )
    def callback(caller,event):
      setMode(v) 
    # set value for all current nodes:
    setMode( v )
    # observe new vtkMRMLSegmentEditorNode's
    slicer.mrmlScene.AddObserver(slicer.mrmlScene.NodeAddedEvent, callback)



################################################################################

# toggle 3D fullscreen
def createToggle3D():
    lm = slicer.app.layoutManager()
    layoutPrev = lm.layout 
    layout3D = slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView
    def toggle3D():
        global layoutPrev 
        if lm.layout == layout3D:
            lm.setLayout( layoutPrev )
        else:
            layoutPrev = lm.layout
            lm.setLayout( layout3D )
    # create GUI button
    widget = mainWindow().findChild('QToolBar', 'ViewToolBar')
    action = widget.addAction("3D") 
    action.setToolTip('Toggle 3D Fullscreen')
    action.connect('triggered()', lambda: toggle3D() )
    # create shortcut: f 
    shortcutToggle3D = qt.QShortcut( mainWindow() )
    shortcutToggle3D.setKey( qt.QKeySequence('f') )
    shortcutToggle3D.connect( 'activated()', toggle3D )



################################################################################
# custom layouts


# 3D view +  segmentation views
LAYOUTXML_SEGMENTATION_3D = """
<layout type="horizontal" split="true" >
 <item splitSize="600">
  <view class="vtkMRMLViewNode" singletontag="1" verticalStretch="0">
    <property name="viewlabel" action="default">1</property>
  </view>
 </item>
 <item splitSize="400">
  <layout type="vertical">

   <item>
    <view class="vtkMRMLSliceNode" singletontag="Segmentation-">
     <property name="orientation" action="default">Axial</property>
     <property name="viewlabel" action="default">Segmentation-</property>
     <property name="viewcolor" action="default">#FBB0E9</property>
    </view>
   </item>

   <item>
    <view class="vtkMRMLSliceNode" singletontag="Segmentation">
     <property name="orientation" action="default">Axial</property>
     <property name="viewlabel" action="default">Segmentation</property>
     <property name="viewcolor" action="default">#CC0099</property>
    </view>
   </item>
  </layout>
 </item>
</layout>
"""

#  segmentation views, fullscreen
LAYOUTXML_SEGMENTATION = """
<layout type="horizontal">

   <item>
    <view class="vtkMRMLSliceNode" singletontag="Segmentation-">
     <property name="orientation" action="default">Axial</property>
     <property name="viewlabel" action="default">Segmentation-</property>
     <property name="viewcolor" action="default">#FBB0E9</property>
    </view>
   </item>

   <item>
    <view class="vtkMRMLSliceNode" singletontag="Segmentation">
     <property name="orientation" action="default">Axial</property>
     <property name="viewlabel" action="default">Segmentation</property>
     <property name="viewcolor" action="default">#CC0099</property>
    </view>
   </item>

</layout>
"""

# out-of-the-blue values
LAYOUTID_SEGMENTATION_3D = 440
LAYOUTID_SEGMENTATION    = 442


# switch layout. 
def setLayout(idx):
    layoutManager = slicer.app.layoutManager()
    layoutManager.setLayout( idx )



# global variables to access our layout actions
actionSegmentation3D = None
actionSegmentation   = None


# callback for action
def triggerLayoutSegmentation():
    # (layout changed by 'LayoutMenu' by using the QAction's QVariant)
    # TODO: turn off 3D render
    pass

# callback for action
def triggerLayoutSegmentation3D():
    # (layout is changed by 'LayoutMenu' by using the QAction's QVariant)
    # TODO: turn on 3D render
    pass

# callback for shortcut
def toggleLayoutSegmentation():
    lm = slicer.app.layoutManager()
    if lm.layout == LAYOUTID_SEGMENTATION_3D:
        actionSegmentation.triggered()
    else: 
        actionSegmentation3D.triggered()

# custom QIcon from pixmap. create hex string with 'hexdump -e '/1 "%02X"' -v file.png'
def createIconSegmentation3D():
    pxm = qt.QPixmap()
    if pxm.loadFromData( qt.QByteArray.fromHex( '89504E470D0A1A0A0000000D4948445200000015000000150806000000A917A59600000006624B474400FF00FF00FFA0BDA793000000097048597300000B1300000B1301009A9C18000001094944415438CBB595DF6DC2301087BF33291B94ACD14A658F8091DA055C662A5EA03CE4CF1C158BA423F401F35012A52186D80DBF8758F29D3FDD9DEF1C11C11120E740E4BA4F02F075A801504A00011CCA73F2F9E9919FB2F602E7ABF4173A9BA976533ADF58253188872CF5DA44CED050E579EEB56D361AC51DD446FA6E56379D77B60C8302381CD656174EC6644840E5FF40ADAD3026BB70B2B61A95C920B40BE946195DD31069ADA7871EF8F0DA96B21D86C6A4EC8DD4986CD4EDBFB0F54F541F2AC8E02DF7DBA9288AF38BE590DEC3A3F59AA4D91BDBD80D0CE0ED5BF3B9C8DBF55FB32F22BCD6EB16DCD764B3DF8547439B7427EBD3A604FBB418B62915F68F3A1E41DDC8EF041FAC44375EE254D80000000049454E44AE426082' ) ):
        return qt.QIcon( pxm )
    else:
        raise ValueError("Hex string does not define a valid image file for QPixmap")

# custom QIcon from pixmap. create hex string with 'hexdump -e '/1 "%02X"' -v file.png'
def createIconSegmentation():
    pxm = qt.QPixmap()
    if pxm.loadFromData( qt.QByteArray.fromHex( '89504E470D0A1A0A0000000D4948445200000015000000150806000000A917A59600000006624B474400FF00FF00FFA0BDA793000000097048597300000B1300000B1301009A9C18000000A74944415438CBED94C10DC2300C45DF8FCA0A30097B20520936602636E0D0884558A48CC0A1E64290406AAD047AAB2FB97C3D7FDBB1256114841948D39A06E071ED5DD86AB7E1C6F9451ED76D75223043683A6F0550D048D075C915C71849C9D7B56D9CA7FC055A1EC77B7CBF92D0D736845F8000877E8F997D6CDC5FCACF09F23F2D865ED6C90557391D03CF32FD3CB0C63B63256ECDACAEA7CB46B983520865477A182038569EFBE62A8F2AF4B91D0000000049454E44AE426082' ) ):
        return qt.QIcon( pxm )
    else:
        raise ValueError("Hex string does not define a valid image file for QPixmap")

# show segmentation overlay on all views except "Segmentation-".
def setSegmentationDisplay2D():
    def callback(caller, event):
      segviewnode = getNode( "Segmentation-" ) # this is a singleton (look at its XML-definition above)
      viewnodes = getNodesByClass('vtkMRMLAbstractViewNode')
      viewnodes.remove( segviewnode ) 
      # set all ViewIDs except "Segmentation-"
      for node in getNodesByClass('vtkMRMLSegmentationDisplayNode'):
          # set all views except "Segmentation-", but only if the set of ViewIDs is undefined
          # by only doing this for undefineds, the user can override
          if not( node.GetViewNodeIDs() ):
             node.SetViewNodeIDs( list( map(lambda node: node.GetID(), viewnodes) ) )
    # observe new SegmentationDisplayNodes
    slicer.mrmlScene.AddObserver( slicer.mrmlScene.NodeAddedEvent, callback )

# make sure Segmentation and Segmentation- shows the same slice
def linkSegmentationViews():
    # linking SliceViews in Slicer are done by watching changes to any SliceNode or SliceCompositeNode and 
    # broadcast changes to the other SliceNodes or SliceCompositeNodes, see 'vtkMRMLSliceLinkLogic.cxx'.
    # what kind of changes for a source node to broadcast to other nodes can be controlled by the source node's InteractionFlags settings.
    # for some changes the orientation of source and target must match, for example scrolling an Axial view will only change views having Axial orientation.
    # however, broadcasts are only between SliceNodes of the same ViewGroup (and for SliceCompositeNode: using the corresponding SliceNode). 
    # ViewGroup is a property of AbstractView.
    # SliceCompositeNode: defining foreground/background/labelmap volume for a SliceNode
    # linking are done through SliceCompositeNode
    #
    # create our own ViewGroup for our views: NOTE: applies to crosshair too, hence commented out
    #slice0 = slicer.app.layoutManager().sliceWidget( "Segmentation" ).mrmlSliceNode()
    #slice1 = slicer.app.layoutManager().sliceWidget( "Segmentation-" ).mrmlSliceNode()
    #SEGMENTATION_VIEWGROUP = 73 # # # M A G I C # # #
    #slice0.SetViewGroup( SEGMENTATION_VIEWGROUP )
    #slice1.SetViewGroup( SEGMENTATION_VIEWGROUP )
    # link our views
    composite0 = slicer.app.layoutManager().sliceWidget( "Segmentation" ).mrmlSliceCompositeNode() 
    composite1 = slicer.app.layoutManager().sliceWidget( "Segmentation-" ).mrmlSliceCompositeNode() 
    composite0.SetLinkedControl( True )
    composite1.SetLinkedControl( True )
    composite0.SetHotLinkedControl( True )
    composite1.SetHotLinkedControl( True )

# create our custom layouts, add actions in layout menu, create shortcut
def createCustomLayouts():
    # create layouts
    slicer.app.layoutManager().layoutLogic().GetLayoutNode().AddLayoutDescription( LAYOUTID_SEGMENTATION_3D, LAYOUTXML_SEGMENTATION_3D )
    slicer.app.layoutManager().layoutLogic().GetLayoutNode().AddLayoutDescription( LAYOUTID_SEGMENTATION, LAYOUTXML_SEGMENTATION )
    # create menu entries
    global actionSegmentation3D
    global actionSegmentation
    actionSegmentation3D = mainWindow().findChild('QMenu', 'LayoutMenu').addAction( "Segmentation+3D" ) 
    actionSegmentation3D.setIcon( createIconSegmentation3D() )
    actionSegmentation3D.setData( LAYOUTID_SEGMENTATION_3D )
    actionSegmentation3D.setToolTip(" Segmentation")
    actionSegmentation3D.connect('triggered()', lambda: triggerLayoutSegmentation3D() )
    actionSegmentation = mainWindow().findChild('QMenu', 'LayoutMenu').addAction( "Segmentation" )
    actionSegmentation.setIcon( createIconSegmentation() )
    actionSegmentation.setData( LAYOUTID_SEGMENTATION );
    actionSegmentation.setToolTip(" Segmentation, fullscreen")
    actionSegmentation.connect('triggered()', lambda: triggerLayoutSegmentation() )
    # create toggle shortcut
    shortcutToggleSeg = qt.QShortcut( mainWindow() )
    shortcutToggleSeg.setKey( qt.QKeySequence('g') )
    shortcutToggleSeg.connect( 'activated()', lambda: toggleLayoutSegmentation() )
    # set custom layout right now. this makes sure volumes are loaded into our custom Slice Views
    actionSegmentation3D.triggered()
    # show segmentation overlay in all SliceViews except "Segmentation-"
    setSegmentationDisplay2D()
    # link Segmentation and Segmentation- so that they are synchronized
    linkSegmentationViews()



################################################################################
# crosshair

def setupCrosshair():
    # show (all) crosshair by default
    for cross in getNodesByClass( "vtkMRMLCrosshairNode" ):
        cross.SetCrosshairMode( slicer.vtkMRMLCrosshairNode.ShowBasic ) 
    # show intersection of other slices in a slice (useful in "Conventional" layout)
    for comp in getNodesByClass("vtkMRMLSliceCompositeNode"):
        comp.SetSliceIntersectionVisibility( True )

################################################################################
# init

def init():
    # no help text
    setModuleHelpSectionVisible( False )
    infoSlicerRC("Module help text hidden. Enable with 'setModuleHelpSectionVisible( True )'")
    # no dataprobe 
    setDataProbeVisible( False )
    infoSlicerRC("Data probe hidden. Enable with 'setDataProbeVisible( True )'")
    # no logo
    setApplicationLogoVisible( False )
    # no interpolation
    setVolumeInterpolation(False)
    infoSlicerRC("Volume interpolation off. Enable with 'setVolumeInterpolation( True )'")
    # default model format
    setModelStorageFormat( 'stl' )
    infoSlicerRC("Default model storage format: .stl")
    # create and set custom layout
    createCustomLayouts()
    infoSlicerRC("Custom layout created.")
    # create toggle 3D fullscreen 
    createToggle3D()
    # allow overlap by default. this makes sure segments inside a Segmentation can overlap
    setSegmentationOverwriteMode( slicer.vtkMRMLSegmentEditorNode.OverwriteNone )
    infoSlicerRC("Segmentation overwrite mode: allow overlap") 
    # setup crosshair
    setupCrosshair()
    # set default module: Data
    selectModule("Data")
    infoSlicerRC("Switched to module 'Data'")



# lets run
init()

