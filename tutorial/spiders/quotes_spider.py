from typing import Tuple
import scrapy
from ..items import TutorialItem

class QuoteSpider(scrapy.Spider):
    name = 'quotes'

    start_urls = [
            'https://quotes.toscrape.com'
        ]
        

    def parse(self, response):
        quotes = response.css('div.quote')

        item = TutorialItem()

        for quote in quotes:
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()

            item['quote_text'] = text
            item['author'] = author
            item['tags'] = tags

            yield item

        next_page = response.css('li.next a').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
