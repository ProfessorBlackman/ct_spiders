import re

import scrapy
import asyncio

import scrapy


# custom settings for this scraper


#  A spider to scrape PrimeNewsGhana.com
class PrimenewsSpider(scrapy.Spider):
    name = "primenews"
    source = 'https://www.primenewsghana.com'
    number_of_pages: int = 3320
    start = 1
    append_source = False

    # This list contains the links for each of the genres in ImDb
    url1 = [
        "https://www.primenewsghana.com/sports.html?mdrv=www.primenewsghana.com&start=",
    ]

    # This function iterates through the above list and forms
    # a new url using url1, start variable, and url2 which is
    # then passed to the parse function for the actual scraping

    def start_requests(self):
        self.number_of_pages += 1
        print(self.number_of_pages)
        for url in self.url1:
            for page_number in range(1, self.number_of_pages):
                yield scrapy.Request(url=f'{url}{self.start}')

                if page_number >= 2:
                    self.start += 30
                else:
                    self.start = 1

    def parse(self, response, **kwargs):

        image_links: list = response.css(
            'body > div.bd-containereffect-11.container-effect.container > div > div > div > div > div > div > div > '
            'div > div > div.bd-grid-3.bd-margins > div > div > div > div > article > div.bd-postimage-19.pull-none > '
            'a > img::attr(src)').extract()
        post_links: list = response.css(
            'body > div.bd-containereffect-11.container-effect.container > div > div > div > div > div > div > div > '
            'div > div > div.bd-grid-3.bd-margins > div > div > div > div > article > div.bd-postimage-19.pull-none > '
            'a::attr(href)').extract()
        image_tags: list = response.css(
            'body > div.bd-containereffect-11.container-effect.container > div > div > div > div > div > div > div > '
            'div > div > div.bd-grid-3.bd-margins > div > div > div > div > article > h2 > a::text').extract()
        new_post_links: list = [self.source + index for index in post_links]
        new_image_links: list = [self.source + i for i in image_links]
        new_image_tags: list = [" ".join(re.findall(r'\w+', item)) for item in image_tags]
        post_headlines: list = response.css(
            'body > div.bd-containereffect-11.container-effect.container > div > div > div > div > div > div > div > '
            'div > div > div.bd-grid-3.bd-margins > div > div > div:nth-child(1) > div > article > h2 > '
            'a::text').extract()

        yield {
            "image_links": new_image_links,
            "post_links": new_post_links,
            "image_source_alt": new_image_tags,
            "post_headlines": post_headlines,
            "append_source": self.append_source,
            "source": self.source,
        }
