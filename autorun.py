# encoding: utf-8

import gvsig
from gvsig import getResource

from addons.quickinfo import actions
from addons.quickinfo import quickinfopropertypage

reload(actions)

from org.gvsig.tools import ToolsLocator
from java.io import File

def main(*args):
  i18nManager = ToolsLocator.getI18nManager()
  i18nManager.addResourceFamily("text",File(getResource(__file__,"i18n")))
  
  actions.selfRegister()
  quickinfopropertypage.selfRegister()
    