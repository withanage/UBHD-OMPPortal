#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 28 Sep 2016

@author: wit
'''
import sys
import os
import time
import stat
import datetime
import csv


from gluon.restricted import RestrictedError, TicketStorage
from gluon import DAL
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth, Service, PluginManager, Crud
from operator import itemgetter
from ompdal import OMPDAL, OMPSettings, OMPItem
from ompformat import dateFromRow, seriesPositionCompare



ompdal = OMPDAL(db, myconf)


def insert_sfs(name, file_id,value):
    d= db.submission_file_settings
    r =  db((d.setting_name==name) & (d.file_id==file_id) & (d.setting_value==value)).select()
    
    if len(r)==0 :
        print file_id, name,value, 'updated'
        s = db.submission_file_settings.insert(setting_name=name,file_id=file_id, setting_value=value, setting_type='', locale='')
        db.commit()
    return 
        
def get_csv(c):
    with open(c, 'rb') as csvfile:
        cs = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        for row in cs:
            if len(row) == 3:
                insert_values(row[0],row[1],row[2])
                
    return
     
def  insert_values(sid,vgWortPublic, vgWortPrivate ):
    pfs =  ompdal.getPublicationFormatsBySubmission(sid, available=True, approved=True)
    if  pfs:
        for pf in pfs:
            sfs = db(db.submission_files.assoc_id==pf.get('publication_format_id')).select()
            if sfs:
                for sf in sfs: 
                    fid= sf['file_id']
                    insert_sfs('vgWortPublic',fid,vgWortPublic)
                    insert_sfs('vgWortPrivate',fid,vgWortPrivate )
                    
                    
    return


if __name__ == '__main__':
    #get_vgwort_public()
    p =  sys.argv[0].split('/')
    p.pop() # removes file name
    p.append('vgwort.csv')
    c = os.path.join(*p) 
    if os.path.isfile(c): 
        get_csv(c)
    else:
        print c,'is', 'undefined'