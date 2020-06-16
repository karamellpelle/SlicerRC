# Python commands in this file are executed on Slicer startup

# Examples:
#
# Load a scene file
# slicer.util.loadScene('c:/Users/SomeUser/Documents/SlicerScenes/SomeScene.mrb')
#
# Open a module (overrides default startup module in application settings / modules)
# slicer.util.mainWindow().moduleSelector().selectModule('SegmentEditor')
#

#set the default model save format to stl (from vtk)
defaultModelStorageNode = slicer.vtkMRMLModelStorageNode()
defaultModelStorageNode.SetUseCompression(0)
defaultModelStorageNode.SetDefaultWriteFileExtension('stl')
slicer.mrmlScene.AddDefaultNode(defaultModelStorageNode)

#disable interpolation of the volumes by default
#def NoInterpolate(caller,event):
#  for node in slicer.util.getNodes('*').values():
#    if node.IsA('vtkMRMLScalarVolumeDisplayNode'):
#      node.SetInterpolate(0)
#slicer.mrmlScene.AddObserver(slicer.mrmlScene.NodeAddedEvent, NoInterpolate)

#hide SLicer logo in module tab
slicer.util.findChild(slicer.util.mainWindow(), 'LogoLabel').visible = False

#collapse Data Probe tab by default to save space modules tab
slicer.util.findChild(slicer.util.mainWindow(), name='DataProbeCollapsibleWidget').collapsed = True

################################################################################
# toggle 3D fullscreen

prevLayout = slicer.vtkMRMLLayoutNode.SlicerLayoutDefaultView

def toggle3DFullscreen():
    global prevLayout
    lm = slicer.app.layoutManager()
    if lm.layout == slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView:
        lm.setLayout( prevLayout )
    else:
        prevLayout = lm.layout
        lm.setLayout( slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView )


# create GUI button
widget = mainWindow().findChild('QToolBar', 'ViewToolBar')
action = widget.addAction("Toggle 3D") 
action.setToolTip('Toggle 3D Fullscreen')
action.connect('triggered()', lambda: toggle3DFullscreen() )


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

# out of the blue
LAYOUTID_MANUALSEGMENTATION_3D  = 440
LAYOUTID_MANUALSEGMENTATION = 442


def setLayout(idx):
    layoutManager = slicer.app.layoutManager()
    layoutManager.setLayout( idx )


#viewToolBar = mainWindow().findChild('QToolBar', 'ViewToolBar')
#layoutMenu = viewToolBar.widgetForAction(viewToolBar.actions()[0]).menu()
#layoutSwitchActionParent = layoutMenu  # use `layoutMenu` to add inside layout list, use `viewToolBar` to add next the standard layout list
#layoutSwitchAction = layoutSwitchActionParent.addAction("My view") # add inside layout list
#layoutSwitchAction.setData(layoutId)
#layoutSwitchAction.setIcon(qt.QIcon(':Icons/Go.png'))
#layoutSwitchAction.setToolTip('3D and slice view')
#layoutSwitchAction.connect('triggered()', lambda layoutId = customLayoutId: slicer.app.layoutManager().setLayout(layoutId))


################################################################################
# toggle segmentation fullscreen

prevLayoutSeg = LAYOUTID_MANUALSEGMENTATION_3D

# jump to fullscreen segmentation (axial)
def toggleSegmentationFullscreen():
    global prevLayoutSeg
    lm = slicer.app.layoutManager()
    if lm.layout == LAYOUTID_MANUALSEGMENTATION:
        lm.setLayout( prevLayoutSeg )
    else:
        prevLayoutSeg = lm.layout
        lm.setLayout( LAYOUTID_MANUALSEGMENTATION )

# also add a GUI button for this
widget = mainWindow().findChild('QToolBar', 'ViewToolBar')
action = widget.addAction("Toggle manual segmentation") 
action.setToolTip('Toggle segmentation view')
action.connect('triggered()', lambda: toggleSegmentationFullscreen() )

################################################################################


# create layout: seg+3D 
def createLayoutSeg():
    # add layout
    slicer.app.layoutManager().layoutLogic().GetLayoutNode().AddLayoutDescription( LAYOUTID_MANUALSEGMENTATION_3D, LAYOUTXML_MANUALSEGMENTATION_3D )
    # create menu entry for layout
    viewMenu = mainWindow().findChild('QToolBar', 'ViewToolBar')
    widget = viewMenu.widgetForAction( viewMenu.actions()[0] ).menu()
    action = widget.addAction("Segmentation") 
    action.setToolTip('Layout for manual segmentation')
    action.connect('triggered()', lambda layoutId = LAYOUTID_MANUALSEGMENTATION_3D: slicer.app.layoutManager().setLayout( layoutId) )

def createLayoutSegAxial():
    # add layout
    slicer.app.layoutManager().layoutLogic().GetLayoutNode().AddLayoutDescription( LAYOUTID_MANUALSEGMENTATION, LAYOUTXML_MANUALSEGMENTATION )
    # create menu entry for layout
    # FIXME: for some reason, this crashes the whole application. i guess it has something to do with the 'createLayoutSeg()' above
    #viewMenu = mainWindow().findChild('QToolBar', 'ViewToolBar')
    #widget = viewMenu.widgetForAction( viewMenu.actions()[0] ).menu()
    #action = widget.addAction("Axial Segmentation") 
    #action.setToolTip('Axial Segmentation (fullscreen)')
    #action.connect('triggered()', lambda layoutId = LAYOUTID_MANUALSEGMENTATION: slicer.app.layoutManager().setLayout( layoutId) )
    #action.connect('triggered()', lambda layoutId = LAYOUTID_MANUALSEGMENTATION: print('hello') )



################################################################################
# shortcuts keyboard keys

# custom shortcuts
def createShortcuts():
    # create shortcut: g for segmentation fullscreen
    shortcutToggleSeg = qt.QShortcut( slicer.util.mainWindow() )
    shortcutToggleSeg.setKey( qt.QKeySequence('g') )
    shortcutToggleSeg.connect( 'activated()', toggleSegmentationFullscreen )

    # create shortcut: f for 3D fullscreen
    shortcutToggle3D = qt.QShortcut( slicer.util.mainWindow() )
    shortcutToggle3D.setKey( qt.QKeySequence('f') )
    shortcutToggle3D.connect( 'activated()', toggle3DFullscreen )




################################################################################
# init

createLayoutSeg()
createLayoutSegAxial()
createShortcuts()
