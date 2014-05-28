#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import random
from FeatureSupport import *
from unidecode import unidecode

class SetOfNamesSupport(FeatureSupport):
  def __init__(self, featuresData, featureId):
    FeatureSupport.__init__(self, featuresData, featureId)
  
  def preprocess(self, s):
    return unidecode(s.strip().lower())
  
  def extract(self, i):
    ret = frozenset(map(lambda n: self.preprocess(n), filter(None, self[i].split(','))))
    if len(ret) == 0: ret = frozenset([''.join(random.choice('abcdefghjiklmnopqrstuvwxyz') for _ in range(20))])
    return ret
  
  def similarity(self, a, b):
    num = len(a & b)
    den = len(a | b)
    return num / den if den != 0 else 1.0


featureSupportLoadersByName = {}

featureNames = [
'Basic: Keywords',
'Basic: Overview',
'Basic: Tagline',
'Basic: Production companies',
'Cast: all',
'Cast: three most important actors',
'Crew: all',
'Genre: set',
'Regional: Production country: set'
]

for featureName in featureNames:
  featureSupportLoadersByName[featureName] = SetOfNamesSupport
