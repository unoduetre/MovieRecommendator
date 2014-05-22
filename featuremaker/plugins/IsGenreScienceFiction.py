#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class IsGenreScienceFiction(Feature):
  description = """
Genre: is it science fiction?
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for g in m.genres:
      if g['name'] == 'Science Fiction':
        return True
    return False
