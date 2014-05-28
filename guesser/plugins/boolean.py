#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from FeatureSupport import *

class BooleanFeatureSupport(FeatureSupport):
  def __init__(self, featuresData, featureId):
    FeatureSupport.__init__(self, featuresData, featureId)
  
  def extract(self, i):
    assert self[i] in ('true', 'false')
    return self[i] == 'true'
  
  def similarity(self, a, b):
    return float(a == b)


featureSupportLoadersByName = {}

genres = [
'Drama', 
'Thriller', 
'Crime', 
'Action', 
'Comedy', 
'Mystery', 
'Adventure', 
'Romance', 
'War', 
'History', 
'Fantasy', 
'Science Fiction', 
'Family', 
'Animation', 
'Western', 
'Film Noir', 
'Suspense', 
'Horror', 
'Musical', 
'Sport', 
'Foreign', 
'Sports Film', 
'Music', 
'Neo-noir'
]

for genre in genres:
  genreName = genre.lower()
  featureName = 'Genre: is it %s?' % genreName
  featureSupportLoadersByName[featureName] = BooleanFeatureSupport

countries = [
('US', 'USA'),
('GB', 'United Kingdom'),
('DE', 'Germany'),
('FR', 'France'),
('JP', 'Japan'),
('IT', 'Italy'),
('CA', 'Canada'),
('IN', 'India'),
('NZ', 'New Zealand'),
('AU', 'Australia'),
('ES', 'Spain'),
('HK', 'Hong Kong'),
('SE', 'Sweden'),
('CH', 'Switzerland'),
('AT', 'Austria'),
('ZA', 'South Africa'),
('MX', 'Mexico'),
('PL', 'Poland'),
('DK', 'Denmark'),
('TW', 'Taiwan'),
('BR', 'Brasil'),
('IE', 'Ireland')
]

for _,country in countries:
  featureName = 'Regional: Production country: is it %s?' % country
  featureSupportLoadersByName[featureName] = BooleanFeatureSupport

languages = [
('en', 'English'),
('fr', 'French'),
('de', 'German'),
('es', 'Spanish'),
('it', 'Italian'),
('ja', 'Japanese'),
('ru', 'Russian'),
('la', 'Latin'),
('ar', 'Arabic'),
('cn', 'Chinese (with incorrect code)'),
('pl', 'Polish'),
('hi', 'Hindi'),
('el', 'Greek'),
('da', 'Danish'),
('pt', 'Portuguese'),
('he', 'Hebrew'),
('vi', 'Vietnamese'),
('zh', 'Chinese'),
('yi', 'Yiddish'),
('no', 'Norwegian'),
('cs', 'Czech'),
('sv', 'Swedish'),
('hu', 'Hungarian'),
('eo', 'Esperanto'),
('fa', 'Persian'),
('xh', 'Xhosa'),
('zu', 'Zulu'),
('ga', 'Irish'),
('af', 'Afrikaans'),
('ne', 'Nepali'),
('ny', 'Chichewa'),
('ta', 'Tamil'),
('gd', 'Scottish Gaelic'),
('tr', 'Turkish'),
('ur', 'Urdu'),
('th', 'Thai'),
('st', 'Southern Sotho')
]

for _, language in languages:
  featureName = 'Regional: Spoken languages: is there %s?' % language
  featureSupportLoadersByName[featureName] = BooleanFeatureSupport


featureNames = [
'Basic: Adult'
]

for featureName in featureNames:
  featureSupportLoadersByName[featureName] = BooleanFeatureSupport
