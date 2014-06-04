#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from Stemmer import Stemmer
from unidecode import unidecode

from FeatureBooleanizer import *

class BagOfWordsFeatureBooleanizer(FeatureBooleanizer):
  def __init__(self, featureName, featuresData, featureId):
    FeatureBooleanizer.__init__(self, featureName, featuresData, featureId)
    self.stemmer = Stemmer('english')
    self.goodChars = frozenset('abcdefghjiklmnopqrstuvwxyz0123456789')
    stopListFn = './resources/general/stopword.csv'
    self.stopList = frozenset(l for l in filter(None, map(lambda l: self.preprocess(l), open(stopListFn, 'rt').readlines())))
    allWords = set()
    if self.featureName == 'Basic: Tagline':
      for row in featuresData: allWords |= set(map(lambda w: self.preprocess(w), filter(None, row[featureId].split(','))))
    else:
      for row in featuresData: allWords |= set(map(lambda w: self.preprocess(w), filter(None, row[featureId].split())))
    self.words = sorted(list(filter(None, allWords - self.stopList)))
  
  def preprocess(self, s):
    chars = []
    for c in unidecode(s.strip().lower()):
      if c in self.goodChars:
        chars.append(c)
    word = ''.join(chars)
    return self.stemmer.stemWord(word)
  
  def getFeatureNames(self):
    return [self.featureName + ': ' + word for word in self.words]
  
  def process(self, v):
    vWords = set(map(lambda w: self.preprocess(w), filter(None, v.split(','))))
    return [(word in vWords) for word in self.words]


featureBooleanizersByName = {}

featureNames = [
'Basic: Title',
'Basic: Tagline'
]

for featureName in featureNames:
  featureBooleanizersByName[featureName] = BagOfWordsFeatureBooleanizer
