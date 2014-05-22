#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class IsGenreAction(Feature):
  description = """
Genre: is it action movie?
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for g in m.genres:
      if g['name'] == 'Action':
        return True
    return False
