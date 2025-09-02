# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os

import pymysql
# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings

from weiboScrapy.bert import Config, Model, load_dataset, final_predict, build_iterator
from weiboScrapy.items import ArticleItem, WeiboItem


# MySQL 处理管道
class MySQLPipeline:
    def open_spider(self, spider):
        # 获取数据库配置
        settings = get_project_settings()
        self.connection = pymysql.connect(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            database=settings['MYSQL_DATABASE'],
            charset='utf8',
            use_unicode=True,
        )
        self.cursor = self.connection.cursor()
        self.connection.commit()

    def close_spider(self, spider):
        # 关闭数据库连接
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        print('MySQL 管道...')
        if 'weibo' in item:
            data = dict(item['weibo'])
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql = """INSERT INTO {table}({keys}) VALUES ({values}) ON
                                 DUPLICATE KEY UPDATE""".format(table='tb_weibo',
                                                                keys=keys,
                                                                values=values)
            update = ','.join([" {key} = {key}".format(key=key) for key in data])
            sql += update

            CYAN = '\033[96m'  # 青色
            RED = '\033[91m'  # 红色
            RESET = '\033[0m'  # 重置为默认颜色

            try:
                self.cursor.execute(sql, tuple(data.values()))
                self.connection.commit()
                print(f"{CYAN}插入数据库成功{RESET}")
            except Exception as E:
                print('**********'+sql)
                print("Error:", E)
                print(f"{RED}插入数据库失败{RESET}")
                self.connection.rollback()

        if isinstance(item, ArticleItem):
            # 插入数据到 MySQL
            sql = """
               INSERT INTO tb_weibo_article (
                   mid, 
                   mblogid, 
                   wtext, 
                   text_raw, 
                   created_at, 
                   region_name, 
                   source, 
                   reposts_count, 
                   comments_count, 
                   attitudes_count, 
                   topic_title, 
                   user_id, 
                   screen_name
               ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           """

            # 确保所有字段都有值，可以根据需要提供默认值或处理缺失值
            values = (
                item.get('mid'), item.get('mblogid'),
                item.get('wtext'), item.get('text_raw'),
                item.get('created_at'), item.get('region_name'),
                item.get('source'),
                item.get('reposts_count', 0),  # 默认值为0
                item.get('comments_count', 0),  # 默认值为0
                item.get('attitudes_count', 0),  # 默认值为0
                item.get('topic_title'), item.get('user_id'), item.get('screen_name')
                )
            self.cursor.execute(sql, values)
            self.connection.commit()  # 提交事务

        return item  # 必须返回 item

# 处理重复信息管道
class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()
        self.file_path = 'seen_ids.json'
        self._load_seen_ids()

    def _load_seen_ids(self):
        """从文件加载已经记录的ID"""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                self.ids_seen = set(json.load(file))

    def _save_seen_ids(self):
        """将记录的ID保存到文件"""
        with open(self.file_path, 'w') as file:
            json.dump(list(self.ids_seen), file)

    def process_item(self, item, spider):
        if 'weibo' in item:
            if item['weibo']['mid'] in self.ids_seen:
                raise DropItem("过滤重复微博: %s" % item)
            else:
                self.ids_seen.add(item['weibo']['mid'])
                self._save_seen_ids()  # 每次添加新ID时保存
                return item

# 处理情感分析的管道
class SentimentPipeline(object):
    def __init__(self):
        self.config = Config()
        self.model = Model(self.config).to(self.config.device)

    def process_item(self, item, spider):
        if 'weibo' in item:
            GOLD = "\033[38;5;214m"  # 使用色号214表示金色
            RESET = "\033[0m"  # 重置颜色
            text = [item['weibo']['text']]
            test_data = load_dataset(text, self.config)
            test_iter = build_iterator(test_data, self.config)
            result = final_predict(self.config, self.model, test_iter)
            for i, j in enumerate(result):
                # print('text:{}'.format(text[i]))
                # print('label:{}'.format(j))
                item['weibo']['label'] = j
                print(f"{GOLD}情感分析微博内容:{item['weibo']['text']},结果:{j}{RESET}")
        return item
