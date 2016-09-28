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


from gluon.restricted import RestrictedError, TicketStorage
from gluon import DAL
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth, Service, PluginManager, Crud
from operator import itemgetter
from ompdal import OMPDAL, OMPSettings, OMPItem
from ompformat import dateFromRow, seriesPositionCompare

ompdal = OMPDAL(db, myconf)

file_id = 149
vgWortPublic = 'c0530bfec7d34921a385be9052b37f2f'
vgWortPrivate=''

def insert_sfs(name, file_id,value):
    try:
        db.submission_file_settings.insert(setting_name=name,file_id=file_id, setting_value=value)
        db.commit()
    except:
        print file_id , value , " could not be inserted"
        

def get_vgwort_public():
    pfs =  ompdal.getPublicationFormatsBySubmission( file_id, available=True, approved=True)
    if  pfs:
        for pf in pfs:
            sfs = db(db.submission_files.assoc_id==pf.get('publication_format_id')).select()
            if sfs:
                for sf in sfs: 
                    fid= sf['file_id']
                    insert_sfs('vgWortPublic',fid,vgWortPublic )
                    insert_sfs('vgWortPrivate',fid,vgWortPrivate )
                    
                    
    return


if __name__ == '__main__':
    
    get_vgwort_public()