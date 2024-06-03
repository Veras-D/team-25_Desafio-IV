import scrapy
import json

headers = {"X-Funds-Nonce": "61495f60b533cc40ad822e054998a3190ea9bca0d94791a1da"}  # Update with valid value

class FiispiderSpider(scrapy.Spider):
    name = "fiispider"
    allowed_domains = ["fundsexplorer.com.br"]

    def start_requests(self):
        start_urls = ["https://www.fundsexplorer.com.br/wp-json/funds/v1/get-ranking"]
        for url in start_urls:
            yield scrapy.Request(url, headers=headers)

    def parse(self, response):
        for row in json.loads(response.json()):
            yield row

# Run the spider
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(FiispiderSpider)
process.start()
