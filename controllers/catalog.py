# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''

def index():
	abstract, author, cleanTitle, subtitle  = '', '', '', ''
	locale = 'de_DE'
	if session.forced_language=='en':
		locale= 'en_US'
	query =  ((db.submissions.context_id == myconf.take('omp.press_id')) & (db.submissions.status == 3)  & (db.submission_settings.submission_id == db.submissions.submission_id) & (db.submission_settings.locale==locale))
	submissions = db(query).select(db.submission_settings.ALL, orderby = db.submissions.submission_id)
        subs = {} 
        for  i in submissions:
		if i.setting_name=='abstract':
			subs.setdefault(i.submission_id,{})['abstract'] = i.setting_value
		if i.setting_name=='subtitle':
			subs.setdefault(i.submission_id,{})['subtitle'] = i.setting_value
		if i.setting_name =='cleanTitle':
			subs.setdefault(i.submission_id, {})['cleanTitle'] =  i.setting_value
		
	return dict(abstract=abstract,  author=author, cleanTitle=cleanTitle, submissions=submissions, subtitle=subtitle, subs=subs )

def book():
  abstract, authors, cleanTitle, subtitle  = '', '', '', ''
  locale = 'de_DE'
  if session.forced_language=='en':
   locale= 'en_US'
  book_id =  request.args[0] if request.args else redirect(URL('home','index')) 
  
  query =  ((db.submission_settings.submission_id == int(book_id)) & (db.submission_settings.locale==locale))
  book = db(query).select(db.submission_settings.ALL)
  if len(book) ==0:
     raise HTTP(404,T('book not found'))

  author_q = ((db.authors.submission_id==book_id)) 
  authors_list = db(author_q).select(db.authors.first_name,db.authors.last_name)
  for i in authors_list:
    authors += i.first_name +' '+ i.last_name+', '
  if authors.endswith(', '):
    authors = authors[:-2]
  author_bio = db((db.authors.submission_id==book_id) & (db.authors.author_id == db.author_settings.author_id) & (db.author_settings.locale==locale) & ( db.author_settings.setting_name=='biography')).select(db.author_settings.setting_value).first()
  
  chapter_query = ((db.submission_chapters.submission_id==book_id) & (db.submission_chapters.chapter_id ==db.submission_chapter_settings.chapter_id ) & (db.submission_chapter_settings.locale==locale) & (db.submission_file_settings.setting_name=="chapterID") &(db.submission_file_settings.setting_value==db.submission_chapters.chapter_id) & (db.submission_file_settings.file_id==db.submission_files.file_id) & (db.submission_chapter_settings.setting_name=='title') ) 
  chapters = db(chapter_query).select(db.submission_chapters.chapter_id, db.submission_chapter_settings.setting_value,db.submission_files.assoc_id, db.submission_files.submission_id, db.submission_files.genre_id, db.submission_files.file_id, db.submission_files.revision, db.submission_files.file_stage, db.submission_files.date_uploaded, orderby=[db.submission_chapters.chapter_id,db.submission_files.assoc_id])
  publication_formats= db((db.publication_formats.submission_id==book_id) & (db.publication_format_settings.publication_format_id==db.publication_formats.publication_format_id) & (db.publication_format_settings.locale==locale)).select(db.publication_format_settings.setting_name,db.publication_format_settings.setting_value,db.publication_formats.publication_format_id, groupby=db.publication_formats.publication_format_id, orderby=db.publication_formats.publication_format_id)
  
  for  i in book:
    if i.setting_name=='abstract':
      abstract = i.setting_value
    if i.setting_name=='subtitle':
      subtitle = i.setting_value
    if i.setting_name =='cleanTitle':
      cleanTitle =  i.setting_value
  cover_image = URL(myconf.take('web.application'),'static','monographs/'+ book_id+'/simple/cover.jpg')
  return dict(abstract=abstract,authors=authors, author_bio=author_bio, chapters=chapters,  cleanTitle=cleanTitle,cover_image=cover_image,publication_formats=publication_formats,  subtitle=subtitle)

