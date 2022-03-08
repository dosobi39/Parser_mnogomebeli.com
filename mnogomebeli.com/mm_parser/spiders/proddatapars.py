import csv
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field
from mm_parser.items import Product

urls = input('Введите ссылку на каталог товаров --> ')


class ProddataparsSpider(CrawlSpider):

    name = 'proddatapars'
    allowed_domains = ['mnogomebeli.com']
    start_urls = [urls]

    rules = (Rule(LinkExtractor(allow=('/divany/',), deny=('personal', 'reviews', 'about', 'filter',)), callback='parse', follow=True),)

    with open("out2.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "НАЗВАНИЕ",
                "ССЫЛКА ТОВАРА",
                # "СТАРАЯ ЦЕНА",
                # "ЦЕНА",
                # "ССЫЛКА НА КАРТИНКИ",
                "ОПИСАНИЕ",
                "ОСОБЕННОСТИ",
                "ПРЕИМУЩЕСТВА",
            )
        )

    def parse(self, response):

        item = Product()
        data = []

        # title = response.xpath('//h1[@class="item-header__title t-h1"]/text()').get()
        # if title is not None:
        #     item['product_url'] = response.url
        #     item['title'] = title
        #     item['description'] = response.xpath('(//div[@class="item-info__desc"]//p)[1]/text()').get()
        #
        #     specifications = response.xpath('(//div[@class="item-info__specs"]/ul)[1]/li/p/text()').getall()
        #     item['specifications'] = [x.replace(" ", "") for x in specifications]
        #     # item['specifications'] = specifications
        #
        #     advantages = response.xpath('(//div[@class="item-info__lists"])[1]/ul/li/text()').getall()
        #     item['advantages'] = [x.replace(" ", "") for x in advantages]
        #     # item['advantages'] = advantages
        #
        #     # item['peculiarities'] = response.xpath("").get()
        #     # нужно получить картинки

        # название
        title = response.xpath('//h1[@class="item-header__title t-h1"]/text()').get()
        product_url = response.url

        # описание
        descriptions = response.xpath('(//div[@class="item-info__desc"]//p)[1]/text()').get()

        # название характеристики
        specifications_1 = response.xpath('(//div[@class="item-info__specs"]/ul)[1]/li/p[1]/text()').getall()
        specifications_1 = [x.strip() for x in specifications_1]
        # specification_1 = ['\n'.join(specifications_1)]

        # значение характеристики
        specifications_2 = response.xpath('(//div[@class="item-info__specs"]/ul)[1]/li/p[2]/text()').getall()
        specifications_2 = [x.strip() for x in specifications_2]
        # specification_2 = ['\n'.join(specifications_2)]

        # обЪединение названия и значения характеристик "Название: значение"
        specification = [': '.join(x) for x in zip(specifications_1, specifications_2)]
        specification = ', '.join(specification)


        # преимущества
        advantages = response.xpath('(//div[@class="item-info__lists"])[1]/ul/li/text()').getall()
        advantages = [x.strip() for x in advantages]
        advantage = ', '.join(advantages)

        if title is not None:
            data.append(
                {
                    "title": title,
                    "product_url": product_url,
                    "descriptions": descriptions,
                    "specification": specification,
                    "advantage": advantage,
                }
            )

            with open(f"out2.csv", "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        title,
                        product_url,
                        descriptions,
                        specification,
                        advantage,
                    )
                )

        yield item

# scrapy crawl proddatapars - run
