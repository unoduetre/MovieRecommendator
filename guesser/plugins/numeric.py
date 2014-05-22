#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from FeatureSupport import *

class NumericFeatureSupport(FeatureSupport):
  def __init__(self, featuresData, featureId):
    FeatureSupport.__init__(self, featuresData, featureId)
    self.lo, self.hi = float(self[0]), float(self[0])
    for row in self.featuresData.data:
      t = float(row[featureId])
      self.lo = min(self.lo, t)
      self.hi = max(self.hi, t)
    if self.hi == self.lo: self.hi = self.lo + 1.0
    self.a = 1.0 / (self.hi - self.lo)
  
  def extract(self, i):
    return (float(self[i]) - self.lo) * self.a
  
  def similarity(self, a, b):
    if a == b: return 1.0
    return 1.0 - abs(a - b) / max(a, b)


featureSupportLoadersByName = {}

featureNames = [
'Basic: Production date: year',
'Cast: average age',
'TMDB votes: average',
'TMDB votes: count'
]

for featureName in featureNames:
  featureSupportLoadersByName[featureName] = NumericFeatureSupport
