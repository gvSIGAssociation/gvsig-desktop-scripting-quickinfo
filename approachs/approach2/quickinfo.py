# encoding: utf-8

import gvsig
from gvsig import getResource

from org.gvsig.fmap.mapcontrol.tools.Behavior import MouseMovementBehavior
from org.gvsig.fmap.mapcontrol.tools.Listeners import AbstractPointListener
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory

class QuickInfo(object):

  def __init__(self):
    self.__behavior = None
    self.__layer = None

  def getTooltipValue(self, point, projection):
    try:
      fieldName = "pob_total"
      store = self.__layer.getFeatureStore()
      query = store.createFeatureQuery()

      # Haremos un filtro espacial para localizar los
      # registros que intersecten con el punto sobre el que
      # esta el raton.
      query.setFilter(SpatialEvaluatorsFactory.getInstance().intersects(point,projection,store))

      # Con que nos devuelba la primera linea es suficiente.
      query.setLimit(1)
      query.retrievesAllAttributes();
      l = store.getFeatures(query,100)
      if len(l) < 1:
        #print '### QuickInfo.getTooltipValue: field %s point %s, no records selected return ""' % (repr(fieldName), point.convertToWKT()) 
        return ""
      return str(l[0].get(fieldName))
    except Exception, ex:
      print str(ex)

  def setTool(self, mapControl):
    #
    # Nos quedamos con nuestra capa de manzanas_pob
    self.__layer = mapControl.getMapContext().getLayers().getLayer("manzanas_pob")
    
    if not mapControl.hasTool("quickinfo"):
      print '### QuickInfo.setTool: Add to MapControl 0x%x the "quickinfo" tool' % mapControl.hashCode()
      #
      # Creamos nuestro "tool" asociando el MouseMovementBehavior con nuestro
      # QuickInfoListener.
      self.__behavior = MouseMovementBehavior(QuickInfoListener(mapControl, self))
      self.__behavior.setMapControl(mapControl)
      
      #
      # Le añadimos al MapControl la nueva "tool".
      mapControl.addBehavior("quickinfo", self.__behavior)
    
    #
    # Activamos la tool.
    mapControl.setTool("quickinfo")
    

class QuickInfoListener(AbstractPointListener):

  def __init__(self, mapControl, quickinfo):
    AbstractPointListener.__init__(self)
    self.mapControl = mapControl
    self.quickinfo = quickinfo    
    self.projection = self.mapControl.getProjection()
    
  def point(self, event):
    p = event.getMapPoint()
    tip = self.quickinfo.getTooltipValue(p,self.projection)
    self.mapControl.setToolTipText(unicode(tip, 'utf-8'))

def main(*args):      
  viewDoc = gvsig.currentView()
  viewPanel = viewDoc.getWindowOfView()
  mapControl = viewPanel.getMapControl()
  
  quickInfo = QuickInfo()
  quickInfo.setTool(mapControl)
