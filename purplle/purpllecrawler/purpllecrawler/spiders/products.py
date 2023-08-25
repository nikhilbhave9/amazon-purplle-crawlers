import scrapy 
import json
from purpllecrawler.items import PurpllecrawlerItem

class ProductSpider(scrapy.Spider):
    name="products"
    allowed_domains = ["purple.com"]
    start_urls = [
        "https://www.purplle.com/hair/hair-oil"
    ]

    def parse(self, response):
        # prod_list = response.xpath('//div[@id="listing"]/div[@_ngcontent-plr-c56]/div') prd-lstng
        yield from json.loads(response.text)['data']
        prod_list = response.xpath('//div[contains(@class, "prd-lstng")]')
        for prod in prod_list:
            item = PurpllecrawlerItem()
            item['name'] = prod.xpath('.//div[contains(@class, "pro-name")]/text()').get()
            # item['price'] = prod.xpath('.//i[contains(@class, "p-rupee")]/text()').get()
            item['price'] = prod.xpath('.//span[contains(@class, "tx-0")]/descendant::*/text()').get()
            item['image'] = prod.xpath('.//img[@class="img-fix-thumb"]/@src').get()
            yield item