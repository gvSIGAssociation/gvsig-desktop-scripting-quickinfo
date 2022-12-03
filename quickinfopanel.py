# encoding: utf-8

import gvsig
from gvsig import getResource
from gvsig.libs.formpanel import FormPanel

from org.gvsig.tools.swing.api import ToolsSwingLocator
from javax.swing import DefaultListModel
from java.awt.event import MouseEvent
from javax.swing import ButtonGroup

import sys

from org.gvsig.fmap.dal import DALLocator
from org.gvsig.tools.evaluator import EvaluatorData

from java.lang import Double
from java.net import URI
from org.gvsig.tools import ToolsLocator
from java.util import Date
from java.net import URL
from java.math import BigDecimal
from java.lang import Float
from java.io import File
from org.gvsig.tools.dataTypes import DataTypes
from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR
from org.gvsig.tools.evaluator import EvaluatorException
from org.gvsig.expressionevaluator.swing import ExpressionEvaluatorSwingLocator
from org.gvsig.expressionevaluator import ExpressionUtils
     
from org.gvsig.fmap.dal.swing import DALSwingLocator
from org.gvsig.tools.dataTypes import DataTypeUtils
from org.gvsig.expressionevaluator import ExpressionUtils

class QuickinfoPanel(FormPanel):
  def __init__(self, layer=None):
    FormPanel.__init__(self,getResource(__file__,"quickinfopanel.xml"))
    i18n = ToolsSwingLocator.getToolsSwingManager()
    i18n.translate(self.rdoUseField)
    i18n.translate(self.lblSelectField)
    i18n.translate(self.rdoUseExpression)
    i18n.translate(self.chbActivate)
    
    self.btgMode = ButtonGroup()
    self.btgMode.add(self.rdoUseField)
    self.btgMode.add(self.rdoUseExpression)
    
    ## Picker
    self.store = layer.getFeatureStore()
    self.expPicker = ExpressionEvaluatorSwingLocator.getManager().createExpressionPickerController(self.txtExp, self.btnExp)
    self.expFilterStore = DALSwingLocator.getSwingManager().createFeatureStoreElement(self.store)
    self.expPicker.getConfig().addElement(self.expFilterStore)
    
    
    self.rdoUseField.setSelected(True)
    self.cboFields.setEnabled(True)
    self.expPicker.setEnabled(False)
    self.setLayer(layer)
    
  def setLayer(self, layer):
    self.__layer = layer
    if layer==None:
      self.cboFields.removeAllItems()
      self.txtExpression.setText("")
      self.rdoUseField.setSelected(True)
    else:
      featureType = self.__layer.getFeatureStore().getDefaultFeatureType()
      self.fillCombo( self.cboFields, featureType )
      s = ExpressionUtils.createExpression(self.__layer.getProperty("quickinfo.expression"))
      self.expPicker.set(s)
      if self.__layer.getProperty("quickinfo.active") != None:
        self.chbActivate.setSelected(DataTypeUtils.toBoolean(self.__layer.getProperty("quickinfo.active")))

      if self.__layer.getProperty("quickinfo.mode") == "useField":
        self.rdoUseField.setSelected(True)
        self.rdoUseField.setSelected(True)
        self.cboFields.setEnabled(True)
        self.expPicker.setEnabled(False)
      elif self.__layer.getProperty("quickinfo.mode") == "useExpression":
        self.rdoUseExpression.setSelected(True)
      else:
        self.rdoUseField.setSelected(True)
      
  #def getListModel(self, featureType):
  #  model = DefaultListModel()
  #  for attr in featureType:
  #    model.addElement(attr.getName())
  #  return model
    
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

  def getExpression(self):
    return self.expPicker.get()
    
  def getMode(self):
    if self.rdoUseField.isSelected():
      return "useField"
    else:
      return "useExpression"
      
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
    self.__layer.setProperty(
      "quickinfo.expression",
      ExpressionUtils.getPhrase(self.getExpression())
    )
    self.__layer.setProperty(
      "quickinfo.active",
      self.chbActivate.isSelected()
      )
    if self.rdoUseField.isSelected():
      self.__layer.setProperty(
        "quickinfo.mode",
        "useField"
      )
    else:
      self.__layer.setProperty(
        "quickinfo.mode",
        "useExpression"
      )

  def rdoUseField_change(self, *args):
    if self.rdoUseField.isSelected():
      self.cboFields.setEnabled(True)
      self.expPicker.setEnabled(False)
    else:
      self.cboFields.setEnabled(False)
      self.expPicker.setEnabled(True)
    
def main(*args):
  viewDoc = gvsig.currentView()
  layer = gvsig.currentLayer() # viewDoc.getLayer("manzanas_pob")
  panel = QuickinfoPanel(layer)
  panel.setPreferredSize(400,300)

  winmgr = ToolsSwingLocator.getWindowManager()
  dialog = winmgr.createDialog(
    panel.asJComponent(),
    "Quickinfo test",
    "Quickinfo information",
    winmgr.BUTTONS_OK_CANCEL
  )
  dialog.show(winmgr.MODE.WINDOW)
  if dialog.getAction()==winmgr.BUTTON_OK:
    panel.save()
    print "Ok"
    print "Show field: ", repr(panel.getFieldName())
  else:
    print "Cancel"
  
