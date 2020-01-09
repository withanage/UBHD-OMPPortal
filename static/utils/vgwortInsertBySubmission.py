#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 28 Sep 2016

@author: wit
'''
import sys
import os

from xlrd import open_workbook
from gluon import DAL
from ompdal import OMPDAL


ompdal = OMPDAL(db, myconf)


def insert_sfs(name, file_id, value):
    d = db.submission_file_settings
    r = db((d.setting_name == name) & (d.file_id == file_id)).select()
    if len(r) == 0:
        print(file_id, name, value, 'updated')
        s = db.submission_file_settings.insert(
            setting_name=name,
            file_id=file_id,
            setting_value=value,
            setting_type='',
            locale='')
        db.commit()
    return


def insert_values(sid, vgWortPublic, vgWortPrivate):
    pfs = ompdal.getPublicationFormatsBySubmission(
        sid, available=True, approved=True)
    if pfs:
        for pf in pfs:
            sfs = db(db.submission_files.assoc_id ==
                     pf.get('publication_format_id')).select()
            if sfs:
                for sf in sfs:
                    fid = sf['file_id']
                    insert_sfs('vgWortPublic', fid, vgWortPublic)
                    insert_sfs('vgWortPrivate', fid, vgWortPrivate)

    return


def get_excel(c):

    wb = open_workbook(c)
    FORMAT = ['submission_id', 'vgWortPublic', 'vgWortPrivate']

    for s in wb.sheets():
        headerRow = s.row(0)
        columnIndex = [x for y in FORMAT for x in range(
            len(headerRow)) if y == headerRow[x].value]
        for row in range(1, s.nrows):
            currentRow = s.row(row)
            row = [currentRow[x].value for x in columnIndex]
            insert_values(int(row[0]), row[1], row[2])

    return


if __name__ == '__main__':
    p = sys.argv[0].split('/')
    p.pop()  # removes file name
    p.append('vgwort.xls')
    c = os.path.join(*p)
    if os.path.isfile(c):
        get_excel(c)
    else:
        print c, 'is', 'undefined'
