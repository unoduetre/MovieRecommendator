#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from unidecode import unidecode

from FeatureBooleanizer import *

class SetFeatureBooleanizer(FeatureBooleanizer):
  def __init__(self, featureName, featuresData, featureId):
    FeatureBooleanizer.__init__(self, featureName, featuresData, featureId)
    self.goodChars = frozenset('abcdefghjiklmnopqrstuvwxyz0123456789')
    stopListFn = './resources/general/stopword.csv'
    self.stopList = frozenset(l for l in filter(None, map(lambda l: self.preprocess(l), open(stopListFn, 'rt').readlines())))
    allWords = set()
    for row in featuresData: allWords |= set(map(lambda w: self.preprocess(w), filter(None, row[featureId].split(','))))
    self.words = sorted(list(filter(None, allWords - self.stopList)))
  
  def preprocess(self, s):
    chars = []
    for c in unidecode(s.strip().lower()):
      if c in self.goodChars:
        chars.append(c)
    word = ''.join(chars)
    return word
  
  def getFeatureNames(self):
    return [self.featureName + ': ' + word for word in self.words]
  
  def process(self, v):
    vWords = set(map(lambda w: self.preprocess(w), filter(None, v.split(','))))
    return [(word in vWords) for word in self.words]


featureBooleanizersByName = {}

featureNames = [
'Basic: Production date: season',
'Basic: Production companies',
'Basic: Similar movies',
'Cast: all',
'Cast: three most important actors',
'Crew: the first movie director',
'Crew: the first movie producer',
'Crew: the first screenplay writer'
]

for featureName in featureNames:
  featureBooleanizersByName[featureName] = SetFeatureBooleanizer
