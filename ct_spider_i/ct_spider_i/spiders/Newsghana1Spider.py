import scrapy


#  A spider to scrape ImDb
class Newsghana1Spider(scrapy.Spider):
    name = "newsghana1"

    # custom settings for this scraper
    append_source = False
    source = "https://newsghana.com.gh"
    number_of_pages: int =1505
    start = 1

    # This list contains the links for each of the genres in ImDb
    url_list = [
        "https://newsghana.com.gh/sports-news/page/",
        "https://newsghana.com.gh/entertainment/page/",
        "https://newsghana.com.gh/businesswire/page/",
        "https://newsghana.com.gh/opinion/page/",
        "https://newsghana.com.gh/auto/page/",
        "https://newsghana.com.gh/real-estates/page/",
        "https://newsghana.com.gh/health/page/",
        "https://newsghana.com.gh/science-and-technology-news/page/",
        "https://newsghana.com.gh/ghana-news/page/",
    ]

    # This function iterates through the above list and forms
    # a new url using url1, start variable, and url2 which is
    # then passed to the parse function for the actual scraping

    def start_requests(self):
        self.number_of_pages += 1
        for url in self.url_list:
            for page_number in range(1, self.number_of_pages):
                yield scrapy.Request(f"{url}{page_number}/")

    def parse(self, response, **kwargs):
        image_links: list = response.css(
            "#td-outer-wrap > div.td-main-content-wrap.td-container-wrap > div > div > "
            "div.td-pb-span8.td-main-content > div > div > div "
            "> div > div.td-module-image > div > a > img::attr(data-img-url)"
        ).extract()
        post_links: list = response.css(
            "#td-outer-wrap > div.td-main-content-wrap.td-container-wrap > div > div > "
            "div.td-pb-span8.td-main-content > div > div > div "
            "> div > div.td-module-image > div > a::attr(href)"
        ).extract()
        image_tags: list = response.css(
            "#td-outer-wrap > div.td-main-content-wrap.td-container-wrap > div > div > "
            "div.td-pb-span8.td-main-content > div > div > div "
            "> div > div.td-module-image > div > a > img::attr(title)"
        ).extract()
        post_headlines: list = response.css(
            '#td-outer-wrap > div.td-main-content-wrap.td-container-wrap > div > div > '
            'div.td-pb-span8.td-main-content > div > div:nth-child(1) > div:nth-child(1) > div > h3 > '
            'a::text').extract()

        yield {
            "image_links": image_links,
            "post_links": post_links,
            "image_source_alt": image_tags,
            "post_headlines": post_headlines,
            "append_source": self.append_source,
            "source": self.source,
        }