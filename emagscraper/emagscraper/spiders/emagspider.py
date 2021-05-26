import scrapy
from scrapy import Selector
import datetime

date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class emagSpider(scrapy.Spider):
    name = "emag"
    base_url = 'https://www.emag.ro'
    search_url = base_url+'/search/'
    start_urls = [
        search_url+'placa+video',
        search_url+'oculus+rift',
    ]

    def parse(self, response):
        for products in response.css('div.card-section-wrapper.js-section-wrapper'):
            try:
                yield {
                    'name': products.css('a.product-title.js-product-url::text').get().strip().encode("ascii", "ignore").decode(),
                    'price': products.css('p.product-new-price::text').get(),
                    'link': products.css('a.product-title.js-product-url').attrib['href']
                }
            except:
                continue
        
        pages = (Selector(text=response.css('#listing-paginator').get())).xpath('//li//a/@href').getall()
        next_page = self.base_url + pages[len(pages)-1]

        print(next_page)
        if "javascript" not in next_page:
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)
