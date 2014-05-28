#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class Countries(Feature):
  description = """
Regional: Production country: set
""".strip()
  
  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    A = sorted([pc['iso_3166_1'] for pc in m.production_countries])
    return ','.join(A)
