# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''
from ompdal import OMPDAL
ompdal = OMPDAL(db, myconf)

locale = ''
if session.forced_language == 'en':
    locale = 'en_US'
elif session.forced_language == 'de':
    locale = 'de_DE'



response.title = settings.title
response.subtitle = settings.subtitle
response.meta.keywords = settings.keywords
response.meta.description = settings.description

press_id = myconf.take('omp.press_id')
categories = ompdal.getCategoriesByPress(press_id)


def title(t):
    return '<a href="#" data-toggle="dropdown" data-hover="dropdown"  class="dropdown-toggle" >{} <b class=" icon-angle-down"></b></a> '.format(
        T(t))

def category_setting(c, name):
    return ompdal.getLocalizedCategorySettings(ompdal.getCategoryByPathAndPress(c['path'], press_id).get('category_id'),
                                               name, locale)['setting_value']


category_list = [LI(A(category_setting(c,'title'), _href=URL(
    'category', '/'.join(['info', c['path']])))) for c in categories.as_list()]


about_us_dict = [['mission_statement', T('Mission Statement')],
                 ['profile', T('Profile')],
                 ['advisory_board', T('Advisory Board')],
                 ['team', T('Team')],
                 ['partners', T('Partners')],
                 ['technology', T('Technology')]
                 ]
about_us_list = [LI(A(i[1], _href=URL('about_us', i[0])))
                 for i in about_us_dict]


publishing_dict = [['for_authors', T('Information for Authors')],
                   ['peer_review', T('Peer Review')],
                   ['rights_and_licences', T('Rights and Licences')],
                   ['plagiarism', T('Plagiarism')],
                   ['data_privacy', T('Data Privacy')]
                   ]

publishing_dict_list = [LI(A(i[1], _href=URL('publishing', i[0])))
                        for i in publishing_dict]


def display_form():
    form=FORM( INPUT(_name='search',_class="form-control", _placeholder=T("Search")),
              #INPUT(_type='submit',_class="btn btn-default",),
               _class="navbar-form navbar-left")
    if form.accepts(request,session):
        redirect(URL('catalog','search?q='+request.vars.search))
    return form


response.menu = UL([LI(A(T('Home'),
                         _href=URL('home',
                                   'index'))),
                    LI(XML(title('About us')),
                        UL(about_us_list,
                           _class="dropdown-menu"),
                       _class="dropdown"),
                    LI(A(T('Books'),
                         _href=URL('catalog',
                                   'index'))),
                    LI(A(T('Series'),
                         _href=URL('series',
                                   'index'))),
                    LI(A(T('Journals'),
                         _href=URL('journals',
                                   'index'))),
                    LI(A(T('Campus Media'),
                         _href=URL('category',
                                   'info/campusmedia'))),
                    LI(XML(title('Publishing')),
                       UL(publishing_dict_list,
                          _class="dropdown-menu"),
                       _class="dropdown"),
                    #LI(display_form(),  _class="dropdown")

                    ],
                   _class="nav navbar-nav")


# response.menu = [(T('Categories'), False, None, [(c['path'], False,
# URL('default', 'index'), [])  )]
