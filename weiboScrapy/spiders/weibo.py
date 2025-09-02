import json
import scrapy

from weiboScrapy.items import ArticleItem
from weiboScrapy.utils import get_format_date


class WeiboSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["weibo.com"]
    # 设置初始的 max_id 列表
    max_ids = list(range(11))  # 从 0 到 10

    def __init__(self, *args, **kwargs):
        super(WeiboSpider, self).__init__(*args, **kwargs)
        self.total_status_count = 0  # 初始化总状态数量

    # # 定义要添加的 Cookie
    # cookies = {
    #     'SUB': '_2AkMRj066f8NxqwFRmf0TzGrkbI5yzA_EieKn079hJRMxHRl-yT9yqnEOtRB6Og9gVYRlK8MjyNQS8SoFk1YpK2-AQy9y',
    #     'SUBP': '0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFgPmLBUsy6MwsMC5xnJgRR',
    #     'XSRF-TOKEN': 'izuNFQukjrNwDKLkHMPEzOzg',
    #     'WBPSESS': 'Av_uyMf5J_yRg2sn7ncLQTeiuJdSBhgltfM3mRx0MxWwamUSH7h4GvtzB0GGitRMjUKnTWeiDcCehmYUuP91JYDPKmR5nREclKR8dN5CqqPRIVVOrSM8MeotWgLhMj4ZKpRmWZp_c0ZUOq1_89nkTf6YXHjfXOTV1W07ZchOugw='
    # }

    def start_requests(self):
        # 从文件中读取 Cookie
        cookies = self.load_cookies('cookies.txt')

        # 循环生成请求
        for max_id in self.max_ids:
            url = f'https://weibo.com/ajax/feed/hottimeline?refresh=2&group_id=1028039999&containerid=102803_ctg1_9999_-_ctg1_9999_home&extparam=discover%7Cnew_feed&max_id={max_id}&count=10'
            yield scrapy.Request(url=url, callback=self.parse, cookies=cookies)

    def load_cookies(self, file_path):
        """从指定文件加载 Cookies"""
        cookies = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            # 读取整行并按分号分割
            cookie_line = f.read().strip()
            for cookie in cookie_line.split(';'):
                key, value = cookie.strip().split('=', 1)  # 分割键和值
                cookies[key] = value
        return cookies

    def parse(self, response):
        # 解析 JSON 数据
        data = json.loads(response.text)
        # 检查 'statuses' 是否存在
        if 'statuses' in data:
            statuses = data['statuses']

            for status in statuses:
                mid = status.get('mid')  # 获取 mid 值
                mblogid = status.get('mblogid')  # 获取 mid 值
                wtext = status.get('text')  # text
                text_raw = status.get('text_raw')  # text_raw
                created_at = get_format_date(status.get('created_at'))  # create_at 格式化后的日期

                # if mid:  # 如果 mid 不为空
                #     self.log(mid)  # 打印 mid 值
                screen_name = status.get('user').get('screen_name')
                user_id = status.get('user').get('idstr')

                topic_struct = status.get('topic_struct')
                try:
                    topic_title = topic_struct[0].get('topic_title')
                except:
                    topic_title = ''

                source = status.get('source')
                region_name = status.get('region_name')

                reposts_count = status.get('reposts_count')
                comments_count = status.get('comments_count')
                attitudes_count = status.get('attitudes_count')

                # 创建 Item 对象
                item = ArticleItem()
                item['mid'] = mid
                item['mblogid'] = mblogid
                item['wtext'] = wtext
                item['text_raw'] = text_raw
                item['created_at'] = created_at
                item['topic_title'] = topic_title
                item['source'] = source
                item['region_name'] = region_name
                item['reposts_count'] = reposts_count
                item['comments_count'] = comments_count
                item['attitudes_count'] = attitudes_count

                item['user_id'] = user_id
                item['screen_name'] = screen_name

                # 使用 yield 返回 Item
                yield item

            status_count = len(statuses)  # 当前请求中的状态数量
            self.total_status_count += status_count  # 累加总状态数量
            self.log(f'总共爬取: {self.total_status_count}')  # 记录当前请求的状态数量

        else:
            self.log("No statuses found in the response.")

