#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class IsLanguageHebrew(Feature):
  description = """
Regional: Spoken languages: is there Hebrew?
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for sl in m.spoken_languages:
      if sl['iso_639_1'] == 'he':
        return True
    return False