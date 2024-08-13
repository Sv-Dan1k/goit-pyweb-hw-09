import scrapy
from spiderproject.items import AuthorItem


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]


    def parse(self, response):
        for author in response.xpath('//div[@class="quote"]'):
            author_url = author.xpath('span/small[@class="author"]//following-sibling::a/@href').get()
            if author_url:
                yield response.follow(author_url, self.parse_author)

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)


    def parse_author(self, response):
        item = AuthorItem()
        name = response.xpath('//h3[@class="author-title"]/text()').get()
        birthdate = response.xpath('//span[@class="author-born-date"]/text()').get()
        born_location = response.xpath('//span[@class="author-born-location"]/text()').get()
        author_url_description = response.url

        item['fullname'] = name
        item['born_date'] = birthdate
        item['born_location'] = born_location
        item['author_url_description'] = author_url_description
    
        yield item