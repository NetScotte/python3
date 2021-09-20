# -*- coding: utf-8 -*-
"""
功能：
设计：
参数：
作者: netliu
时间：
"""
import unittest
from scrap.scrap1 import *
from scrap.csv_callback import CsvCallback

class Scrap1Test(unittest.TestCase):
    def setUp(self):
        self.url = "http://example.python-scraping.com/"

    def test_download_sample_url(self):
        print(download(self.url))

    def test_crawl_sitemap(self):
        crawl_sitemap("http://example.python-scraping.com/sitemap.xml")

    def test_crawl_site(self):
        crawl_site("http://example.python-scraping.com/view/")

    def test_link_crawler(self):
        link_crawler('http://example.python-scraping.com', '.*?/(index|view)/')

    def test_link_crawler_with_bad_agent(self):
        link_crawler('http://example.python-scraping.com', '.*?/(index|view)/', user_agent="BadCrawler")

    def test_link_crawler_normal(self):
        link_crawler('http://example.python-scraping.com/index', '.*?/(index|view)/', max_depth=1)

    def test_link_crawler_callback(self):
        link_crawler('http://example.python-scraping.com', '.*?/(index|view)/', scrape_callback=scrape_callback)

    def test_link_crawler_csvcallback(self):
        csvcallback = CsvCallback("./csvcallback.csv")
        link_crawler('http://example.python-scraping.com', '.*?/(index|view)/', max_depth=1, scrape_callback=csvcallback)