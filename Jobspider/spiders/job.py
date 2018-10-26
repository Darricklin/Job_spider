# -*- coding: utf-8 -*-
import scrapy
from Jobspider.items import JobspiderItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['zhaopin.com']
    start_urls = ['https://sou.zhaopin.com/?p=%d&Size=60&jl=530&kw=Python&kt=3'% i for i in range(1,6)]
    # rules = (
    #     Rule(LinkExtractor(allow=r'https://sou.zhaopin.com/?p=\d+&Size=60&jl=530&kw=Python&kt=3'),callback='parse',follow=True),
    # )
    def parse(self, response):
        job_list=response.xpath("//div[@class='infoBox']")
        for job in job_list:
            item = JobspiderItem()
            item['job']=job.xpath(".//a/span[@class='job_title']/@title").extract()[0]
            item['company']=''.join(re.findall(r'(\w)','--'.join(job.xpath(".//div[@class='commpanyName']/a/@title").extract()+job_list.xpath(".//div[@class='commpanyDesc']/span/text()").extract()[0:2])))
            item['money'] = job.xpath(".//div[@class='jobDesc']/p/text()").extract()[0]
            url=job.xpath(".//div[@class='jobName']/a/@href").extract()[0]
            yield scrapy.Request(url=url,callback=self.next_parse,meta={'item':item},)
    def next_parse(self,response):
        item=response.meta['item']
        item['ability'] =''.join(re.findall(r'(\w)',''.join(response.xpath("//div[@class='terminalpage-main clearfix']//div[@class='tab-inner-cont'][1]//p//text()").extract())))
        item['location'] = ''.join(re.findall(r'(\w)',''.join(response.xpath("//div[@class='tab-inner-cont']/h2/text()").extract())))
        item['fuli']=''.join(re.findall(r'(\w)',''.join(response.xpath("//div[@class='welfare-tab-box']//text()").extract())))
        print(item)
        yield item


