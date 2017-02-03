# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''
from ompdal import OMPDAL
ompdal = OMPDAL(db, myconf)


response.title = settings.title
response.subtitle = settings.subtitle
response.meta.keywords = settings.keywords
response.meta.description = settings.description


categories = ompdal.getCategoriesByPress(myconf.take('omp.press_id'))
def title(t):
    return '<a href="#" data-toggle="dropdown" data-hover="dropdown"  class="dropdown-toggle" >{} <b class=" icon-angle-down"></b></a> '.format(T(t))


category_list = [LI(A(c['path'],_href=URL('catalog','/'.join(['category',c['path']])))) for c in categories.as_list()]


about_us_dict = [['mission_statement',T('Mission Statement')],
                  ['profile',T('Profile')],
                  ['advisory_board',T('Advisory Board')],
                  ['team',T('Team')],
                  ['partners',T('Partners')]
                 ]
about_us_list = [LI(A(i[1],_href=URL('about_us',i[0]))) for i in about_us_dict]


publishing_dict = [['for_authors', T('Information for Authors')],
                   ['rights_and_licences',T('Rights and Licences')]
                   ]

publishing_dict_list  = [LI(A(i[1],_href=URL('publishing',i[0]))) for i in publishing_dict]



quality_control_dict = [
                        ['peer_review',T('Peer Review')],
                        ['plagiarism',T('Plagiarism')],
                        ['data_privacy',T('Data Privacy')],
                        ]

quality_control_dict_list  = [LI(A(i[1],_href=URL('quality_control',i[0]))) for i in quality_control_dict]


response.menu = UL(
                    [
                        LI(A(T('Home'), _href=URL('home','index'))),
                        LI(
                            XML(title('About us')),UL( about_us_list, _class="dropdown-menu" ), _class="dropdown"
                        ),
                        LI(A(T('Books'), _href=URL('catalog','index'))),
                        LI(A(T('Series'), _href=URL('series','index'))),
                        LI(A(T('Journals'), _href=URL('journals','index'))),
                        LI(
                            XML(title('Categories')), UL(category_list, _class="dropdown-menu"), _class="dropdown"
                        ),
                        LI(
                            XML(title('Publishing')), UL(publishing_dict_list, _class="dropdown-menu"), _class="dropdown"
                        ),
                        LI(
                            XML(title('Quality Control')), UL(quality_control_dict_list, _class="dropdown-menu"), _class="dropdown"
                        ),

                    ]
                    ,_class="nav navbar-nav"
                )








#response.menu = [(T('Categories'), False, None, [(c['path'], False, URL('default', 'index'), [])  )]

