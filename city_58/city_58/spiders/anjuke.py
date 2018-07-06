# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.loader import ItemLoader
from city_58.items import AnjukeItem


class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://ty.fang.anjuke.com/loupan/xinghualing/']

    def parse(self, response):
        item_loader = ItemLoader(item=AnjukeItem(), response=response)
        item_loader.add_xpath('price', '//p[@class = "price"]/span/text()')
        return item_loader.load_item()

