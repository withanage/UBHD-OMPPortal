#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: wit
python3.5 /home/withanage/projects/web2py3/web2py/web2py.py -R  /home/withanage/projects/web2py3/web2py/applications/UBHD_OMPPortal/static/utils/imagesJATSXMLBySubmission.py   --shell UBHD_OMPPortal  -M
'''

from gluon import DAL
from ompdal import OMPDAL

ompdal = OMPDAL(db, myconf)
PRESS_ID = myconf.get('omp.press_id')

s = db.submissions
sc = db.submission_chapters
a = db.authors
aus = db.author_settings

submissions_rows = db(s.context_id == PRESS_ID).select(s.submission_id).as_list()

submissions = sorted(list(map(lambda s: s['submission_id'], submissions_rows)))

submission_chapters = []

for s in submissions:
    chapter_rows = db(sc.submission_id == s).select(sc.chapter_id).as_list()
    submission ={"submission": s, "chapter": "", "type": "Band"}
    authors_rows = db(a.submission_id == s).select(a.author_id).as_list()

    for author in authors_rows:
        author_settings = db(aus.author_id ==author['author_id']).select(aus.setting_name,aus.setting_value).as_list()
        authors_rows = ', '.join(sorted(list(map(lambda s: ' '.join([s['givenName'], s['familyName']]), author_settings))))
        submission['authors_rows'] = authors_rows


    submission_chapters.append(submission)
    for chapter in chapter_rows:
        submission_chapters.append({"submission":s,"chapter":chapter['chapter_id'], "type":"Kapitel"})


#sfor sch in submission_chapters:

#submission_chapter_authors

print()

