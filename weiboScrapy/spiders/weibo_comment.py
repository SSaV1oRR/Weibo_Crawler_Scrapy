import scrapy
import json

from weiboScrapy.utils import load_cookies, get_format_date


class WeiboCommentsSpider(scrapy.Spider):
    name = 'weibo_comment'
    allowed_domains = ['weibo.com']
    start_urls = ['https://weibo.com/ajax/statuses/buildComments']

    def start_requests(self):
        # 从文件中读取 Cookie
        cookies = load_cookies('cookies.txt')
        # 这里可以根据需要自定义请求参数
        for post_id in ['5079329078513140']:  # 这里填入要爬取的微博的 post_id
            url = f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={post_id}&is_show_bulletin=3&is_mix=0&count=10&uid=5525643726&fetch_level=0&locale=zh-CN'
            yield scrapy.Request(url=url, callback=self.parse_comments,
                                 meta={'post_id': post_id,'cookies':cookies },  cookies=cookies)

    def parse_comments(self, response):
        # 获取 post_id
        post_id = response.meta['post_id']

        # 解析 JSON 数据
        data = json.loads(response.text)

        # 检查数据结构并提取评论
        if 'data' in data :
            comments = data['data']
            for comment in comments:
                # 打印每条评论的数据
                screen_name = comment.get('user', {}).get('screen_name')
                user_id = comment.get('user', {}).get('idstr')
                text = comment.get('text')
                created_at = get_format_date(comment.get('created_at'))
                like_counts = comment.get('like_counts')
                source = comment.get('source')

                # 打印到控制台
                print(f'screen_name: {screen_name}')
                print(f'user_id: {user_id}')
                print(f'text: {text}')
                print(f'Created At: {created_at}')
                print(f'likes_count: {like_counts}')
                print(f'source: {source}')
                print('-' * 50)  # 分隔线

                # 如果需要，也可以将数据 yield 给其他处理
                yield {
                    'user': screen_name,
                    'text': text,
                    'created_at': created_at,
                    'like_counts': like_counts,
                    'source': source,
                }

        # 处理翻页逻辑（如果需要）
        if data['max_id']:
            print(f"下一页 max_id = {data['max_id']}")
            next_max_id = data['max_id']
            cookies = response.meta['cookies']
            url = f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={post_id}&max_id={next_max_id}&is_show_bulletin=3&is_mix=0&count=10&uid=5525643726&fetch_level=0&locale=zh-CN'
            # url = f'https://weibo.com/ajax/statuses/buildComments?mid={post_id}&max_id={next_max_id}&count=20'
            yield scrapy.Request(url=url, callback=self.parse_comments, meta={'post_id': post_id, 'cookies': cookies}, cookies=cookies)
