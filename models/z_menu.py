# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''
from ompdal import OMPDAL
ompdal = OMPDAL(db, myconf)


response.title = settings.title
response.subtitle = settings.subtitle
response.meta.keywords = settings.keywords
response.meta.description = settings.description
#response.menu = []


categories = ompdal.getCategoriesByPress(myconf.take('omp.press_id'))

response.menu = [(T('Categories'), False, None, [(c['path'], False, URL('default', 'index'), [])  for c in categories.as_list()])]

