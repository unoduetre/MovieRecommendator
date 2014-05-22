#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class IsGenreAdventure(Feature):
  description = """
Genre: is it adventure movie?
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for g in m.genres:
      if g['name'] == 'Adventure':
        return True
    return False
