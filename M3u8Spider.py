import random
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class M3u8Spider:
    def __init__(self, url):
        self.url = url
        self.http = urllib3.PoolManager()
        self.userAgent = self.getUserAgent()
        self.headers = {
            'user-agent': self.userAgent
        }

    def getUserAgent(self):
        userAgentList = [
            'Mozilla/5.0 (Linux; Android 8.1; MI 8 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044306 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070336) NetType/WIFI Language/zh_CN Process/tools',
            'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; MI 8 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.1.8.998 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        ]
        return random.choice(userAgentList)

    def get_soup(self, urls):
        try:
            res = self.http.request('get', urls, headers=self.headers)
        except urllib3.exceptions.NewConnectionError:
            # 待剔除该代理ip
            exit()
        html_cate1 = res.data.decode('utf-8')
        soup = BeautifulSoup(html_cate1, 'lxml')
        return soup

    def get_category1(self):
        soup = self.get_soup(self.url)
        # 找出class属性值为news-list的div
        category1_list = soup.find_all('div', {'class': 'row-item'})
        return category1_list

    def get_category_name(self, category):
        return category.find('a').text

    def get_category2(self, category1):
        category2_list = category1.find_all('li', {'class': 'item'})
        return category2_list

    def get_items(self, category2):
        category2_url = self.url + category2.find('a').get('href')
        print(category2_url)

        soup = self.get_soup(category2_url)
        item_list = soup.find_all('a', {'class': 'video-pic loading'})
        return item_list

    def get_item_name(self, item):
        return item.get('title')

    def get_item_gif(self, item):
        return item.get('data-original')

    def get_m3u8(self, item):
        item_url = self.url + item.get('href')
        return self.parse_m3u8(item_url)

    def parse_m3u8(self, urls):
        CN2 = CN1 = CN3 = CN4 = 'm3u8.40cdn.com'
        soup = self.get_soup(urls)
        # m3u8_add = soup.find(id="video-player").find("source")['src']
        m3u8_add = soup.find_all('script', {'type': 'text/javascript'})[1].text.replace('\nvar vHLSurl = ', '')\
            .replace(';\n', '')
        return eval(m3u8_add)


if __name__ == '__main__':
    url = "https://21hukk.com"
    spider = M3u8Spider(url)
    userAgent = spider.getUserAgent()
    header = {
        'user-agent': userAgent
    }

    f = open('./4hu.csv', 'a', encoding='utf-8')
    cate1_list = spider.get_category1()
    for cate1 in cate1_list:
        cate1_name = spider.get_category_name(cate1)
        if cate1_name == '图片系列':
            break
        cate2_list = spider.get_category2(cate1)
        for cate2 in cate2_list:
            cate2_name = spider.get_category_name(cate2)
            if cate2_name == '最新地址':
                continue
            items = spider.get_items(cate2)
            for item in items:
                item_name = spider.get_item_name(item)
                item_gif = spider.get_item_gif(item)
                m3u8_add = spider.get_m3u8(item)
                f.writelines([cate1_name, ',', cate2_name, ',', item_name, ',', item_gif, ',',  m3u8_add, '\n'])
            f.flush()
    f.close()

    # class_list = spider.get_class(header)
