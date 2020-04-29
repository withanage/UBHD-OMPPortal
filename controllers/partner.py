# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''

from os.path import exists

def index():
    if request.args == []:
        redirect( URL('home', 'index'))
    partner_token = request.args[0]
    if exists(request.folder+'/views/partner/'+partner_token+'.html'):
        content = 'partner/'+partner_token+'.html'
    else:
        redirect( URL('home', 'index'))
        
    return locals()
