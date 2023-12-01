import scrapy
from scrapy.loader import ItemLoader
from project_name.items import MyItem

class GuardianSpider(scrapy.Spider):
    name = 'theguardian'
    allowed_domains = ['metatext.io/datasets']
    start_urls = ['https://metatext.io/datasets-list/english-language']
    visited_urls = set()

    def parse(self, response):
        # Extract information from the current page
        loader = ItemLoader(item=MyItem(), response=response)
        loader.add_css('title', 'title::text')
        loader.add_css('author', '.dcr-byline span[itemprop="name"]::text')
        loader.add_css('timestamp', 'time[itemprop="datePublished"]::attr(datetime)')
        loader.add_css('content', '.js-article__body p::text')
        item = loader.load_item()
        yield item

        # Add the current URL to the set of visited URLs
        self.visited_urls.add(response.url)

        # Follow links to individual articles
        for link in response.css('.fc-item__title a::attr(href)').getall():
            full_link = response.urljoin(link)
            if full_link not in self.visited_urls:
                yield scrapy.Request(full_link, callback=self.parse_article)

        # Follow pagination links to the next page
        next_page = response.css('.pagination__item--next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            if next_page_url not in self.visited_urls:
                yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_article(self, response):
        yield from self._parse_content(response, '.content__headline', '.byline a', '.content__article-body p::text', self.parse_sub_article)

    def parse_sub_article(self, response):
        yield from self._parse_content(response, '.content__headline', '.byline a', '.content__article-body p::text', self.parse_sub_article)

    def _parse_content(self, response, title_selector, author_selector, content_selector, callback):
        try:
            # Extract information from articles and sub-articles
            loader = ItemLoader(item=MyItem(), response=response)
            loader.add_css('title', title_selector)
            loader.add_css('author', author_selector)
            loader.add_css('timestamp', 'time[itemprop="datePublished"]::attr(datetime)')
            loader.add_css('content', content_selector)
            item = loader.load_item()
            yield item

            # Follow links to sub-articles within the current article
            for sub_link in response.css('.content__subheading a::attr(href)').getall():
                full_sub_link = response.urljoin(sub_link)
                if full_sub_link not in self.visited_urls:
                    yield scrapy.Request(full_sub_link, callback=callback)

        except Exception as e:
            self.log(f"Error in parsing: {str(e)}")
