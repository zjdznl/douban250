#-*-encoding:utf-8-*-
from scrapy.spiders import Spider
from scrapy import Request
from scrapyspider.items import DoubanMovieItem

class DoubanMovieTop205Spider(Spider):
    name = 'douban_movie_250'

    url = 'https://movie.douban.com/top250'
    # custom_settings = {
    #     'FEDD_URI' : 'tmp/movie.csv'
    # }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        yield Request(self.url, headers=self.headers)

    def parse(self, response):

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        item = DoubanMovieItem()

        movies = response.xpath('//ol[@class="grid_view"]/li')

        for movie in movies:


            item['movie_name'] = movie.xpath('.//div[@class]/a/span[1]/text()').extract()[0]
            item['ranking'] = movie.xpath('.//em/text()').extract()[0]
            item['score'] = movie.xpath('.//span[@class="rating_num"]/text()').extract()[0]
            item['people_num'] = movie.xpath('.//div[@class="star"]/span[4]/text()').re(ur'(\d)+人评价')[0]
            item['image_urls'] = movie.xpath('.//img/@src').extract()
            yield item

        next_url = response.xpath('.//span[@class="next"]/a/@href').extract()[0]
        if next_url:
            next_url = self.url + next_url
            yield Request(next_url, headers=self.headers)


