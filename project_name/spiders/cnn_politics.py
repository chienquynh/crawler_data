import scrapy
from project_name.items import MyItem

class NBCNewsSpider(scrapy.Spider):
    name = 'nbc_news'
    allowed_domains = ['nbcnews.com']
    start_urls = ['https://www.nbcnews.com/']

    def parse(self, response):
        # Điều hướng đến từng trang bài báo
        # Trích xuất tất cả các liên kết
        links = response.css('a.title::attr(href)').getall()

        for link in links:
            full_link = response.urljoin(link)
            yield scrapy.Request(full_link, callback=self.parse_article)

    def parse_article(self, response):
        # Trích xuất thông tin chi tiết từ trang bài báo
        title = response.css('h1::text').get()
        author = response.css('.author-byline span span::text').get()
        timestamp = response.css('.time time::text').get()
        content = ' '.join(response.css('.article-body p::text').getall())

        # Tạo một từ điển dựa trên Item và gửi dữ liệu để lưu
        item = MyItem()
        item['title'] = title
        item['author'] = author
        item['timestamp'] = timestamp
        item['content'] = content
        yield item
