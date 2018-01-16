#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 11 Jan 2018

@author: wit
'''

import datetime
import json
import os
from string import Template

from ompdal import OMPDAL



ompdal = OMPDAL(db, myconf)


class Templates:

    def __init__(self):
        pass

    def url(self, x):
        loc = x[0]
        lastmod = x[1]
        changefreq = 'weekly'
        priority = x[2] if len(x) == 3 else 0.5
        try:
            loc = '{}{}'.format(myconf['web']['url'], loc)
        except:
            print('web.url not defined in appconfig.ini')

        t = Template(
            '<url><loc>/${loc}</loc><lastmod>$lastmod</lastmod><changefreq>$changefreq</changefreq><priority>$priority</priority></url>')
        return t.substitute(loc=loc, lastmod=lastmod, changefreq=changefreq, priority=priority)

    def url_set(self, urls):
        urls_str = '\n'.join(urls)
        return '{}\n{}\n{}'.format('<urlset xmlns = "http://www.sitemaps.org/schemas/sitemap/0.9" >', urls_str,
                                   '</urlset>')


class SiteMap:

    def __init__(self):
        self.path = '{}/{}'.format(request.env.web2py_path, request.folder)
        self.PRESS_ID = myconf.take('omp.press_id')
        self.stop_words = ['snippets']
        self.site_map_priority = '{}/{}'.format(self.path, 'sitemap.json')
        self.t = Templates()
        self.views = '{}/{}'.format(self.path, 'views')

    def create_monographs(self):
        submissions = ompdal.getSubmissionsByPress(self.PRESS_ID).as_list()
        return list(map(lambda x: ('/catalog/book/{}'.format(x['submission_id']), x['last_modified'].date(), 0.9),
                        submissions))

    def create_series(self):
        series = ompdal.getSeriesByPress(self.PRESS_ID).as_list()
        s = list(map(lambda x: ('/series/{}'.format(x['path']), datetime.datetime.now().date(), 0.9),series))
        s_info = list(map(lambda x: ('/series/info/{}'.format(x['path']), datetime.datetime.now().date(), 0.9),                        series))
        return s + s_info

    def create_sitemap(self):
        file_list = self.create_monographs() + self.create_static_map()+ self.create_series()
        return self.t.url_set(list(map(lambda x: self.t.url(x), file_list)))

    def get_files(self):
        files = []
        for root, directories, filenames in os.walk(self.views):
            for filename in filenames:
                date_modified = (datetime.datetime.fromtimestamp(os.path.getmtime(root)).date())
                files.append((os.path.join(root.replace(self.views, ''), filename), date_modified.isoformat()))
        return files

    def remove_unwanted_files(self, l):
        l = list(filter(lambda x: x[0].endswith('.html'), l))
        l = list(filter(lambda x: x[0].startswith('/'), l))
        l = list(filter(lambda x: x[0] not in self.stop_words, l))
        return l

    def read_configuration(self):
        if os.path.exists(self.site_map_priority):
            with open(self.site_map_priority) as f:
                return json.load(f)
        else:
            print('{} {}'.format('File not found:\t', self.site_map_priority))

    def create_static_map(self):
        dirs = self.read_configuration().get('directories')

        paths = list(map(lambda x: x["path"], dirs))

        l = self.remove_unwanted_files(self.get_files())

        for i in xrange(len(l)):
            d = l[i][0].split('/')[1]
            if d in paths:
                j = filter(lambda x: x['path'] == d, dirs)
                prio = j[0]['priority'] if j else 0.5
                l[i] = l[i] + (prio,)

        return l


if __name__ == '__main__':
    s = SiteMap()
    # print(s.read_configuration())
    # print(s.get_files())
    # print(s.set_configuration())
    print(s.create_sitemap())
    #print(s.create_monographs())
    #print(s.create_series())

