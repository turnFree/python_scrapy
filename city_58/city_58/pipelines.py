# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from pymongo import MongoClient
from traceback import format_exc
from .items import XiaoQuItem, ChuZuItem
from scrapy.exceptions import DropItem
from pymongo.errors import DuplicateKeyError


class City58Pipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGODB_URI'),
                   mongo_db=crawler.settings.get('MONGODB_DATABASE', 'items'))

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db['city58_info'].ensure_index('id', unique=True)
        self.db['city58_chuzu_info'].ensure_index('url', unique=True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            if isinstance(item, XiaoQuItem):
                self.db['city58_info'].update({'id': item['id']}, {'$set': item}, upsert=True)
            elif isinstance(item, ChuZuItem):
                try:
                    fangjia = HandleFangjiaPipline.price_per_squert_meter_dict[item['id']]
                    item['price_pre'] = fangjia
                    self.db['city58_chuzu_info'].update({'url': item['url']}, {'$set': item}, upsert=True)
                except Exception as e:
                    spider.logger.error(format_exc())
        except DuplicateKeyError:
            spider.logger.debug(DuplicateKeyError.details)
        except Exception as e:
            spider.logger.error(format_exc())
        return item


class HandleZuFangPipline(object):
    def process_item(self, item, spider):
        _ = spider
        if isinstance(item, ChuZuItem) and 'mianji' in item:
            item['chuzu_price_pre'] = int(item('zu_price'))/int(item['mianji'])
        return item


class HandleFangjiaPipline(object):
    price_per_squert_meter_dict = dict()

    def process_item(self, item, spider):
        _ = spider
        if isinstance(item, dict) and 'price_list' in item:
            item['price_list'] = [int(i) for i in item['price_list']]
            if item['price_list']:
                self.price_per_squert_meter_dict[item['id']] = sum(item['price_list'])/len(item['price_list'])
            else:
                self.price_per_squert_meter_dict[item['id']] = 0
            raise DropItem()
        return item


class AnjukePipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'scrapy', port=3306,
                                    charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(url_object_id, title, url, create_date, fav_nums)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["url_object_id"], item["title"], item["url"], item["create_date"], item["fav_nums"]))
        self.conn.commit()


