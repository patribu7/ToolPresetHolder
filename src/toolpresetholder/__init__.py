from krita import Krita, DockWidgetFactory, DockWidgetFactoryBase
from .toolpresetholder import ToolPresetHolder, ToolPresetHolderDocker

Krita.instance().addExtension(ToolPresetHolder(Krita.instance()))
Krita.instance().addDockWidgetFactory(DockWidgetFactory("ToolPresetHolder", DockWidgetFactoryBase.DockLeft, ToolPresetHolderDocker))







# if __name__ == "__main__":
#     print("this is an scripter")


# else:

#     # add the extension to Krita's list of extensions:
#     Krita.instance().addExtension(ToolPresetsHolder(Krita.instance()))