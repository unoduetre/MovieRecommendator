#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from FeatureSupport import *
from unidecode import unidecode

class SetOfNamesSupport(FeatureSupport):
  def __init__(self, featuresData, featureId):
    FeatureSupport.__init__(self, featuresData, featureId)
  
  def preprocess(self, s):
    return unidecode(s.strip().lower())
  
  def extract(self, i):
    return frozenset(map(lambda n: self.preprocess(n), filter(None, self[i].split(','))))
  
  def similarity(self, a, b):
    num = len(a & b)
    den = len(a | b)
    return num / den if den != 0 else 1.0


featureSupportLoadersByName = {}

featureNames = [
'Cast: three most important actors'
]

for featureName in featureNames:
  featureSupportLoadersByName[featureName] = SetOfNamesSupport
