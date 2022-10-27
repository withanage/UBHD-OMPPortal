# -*- coding: utf-8 -*-

from ompdal import OMPDAL, OMPSettings, OMPItem
import ompindex

ompdal = OMPDAL(db, myconf)
press = ompdal.getPress(myconf.take('omp.press_id'))


def index():
    context = dict()
    context['q'] = request.vars.q if request.vars.q else ''

    return context


def authors():
    search_initial = request.vars.searchInitial.upper() if request.vars.searchInitial else None
    rows = ompdal.getAuthorsByPress(press.press_id)
    return ompindex.author_names(search_initial, rows)
