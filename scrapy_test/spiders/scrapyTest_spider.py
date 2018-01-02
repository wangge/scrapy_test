import scrapy
from scrapy_test.items import ScrapyTestItem
from scrapy.http import Request
from bs4 import BeautifulSoup
class ScrapyTestSpider(scrapy.Spider):
    name = 'ScrapyTest'
    allowed_domains = ["sina.com.cn"]
    start_urls =[
        "http://sc.sina.com.cn/",
    ]

    def parse(self, response):
        for sel in response.xpath('//ul/li[@doc_id]'):
            item = ScrapyTestItem()
            item['title'] = sel.xpath('.//h2/a/text()').extract()
            item['link'] = sel.xpath('.//h2/a/@href').extract()
            item['image_urls'] = sel.xpath('.//a/img/@src').extract()

            next_url = item["link"][0]
            yield Request(url=next_url, meta={"item": item}, callback=self.parse2)

    def parse2(self, response):
        item = response.meta['item']
        content = response.css('div[class="swpt-1013"]::text').extract()
        item["desc"] = content
        return item