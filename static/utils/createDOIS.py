#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: wit
python3.5 /home/withanage/projects/web2py3/web2py/web2py.py -R  /home/withanage/projects/web2py3/web2py/applications/UBHD_OMPPortal/static/utils/imagesJATSXMLBySubmission.py   --shell UBHD_OMPPortal  -M
'''
import sys
import xlsxwriter
from ompdal import OMPDAL

ompdal = OMPDAL(db, myconf)
PRESS_ID = myconf.get('omp.press_id')
OUTPUT_PATH = '{}{}{}{}{}'.format(request.env.web2py_path, '/applications/', request.application,'/static/utils/','doi.xlsx')
DOI_DATA = []
# tables
a = db.authors
aus = db.author_settings
pf = db.publication_formats
pfs = db.publication_format_settings
s = db.submissions
sc = db.submission_chapters
sca = db.submission_chapter_authors
ugs = db.user_group_settings


def getTableSetting(settingsList, name):
    result = ''. join(set([settings['setting_value'] for settings in settingsList if settings['setting_name'] == name]))
    return result


def getAuthorsByRoles(authors_rows, roles, submission):
    authors = []
    for author in authors_rows:
        ast = ompdal.getAuthorSettings(author['author_id']).as_list()

        role = db((ugs.user_group_id == a.user_group_id) & (a.author_id == author["author_id"]) & (
                ugs.setting_name == "abbrev")).select(ugs.setting_value)
        role = role.first().get('setting_value') if role else []
        if role in roles:
            authors.append(' '.join([getTableSetting(ast, 'givenName'), getTableSetting(ast, 'familyName')]))

    submission['authors'] = ', '.join(authors)

    return submission

def setWorksheetStyle(workbook):
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 0, 20)
    worksheet.set_column(1, 1, 40)
    worksheet.set_column(2, 2, 70)
    worksheet.set_column(3, 3, 50)
    for i,value  in enumerate(['ID','Autoren','Titel','DOI','Type']):
            worksheet.write_string(0, i, value)
    return worksheet


def setWorksheetData(worksheet):
    for row, v in enumerate(DOI_DATA):
        row += 1
        if v['type'] == 'Band':
            worksheet.write_string(row, 0, str(v['submission']))
        else:
            worksheet.write_string(row, 0, '-c'.join([str(v['submission']), str(v['chapter'])]))
        if v.get('authors'):   worksheet.write_string(row, 1, v['authors'])
        if v.get('title'): worksheet.write_string(row, 2, v['title'])
        worksheet.write_url(row, 3, ''.join(['https://', v['doi']]))
        worksheet.write_string(row, 4, v['type'])


def createChapters(s):
    chapter_rows = db(sc.submission_id == s).select(sc.chapter_id).as_list()
    for c in chapter_rows:
        chapter = {"submission": s, "chapter": c['chapter_id'], "type": "Kapitel"}
        chapter_authors_rows = db(sca.chapter_id == c['chapter_id']).select(sca.author_id).as_list()
        if chapter_authors_rows:
            chapter = getAuthorsByRoles(chapter_authors_rows, ['CA'], chapter)

        chapter_settings_rows = ompdal.getChapterSettings(c['chapter_id']).as_list()
        chapter['title'] = getTableSetting(chapter_settings_rows, 'title')
        chapter['doi'] = getTableSetting(chapter_settings_rows, 'pub-id::doi')

        if chapter['doi']:  DOI_DATA.append(chapter)
    return chapter_rows


def createSubmission(s):
    submission_rows = ompdal.getSubmissionSettings(s)
    authors_rows = db(a.submission_id == s).select(a.author_id).as_list()

    submission = {"submission": s, "chapter": "", "type": "Band"}
    submission = getAuthorsByRoles(authors_rows, ['AU', 'VE'], submission)
    if submission_rows:
        submission['title'] = getTableSetting(submission_rows.as_list(), 'title')
        submission['doi'] = getTableSetting(submission_rows.as_list(), 'pub-id::doi')
        if not submission['doi']:
            pfs = db(pf.submission_id == s).select(pf.publication_format_id).as_list()

            for p in list(map(lambda s: s['publication_format_id'], pfs)):
                pfs_rows = ompdal.getPublicationFormatSettings(p).as_list()
                if not submission['doi']:
                    submission['doi'] = getTableSetting(pfs_rows, 'pub-id::doi')

    if submission['doi']:   DOI_DATA.append(submission)
    return submission


def createSubmissionsList():
    global s
    submissions_rows = db(s.context_id == PRESS_ID).select(s.submission_id).as_list()
    submissions = sorted(list(map(lambda s: s['submission_id'], submissions_rows)))
    for s in submissions:
        createSubmission(s)
        createChapters(s)


def createExcelSheet():
    createSubmissionsList()
    workbook = xlsxwriter.Workbook(OUTPUT_PATH)
    worksheet = setWorksheetStyle(workbook)
    setWorksheetData(worksheet)
    workbook.close()


createExcelSheet()
