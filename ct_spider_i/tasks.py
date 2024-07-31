from celery import app
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


@app.task
def run_newsghana_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl("newsghana1")
    process.start()


@app.task
def run_primenews_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl("primenews")
    process.start()
