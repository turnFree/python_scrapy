# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class City58Item(scrapy.Item):
    # define the fields for your item here like:
    price = scrapy.Field()
    pay_way = scrapy.Field()
    house_type = scrapy.Field()


class AnjukeItem(scrapy.Item):
    # define the fields for your item here like:
    price = scrapy.Field()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()


class XiaoQuItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    reference_price = scrapy.Field()
    address = scrapy.Field()
    times = scrapy.Field()


class ChuZuItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    zu_price = scrapy.Field()
    type = scrapy.Field()
    mianji = scrapy.Field()
    chuzu_price_pre = scrapy.Field()
    url = scrapy.Field()
    price_pre = scrapy.Field()









