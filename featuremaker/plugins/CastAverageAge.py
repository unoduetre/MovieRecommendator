#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class CastAverageAge(Feature):
  description = """
Cast: average age
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
    self.persons = kwargs['persons']
 
  def extract(self, m):
    num = 0
    den = 0
    y1 = int(m.release_date[:4])
    for c in m.cast:
      if self.persons[c['id']].birthday != None:
        y0 = self.persons[c['id']].birthday[:4]
        if y0.strip() == '': continue
        y0 = int(y0)
        num += y1 - y0
        den += 1
    return num / den
