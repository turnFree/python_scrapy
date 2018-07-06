# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from scrapy.http import Request
from urllib import parse
import re
from city_58.items import JobBoleArticleItem
from city_58.utils.common import get_md5


class JobbleSpider(scrapy.Spider):
    name = 'jobble'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1、获取文章列表页的文章url，并交给scrapy后进行解析
        2、获取下一页的url，并交给scrapy进行下载，下载完成后交给parse
        """
        post_nodes = response.css('#archive .post.floated-thumb .post-thumb a')
        for post_node in post_nodes:
            img_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": img_url},
                          callback=self.parse_detail)

        next_url = response.css('.next.page-numbers::attr(href)').extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()
        front_image_url = response.meta.get("front_image_url", "")
        title = response.css("span[data-rel='title']::text").extract_first("")
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract_first("").strip().\
            replace("·", "").strip()
        praise_nums = response.css("span.vote-post-up h10::text").extract_first("")
        fav_nums = response.css(".bookmark-btn::text").extract_first("")
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        else:
            fav_nums = 0

        comments_nums = response.css("a[href='#article-comment'] span::text").extract_first("")
        match_re = re.match(".*?(\d+).*", comments_nums)
        if match_re:
            comments_nums = match_re.group(1)
        else:
            comments_nums = 0

        content = response.css("div.entry").extract_first("")

        article_item["url_object_id"] = get_md5(response.url)
        article_item["title"] = title
        article_item["url"] = response.url
        try:
            create_date = datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.now().date()

        article_item["create_date"] = create_date
        article_item["front_image_url"] = front_image_url
        article_item["praise_nums"] = praise_nums
        article_item["comment_nums"] = comments_nums
        article_item["fav_nums"] = fav_nums
        article_item["content"] = content

        yield article_item


