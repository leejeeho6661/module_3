# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Module03Item(scrapy.Item):
    title =scrapy.Field()
    weekend = scrapy.Field()
    gross = scrapy.Field()
    weeks = scrapy.Field()
    rating = scrapy.Field()
    people = scrapy.Field()
    genre = scrapy.Field()
    movie_release = scrapy.Field()