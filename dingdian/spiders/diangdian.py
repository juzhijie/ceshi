# -*- coding: utf-8 -*-
import scrapy  # 使用scrapy中的方法
from urllib import parse # 使用urllib中parse的解析方式 用于字符串拼接
from scrapy import Request  # 使用request生成值 传入到下一个函数中
from dingdian.items import DingdianItem  # 引入你定义的mysql字段
# from urllib.parse import urljoin


# 你的顶点类
class DiangdianSpider(scrapy.Spider):
    name = "diangdian"
    start_urls = ['http://www.x23us.com/']  # 你爬取的主网页


    #  你的解析函数
    def parse(self, response):
        # 得到你主网页中的分类的href链接 这里使用的是它自带的xpath方法
        title = response.xpath('/html/body/div[2]/ul/li/a/@href').extract()[1:12]
        # 遍历你的到的所有链接
        for i in title:
            # 得到url  有的网页上没有域名只有一点数据进行数据拼接 使用urllib中的parse进行拼接 并传入到下一个解析分页的函数中
            yield Request(url=parse.urljoin(response.url, i), callback=self.parse_get)


    # 分页的解析函数
    def parse_get(self, response):
        # 得到最大页数
        name = response.xpath('//*[@id="pagelink"]/a[14]/text()').extract()[0]
        # 遍历最大页
        for i in range(1, int(name)):
            if response.url != 'http://www.x23us.com/quanben/1':
                left_url = response.url[:-6]
                right_url = response.url[-5:]
                # 得到最大页进行拼接
                yield Request(left_url + str(i) + right_url, callback=self.get_parse)
            else:
                # 传入到章节分析的函数中
                yield Request(parse.urljoin(response.url, str(i)), callback=self.get_parse)

    # 文章节分析的函数
    def get_parse(self, response):
        try:
            # 得到文章的url
            article_url = response.xpath('//*[@id="content"]/dd/table/tr/td/a/@href').extract()[1]
            # 作者名称
            author = response.xpath('//*[@id="content"]/dd[1]/table/tr/td/text()').extract()[0]
            yield Request(article_url, callback=self.page_list, meta={'author': author})  # 传入到分析内容的函数中
        except:
            pass

    # 章节
    def page_list(self, response):
        # 小说的名称
        title = response.xpath('//*[@id="a_main"]/div/dl/dd/h1/text()').extract()[0]
        # 章节的链接
        content_url = response.xpath('//*[@id="at"]/tr/td/a/@href').extract()[0]
        # 传入到内容分析的函数中 并把小说的标题传入到下一个函数中
        yield Request(parse.urljoin(response.url, content_url), callback=self.content_html,
                      meta={'title': title, 'author': response.meta['author']})

    # 内容的解析函数
    def content_html(self, response):
        item = DingdianItem()  # 引入定义存数据的item文件
        # 找到文章的标题
        title1 = response.xpath('//*[@id="amain"]/dl/dd[1]/h1/text()').extract()[0]
        item['book'] = response.meta['title']  # 书名
        item['article_title'] = title1  # 文章的标题
        item['author'] = response.meta['author']  # 作者
        content_all = ''  # 定一个空字符串 用来接受你得到的数据
        # 文章的内容 返回一个列表 mysql不能直接存列表
        content_con = response.xpath('//*[@id="contents"]/text()').extract()
        for i in content_con:  # 遍历你的列表
            content_all = content_all + i.strip()  # 得到内容后 去除空格 加入到空字符串
        item['content'] = content_all  # 得到你的内容
        yield item
