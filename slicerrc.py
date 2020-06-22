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
        layoutPrev # FIXME: global? no, according to https://stackoverflow.com/a/279586
        if lm.layout == layout3D:
            lm.setLayout( layoutPrev )
        else:
            layoutPrev = lm.layout
            lm.setLayout( layout3D )
    # create GUI button
    widget = mainWindow().findChild('QToolBar', 'ViewToolBar')
    action = widget.addAction("3D") 
    action.setToolTip('Toggle 3D Fullscreen')
    action.connect('triggered()', lambda: toggle3DFullscreen() )
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
    <view class="vtkMRMLSliceNode" singletontag="ManualSegmentation-">
     <property name="orientation" action="default">Axial</property>
     <property name="viewlabel" action="default">ManualSegmentation-</property>
     <property name="viewcolor" action="default">#FF99E6</property>
    </view>
   </item>

   <item>
    <view class="vtkMRMLSliceNode" singletontag="ManualSegmentation">
     <property name="orientation" action="default">Axial</property>
     <property name="viewlabel" action="default">ManualSegmentation</property>
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
    <view class="vtkMRMLSliceNode" singletontag="ManualSegmentation-">
     <property name="orientation" action="default">Axial</property>
     <property name="viewlabel" action="default">ManualSegmentation-</property>
     <property name="viewcolor" action="default">#FF99E6</property>
    </view>
   </item>

   <item>
    <view class="vtkMRMLSliceNode" singletontag="ManualSegmentation">
     <property name="orientation" action="default">Axial</property>
     <property name="viewlabel" action="default">ManualSegmentation</property>
     <property name="viewcolor" action="default">#CC0099</property>
    </view>
   </item>

</layout>
"""

# out-of-the-blue values
LAYOUTID_MANUALSEGMENTATION_3D = 440
LAYOUTID_MANUALSEGMENTATION    = 442


# switch layout
def setLayout(idx):
    layoutManager = slicer.app.layoutManager()
    layoutManager.setLayout( idx )



# global variables to access our layout actions
actionSegmentation3D = None
actionSegmentation   = None


# callback for action
def triggerLayoutManualSegmentation():
    # set layout
    setLayout( LAYOUTID_MANUALSEGMENTATION )
    # TODO: turn off 3D render

# callback for action
def triggerLayoutManualSegmentation3D():
    # set layout
    setLayout( LAYOUTID_MANUALSEGMENTATION_3D )
    # TODO: turn on 3D render

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
    actionSegmentation3D.setToolTip("Manual Segmentation")
    actionSegmentation3D.connect('triggered()', lambda: triggerLayoutManualSegmentation3D() )
    actionSegmentation = mainWindow().findChild('QMenu', 'LayoutMenu').addAction( "Segmentation" ) # TODO: create Icon: #.setIcon(qt.QIcon(':Icons/Go.png'))
    actionSegmentation.setToolTip("Manual Segmentation, fullscreen")
    actionSegmentation.connect('triggered()', lambda: triggerLayoutManualSegmentation() )
    # create toggle shortcut
    shortcutToggleSeg = qt.QShortcut( mainWindow() )
    shortcutToggleSeg.setKey( qt.QKeySequence('g') )
    shortcutToggleSeg.connect( 'activated()', lambda: toggleLayoutManualSegmentation() )
    # set custom layout right now. this makes sure volumes are loaded into our custom Slice Views
    #actionSegmentation3D.triggered()




################################################################################
# init

def init():
    # no interpolation
    setVolumeInterpolation(False)
    infoSlicerRC("Volume interpolation off. enable with 'setVolumeInterpolation( True )")
    # default model format
    setModelStorageFormat( 'stl' )
    infoSlicerRC("Default model storage format: .stl")
    # no dataprobe 
    setDataProbeVisible( False )
    infoSlicerRC("Data probe hidden. enable with 'setDataProbeVisible( True )'")
    # no logo
    setApplicationLogoVisible( False )
    # create and set custom layout
    createCustomLayouts()
    # create toggle 3D fullscreen 
    createToggle3D()
    infoSlicerRC("Custom layout created.")
    # set default module: Data
    selectModule("Data")
    infoSlicerRC("Switched to module 'Data'")



# lets run
init()

