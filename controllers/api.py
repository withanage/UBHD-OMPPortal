# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''

import gluon.contrib.simplejson as sj
from ompdal import OMPDAL
from ompcsl import OMPCSL
from os.path import join

response.headers['Content-Type'] = 'application/json'
response.view = 'generic.json'
url = join(request.env.http_host, request.application, request.controller)

ompdal = OMPDAL(db, myconf)
press = ompdal.getPress(myconf.take('omp.press_id'))

if session.forced_language == 'en':
    locale = 'en_US'
elif session.forced_language == 'de':
    locale = 'de_DE'
else:
    locale = ''


@request.restful()
def index():
    """
    Returns all the rest services
    """

    def GET(*args, **vars):
        l = ['catalog', 'csl', 'oastatistik']

        apis = {}
        for i in l:
            apis[i] = join(url, i)
        return apis

    return locals()


@request.restful()
def catalog():
    """ Returns  press submissions """

    def GET(*args, **vars):
        submissions = ompdal.getSubmissionsByPress(press.press_id, -1).as_list()
        submission_ids = [{s['submission_id']: join(url, 'catalog', str(s['submission_id']))} for s in submissions]
        return dict(submissions=request.vars.sort_by)

    return locals()


def remove_url_prefix(url):
    url = url.replace("http://", "")
    url = url.replace("https://", "")
    urls = [url.split('/')[0] for url in url.split()]
    return ''.join(urls)


def get_series_info(b):
    r = None
    series = ompdal.getSeriesBySubmissionId(b['submission_id'])
    s_id = series.get('series_id') if series else ''
    sp = series.get('path') if series else ''
    s_t = db((db.series_settings.series_id == s_id) & (db.series_settings.locale == locale) & (
                db.series_settings.setting_name == 'title')).select()
    s_t = s_t.first().get('setting_value') if s_t else None
    if series:
        r = {
            "label"                  : s_t,
            'id'                     : 'url:{}/catalog/series/{}'.format(remove_url_prefix(myconf.take('web.url')), sp),
            "type"                   : "collection",
            "associate_via_hierarchy": [get_press_info(locale)]
        }
    return r


def oastatistik():
    locale = 'de_DE'
    if session.forced_language == 'en':
        locale = 'en_US'
    query = (
            (db.submissions.context_id == myconf.take('omp.press_id')) & (
            db.submissions.status == 3) & (
                    db.submission_settings.submission_id == db.submissions.submission_id) & (
                    db.submission_settings.locale == locale))
    submissions = db(query).select(db.submission_settings.ALL, orderby=db.submissions.submission_id)
    subs = {}
    title, publication_format_settings_doi = '', None
    for book_id in submissions:
        # full book
        publication_format_settings = get_publication_format_settings(book_id)
        if publication_format_settings:
            publication_format_settings_doi = get_publication_format_settings_doi(publication_format_settings,
                                                                                  publication_format_settings_doi)

        if book_id.setting_name == 'title':
            title = book_id.setting_value

        #authors = get_authors(book_id)
        full_files = get_full_books(book_id)
        press_info = get_press_info(locale)
        series_info = get_series_info(book_id)

        for f in full_files:
            full = {}
            full["label"] = title
            full["type"] = "volume"

            full = get_as(full, press_info, series_info)
            statics_id = str(book_id.submission_id) + '-' + str(f.file_id)

            if publication_format_settings_doi:
                full["norm_id"] = publication_format_settings_doi['setting_value']
            else:
                full["id"] = myconf.take('statistik.id') + ':' + statics_id

            file_name = statics_id + '-' + str(f.original_file_name.rsplit('.')[1])
            subs[file_name] = full

        fullbook = {}
        fullbook["label"] = title
        fullbook["type"] = "volume"

        if publication_format_settings_doi:
            fullbook["norm_id"] = publication_format_settings_doi['setting_value']
        fullbook = get_as(fullbook, press_info, series_info)

        chapters = get_chapters(book_id)
        for c in chapters:
            chapter_id = str(book_id['submission_id']) + '-' + str(c['submission_chapters']['chapter_id'])
            type = db(db.submission_files.file_id == c['submission_file_settings']['file_id']).select(
                    db.submission_files.original_file_name).first()['original_file_name'].rsplit('.')[1]
            file_id = str(book_id['submission_id']) + '-' + \
                      str(c['submission_file_settings']['file_id']) + '-' + str(type)

            subs[file_id] = []
            part_title = get_parts_title(c, locale)
            bookpart = get_book_part(c, chapter_id, part_title)
            subs[file_id] = bookpart
            subs[file_id]["associate_via_hierarchy"] = [fullbook]

    return sj.dumps(subs, separators=(',', ':'), sort_keys=True)


def get_as(fullbook, press_info, series_info):
    fullbook["associate_via_hierarchy"] = []
    if series_info:
        fullbook["associate_via_hierarchy"].append(series_info)
    else:
        fullbook["associate_via_hierarchy"].append(press_info)
    return fullbook


def get_press_info(locale):
    press_info = {
        'id'   : 'url:{}/{}'.format(remove_url_prefix(myconf.take('web.url')), myconf.take('web.application')),
        'type' : 'press',
        'label': db(((db.press_settings.locale == locale) & (
                db.press_settings.press_id == myconf.take('omp.press_id')) & (
                             db.press_settings.setting_name == 'name'))).select().first()['setting_value']
        }
    return press_info


def get_authors(book_id):
    authors = []
    a = ompdal.getAuthorsBySubmission(book_id.submission_id).as_list()

    for i in a:
        author = {}
        author['type'] = 'person'
        author['relation'] = 'creators'
        author = ompdal.getAuthorSettings(i['author_id']).as_list()
        # family_name, given_name = get_author_name(author)
        # author['label'] = given_name + ' ' + family_name
        authors.append(author)
    return authors


def get_author_name(author):
    given_name, family_name = '', ''
    for i in author:
        if i['setting_name'] == 'givenName':
            given_name = i['setting_value']
        if i['setting_name'] == 'familyName':
            family_name = i['setting_value']
    return family_name, given_name


def get_book_part(c, chapter_id, part_title):
    bookpart = {}
    if part_title:
        bookpart["label"] = part_title['setting_value']
    bookpart["id"] = myconf.take('statistik.id') + ':' + chapter_id
    bookpart["type"] = "part"
    # chapter_autors = []
    # authors = get_chapter_authors(c).as_list()
    # for i in authors:
    #     chapter_autors.append({"type": "person"})
    #     chapter_autors.append({"relation": "creators"})
    #     author = ompdal.getAuthorSettings(i['author_id']).as_list()
    #     family_name, given_name = get_author_name(author)
    #     chapter_autors.append({'name': ' '.join([given_name, family_name])})
    # if chapter_autors:
    #     bookpart["associate_via_hierarchy"] = chapter_autors
    return bookpart


def get_chapter_authors(c):
    author_id_list = db(
            db.submission_chapter_authors.chapter_id == int(
                    c['submission_chapters']['chapter_id'])).select(
            db.submission_chapter_authors.author_id,
            orderby=db.submission_chapter_authors.seq)
    return author_id_list


def get_parts_title(c, locale):
    part_title = db(
            (db.submission_chapter_settings.chapter_id == int(
                    c['submission_chapters']['chapter_id'])) & (
                    db.submission_chapter_settings.locale == locale) & (
                    db.submission_chapter_settings.setting_name == 'title')).select(
            db.submission_chapter_settings.setting_value).first()
    return part_title


def get_chapters(book_id):
    chapters = db(
            (db.submission_chapters.submission_id == book_id['submission_id']) & (
                    db.submission_file_settings.setting_name == 'chapterID') & (
                    db.submission_file_settings.setting_value == db.submission_chapters.chapter_id)).select(
            db.submission_chapters.chapter_id,
            db.submission_file_settings.file_id,
            orderby=db.submission_chapters.seq)
    return chapters


def get_full_books(book_id):
    full_files = db(
            (db.submission_files.genre_id == myconf.take('omp.monograph_type_id')) & (
                    db.submission_files.file_stage > 5) & (
                    db.submission_files.submission_id == book_id.submission_id)).select(
            db.submission_files.submission_id,
            db.submission_files.file_id,
            db.submission_files.original_file_name)
    return full_files


def get_publication_format_settings_doi(publication_format_settings, publication_format_settings_doi):
    publication_format_settings_doi = db(
            (db.publication_format_settings.setting_name == 'pub-id::doi') & (
                    db.publication_format_settings.publication_format_id == publication_format_settings.first()[
                'publication_format_id']) & (
                    publication_format_settings.first()['setting_value'] == myconf.take('omp.doi_format_name'))).select(
            db.publication_format_settings.setting_value).first()
    return publication_format_settings_doi


def get_publication_format_settings(book_id):
    publication_format_settings = db(
            (db.publication_format_settings.setting_name == 'name') & (
                    db.publication_formats.submission_id == book_id['submission_id']) & (
                    db.publication_formats.publication_format_id ==
                    db.publication_format_settings.publication_format_id)).select(
            db.publication_format_settings.publication_format_id,
            db.publication_format_settings.setting_value)
    return publication_format_settings


def csl():
    if request.args:
        submission_id = request.args[0]
    else:
        raise HTTP(405, "Missing submission ID and getting of all submissions not supported")
    locale = 'de_DE'
    if session.forced_language == 'en':
        locale = 'en_US'
    ompcsl = OMPCSL(OMPDAL(db, myconf), myconf, locale)
    response.headers['Content-Type'] = 'application/json'
    try:
        cls_data = ompcsl.load_csl_data(submission_id)
    except ValueError as e:
        # Invalid argument
        raise HTTP(400, e.message)

    return sj.dumps(cls_data, separators=(',', ':'), sort_keys=True)
