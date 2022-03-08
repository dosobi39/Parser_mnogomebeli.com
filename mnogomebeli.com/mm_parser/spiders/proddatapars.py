import scrapy


class ProddataparsSpider(scrapy.Spider):
    name = 'proddatapars'
    allowed_domains = ['mnogomebeli.com']
    start_urls = ['https://mnogomebeli.com/krovati/odnospalnye-krovati/']

    def parse(self, response):
        pass
