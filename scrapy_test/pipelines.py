# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymongo
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

class ScrapyTestPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient("192.168.222.100", 27017)
        db = connection["wechat"] # you need no build database named testdouban
        # db.authenticate(name = "root", password = "fireling") # no name and password for localhost
        self.posts = db["sina"] # you need not build collection named book

    # pipeline default function
    def process_item(self, item, spider):
        self.posts.insert(dict(item))  # convert json to dict
        return item

class ScrapyTestImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok] #ok判断是否下载成功
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
