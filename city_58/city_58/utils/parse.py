# -*- coding: utf-8 -*-
""" 
@author: Andy 
@software: PyCharm 
@file: parse.py 
@time: 2018/7/1 16:42 
"""
from pyquery import PyQuery


def xiaoqu_detail_parse(response):
    """
    小区详情页样例url:http://sh.58.com/xiaoqu/shimaobinjianghuayuan/
    返回这个小区详细信息的dict字典，内容包括小区名称、小区参考房价、小区地址、建筑年代
    :param response:
    :return: result
    """
    pyq = PyQuery(response.text)
    result = dict()
    result['name'] = pyq('body > div.body-wrapper > div.title-bar > span.title').text()
    result['reference_price'] = \
        pyq('body > div.body-wrapper > div.basic-container > div.info-container > div.price-container > span.price')\
        .text()
    result['address'] = pyq('table > tr:nth-child(1) > td:nth-child(4)').text()
    result['times'] = pyq('body > div.body-wrapper > div.basic-container > div.info-container > '
                          'div.info-tb-container > table > tr:nth-child(5) > td:nth-child(2)').text().strip()
    return result

def get_ershou_list_price(response):
    """
    获取二手房列表页价格
    :param response:
    :return:
    """
    pyq = PyQuery(response.text)
    price_tag = pyq('td.tc > span:nth-child(3)').text().split()
    price_tag = [i[:-3] for i in price_tag]
    return price_tag

def chuzu_list_get_detail_url(response):
    """
    回去出租房详情页url
    :param response:
    :return: list
    """
    pyq = PyQuery(response.text)
    a_list = pyq('tr > td.t > a.t').items()
    url_list = [i.attr('href') for i in a_list]
    return url_list

def get_chuzu_house_info(response):
    pyq = PyQuery(response.text)
    result = dict()
    result['name'] = pyq('body > div.main-wrap > div.house-title > h1').text()
    result['zu_price'] = pyq('div.house-desc-item > div > span > b').text()
    result['type'] = pyq('div.house-desc-item > ul > li:nth-child(2) > span:nth-child(2)').text()
    print(len(result['type'].split()))
    result['type'], result['mianji'], *_ = result['type'].split()
    return result



