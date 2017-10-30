# encoding: utf-8

import gvsig
from gvsig import getResource
from gvsig.libs.formpanel import FormPanel

from org.gvsig.tools.swing.api import ToolsSwingLocator

class QuickinfoPanel(FormPanel):
  def __init__(self, layer=None):
    FormPanel.__init__(self,getResource(__file__,"quickinfopanel.xml"))
    self.setLayer(layer)

  def setLayer(self, layer):
    self.__layer = layer
    if layer==None:
      self.cboFields.removeAllItems()
    else:
      self.fillCombo(
        self.cboFields, 
        self.__layer.getFeatureStore().getDefaultFeatureType()
      )

  def getLayer(self):
    return self.__layer

  def getFieldName(self):
    name = self.cboFields.getSelectedItem()
    if name == None:
      return None
    name = name.strip()
    if name == "":
      return None
    return name
    
  def fillCombo(self, combo, featureType):
    combo.removeAllItems()
    combo.addItem(" ")
    for attr in featureType:
      combo.addItem(attr.getName())
    x = self.__layer.getProperty("quickinfo.fieldname")
    if x in ("", None):
      combo.setSelectedIndex(0)
    else:
      combo.setSelectedItem(x)

  def save(self):
    self.__layer.setProperty(
      "quickinfo.fieldname",
      self.getFieldName()
    )
    
  
def main(*args):
  viewDoc = gvsig.currentView()
  layer = viewDoc.getLayer("manzanas_pob")
  panel = QuickinfoPanel(layer)

  winmgr = ToolsSwingLocator.getWindowManager();
  dialog = winmgr.createDialog(
    panel.asJComponent(),
    "Quickinfo test",
    "Quickinfo information",
    winmgr.BUTTONS_OK_CANCEL
  )
  dialog.show(winmgr.MODE.DIALOG)
  if dialog.getAction()==winmgr.BUTTON_OK:
    print "Ok"
    print "Show field: ", repr(panel.getFieldName())
  else:
    print "Cancel"
  