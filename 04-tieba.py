# 使用爬虫爬取百度贴吧a标签的title和对应的href
# xpath语法：
# 提取下一页的链接： //*[@id="frs_list_pager"]/a[contains(text(), '下一页')]
# 提取所有帖子的a标签：//*[@id="thread_list"]/li[contains(@class, "j_thread_list")]/div/div[2]/div[1]/div/a

import requests
from lxml import etree

class Tieba(object):
    def __init__(self, name):
        self.name = name
        self.url = 'http://tieba.baidu.com/f?kw={}'.format(self.name)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
    
    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def parse_list_page(self, data):
        # 处理data
        data = data.decode().replace("<!--", "").replace("-->", "")
        html = etree.HTML(data)

        # 选取所有帖子的a标签，列表
        el_list = html.xpath('//*[@id="thread_list"]/li[contains(@class, "j_thread_list")]/div/div[2]/div[1]/div/a')
        data_list = []
        for el in el_list:
            # 构造字典
            temp = {}
            temp['title'] = el.xpath('./text()')[0]
            temp['link'] = 'http://tieba.baidu.com' + el.xpath('./@href')[0]
            data_list.append(temp)
        
        next_url_element = html.xpath('//*[@id="frs_list_pager"]/a[contains(text(), "下一页")]')
        if next_url_element:
            next_url = 'http:' + next_url_element[0].xpath('@href')[0]
        else:
            next_url = None
            
        return data_list, next_url
    
    def run(self):
        next_url = self.url
        while True:
            # 发送请求，获取响应
            list_page_data = self.get_data(next_url)
            # 元祖的形式 获取数据，和下一页的链接
            data_list, next_url = self.parse_list_page(list_page_data)
            
            # 遍历帖子列表，打印标题和链接
            for data in data_list:
                print(f"Title: {data['title']}")
                print(f"Link: {data['link']}")
                print('')
            
            if not next_url:
                break

if __name__ == '__main__':
    tieba = Tieba("孙笑川")
    tieba.run()
