# -*- coding: utf-8 -*-
"""
功能：
设计：
参数：
作者: netliu
时间：
"""
from lxml.html import fromstring, tostring

# 第一步：将有可能不合法的HTML解析为统一格式
broken_html = "<ul class=country_or_district><li>Area<li>Population</ul>"
tree = fromstring(broken_html)

# 显示解析后的结果
fixed_html = tostring(tree, pretty_print=True)

# 第二步：选择元素
# css选择器
# 选择表格中ID为places_area_row的行元素，然后是类为w2p_fw的子表格数据标签
td = tree.cssselect("tr#places_area_row > td.w2p_fw")[0]
area = td.text_content()
# select any tag: *
# select by tag <a>: a
# select by class of "link": .link
# select by tag <a> with class "link": a.link
# select by tag <a> with id "home": a#home
# select by child <span> of tag <a>: a > span
# select by descendant <span> of tag <a> : a span
# select by tag <a> with attribute title of "home": a[title=home]
# jquery使用: $('div.class_name')

# xpath选择器
# select any tag: *
# select by tag <a>: //a
# select by tag <a> with class "link": //a[@class="link"]
# select by tag <a> with id "home": //a[@id="home"]
# select by child <span> of tag <a>: //a/span
# 从所有段落中选择文本： //p/text()
# 选择所有类名中包含"test"的div元素 //div[contains(@class, "test")]
# 选择所有包含链接或列表的div元素 //div[a|ul]
# 选择href属性中包含google.com的链接 //a[contains(@href, "google.com")]
# 控制台中的用法为$x('//td/img')
area = tree.xpath('//tr[@id="places_area_row"]/td[@class="w2p_fw"]/text()')[0]
