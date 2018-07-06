# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.loader import ItemLoader
# from pyquery import PyQuery
from city_58.items import City58Item


class SpiderCity58Spider(scrapy.Spider):
    name = 'spider_city_58'
    allowed_domains = ['58.com']
    start_urls = ['http://yuncheng.58.com/zufang/27317372796230x.shtml']

    def parse(self, response):
        # jpy = PyQuery(response.text)
        print(response.text)
        item_loader = ItemLoader(item=City58Item(), response=response)
        item_loader.add_xpath('price', '//div[contains(@class, "house-pay-way")]/span[1]/b/text()')
        item_loader.add_xpath('pay_way', '//div[contains(@class, "house-pay-way")]/span[2]/text()')
        item_loader.add_xpath('house_type', '//div[contains(@class,"house-desc-item")]/ul/li[2]/span[2]/text()')
        return item_loader.load_item()


