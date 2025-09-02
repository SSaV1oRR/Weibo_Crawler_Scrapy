from scrapy import cmdline

# 爬取Hotline (实时热点)
# cmdline.execute("scrapy crawl weibo".split())

# 爬取话题文章
cmdline.execute("scrapy crawl weibo_search".split())

# 爬取评论
# cmdline.execute("scrapy crawl weibo_comment".split())


