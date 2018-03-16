import codecs

from selenium import webdriver
import time

"""第一步打开浏览器，把所有节点点开，保存网页为文件"""
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('http://data.stats.gov.cn/easyquery.htm?cn=B01')
time.sleep(2)
but_close=driver.find_element_by_xpath("/html/body/div[2]/em")
if but_close:
        but_close.click()
        print("已关闭浏览器提醒===========")

start = 2
for i in range(1, 5):
    node_list = driver.find_elements_by_xpath('//li[@class="level%d"]' % i)
    if node_list:
        end = start + len(node_list)
        for j in range(start, end):
            """找到当前level元素,点击"""
            # print("treeZhiBiao_%d_span" % (j))
            driver.find_element_by_id("treeZhiBiao_%d_span" % (j)).click()
            time.sleep(2)
            """滑动，让子节点渲染"""
            # if j >= 5:
            #     js = "document.documentElement.scrollTop=10000"
            #     driver.execute_script(js)
            #     time.sleep(1)
        start = end

content = driver.page_source
with codecs.open('page_source.html','w+','utf-8') as f:
    f.write(content)