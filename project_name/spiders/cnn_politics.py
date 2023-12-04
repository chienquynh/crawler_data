import scrapy
from scrapy.loader import ItemLoader
from project_name.items import MyItem

class MSNBCSpider(scrapy.Spider):
    name = 'msnbc'
    allowed_domains = ['msnbc.com']
    start_urls = ['http://www.msnbc.com/']

    visited_urls = set()

    def parse(self, response):
        # Extract information from the current page
        loader = ItemLoader(item=MyItem(), response=response)
        loader.add_css('title', 'h2.headline::text')
        loader.add_css('author', 'span[data_test="author_name"]::text')
        loader.add_css('timestamp', 'time[data_time_published]::attr(data_time_published)')
        loader.add_css('content', 'div[itemprop="articleBody"] p::text')
        item = loader.load_item()
        yield item

        # Add the current URL to the set of visited URLs
        self.visited_urls.add(response.url)

        # Follow links to individual articles
        for link in response.css('h2.headline a::attr(href)').getall():
            full_link = response.urljoin(link)
            if full_link not in self.visited_urls:
                yield scrapy.Request(full_link, callback=self.parse_article)

    def parse_article(self, response):
        yield from self._parse_content(response, 'h1.headline', 'span[data_test="author_name"]', 'div[itemprop="articleBody"] p::text', self.parse_sub_article)

    def parse_sub_article(self, response):
        yield from self._parse_content(response, 'h1.headline', 'span[data_test="author_name"]', 'div[itemprop="articleBody"] p::text', self.parse_sub_article)

    def _parse_content(self, response, title_selector, author_selector, content_selector, callback):
        try:
            # Extract information from articles and sub-articles
            loader = ItemLoader(item=MyItem(), response=response)
            loader.add_css('title', title_selector)
            loader.add_css('author', author_selector)
            loader.add_css('timestamp', 'time[data_time_published]::attr(data_time_published)')
            loader.add_css('content', content_selector)
            item = loader.load_item()
            yield item

            # Follow links to sub-articles within the current article
            for sub_link in response.css('a.sub_headline::attr(href)').getall():
                full_sub_link = response.urljoin(sub_link)
                if full_sub_link not in self.visited_urls:
                    yield scrapy.Request(full_sub_link, callback=callback)
        except Exception as e:
            self.log(f"Error in parsing: {str(e)}")
