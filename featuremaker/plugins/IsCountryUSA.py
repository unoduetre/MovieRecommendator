#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class IsCountryUSA(Feature):
  description = """
Regional: Production country: is it USA?
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for pc in m.production_countries:
      if pc['iso_3166_1'] == 'US':
        return True
    return False
