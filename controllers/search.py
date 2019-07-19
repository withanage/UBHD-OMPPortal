# -*- coding: utf-8 -*-

from ompdal import OMPDAL, OMPSettings, OMPItem

ompdal = OMPDAL(db, myconf)
press = ompdal.getPress(myconf.take('omp.press_id'))


def authors():
    searchInitial = unicode(request.vars.searchInitial, 'utf-8') if request.vars.searchInitial else None
    authors, author_index = [], set()
    prev_author, prev_index = '',''
    prev = 1

    for a in ompdal.getAuthorsByPress(press.press_id):
        last_name = a['last_name']
        first_name = a['first_name']
        initial = last_name[:1]
        if initial != prev_index:
            a['initial'] = initial.upper()
        this_author = unicode('{}{}').format(last_name, first_name)
        prev = prev + 1 if prev_author == this_author else 1
        a['index'] = prev
        if searchInitial and last_name.startswith(searchInitial):
            authors.append(a)
        elif not searchInitial:
            authors.append(a)
        author_index.add(initial)
        prev_author = this_author
        prev_index = initial

    return locals()
