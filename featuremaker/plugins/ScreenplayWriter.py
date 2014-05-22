#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class ScreenplayWriter(Feature):
  description = """
Crew: the first screenplay writer
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for c in m.crew:
      if c['job'] == 'Screenplay' and c['department'] == 'Writing':
        return c['name']
