#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class IsCountryIndia(Feature):
  description = """
Regional: Production country: is it India?
""".strip()
  
  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for pc in m.production_countries:
      if pc['iso_3166_1'] == 'IN':
        return True
    return False