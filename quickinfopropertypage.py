# encoding: utf-8

import gvsig

from org.gvsig.propertypage import PropertiesPage
from org.gvsig.fmap.mapcontext.layers.vectorial import VectorLayer
from org.gvsig.app.project.documents.view import ViewDocument
from org.gvsig.propertypage import PropertiesPageFactory
from org.gvsig.fmap.mapcontrol import MapControlLocator

from addons.quickinfo.quickinfopanel import QuickinfoPanel

from org.gvsig.tools import ToolsLocator

class QuickinfoPropertyPage(PropertiesPage):

  def __init__(self, layer=None):
    self.__panel = QuickinfoPanel(layer)
      
  def getTitle(self):
    i18n = ToolsLocator.getI18nManager()
    return i18n.getTranslation("_Quickinfo")

  def asJComponent(self):
    return self.__panel.asJComponent()
  
  def getPriority(self):
    return 1

  def whenAccept(self):
    self.__panel.save()
    return True

  def whenApply(self):
    return self.whenAccept()

  def whenCancel(self):
    return True

class QuickinfoPropertyPageFactory(PropertiesPageFactory):

  def __init__(self):
    pass

  def getName(self):
    return "Quickinfo"
    
  def getGroupID(self):
    return ViewDocument.LAYER_PROPERTIES_PAGE_GROUP
    
  def isVisible(self, layer):
    if isinstance(layer,VectorLayer):
      return True
    return False
    
  def create(self, object1, layer):
    if not isinstance(layer,VectorLayer):
      return None
    return QuickinfoPropertyPage(layer)

def selfRegister():
  propertiesPageManager = MapControlLocator.getPropertiesPageManager()
  propertiesPageManager.registerFactory(QuickinfoPropertyPageFactory())
  
  dynObjectManager = ToolsLocator.getDynObjectManager()
  dynObjectManager.registerTag("Layer.quickinfo.active", "Values are true or false.")
  dynObjectManager.registerTag("Layer.quickinfo.mode", "Values are useField or useExpression")
  dynObjectManager.registerTag("Layer.quickinfo.expression", "")
  dynObjectManager.registerTag("Layer.quickinfo.fieldname", "")


def main(*args):
  selfRegister()
    