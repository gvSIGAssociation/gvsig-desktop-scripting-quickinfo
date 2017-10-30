# encoding: utf-8

import gvsig

import os.path

from os.path import join, dirname

from gvsig import currentView
from gvsig import currentLayer

from java.io import File

from org.gvsig.app import ApplicationLocator
from org.gvsig.andami import PluginsLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools.swing.api import ToolsSwingLocator

from quickinfo import QuickInfo
  
from org.gvsig.tools import ToolsLocator

class QuickinfoExtension(ScriptingExtension):
  def __init__(self):
    pass

  def isVisible(self):
    return True

  def isLayerValid(self, layer):
    if layer == None:
      #print "### QuickinfoExtension.isLayerValid: None, return False"
      return False
    mode = layer.getProperty("quickinfo.mode")
    if mode in ("", None):
      # Si la capa no tiene configurado el campo a mostrar
      # no activamos la herramienta
      return False
    return True
    
  def isEnabled(self):
    layer = currentLayer()
    if not self.isLayerValid(layer):
      return False
    return True

  def execute(self,actionCommand, *args):
    actionCommand = actionCommand.lower()
    if actionCommand == "settool-quickinfo":
      #print "### QuickinfoExtension.execute(%s)" % repr(actionCommand)
      layer = currentLayer()
      if not self.isLayerValid(layer):
        return
      viewPanel = currentView().getWindowOfView()
      mapControl = viewPanel.getMapControl()
      quickInfo = QuickInfo()
      quickInfo.setTool(mapControl)

def selfRegister():
  i18n = ToolsLocator.getI18nManager()
  application = ApplicationLocator.getManager()
  actionManager = PluginsLocator.getActionInfoManager()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()

  quickinfo_icon = File(join(dirname(__file__),"images","quickinfo.png")).toURI().toURL()
  iconTheme.registerDefault("scripting.quickinfo", "action", "tools-quickinfo", None, quickinfo_icon)

  quickinfo_extension = QuickinfoExtension()
  quickinfo_action = actionManager.createAction(
    quickinfo_extension,
    "tools-quickinfo",   # Action name
    "Show quick info",   # Text
    "settool-quickinfo", # Action command
    "tools-quickinfo",   # Icon name
    None,                # Accelerator
    1009000000,          # Position
    i18n.getTranslation("_Show_quick_info")    # Tooltip
  )
  quickinfo_action = actionManager.registerAction(quickinfo_action)

  # Añadimos la entrada "Quickinfo" en el menu herramientas
  application.addMenu(quickinfo_action, "tools/_Quickinfo")
  # Añadimos el la accion como un boton en la barra de herramientas "Quickinfo".
  application.addSelectableTool(quickinfo_action, "Quickinfo")

def main(*args):
  selfRegister()
  