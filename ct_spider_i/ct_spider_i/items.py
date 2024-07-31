from dataclasses import dataclass

import scrapy


@dataclass
class CtSpiderIItem(scrapy.Item):
    # define the fields for your item here like:
    image_links: list
    post_links: list
    image_source_alt: list
    post_headlines: list
    append_source: bool
    source: str
