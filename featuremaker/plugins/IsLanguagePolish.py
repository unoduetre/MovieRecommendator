#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class IsLanguagePolish(Feature):
  description = """
Regional: Spoken languages: is there Polish?
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for sl in m.spoken_languages:
      if sl['iso_639_1'] == 'pl':
        return True
    return False
