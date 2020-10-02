import scrapy
from scrapy.http import FormRequest
import logging
from datetime import datetime
import credentials


class SevenfiftySpider(scrapy.Spider):
    name = 'sevenfifty'
    allowed_domains = ['750words.com']
    start_urls = ['https://750words.com/auth']

    def parse(self, response):
        self.logger.warning('Visiting %s...' % self.start_urls[0])
        authenticity_token = response.xpath(
            '//*[@name="authenticity_token"]/@value').extract_first()
        yield FormRequest.from_response(response,
                                        formdata={
                                            'authenticity_token': authenticity_token,
                                            'person[email_address]': credentials.sevenfifty['user'],
                                            'person[password]': credentials.sevenfifty['password']},
                                        callback=self.parse_after_login)

    def parse_after_login(self, response):
        self.logger.warning('Logged in, getting words...')
        words = response.xpath('//*[@id="entry_body"]/text()').get()
        # print(words)
        filename = '/home/kai/blog/days/%s.txt' % datetime.today().strftime('%Y-%m-%d')
        with open(filename, 'w') as f:
            f.write(words)
        self.logger.warning('Saved today\'s words from %s to file %s' % (
            self.allowed_domains[0], filename))
