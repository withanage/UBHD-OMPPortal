# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''

# required - do no delete
import os
import json
from ompdal import OMPDAL, OMPSettings, OMPItem
import ompformat
from os.path import exists
import gluon

locale = 'en_US' if session.forced_language == 'en' else 'de_DE'

def user(): return dict(form=auth())


# ef download(): return response.download(request,db)

def call():
    session.forget()
    return service()


# end requires

def index():
    ompdal = OMPDAL(db, myconf)
    json_list = dict(xml_url='')
    if len(request.args) < 2 :
        raise HTTP(404)
    submission_id = request.args[0]
    file_id = request.args[1]

    if str(file_id).endswith('.xml'):
        path = os.path.join(request.folder, 'static/files/presses', myconf.take('omp.press_id'), 'monographs',
                            submission_id, 'submission/proof', file_id)
        if os.path.exists(path) is False:
            raise HTTP(404)

        submission_settings = ompdal.getSubmissionSettings(submission_id)
        series = ompdal.getSeriesBySubmissionId(submission_id)
        series_settings = ompdal.getSeriesSettings(series.get('series_id')) if series else []

        cssStyles = get_setting_value(series_settings,'cssStyles')
        if not cssStyles:
            cssStyles = get_setting_value(submission_settings,'cssStyles')

        cssStylesStr = cssStyles.replace("'", "\"") if len(cssStyles) >0 else '{}'
        cssStylesDict = json.loads(cssStylesStr)
        font_family = cssStylesDict.get('font-face').get('family') if  cssStylesDict.get('font-face') else 'Source Sans Pro'


        authors = [OMPItem(author, OMPSettings(ompdal.getAuthorSettings(author.author_id)))
                   for author in ompdal.getAuthorsBySubmission(submission_id)]
        authors_string = ', '.join((ompformat.formatName(a.settings) for a in authors))

        return dict(json_list=XML(gluon.serializers.json(json_list)), authors=authors_string, font_family=font_family)
    else:
        path = os.path.join(request.folder, 'static/files/presses', myconf.take('omp.press_id'), 'monographs',
                            submission_id, 'submission/', file_id)
        return response.stream(path, chunk_size=1048576)



def get_setting_value(settings, name):
    val = []
    if settings:
        for i in settings.as_list():
            if i['locale'] == locale and i['setting_name'] == name:
                val = i['setting_value']
    return val


def home():
    return dict()




def download():
    if len(request.args) < 2:
        raise HTTP(404)
    submission_id = request.args[0]
    submission_file = request.args[1]
    if not submission_id or not submission_file:
        raise HTTP(404)
    path = os.path.join(request.folder, 'static/files/presses', myconf.take('omp.press_id'), 'monographs',
                        submission_id, 'submission/proof', submission_file)
    response.headers['ContentType'] = "application/pdf"
    #response.headers['Content-Disposition'] = "attachment; filename=" + submission_file
    return response.stream(path, chunk_size=1048576)


def download_image():
    submission_id = request.args[0]
    submission_file = request.args[1]
    path = os.path.join(request.folder, 'static/files/presses', myconf.take('omp.press_id'), 'monographs',
                        submission_id, 'submission', submission_file)
    return response.stream(path)
