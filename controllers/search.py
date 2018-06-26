# -*- coding: utf-8 -*-

from ompdal import OMPDAL, OMPSettings, OMPItem


ompdal = OMPDAL(db, myconf)
press = ompdal.getPress(myconf.take('omp.press_id'))

def authors():
    searchInitial = request.vars.searchInitial
    authors = ompdal.getAuthorsByPress(press.press_id).as_list()
    index = sorted(set([a['last_name'] for a in authors]))


    if searchInitial:
        authors = [a for a in authors  if a['last_name'].startswith(searchInitial)]


    return locals()


