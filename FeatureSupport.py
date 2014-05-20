#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from FeaturesData import *

class FeatureSupport(object):
  def __init__(self, featuresData, featureId):
    self.featuresData = featuresData
    self.featureId = featureId
  
  def __getitem__(self, i):
    return self.featuresData.data[i][self.featureId]
  
  """i -- number of row in raw self.featuresData.data"""
  def extract(self, i):
    raise 'Implementation not provided, template called.'
    return self[i]
  
  """a,b -- referenes to the results of extraction"""
  def similarity(self, a, b):
    raise 'Implementation not provided, template called.'
    return 1.0
