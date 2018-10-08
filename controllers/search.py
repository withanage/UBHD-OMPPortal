# -*- coding: utf-8 -*-

from ompdal import OMPDAL, OMPSettings, OMPItem

ompdal = OMPDAL(db, myconf)
press = ompdal.getPress(myconf.take('omp.press_id'))


def authors():
    searchInitial = request.vars.searchInitial
    authors, author_index = [], set()
    prev_author, prev_index = '',''
    prev = 1

    for i,a in enumerate(ompdal.getAuthorsByPress(press.press_id).as_list()):
        initial = a['last_name'].decode('utf-8')[:1]
        if initial != prev_index:
            a['initial'] = initial.upper()
        this_author = '{}{}'.format(a['last_name'], a['first_name'])
        prev = prev + 1 if prev_author == this_author else 1
        a['index'] = prev
        authors.append(a)
        author_index.add(initial)
        prev_author = this_author
        prev_index = initial

    if searchInitial:
        authors = [a for a in authors  if a['last_name'].startswith(searchInitial)]

    return locals()
