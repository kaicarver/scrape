import scrapy

class QuotesSpider(scrapy.Spider):
  name = "quotes"
def start_requests(self):
  