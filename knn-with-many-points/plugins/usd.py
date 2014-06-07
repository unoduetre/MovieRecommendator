#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from FeatureSupport import *

class DollarFeatureSupport(FeatureSupport):
  def __init__(self, featuresData, featureId):
    FeatureSupport.__init__(self, featuresData, featureId)
    
    self.usdByYear = {}
    usdFn = './resources/general/usd-by-year.csv'
    for l in filter(None, map(lambda l: l.strip(), open(usdFn, 'rt').readlines())):
      w = l.split(';')
      year = int(w[0])
      cf = float(w[1])
      self.usdByYear[year] = cf
    
    self.yearFeatureId = self.featuresData.featureIdsByName['Basic: Production date: year']
    
    self.lo, self.hi = float(self[0]), float(self[0])
    for row in self.featuresData.data:
      t = float(row[featureId]) * self.usdByYear[int(row[self.yearFeatureId])]
      self.lo = min(self.lo, t)
      self.hi = max(self.hi, t)
    if self.hi == self.lo: self.hi = self.lo + 1.0
    self.a = 1.0 / (self.hi - self.lo)
  
  def extract(self, i):
    t = float(self[i]) * self.usdByYear[int(self.featuresData.data[i][self.yearFeatureId])]
    return (t - self.lo) * self.a
  
  def similarity(self, a, b):
    if a == b: return 1.0
    return 1.0 - abs(a - b) / max(a, b)


featureSupportLoadersByName = {}

featureNames = [
'Basic: Budget'
]

for featureName in featureNames:
  featureSupportLoadersByName[featureName] = DollarFeatureSupport
