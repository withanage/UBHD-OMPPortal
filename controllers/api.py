# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''
import gluon.contrib.simplejson as sj


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
    filter_ids = []
    if request.vars.ids:
        filter_ids = request.vars.ids.split(',')

    for book_id in submissions:

        # full book
        publication_format_settings = db(
            (db.publication_format_settings.setting_name == 'name') & (
                db.publication_format_settings.locale == locale) & (
                db.publication_formats.submission_id == book_id['submission_id']) & (
                db.publication_formats.publication_format_id == db.publication_format_settings.publication_format_id)).select(
                    db.publication_format_settings.publication_format_id,
            db.publication_format_settings.setting_value)
        if publication_format_settings:
            publication_format_settings_doi = db(
                (db.publication_format_settings.setting_name == 'pub-id::doi') & (
                    db.publication_format_settings.publication_format_id == publication_format_settings.first()['publication_format_id']) & (
                    publication_format_settings.first()['setting_value'] == myconf.take('omp.doi_format_name'))).select(
                db.publication_format_settings.setting_value).first()

        if book_id.setting_name == 'title':
            title = book_id.setting_value

        authors = {}
        authors_list = db(
            (db.authors.submission_id == book_id.submission_id)).select(
            db.authors.first_name, db.authors.last_name)
        for i in authors_list:
            authors['type'] = 'person'
            authors['relation'] = 'creators'
            authors['label'] = i.first_name + " " + i.last_name

        ##
        full_files = db(
            (db.submission_files.genre_id == myconf.take('omp.monograph_type_id')) & (
                db.submission_files.file_stage > 5) & (
                db.submission_files.submission_id == book_id.submission_id)).select(
            db.submission_files.submission_id,
            db.submission_files.file_id,
            db.submission_files.original_file_name)

        for f in full_files:
            full = {}
            full["label"] = title
            full["type"] = "volume"
            full["associate_via_hierarchy"] = [authors]
            full["norm_id"] = str(book_id.submission_id)
            file_name = str(book_id.submission_id)+'-'+str(f.file_id)+'-'+str(f.original_file_name.rsplit('.')[1])
            for j in filter_ids:
                    if file_name == str(j):
                      subs[file_name] = full

        
        fullbook = {}
        fullbook["label"] = title
        fullbook["type"] = "volume"

        if publication_format_settings_doi:
            fullbook["norm_id"] = publication_format_settings_doi['setting_value']
        fullbook["associate_via_hierarchy"] = [authors]

        '''
      if request.vars.ids:
        for j in filter_ids:
          if str(j) == str(book_id.submission_id):
            subs[book_id.submission_id] = fullbook

      else:
          subs[book_id.submission_id] = fullbook
      '''

        chapters = db(
            (db.submission_chapters.submission_id == book_id['submission_id']) & (
                db.submission_file_settings.setting_name == 'chapterID') & (
                db.submission_file_settings.setting_value == db.submission_chapters.chapter_id)).select(
            db.submission_chapters.chapter_id,
            db.submission_file_settings.file_id,
            orderby=db.submission_chapters.chapter_seq)
        for c in chapters:
            chapter_id = str(book_id['submission_id']) + '-' + \
                str(c['submission_chapters']['chapter_id'])
            type = db(db.submission_files.file_id == c['submission_file_settings']['file_id']).select(
                db.submission_files.original_file_name).first()['original_file_name'].rsplit('.')[1]
            file_id = str(book_id['submission_id']) + '-' + \
                str(c['submission_file_settings']['file_id']) + '-' + str(type)
            part_filter = False
            if request.vars.ids:
                for j in filter_ids:
                    if str(file_id) == str(j):
                        part_filter = True
            if part_filter:
                subs[file_id] = []
                part_title = db(
                    (db.submission_chapter_settings.chapter_id == int(
                        c['submission_chapters']['chapter_id'])) & (
                        db.submission_chapter_settings.locale == locale) & (
                        db.submission_chapter_settings.setting_name == 'title')).select(
                    db.submission_chapter_settings.setting_value).first()
                bookpart = {}
                if part_title:
                    bookpart["label"] = part_title['setting_value']
                bookpart["norm_id"] = myconf.take('oastatistik.id') + ':' + chapter_id
                bookpart["type"] = "part"
                part_authors = []
                author_id_list = db(
                    db.submission_chapter_authors.chapter_id == int(
                        c['submission_chapters']['chapter_id'])).select(
                    db.submission_chapter_authors.author_id,
                    orderby=db.submission_chapter_authors.seq)
                for author in author_id_list:
                    part_authors.append({"type": "person"})
                    part_authors.append({"relation": "creators"})
                    author_name = db(
                        (db.authors.author_id == author['author_id'])).select(
                        db.authors.first_name, db.authors.last_name).first()
                    if author_name:
                        part_authors.append(
                            {'name': author_name['first_name'] + " " + author_name['last_name']})
                if part_authors:
                    bookpart["associate_via_hierarchy"] = [part_authors]
                subs[file_id] = bookpart
                subs[file_id]["associate_via_hierarchy"] = [fullbook]
           

    return sj.dumps(subs, separators=(',', ':'), sort_keys=True)
