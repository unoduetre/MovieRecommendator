#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class ProductionSeason(Feature):
  description = """
Basic: Production date: season
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    year, month, day = map(int, m.release_date.split('-'))
    if month < 3:
      return 'winter'
    elif month == 3:
      return 'winter' if day < 21 else 'spring'
    elif month < 6:
      return 'spring'
    elif month == 6:
      return 'spring' if day < 21 else 'summer'
    elif month < 9:
      return 'summer'
    elif month == 9:
      return 'summer' if day < 23 else 'autumn'
    elif month < 12:
      return 'autumn'
    else:
      return 'autumn' if day < 22 else 'winter'
