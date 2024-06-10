import scrapy
import json
from scrapy.crawler import CrawlerProcess

headers = {"X-Funds-Nonce": "61495f60b533cc40ad822e054998a3190ea9bca0d94791a1da"}

class FiispiderSpider(scrapy.Spider):
    name = "fiispider"
    allowed_domains = ["fundsexplorer.com.br"]

    def start_requests(self):
        start_urls = ["https://www.fundsexplorer.com.br/wp-json/funds/v1/get-ranking"]
        # https://www.fundsexplorer.com.br/wp-json/funds/v1/get-properties
        for url in start_urls:
            yield scrapy.Request(url, headers=headers)

    def parse(self, response):
        for row in json.loads(response.json()):
            yield row

# Run the spider

process = CrawlerProcess()
process.crawl(FiispiderSpider)
process.start()
