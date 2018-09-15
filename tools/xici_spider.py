# -*- coding:utf-8 -*-
__author__ = 'maruimin'


import requests
from scrapy.selector import Selector
import random
from fake_useragent import UserAgent

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}



#def get_random_ip():
ip_list = []
port_list = []
type_list = []
for i in range(1, 3):
    response = requests.get('http://www.xicidaili.com/nn/{}'.format(i), headers=headers)

    xici_response = Selector(text=response.text)

    #获取所有的ip地址
    all_ips = xici_response.xpath('//*[@id="ip_list"]/tr[@class="odd"]/td[2]/text()|//*[@id="ip_list"]/tr[@class=""]/td[2]/text()').extract()
    for ip in all_ips:
        ip_list.append(ip)

    #获取所有的port
    all_ports = xici_response.xpath('//*[@id="ip_list"]/tr[@class="odd"]/td[3]/text()|//*[@id="ip_list"]/tr[@class=""]/td[3]/text()').extract()
    for port in all_ports:
        port_list.append(port)

    #获取所有的类型
    all_type = xici_response.xpath('//*[@id="ip_list"]/tr[@class="odd"]/td[6]/text()|//*[@id="ip_list"]/tr[@class=""]/td[6]/text()').extract()
    for type in all_type:
        type_list.append(type)
#
# random_num = random.randint(0, len(ip_list)-1)
# random_ip = '{}//{}:{}'.format(type_list[random_num], ip_list[random_num], port_list[random_num])
#return random_ip


print(len(ip_list))

# #https//123:222
#
# index = random.randint(0, len(a)-1)
#
# print(index)
# # ip = '{}//{}:{}'.format(c[index], a[index], b[index])
# # print(ip)