import scrapy 
from amazoncrawler.items import AmazoncrawlerItem

class ProductSpider(scrapy.Spider):
    name="products"
    allowed_domains = ["amazon.in"]
    # start_urls = [
    #     "https://www.amazon.in/s?k=denim+shirt"
    # ]

    def start_requests(self):
        category = getattr(self, 'category', '')
        urls = [
            f'https://www.amazon.in/s?k={category}'
        ]

        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        prod_list = response.xpath('//div[@data-component-type="s-search-result"]')
        for prod in prod_list:
            item = AmazoncrawlerItem()
            item['name'] = prod.xpath('.//h2[contains(@class, "s-line-clamp-2")]//span[contains(@class, "a-text-normal")]/text()').get()
            item['brand'] = prod.xpath('.//h2[contains(@class, "s-line-clamp-1")]//span/text()').get()
            item['price'] = prod.xpath('.//span[@class="a-price-whole"]/text()').get()
            item['image'] = prod.xpath('.//img[@class="s-image"]/@src').get()
            yield item