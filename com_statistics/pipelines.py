# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from com_statistics.items import ComStatisticsItem
import pymongo
class ComStatisticsPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient("localhost",27017)
        db = client["ComStatistics"]
        self.Collection = db["JD"]

    def process_item(self, item, spider):
        try :
            self.Collection.insert(dict(item))
        except Exception:
            pass
        return item
