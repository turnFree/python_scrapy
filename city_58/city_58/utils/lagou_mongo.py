# -*- coding: utf-8 -*-
""" 
@author: Andy 
@software: PyCharm 
@file: lagou_mongo.py 
@time: 2018/6/28 9:22 
"""

from pymongo import MongoClient
import requests
from fake_useragent import UserAgent
import time


client = MongoClient()
db = client.lagou  # 创建一个lagou数据库
my_set = db.job  # 创建job集合

headers = {
    'Cookie': 'JSESSIONID=ABAAABAAAGFABEFEAF7DE6B46505A65A1A0D578B4B257AF; _ga=GA1.2.2072305624.1530247282;'
              ' _gid=GA1.2.1823526530.1530247282; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530247282;'
              ' user_trace_token=20180629123950-756c8972-7b56-11e8-9775-5254005c3644; LGSID=20180629123950-75'
              '6c8ba1-7b56-11e8-9775-5254005c3644; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fww'
              'w.baidu.com%2Flink%3Furl%3Dmz33IcGjyi1GQZKKBLTyDhmak7xp_gw2Sya-v1vQ8h7%26wd%3D%26eqid%3Dce407096'
              '000022a0000000035b35b80f; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGUID=20180629123950-756c8d55'
              '-7b56-11e8-9775-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_search'
              '; LGRID=20180629123957-7989fecc-7b56-11e8-b365-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf'
              '756e6=1530247290; SEARCH_ID=7047a575d8384e16a77487b80558e275',
    'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=',
}  # 填入对应的headers信息


def crawl_one_page(page_num):
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
    payload = {
        'first': 'true',
        'pn': page_num,
        'kd': '爬虫',
    }
    ua = UserAgent()
    headers['User-Agent'] = ua.random
    response = requests.post(url, data=payload, headers=headers)  # 使用POST方法请求数据，加上payload和headers信息
    if response.status_code == 200:
        my_set.insert(response.json()['content']['positionResult']['result'])  # 把对应的数据保存到MOngoDB
    else:
        print('Something Wrong!')
    print('正在爬去第' + str(page_num) + '页的数据')
    time.sleep(3)


if __name__ == '__main__':
    for i in range(5):
        crawl_one_page(i+1)
