# coding: utf-8
#!/usr/bin/env python

# The MIT License

# Copyright 26-Apr-2016, 15:12:43
#
# Author    : Dulip Withanage , University of Heidelberg
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import json
import os
import mysql.connector
import sys
import operator
import logging
import socket
import struct
from html import HTML

logging.basicConfig(filename='jatsPostProcess.log', level=logging.DEBUG)


class BookStats:

    def __init__(self, config):
        self.config = self.get_config(config)
        self.con = self.get_connection(self.get_config(config))
        self.cursor = self.con.cursor()
        self.locale = '"de_DE"'
        self.h = HTML()

    def __del__(self):
        self.cursor.close()
        self.con.close()

    def ip2long(self, ip):
        """
        Convert an IP string to long
        """
        packedIP = socket.inet_aton(ip)
        return struct.unpack("!L", packedIP)[0]

    def get_ips(self, m):
        """
        returns the IPS per monograph
        """
        r = list()
        q = ''.join(
            [
                "SELECT request_args,  INET_ATON(REPLACE(client_ip, 'xxx', '0')), 1 FROM omp.t_usage_statistics where request_args like '|",
                str(m),
                "|%' "])
        self.cursor.execute(q)
        [r.append((row[0], row[1], row[2])) for row in self.cursor]
        return r

    def get_chapter_name(self, m):
        """
        returns the Chapter name of monograph
        """
        q = ''.join(
            [
                'SELECT scs.setting_value FROM  omp.submission_chapter_settings scs , omp.submission_chapters sc, omp.submission_file_settings sfs  where  scs.chapter_id = sc.chapter_id and sfs.setting_value = sc.chapter_id and   sfs.setting_name="chapterID" and sfs.file_id = ',
                str(m),
                '  and scs.locale = ',
                self.locale,
                ' and scs.setting_name ="title"  order by sc.chapter_seq ;'])
        try:
            self.cursor.execute(q)
        except:
            logging.error(q)
        return [row for row in self.cursor]

    def u(self, s):
        """
        converst to utf-8
        """
        return s.encode('utf-8')

    def filter_ip(self, ip, list):
        """
        filters a list of ips
        """
        for i in list:
            if ip == self.ip2long(i):
                return False

        else:
            return True

    def get_stats_by_country(self, iplist, pos, filter):
        """
        returns dictionary for a list of ips as sets, where  ip is in position pos
        """
        rs = {}
        for ips in iplist:
            if self.filter_ip(ips[pos], filter):
                q = "".join(["SELECT country_code, country_name  FROM omp.t_geoip_country where  INET_ATON(ip_begin) < ", str(
                    ips[pos]), " and INET_ATON(ip_end) > ", str(ips[pos]), ";"])
                try:
                    self.cursor.execute(q)
                except:
                    logging.error(q)
                for row in self.cursor:
                    f = ips[0].strip()
                    if rs.get(f):
                        if rs.get(f).get(row[1]):
                            rs[f][row[1]] = ips[2] + rs[f][row[1]]
                        else:
                            rs[f][row[1]] = ips[2]
                    else:
                        rs[f] = {}
                        rs[f][row[1]] = ips[2]
        return rs

    def filter_monographs(self, s):
        """
        filter the monographs with length
        """
        return True if len(s) == 32 or len(s) == 4 else False

    def create_html(self, m, filter):
        """
        generates HTML Table
        """
        result = self.get_stats_by_country(self.get_ips(m), 1, filter)
        t = self.h.table(style=" border-collapse: collapse; border: 1px solid black;")
        for r in sorted(result):
            ls = sum(result[r].values())
            if self.filter_monographs(r):
                if len(r.split('-')) > 2:
                    if r.split('-')[2]:
                        chapter = self.get_chapter_name(r.split('-')[2])
                        cn = '\t'.join([chapter[0][0],
                                        ' (',
                                        str(r.split('.')[1].rsplit('|')[0]),
                                        ')']) if chapter else '\t'.join(['Full',
                                                                         r.split('.')[1].replace('|',
                                                                                                 '')])
                        tr = t.tr(bgcolor="#dfdfdf")
                        tr.th(self.u(cn))
                        tr.th(str(ls))
                else:
                    tr = t.tr(bgcolor="grey")
                    tr.th(self.u(r))
                    tr.th(str(ls))
                for c in sorted(
                        result[r].items(),
                        key=operator.itemgetter(1),
                        reverse=True):
                    tr = t.tr(style="border: 1px solid black;")
                    tr.td(str(c[0]))
                    tr.td(str(c[1]))
        return ''.join(['<head><meta charset="utf-8"></head> ',str(t)])

    def get_config(self, f):
        """
        get config file
        """
        try:
            with open(f) as j:
                conf = json.load(j)
            return conf
        except:
            print ' '.join([f, ' file not found']), sys.exit(1)

    def get_connection(self, config):
        """
        get a mysql connection
        """
        cnx = mysql.connector.connect(
            user=config["mysql"]["user"],
            password=config["mysql"]["passwd"],
            host=config["mysql"]["host"],
            database=config["mysql"]["db"])
        return cnx

    def create_stats(self, bs, m):
        """
        generate stats html, with filter and without filter
        """
        ofilter = ''.join([os.getcwd(), '/', str(m), '-filter.html'])
        f = open(ofilter, 'w')
        f.write(bs.create_html(m, bs.config["filters"]))
        f.close()

        outfile = ''.join([os.getcwd(), '/', str(m), '.html'])
        f = open(outfile, 'w')
        f.write(bs.create_html(m, []))
        f.close()
if __name__ == "__main__":

    m = sys.argv[1] if len(sys.argv) > 1 else ''
    bs = BookStats("bookStatsConfig.json")
    bs.create_stats(bs, m)
