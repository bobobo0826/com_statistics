import codecs
from scrapy import Selector
"""第二步打开文件，解析出所有节点code"""
order_list = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H",
              "I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

zhibiao_list = []
code_list = []

def parse(content,level,parent_code):
    selector = Selector(text=content)
    node_list = selector.xpath('//li[@class="level%d"]'%level).extract()
    # print("node_list==================")
    # print(node_list)
    for index, node_content in enumerate(node_list, 1):
        # print(level)
        zhibiao_dict = {}
        selector1 = Selector(text=node_content)
        # print(node_content)
        node_name = selector1.xpath('//a[@class = "level%d"]/span[2]/text()'%level).extract_first()
        zhibiao_dict["zhibiao"] = node_name

        code = "%s%s%s"%(parent_code,order_list[int(index/36)],order_list[int(index%36)])
        # print("code===================",code)
        zhibiao_dict["code"] = code
        next_level = level + 1
        child_node = selector1.xpath('//li[@class = "level%d"]'%next_level).extract()
        # print("child_node===========",child_node)
        if child_node:
            zhibiao_dict["has_child"] = True
            parse(node_content, level=next_level, parent_code=code)
        else:
            zhibiao_dict["has_child"] = False

        zhibiao_list.append(zhibiao_dict)
def code(list):
    for index, content in enumerate(list):
        # print("code========list[index]=================")
        # print(list[index])
        if list[index]["has_child"] == False:
            code = list[index]["code"]
            code_list.append(code)

with codecs.open('D:\scrapy_test\statistics\com_statistics\com_statistics\page_source.html', 'r', 'utf-8') as f:
    content = f.read()
    parse(content,level=1,parent_code="A")
    # print(len(zhibiao_list))
    # print(zhibiao_list)
    code(zhibiao_list)
    print(code_list)