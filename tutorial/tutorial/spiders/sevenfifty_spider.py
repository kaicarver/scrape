import scrapy
from scrapy.http import FormRequest
import logging


class SevenfiftySpider(scrapy.Spider):
    name = 'sevenfifty'
    allowed_domains = ['750words.com']
    start_urls = ['https://750words.com/auth']

    def parse(self, response):
        authenticity_token = response.xpath(
            '//*[@name="authenticity_token"]/@value').extract_first()
        yield FormRequest.from_response(response,
                                        formdata={
                                            'authenticity_token': authenticity_token,
                                            'person[email_address]': 'kaicarver@gmail.com',
                                            'person[password]': 'kaS369CLVDIxQ'},
                                        callback=self.parse_after_login)

    def parse_after_login(self, response):
        words = response.xpath('//*[@id="entry_body"]/text()').get()
        print(words)
        filename = '/home/kai/blog/sevenfifty.html'
        with open(filename, 'w') as f:
            f.write(words)
        self.logger.warning('Saved file %s' % filename)
