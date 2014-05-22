#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class Director(Feature):
  description = """
Crew: the first movie director
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for c in m.crew:
      if c['job'] == 'Director':
        return c['name']
