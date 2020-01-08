# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''

from ompdal import OMPDAL, OMPSettings, OMPItem, DOI_SETTING_NAME
from ompformat import dateFromRow, seriesPositionCompare, formatDoi, dateToStr, downloadLink

from ompsolr import OMPSOLR
from ompbrowse import Browser
from gluon import current
import json
from datetime import datetime

ONIX_PRODUCT_IDENTIFIER_TYPE_CODES = {"01": "Proprietary",
                                      "02": "ISBN-10",
                                      "03": "GTIN-13",
                                      "04": "UPC",
                                      "05": "ISMN-10",
                                      "06": "DOI",
                                      "13": "LCCN",
                                      "14": "GTIN-14",
                                      "15": "ISBN",
                                      "17": "Legal deposit number",
                                      "22": "URN",
                                      "23": "OCLC number",
                                      "24": "ISBN",
                                      "25": "ISMN-13",
                                      "26": "ISBN-A",
                                      "27": "JP e-code",
                                      "28": "OLCC number",
                                      "29": "JP Magazine ID",
                                      "30": "UPC12+5",
                                      "31": "BNF Control number",
                                      "35": "ARK"
                                      }
IDENTIFIER_ORDER = ['06', '22.PDF', '15.PDF', '15.Hardcover', '15.Softcover', '15.Print', '15.Online','15.EPUB']

def raise400():
    raise HTTP(400)

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

        publication_dates = [dateFromRow(pd) for pf in
                             ompdal.getAllPublicationFormatsBySubmission(submission_row.submission_id)
                             for pd in ompdal.getPublicationDatesByPublicationFormat(pf.publication_format_id)]
        if publication_dates:
            submission.associated_items['publication_dates'] = publication_dates
        submissions.append(submission)

    sortby = ompdal.getCategorySettings(category_row.category_id).find(
        lambda row: row.setting_name == 'sortOption').first()
    if sortby:
        b = Browser(submissions, 0, locale, 100, sortby.get('setting_value'), [])
        submissions = b.process_submissions(submissions)

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

        publication_dates = [dateFromRow(pd) for pf in
                             ompdal.getAllPublicationFormatsBySubmission(submission_row.submission_id, available=True,
                                                                         approved=True) for pd in
                             ompdal.getPublicationDatesByPublicationFormat(pf.publication_format_id)]
        if publication_dates:
            submission.associated_items['publication_dates'] = publication_dates
        submissions.append(submission)

    sort_option = ompdal.getSeriesSettings(series_row.series_id).find(lambda row: row.setting_name == 'sortOption')
    sortby = sort_option.first()
    b = Browser(submissions, 0, locale, 100, sortby.get('setting_value'), [])
    submissions = b.process_submissions(submissions)

    series.associated_items['submissions'] = submissions

    return locals()


def search():
    q = '{}'.format(request.vars.q) if request.vars.q else '*'

    form = form = SQLFORM.factory(
        Field("title"),
        Field("press_id"),
        formstyle='divs',
        submit_button="Search",
    )
    if form.process().accepted:
        title = form.vars.title

    sort = ['title_de', 'title_en']
    start = 0
    rows = 10
    fq = {'title_en': '*', 'locale': 'de'}
    exc = {'submission_id': '42'}
    fl = ['title_de', 'submission_id', 'press_id', 'title_en']

    if myconf.take("plugins.solr") == str(1):
        solr = OMPSOLR(db, myconf)
        # r = solr.si.query(solr.si.Q(title_en=title)  | solr.si.Q(title_de=title))
        # r = solr.si.query(solr.si.Q(title_de='*Leben*'))
        r = solr.si.query(solr.si.Q(q.decode('utf-8')) & solr.si.Q(press_id=myconf.take('omp.press_id')))
        # for s in sort:
        #    r =r.sort_by(s)
        # r = r.filter(**fq)
        # r = r.exclude(**exc)
        # r = r.field_limit(fl)
        # r = r.highlight(q.keys())
        r = r.paginate(start=start, rows=rows)
        results = r.execute()
        hl = results.highlighting

    from paginate import Page, make_html_tag

    def paginate_link_tag(item):
        """
        Create an A-HREF tag that points to another page usable in paginate.
        """
        a_tag = Page.default_link_tag(item)
        if item['type'] == 'current_page':
            return make_html_tag('li', a_tag, **{'class': 'active'})
        return make_html_tag('li', a_tag)

    p = Page(['test', 'test2'], page=15, items_per_page=15, item_count=10)

    return locals()


def index():
    ompdal = OMPDAL(db, myconf)
    press = ompdal.getPress(myconf.take('omp.press_id'))

    if not press:
        redirect(URL('home', 'index'))
    press_settings = OMPSettings(ompdal.getPressSettings(press.press_id))

    ignored_submission_id = myconf.take('omp.ignore_submissions') if myconf.take(
        'omp.ignore_submissions') else -1

    submissions = []
    session.filters = request.vars.get('filter_by').strip('[').strip(']') if request.vars.get(
            'filter_by') else session.get('filters', '')
    session.per_page = int(request.vars.get('per_page')) if request.vars.get('per_page') else int(
            session.get('per_page', 20))
    '''
    if request.vars.get('sort_by'):
        session.sort_by = request.vars.get('sort_by')
    elif session.get('sort_by'):
        session.sort_by = session.get('sort_by')
    else:
        session.sort_by = 'datePublished-2'
    '''
    current_page = int(request.vars.get('page_nr', 1)) - 1
    page_begin = current_page * session.per_page
    page_end = (current_page+1) * session.per_page


    submission_rows = ompdal.getSubmissionsRangeByPress(press.press_id, page_begin,page_end, ignored_submission_id)

    for submission_row in submission_rows:
        authors = [OMPItem(author, OMPSettings(ompdal.getAuthorSettings(author.author_id)))
                   for author in ompdal.getAuthorsBySubmission(submission_row.submission_id)]
        editors = [OMPItem(editor, OMPSettings(ompdal.getAuthorSettings(editor.author_id)))
                   for editor in ompdal.getEditorsBySubmission(submission_row.submission_id)]
        publication_dates = [dateFromRow(pd) for pf in
                             ompdal.getAllPublicationFormatsBySubmission(submission_row.submission_id, available=True,
                                                                         approved=True)
                             for pd in ompdal.getPublicationDatesByPublicationFormat(pf.publication_format_id)]
        digital_publication_formats = [f for f in
                                       ompdal.getDigitalPublicationFormats(submission_row.submission_id, available=True,
                                                                           approved=True)]
        submission = OMPItem(submission_row,
                             OMPSettings(ompdal.getSubmissionSettings(
                                 submission_row.submission_id)),
                             {'authors': authors, 'editors': editors,
                              'digital_publication_formats': digital_publication_formats}
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

    all_submissions = len(ompdal.getSubmissionsByPress(press.press_id, ignored_submission_id))
    navigation_select = get_navigation_select() if all_submissions > 20 else DIV()
    navigation_list = get_navigation_list(current_page, all_submissions, session.per_page)  if all_submissions > 20 else DIV()


    return locals()

def get_navigation_list(current_page, all_submissions, per_page):
        li = []
        al = {'_aria-label': "Page navigation"}
        total = all_submissions / per_page + 1 if all_submissions % per_page > 0 else all_submissions / per_page
        for i in range(0, int(total)):
            l = A(i + 1, _href=URL('index?page_nr=' + str(i + 1)))
            li.append(LI(l, _class="active")) if i == current_page else li.append(LI(l))

        return TAG.nav(UL(li, _class="pagination pull-left"), **al)


def get_navigation_select():
    per_page = [10, 20, 30]
    li = [LI(A(i, _href=URL('index?per_page=' + str(i)))) for i in per_page]
    ul = UL(li, _class="dropdown-menu")
    button_cs = {
        "_type"         : "button", "_class": "btn btn-default dropdown-toggle", "_data-toggle": "dropdown",
        "_aria-haspopup": "true", "_aria-expanded": "false"
        }
    button = TAG.button(current.T("Results per Page"), SPAN(_class='caret'), **button_cs)
    return DIV(button, ul, _class="btn-group pull-left")
def preview():
    return locals()

def book():

    ompdal = OMPDAL(db, myconf)

    submission_id = request.args[0] if request.args  and request.args[0].isdigit() else raise400()
    press_id = myconf.take('omp.press_id')
    press = ompdal.getPress(press_id)
    submission = ompdal.getPublishedSubmission(submission_id, press_id=press_id)
    chapter_id = int(str(request.args[1])[1:]) if len(request.args) > 1 else 0

    if not submission or not press:
        raise HTTP(400)

    submission_settings = OMPSettings(ompdal.getSubmissionSettings(submission_id))
    press_settings = OMPSettings(ompdal.getPressSettings(press.press_id))


    chapters = []
    chapter = {}
    for i in ompdal.getChaptersBySubmission(submission_id):
        item = OMPItem(i, OMPSettings(ompdal.getChapterSettings(i.chapter_id)), {
            'authors': [OMPItem(a, OMPSettings(ompdal.getAuthorSettings(a.author_id))) for a in
                        ompdal.getAuthorsByChapter(i.chapter_id)]
        })
        chapters.append(item)





    # Get contributors and contributor settings
    editor_rows = ompdal.getEditorsBySubmission(submission_id)
    editors = [OMPItem(e, OMPSettings(ompdal.getAuthorSettings(e.author_id)))
               for e in editor_rows]

    # Do not load authors if the submission has editors
    authors = [] if editors else [OMPItem(a, OMPSettings(ompdal.getAuthorSettings(a.author_id))) for a in
                                  ompdal.getActualAuthorsBySubmission(submission_id, filter_browse=True)]

    # Get chapters and chapter authors


    # Get digital publication formats, settings, files, and identification codes
    c = None
    chapter_doi = None
    digital_publication_formats = []
    for pf in ompdal.getDigitalPublicationFormats(submission_id, available=True, approved=True):
        publication_format = OMPItem(pf, OMPSettings(ompdal.getPublicationFormatSettings(pf.publication_format_id)), {'identification_codes': ompdal.getIdentificationCodesByPublicationFormat(pf.publication_format_id), 'publication_dates': ompdal.getPublicationDatesByPublicationFormat(pf.publication_format_id)})
        full_file = ompdal.getLatestRevisionOfFullBookFileByPublicationFormat(submission_id, pf.publication_format_id)
        full_epub_file = ompdal.getLatestRevisionOfEBook(submission_id, pf.publication_format_id)
        if full_epub_file:
            publication_format.associated_items['full_file'] = OMPItem(full_epub_file, OMPSettings(ompdal.getSubmissionFileSettings(full_epub_file.file_id)))

        if full_file:
            publication_format.associated_items['full_file'] = OMPItem(full_file, OMPSettings(ompdal.getSubmissionFileSettings(full_file.file_id)))

        digital_publication_formats.append(publication_format)

        for i in chapters:
            chapter_file = ompdal.getLatestRevisionOfChapterFileByPublicationFormat(i.attributes.chapter_id, pf.publication_format_id)
            if chapter_file:
                i.associated_items.setdefault('files', {})[pf.publication_format_id] = OMPItem(chapter_file, OMPSettings(ompdal.getSubmissionFileSettings(chapter_file.file_id)))
            if chapter_id > 0 and chapter_id == i.attributes.chapter_id:
                c = i
    if c:
        c_title = c.settings.getLocalizedValue('title', locale)
        c_subtitle = c.settings.getLocalizedValue('subtitle', locale)
        c_abstract = c.settings.getLocalizedValue('abstract', locale)
        c_authors = c.associated_items.get('authors', [])
        c_files = c.associated_items.get('files', {})
        chapter_doi = c.settings.getLocalizedValue(DOI_SETTING_NAME, '')


    # Get physical publication formats, settings, and identification codes
    physical_publication_formats = []
    for pf in ompdal.getPhysicalPublicationFormats(submission_id, available=True, approved=True):
        physical_publication_formats.append(OMPItem(pf, OMPSettings(ompdal.getPublicationFormatSettings(pf.publication_format_id)), {'identification_codes': ompdal.getIdentificationCodesByPublicationFormat(pf.publication_format_id), 'publication_dates': ompdal.getPublicationDatesByPublicationFormat(pf.publication_format_id)}))

    pdf = ompdal.getPublicationFormatByName(submission_id, myconf.take('omp.doi_format_name')).first()

    doi = ""
    submission_doi = submission_settings.getLocalizedValue(DOI_SETTING_NAME, '')
    if submission_doi:
        doi = submission_doi
    elif pdf:
        # DOI always has empty locale
        doi = OMPSettings(ompdal.getPublicationFormatSettings(pdf.publication_format_id)).getLocalizedValue(DOI_SETTING_NAME, "")

    date_published = None
    date_first_published = None
    # Get the OMP publication date (column publication_date contains latest catalog entry edit date.) Try:
    # 1. Custom publication date entered for a publication format calles "PDF"
    if pdf:
        date_published = dateFromRow(ompdal.getPublicationDatesByPublicationFormat(pdf.publication_format_id, "01").first())
        date_first_published = dateFromRow(ompdal.getPublicationDatesByPublicationFormat(pdf.publication_format_id, "11").first())
    # 2. Date on which the catalog entry was first published
    if not date_published:
        metadatapublished_date = ompdal.getMetaDataPublishedDates(submission_id).first()
        date_published = metadatapublished_date.date_logged if metadatapublished_date else None
    # 3. Date on which the submission status was last modified (always set)
    if not date_published:
        date_published = submission.date_status_modified

    series = ompdal.getSeriesBySubmissionId(submission_id)
    if series:
        series = OMPItem(series, OMPSettings(ompdal.getSeriesSettings(series.series_id)))

    # Get purchase info
    representatives = ompdal.getRepresentativesBySubmission(submission_id, myconf.take('omp.representative_id_type'))

    # stats = OMPStats(myconf, db, locale)
    onix_types = ONIX_PRODUCT_IDENTIFIER_TYPE_CODES
    # submissions = sorted(submissions, key=lambda s: s.attributes['series_id'], reverse=True)
    pfs = digital_publication_formats + physical_publication_formats
    idntfrs = {}

    for p in pfs:
        for i in p.associated_items['identification_codes'].as_list():
            idntfrs['{}.{}'.format(i['code'], p.settings.getLocalizedValue('name', locale))] = (
                i['value'], i['code'], p.settings.getLocalizedValue('name', locale))

    idntfrs = sorted(idntfrs.items(), key=lambda i: IDENTIFIER_ORDER.index((i[0]) if i in IDENTIFIER_ORDER else '15.PDF'))


    category_row = ompdal.getCategoryBySubmissionId(submission_id)
    category = OMPItem(category_row, OMPSettings(ompdal.getCategorySettings(category_row.category_id))) if category_row else None

    cleanTitle = " ".join([submission_settings.getLocalizedValue('prefix', locale),
                           submission_settings.getLocalizedValue('title', locale)])
    subtitle = submission_settings.getLocalizedValue('subtitle', locale)
    abstract = submission_settings.getLocalizedValue('abstract', locale)
    series_name = ""

    if series:
        series_title = " ".join([series.settings.getLocalizedValue('prefix', locale), series.settings.getLocalizedValue('title', locale)])
        series_subtitle = series.settings.getLocalizedValue('subtitle', locale)
        series_name = " – ".join([t for t in [series_title.strip(), series_subtitle] if t])


    return locals()
