# coding: utf-8
import codecs
import json
import re, time, os
import datetime
from lxml import etree
import requests
import scrapy
from anjukecomm.items import RentItem
from anjukecomm.models import House, Price, DBSession


# 移动端
class AnjukeRent(scrapy.Spider):
    name = 'anjuke_rent'
    allowed_domains = ['m.anjuke.com']

    def __init__(self,city=None, *args, **kwargs):
        super(AnjukeRent, self).__init__(*args, **kwargs)
        self.city_name=city
        self.origin = 'AJK'
        self.headers = {
            'accept': 'text/html',
            'accept-encoding': 'gzip, deflate, sdch',
            'accept-language': 'zh-CN,zh;q=0.8',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus)U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
            'x-requested-with': 'XMLHttpRequest',
            'cookie': 'als=0; isp=true; Hm_lvt_c5899c8768ebee272710c9c5f365a6d8=1502856226; sessid=1551E6AF-1AA9-2526-E4E9-D494551F4A2F; search_words361=%E9%98%B3%E5%85%89%E5%B0%8F%E5%8C%BA; search_words24=%E9%9D%96%E6%B1%9F%E9%9B%85%E5%9B%AD11%E5%8F%B7%E6%A5%BC%7C%E6%9C%88%E6%A1%82%E8%A5%BF%E5%9B%AD; search_words14=%E8%B6%85%E6%98%8E%E5%9B%AD; search_words25=%E6%96%B0%E6%83%A0%E5%AE%B6%E5%9B%AD; browse_comm_ids13=95393; seo_source_type=0; search_words13=%E6%AC%A7%E9%99%86%E7%BB%8F%E5%85%B8%7C%E5%8D%97%E6%96%B9%E6%98%8E%E7%8F%A0%E8%8A%B1%E5%9B%AD%7C%E5%8D%97%E6%96%B9%E6%98%8E%E7%8F%A0%E8%8A%B1%E5%9B%AD%E4%BA%8C%E6%9C%9F1%E6%A0%8B; twe=2; __xsptplus8=8.43.1504789824.1504790391.8%233%7C123.sogou.com%7C%7C%7C%7C%23%23hvhL5eg3_ejnK-ngxJE-qwbIXXbQIk81%23%3B%20aQQ_a; _ga=GA1.2.1188068084.1502419352; _gid=GA1.2.1082371756.1504696715; lps="/cityList/|"; aQQ_ajkguid=B97BFB26-048C-2797-947E-7543B95A2D8A; ctid=13; 58tj_uuid=a4461385-7d0d-4e1a-9e94-85fa7b69f6aa; new_session=0; init_refer=; new_uv=61'
        }
        current = datetime.datetime.now()
        self.crawl_date = current.strftime('%Y-%m-%d')

    def start_requests(self):
        self.session = DBSession()
        #print self.city_name
        #print type(self.city_name)
        urls_info = self.session.query(House.id, House.url).join(Price).filter(Price.origin == 'AJK').filter(House.city_name==self.city_name).all()
        # 从数据库提取小区的url和id
        if not urls_info:
            print "city not found"
            return
        print len(urls_info)
        for url in urls_info:
            yield scrapy.Request(url=url[1] + 'rent/', headers=self.headers, callback=self.parse_rent,
                                 meta={'id': url[0]})

    # 小区租金抓取
    def parse_rent(self, response):
        house_id = response.meta['id']
        tree = etree.HTML(response.body, parser=etree.HTMLParser(encoding='utf-8'))
        # 判断是否有房子出租, 没有直接退出
        rent_not = tree.xpath('//p[@class="bu-tips bu-tips-warning bu-tips-middle"]')
        if rent_not:
            return

        # 有房子出租信息, 获取出租url
        a_node = tree.xpath('//div[@class="bu-list rentlist"]/a')
        for node in a_node:
            items = RentItem()

            url = node.xpath('.//@href')[0]
            title = node.xpath('.//div[@class="bu-item-inner"]/h4/text()')[0]
            house_type = node.xpath('.//p[@class="bu-item-row-cell"]/span/text()')[0]
            rent_type = node.xpath('.//p[@class="bu-item-row-cell"]/span/text()')[1]
            rent_price = node.xpath('.//p[@class="bu-item-row-cell bu-after"]/em/text()')[0]
            try:
                # 未知或者非数字的一律转为0
                rent_price = int(rent_price)
            except:
                rent_price = 0

            items['title'] = title
            items['url'] = url
            items['rent_price'] = rent_price
            items['rent_type'] = rent_type
            items['house_type'] = house_type
            items['h_id'] = house_id
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_other_info, meta={'items': items})

    def parse_other_info(self, response):
        items = response.meta['items']
        tree = etree.HTML(response.body, parser=etree.HTMLParser(encoding='utf-8'))
        nodes = tree.xpath('//ul[@class="clearfix view-info-detail"]/li')
        try:
            area = nodes[3].xpath('.//text()')[2]
        except:
            area = ''
        try:
            floor = nodes[4].xpath('.//text()')[1]
        except:
            floor = ''
        try:
            publish_time = nodes[8].xpath('.//text()')[2].encode('utf-8').strip()
            publish_time = datetime.datetime.strptime(publish_time, '%Y-%m-%d')
        except:
            publish_time = ''

        items['area'] = area
        items['floor'] = floor
        items['publish_time'] = publish_time
        items['crawl_date'] = self.crawl_date
        items['origin'] = self.origin
        yield items
