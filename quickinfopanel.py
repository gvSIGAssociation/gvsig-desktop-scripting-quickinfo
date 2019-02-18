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

from org.gvsig.tools.evaluator import EvaluatorException

     
  
class QuickinfoPanel(FormPanel):
  def __init__(self, layer=None):
    FormPanel.__init__(self,getResource(__file__,"quickinfopanel.xml"))
    i18n = ToolsSwingLocator.getToolsSwingManager()
    i18n.translate(self.rdoUseField)
    i18n.translate(self.lblSelectField)
    i18n.translate(self.rdoUseExpression)
    i18n.translate(self.lblFields)
    i18n.translate(self.btnTest)
    
    self.btgMode = ButtonGroup()
    self.btgMode.add(self.rdoUseField)
    self.btgMode.add(self.rdoUseExpression)
    self.setLayer(layer)
    
  def setLayer(self, layer):
    self.__layer = layer
    if layer==None:
      self.cboFields.removeAllItems()
      self.lstFields.setModel(DefaultListModel())
      self.txtExpression.setText("")
      self.rdoUseField.setSelected(True)
    else:
      featureType = self.__layer.getFeatureStore().getDefaultFeatureType()
      self.fillCombo( self.cboFields, featureType )
      self.lstFields.setModel(self.getListModel(featureType))
      s = self.__layer.getProperty("quickinfo.expression")
      if s == None:
        s = ""
      self.txtExpression.setText(s)
      if self.__layer.getProperty("quickinfo.mode") == "useField":
        self.rdoUseField.setSelected(True)
      else:
        self.rdoUseExpression.setSelected(True)
      
  def getListModel(self, featureType):
    model = DefaultListModel()
    for attr in featureType:
      model.addElement(attr.getName())
    return model
    
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
    return self.txtExpression.getText()

  def getMode(self):
    if self.rdoUseField.isSelected():
      return "useField"
    else:
      return "useExpression"

  def lstFields_mouseClick(self, e):
    if e.getClickCount()==2 and e.getID() == MouseEvent.MOUSE_CLICKED:
      x = self.lstFields.getSelectedValue()
      self.txtExpression.replaceSelection(x+" ")
      self.txtExpression.requestFocusInWindow()
      
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
      self.getExpression()
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
      self.lstFields.setEnabled(False)
      self.txtExpression.setEnabled(False)
      self.btnTest.setEnabled(False)
    else:
      self.cboFields.setEnabled(False)
      self.lstFields.setEnabled(True)
      self.txtExpression.setEnabled(True)
      self.btnTest.setEnabled(True)
    
  def btnTest_click(self, *args):
    i18n = ToolsLocator.getI18nManager()

    defaultValues = dict()
    defaultValues[DataTypes.BOOLEAN] = True
    defaultValues[DataTypes.BYTE] = 0
    defaultValues[DataTypes.CHAR] = 0
    defaultValues[DataTypes.INT] = 0
    defaultValues[DataTypes.LONG] = 0
    defaultValues[DataTypes.FLOAT] = Float(0.0)
    defaultValues[DataTypes.DOUBLE] = Double(0.0)
    defaultValues[DataTypes.STRING] = ""
    defaultValues[DataTypes.DATE] = Date()
    defaultValues[DataTypes.TIME] = Date()
    defaultValues[DataTypes.FILE] = File(getResource(__file__))
    defaultValues[DataTypes.FOLDER] = File(getResource(__file__)).getParentFile()
    defaultValues[DataTypes.URL] = URL("http://acme.com")
    defaultValues[DataTypes.URI] = URI("http://acme.com")
    defaultValues[DataTypes.VERSION] = ToolsLocator.getPackageManager().createVersion("1.0.0")
    defaultValues[DataTypes.BIGDECIMAL] = BigDecimal(0)

    values = dict()
    featureType = self.__layer.getFeatureStore().getDefaultFeatureType()
    for attr in featureType:
      values[attr.getName()] = defaultValues.get(attr.getType(),None)
    try:
      expression = self.getExpression().replace("\n"," ")
      x = eval(expression,globals(),values)
      #print "x = ", x
      gvsig.commonsdialog.msgbox(i18n.getTranslation("_Correct_expression"))
    except Exception,ex:
      gvsig.commonsdialog.msgbox(i18n.getTranslation("_Errors_have_occurred_checking_the_expression") + "\n\n" + str(ex))
    except :
      gvsig.commonsdialog.msgbox(i18n.getTranslation("_Errors_have_occurred_checking_the_expression") + "\n\n")
    
    
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
  dialog.show(winmgr.MODE.DIALOG)
  if dialog.getAction()==winmgr.BUTTON_OK:
    panel.save()
    print "Ok"
    print "Show field: ", repr(panel.getFieldName())
  else:
    print "Cancel"
  
