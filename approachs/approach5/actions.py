# encoding: utf-8

import gvsig
from gvsig import getResource

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
  
class QuickinfoExtension(ScriptingExtension):
  def __init__(self):
    pass

  def isVisible(self):
    return True

  def isLayerValid(self, layer):
    if layer == None:
      print "### QuickinfoExtension.isLayerValid: None, return False"
      return False
    fieldName = layer.getProperty("quickinfo.fieldname")
    print "### QuickinfoExtension.isLayerValid: %s, fieldname %s return %s" % (repr(layer.getName()),repr(fieldName), not (fieldName in ("", None)))
    if fieldName in ("", None):
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
      print "### QuickinfoExtension.execute(%s)" % repr(actionCommand)
      layer = currentLayer()
      if not self.isLayerValid(layer):
        return
      viewPanel = currentView().getWindowOfView()
      mapControl = viewPanel.getMapControl()
      quickInfo = QuickInfo()
      quickInfo.setTool(mapControl)

def selfRegister():
  application = ApplicationLocator.getManager()
  actionManager = PluginsLocator.getActionInfoManager()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()

  quickinfo_icon = File(getResource(__file__,"images","quickinfo.png")).toURI().toURL()
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
    "Show quick info"    # Tooltip
  )
  quickinfo_action = actionManager.registerAction(quickinfo_action)

  # Añadimos la entrada "Quickinfo" en el menu herramientas
  application.addMenu(quickinfo_action, "tools/Quickinfo")
  # Añadimos el la accion como un boton en la barra de herramientas "Quickinfo".
  application.addSelectableTool(quickinfo_action, "Quickinfo")

def main(*args):
  selfRegister()
  