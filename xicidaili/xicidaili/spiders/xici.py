# -*- coding: utf-8 -*-
import scrapy
import re
#from scrapy_redis.spiders import RedisSpider


class XiciSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/']

    def __init__(self, ipType = None):
        if ipType == 'http':
            self.ips = 'http://www.xicidaili.com/wt'
        elif ipType == 'https':
            self.ips = 'http://www.xicidaili.com/wn'
        elif ipType == 'nn':
            self.ips = 'http://www.xicidaili.com/nn'
        elif ipType == 'nt':
            self.ips = 'http://www.xicidaili.com/nt'
        elif ipType == 'qq':
            self.ips = 'http://www.xicidaili.com/qq'
        else:
            self.ips = 'http://www.xicidaili.com/wt'

    def parse(self, response):
        print('=============')
        print(response.body)
        url = self.ips
        yield scrapy.Request(url, callback=self.getPage, dont_filter=True)

    def getPage(self, response):
        print('------------')
        pageNum = response.xpath('//a/text()').extract()[-2]
        print(pageNum)
        for i in range(1, int(pageNum) + 1):
            pageUrl = self.ips + '/%d' % i
            yield scrapy.Request(url=pageUrl, callback=self.getips, dont_filter=True)

    def getips(self, response):
        httpIp = response.xpath('//table[@id="ip_list"]/tr')[1:]
        ip = httpIp[0].xpath('//td[2]/text()').extract()
        port = httpIp[0].xpath('//td[3]/text()').extract()
        Type = httpIp[0].xpath('//td[6]/text()').extract()
        for i in range(len(ip)):
            ip_list = Type[i] + '://' + ip[i] + ':' + port[i]
            data = {}
            data['proxy'] = ip_list
            yield scrapy.Request(url='http://2017.ip138.com/ic.asp', callback=self.getuse, meta=data, dont_filter=True)

    def getuse(self, response):
        reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
        ip = response.xpath('/html/body/center/text()').extract()[0]
        proxIp = response.meta['proxy']
        print(proxIp)
        sip = proxIp.split('://')[1].split(':')[0]
        dip = reip.findall(ip)[0]
        print('#'*25)
        print(dip)
        print(sip)
        if dip == sip:
            print('OK====%s===' % sip)
            with open('ips.txt', 'a') as f:
                f.write(proxIp + '\n')
        else:
            print('not ok')



