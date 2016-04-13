# -*- coding: utf-8 -*-
import urllib
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''
import os
from ompdal import OMPDAL


def index():
    locale = 'de_DE'
    if session.forced_language == 'en':
        locale = 'en_US'
    ignored_submissions =  myconf.take('omp.ignore_submissions') if myconf.take('omp.ignore_submissions') else -1
    query = ((db.submissions.context_id == myconf.take('omp.press_id')) & (db.submissions.submission_id!=ignored_submissions) & (db.submissions.status == 3) & (
        db.submission_settings.submission_id == db.submissions.submission_id) & (db.submission_settings.locale == locale))
    submissions = db(query).select(db.submission_settings.ALL, db.submissions.series_id, db.submissions.series_position,
                                   orderby=~db.submissions.date_submitted)
    subs = {}
    order = []
    series_info = {}
    ompdal = OMPDAL(db, myconf)
    for i in submissions:
        id = i.submission_settings.submission_id
        if id not in order:
            order.append(id)
        setting_name = i.submission_settings.setting_name
        setting_value = i.submission_settings.setting_value
        if setting_name == 'abstract':
            subs.setdefault(id, {})['abstract'] = setting_value
        if setting_name == 'subtitle':
            subs.setdefault(id, {})['subtitle'] = setting_value
        if setting_name == 'title':
            subs.setdefault(id, {})['title'] = setting_value
        subs.setdefault(id, {})['authors'] = ompdal.getAuthors(id)
        for row in ompdal.getPublicationDates(id):
            if row['date_format'] == '00':
                subs[id]['publication_date'] = row['date']
        subs[id]['editors'] = ompdal.getEditors(id)
        subs[id]['series_position'] = i.submissions.series_position
        series_id = i.submissions.series_id
        if series_id != 0:
            subs[id]['series_id'] = series_id
            if series_id not in series_info:
                series_settings = ompdal.getLocalizedSeriesSettings(series_id, locale)
                if not series_settings:
                    series_settings = ompdal.getSeriesSettings(series_id)
                series_info[series_id] = {}
                for s in series_settings:
                    if s.setting_name == 'title':
                        series_info[series_id]['title'] = s.setting_value
                    if s.setting_name == 'subtitle':
                        series_info[series_id]['subtitle'] = s.setting_value

    if len(subs) == 0:
      redirect( URL('home', 'index'))  
    return dict(submissions=submissions, subs=subs, order=order, series_info=series_info)


def book():
    abstract, authors, cleanTitle, publication_format_settings_doi, press_name, subtitle = '', '', '', '', '', ''
    locale = ''
    if session.forced_language == 'en':
        locale = 'en_US'

    if session.forced_language == 'de':
        locale = 'de_DE'
    book_id = request.args[0] if request.args else redirect(
        URL('home', 'index'))

    query = ((db.submission_settings.submission_id == int(book_id))
             & (db.submission_settings.locale == locale))
    book = db(query).select(db.submission_settings.ALL)

    #if len(book) == 0:
    #    redirect(URL('catalog', 'index'))

    author_q = ((db.authors.submission_id == book_id))
    authors_list = db(author_q).select(
        db.authors.first_name, db.authors.last_name)

    for i in authors_list:
        authors += i.first_name + ' ' + i.last_name + ', '
    if authors.endswith(', '):
        authors = authors[:-2]

    author_bio = db((db.authors.submission_id == book_id) & (db.authors.author_id == db.author_settings.author_id) & (
        db.author_settings.locale == locale) & (db.author_settings.setting_name == 'biography')).select(db.author_settings.setting_value).first()

    chapter_query = ((db.submission_chapters.submission_id == book_id) & (db.submission_chapters.chapter_id == db.submission_chapter_settings.chapter_id) & (db.submission_chapter_settings.locale == locale) & (db.submission_file_settings.setting_name ==
                                                                                                                                                                                                                 "chapterID") & (db.submission_file_settings.setting_value == db.submission_chapters.chapter_id) & (db.submission_file_settings.file_id == db.submission_files.file_id) & (db.submission_chapter_settings.setting_name == 'title'))

    chapters = db(chapter_query).select(db.submission_chapters.chapter_id, db.submission_chapter_settings.setting_value, db.submission_files.assoc_id, db.submission_files.submission_id, db.submission_files.genre_id,
                                        db.submission_files.file_id, db.submission_files.revision, db.submission_files.file_stage, db.submission_files.date_uploaded, orderby=[db.submission_chapters.chapter_id, db.submission_files.assoc_id])

    pub_query = (db.publication_formats.submission_id == book_id) & (db.publication_format_settings.publication_format_id == db.publication_formats.publication_format_id) & (
        db.publication_format_settings.locale == locale)

    publication_formats = db(pub_query & (db.publication_format_settings.setting_value != myconf.take('omp.ignore_format'))).select(db.publication_format_settings.setting_name, db.publication_format_settings.setting_value,
                                                                                                                                    db.publication_formats.publication_format_id, groupby=db.publication_formats.publication_format_id, orderby=db.publication_formats.publication_format_id)

    press_settings = db(db.press_settings.press_id == myconf.take('omp.press_id')).select(
        db.press_settings.setting_name, db.press_settings.setting_value)

    publication_format_settings = db((db.publication_format_settings.setting_name == 'name') & (db.publication_format_settings.locale == locale) & (db.publication_formats.submission_id == book_id) & (
        db.publication_formats.publication_format_id == db.publication_format_settings.publication_format_id)).select(db.publication_format_settings.publication_format_id, db.publication_format_settings.setting_value)

    if publication_format_settings:
        publication_format_settings_doi = db((db.publication_format_settings.setting_name == 'pub-id::doi') & (db.publication_format_settings.publication_format_id == publication_format_settings.first(
        )['publication_format_id']) & (publication_format_settings.first()['setting_value'] == myconf.take('omp.doi_format_name'))).select(db.publication_format_settings.setting_value).first()

    identification_codes = {}
    identification_codes_publication_formats = db(
        db.publication_formats.submission_id == book_id).select(
        db.publication_formats.publication_format_id)

    for i in identification_codes_publication_formats:
        name = db(
            (db.publication_format_settings.locale == locale) & (
                db.publication_format_settings.publication_format_id == i['publication_format_id']) & (
                db.publication_format_settings.setting_name == 'name') & (
                db.publication_format_settings.setting_value != myconf.take('omp.xml_category_name'))) .select(
                    db.publication_format_settings.setting_value).first()
        identification_code = db(
            (db.identification_codes.publication_format_id == i['publication_format_id']) & (
                db.identification_codes.code == 15)).select(
            db.identification_codes.value).first()
        if name and identification_code:
            identification_codes[
                identification_code['value']] = name['setting_value']

    published_date = db(pub_query & (db.publication_format_settings.setting_value == myconf.take('omp.doi_format_name')) & (
        db.publication_dates.publication_format_id == db.publication_format_settings.publication_format_id)).select(db.publication_dates.date)

    representatives = db(
        (db.representatives.submission_id == book_id) & (
            db.representatives.representative_id_type == myconf.take('omp.representative_id_type'))).select(
        db.representatives.name,
        db.representatives.url,
        orderby=db.representatives.representative_id)

    full_files = db((db.submission_files.submission_id == book_id) & (db.submission_files.genre_id == myconf.take('omp.monograph_type_id'))).select(db.submission_files.original_file_name, db.submission_files.submission_id, db.submission_files.genre_id,
    #full_files = db((db.submission_files.submission_id == book_id) & (db.submission_files.file_stage >= 5)).select(db.submission_files.original_file_name, db.submission_files.submission_id, db.submission_files.genre_id,
                                                                                                                                                    db.submission_files.file_id, db.submission_files.revision, db.submission_files.file_stage, db.submission_files.date_uploaded)

    for j in press_settings:
        if j.setting_name == 'name':
            press_name = j.setting_value

    for i in book:
        if i.setting_name == 'abstract':
            abstract = i.setting_value
        if i.setting_name == 'subtitle':
            subtitle = i.setting_value
        if i.setting_name == 'title':
            cleanTitle = i.setting_value

    cover_image=''
    path=request.folder+'static/monographs/'+book_id+'/simple/cover.'
    for t in ['jpg','png','gif']:
        if os.path.exists(path+t):
                cover_image= URL(myconf.take('web.application'), 'static','monographs/' + book_id + '/simple/cover.'+t)

    if  int(myconf.take('omp.vgwort_enable')) == 1 :
	vgwort_server=myconf.take('web.vgwort_server1')
    	if urllib.urlopen(vgwort_server).getcode()!=200:
		gwort_server=myconf.take('web.vgwort_server2')
		if urllib.urlopen(vgwort_server).getcode()!=200:
			vgwort_server= None
    else:
	vgwort_server= None


    return dict(abstract=abstract, authors=authors, author_bio=author_bio, book_id=book_id, chapters=chapters, cleanTitle=cleanTitle, cover_image=cover_image, full_files=full_files, identification_codes=identification_codes,
                publication_formats=publication_formats, publication_format_settings_doi=publication_format_settings_doi, published_date=published_date, subtitle=subtitle, press_name=press_name, representatives=representatives,vgwort_server=vgwort_server)
