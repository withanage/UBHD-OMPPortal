# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''

from ompdal import OMPDAL, OMPSettings, OMPItem
from ompformat import dateFromRow, seriesPositionCompare
from datetime import datetime
from ompsolr import OMPSOLR
import json


def category():



    ignored_submission_id = myconf.take('omp.ignore_submissions') if myconf.take(
        'omp.ignore_submissions') else -1

    if request.args == []:
        redirect(URL('home', 'index'))
    category_path = request.args[0]

    ompdal = OMPDAL(db, myconf)

    press = ompdal.getPress(myconf.take('omp.press_id'))
    if not press:
        redirect(URL('home', 'index'))

    category_row = ompdal.getCategoryByPathAndPress(
        category_path, press.press_id)

    if not category_row:
        redirect(URL('home', 'index'))

    category = OMPItem(category_row, OMPSettings(
        ompdal.getCategorySettings(category_row.category_id)))
    submission_rows = ompdal.getSubmissionsByCategory(
        category_row.category_id, ignored_submission_id=ignored_submission_id, status=3)
    submissions = []
    for submission_row in submission_rows:
        authors = [OMPItem(author, OMPSettings(ompdal.getAuthorSettings(author.author_id))) for author in
                   ompdal.getAuthorsBySubmission(submission_row.submission_id)]
        editors = [OMPItem(editor, OMPSettings(ompdal.getAuthorSettings(editor.author_id))) for editor in
                   ompdal.getEditorsBySubmission(submission_row.submission_id)]
        submission = OMPItem(submission_row,
                             OMPSettings(ompdal.getSubmissionSettings(
                                 submission_row.submission_id)),
                             {'authors': authors, 'editors': editors}
                             )
        series_row = ompdal.getSeries(submission_row.series_id)
        if series_row:
            submission.associated_items['series'] = OMPItem(
                series_row, OMPSettings(ompdal.getSeriesSettings(series_row.series_id)))

        category_row = ompdal.getCategoryBySubmissionId(submission_row.submission_id)
        if category_row:
            submission.associated_items['category'] = OMPItem(
                category_row, OMPSettings(ompdal.getCategorySettings(category_row.category_id)))

        submissions.append(submission)

    submissions = sorted(submissions, key=lambda s: s.attributes['series_id'], reverse=True)


    return locals()


def series():

    ignored_submission_id = myconf.take('omp.ignore_submissions') if myconf.take(
        'omp.ignore_submissions') else -1

    if not request.args:
        redirect(URL('home', 'index'))
    series_path = request.args[0]

    ompdal = OMPDAL(db, myconf)

    press = ompdal.getPress(myconf.take('omp.press_id'))
    if not press:
        redirect(URL('home', 'index'))

    series_row = ompdal.getSeriesByPathAndPress(series_path, press.press_id)

    # If series path is unknown
    if not series_row:
        redirect(URL('home', 'index'))

    series = OMPItem(series_row, OMPSettings(
        ompdal.getSeriesSettings(series_row.series_id)))
    submission_rows = ompdal.getSubmissionsBySeries(
        series_row.series_id, ignored_submission_id=ignored_submission_id, status=3)

    submissions = []
    for submission_row in submission_rows:
        authors = [OMPItem(author, OMPSettings(ompdal.getAuthorSettings(author.author_id)))
                   for author in ompdal.getAuthorsBySubmission(submission_row.submission_id)]
        editors = [OMPItem(editor, OMPSettings(ompdal.getAuthorSettings(editor.author_id)))
                   for editor in ompdal.getEditorsBySubmission(submission_row.submission_id)]
        submission = OMPItem(submission_row,
                             OMPSettings(ompdal.getSubmissionSettings(
                                 submission_row.submission_id)),
                             {'authors': authors, 'editors': editors}
                             )

        category_row = ompdal.getCategoryBySubmissionId(submission_row.submission_id)
        if category_row:
            submission.associated_items['category'] = OMPItem(
                category_row, OMPSettings(ompdal.getCategorySettings(category_row.category_id)))

        submissions.append(submission)

    submissions = sorted(submissions, cmp=seriesPositionCompare, reverse=True)
    series.associated_items['submissions'] = submissions

    return locals()



def search():
    title = '{}'.format(request.vars.title) if request.vars.title else ''
    press_id = request.vars.press_id if request.vars.press_id else ''

    form = form = SQLFORM.factory(
        Field("title"),
        Field("press_id"),
        formstyle='divs',
        submit_button="Search",
    )
    if form.process().accepted:
        title = form.vars.title

    sort= ['title_de','title_en']
    start= 0
    rows =10
    fq = {'title_en':'*','locale': 'de'}
    exc = {'submission_id':'42'}
    fl = ['title_de','submission_id','press_id','title_en']

    if myconf.take("plugins.solr") == str(1):
        solr = OMPSOLR(db,myconf)
        #r = solr.si.query(solr.si.Q(title_en=title)  | solr.si.Q(title_de=title))
        r = solr.si.query('aktuelle*')
        #for s in sort:
        #    r =r.sort_by(s)
        #r = r.filter(**fq)
        #r = r.exclude(**exc)
        #r = r.field_limit(fl)
        #r = r.highlight(q.keys())
        r= r.paginate(start=start, rows=rows)
        results = r.execute()
        #hl = results.highlighting

    from paginate import Page, make_html_tag

    def paginate_link_tag(item):
        """
        Create an A-HREF tag that points to another page usable in paginate.
        """
        a_tag = Page.default_link_tag(item)
        if item['type'] == 'current_page':
            return make_html_tag('li', a_tag, **{'class': 'active'})
        return make_html_tag('li', a_tag)


    p = Page(['test','test2'], page=15, items_per_page=15, item_count=10)

    return  locals()




def index():
    def create_pagination(total, per_page, current):
        li = []
        al = {'_aria-label': "Page navigation"}
        for i in range(0, total):
            l = A(i + 1, _href=URL('index?page_nr=' + str(i + 1)))
            li.append(LI(l, _class="active")) if i == current  else li.append(LI(l))
        return TAG.nav(UL(li, _class="pagination"), **al)

    def create_per_page_nav():
        li = [LI(A(i, _href=URL('index?per_page=' + str(i)))) for i in [2,3,4]]
        ul =UL(li, _class="dropdown-menu")
        button_cs= { "_type":"button", "_class":"btn btn-default dropdown-toggle","_data-toggle":"dropdown", "_aria-haspopup":"true","_aria-expanded":"false"}
        button =TAG.button("Results per Page",SPAN(_class='caret'),**button_cs )
        return  DIV(button,ul,_class="btn-group")

    def create_sort(submissions, sort_by):
        results = sorted(submissions, key=lambda s: min(s.associated_items.get('publication_dates', [datetime(1, 1, 1)])),
               reverse=False)
        if sort_by=="title":
            results = sorted(submissions, key=lambda s: s.settings.getLocalizedValue('title', locale).lower(), reverse=False)
        elif sort_by=="category":
            results = sorted(submissions, key=lambda s: s.associated_items.get('category'), reverse=False)
        return results

    def create_sort_nav():
        li = [LI(A(i, _href=URL('index?sort_by=' + str(i)))) for i in ["title","date","category"]]
        ul =UL(li, _class="dropdown-menu")
        button_cs= { "_type":"button", "_class":"btn btn-default dropdown-toggle","_data-toggle":"dropdown", "_aria-haspopup":"true","_aria-expanded":"false"}
        button =TAG.button(T("sort by"),SPAN(_class='caret'),**button_cs )
        return  DIV(button,ul,_class="btn-group")

    ompdal = OMPDAL(db, myconf)
    press = ompdal.getPress(myconf.take('omp.press_id'))
    sort_by = request.vars.get('sort_by')
    session.sort_by = sort_by if sort_by else session.get('sort_by','date')



    per_page = request.vars.get('per_page')
    if per_page :
        session.catalog_per_page = int(per_page)

    per_page = int(session.get('catalog_per_page', 20))

    page_nr = int(request.vars.get('page_nr',1))-1



    if not press:
        redirect(URL('home', 'index'))
    press_settings = OMPSettings(ompdal.getPressSettings(press.press_id))

    ignored_submission_id = myconf.take('omp.ignore_submissions') if myconf.take(
        'omp.ignore_submissions') else -1

    submissions = []
    submission_rows = ompdal.getSubmissionsByPress(press.press_id, ignored_submission_id)

    for submission_row in submission_rows:
        authors = [OMPItem(author, OMPSettings(ompdal.getAuthorSettings(author.author_id)))
                   for author in ompdal.getAuthorsBySubmission(submission_row.submission_id)]
        editors = [OMPItem(editor, OMPSettings(ompdal.getAuthorSettings(editor.author_id)))
                   for editor in ompdal.getEditorsBySubmission(submission_row.submission_id)]
        publication_dates = [dateFromRow(pd) for pf in ompdal.getAllPublicationFormatsBySubmission(submission_row.submission_id, available=True, approved=True)
                             for pd in ompdal.getPublicationDatesByPublicationFormat(pf.publication_format_id)]
        submission = OMPItem(submission_row,
                             OMPSettings(ompdal.getSubmissionSettings(
                                 submission_row.submission_id)),
                             {'authors': authors, 'editors': editors}
                             )
        category_row = ompdal.getCategoryBySubmissionId(
            submission_row.submission_id)
        if category_row:
            submission.associated_items['category'] = OMPItem(
                category_row, OMPSettings(ompdal.getCategorySettings(category_row.category_id)))

        series_row = ompdal.getSeries(submission_row.series_id)
        if series_row:
            submission.associated_items['series'] = OMPItem(
                series_row, OMPSettings(ompdal.getSeriesSettings(series_row.series_id)))
        if publication_dates:
            submission.associated_items['publication_dates'] = publication_dates

        submissions.append(submission)

    submissions = create_sort(submissions,session.get('sort_by'))

    submissions = submissions[page_nr*per_page:(page_nr+1)*(per_page)]

    pages = len(submission_rows)/per_page
    if len(submission_rows) % per_page >0:
        pages = pages +1
    pagination = create_pagination(pages, per_page, page_nr)
    results_per_page = create_per_page_nav()
    sort_nav = create_sort_nav()

    return locals()


def book():

    submission_id = request.args[0] if request.args else redirect(
        URL('home', 'index'))

    ompdal = OMPDAL(db, myconf)

    press = ompdal.getPress(myconf.take('omp.press_id'))
    if not press:
        redirect(URL('home', 'index'))
    press_settings = OMPSettings(ompdal.getPressSettings(press.press_id))

    # Get basic submission info (check, if submission is associated with the
    # actual press and if the submission has been published)
    submission = ompdal.getPublishedSubmission(
        submission_id, press_id=myconf.take('omp.press_id'))
    if not submission:
        redirect(URL('home', 'index'))

    submission_settings = OMPSettings(
        ompdal.getSubmissionSettings(submission_id))

    # Get contributors and contributor settings
    editor_rows = ompdal.getEditorsBySubmission(submission_id)
    editors = [OMPItem(e, OMPSettings(ompdal.getAuthorSettings(e.author_id)))
               for e in editor_rows]

    # Do not load authors if the submission has editors
    authors = [] if editors else [OMPItem(a, OMPSettings(ompdal.getAuthorSettings(a.author_id))) for a in
                                  ompdal.getActualAuthorsBySubmission(submission_id, filter_browse=True)]

    # Get chapters and chapter authors
    chapters = []
    for chapter in ompdal.getChaptersBySubmission(submission_id):
        chapters.append(OMPItem(chapter,
                                OMPSettings(ompdal.getChapterSettings(
                                    chapter.chapter_id)),
                                {'authors': [OMPItem(a, OMPSettings(ompdal.getAuthorSettings(a.author_id))) for a in ompdal.getAuthorsByChapter(chapter.chapter_id)]})
                        )

    # Get digital publication formats, settings, files, and identification codes
    digital_publication_formats = []
    for pf in ompdal.getDigitalPublicationFormats(submission_id, available=True, approved=True):
        publication_format = OMPItem(pf,
                                     OMPSettings(ompdal.getPublicationFormatSettings(
                                         pf.publication_format_id)),
                                     {'identification_codes': ompdal.getIdentificationCodesByPublicationFormat(pf.publication_format_id),
                                         'publication_dates': ompdal.getPublicationDatesByPublicationFormat(pf.publication_format_id)}
                                     )
        full_file = ompdal.getLatestRevisionOfFullBookFileByPublicationFormat(
            submission_id, pf.publication_format_id)
        if full_file:
            publication_format.associated_items['full_file'] = OMPItem(
                full_file, OMPSettings(ompdal.getSubmissionFileSettings(full_file.file_id)))
        digital_publication_formats.append(publication_format)

        for chapter in chapters:
            chapter_file = ompdal.getLatestRevisionOfChapterFileByPublicationFormat(
                chapter.attributes.chapter_id, pf.publication_format_id)
            if chapter_file:
                chapter.associated_items.setdefault('files', {})[pf.publication_format_id] = OMPItem(
                    chapter_file, OMPSettings(ompdal.getSubmissionFileSettings(chapter_file.file_id)))

    # Get physical publication formats, settings, and identification codes
    physical_publication_formats = []
    for pf in ompdal.getPhysicalPublicationFormats(submission_id, available=True, approved=True):
        physical_publication_formats.append(OMPItem(pf,
                                                    OMPSettings(ompdal.getPublicationFormatSettings(
                                                        pf.publication_format_id)),
                                                    {'identification_codes': ompdal.getIdentificationCodesByPublicationFormat(pf.publication_format_id),
                                                        'publication_dates': ompdal.getPublicationDatesByPublicationFormat(pf.publication_format_id)})
                                            )

    pdf = ompdal.getPublicationFormatByName(
        submission_id, myconf.take('omp.doi_format_name')).first()
    # Get DOI from the format marked as DOI
    if pdf:
        doi = OMPSettings(ompdal.getPublicationFormatSettings(pdf.publication_format_id)).getLocalizedValue(
            "pub-id::doi", "")    # DOI always has empty locale
    else:
        doi = ""


    date_published = None
    date_first_published = None
    # Get the OMP publication date (column publication_date contains latest catalog entry edit date.) Try:
    # 1. Custom publication date entered for a publication format calles "PDF"
    if pdf:
        date_published = dateFromRow(ompdal.getPublicationDatesByPublicationFormat(pdf.publication_format_id, "01")
                                     .first())
        date_first_published = dateFromRow(ompdal.getPublicationDatesByPublicationFormat(pdf.publication_format_id, "11")
                                           .first())
    # 2. Date on which the catalog entry was first published
    if not date_published:
        metadatapublished_date = ompdal.getMetaDataPublishedDates(submission_id).first()
        date_published = metadatapublished_date.date_logged if metadatapublished_date else None
    # 3. Date on which the submission status was last modified (always set)
    if not date_published:
        date_published = submission.date_status_modified

    series = ompdal.getSeriesBySubmissionId(submission_id)
    if series:
        series = OMPItem(series, OMPSettings(
            ompdal.getSeriesSettings(series.series_id)))

    # Get purchase info
    representatives = ompdal.getRepresentativesBySubmission(
        submission_id, myconf.take('omp.representative_id_type'))

    #stats = OMPStats(myconf, db, locale)

    return locals()
