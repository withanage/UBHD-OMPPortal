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
OUTPUT_PATH = '{}{}{}{}{}'.format(request.env.web2py_path, '/applications/', request.application, '/static/utils/', 'doi.xlsx')
DOI_DATA = []


class SubmissionDOI:
	"""
	Submission DOI Class

	"""

	def __init__ (self):

		self.a = db.authors
		self.aus = db.author_settings
		self.pf = db.publication_formats
		self.pfs = db.publication_format_settings
		self.sb = db.submissions
		self.sc = db.submission_chapters
		self.sca = db.submission_chapter_authors
		self.ugs = db.user_group_settings

	def getTableSetting (self, settings_list, name):
		"""
		get table setting from OMP
		:param settings_list: array
		:param name:
		:return:
		"""
		result = ''.join(set([settings['setting_value'] for settings in settings_list if settings['setting_name'] == name]))
		return result

	def getAuthorsByRoles (self, authors_rows, roles, submission):
		authors = []
		for author in authors_rows:
			ast = ompdal.getAuthorSettings(author['author_id']).as_list()

			role = db((self.ugs.user_group_id == self.a.user_group_id) & (self.a.author_id == author["author_id"]) & (
					self.ugs.setting_name == "abbrev")).select(self.ugs.setting_value)
			role = role.first().get('setting_value') if role else []
			if role in roles:
				authors.append(' '.join([self.getTableSetting(ast, 'givenName'), self.getTableSetting(ast, 'familyName')]))

		submission['authors'] = ', '.join(authors)

		return submission

	def setWorksheetStyle (self, workbook):
		worksheet = workbook.add_worksheet()

		worksheet.set_column(0, 0, 20)
		worksheet.set_column(1, 1, 40)
		worksheet.set_column(2, 2, 70)
		worksheet.set_column(3, 3, 50)

		for i, value in enumerate(['ID', 'Autoren', 'Titel', 'DOI', 'Type']):
			worksheet.write_string(0, i, value)

		return worksheet

	def setWorksheetData (self, worksheet):
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

	def createChapters (self, s):
		chapter_rows = db(self.sc.submission_id == s).select(self.sc.chapter_id).as_list()
		for c in chapter_rows:
			chapter = {"submission": s, "chapter": c['chapter_id'], "type": "Kapitel"}
			chapter_settings_rows = ompdal.getChapterSettings(c['chapter_id']).as_list()
			chapter['title'] = self.getTableSetting(chapter_settings_rows, 'title')
			chapter['doi'] = self.getTableSetting(chapter_settings_rows, 'pub-id::doi')
			chapter_authors_rows = db(self.sca.chapter_id == c['chapter_id']).select(self.sca.author_id).as_list()
			if chapter_authors_rows:
				chapter = self.getAuthorsByRoles(chapter_authors_rows, ['CA'], chapter)

			if chapter.get('doi'):  DOI_DATA.append(chapter)
		return chapter_rows

	def createSubmissionsList (self):
		submissions_rows = db(self.sb.context_id == PRESS_ID).select(self.sb.submission_id).as_list()
		submissions = sorted(list(map(lambda s: s['submission_id'], submissions_rows)))
		for s in submissions:
			self.createSubmission(s)
			self.createChapters(s)

	def createSubmission (self, s):
		submission_rows = ompdal.getSubmissionSettings(s)
		authors_rows = db(self.a.submission_id == s).select(self.a.author_id).as_list()

		submission = {"submission": s, "chapter": "", "type": "Band"}
		submission = self.getAuthorsByRoles(authors_rows, ['AU', 'VE'], submission)
		if submission_rows:
			submission['title'] = self.getTableSetting(submission_rows.as_list(), 'title')
			submission['doi'] = self.getTableSetting(submission_rows.as_list(), 'pub-id::doi')
			if not submission['doi']:
				self.getPublicationFormatDOI(s, submission)

		if submission.get('doi'):   DOI_DATA.append(submission)
		return submission

	def getPublicationFormatDOI (self, s, submission):
		pfs = db(self.pf.submission_id == s).select(self.pf.publication_format_id).as_list()
		for p in list(map(lambda s: s['publication_format_id'], pfs)):
			pfs_rows = ompdal.getPublicationFormatSettings(p).as_list()
			if not submission['doi']:
				submission['doi'] = self.getTableSetting(pfs_rows, 'pub-id::doi')

	def createExcelSheet (self):
		self.createSubmissionsList()
		workbook = xlsxwriter.Workbook(OUTPUT_PATH)
		worksheet = self.setWorksheetStyle(workbook)
		self.setWorksheetData(worksheet)
		workbook.close()


sd = SubmissionDOI()
sd.createExcelSheet()
