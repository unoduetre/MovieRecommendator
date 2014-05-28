#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class IsGenreMusical(Feature):
  description = """
Genre: is it musical?
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for g in m.genres:
      if g['name'] == 'Musical':
        return True
    return False
