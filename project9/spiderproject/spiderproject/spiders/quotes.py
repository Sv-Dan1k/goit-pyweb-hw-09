import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']


    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('span[@class="text"]/text()').get(),
                'author': quote.xpath('span/small[@class="author"]/text()').get(),
                'tags': quote.xpath('div[@class="tags"]/a[@class="tag"]/text()').getall(),
            }
        
        
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
