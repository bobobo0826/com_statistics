import scrapy
import time
from urllib.parse import quote
import os
import json
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from com_statistics.acquire_code import code_list
from com_statistics.items import ComStatisticsItem
class Spider(scrapy.Spider):
    name = "com_statistics"
    allowed_domains = ["data.stats.gov.cn"]
    def start_requests(self):
        code=code_list
        print("code_list==============================")
        print(code_list)
        period=["1949-"]
        start_url = "http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgjd&rowcode=zb&colcode=sj"
        for item in enumerate(code):
            for index in enumerate(period):
                # print("******************************************")
                # print(item[1])
                # print(index[1])
                dfwds = [{"wdcode": "zb", "valuecode": item[1]}, {"wdcode": "sj", "valuecode": index[1]}]
                k1 = int(round(time.time() * 1000))
                backurl = "&wds=[]&dfwds=" + str(dfwds) + "&k1=" + str(k1)
                url = start_url + backurl.replace("[", quote("[")).replace("]", quote("]")).replace("{", quote("{")).replace("}", quote("}")).replace(":", quote(":")).replace("'", quote('"')).replace(" ", "")
                request = Request(url=url, callback=self.parse)
                yield request

    def parse(self, response):
        # print("444444444444444444444444444")
        # print(response.body)
        # selector = Selector(response)
        json_data = json.loads(response.body.decode("utf-8"))
        return_code = json_data.get("returncode")

        """如果获取数据成功，解析获取的数据"""

        if return_code == 200:
            return_data = json_data.get("returndata")
            data_list = return_data.get("datanodes")
            item_list = return_data.get("wdnodes")[0].get("nodes")
            year_len = len(return_data.get("wdnodes")[1].get("nodes"))

            res_data = {}
            for i in range(len(item_list)):
                res_data_list = []
                for j in range(year_len):
                    res_data_list_item = {}
                    data = data_list[i * year_len + j]
                    has_data = bool(data.get("data").get("hasdata"))
                    if has_data is True:
                        res_data_list_item["name"] = item_list[i].get("cname")
                        res_data_list_item["year"] = data.get("code").split(".")[-1]
                        res_data_list_item["data"] = data.get("data").get("data")
                    if res_data_list_item:
                        res_data_list.append(res_data_list_item)
                if res_data_list:
                    # item = ComStatisticsItem()
                    # item["code"] = item_list[i].get("code")
                    # item["table_list"] = res_data_list
                    # print("888888888888888888888888888")
                    # print(item)
                    # yield item
                    # print("888888888888888888888888888")
                    # print(res_data_list)
                    code = item_list[i].get("code")
                    res_data[code] = res_data_list
                    # print(res_data[code])
            # print(res_data)
            for key,value in res_data.items():
                # print("888888888888888888888888888")
                # print(key)
                # print(value)
                item = ComStatisticsItem()
                item["code"] = key
                item["table_list"] = value
                yield item




