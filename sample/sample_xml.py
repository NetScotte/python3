# -*- coding: utf-8 -*-
"""
功能： 对xml进行解析，展示xml.etree.ElementTree
设计：
备注：
时间：
"""
import xml.etree.ElementTree as ET

# 也可以使用fromstring()直接解析字符串
tree = ET.parse("../files/daemon.xml")
# 如果每次只能传递xml文档的部分信息，可以使用XMLPullParser()
# parser = ET.XMLPullParser(['start', 'end'])
# parser.feed('<mytag>sometext')
# parser.feed(' more text</mytag>')
# for event, elem in parser.read_events():
# ...     print(event)
# ...     print(elem.tag, 'text=', elem.text)
root = tree.getroot()


# 迭代
def func_iter1():
    print("root.tag: {}".format(root.tag))
    print("root.attrib: {}".format(root.attrib))
    print()
    print("{0}{1}{0}".format("*" * 20, "for"))
    print()
    for child in root:
        print("child.tag: {}".format(child.tag))
        print("child.attrib: {}".format(child.attrib))
        for index, node in enumerate(child):
            print("{}{}".format("*" * 10, node.text))
        print()
        # 可以直接使用索引获取对象
        # print("root[0][0].text: {}".format(root[0][0].text))


# 迭代2
def func_iter2():
    print()
    print("{0}{1}{0}".format("*" * 20, "iter"))
    print()
    for neighbor in root.iter('neighbor'):
        print(neighbor.attrib)


# 查找
def func_find():
    print()
    print("{0}{1}{0}".format("*" * 20, "find"))
    print()
    for country in root.findall('country'):
        rank = country.find('rank').text
        name = country.get('name')
        print(name, rank)


# 修改
def func_modify():
    print()
    print("{0}{1}{0}".format("*" * 20, "修改"))
    print()
    for rank in root.iter('rank'):
        new_rank = int(rank.text) + 1
        rank.text = str(new_rank)
        rank.set('updated', 'yes')
    tree.write('output.xml')


# 移除
def func_remove():
    print()
    print("{0}{1}{0}".format("*" * 20, "移除"))
    print()
    for country in root.findall('country'):
        rank = int(country.find('rank').text)
        if rank > 50:
            root.remove(country)
    tree.write('output.xml')


# 构建
def func_build():
    print()
    print("{0}{1}{0}".format("*" * 20, "build"))
    print()
    a = ET.Element('a')
    b = ET.SubElement(a, 'b')
    c = ET.SubElement(a, 'c')
    d = ET.SubElement(c, 'd')
    ET.dump(a)


# 命名空间
def func_namespace():
    """
    :return:
    """
    xml_string = """
    <?xml version="1.0"?>
    <actors xmlns:fictional="http://characters.example.com"
            xmlns="http://people.example.com">
        <actor>
            <name>John Cleese</name>
            <fictional:character>Lancelot</fictional:character>
            <fictional:character>Archie Leach</fictional:character>
        </actor>
        <actor>
            <name>Eric Idle</name>
            <fictional:character>Sir Robin</fictional:character>
            <fictional:character>Gunther</fictional:character>
            <fictional:character>Commander Clement</fictional:character>
        </actor>
    </actors>
    """
    tree = ET.fromstring(xml_string)
    root = tree.getroot()
    print()
    print("{0}{1}{0}".format("*" * 20, "namespace"))
    print()
    ns = {'real_person': 'http://people.example.com',
          'role': 'http://characters.example.com'}

    for actor in root.findall('real_person:actor', ns):
        name = actor.find('real_person:name', ns)
        print(name.text)
        for char in actor.findall('role:character', ns):
            print(' |-->', char.text)


# xpath
def func_xpath():
    print()
    print("{0}{1}{0}".format("*" * 20, "xpath"))
    print()
    # tree.xpath()
    # Top-level elements
    exit(0)
    root.findall(".")

    # All 'neighbor' grand-children of 'country' children of the top-level
    # elements
    root.findall("./country/neighbor")

    # Nodes with name='Singapore' that have a 'year' child
    root.findall(".//year/..[@name='Singapore']")

    # 'year' nodes that are children of nodes with name='Singapore'
    root.findall(".//*[@name='Singapore']/year")

    # All 'neighbor' nodes that are the second child of their parent
    root.findall(".//neighbor[2]")


result = 3.5 + 36.4 + 3.5 + 3.5 + 30.3 + 17.6 + 3.5 + 207.4 + 207.4 - 37.8 - 8.8 - 18.9 - 119 - 22.9 + 3.5 + 33.3 + 99.5 + 3.5 + 123.74 + 6.0 + 2.1 + 27 + 3.15 + 4.5 + 247.5 - 7.0 + 3.15 + 1.2 + 19  + 3.15 + 3.15 + 45.3 + 3.15 + 3.15 + 34.3 + 3.15 + 21.9 + 3.15 + 17.3 + 17.3 + 3.15 + 3.6 + 120 + 6.0 + 79.8 + 83.8 + 300 + 3.15 + 3.15 + 15.0 + 3.15 + 3.15 + 18.2 + 19.0 + 3.15 + 3.15 + 20.2 + 4.5 + + 2.7 + 2.7 + 3.7 + 4.5 + 576.0 + 80.07 + 4.5 + 6.8 + 4.5 + 2.7 + 38.0 + 4.5 + 4.5 + 4.5 + 18.5 + 4.5 + 4.5 + 35.3 + 4.5 + 4.5 + 3.5 + 33.7 + 4.5 + 3.5 + 33.7 + 19.9 + 4.5 + 102.17 + 15.0 + 2.7 + 35.67 + 28.7 + 2.0 + 4.0
print(result)