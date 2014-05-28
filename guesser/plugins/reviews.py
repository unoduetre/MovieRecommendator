#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import random
from FeatureSupport import *
from unidecode import unidecode

class ReviewsFeatureSupport(FeatureSupport):
  def __init__(self, featuresData, featureId):
    FeatureSupport.__init__(self, featuresData, featureId)
  
  def extract(self, i):
    ret = {}
    for review in filter(None, map(lambda r: r.strip(), self[i].split(','))):
      for word in filter(None, map(lambda r: r.strip(), review.split())):
        if word in ret: ret[word] += 1
        else: ret[word] = 1
    return ret
  
  def similarity(self, a, b):
    words = set(a.keys()) | set(b.keys())
    num = 0
    den = 0
    for word in words:
      if word in a and word in b:
        num += min(a[word], b[word])
        den += max(a[word], b[word])
      elif word in a:
        den += a[word]
      elif word in b:
        den += b[word]
    return num / den if den != 0 else 1.0


featureSupportLoadersByName = {}

featureNames = [
'Basic: Reviews'
]

for featureName in featureNames:
  featureSupportLoadersByName[featureName] = ReviewsFeatureSupport
