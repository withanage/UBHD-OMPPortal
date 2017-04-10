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


ompdal = OMPDAL(db, myconf)


class Solr:
    def __init__(self):
        pass

def main():
    ps = ompdal.getPresses()
    solr = OMPSOLR(db, myconf)
    submissions = []

    for p in ps:
        submissions =  ompdal.getSubmissionsByPress(p.press_id)
        for s in submissions:
            sub = {}
            sub['omp_press_id'] = p.press_id
            sub['submission_id'] = s.submission_id

            #print ompdal.getActualAuthorsBySubmission(s.submission_id)
            ss = ompdal.getSubmissionSettings(s.submission_id)
            for value in ss:
                print value.get('locale')
                print value


    document = [{"id": "0553573403",
                "cat": "book",
                "name": "A Game of Thrones",
                "price": 7.99,
                "inStock": True,
                "author_t":
                    "George R.R. Martin",
                "series_t": "A Song of Ice and Fire",
                "sequence_i": 1,
                "genre_s": "fantasy"}]

    #solr.si.add(submissions)
    #solr.si.commit()


if __name__ == '__main__':
    main()