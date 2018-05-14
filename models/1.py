# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''

langs = ['en','de']

if request.vars.lang:
    if not request.vars.lang in langs:
        raise HTTP(404,'language not available')
    for l in langs:
        if request.vars.lang.lower() ==l:
            session.forced_language = l

if not session.forced_language:
    session.forced_language = 'de'

T.force(session.forced_language)
