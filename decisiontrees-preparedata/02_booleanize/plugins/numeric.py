#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from FeatureBooleanizer import *

class NumericFeatureBooleanizer(FeatureBooleanizer):
  def __init__(self, featureName, featuresData, featureId):
    FeatureBooleanizer.__init__(self, featureName, featuresData, featureId)
    values = sorted(float(row[featureId]) for row in featuresData)
    self.D = [values[int((len(values)-1)*i/9.0)] for i in range(1, 9)]
  
  def getFeatureNames(self):
    subnames = ['<D2', '<D3', '<D4', '<D5', '<D6', '<D7', '<D8', '<D9']
    return [self.featureName + ': ' + subname for subname in subnames]
  
  def process(self, v):
    vv = float(v)
    ret = [vv < d for d in self.D]
    return ret


featureBooleanizersByName = {}

featureNames = [
'Basic: Budget',
'Basic: Production date: year',
'Cast: average age',
'TMDB votes: average',
'TMDB votes: count'
]

for featureName in featureNames:
  featureBooleanizersByName[featureName] = NumericFeatureBooleanizer
