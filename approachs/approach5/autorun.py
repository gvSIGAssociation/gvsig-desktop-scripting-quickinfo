# encoding: utf-8

import gvsig

import actions
import quickinfopropertypage

reload(actions)

def main(*args):
  actions.selfRegister()
  quickinfopropertypage.selfRegister()
    