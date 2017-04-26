# -*- coding: utf-8 -*-
'''
Copyright (c) 2017 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''

from gluon import DAL
from ompdal import OMPDAL
import sunburnt
from ompsolr import OMPSOLR
import sys


ompdal = OMPDAL(db, myconf)


class Solr:
    def __init__(self):
        pass

def main():
    ps = ompdal.getPresses()
    solr = OMPSOLR(db, myconf)
    document = []
    solr.si.delete(queries=solr.si.Q("*"))
    solr.si.commit()

    for p in ps:
        submissions =  ompdal.getSubmissionsByPress(p.press_id)
        for s in submissions:
            sub = {}
            sub['press_id'] = p.press_id
            sub['submission_id'] = s.submission_id
            #sub['id'] = s.submission_id
            sub['locale'] = s.locale
            #print ompdal.getActualAuthorsBySubmission(s.submission_id)
            s_settings = ompdal.getSubmissionSettings(s.submission_id)
            for v in s_settings:
                if v.get('locale'):
                    key = '{}_{}'.format(v.get('setting_name').lower(),v.get('locale').split('_')[0])
                    sub[key] =  v.get('setting_value').decode('utf-8')
            document.append(sub)




    #print document
    solr.si.add(document)
    solr.si.commit()


if __name__ == '__main__':
    main()