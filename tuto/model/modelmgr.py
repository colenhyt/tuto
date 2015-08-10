__author__ = 'colen'
# -*- coding: utf-8 -*-
from tuto.util.basic import *

class ModelMgr(Singleton):
  def __init__(self):
    self.modelMap = {}