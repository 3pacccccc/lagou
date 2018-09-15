# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
import re
from fake_useragent import UserAgent

from lagou.function.get_md5 import get_md5
from lagou.items import lagouitem


class LagouSpider(CrawlSpider):
    name = 'Lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']


    ua = UserAgent()

    custom_settings = {
        "COOKIES_ENABLED": False,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'user_trace_token=20171015132411-12af3b52-3a51-466f-bfae-a98fc96b4f90; LGUID=20171015132412-13eaf40f-b169-11e7-960b-525400f775ce; SEARCH_ID=070e82cdbbc04cc8b97710c2c0159ce1; ab_test_random_num=0; X_HTTP_TOKEN=d1cf855aacf760c3965ee017e0d3eb96; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DsXIrWUxpNGLE2g_bKzlUCXPTRJMHxfCs6L20RqgCpUq%26wd%3D%26eqid%3Dee53adaf00026e940000000559e354cc; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_hotjob; login=false; unick=""; _putrc=""; JSESSIONID=ABAAABAAAFCAAEG50060B788C4EED616EB9D1BF30380575; _gat=1; _ga=GA1.2.471681568.1508045060; LGSID=20171015203008-94e1afa5-b1a4-11e7-9788-525400f775ce; LGRID=20171015204552-c792b887-b1a6-11e7-9788-525400f775ce',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/',
            'User-Agent': ua.random,
        }
    }


    rules = (
        Rule(LinkExtractor(allow=('zhaopin/')), callback='parse_type', follow=True),
    )




    def parse_type(self, response):
        type_match = re.match('.*/zhaopin/?(.*)/', response.url)
        if type_match:
            type = type_match.group(1)
        all_urls = response.css('a::attr(href)').extract()
        for url in all_urls:
            if re.match('.*/jobs/\d+.html', url):
                yield scrapy.Request(url, callback=self.parse_item, meta={'type': type}, dont_filter=True)




    def parse_item(self, response):
        #获取工种
        type = response.meta.get('type')
        if '/' in type:
            work_type = type.split('/')[0]
        else:
            work_type = type

        #获取职位的标题
        title = response.css('.position-head span.name::text').extract()[0]

        #获取工作城市
        city = response.xpath('//*[@class="job_request"]/p/span[2]/text()').extract()[0]
        work_city = city.replace('/', '').strip()

        #获取薪资
        salary_str = response.xpath('//*[@class="job_request"]/p/span[1]/text()').extract()[0]
        salary_min = int(re.findall('.*?(\d+)k', salary_str)[0]) *1000   #获取薪资的最小值
        salary_max = int(re.findall('.*?(\d+)k', salary_str)[1]) *1000  #获取薪资的最大值

        #获取公司名称
        company_name = response.css('#job_company .fl::text').extract()[0].split()[0]

        #获取工作经验要求
        work_experience = response.xpath('//*[@class="job_request"]/p/span[3]/text()').extract()[0].replace('/', '').strip()

        #获取学历要求
        work_degree = response.xpath('//*[@class="job_request"]/p/span[4]/text()').extract()[0].replace('/', '').strip()

        #获取url
        url_object_id = get_md5(response.url)



        item = lagouitem()
        item['work_type'] = work_type
        item['title'] = title
        item['work_city'] = work_city
        item['salary_min'] = salary_min
        item['salary_max'] = salary_max
        item['company_name'] = company_name
        item['work_experience'] = work_experience
        item['work_degree'] = work_degree
        item['url_object_id'] = url_object_id

        return item

