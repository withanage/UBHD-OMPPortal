# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''

import os
from operator import itemgetter
from ompdal import OMPDAL, OMPSettings, OMPItem
from ompformat import dateFromRow, seriesPositionCompare
from ompstats import OMPStats
from datetime import datetime

def series():
    if session.forced_language == 'en':
        locale = 'en_US'
    elif session.forced_language == 'de':
        locale = 'de_DE'
    else:
        locale = ''

    ignored_submission_id = myconf.take('omp.ignore_submissions') if myconf.take('omp.ignore_submissions') else -1
    
    if request.args == []:
        redirect( URL('home', 'index'))
    series_path = request.args[0]
    
    ompdal = OMPDAL(db, myconf)
    
    press = ompdal.getPress(myconf.take('omp.press_id'))
    if not press:
        redirect(URL('home', 'index'))
    
    series_row = ompdal.getSeriesByPathAndPress(series_path, press.press_id)
    
    # If series path is unknown
    if not series_row:
        redirect(URL('home', 'index'))
        
    series = OMPItem(series_row, OMPSettings(ompdal.getSeriesSettings(series_row.series_id)))
    submission_rows = ompdal.getSubmissionsBySeries(series_row.series_id, ignored_submission_id=ignored_submission_id, status=3)
    
    submissions = []
    for submission_row in submission_rows:
        authors = [OMPItem(author, OMPSettings(ompdal.getAuthorSettings(author.author_id))) for author in ompdal.getAuthorsBySubmission(submission_row.submission_id)]
        editors = [OMPItem(editor, OMPSettings(ompdal.getAuthorSettings(editor.author_id))) for editor in ompdal.getEditorsBySubmission(submission_row.submission_id)]
        submission = OMPItem(submission_row,
                             OMPSettings(ompdal.getSubmissionSettings(submission_row.submission_id)),
                             {'authors': authors, 'editors': editors}
        )
        
        submissions.append(submission)

    submissions = sorted(submissions, cmp=seriesPositionCompare, reverse=True)
    series.associated_items['submissions'] = submissions

    return locals()

def index():
    if session.forced_language == 'en':
        locale = 'en_US'
    elif session.forced_language == 'de':
        locale = 'de_DE'
    else:
        locale = ''
    
    ompdal = OMPDAL(db, myconf)
    
    press = ompdal.getPress(myconf.take('omp.press_id'))
    if not press:
        redirect(URL('home', 'index'))            
    press_settings = OMPSettings(ompdal.getPressSettings(press.press_id))
    
    ignored_submission_id =  myconf.take('omp.ignore_submissions') if myconf.take('omp.ignore_submissions') else -1

    submissions = []
    for submission_row in ompdal.getSubmissionsByPress(press.press_id, ignored_submission_id):
        authors = [OMPItem(author, OMPSettings(ompdal.getAuthorSettings(author.author_id))) for author in ompdal.getAuthorsBySubmission(submission_row.submission_id)]
        editors = [OMPItem(editor, OMPSettings(ompdal.getAuthorSettings(editor.author_id))) for editor in ompdal.getEditorsBySubmission(submission_row.submission_id)]
        publication_dates = [dateFromRow(pd) for pf in ompdal.getAllPublicationFormatsBySubmission(submission_row.submission_id, available=True, approved=True) 
                                for pd in ompdal.getPublicationDatesByPublicationFormat(pf.publication_format_id)]
        submission = OMPItem(submission_row,
                             OMPSettings(ompdal.getSubmissionSettings(submission_row.submission_id)),
                             {'authors': authors, 'editors': editors}
        )
        series_row = ompdal.getSeries(submission_row.series_id)
        if series_row:
            submission.associated_items['series'] = OMPItem(series_row, OMPSettings(ompdal.getSeriesSettings(series_row.series_id)))
        if publication_dates:
            submission.associated_items['publication_dates'] = publication_dates
            
        submissions.append(submission)

    submissions = sorted(submissions, key=lambda s: min(s.associated_items.get('publication_dates', [datetime(1, 1, 1)])), reverse = True)
    
    return locals()

def book():
    if session.forced_language == 'en':
        locale = 'en_US'
    elif session.forced_language == 'de':
        locale = 'de_DE'
    else:
        locale = ''

    submission_id = request.args[0] if request.args else redirect(
        URL('home', 'index'))
    
    ompdal = OMPDAL(db, myconf)
    
    press = ompdal.getPress(myconf.take('omp.press_id'))
    if not press:
        redirect(URL('home', 'index'))
    press_settings = OMPSettings(ompdal.getPressSettings(press.press_id))
    
    # Get basic submission info (check, if submission is associated with the actual press and if the submission has been published)
    submission = ompdal.getPublishedSubmission(submission_id, press_id=myconf.take('omp.press_id'))    
    if not submission:
        redirect(URL('home', 'index'))

    submission_settings = OMPSettings(ompdal.getSubmissionSettings(submission_id))
    
    # Get contributors and contributor settings
    authors = []
    for author in ompdal.getAuthorsBySubmission(submission_id):
        authors.append(OMPItem(author, OMPSettings(ompdal.getAuthorSettings(author.author_id))))
    
    editors = []
    for editor in ompdal.getEditorsBySubmission(submission_id):
        editors.append(OMPItem(editor, OMPSettings(ompdal.getAuthorSettings(editor.author_id))))
    
    # Get chapters and chapter authors
    chapters = []
    for chapter in ompdal.getChaptersBySubmission(submission_id):
        chapters.append(OMPItem(chapter,
                             OMPSettings(ompdal.getChapterSettings(chapter.chapter_id)),
                             {'authors': [OMPItem(a, OMPSettings(ompdal.getAuthorSettings(a.author_id))) for a in ompdal.getAuthorsByChapter(chapter.chapter_id)]})
        )
        
    # Get digital publication formats, settings, files, and identification codes
    digital_publication_formats = []
    for pf in ompdal.getDigitalPublicationFormats(submission_id, available=True, approved=True):
        digital_publication_formats.append(OMPItem(pf, 
            OMPSettings(ompdal.getPublicationFormatSettings(pf.publication_format_id)),
            {'full_file': ompdal.getLatestRevisionOfFullBookFileByPublicationFormat(submission_id, pf.publication_format_id),
             'identification_codes': ompdal.getIdentificationCodesByPublicationFormat(pf.publication_format_id),
             'publication_dates': ompdal.getPublicationDatesByPublicationFormat(pf.publication_format_id)})
        )
        for chapter in chapters:
            chapter_file = ompdal.getLatestRevisionOfChapterFileByPublicationFormat(chapter.attributes.chapter_id, pf.publication_format_id)
            if chapter_file:
                chapter.associated_items.setdefault('files', {})[pf.publication_format_id] = chapter_file
            
    # Get physical publication formats, settings, and identification codes
    physical_publication_formats = []
    for pf in ompdal.getPhysicalPublicationFormats(submission_id, available=True, approved=True):
        physical_publication_formats.append(OMPItem(pf, 
            OMPSettings(ompdal.getPublicationFormatSettings(pf.publication_format_id)),
            {'identification_codes': ompdal.getIdentificationCodesByPublicationFormat(pf.publication_format_id),
             'publication_dates': ompdal.getPublicationDatesByPublicationFormat(pf.publication_format_id)})
        )
    
    pdf = ompdal.getPublicationFormatByName(submission_id, myconf.take('omp.doi_format_name')).first()
    # Get DOI from the format marked as DOI carrier
    if pdf:
        doi = OMPSettings(ompdal.getPublicationFormatSettings(pdf.publication_format_id)).getLocalizedValue("pub-id::doi", "")    # DOI always has empty locale
    else:
        doi = ""
        
    def get_first(l):
        if l:
            return l[0]
        else:
            return None
    
    date_published = None
    # Get the OMP publication date (column publication_date contains latest catalog entry edit date.) Try:
    # 1. Custom publication date entered for a publication format calles "PDF"
    if pdf:
        date_published = get_first([dateFromRow(pd) for pd in ompdal.getPublicationDatesByPublicationFormat(pdf.publication_format_id) if pd.role=="01"])
    # 2. Date on which the catalog entry was first published
    if not date_published:
        date_published = get_first([pd.date_logged for pd in ompdal.getMetaDataPublishedDates(submission_id)])
    # 3. Date on which the submission status was last modified (always set)
    if not date_published:
        date_published = submission.date_status_modified
        
    series = ompdal.getSeriesBySubmissionId(submission_id)
    if series:
        series = OMPItem(series, OMPSettings(ompdal.getSeriesSettings(series.series_id)))
    
    # Get purchase info
    representatives = ompdal.getRepresentativesBySubmission(submission_id, myconf.take('omp.representative_id_type'))
    
    stats = OMPStats(myconf, db, locale)

    return locals()
