#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class ProductionCompanies(Feature):
  description = """
Basic: Production companies
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    return ','.join(sorted(pc['name'] for pc in m.production_companies))
