# -*- coding: utf-8 -*-
'''
Copyright (c) 2017 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''

from gluon import DAL
from ompdal import OMPDAL

ompdal = OMPDAL(db, myconf)

class Solr:
    def __init__(self):
        pass

def main():
    solr = Solr()
    ps = ompdal.getPresses()
    for p in ps:
        submissions =  ompdal.getSubmissionsByPress(p.press_id)
        for s in submissions:
            print p.press_id, s.submission_id
            #print ompdal.getActualAuthorsBySubmission(s.submission_id)
            print ompdal.getSubmissionSettings(s.submission_id)



if __name__ == '__main__':
    main()