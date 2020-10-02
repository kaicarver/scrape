import scrapy
from scrapy.http import FormRequest


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
        print("logged in!")
        #print(response.body)
        print(response.xpath('//*[@id="entry_body"]/text()').get())
        filename = 'sevenfifty.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
