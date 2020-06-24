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


# 3D view + manual segmentation views
LAYOUTXML_MANUALSEGMENTATION_3D = """
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

# manual segmentation views, fullscreen
LAYOUTXML_MANUALSEGMENTATION = """
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
LAYOUTID_MANUALSEGMENTATION_3D = 440
LAYOUTID_MANUALSEGMENTATION    = 442


# switch layout. 
def setLayout(idx):
    layoutManager = slicer.app.layoutManager()
    layoutManager.setLayout( idx )



# global variables to access our layout actions
actionSegmentation3D = None
actionSegmentation   = None


# callback for action
def triggerLayoutManualSegmentation():
    # (layout changed by 'LayoutMenu' by using the QAction's QVariant)
    # TODO: turn off 3D render
    pass

# callback for action
def triggerLayoutManualSegmentation3D():
    # (layout is changed by 'LayoutMenu' by using the QAction's QVariant)
    # TODO: turn on 3D render
    pass

# callback for shortcut
def toggleLayoutManualSegmentation():
    lm = slicer.app.layoutManager()
    if lm.layout == LAYOUTID_MANUALSEGMENTATION_3D:
        actionSegmentation.triggered()
    else: 
        actionSegmentation3D.triggered()


# create our custom layouts, add actions in layout menu, create shortcut
def createCustomLayouts():
    # create layouts
    slicer.app.layoutManager().layoutLogic().GetLayoutNode().AddLayoutDescription( LAYOUTID_MANUALSEGMENTATION_3D, LAYOUTXML_MANUALSEGMENTATION_3D )
    slicer.app.layoutManager().layoutLogic().GetLayoutNode().AddLayoutDescription( LAYOUTID_MANUALSEGMENTATION, LAYOUTXML_MANUALSEGMENTATION )
    # create menu entries
    global actionSegmentation3D
    global actionSegmentation
    actionSegmentation3D = mainWindow().findChild('QMenu', 'LayoutMenu').addAction( "Segmentation+3D" ) # TODO: create Icon: #.setIcon(qt.QIcon(':Icons/Go.png'))
    actionSegmentation3D.setData( LAYOUTID_MANUALSEGMENTATION_3D );
    actionSegmentation3D.setToolTip("Manual Segmentation")
    actionSegmentation3D.connect('triggered()', lambda: triggerLayoutManualSegmentation3D() )
    actionSegmentation = mainWindow().findChild('QMenu', 'LayoutMenu').addAction( "Segmentation" ) # TODO: create Icon: #.setIcon(qt.QIcon(':Icons/Go.png'))
    actionSegmentation.setData( LAYOUTID_MANUALSEGMENTATION );
    actionSegmentation.setToolTip("Manual Segmentation, fullscreen")
    actionSegmentation.connect('triggered()', lambda: triggerLayoutManualSegmentation() )
    # create toggle shortcut
    shortcutToggleSeg = qt.QShortcut( mainWindow() )
    shortcutToggleSeg.setKey( qt.QKeySequence('g') )
    shortcutToggleSeg.connect( 'activated()', lambda: toggleLayoutManualSegmentation() )
    # set custom layout right now. this makes sure volumes are loaded into our custom Slice Views
    actionSegmentation3D.triggered()




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
    infoSlicerRC("Volume interpolation off. Enable with 'setVolumeInterpolation( True )")
    # default model format
    setModelStorageFormat( 'stl' )
    infoSlicerRC("Default model storage format: .stl")
    # create and set custom layout
    createCustomLayouts()
    infoSlicerRC("Custom layout created.")
    # create toggle 3D fullscreen 
    createToggle3D()
    # set default module: Data
    selectModule("Data")
    infoSlicerRC("Switched to module 'Data'")



# lets run
init()

