#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class ProductionYear(Feature):
  description = """
Basic: Production date: year
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    return m.release_date[:4]
