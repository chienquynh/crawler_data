import scrapy

class MyItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    timestamp = scrapy.Field()
    content = scrapy.Field()
