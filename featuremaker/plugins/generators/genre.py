#!/usr/bin/env python3
# -*- coding: utf-8 -*-

genres = [
'Drama', 
'Thriller', 
'Crime', 
'Action', 
'Comedy', 
'Mystery', 
'Adventure', 
'Romance', 
'War', 
'History', 
'Fantasy', 
'Science Fiction', 
'Family', 
'Animation', 
'Western', 
'Film Noir', 
'Suspense', 
'Horror', 
'Musical', 
'Sport', 
'Foreign', 
'Sports Film', 
'Music', 
'Neo-noir'
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

for genre in genres:
  cn = fix(genre)
  fn = 'IsGenre%s.py' % cn
  f = open(fn, 'wt')
  f.write("""#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class IsGenre%s(Feature):
  description = \"\"\"
Genre: is it %s?
\"\"\".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for g in m.genres:
      if g['name'] == '%s':
        return True
    return False
""" % (cn, genre.lower(), genre))
  f.close()
