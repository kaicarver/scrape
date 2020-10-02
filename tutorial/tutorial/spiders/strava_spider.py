import scrapy
from scrapy.http import FormRequest
import logging
from datetime import datetime
import credentials


class StravaSpider(scrapy.Spider):
    name = 'strava'
    allowed_domains = ['strava.com']
    start_urls = ['https://www.strava.com/login']

    def parse(self, response):
        self.logger.warning('Visiting %s...' % self.start_urls[0])
        authenticity_token = response.xpath(
            '//*[@name="authenticity_token"]/@value').extract_first()
        yield FormRequest.from_response(response,
                                        formdata={
                                            'authenticity_token': authenticity_token,
                                            'email': credentials.strava['user'],
                                            'password': credentials.strava['password']},
                                        callback=self.parse_after_login)

    def parse_after_login(self, response):
        self.logger.warning('Logged in, getting content...')
        #words = response.xpath('//*[@id="entry_body"]/text()').get()
        print(response.body)
        self.logger.warning('Done.')
