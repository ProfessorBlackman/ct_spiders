from typing import Iterable, Any

import scrapy
from scrapy import Request
from scrapy.http import Response
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class HoboSpider(CrawlSpider):
    name = "hobo"
    allowed_domains = ["https://jiji.com.gh"]
    start_urls = [
        "https://jiji.com.gh/cars",
        "https://jiji.com.gh/buses",
        "https://jiji.com.gh/heavy-equipments-machinery",
        "https://jiji.com.gh/motorcycles-and-scooters",
        "https://jiji.com.gh/watercrafts-vehicle"
    ]

    def parse_item(self, response: Response) -> Iterable[dict[str, Any]]:

        yield {
            "url": response.url
        }