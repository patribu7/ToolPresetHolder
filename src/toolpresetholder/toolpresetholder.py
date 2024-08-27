from krita import Krita, Extension, DockWidget
from PyQt5.QtWidgets import QWidget, QRadioButton, QVBoxLayout, QMessageBox

appNotifier  = Krita.instance().notifier()
appNotifier.setActive(True)

presets = Krita.instance().resources('preset')


class ToolPresetHolder(Extension):

    def __init__(self, parent):
        super().__init__(parent)

        self.is_ready = False
        appNotifier.setActive(True)
        appNotifier.windowCreated.connect(self.enableFunc) #non funziona su setup
        appNotifier.viewClosed.connect(self.registerPreset)

        self.currentTool = "brush"
        self.tools = {
            "brush": {
                "current_preset": presets["Fill circle"],
                "valid_list": []
            },
            
            "eraser": {
                 "current_preset": presets["a) Eraser Circle"],
                 "valid_list": []
            },
            
            "blender": {
                "current_preset": presets["k) Blender Basic"],
                "valid_list": []
            },

            "adjust_light": {
                "current_preset": presets["l) Adjust Dodge"],
                "valid_list": []
            },

            "clone": {
                "current_preset": presets["v) Clone Tool"],
                "valid_list": []
            },

            "distort": {
                "current_preset": presets["v) Distort Move"],
                "valid_list": []
        }
        }

        self.setValidPresetDefault()
       

    def setup(self):
        pass
            


    def createActions(self, window):
        select_brush = window.createAction('tph_select_brush', 'brush', "tools/script")
        select_brush.triggered.connect(self.setBrushTool)
        
        select_eraser = window.createAction('tph_select_eraser', 'eraser', "tools/script")
        select_eraser.triggered.connect(self.setEraserTool)

        select_blender = window.createAction('tph_select_blender', 'blender', "tools/script")
        select_blender.triggered.connect(self.setBlenderTool)

        select_adjust_light = window.createAction('tph_select_adjust_light', 'adjust_light', "tools/script")
        select_adjust_light.triggered.connect(self.setAdjustTool)

        select_clone = window.createAction('tph_select_clone', 'clone', "tools/script")
        select_clone.triggered.connect(self.setCloneTool)

        select_distort = window.createAction('tph_select_distort', 'distort', "tools/script")
        select_distort.triggered.connect(self.setDistortTool)
  

    def registerPreset(self):
        if self.is_ready:
           
           if self.view().currentBrushPreset().name() in self.tools[self.currentTool]["valid_list"]:
               self.tools[self.currentTool]["current_preset"] = self.view().currentBrushPreset()


    def setBrushTool(self):
        Krita.instance().action("KritaShape/KisToolBrush").trigger()
        self.registerPreset()

        self.view().setCurrentBrushPreset(self.tools["brush"]["current_preset"])
        self.view().setCurrentBlendingMode("normal")
        self.changeTool("brush")
            

    def setEraserTool(self):
        Krita.instance().action("KritaShape/KisToolBrush").trigger()
        self.registerPreset()

        self.view().setCurrentBrushPreset(self.tools["eraser"]["current_preset"])
        self.view().setCurrentBlendingMode("erase")
        self.changeTool("eraser")


    def setBlenderTool(self):
        Krita.instance().action("KritaShape/KisToolBrush").trigger()
        self.registerPreset()

        self.view().setCurrentBrushPreset(self.tools["blender"]["current_preset"])
        self.view().setCurrentBlendingMode("normal")
        self.changeTool("blender")


    def setAdjustTool(self):
        Krita.instance().action("KritaShape/KisToolBrush").trigger()
        self.registerPreset()

        self.view().setCurrentBrushPreset(self.tools["adjust_light"]["current_preset"])
        self.changeTool("adjust_light")


    def setCloneTool(self):
        Krita.instance().action("KritaShape/KisToolBrush").trigger()
        self.registerPreset()

        self.view().setCurrentBrushPreset(self.tools["clone"]["current_preset"])
        self.view().setCurrentBlendingMode("normal")
        self.changeTool("clone")


    def setDistortTool(self):
        Krita.instance().action("KritaShape/KisToolBrush").trigger()
        self.registerPreset()

        self.view().setCurrentBrushPreset(self.tools["distort"]["current_preset"])
        self.changeTool("distort")
    

    def isPresetType(self, preset_name, type):
        return preset_name.lower().find(type.lower()) >= 0
    

    def setValidPresetDefault(self):
        for key in presets:
            if self.isPresetType(presets[key].name(), "blender") or self.isPresetType(presets[key].name(), "smudge"):
                self.tools["blender"]["valid_list"].append(presets[key].name())

            elif self.isPresetType(presets[key].name(), "adjust"):
                self.tools["adjust_light"]["valid_list"].append(presets[key].name())
            
            elif self.isPresetType(presets[key].name(), "clone"):
                self.tools["clone"]["valid_list"].append(presets[key].name())

            elif self.isPresetType(presets[key].name(), "distort"):
                self.tools["distort"]["valid_list"].append(presets[key].name())

            else:
                self.tools["brush"]["valid_list"].append(presets[key].name())
                self.tools["eraser"]["valid_list"].append(presets[key].name())


    def changeTool(self, new_tool):
        self.currentTool = new_tool
        self.toolChangedEmit(new_tool)


    def toolChangedEmit(self, new_tool):
       self.docker.toggleRadioButton(new_tool)


    def view(self):
        return Krita.instance().activeWindow().activeView() 


    def enableFunc(self):
        for docker in Krita.instance().dockers():
            if docker.objectName() == "ToolPresetHolder":
                self.docker = docker
        
        self.is_ready = True


class ToolPresetHolderDocker(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tool Preset Holder")        

        #main widget
        mainWidget = QWidget(self)
        self.setWidget(mainWidget)

        #set button brush
        buttonBrush = QRadioButton("Brush", mainWidget)
        buttonBrush.setDisabled(True)
  
        buttonBrush.toggle()
        
        #set button eraser
        buttonEraser = QRadioButton("Eraser", mainWidget)
        buttonEraser.setDisabled(True) 
        
        #set button blender
        buttonBlender = QRadioButton("Blender", mainWidget)
        buttonBlender.setDisabled(True)
                
        #set button adjust_light
        buttonAdjust = QRadioButton("Adjust Light", mainWidget)
        buttonAdjust.setDisabled(True)
        
        #set button clone
        buttonClone = QRadioButton("Clone", mainWidget)
        buttonClone.setDisabled(True)
                
        #set button distort
        buttonDistort = QRadioButton("Distort", mainWidget)
        buttonDistort.setDisabled(True)
        
        #layout button
        mainWidget.setLayout(QVBoxLayout())
        mainWidget.layout().addWidget(buttonBrush)
        mainWidget.layout().addWidget(buttonEraser)
        mainWidget.layout().addWidget(buttonBlender)
        mainWidget.layout().addWidget(buttonAdjust)
        mainWidget.layout().addWidget(buttonClone)
        mainWidget.layout().addWidget(buttonDistort)
        
        self.buttons = {
            "brush": buttonBrush,
            "eraser": buttonEraser,
            "blender": buttonBlender,
            "adjust_light": buttonAdjust,
            "clone": buttonClone,
            "distort": buttonDistort
            }

 
    def toggleRadioButton(self, new_tool):
        self.buttons[new_tool].toggle()


    def canvasChanged(self, canvas):
        pass


def success(message):
    QMessageBox.information(QWidget(), i18n("Warnning"), i18n(message))

btn_style = """
    QRadioButton {
        background-color: #f0f0f0;
        border: 1px solid #b4b4b4;
        border-radius: 5px;
        padding: 5px;
    }
    QRadioButton::indicator {
        display: none;
    }
    QRadioButton:checked {
        background-color: #d0d0d0;
    }
"""