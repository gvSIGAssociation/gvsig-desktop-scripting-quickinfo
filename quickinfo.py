# encoding: utf-8

import gvsig

from org.gvsig.fmap.mapcontrol.tools.Behavior import MouseMovementBehavior
from org.gvsig.fmap.mapcontrol.tools.Listeners import AbstractPointListener
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory

def trace(msg):
  #print "###> ", msg
  pass
  
class QuickInfo(object):

  def __init__(self):
    self.__behavior = None
    self.__layer = None

  def getTooltipValue(self, point, projection):
    try:
      fieldName = self.__layer.getProperty("quickinfo.fieldname")
      expression = self.__layer.getProperty("quickinfo.expression")
      mode = self.__layer.getProperty("quickinfo.mode")
      if mode == "useField":
        if fieldName in ("", None):
          trace('QuickInfo.getTooltipValue: %s return ""' % repr(fieldName))
          return ""
      else:
        if expression in ("", None):
          trace('QuickInfo.getTooltipValue: %s return ""' % repr(fieldName))
          return ""
      
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
        trace('QuickInfo.getTooltipValue: %s point %s, no records selected return ""' % (repr(fieldName), point.convertToWKT()) )
        return ""
      if mode == "useField":
        return str(l[0].get(fieldName))
      _globals = dict()
      _globals.update(globals())
      _globals["store"] = store
      _globals["layer"] = self.__layer
      _locals = dict()
      _locals.update(l[0])
      expression = expression.replace("\n"," ")
      x = eval(expression, _globals,_locals)
      trace("tooltip: %s" % repr(x))
      return x
    except Exception, ex:
      print str(ex)

  def setTool(self, mapControl):
    actives = mapControl.getMapContext().getLayers().getActives()
    if len(actives)!=1:
      # Solo activamos la herramienta si hay una sola capa activa
      trace("QuickInfo.setTool: active layers != 1 (%s)" % len(actives))
      return
    mode = actives[0].getProperty("quickinfo.mode")
    if mode in ("", None):
      # Si la capa activa no tiene configurado el campo a mostrar
      # tampoco activamos la herramienta
      trace('QuickInfo.setTool: active layer %s not has property "quickinfo.fieldname"' % actives[0].getName())
      return 
    self.__layer = actives[0]
    if True or not mapControl.hasTool("quickinfo"):
      trace('QuickInfo.setTool: Add to MapControl 0x%x the "quickinfo" tool' % mapControl.hashCode())
      #
      # Creamos nuestro "tool" asociando el MouseMovementBehavior con nuestro
      # QuickInfoListener.
      self.__behavior = MouseMovementBehavior(QuickInfoListener(mapControl, self))
      self.__behavior.setMapControl(mapControl)    
      #
      # Le añadimos al MapControl la nueva "tool".
      mapControl.addBehavior("quickinfo", self.__behavior)

    trace('QuickInfo.setTool: setTool("quickinfo") to MapControl 0x%x' % mapControl.hashCode())
    #
    # Activamos la tool.
    mapControl.setTool("quickinfo")
    
    

class QuickInfoListener(AbstractPointListener):

  def __init__(self, mapControl, quickinfo):
    AbstractPointListener.__init__(self)
    self.mapControl = mapControl
    self.quickinfo = quickinfo    
    self.projection = self.mapControl.getProjection()
    self.__tolerance = mapControl.getViewPort().toMapDistance(3);
    
    
  def point(self, event):
    p = event.getMapPoint()
    p = p.buffer(self.__tolerance).getEnvelope().getGeometry()
    tip = self.quickinfo.getTooltipValue(p,self.projection)
    self.mapControl.setToolTipText(unicode(tip, 'utf-8'))

def main(*args):      
  viewDoc = gvsig.currentView()
  viewPanel = viewDoc.getWindowOfView()
  mapControl = viewPanel.getMapControl()
  
  quickInfo = QuickInfo()
  quickInfo.setTool(mapControl)
