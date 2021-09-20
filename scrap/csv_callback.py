# -*- coding: utf-8 -*-
"""
功能：
设计：
参数：
作者: netliu
时间：
"""
import csv
import re
from lxml.html import fromstring
import unittest

class CsvCallback:
    def __init__(self, filename):
        self.file = open(filename, "w")
        self.writer = csv.writer(self.file)
        self.fields = ("area", "population", "iso", "country_or_district")
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search("/view/", url):
            tree = fromstring(html)
            allow_rows = [tree.xpath("//tr[@id='places_%s__row']/td[@class='w2p_fw']" % field)[0].text_content() for
                          field in self.fields]
            self.writer.writerow(allow_rows)

    def __del__(self):
        self.file.close()

