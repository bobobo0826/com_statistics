# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import time
from selenium import webdriver
from scrapy.http import HtmlResponse

class ComStatisticsSpiderMiddleware(object):
    def process_request(self,request,spider):
        driver = webdriver.Chrome()  # 也可换成Ie()，Firefox()等
        driver.maximize_window()
        driver.get('http://data.stats.gov.cn/easyquery.htm?cn=B01')
        time.sleep(5)
        len_list = 0
        len_re_list = 0
        if "clickJs" in request.meta:
            list = driver.find_elements_by_xpath('//li[@class="level1"]')
            len_list = len(list)
            # print("list============")
            # print(len(list))
            for i in range(2, len(list) + 2):
                # print("treeZhiBiao_%d_span" % (i))
                driver.find_element_by_id("treeZhiBiao_%d_span" % (i)).click()
                time.sleep(3)
                if i >= 5:
                    js = "document.documentElement.scrollTop=10000"
                    driver.execute_script(js)
                    time.sleep(3)
            re_list = driver.find_elements_by_class_name('level1')
            len_re_list = len(re_list)
            print("re_list=========")
            print(len(re_list))
            # for index in range(len(list) + 2, len(re_list) + 2):
            #     print("index=======", index)
            #     ID = "treeZhiBiao_%d_span" % (index)
            #     driver.find_element_by_xpath('//span[@id=ID]').click()
            #     time.sleep(3)
        time.sleep(5)  # 等待JS执行
        content = driver.page_source
        # print("content==================")
        # print(content)
        # driver.quit()
        return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)



