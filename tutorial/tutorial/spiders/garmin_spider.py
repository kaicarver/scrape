import scrapy
from scrapy.http import FormRequest
import logging
from datetime import datetime
import credentials


class GarminSpider(scrapy.Spider):
    name = 'garmin'
    allowed_domains = ['connect.garmin.com']
    start_urls = ['https://connect.garmin.com/signin/']

    def parse(self, response):
        self.logger.warning('Visiting %s...' % self.start_urls[0])
        authenticity_token = response.xpath(
            '//*[@name="_csrf"]/@value').extract_first()
        yield FormRequest.from_response(response,
                                        formdata={
                                            '_csrf': authenticity_token,
                                            'username': credentials.garmin['user'],
                                            'password': credentials.garmin['password']},
                                        callback=self.parse_after_login)

    def parse_after_login(self, response):
        self.logger.warning('Logged in, getting content...')
        #words = response.xpath('//*[@id="entry_body"]/text()').get()
        print(response.body)
        self.logger.warning('Done.')
