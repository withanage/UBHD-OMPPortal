# -*- coding: utf-8 -*-

from ompdal import OMPDAL, OMPSettings, OMPItem

ompdal = OMPDAL(db, myconf)
press = ompdal.getPress(myconf.take('omp.press_id'))


def authors():
    searchInitial = request.vars.searchInitial.upper() if request.vars.searchInitial else None
    authors = []
    initials = set()
    author_index = []
    prev_author, prev_index = '',''
    prev = 1

    for a in ompdal.getAuthorsByPress(press.press_id):
        last_name = a['last_name']
        first_name = a['first_name']
        initial = last_name[:1].upper()
        if initial != prev_index:
            a['initial'] = initial
        this_author = '{}{}'.format(last_name, first_name)
        prev = prev + 1 if prev_author == this_author else 1
        a['index'] = prev
        if searchInitial and last_name.upper().startswith(searchInitial):
            authors.append(a)
        elif not searchInitial:
            authors.append(a)
        if initial not in initials:
            author_index.append(initial)
            initials.add(initial)

        prev_author = this_author
        prev_index = initial

    return locals()
