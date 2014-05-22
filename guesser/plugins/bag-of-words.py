#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from FeatureSupport import *
from Stemmer import Stemmer
from unidecode import unidecode

class BagOfWordsFeatureSupport(FeatureSupport):
  def __init__(self, featuresData, featureId):
    FeatureSupport.__init__(self, featuresData, featureId)
    self.stemmer = Stemmer('english')
    self.goodChars = frozenset('abcdefghjiklmnopqrstuvwxyz0123456789')
    stopListFn = './resources/general/stopword.csv'
    self.stopList = frozenset(l for l in filter(None, map(lambda l: self.preprocess(l), open(stopListFn, 'rt').readlines())))
  
  def preprocess(self, s):
    chars = []
    for c in unidecode(s.strip().lower()):
      if c in self.goodChars:
        chars.append(c)
    word = ''.join(chars)
    return self.stemmer.stemWord(word)
  
  def extract(self, i):
    bag = frozenset(map(lambda w: self.preprocess(w), filter(None, self[i].split())))
    return bag - self.stopList
  
  def similarity(self, a, b):
    num = len(a & b)
    den = len(a | b)
    return num / den if den != 0 else 1.0


featureSupportLoadersByName = {}

featureNames = [
'Basic: Title'
]

for featureName in featureNames:
  featureSupportLoadersByName[featureName] = BagOfWordsFeatureSupport
