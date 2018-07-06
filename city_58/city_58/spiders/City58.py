# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from pyquery import PyQuery
import re
from traceback import format_exc
from ..utils.parse import xiaoqu_detail_parse, \
    get_ershou_list_price,\
    chuzu_list_get_detail_url,\
    get_chuzu_house_info
from ..items import XiaoQuItem, ChuZuItem


class City58Spider(scrapy.Spider):
    name = 'city_58'
    allowed_domains = ['58.com']
    start_urls = ['http://sh.58.com/xiaoqu/']
    host = 'sh.58.com'

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        # 解析上海各分区的id
        pyq = PyQuery(response.text)
        quyu_list = pyq('#filter_quyu > dd > a').items()
        re_get_id = re.compile(r'\d+')
        for quyu in quyu_list:
            search = re_get_id.search(quyu.attr('listname'))
            if search:
                yield Request('http://{}/xiaoqu/{}/'.format(self.host, search.group(0)),
                              callback=self.xiaoqu_parse,
                              priority=5)

    def xiaoqu_parse(self, response):
        # 抓取小区列表页所有小区url
        jpy = PyQuery(response.text)
        xiaoqu_list = jpy('#infolist > div.listwrap > table > tbody > tr').items()
        for xiaoqu in xiaoqu_list:
            url = xiaoqu('td > a').attr('href')
            yield Request(url=url,
                          callback=self.xiaoqu_detail_parse,
                          errback=self.err_back,
                          priority=4)

    def xiaoqu_detail_parse(self, response):
        # 抓取小区详情页信息
        data = xiaoqu_detail_parse(response)
        item = XiaoQuItem()
        item.update(data)
        item['id'] = response.url.split('/')[4]
        yield item

        # 二手房
        url = "http://{}/xiaoqu/{}/ershoufang/".format(self.host, item['id'])
        yield Request(url=url,
                      callback=self.ershoufang_parse,
                      errback=self.err_back,
                      meta={'id': item['id']},
                      priority=3)

        # 出租房
        url = "http://{}/xiaoqu/{}/chuzu/".format(self.host, item['id'])
        yield Request(url=url,
                      callback=self.chuzu_parse,
                      errback=self.err_back,
                      meta={'id': item['id']},
                      priority=2)

    def ershoufang_parse(self, response):
        price_list = get_ershou_list_price(response)
        yield {'id': response.meta['id'], 'price_list': price_list}

    def chuzu_parse(self, response):
        url_list = chuzu_list_get_detail_url(response)
        for url in url_list:
            yield response.request.replace(url=url,
                                           callback=self.chuzu_detail_parse,
                                           errback=self.err_back,
                                           priority=1)

    def chuzu_detail_parse(self, response):
        data = get_chuzu_house_info(response)
        item = ChuZuItem()
        item.update(data)
        item['id'] = response.meta['id']
        item['url'] = response.url
        yield item

    def err_back(self, e):
        _ = e
        self.logger.error(format_exc())

