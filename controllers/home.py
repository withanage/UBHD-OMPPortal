# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''
from ompannouncements import Announcements

def index():
    a = Announcements(myconf, db, locale)
    news_list = a.create_announcement_list()
    return locals()
