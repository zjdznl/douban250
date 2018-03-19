# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import  DropItem


class ScrapyspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class DoubanTop250imgPipeline(ImagesPipeline):
    headers = {
        'accept': 'image/webp,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'cookie': 'bid=yQdC/AzTaCw',
        'referer': 'https://www.douban.com/photos/photo/2370443040/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            self.headers['referer'] = image_url
            yield Request(image_url, headers=self.headers)

    def item_completed(self, results, item, info):
        image_path = [i['path'] for ok, i in results if ok]
        if not image_path:
            raise DropItem("Items contains no images")

        item['image_path'] = image_path
        return item


