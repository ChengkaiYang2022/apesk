from scrapy.cmdline import execute
# 运行配置：在pycharm中运行参数配置 crawl bdxy -o bdxy.json
if __name__ == "__main__":
    execute("scrapy crawl mensa".split())
