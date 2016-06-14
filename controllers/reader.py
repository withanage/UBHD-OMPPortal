# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''

# required - do no delete
import os

def user(): return dict(form=auth())
# ef download(): return response.download(request,db)

def call():
    session.forget()
    return service()
# end requires

def index():
    from gluon.serializers import json
    json_list = dict(xml_url='')
    locale = 'de_DE'
    if session.forced_language == 'en':
        locale = 'en_US'
    submission_id = request.args[0]
    file_id = request.args[1]

    # check if it is xml
    if str(file_id).endswith('.xml'):
        query = ((db.submission_settings.submission_id == int(submission_id))
                 & (db.submission_settings.locale == locale))
        author_q = ((db.authors.submission_id == submission_id))
        authors_list = db(author_q).select(
            db.authors.first_name, db.authors.last_name)
        authors = ''
        for i in authors_list:
            authors += i.first_name + ' ' + i.last_name + ', '
        if authors.endswith(', '):
            authors = authors[:-2]
        return dict(json_list=XML(json(json_list)), authors=authors)
    else:
        path = os.path.join(request.folder, 'static/files/presses', myconf.take('omp.press_id'), 'monographs',
                            submission_id, 'submission', file_id)
       
        return response.stream(path)

def home():
    return dict()

def index2():
    from gluon.serializers import json
    json_list = dict(xml_url='')
    return dict(json_list=XML(json(json_list)))

def download():
    submission_id = request.args[0]
    submission_file = request.args[1]
    path = os.path.join(request.folder, 'static/files/presses', myconf.take('omp.press_id'), 'monographs',
                        submission_id, 'submission/proof', submission_file)
    response.headers['ContentType'] = "application/octet-stream"
    response.headers[
        'Content-Disposition'] = "attachment; filename=" + submission_file
    db.t_usage_statistics.insert()
    db.commit()
    return response.stream(path, chunk_size=4096)

def download_image():
    submission_id = request.args[0]
    submission_file = request.args[1]
    path = os.path.join(request.folder, 'static/files/presses', myconf.take('omp.press_id'), 'monographs',
                        submission_id, 'submission', submission_file)
    return response.stream(path)
