#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class IsLanguageEnglish(Feature):
  description = """
Regional: Spoken languages: is there English?
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for sl in m.spoken_languages:
      if sl['iso_639_1'] == 'en':
        return True
    return False
