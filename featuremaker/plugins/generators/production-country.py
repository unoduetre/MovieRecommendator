#!/usr/bin/env python3
# -*- coding: utf-8 -*-

countries = [
('US', 'USA'),
('GB', 'United Kingdom'),
('DE', 'Germany'),
('FR', 'France'),
('JP', 'Japan'),
('IT', 'Italy'),
('CA', 'Canada'),
('IN', 'India'),
('NZ', 'New Zealand'),
('AU', 'Australia'),
('ES', 'Spain'),
('HK', 'Hong Kong'),
('SE', 'Sweden'),
('CH', 'Switzerland'),
('AT', 'Austria'),
('ZA', 'South Africa'),
('MX', 'Mexico'),
('PL', 'Poland'),
('DK', 'Denmark'),
('TW', 'Taiwan'),
('BR', 'Brasil'),
('IE', 'Ireland')
]

gc = frozenset(list('abcdefghjiklmnopqrstuvwxyz'))

def fix(s):
  r = []
  b = True
  for c in s:
    if c.lower() in gc:
      if b:
        r.append(c.upper())
        b = False
      else:
        r.append(c)
    else:
      b = True
  return ''.join(r)

for code, country in countries:
  cn = fix(country)
  fn = 'IsCountry%s.py' % cn
  f = open(fn, 'wt')
  f.write("""#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class IsCountry%s(Feature):
  description = \"\"\"
Regional: Production country: is it %s?
\"\"\".strip()
  
  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for pc in m.production_countries:
      if pc['iso_3166_1'] == '%s':
        return True
    return False
""" % (cn, country, code))
  f.close()
