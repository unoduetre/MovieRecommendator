#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from FeatureSupport import *

class SeasonFeatureSupport(FeatureSupport):
  def __init__(self, featuresData, featureId):
    FeatureSupport.__init__(self, featuresData, featureId)
    self.seasonToInt = {}
    self.seasonToInt['winter'] = 0
    self.seasonToInt['spring'] = 1
    self.seasonToInt['summer'] = 2
    self.seasonToInt['autumn'] = 3
  
  def extract(self, i):
    assert self[i] in self.seasonToInt
    return self.seasonToInt[self[i]]
  
  def similarity(self, a, b):
    return 1.0 - min((4 + a - b) & 3, (4 - a + b) & 3) * 0.5


featureSupportLoadersByName = {}

featureNames = [
'Basic: Production date: season'
]

for featureName in featureNames:
  featureSupportLoadersByName[featureName] = SeasonFeatureSupport
