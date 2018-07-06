# -*- coding: utf-8 -*-
""" 
@author: Andy 
@software: PyCharm 
@file: pyq_test.py 
@time: 2018/7/1 7:49 
"""
from pyquery import PyQuery as pq

html = '''<div class=‘content’>
    <ul id = 'haha'>
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul></div>'''

doc = pq(html)
item = doc('div ul')
print(item.find('a').items())
# 注意这里查找ul标签的所有子标签，也就是li标签，下面是查找含有class属性的标签，如果你把class换成href肯定不行，它指的只是儿子并不是子子孙孙
# print(item.children('[class]'))
