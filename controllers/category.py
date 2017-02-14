# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''

from ompdal import OMPDAL, OMPSettings, OMPItem
from os.path import exists


def info():
    if request.args == []:
        redirect(URL('home', 'index'))
    category_path = request.args[0]
    press = ompdal.getPress(myconf.take('omp.press_id'))

    content = []
    category = []

    if exists(request.folder + 'views/catalog/' + category_path + "_info.html"):
        content = "category/" + category_path + "_info.html"
    else:
        row = ompdal.getCategoryByPathAndPress(category_path, press.press_id)
        category = OMPItem(row,
                           OMPSettings(ompdal.getCategorySettings(row.category_id))
                           )

        #category.sort(key=lambda s: s.settings.getLocalizedValue('title', locale))


    return locals()
