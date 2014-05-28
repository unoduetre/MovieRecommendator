#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import random
from FeatureSupport import *
from unidecode import unidecode

class SimilarMoviesFeatureSupport(FeatureSupport):
  def __init__(self, featuresData, featureId):
    FeatureSupport.__init__(self, featuresData, featureId)
  
  def extract(self, i):
    tmdbId = int(self.featuresData.data[i][self.featuresData.featureIdsByName['Helpers: TMDB Id']])
    similar = frozenset(map(int, filter(None, self[i].strip().split(','))))
    return (tmdbId, similar)
  
  def similarity(self, a, b):
    return float(a[0] == b[0] or a[0] in b[1] or b[0] in a[1])


featureSupportLoadersByName = {}

featureNames = [
'Basic: Similar movies'
]

for featureName in featureNames:
  featureSupportLoadersByName[featureName] = SimilarMoviesFeatureSupport
