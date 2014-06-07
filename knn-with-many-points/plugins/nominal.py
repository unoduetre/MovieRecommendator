#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import random
from FeatureSupport import *
from unidecode import unidecode

class NominalFeatureSupport(FeatureSupport):
  def __init__(self, featuresData, featureId):
    FeatureSupport.__init__(self, featuresData, featureId)
  
  def preprocess(self, s):
    return unidecode(s.strip().lower())
  
  def extract(self, i):
    ret = self.preprocess(self[i])
    if len(ret) == 0: ret = ''.join(random.choice('abcdefghjiklmnopqrstuvwxyz' for _ in range(20)))
    return ret
  
  def similarity(self, a, b):
    return float(a == b)


featureSupportLoadersByName = {}

featureNames = [
'Crew: the first movie director',
'Crew: the first movie producer',
'Crew: the first screenplay writer',
'Helpers: TMDB Id'
]

for featureName in featureNames:
  featureSupportLoadersByName[featureName] = NominalFeatureSupport
