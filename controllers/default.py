# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''

# required - do no delete
def user(): return dict(form=auth())

def download(): return response.download(request, db)

def call():
    session.forget()
    return service()
# end requires

def index():
    return dict()

def error():
    return dict()

def set_knv_metadata():
    if len(db(db.t_knv_metadata.submission_id == request.args(0)).select(db.t_knv_metadata.submission_id)) > 0:
        redirect(URL('set_onix_data/' + request.args(0)))
    #form.element(name='file')['_onchange']='... your js here ...'
    form = SQLFORM(db.t_knv_metadata, record=None,
                   deletable=False, linkto=None,
                   upload=None, fields=None, labels=None,
                   col3={
                       'rueckenart': DIV(B(T("Bei PB ist nur square möglich.")), _class="alert alert-success"),
                       'speicherung': DIV(B(T('"temp" zum einmaligen Testen')), _class="alert alert-success"),
                       'anzahl_seiten': DIV(B(T('bei 4/0 Seitenzahl = 1, bei 4/4 Seitenzahl = 2')), _class="alert alert-success"),
                       'druckfarbe': DIV(B(T('z. B. 4/0 Außenumschlag farbig, innen unbedruckt.')), _class="alert alert-success"),
                       'pruefung_trimbox': DIV(B(T('yes setzt voraus, dass im PDF die Trimbox gesetzt ist. Bei no wird innerhalb der Mediabox zentriert.')), _class="alert alert-success"),
                       'prueftoleranz': DIV(B(T('Nur wenn check-trim-box yes ist, Standardwert 4 mm, kann aber frei gewählt werden.')), _class="alert alert-success"),
                       'papiertyp': DIV(B(T('PB: cov-4 = einseitig gestrichener Sulfatkarton / 240 gr , cov-5 / beidseitig halbmatt gestrichener Karton / 300 gr. , bei HB: cov-1: halbmatt / 150 gr.')), _class="alert alert-success"),
                       'breite_der_trimbox': DIV(B(T('Endformatbreite, min. 105 / max. 210 bei PB, bei HB min. 148 / max. abhängig von Rückenbreite, aufgeklappter Buchdeckel max. 450.')), _class="alert alert-success"),
                       'hoehe_der_trimbox': DIV(B(T(' min. 150 / max. 297 bei PB, bei HB min. 155 / max. 280.')), _class="alert alert-success"),
                       'prueftoleranz': DIV(B(T('Nur wenn Prüfung Trimbox "yes" ist, Standardwert 2,5 mm, kann aber frei gewählt werden. Bei Dezimalzahlen Trennzeichen "Punkt".')), _class="alert alert-success"),
                       'f_papiertyp': DIV(B(T('bei PB: ')), BR(), B(T('iw-2: Matt MC / 080 gr / 0,93 Volumen')), BR(), B(T('iw-3: Offset weiß / 080 gr / 1,28 Volumen')), BR(), B(T('iw-10: Offset weiß / 120 gr / 1,28 Volumen ')), BR(), B(T(' iw-12: Werkdruck / 090 gr / 1,30 Volumen')), BR(), B(T(' iw-13: Matt MC / 115 gr / 0,93 Volumen ')), BR(), B(T('iw-15: Munken Premium / 080 gr / 1,30 Volumen ')), BR(), B(T('bei HB:')), BR(), B(T(' iw-2: Matt MC / 080 gr / 0,93 Volumen')), BR(), B(T(' iw-3: Offset weiß / 080 gr / 1,28 Volumen')), BR(), B(T(' iw-12: Werkdruck / 090 gr / 1,30 Volumen ')), BR(), B(T('iw-15: Munken Premium / 080 gr / 1,30 Volumen ')), _class="alert alert-success"),
                       'letzte_seite': DIV(B(T('Fügt bei PB automatisch eine letzte Seite mit Druckimpressum ein, Standardwert ist yes bei fehlender Angabe.')), _class="alert alert-success"),

                   },
                   submit_button='Einfügen',
                   delete_label='Check to delete:',
                   showid=True, readonly=False,
                   comments=True, keepopts=[],
                   ignore_rw=False, record_id=None,
                   formstyle='table3cols',
                   # buttons=['Einfügen'],
                   separator=': ',
                   )
    form[0].insert(11, DIV(H3('Cover', _style='color:green')))
    form[0].insert(29, DIV(H3('Buchblock', _style='color:green')))
    if form.process().accepted:
        redirect(URL('set_onix_data/' + request.args(0)))
    return dict(form=form)

def get_onix_data():
    if not request.args(0):
        redirect(URL('error'))
    data = db(db.t_onix_additionals.submission_id ==
              request.args(0)).select().first()
    authors_pre = db(db.authors.submission_id == submission_id).select(db.authors.last_name,
                                                                       db.authors.first_name, db.authors.user_group_id, db.authors.country, db.authors.author_id)
    locale_pre = db(db.submissions.submission_id == submission_id).select(
        db.submissions.locale).first()
    locale = locale_pre['locale'] if locale_pre else 'de_DE'
    publication_formats = db(
        db.publication_formats.submission_id == submission_id).select()
    title_text = db((db.submissions.submission_id == submission_id) & (db.submission_settings.submission_id == db.submissions.submission_id) & (
        db.series_settings.locale == locale) & (db.series_settings.setting_name == 'title')).select(db.series_settings.setting_value).first()['setting_value']

    return dict(data=data, authors_pre=authors_pre, locale=locale, publication_formats=publication_formats, title_text=title_text)
    # return dict(data=crud.read(db.t_onix_additionals, request.args(0)))

def onix_additionals_manage():
    form = SQLFORM.smartgrid(
        db.t_onix_additionals, onupdate=auth.archive, user_signature=False,  exportclasses=None)
    return locals()

def set_onix_data():
    if (request.args(0) is None) | (len(db(db.t_onix_additionals.submission_id == request.args(0)).select(db.t_onix_additionals.submission_id)) > 0):
        redirect(URL('get_books'))
    if not db(db.t_knv_metadata.submission_id == request.args(0)).select(db.t_knv_metadata.submission_id):
        redirect(URL('set_knv_metadata/' + request.args(0)))
    book_id = request.args(0)
    crud.settings.create_next = URL('index')
    crud.settings.detect_record_change = True
    crud.settings.formstyle = 'table3cols'
    crud.messages.submit_button = 'Einfügen'
    form = SQLFORM(db.t_onix_additionals, record=None,
                   deletable=False, linkto=None,
                   upload=None, fields=None, labels=None,
                   col3={
                       'f_verlagsverkehrsnummer': DIV(B(T(".")), _class=""),
                   },
                   submit_button='Einfügen',
                   delete_label='Check to delete:',
                   showid=True, readonly=False,
                   comments=True, keepopts=[],
                   ignore_rw=False, record_id=None,
                   formstyle='table3cols',
                   # buttons=['Einfügen'],
                   separator=': ',
                   )
    if form.process().accepted:
        redirect(URL('get_books'))
    '''
     n_fields = len(form[0].components)
     fields = form[0].components
     bot_half = fields[n_fields/2:]
     top_half = fields[:n_fields/2]
     form[0]=TABLE(
            TR(
             TD(TABLE(*top_half,_class="table table-hover")),
             TD(TABLE(*bot_half,_class="table table-hover"))
            )
     )
     '''
    published_submissions = crud.select(
        db.published_submissions, db.published_submissions.submission_id == book_id)
    publication_formats = crud.select(
        db.publication_formats, db.publication_formats.submission_id == book_id)
    submissions = crud.select(
        db.submissions, db.submissions.submission_id == book_id)
    submissions = crud.select(
        db.submissions, db.submissions.submission_id == book_id)
    submission_settings = crud.select(
        db.submission_settings, db.submission_settings.submission_id == book_id)
    return dict(form=form,
                published_submissions=published_submissions,
                publication_formats=publication_formats,
                submissions=submissions,
                submission_settings=submission_settings
                )

def get_books():
    query = (db.submission_settings.submission_id == db.submissions.submission_id) & (
        db.submission_settings.setting_name == 'title') & (db.t_onix_additionals.submission_id == db.submission_settings.submission_id)

    entries = SQLFORM.grid(
        query,
        fields=[db.submission_settings.submission_id,
                db.submission_settings.setting_value, db.submissions.date_submitted],
        field_id=None,
        left=None,
        headers={},
        orderby=db.submission_settings.submission_id,
        groupby=db.submission_settings.submission_id,
        searchable=False,
        sortable=True,
        paginate=20,
        deletable=False,
        editable=False,
        details=True,
        selectable=None,
        create=False,
        csv=False,
        links=[

            dict(header=T('ONIX'), body=(lambda row: A('ONIX', _href=T(
                'get_onix_data/' + str(row.submission_settings.submission_id))))),
            dict(header=T('KNV'), body=(lambda row: A('XML', _href=T(
                'get_knv_metadata.xml/' + str(row.submission_settings.submission_id))))),

        ],
        links_in_grid=True,
        upload='<default>',
        args=[],
        user_signature=False,
        maxtextlengths={},
        maxtextlength=20,
        onvalidation=None,
        oncreate=None,
        onupdate=None,
        ondelete=None,
        sorter_icons=(XML('&#x2191;'), XML('&#x2193;')),
        ui='web2py',
        showbuttontext=True,
        _class="web2py_grid",
        formname='web2py_grid',
        search_widget='default',
        ignore_rw=False,
        formstyle='table3cols',
        exportclasses=None,
        formargs={},
        createargs={},
        editargs={},
        viewargs={},
        buttons_placement='right',
        links_placement='right'
    )
    unpublised_query = (db.submission_settings.submission_id == db.submissions.submission_id) & (
        db.submission_settings.setting_name == 'title')

    onix_view = dict(header=T('ONIX'), body=(lambda row: A('ONIX', _href=T(
        'get_onix_data/' + str(row.submission_settings.submission_id))))),
    unpublised_entries = SQLFORM.grid(
        unpublised_query,
        fields=[db.submission_settings.submission_id,
                db.submission_settings.setting_value, db.submissions.date_submitted],
        field_id=None,
        left=None,
        headers={},
        orderby=~db.submission_settings.submission_id,
        groupby=db.submission_settings.submission_id,
        searchable=False,
        sortable=True,
        paginate=20,
        deletable=False,
        editable=False,
        details=True,
        selectable=None,
        create=False,
        csv=False,
        links=[
            dict(header=T('Status'), body=(lambda row: '' if len(db(db.t_onix_additionals.submission_id == row.submission_settings.submission_id).select(
            )) > 0 else A('In KNV zuschicken', _href=T('set_knv_metadata/' + str(row.submission_settings.submission_id))))),
            dict(header=T('KNV-XML'), body=(lambda row: A('KNV', _href=T('get_knv_metadata.xml/' + str(row.submission_settings.submission_id)))
                                            if len(db(db.t_onix_additionals.submission_id == row.submission_settings.submission_id).select()) > 0 else '')),
            dict(header=T('Onix'), body=(lambda row: A('ONIX', _href=T('get_onix_data/' + str(row.submission_settings.submission_id)))
                                         if len(db(db.t_onix_additionals.submission_id == row.submission_settings.submission_id).select()) > 0 else ''))
        ],
        links_in_grid=True,
        upload='<default>',
        args=[],
        user_signature=False,
        maxtextlengths={},
        maxtextlength=20,
        onvalidation=None,
        oncreate=None,
        onupdate=None,
        ondelete=None,
        sorter_icons=(XML('&#x2191;'), XML('&#x2193;')),
        ui='web2py',
        showbuttontext=True,
        _class="web2py_grid",
        formname='web2py_grid',
        search_widget='default',
        ignore_rw=False,
        formstyle='table3cols',
        exportclasses=None,
        formargs={},
        createargs={},
        editargs={},
        viewargs={},
        buttons_placement='right',
        links_placement='right'
    )

    return dict(entries=entries, unpublised_entries=unpublised_entries)
