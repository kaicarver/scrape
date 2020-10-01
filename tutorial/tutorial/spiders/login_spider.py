import scrapy
from scrapy.http import FormRequests


class LoginSpider(Scrapy.spider):
    name = 'login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']


def parse(self, response):
        csrf_token = response.xpath('//*[@name='csrf_token']
                     /@value').extract_first()')
        yield FormRequests.from_response(response, formdata = {'csrf_token': csrf_token, 'user': 'user', 'pass', 'pass'}, callback = self.parse_after_login)
def parse_after_login(self, response):
    pass