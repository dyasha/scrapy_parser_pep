import re

import scrapy

from ..items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        section = response.css(
            'section[id^="numerical-index"]')
        href = section.css(
            'tbody tr td:nth-child(2) a::attr(href)').getall()
        for link in href:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        pattern = r'^... (\w+)...(.*)'
        title = response.css('section[id^="pep-content"] h1::text').get()
        data = {
            'number': re.search(pattern, title).group(1),
            'name': re.search(pattern, title).group(2),
            'status': response.css('abbr::text').get()
        }
        yield PepParseItem(data)
