# import scrapy
# from project_name.items import MyItem


# class CNNPoliticsSpider(scrapy.Spider):
#     name = 'cnn_politics'
#     allowed_domains = ['edition.cnn.com']
#     start_urls = ['https://www.foxnews.com/']

#     def parse(self, response):
#         # Điều hướng đến từng trang bài báo
#         # Trích xuất tất cả a?các liên kết có class "container__link"
#         links = response.css('a.container__link::attr(href)').getall()
        
#         for link in links:
#             full_link = response.urljoin(link)
#             yield response.follow(full_link, callback=self.parse_article)
            
#     def parse_article(self, response):
#         # Trích xuất thông tin chi tiết từ trang bài báo
#         title = response.css('.headline__text.inline-placeholder::text').get()
#         author = response.css('.byline__name::text').get()
#         timestamp = response.css('.timestamp::text').get()
#         content = ' '.join(response.css('.paragraph.inline-placeholder::text').getall())
        
#         # Tạo một từ điển dựa trên Item và gửi dữ liệu để lưu
#         item = MyItem()
#         item['title'] = title
#         item['author'] = author
#         item['timestamp'] = timestamp
#         item['content'] = content
#         yield item
# bạn chỉnh sửa code này để crawl dữ liệu về trang này code đã chạy được nhưng chưa crawl được thông tin gì tôi đã được cấp phép crawl những trang này






# import scrapy
# from project_name.items import MyItem

# class CNNPoliticsSpider(scrapy.Spider):
#     name = 'cnn_politics'
#     allowed_domains = ['edition.cnn.com']
#     start_urls = ['https://edition.cnn.com/politics']

#     def parse(self, response):
#         # Điều hướng đến từng trang bài báo
#         # Trích xuất tất cả các liên kết có class "container__link"
#         links = response.css('a.container__link::attr(href)').getall()
        
#         for link in links:
#             full_link = response.urljoin(link)
#             yield response.follow(full_link, callback=self.parse_article)
            
#     def parse_article(self, response):
#         # Trích xuất thông tin chi tiết từ trang bài báo
#         title = response.css('.headline__text::text').get()
#         author = response.css('.metadata__byline__author::text').get()
#         timestamp = response.css('.metadata__date::text').get()
#         content = ' '.join(response.css('.zn-body__paragraph::text').getall())
        
#         # Tạo một từ điển dựa trên Item và gửi dữ liệu để lưu
#         item = MyItem()
#         item['title'] = title
#         item['author'] = author
#         item['timestamp'] = timestamp
#         item['content'] = content
#         yield item
