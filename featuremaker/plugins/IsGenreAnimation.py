#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class IsGenreAnimation(Feature):
  description = """
Genre: is it animation?
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for g in m.genres:
      if g['name'] == 'Animation':
        return True
    return False
