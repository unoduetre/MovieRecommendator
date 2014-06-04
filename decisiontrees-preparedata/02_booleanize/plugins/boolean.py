#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from FeatureBooleanizer import *

class BooleanFeatureBooleanizer(FeatureBooleanizer):
  def __init__(self, featureName, featuresData, featureId):
    FeatureBooleanizer.__init__(self, featureName, featuresData, featureId)
  
  def getFeatureNames(self):
    return [self.featureName]
  
  def process(self, v):
    assert v in ('true', 'false')
    return [v == 'true']


featureBooleanizersByName = {}

featureNames = [
'Genre: is it action?',
'Genre: is it adventure?',
'Genre: is it animation?',
'Genre: is it comedy?',
'Genre: is it crime?',
'Genre: is it drama?',
'Genre: is it family?',
'Genre: is it fantasy?',
'Genre: is it film noir?',
'Genre: is it foreign?',
'Genre: is it history?',
'Genre: is it horror?',
'Genre: is it music?',
'Genre: is it musical?',
'Genre: is it mystery?',
'Genre: is it neo-noir?',
'Genre: is it romance?',
'Genre: is it science fiction?',
'Genre: is it sport?',
'Genre: is it sports film?',
'Genre: is it suspense?',
'Genre: is it thriller?',
'Genre: is it war?',
'Genre: is it western?',
'Regional: Production country: is it Australia?',
'Regional: Production country: is it Austria?',
'Regional: Production country: is it Brasil?',
'Regional: Production country: is it Canada?',
'Regional: Production country: is it Denmark?',
'Regional: Production country: is it France?',
'Regional: Production country: is it Germany?',
'Regional: Production country: is it Hong Kong?',
'Regional: Production country: is it India?',
'Regional: Production country: is it Ireland?',
'Regional: Production country: is it Italy?',
'Regional: Production country: is it Japan?',
'Regional: Production country: is it Mexico?',
'Regional: Production country: is it New Zealand?',
'Regional: Production country: is it Poland?',
'Regional: Production country: is it South Africa?',
'Regional: Production country: is it Spain?',
'Regional: Production country: is it Sweden?',
'Regional: Production country: is it Switzerland?',
'Regional: Production country: is it Taiwan?',
'Regional: Production country: is it United Kingdom?',
'Regional: Production country: is it USA?',
'Regional: Spoken languages: is there Arabic?',
'Regional: Spoken languages: is there Chinese?',
'Regional: Spoken languages: is there Czech?',
'Regional: Spoken languages: is there Esperanto?',
'Regional: Spoken languages: is there Greek?',
'Regional: Spoken languages: is there Irish?',
'Regional: Spoken languages: is there Nepali?',
'Regional: Spoken languages: is there Norwegian?',
'Regional: Spoken languages: is there Persian?',
'Regional: Spoken languages: is there Polish?',
'Regional: Spoken languages: is there Russian?',
'Regional: Spoken languages: is there Southern Sotho?',
'Regional: Spoken languages: is there Swedish?',
'Regional: Spoken languages: is there Tamil?',
'Regional: Spoken languages: is there Thai?',
'Regional: Spoken languages: is there Urdu?',
'Regional: Spoken languages: is there Vietnamese?',
'Regional: Spoken languages: is there Xhosa?',
'Regional: Spoken languages: is there Yiddish?',
'Regional: Spoken languages: is there English?',
'Regional: Spoken languages: is there French?',
'Regional: Spoken languages: is there German?',
'Regional: Spoken languages: is there Italian?',
'Regional: Spoken languages: is there Japanese?',
'Regional: Spoken languages: is there Latin?',
'Regional: Spoken languages: is there Spanish?'
]

for featureName in featureNames:
  featureBooleanizersByName[featureName] = BooleanFeatureBooleanizer
