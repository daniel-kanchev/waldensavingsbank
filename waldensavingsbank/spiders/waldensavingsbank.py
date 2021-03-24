import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from waldensavingsbank.items import Article


class WaldensavingsbankSpider(scrapy.Spider):
    name = 'waldensavingsbank'
    start_urls = ['https://waldensavings.bank/news']

    def parse(self, response):
        links = response.xpath('//a[@class="list-learn-more"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//p[@class="news-title"]//text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//p[@class="news-date"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//section[@class="news-detail-box"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[5:]).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
