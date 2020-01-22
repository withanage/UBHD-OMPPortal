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
from ompformat import dateFromRow, seriesPositionCompare, formatDoi, dateToStr, downloadLink
import re
import json

response.headers['Content-Type'] = 'application/json'
response.view = 'generic.json'
url = join(request.env.http_host, request.application, request.controller)

ompdal = OMPDAL(db, myconf)
press = ompdal.getPress(myconf.take('omp.press_id'))
STATUS_PUBLISHED = 3
locale = ''

if session.forced_language == 'en':
    locale = 'en_US'
elif session.forced_language == 'de':
    locale = 'de_DE'


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


def getAuthorList(contribs):
    authors = []
    for contrib in contribs:

        author = {}
        author_settings = ompdal.getAuthorSettings(contrib["author_id"]).as_list()
        for setting in author_settings:
            author[setting['setting_name']] = setting["setting_value"]
        authors.append(author)
    return authors


def submissions():
    # apiToken = myconf.take('web.api_token')

    # if apiToken != request.vars.get('apiToken'):
    #    raise HTTP(404,"Error")

    result = {}
    items = []
    context_id = myconf.take('omp.press_id')
    db_submissions = db.submissions

    q = ((db_submissions.context_id == context_id) & (db_submissions.status == STATUS_PUBLISHED))
    submissions = db(q).select(orderby=(db_submissions.submission_id)).as_list()

    for s in submissions:
        item = {}
        item["id"] = s["submission_id"]
        item["locale"] = s["locale"]
        item["dateSubmitted"] = str(s["date_submitted"])
        item["lastModified"] = str(s["last_modified"])
        item["dateStatusModified"] = str(s["date_status_modified"])


        items.append(item)

    result["itemsMax"] = len(submissions)
    result["items"] = items

    return sj.dumps(result, separators=(',', ':'))


def submission():

    if len(request.args) == 0 :
        raise HTTP(404)
    submission_id = request.args[0]

    context_id = myconf.take('omp.press_id')
    db_submissions = db.submissions

    q = ((db_submissions.context_id == context_id) & (db_submissions.status == STATUS_PUBLISHED) & (db_submissions.submission_id==submission_id))
    submissions = db(q).select(orderby=(db_submissions.submission_id))
    if submissions:
        submission = submissions.first()
    else:
        raise HTTP(404)

    item = {}

    item["id"] = submission_id
    item["locale"] = submission["locale"]
    item["dateSubmitted"] = str(submission["date_submitted"])
    item["lastModified"] = str(submission["last_modified"])
    item["dateStatusModified"] = str(submission["date_status_modified"])
    # formats
    pf = ompdal.getPublicationFormatByName(submission_id, myconf.take('omp.doi_format_name')).first()
    if pf:
        date_published = dateFromRow(
                ompdal.getPublicationDatesByPublicationFormat(pf.publication_format_id, "01").first())
        item["datePublished"] = str(date_published)
    item["status"] = {"id": STATUS_PUBLISHED, "label": "Published"}
    # submission settings
    submission_settings = ompdal.getSubmissionSettings(submission_id).as_list()
    dc = {"abstract": {}, "prefix": {}, "source": {}, "subtitle": {}, "title": {}, "type": {}}
    for submission in submission_settings:
        for k in dc:
            if submission["setting_name"] == k:
                if not item.get(k):
                    item[k] = {}
                item[k][submission["locale"]] = submission['setting_value']
    # series
    series_id = submission.get("series_id")
    if series_id:
        series = {"id": series_id, "position": submission["series_position"]}
        series_settings = ompdal.getSeriesSettings(series_id)
        for srs in series_settings:
            if srs["setting_name"] == 'title':
                if not series.get("title"):
                    series["title"] = {}
                series["title"][srs["locale"]] = srs["setting_value"]

        item["series"] = series
    # controlled vocabularies
    cv = ompdal.getControlledVocabsBySubmission(submission_id).as_list()
    keywords = ["submissionAgency", "submissionDiscipline", "submissionKeyword", "submissionSubject"]
    for keyword in keywords:
        cv_ids = list(filter(lambda x: x['symbolic'] == keyword, cv))
        cv_id = cv_ids[0]["controlled_vocab_id"] if cv_ids else []
        cv_entries = ompdal.getControlledVocabEntriesByID(cv_id) if cv_id else []

        for i in cv_entries:
            entries = ompdal.controlledVocabEntrySettingsByID(i["controlled_vocab_entry_id"]).as_list()
            entry = entries[0] if entries else []
            if entry:
                if not item.get(keyword):
                    item[keyword] = {}
                if not item[keyword].get(entry['locale']):
                    item[keyword][entry['locale']] = []

                item[keyword][entry['locale']].append(entry["setting_value"])
        if item.get(keyword):
            item[re.sub('^submission', '', keyword).lower()] = item.pop(keyword)
    contribs = ompdal.getAuthorsBySubmission(submission_id).as_list()
    item["authors"] = getAuthorList(contribs)
    category_settings = ompdal.getCategoryBySubmissionId(submission_id)
    # galleys
    galleys = []
    pdfName = "PDF"
    PdfFormats = ompdal.getPublicationFormatByName(submission_id, pdfName)
    for pf in PdfFormats:
        pdfObject = {"id": pf["publication_format_id"], "label": pdfName}

        e_file = ompdal.getLatestRevisionOfFullBookFileByPublicationFormat(submission_id,
                                                                           pf["publication_format_id"])
        pdfObject["urlRemote"] = myconf.take('web.url') + downloadLink(request, e_file, myconf.take('web.url'), [],
                                                                       "")

        fileKeys = ['file_id', 'revision', 'file_stage', 'genre_id', 'original_file_name']
        pdfObject["file"] = {k: e_file.get(k) for k in fileKeys}

        e_file_settings = ompdal.getSubmissionFileSettings(e_file["file_id"]).as_list()

        for setting in e_file_settings:
            if not pdfObject["file"].get(setting['setting_name']):
                pdfObject["file"][setting['setting_name']] = {}
            pdfObject["file"][setting['setting_name']][setting['locale']] = setting["setting_value"]

        for p in ["vgWortPublic", "vgWortPrivate"]:
            if pdfObject["file"].get(p):
                pdfObject["file"].pop(p)

        galleys.append(pdfObject)
    item["galleys"] = galleys
    # chapters
    chapter_rows = ompdal.getChaptersBySubmission(submission_id).as_list()
    chapters = []
    for c in chapter_rows:
        chapter = {}
        chapter['id'] = c["chapter_id"]
        chapter['seq'] = c["seq"]
        chapter_settings = ompdal.getChapterSettings(c["chapter_id"]).as_list()

        contribs = ompdal.getAuthorsByChapter(c["chapter_id"]).as_list()
        chapter["authors"] = getAuthorList(contribs)
        for submission in chapter_settings:
            setting_name = submission["setting_name"]
            if not chapter.get(setting_name):
                chapter[setting_name] = {}
            chapter[setting_name][submission["locale"]] = submission['setting_value']
            galleys = []
            for pf in PdfFormats:
                pdfObject = {"id": pf["publication_format_id"], "label": pdfName}
                chapter_file = ompdal.getLatestRevisionOfChapterFileByPublicationFormat(c["chapter_id"],
                                                                                        pf.publication_format_id)
                if chapter_file:
                    fileKeys = ['file_id', 'revision', 'file_stage', 'genre_id', 'original_file_name']
                    pdfObject["file"] = {k: chapter_file.get(k) for k in fileKeys}
                    pdfObject["urlRemote"] = myconf.take('web.url') + downloadLink(request, chapter_file,
                                                                                   myconf.take('web.url'), [], "")
                    galleys.append(pdfObject)
            if galleys:
                chapter["galleys"] = galleys

        chapters.append(chapter)
    item["chapters"] = chapters
    return sj.dumps(item, separators=(',', ':'))


def oastatistik():
    ompdal = OMPDAL(db, myconf)
    result = []
    locale = 'de_DE'
    context_id = myconf.take('omp.press_id')
    stats_id = myconf.take('statistik.id')
    db_submissions = db.submissions
    q = ((db_submissions.context_id == context_id) & (db_submissions.status == 3))
    submissions = db(q).select(db_submissions.submission_id, orderby=(db_submissions.submission_id))
    press_path = ompdal.getPress(context_id).get('path')

    series_list = ompdal.getSeriesByPress(context_id)

    for series in series_list:
        if series:
            s = {}
            dbs = db.series_settings
            title = db(
                    (dbs.series_id == series.get('series_id')) & (dbs.locale == locale) & (
                            dbs.setting_name == 'title')).select(
                    dbs.setting_value)

            series_norm_id = '{}:{}:{}'.format(stats_id, press_path, series.get('path'))
            s['doc_id'] = series_norm_id
            s['type'] = 'collection'
            s['title'] = title.first().get('setting_value') or ''
            s['id'] = 'MD:{}'.format(series_norm_id)

            result.append(s)

    for submission in submissions:

        submission_id = submission.submission_id
        norm_id = '{}:{}'.format(stats_id, submission_id)

        metadata_published_date = ompdal.getMetaDataPublishedDates(submission_id).first()
        date_published = metadata_published_date.date_logged if metadata_published_date else None
        if not date_published:
            date_published = submission.date_status_modified
        year = date_published.year if date_published else []

        volume = {
            "id"  : 'MD:{}'.format(norm_id),
            "type": "volume",
            }
        if year:
            volume['year'] = year

        volume["doc_id"] = '{}'.format(norm_id)
        # submission
        submission_settings = ompdal.getSubmissionSettings(submission_id).as_list()

        srs = ompdal.getSeriesBySubmissionId(submission_id)
        series_norm_id = '{}:{}:{}'.format(stats_id, press_path, srs.get('path')) if srs else []

        for setting in submission_settings:
            if setting["locale"] == locale and setting["setting_name"] == 'title':
                volume["title"] = setting["setting_value"]
            if setting["setting_name"] == 'pub-id::doi':
                volume["norm_id"] = setting["setting_value"]
            if series_norm_id:
                volume["parent"] = 'MD:{}'.format(series_norm_id)
        result.append(volume)

        chapters = ompdal.getChaptersBySubmission(submission_id).as_list()

        for chapter in chapters:
            chapter_id = chapter["chapter_id"]

            chapter_norm_id = "{}:{}-c{}".format(stats_id, submission_id, chapter_id)
            chs_ = {
                "id"    : 'MD:{}'.format(chapter_norm_id),
                "type"  : "part",
                "parent": 'MD:{}'.format(norm_id),
                "doc_id": chapter_norm_id
                }
            chapter_settings = ompdal.getChapterSettings(chapter_id).as_list()
            for chapter_setting in chapter_settings:
                if chapter_setting["locale"] == locale and chapter_setting["setting_name"] == 'title':
                    chs_["title"] = chapter_setting["setting_value"]
                if chapter_setting["setting_name"] == 'pub-id::doi':
                    chs_["norm_id"] = chapter_setting["setting_value"]

            result.append(chs_)

    return sj.dumps(result, separators=(',', ':'))


def get_submission_files(book_id):
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
    return publication_format_setting


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
