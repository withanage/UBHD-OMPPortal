# -*- coding: utf-8 -*-

class OMPDAL:
	"""
	A rudimentary database abstraction layer for the OMP database.
	"""
	def __init__(self, db, conf):
		self.db = db
		self.conf = conf

	def getAuthors(self, submission_id):
        	"""
	       	Get all authors associated with the specified submission regardless of exact role.
        	"""
		return self.db((self.db.authors.submission_id==submission_id)).select(
					self.db.authors.first_name, 
					self.db.authors.middle_name, 
					self.db.authors.last_name, 
					orderby=self.db.authors.seq
		)

	def getEditors(self, submission_id):
        	"""
	       	Get all authors associated with the specified submission with editor role.
       		"""
		try:
			editor_group_id = self.conf.take('omp.editor_id')
		except:
			return []
		return self.db((self.db.authors.submission_id==submission_id) 
				& (self.db.authors.user_group_id==editor_group_id)).select(
					self.db.authors.first_name, 
					self.db.authors.middle_name, 
					self.db.authors.last_name, 
					orderby=self.db.authors.seq
		)

	def getChapterAuthors(self, submission_id):
       		"""
       		Get all authors associated with the specified submission with chapter author role
       		"""
		try:
			chapter_author_group_id = self.conf.take('omp.author_id')
		except:
			return []
		return self.db((self.db.authors.submission_id==submission_id) 
				& (self.db.authors.user_group_id==chapter_author_group_id)).select(
					self.db.authors.first_name, 
					self.db.authors.middle_name, 
					self.db.authors.last_name, 
					orderby=self.db.authors.seq
		)

        def getSubmission(self, submission_id):
		"""
		Get submission table row for a given id.
		"""
                return self.db.submissions[submission_id]

	def getSeries(self):
		"""
		Get series info.
		"""
		return self.db(self.db.series.press_id==self.conf.take("omp.press_id")).select(
					self.db.series.series_id, 
					self.db.series.path, 
					self.db.series.image
		)

	def getLocalizedSeriesSettings(self, series_id, locale):
		"""
		Get series settings for a given locale.
		"""
		return self.db((self.db.series_settings.series_id==series_id) 
				& (self.db.series_settings.locale==locale)).select(
					self.db.series_settings.series_id, 
					self.db.series_settings.locale, 
					self.db.series_settings.setting_name, 
					self.db.series_settings.setting_value
		)

        def getSeriesSettings(self, series_id):
		"""
		Get series settings.
		"""
        	return self.db(self.db.series_settings.series_id==series_id).select(
					self.db.series_settings.series_id, 
					self.db.series_settings.locale, 
					self.db.series_settings.setting_name, 
					self.db.series_settings.setting_value
		)

	def getLocalizedChapters(self, submission_id, locale):
		"""
		Get all chapters associated with the given submission and a given locale.
		"""
		q = ((self.db.submission_chapters.submission_id == submission_id) 
				& (self.db.submission_chapters.chapter_id == self.db.submission_chapter_settings.chapter_id)
				& (self.db.submission_file_settings.locale == locale)
				& (self.db.submission_file_settings.setting_name == "chapterID") 
				& (self.db.submission_file_settings.setting_value == self.db.submission_chapters.chapter_id) 
				& (self.db.submission_file_settings.file_id == self.db.submission_files.file_id) 
				& (self.db.submission_chapter_settings.setting_name == 'title')
		)

		return self.db(q).select(self.db.submission_chapters.chapter_id, 
					self.db.submission_chapter_settings.setting_value, 
					self.db.submission_files.ALL, 
					orderby=[self.db.submission_chapters.chapter_seq, self.db.submission_files.assoc_id], 
		)

        def getChapters(self, submission_id, locale):
		"""
		Get all chapters associated with the given submission.
		"""
                q = ((self.db.submission_chapters.submission_id == submission_id)
                        	& (self.db.submission_chapters.chapter_id == self.db.submission_chapter_settings.chapter_id)
                        	& (self.db.submission_file_settings.setting_name == "chapterID")
                        	& (self.db.submission_file_settings.setting_value == self.db.submission_chapters.chapter_id)
                        	& (self.db.submission_file_settings.file_id == self.db.submission_files.file_id)
                        	& (self.db.submission_chapter_settings.setting_name == 'title')
		)

                return self.db(q).select(self.db.submission_chapters.chapter_id,
                                        self.db.submission_chapter_settings.setting_value,
                                        self.db.submission_files.ALL,
                                	orderby=[self.db.submission_chapters.chapter_seq, self.db.submission_files.assoc_id],
		)

	def getLocalizedLatestRevisionOfChapters(self, submission_id, locale):
                """
                Get the latest revision for all chapter files associated with the given submission and a given locale.
                """
                q = ((self.db.submission_chapters.submission_id == submission_id)
                                & (self.db.submission_chapters.chapter_id == self.db.submission_chapter_settings.chapter_id)
                                & (self.db.submission_file_settings.locale == locale)
                                & (self.db.submission_file_settings.setting_name == "chapterID")
                                & (self.db.submission_file_settings.setting_value == self.db.submission_chapters.chapter_id)
                                & (self.db.submission_file_settings.file_id == self.db.submission_files.file_id)
                                & (self.db.submission_chapter_settings.setting_name == 'title')
                )

                chapters = self.db(q).select(self.db.submission_chapters.chapter_id,
                                        self.db.submission_chapter_settings.setting_value,
                                        self.db.submission_files.ALL,
                                        orderby=[self.db.submission_chapters.chapter_seq, self.db.submission_files.assoc_id],
                                        distinct=True
                )
                
		latest_revision_chapters = []
                for row in chapters:
                        latest_revision = self.db(self.db.submission_files.file_id == row.submission_files.file_id).select(self.db.submission_files.revision.max()).first()[self.db.submission_files.revision.max()]
                        if row.submission_files.revision == latest_revision:
                                latest_revision_chapters.append(row)

                return latest_revision_chapters

	def getLatestRevisionOfChapters(self, submission_id):
                """
                Get the latest revision for all chapter files associated with the given submission.
                """
                q = ((self.db.submission_chapters.submission_id == submission_id)
                                & (self.db.submission_chapters.chapter_id == self.db.submission_chapter_settings.chapter_id)
                                & (self.db.submission_file_settings.setting_name == "chapterID")
                                & (self.db.submission_file_settings.setting_value == self.db.submission_chapters.chapter_id)
                                & (self.db.submission_file_settings.file_id == self.db.submission_files.file_id)
                                & (self.db.submission_chapter_settings.setting_name == 'title')
                )

		chapters = self.db(q).select(self.db.submission_chapters.chapter_id,
                                        self.db.submission_chapter_settings.setting_value,
                                        self.db.submission_files.ALL,
					orderby=[self.db.submission_chapters.chapter_seq, self.db.submission_files.assoc_id],
                                        distinct=True
		)
		
		latest_revision_chapters = []
		for row in chapters:
			latest_revision = self.db(self.db.submission_files.file_id == row.submission_files.file_id).select(self.db.submission_files.revision.max()).first()[self.db.submission_files.revision.max()]
			if row.submission_files.revision == latest_revision:
				latest_revision_chapters.append(row)

		return latest_revision_chapters

	def getLatestRevisionsOfFullBook(self, submission_id):
		try:
			monograph_type_id = self.conf.take('omp.monograph_type_id')
		except:
			return []
		sf = self.db.submission_files
		q = ((sf.submission_id == submission_id)
                        & (sf.genre_id == monograph_type_id)
                        & (sf.file_stage > 5)
		)
		files = []
		for f in self.db(q).select(sf.file_id, orderby=sf.file_id, distinct=True):
			latest_revision = self.db(sf.file_id == f.file_id).select(sf.revision.max()).first()[sf.revision.max()]
			q_latest = ((sf.file_id == f.file_id)
				& (sf.revision == latest_revision)
                	)
			files.append(self.db(q_latest).select(sf.ALL, orderby=sf.file_id, distinct=True).first())

		return files

	def getPublicationDates(self, submission_id):
		q = ((self.db.publication_formats.submission_id == submission_id)
			& (self.db.publication_format_settings.publication_format_id == self.db.publication_formats.publication_format_id)
			& (self.db.publication_format_settings.setting_value == self.conf.take('omp.doi_format_name'))
			& (self.db.publication_dates.publication_format_id == self.db.publication_format_settings.publication_format_id)
		)
		return self.db(q).select(self.db.publication_dates.date, 
			self.db.publication_dates.role, 
			self.db.publication_dates.date_format
		)

