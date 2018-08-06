# -*- coding: utf-8 -*-
import scrapy
from fangworld.items import FanghouseItem, FirstItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import datetime
import re


class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['zu.sh.fang.com']
    # start_urls = ['http://zu.sh.fang.com/integrate/']

    def start_requests(self):
        yield scrapy.Request(url='http://zu.sh.fang.com/integrate/')

    def parse(self, response):
        # 区域
        area = response.css(u'#rentid_D04_01 dd a:not(:contains("不限"))::attr(href)').extract()
        for a in area:
            yield response.follow(url=a, callback=self.ring)

    def ring(self, response):
        # 商圈
        ring_name = response.css('#rentid_D04_08 a:not(a[class])::attr(href)').extract()
        for s in ring_name:
            yield response.follow(url=s, callback=self.house_list)

    def house_list(self, response):
        urls = response.css('.houseList dl.list dd p.title a::attr(href)').extract()
        images = response.css('.houseList dl.list dt a img::attr(data-src)').extract()
        for index, url in enumerate(urls):
            yield response.follow(url=url, callback=self.detail, meta={'image': images[index]})
        next_page = response.css('#rentid_D10_01 a:contains("下一页")::attr(href)').extract_first()
        if next_page:
            yield response.follow(url=next_page, callback=self.house_list)

    def detail(self, response):
        meta = response.meta
        if 'zfyxfy_B03_01' or 'zfyxfy_B03_02' in response.text:
            item = FirstItemLoader(item=FanghouseItem(), response=response)
            # 小区id 名称
            item.add_css('village_name', '#zfyxfy_B03_01::text')
            item.add_css('city', '#dsy_H01_01 div.s4Box a::text')
            # 标题
            item.add_css('title', 'h1.title::text')
            # 来源url
            item.add_value('source_url', response.url)
            # 封面
            item.add_value('image', meta['image'])

            # 轮播img
            item.add_css('litImg','ul.litImg li img::attr(src)')
            # 右侧详情
            selector = response.css('.tab-cont-right')
            # 价格
            item.add_css('price', '.zf_new_title .trl-item i::text')
            # 面积
            item.add_css('acreage', '.tt', re='.*?(\d+\.\d+).*')
            # 厅数量 室数量
            building_name = response.css(
                '.tab-cont-right div:nth-child(3) div:nth-child(2) .tt::text').extract_first()
            if building_name:
                try:
                    item.add_value('house_type_name', building_name)
                    # item.add_value('building_type_name', building_name)
                    bedroom = re.match(ur'.*?(\d+)室', building_name)
                    bedroom_count = bedroom.group(1)
                    liveroom = re.match(ur'.*?(\d+)厅', building_name)
                    liveroom_count = liveroom.group(1)
                    item.add_value('bedroom_count', bedroom_count)
                    item.add_value('liveroom_count', liveroom_count)
                except Exception as e:
                    print e.message
            # 装修类型
            item.add_css('renovation_name', '.tab-cont-right div:nth-child(4) div:nth-child(3) .tt::text')
            # 朝向
            item.add_css('orientation_name', '.tab-cont-right div:nth-child(4) div:nth-child(1) .tt::text')
            # 楼层
            item.add_css('floor_name', '.tab-cont-right div:nth-child(4) div:nth-child(2) .tt::text')
            # 房屋详情,描述

            def hasValue(value):
                return re.sub('\s', '', value)

            item.add_css('house_info', '.fydes-item .cont p::text', MapCompose(hasValue))
            # 出租方式 名称
            # item.add_css('rental_mode_id', '')
            item.add_css('rental_mode_name', '.tab-cont-right div:nth-child(3) div:nth-child(1) .tt::text')
            # 价格
            item.add_css('price', '.tab-cont-right .zf_new_title .trl-item i::text')

            # 经纪人数据
            tj_list = response.css('.tab-cont-right div:nth-child(6) .tjcont-list')
            for tj in tj_list:
                tj_nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 经纪人姓名
                broker_name = tj.css('.tjcont-list-cline1 .zf_jjname a::text').extract_first()
                # 电话
                broker_mobile = tj.css('.tjcont-list-cline3 span:nth-child(2) b::text').extract_first()
                # 公司
                broker_company_name = tj.css('.tjcont-list-cline2 span:nth-child(2)::text').extract_first()
                # 报价
                public_price = tj.css('.tjcont-list-cline3 span:nth-child(1) b::text').extract_first()

                item.add_value('broker_name', broker_name)
                item.add_value('broker_mobile', broker_mobile)
                item.add_value('broker_company_name', broker_company_name)
                item.add_value('public_price', public_price)
            yield item.load_item()
