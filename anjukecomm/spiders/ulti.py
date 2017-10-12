# coding: utf-8
import requests
from lxml import etree


def getcity():
    url = 'https://m.anjuke.com/cityList/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}
    s = requests.Session()
    result = s.get(url=url, headers=headers)
    content = result.text
    tree = etree.HTML(content)
    city = tree.xpath('//div[@class="cl-c-l-h"]')
    l= city.xpath('.//li[@class="cl-c-l-li"]/a/text()')
    for i in l:
        print i
#getcity()

