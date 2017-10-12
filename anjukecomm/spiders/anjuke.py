# coding: utf-8
import codecs
import json
import re, time, os
import datetime
from lxml import etree
import requests
import scrapy
from anjukecomm.items import AnjukecommItem, RentItem


# 移动端
class AnjukeSpiderMobile(scrapy.Spider):
    name = 'anjuke_m'
    allowed_domains = ['m.anjuke.com']

    def __init__(self, city=None, *args, **kwargs):
        super(AnjukeSpiderMobile, self).__init__(*args, **kwargs)
        self.city = city
        fp = codecs.open('anjuke_city', 'r').read()
        js = json.loads(fp)
        self.city_name = js[self.city]
        self.origin = 'AJK'
        current = datetime.datetime.now()
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
        self.headers['referer'] = 'https://m.anjuke.com/%s/community/?from=anjuke_home' % self.city
        self.headers['Origin'] = 'http://m.%s.lianjia.com' % self.city
        self.crawl_date = current.strftime('%Y-%m-%d')
        # self.price_month = current.strftime('%Y-%m')
        # self.price_month = (current + datetime.timedelta(days=-31)).strftime('%Y-%m')

    def start_requests(self):

        for i in range(1, 150):
            start_url = 'https://m.anjuke.com/%s/community/?from=anjuke_home&p=%d' % (self.city, i)
            r = requests.get(url=start_url, headers=self.headers)
            try:
                if r.json()['data']:
                    yield scrapy.Request(url=start_url, headers=self.headers)
                else:
                    break
            except:
                break

    # 得到小区的url
    def parse(self, response):

        try:
            js = json.loads(response.body)
            body = js['data']
        except Exception, e:
            return
        for element in body:
            new_header = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.8',
                'cache-control': 'no-cache',
                'cookie': 'als=0; isp=true; Hm_lvt_c5899c8768ebee272710c9c5f365a6d8=1502789242; __xsptplus8=8.48.1503983029.1503983038.2%232%7Cbzclk.baidu.com%7C%7C%7C%25E5%25AE%2589%25E5%25B1%2585%25E5%25AE%25A2%7C%23%23ePB-pvQkSL2NJUApeF2t0wzwiguOpeeh%23; _ga=GA1.2.198967165.1502172457; lps="/qian/community/874335/|"; sessid=8E792345-4689-3170-7BC5-F8394AE63761; seo_source_type=0; Ref=https%3A%2F%2Fm.anjuke.com%2Fqian%2Fmap%2F%3Fadr%3D%25E4%25B8%259C%25E8%258D%2586%25E5%25A4%25A7%25E9%2581%2593%252C%25E8%25BF%2591%25E9%25A9%25AC%25E6%2598%258C%25E5%259E%25B8%25E8%25B7%25AF%26lng%3D112.88674912697%26lat%3D30.4314923944%26tp%3Dcomm%26id%3D874335%26from%3Dcommunity_jjzs; ctid=350; aQQ_ajkguid=6C8321F4-620F-0E6B-9572-5756933A00B5; 58tj_uuid=9ab24c8b-fd0d-4090-805e-d25b0b63b601; new_session=0; init_refer=; new_uv=48',
                'pragma': 'no-cache',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
            # 小区信息
            yield scrapy.Request(url=element['url'], headers=new_header, callback=self.parse_lng_lat)

    def parse_lng_lat(self, response):
        items = AnjukecommItem()
        tree = etree.HTML(response.body, parser=etree.HTMLParser(encoding='utf-8'))
        try:
            price = tree.xpath('//a[@data-soj="community_topprice"]/div[@class="txt-c"]/p[@class="price"]/text()')[0]
            price = int(price)
            # 低于1000的为无效
            if price < 1000 and price > 0:
                price = 0
        except:
            price = 0
        try:
            months = tree.xpath('//a[@data-soj="community_topprice"]/div[@class="txt-c"]/p[@class="desc-text"]/text()')[0].encode('utf-8')
            # 返回类似 于 9月均价（元/m²）
            months = re.findall('(\d+)月均价', months)[0]
            months_price = '2017-' + months
        except:
            months_price = ''
        content = response.body
        pattern = 'data-center="(.*?)"'

        data = re.findall(pattern, content)
        bd_map = data[0].split(',')
        longitude = bd_map[0]
        latitude = bd_map[1]
        items['longitude'] = longitude
        items['latitude'] = latitude

        name = tree.xpath('//div[@class="comm-tit"]/h1/text()')[0]

        try:
            address = tree.xpath('//div[@class="comm-tit"]/div[@class="comm-ad"]/p/text()')[0]
            address = re.sub(u'地址：', '', address)
            district = address.split('-')[0]
        except:
            address = ''
            district = ''
        try:
            building_type = tree.xpath('//div[@class="header-field"]/span')[0].xpath('./text()')[0]
            if building_type.encode('utf-8') == u'暂无数据':
                building_type=''
        except:
            building_type = ''

        try:
            building_date = tree.xpath('//div[@class="header-field"]/span')[2].xpath('./text()')[0]
            if building_date.encode('utf-8') == u'暂无数据':
                building_date=''
        except:
            building_date = ''

        try:
            developers = tree.xpath('//dl[@class="comm-other-field"]/dd/text()')[0]
            if developers.encode('utf-8') == u'暂无数据':
                developers=''
        except:
            developers = ''
        try:
            property_corp = tree.xpath('//dl[@class="comm-other-field"]/dd/text()')[1]
            if property_corp.encode('utf-8') == u'暂无数据':
                property_corp=''
        except:
            property_corp = ''

        items['name'] = name
        items['price'] = price
        items['url'] = response.url
        items['building_date'] = building_date
        items['location'] = address
        items['building_type'] = building_type
        items['city_name'] = self.city_name
        items['district'] = district
        items['developers'] = developers
        items['property_corp'] = property_corp
        items['months'] = months_price
        items['crawl_date'] = self.crawl_date
        items['origin'] = self.origin
        yield items
