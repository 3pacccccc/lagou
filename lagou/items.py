# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class lagouitem(scrapy.Item):
    company_name = scrapy.Field()
    salary_max = scrapy.Field()
    salary_min = scrapy.Field()
    title = scrapy.Field()
    work_city = scrapy.Field()
    work_degree = scrapy.Field()
    work_experience = scrapy.Field()
    work_type = scrapy.Field()
    url_object_id = scrapy.Field()


    def get_insert_sql(self):
        insert_sql = """
        insert into lagou(company_name, work_type, title, work_city, salary_min, salary_max, work_degree, work_experience, url_object_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
        ON DUPLICATE KEY UPDATE work_degree = VALUES (work_degree)
        """


        params = (self['company_name'], self['work_type'], self['title'], self['work_city'], self['salary_min'], self['salary_max']
                  , self['work_degree'], self['work_experience'], self['url_object_id'])


        return insert_sql, params