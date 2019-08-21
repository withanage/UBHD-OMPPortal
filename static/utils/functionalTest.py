#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 11 Jan 2018

@author: wit
'''

import datetime
import json
import os
import sys
from os.path import join
from string import Template
from urllib2 import urlopen

from ompdal import OMPDAL

ompdal = OMPDAL(db, myconf)


class Templates:

    def __init__(self):
        pass

    def url(self, x):
        loc = x[0]
        print(loc)
        lastmod = x[1]
        change_frequency = 'weekly'
        priority = x[2] if len(x) == 3 else 0.5

        t = Template(
                '<url>'
                '<loc>${loc}</loc>'
                '<lastmod>$lastmod</lastmod>'
                '<changefreq>$changefreq</changefreq>'
                '<priority>$priority</priority>'
                '</url>')

        return t.substitute(loc=loc, lastmod=lastmod,
                            changefreq=change_frequency, priority=priority)

    def url_set(self, urls):
        urls_str = '\n'.join(urls)

        return '{}\n{}\n{}'.format(
            '<urlset xmlns = "http://www.sitemaps.org/schemas/sitemap/0.9" >',
            urls_str,
            '</urlset>')


class SiteMap:

    def __init__(self):

        self.path = '{}/{}'.format(request.env.web2py_path, request.folder)
        self.press_id = myconf.take('omp.press_id')
        self.stop_words = ['snippets', 'series', 'catalog/snippets', 'partner',
                           'reader', 'default']
        self.site_map_priority = '{}/{}'.format(self.path, 'sitemap.json')
        self.templates = Templates()
        self.static_path = '{}/{}'.format(self.path, 'static')
        self.views_path = '{}/{}'.format(self.path, 'views')
        self.monographs_priority = 0.9
        self.series_priority = 0.9
        self.ignore_apps = ['heiup']

    def create_monographs(self):

        submissions = ompdal.getSubmissionsByPress(self.press_id).as_list()

        return list(map(lambda x: (
            '/catalog/book/{}'.format(x['submission_id']),
            x['last_modified'].date(), self.monographs_priority),
                        submissions))

    def create_series(self):

        series = ompdal.getSeriesByPress(self.press_id).as_list()
        series_map = list(
                map(lambda x: ('/catalog/series/{}'.format(x['path']),
                               datetime.datetime.now().date(),
                               self.series_priority),
                    series))
        series_info_map = list(
                map(lambda x: ('/series/info/{}'.format(x['path']),
                               datetime.datetime.now().date(),
                               self.series_priority),
                    series))

        return series_map + series_info_map

    def http_url(self, x):
        if myconf['web']['application'] not in self.ignore_apps:
            loc = '{}/{}{}'.format(myconf['web']['url'],
                                   myconf['web']['application'], x)
        else:
            loc = '{}{}'.format(myconf['web']['url'], x)
        return loc

    def url_is_ok(self, u):
        try:
            a = urlopen(u)
            if a.getcode() == 200:
                return True
            else:
                return False
        except:
            return False

    def create_sitemap(self):
        file_list = self.create_static_map() + self.create_monographs() + \
                    self.create_series()
        file_list = list(map(lambda x: (self.http_url(x[0]), x[1]), file_list))
        for s in file_list:
            if not self.url_is_ok(s[0]):
                file_list.remove(s)

        return self.templates.url_set(
            list(map(lambda x: self.templates.url(x), file_list)))

    def get_files(self):

        files = []

        for root, directories, filenames in os.walk(self.views_path):
            for f in filenames:

                date_modified = (
                    datetime.datetime.fromtimestamp(
                        os.path.getmtime(root)).date())
                controller_path = root.replace(self.views_path, '')
                if controller_path[1:] not in self.stop_words:
                    if (os.path.getsize(os.path.join(root, f))):
                        files.append(
                                (os.path.join(controller_path, f),
                                 date_modified.isoformat()))
        return files

    def remove_unwanted_files(self, file_list):

        file_list = list(filter(lambda x: x[0].endswith('.html'), file_list))
        file_list = list(filter(lambda x: x[0].startswith('/'), file_list))
        file_list = list(
            filter(lambda x: x[0] not in self.stop_words, file_list))

        return file_list

    def read_configuration(self):

        if os.path.exists(self.site_map_priority):
            with open(self.site_map_priority) as f:
                return json.load(f)
        else:
            print('{} {}'.format('File not found:\t', self.site_map_priority))

    def create_static_map(self):

        dirs = self.read_configuration().get(
            'directories') if self.read_configuration() else []
        paths = list(map(lambda x: x["path"], dirs))
        file_list = self.remove_unwanted_files(self.get_files())

        for item in xrange(len(file_list)):
            d = file_list[item][0].split('/')[1]
            if d in paths:
                j = filter(lambda x: x['path'] == d, dirs) if dirs else d
                priority = j[0]['priority'] if j else 0.5
                file_list[item] = file_list[item] + (priority,)

        return file_list

    def create_sitempap_file(self):

        f = open(join(s.static_path, 'sitemap.xml'), 'w')
        f.write(s.create_sitemap())
        f.close()


if __name__ == '__main__':

    s = SiteMap()
    s.create_sitempap_file()
