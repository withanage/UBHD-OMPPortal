# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''

########################################

db.define_table("authors",
     Field("author_id","integer"),
     Field("submission_id","integer"),
     Field("primary_contact","integer"),
     Field("seq","integer"),
     Field("first_name","string"),
     Field("middle_name","string"),
     Field("last_name","string"),
     Field("suffix","string"),
     Field("country","string"),
     Field("email","string"),
     Field("url","string"),
     Field("user_group_id","integer"),
     Field("include_in_browse","integer"),
     migrate=False
)


db.define_table("author_settings",
     Field("author_id","integer"),
     Field("locale","string"),
     Field("setting_name","string"),
     Field("setting_value","string"),
     Field("setting_type","string"),
     migrate=False
)


db.define_table("submission_chapters",
     Field("chapter_id","integer"),
     Field("submission_id",'integer'),
     Field("chapter_seq",'integer'),
     migrate=False
)


db.define_table("submission_chapter_settings",
     Field("chapter_id","integer"),
     Field("locale","string"),
     Field("setting_name","string"),
     Field("setting_value","string"),
     Field("setting_type","string"),
     migrate=False
)
db.define_table("press_settings",
     Field("press_id","integer"),
     Field("locale","string"),
     Field("setting_name","string"),
     Field("setting_value","string"),
     Field("setting_type","string"),
     migrate=False
)

db.define_table("presses",
     Field("press_id","integer"),
     Field("path","string"),
     Field("seq","integer"),
     Field("primary_locale","string"),
     Field("enabled","integer"),
     primarykey=['press_id'],
     migrate = False
)

db.define_table("published_submissions",
     Field("pub_id","integer"),
     Field("submission_id","integer"),
     Field("date_published","datetime",requires=IS_DATETIME(format="%Y-%m-%d %H:%M:%S")),
     Field("audience","string"),
     Field("audience_range_qualifier","string"),
     Field("audience_range_from","string"),
     Field("audience_range_to","string"),
     Field("audience_range_exact","string"),
     Field("cover_image","string"),#TODO coverimage versoppelt
     primarykey=['pub_id'],
     migrate = False
)


db.define_table("publication_formats",
     Field("publication_format_id","integer"),
     Field("submission_id","integer"),
     Field("physical_format","integer"),
     Field("entry_key","string"),
     Field("seq","double"),
     Field("file_size","string"),
     Field("front_matter","string"),
     Field("back_matter","string"),
     Field("height","string"),
     Field("height_unit_code","string"),
     Field("width","string"),
     Field("width_unit_code","string"),
     Field("thickness","string"),
     Field("thickness_unit_code","string"),
     Field("weight","string"),
     Field("weight_unit_code","string"),
     Field("product_composition_code","string"),
     Field("product_form_detail_code","string"),
     Field("country_manufacture_code","string"),
     Field("imprint","string"),
     Field("product_availability_code","string"),
     Field("technical_protection_code","string"),
     Field("returnable_indicator_code","string"),
     Field("is_approved","integer"),
     Field("is_available","integer"),
     primarykey=['publication_format_id'],
     migrate = False
)

db.define_table("publication_format_settings",
     Field("publication_format_id","integer"),
     Field("locale","string"),
     Field("setting_name","string"),
     Field("setting_value","string"),
     Field("setting_type","string"),
     primarykey=['publication_format_id','locale','setting_name'],
     migrate = False
)
db.define_table("series_settings",
     Field("series_id","integer"),
     Field("locale","string"),
     Field("setting_name","string"),
     Field("setting_value","string"),
     Field("setting_type","string"),
     migrate = False
)



db.define_table("submissions",
     Field("submission_id","integer"),
     Field("locale","string"),
     Field("user_id","integer"),
     Field("context_id","integer"),
     Field("series_id","integer"),
     Field("series_position","string"),
     Field("edited_volume","integer"),
     Field("language","string"),
     Field("comments_to_ed","string"),
     Field("date_submitted","string"),
     Field("last_modified","datetime",requires=IS_DATETIME(format="%Y-%m-%d %H:%M:%S")),
     Field("date_status_modified","datetime",requires=IS_DATETIME(format="%Y-%m-%d %H:%M:%S")),
     Field("status","integer"),
     Field("submission_progress","integer"),
     Field("pages","string"),
     Field("fast_tracked","integer"),
     Field("hide_author","integer"),
     Field("comments_status","integer"),
     Field("stage_id","integer"),
     primarykey=['submission_id'],
     migrate = False
)

db.define_table("submission_settings",
     Field("submission_id","integer"),
     Field("locale","string"),
     Field("setting_name","string"),
     Field("setting_value","string"),
     Field("setting_type","string"),
     primarykey=['submission_id'],
     migrate = False
)
db.define_table("submission_file_settings",
     Field("file_id","integer"),
     Field("locale","string"),
     Field("setting_name","string"),
     Field("setting_value","string"),
     Field("setting_type","string"),
     migrate =False, 
)

db.define_table('submission_files',
Field('file_id', 'integer'),
Field('revision', 'integer'),
Field('source_file_id', 'integer' ),
Field('source_revision', 'integer' ),
Field('submission_id', 'integer'),
Field('file_type'),
Field('genre_id', 'integer' ),
Field('file_size', 'integer'),
Field('original_file_name'),
Field('file_stage' ,'integer'),
Field('direct_sales_price'),
Field('sales_type'),
Field('viewable','integer'),
Field('date_uploaded', 'datetime'),
Field('date_modified' ,'datetime'),
Field('user_group_id','integer'),
Field('uploader_user_id','integer'),
Field('assoc_type','integer'),
Field('assoc_id', 'integer'),

migrate=False
)

db.define_table("identification_codes",
     Field("identification_code_id","integer"),
     Field("publication_format_id","integer"),
     Field("code","integer"),
     Field("value","string"),
     migrate = False
)

db.define_table("user_group_settings",
     Field("user_group_id","integer"),
     Field("locale","string"),
     Field("setting_name","string"),
     Field("setting_value","string"),
     Field("setting_type","string"),
     migrate = False
)
'''
# read omp values
submission_id       = request.args(0) if  request.args(0) else 0
error_code          = T('in OMP nicht angegeben')
locale_pre= db(db.submissions.submission_id==submission_id).select(db.submissions.locale).first()
locale = locale_pre['locale'] if locale_pre else 'de_DE'

publisher_record    = db(db.press_settings.setting_name=='publisher').select(db.press_settings.setting_value).first()
publisher           = publisher_record['setting_value'] if publisher_record else error_code

publication_formats = db(db.publication_formats.submission_id==submission_id).select(db.publication_formats.publication_format_id).first()
isbn_pre            = db(db.identification_codes.publication_format_id==publication_formats['publication_format_id']).select(db.identification_codes.value).first() if publication_formats else None #TODO add code=15 oder 24
isbn                = isbn_pre['value'] if isbn_pre else error_code
#

authors_pre= db(db.authors.submission_id==submission_id).select(db.authors.last_name,db.authors.first_name, db.authors.user_group_id,db.authors.country, db.authors.author_id)
authors_surname_firstname = ''
for i in authors_pre:
    authors_surname_firstname += i.last_name+', '+i.first_name+ ' '

authors_firstname_surname =  ''
for i in authors_pre:
    authors_firstname_surname += i.first_name+' '+i.last_name+ ' '


contributor_role = '' # locale db.authors.group_id== user_group_settings.locale==locale & , davon setting_value
country = ''
#for i in authors_pre:
#    country += i.country

#

title_pre = db((db.submission_settings.submission_id==submission_id) & (db.submission_settings.setting_name=='title') & (db.submission_settings.locale==locale)).select(db.submission_settings.setting_value).first()
title = title_pre['setting_value'] if title_pre else error_code

sub_title_pre = db((db.submission_settings.submission_id==submission_id) & (db.submission_settings.setting_name=='subtitle') & (db.submission_settings.locale==locale)).select(db.submission_settings.setting_value).first()
sub_title = sub_title_pre['setting_value'] if sub_title_pre else error_code

series_id_pre = db(db.submissions.submission_id==submission_id).select(db.submissions.series_id).first()
series_id = series_id_pre['series_id'] if series_id_pre else 0
series_title_pre = db((db.series_settings.series_id==series_id) & (db.series_settings.locale==locale) & (db.series_settings.setting_name=='title')).select(db.series_settings.setting_value).first()
series_title = series_title_pre['setting_value'] if series_title_pre else error_code


#TOTO je nach format sollte format artikel_format_pre ausgelesen werden
artikel_format_pre = db((db.publication_format_settings.locale==locale) & (db.publication_format_settings.setting_value=='Hardcover')).select(db.publication_format_settings.publication_format_id).first()

artikel_format =  artikel_format_pre['publication_format_id'] if artikel_format_pre else 0
artikel_format_pre = db((db.publication_formats.submission_id == submission_id) & (db.publication_formats.publication_format_id==artikel_format)).select(db.publication_formats.ALL).first()
artikel_format = str(artikel_format_pre['height']) + ' X' +str(artikel_format_pre['width']) + ' X' + str(artikel_format_pre['thickness'])  if artikel_format_pre else error_code

abstract_pre = db((db.submission_settings.submission_id==submission_id) & (db.submission_settings.setting_name=='abstract') & (db.submission_settings.locale==locale)).select(db.submission_settings.setting_value).first()
abstract = abstract_pre['setting_value'] if abstract_pre else error_code

author_id_pre = db((db.authors.submission_id==submission_id) & (db.authors.primary_contact==1)).select(db.authors.author_id).first() #for primary contact
author_id = author_id_pre['author_id'] if author_id_pre else None
author_biography_pre = db((db.author_settings.author_id==author_id) & (db.author_settings.locale==locale) & (db.author_settings.setting_name=='biography')).select(db.author_settings.setting_value).first()
author_biography = author_biography_pre['setting_value'] if author_biography_pre else error_code





#


db.define_table('t_onix_additionals',
    Field('submission_id', type='integer',readable=True,writable=False,default=request.args(0),label=T('Submission id')),
    Field('omp_publisher','string',default=publisher,writable=False,readable=True),
    Field('omp_isbn','string',notnull=True,default=isbn,label=T('ISBN-13'),writable=False),
    Field('f_verlagsverkehrsnummer', type='integer', label=T('Verlagsverkehrsnummer'),writable=False), # TODO anja liefert daten als
    Field('f_zusatz_isbn_ean', type='string', notnull=False,   label=T('ISBN / EAN Weitere Ausgabe')), #TODO the same as omp_isbn
    Field('f_verlags_bestell_nr', type='string', label=T('Verlags Bestell Nr.')),
    Field('omp_autor_surname_firstname', type='string', default=authors_surname_firstname, label=T('Autoren'),writable=False),#Sammelband: Herausgeber, Monographie Authoren
    #Field('omp_contributor_role',type='string', label=T('Contributor Role'), default=contributor_role),
    #Field('omp_autor_firstname_surname', type='string', default=authors_firstname_surname, label=T('Autoren : Vorname Nachname )'),writable=False),#Sammelband: Herausgeber, Monographie Authoren
    #Field('omp_autor_firstname','string'),
    #Field('omp_autor_surname','string'),
    #Field('omp_autor_country','string', default=country),
    #Field ('omp_biography', 'text', default=author_biography),
    Field('f_sende_datum', type='date', label=T('Sendedatum')),  #TODO Date format 20150101
    Field('omp_title', type='string', default=title, label=T('Titel'),writable=False),#Sammelband: Herausgeber, Monographie Authoren
    Field('f_medienbeilage', type='string', label=T('Medienbeilage z.B "mit CD-ROM"'),default=""),
    Field('omp_sub_title', type='string', default=sub_title, label=T('Untertitel'),writable=False),#Sammelband: Herausgeber, Monographie Authoren
    Field('f_belletristik', type='string', label=T('Titel der Original Ausgabe')),
    Field('f_weitere_angaben', type='string', label=T('Weitere Angaben')),
    Field('f_produktionsjahr', type='string', label=T('Produktionsjahr')),
    Field('f_zusatzinformationen', type='string', label=T('Zusatzinformationen')),
    Field('omp_language',"string",label=T('Sprache'),default=locale, writable=False),
    Field('omp_series',"string",label=T('Reihe'),default=series_title, writable=False),
    Field('omp_series_position',"string",label=T('Band Nr.'),default='XXXXXX', writable=False), #TODO Series_position in submissions
    Field('f_teilband', type='string', label=T('Teilband')),
    Field('f_auflage', type='string', notnull=True,label=T('Auflage')),
    Field('f_laufzeit_in_minuten', type='string',label=T('Laufzeit In Minuten')),
    Field('f_umfang', type='string', notnull=True, label=T('Umfang')),
    Field('f_abbildungen', type='string', label=T('Abbildungen')),
    Field('omp_artikel_format', type='string', label=T('Abbildungen'), default='', writable=False),
    Field('omp_amount',"string",label=T('Mengen Angabe'),default='XXXXXX', writable=False), #TODO in publication_formats beim hardcover , weight
    Field('f_verpackungs_angaben_in_mm', type='string',label=T('Verpackungsangaben In mm')),
    Field('f_fsk_or_usk_angabe', type='string', notnull=True,label=T('FSK / USK Angabe')),
    Field('f_altersempfehlung', type='string', notnull=True, default='', label=T('Altersempfehlung')),
    Field('f_warnhinweis', type='string', notnull=True,label=T('Warnhinweis')),
    Field('f_warengruppe_lt_vlb', type='string',label=T('Warengruppe lt. VLB')),
    Field('omp_product_form', type='string', label=T('Produktform/Medienart'), writable=True, notnull=True),#TODO  falls in omp gibt : catalog . product composition: product detail
    Field('f_number', type='integer',label=T('Anz. der Medien')),
    Field('f_weiter_angaben', type='string', notnull=False,  label=T('weitere Angaben zur Produktform')),
    Field('f_auslieferungstermin', type='string', notnull=True,  label=T('Auslieferungstermin')),
    Field('omp_first_selling_day','string', label=T('Erstverkaufstag')),#publication_formats ????
    Field('f_ladenpreis_euro_de', type='double', notnull=True, label=T('Ladenpreis EURO DE')),    
    Field('f_ladenpreis_euro_at', type='double', notnull=True,label=T('Ladenpreis EURO AT')),
    Field('f_mwst', type='double', notnull=True,label=T('Mwst.')),
    Field('f_vorbestelldatum', type='date',label=T('Vorbestelldatum')),
    Field('f_vorbestellpreis_euro_de', type='double', notnull=True,label=T('Vorbestellpreis EURO DE')),
    Field('f_vorbestellpreis_euro_at', type='double', notnull=True,label=T('Vorbestellpreis EURO AT')),
    Field('f_vorbestellpreis_euro_sfr', type='double', notnull=True,label=T('Vorbestellpreis EURO SFR')),
    Field('omp_abstract', type='text', default=abstract, label=T('Kurztext'),writable=False), #abstract
    Field('f_klappentext', type='string',label=T('Klappentext')),
    Field('f_content_directory', type='string',label=T('Inhaltsverzeichnis')),
    Field('f_tracklist', type='string',label=T('Tracklist bei Musik')),
    Field('f_leseprobe', type='text',label=T('Leseprobe')),
    Field('f_', type='string',label=T('')),
    Field('omp_author_biography', type='text', default=author_biography, label=T('Porträt'),writable=False), #abstract
    Field('f_zolltarifnummer_verzeihnis', type='string', notnull=True,    label=T('Zolltarifnummer Verzeihnis')),
    Field('f_warennummer_ztn', type='string', notnull=True,label=T('Warennummer Ztn')),
    Field('f_ursprungsland', type='string', notnull=True,label=T('Ursprungsland')),
    Field('f_cover_image', type='upload',label=T('Cover Image')),
    Field('f_klassifizierung_hochschulschriften', type='string', notnull=True,   label=T('Klassifizierung Hochschulschriften')),
    Field('f_mehrbaendiger_werke', type='string', notnull=True,  label=T('Mehrbaendiger Werke')),
    Field('f_issn', type='string', notnull=True, label=T('ISSN')),
    format='%(f_verlagsverkehrsnummer)s',
    migrate=settings.migrate,
    #redefine=True
)


db.define_table("t_knv_metadata",
     Field('submission_id', type='integer',readable=True,writable=False,default=request.args(0),
          label=T('Submission id')),
     Field("isbn","integer", label=T('ISBN'), requires=IS_LENGTH(minsize=13,maxsize=13),notnull=True),
     Field("buchtitel","string",label=T('Buchtitel (OMP)'),default=title,writable=True, requires=IS_LENGTH(maxsize=60)),
     Field("anz_teile","integer", default=1,label=T('Anz. Teile'),writable=False),
     Field("verlagsname","string", default=T("Heidelberg University Publishing"),label=T('Verlagsname'),writable=False),
     Field("gln","integer",label=T('GLN'), writable=False), #TODO anja liefert die daten von nv, ist eine fixe nr.
     Field("bindeart","string", label=T('Bindeart') ,default=T('HB'),  requires=IS_IN_SET(('HB','PB'))),
     Field("anz_rillungen","integer",default=T('2'),label=T('Anz. Rillungen'), requires=IS_IN_SET(('2','4'))),
     Field("kapitalband","string",label=T('Kapitalband'), requires=IS_IN_SET(('white','none'))),
     Field("rueckenart","string",label=T('Rückenart'), requires=IS_IN_SET(('square','round')), default='round'),
     Field("ansichtsexemplar","string", default="yes",label=T('Ansichtsexemplar'),requires=IS_IN_SET(('yes','no'))),
     Field("laendercode","string",default="DE", label=T('Ländercode'),writable=False),
     Field("adresszeile1","string",default=" ",label=T('Adresszeile1'),writable=False),
     Field("adresszeile2","string",default=T('Heidelberg University Publishing'),label=T('Adresszeile2'),writable=False),
     Field("adresszeile3","string",default=T('c/o Universitätsbibliothek Heidelberg'),label=T('Adresszeile3'),writable=False),
     Field("ort","string",default="Heidelberg",label=T('Ort'),writable=False),
     Field("plz","integer",default="69047",label=T('PLZ'), writable=False),
     Field("strasse_und_nr","string",default="Plöck 107-109",label=T('Straße und Nr.'),writable=False),
     Field("postfach","string",default="105749",label=T('Postfach'),writable=False),
     Field("speicherung","string",default="yes",label=T('Speicherung'),requires=IS_IN_SET(('yes','temp'))),
     Field("dateiname_pdf_cover","upload",label=T('Dateiname PDF (cover)')),#TODO isbdn ohne bindestirche .cover.pdf automatisch generieren , ein neues feld
     Field("teilnummer","integer",label=T('Teilnummer'),default=1, writable=False),
     Field("anzahl_seiten","integer",label=T('Anzahl Seiten'),requires=IS_IN_SET((1,2)), default=2),
     Field("druckfarbe","string",label=T('Druckfarbe'), requires=IS_IN_SET(('4/0','4/4')) ),
     Field("pruefung_trimbox","string",label=T('Prüfung Trimbox'), requires=IS_IN_SET(('yes','no'))),
     Field("prueftoleranz","string",label=T('Prüftoleranz'), default=4),
     Field("papiertyp","string",label=T('Papiertyp'), requires=IS_IN_SET(('cov-1','cov-2','cov-5')) ),
     Field("laminierungsart","string",label=T('Laminierungsart'), requires=IS_IN_SET(('gloss','matte'))),
     Field("barcode_position","string",default='bottom right', label=T('Barcode Position'), requires=IS_IN_SET(('bottom right',"bottom-center","bottom-left","front-bottom-left","front-bottom-center","front bottom-right"))),
     Field("dateiname_pdf_innerwork_","upload",label=T('Dateiname PDF (innerwork)')),#TODO isbdn ohne bindestirche .innerwork.pdf automatisch generieren , ein neues feld
     Field("teilnummer","integer",default=1, label=T('Teilnummer')),
     Field("anzahl_seiten","integer",label=T('Anzahl Seiten'), writable=False),
     Field("farbraum","string",label=T('Farbraum'),requires=IS_IN_SET(("Graustufen","CMYK"))),
     Field("anzahl_farbseiten","integer",label=T('Anzahl Farbseiten')),
     Field("breite_der_trimbox","integer",label=T('Breite der Trimbox')),
     Field("hoehe_der_trimbox","integer",label=T('Höhe der Trimbox')),
     Field("pruefung_trimbox","string",label=T('Prüfung Trimbox'),requires=IS_IN_SET(("yes","no"))),
     Field("prueftoleranz","double",label=T('Prüftoleranz')),
     Field("f_papiertyp","string",label=T('Papiertyp'),requires=IS_IN_SET(("iw-2", "iw-3", "iw-10", "iw-12", "iw-13", "iw-15"))),
     Field("letzte_seite","string",default="yes",label=T('Letzte Seite'),requires=IS_IN_SET(('yes','no'))),
     migrate=settings.migrate,
     redefine=True
)
'''
request_client = ''
if request.client:
    request_client_sp = request.client.split('.')
    if len(request_client_sp) ==4 :
        request_client = request_client_sp[0]+'.'+request_client_sp[1]+'.'+request_client_sp[2]+'.xxx'

db.define_table('t_usage_statistics',
    Field('time_stamp','datetime', default=request.now),
    Field('client_ip','string', default=request_client),
    Field('request_controller','string', default=request.controller),
    Field('request_function','string', default=request.function),
    Field('request_extension','string', default=request.extension),
    Field('request_ajax','string', default=request.ajax),
    Field('request_args','string', default=request.args),
    Field('request_vars','string', default=request.vars),
    Field('request_view','string', default=request.view),
    Field('request_http_user_agent','string', default=request.env.http_user_agent),
    Field('request_language','string', default=request.env.http_accept_language),
    Field('description', 'text'),
    migrate=False,
    )
