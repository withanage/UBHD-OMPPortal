#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: wit
python /home/wit/software/web2py/web2py.py -R  /home/wit/software/web2py/applications/UBHD_OMPPortal/static/utils/imagesJATSXMLBySubmission.py   --shell UBHD_OMPPortal  -M
'''
import sys
import os
import pwd
import grp

from xlrd import open_workbook
from gluon import DAL
from ompdal import OMPDAL


ompdal = OMPDAL(db, myconf)


def main():
    press_id = myconf.get('omp.press_id')


    submissions = db(db.submissions.context_id == press_id).select(db.submissions.ALL)
    for s in submissions:
        files =ompdal.getSubmissionFileBySubmission(s.submission_id)
        file_path = '{}{}{}{}{}{}{}{}'.format(request.env.web2py_path, '/applications/', request.application,
                                              '/static/files/presses/', press_id, '/monographs/', s.submission_id,
                                              '/submission/')
        try:
            xml_file = open("{}/{}-figures.xml".format(file_path,s.submission_id), "w")
            xml_file.write('<all-images>\n')
            for f in files:
                for t in ['bmp','exif','gif','jpeg','jpg','png','tiff']:
                    if f.original_file_name.lower().endswith(t):
                        file_type = f.original_file_name.split('.').pop().strip().lower()
                        file_name_items = [f.submission_id,
                                           f.genre_id,
                                           f.file_id,
                                           f.revision,
                                           f.file_stage,
                                           f.date_uploaded.strftime('%Y%m%d'),
                                           ]
                        file_name = '-'.join([str(i) for i in file_name_items]) + '.' + file_type
                        if os.path.isfile(file_path+file_name):
                            xml_file.write('<fig-group><fig id="fig_{}_{}" position="float"><label> {} </label><graphic xlink:href="{}"/></fig></fig-group>\n'.format(f.submission_id, f.file_id,f.original_file_name, file_name))

            xml_file.write('</all-images>\n')
            xml_file.close()
        except:
            pass

if __name__ == "__main__":
    main()
