#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from FeatureSupport import *
from unidecode import unidecode

class NominalFeatureSupport(FeatureSupport):
  def __init__(self, featuresData, featureId):
    FeatureSupport.__init__(self, featuresData, featureId)
  
  def preprocess(self, s):
    return unidecode(s.strip().lower())
  
  def extract(self, i):
    return self.preprocess(self[i])
  
  def similarity(self, a, b):
    return float(a == b)


featureSupportLoadersByName = {}

featureNames = [
'Crew: the first movie director',
'Crew: the first movie producer',
'Crew: the first screenplay writer'
]

for featureName in featureNames:
  featureSupportLoadersByName[featureName] = NominalFeatureSupport
