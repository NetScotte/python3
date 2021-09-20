# -*- coding: utf-8 -*-
"""
功能：
设计：
参数：
作者: netliu
时间：
"""
import re
import itertools
import time
import urllib.request as urlrequest
from urllib.error import URLError, HTTPError, ContentTooShortError
from urllib.parse import urljoin, urlparse
from urllib import robotparser
from lxml.html import fromstring


class Throttle:
    """
    Add a delay between downloads to the same domain
    """
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed:
            sleep_secs = self.delay - (time.time() - last_accessed)
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = time.time()


def download(url, user_agent="wswp", num_retries=2, charset="utf-8", proxy=None):
    print("Downloading: ", url)
    request = urlrequest.Request(url)
    request.add_header("User-agent", user_agent)
    try:
        # 使用urllib支持代理
        if proxy:
            proxy_support = urlrequest.ProxyHandler({"http": proxy})
            opener = urlrequest.build_opener(proxy_support)
            urlrequest.install_opener(opener)
        resp = urlrequest.urlopen(request)
        cs = resp.headers.get_content_charset()
        if not cs:
            cs = charset
        html = resp.read().decode(cs)
    except (URLError, HTTPError, ContentTooShortError) as e:
        print("Download error: ", e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code <= 600:
                return download(url, num_retries=num_retries-1)
    return html


# sitemap基本爬虫
def crawl_sitemap(url):
    sitemap = download(url)
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    for link in links:
        download(link)


# id遍历爬虫
def crawl_site(url, max_errors=5):
    num_errors = 0
    for page in itertools.count(1):
        pg_url = "{}{}".format(url, page)
        html = download(pg_url)
        if not html:
            num_errors += 1
            if num_errors > max_errors:
                break
        else:
            # success - can scrape the result
            num_errors = 0


def link_crawler(start_url, link_regex, robots_url=None, user_agent="wswp", delay=5, max_depth=4, scrape_callback=None):
    """
    Crawl from the given start URL flowing links matched by link_regex
    :param start_url:
    :param link_regex:
    :return:
    """
    if not robots_url:
        robots_url = "{}/robots.txt".format(start_url)
    throttle = Throttle(delay)
    rp = get_robots_parser(robots_url)
    crawl_queue = [start_url]
    # 避免重复爬取，需要记录爬取过的url
    # seen = set(crawl_queue)
    # 将seen更新为字典，记录深度: 到达该网页经历了多少个链接
    seen = {}
    data = []
    while crawl_queue:
        url = crawl_queue.pop()
        if rp.can_fetch(user_agent, url):
            depth = seen.get(url, 0)
            if depth > max_depth:
                print("Skipping %s due to depth" % url)
                continue
            throttle.wait(url)
            html = download(url)
        else:
            print("Blocked by robots.txt: ", url)
            continue

        if not html:
            continue

        if scrape_callback:
            data.extend(scrape_callback(url, html) or [])
        # custom: 如果当前页面的深度已经达到了最大值，那么就不用解析当前页面的url了
        if depth == max_depth:
            continue

        for link in get_links(html):
            if re.match(link_regex, link):
                abs_link = urljoin(start_url, link)
                if abs_link not in seen:
                    # seen.add(abs_link)
                    seen[abs_link] = depth + 1
                    crawl_queue.append(abs_link)


def get_links(html):
    """
    Retuen a list of links from html
    :param html:
    :return:
    """
    # 如下的正则表达式[^>]是什么意思
    webpage_regex = re.compile("""<a[^>]href=["'](.*?)["']""", re.IGNORECASE)
    return webpage_regex.findall(html)


def get_robots_parser(robots_url):
    """
    Return the robots parser object using the robots_url
    :param robots_url:
    :return:
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp


def scrape_callback(url, html):
    fields = ("area", "population", "iso", "country_or_district")
    if re.search("/view/", url):
        tree = fromstring(html)
        allow_rows = [tree.xpath("//tr[@id='places_%s__row']/td[@class='w2p_fw']" % field)[0].text_content() for field in fields]
        print(url, allow_rows)