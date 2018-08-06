# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from peopleSpider.items import PeoplespiderItem
import json
import re
import requests
from scrapy.loader.processors import MapCompose, TakeFirst, Join
# from peopleSpider.items import DazhongItemLoader


class ChildrenSpider(scrapy.Spider):
    name = 'children'
    cityList = [
        'shanghai',
        # 'beijing', 'guangzhou', 'nanjing', 'shenzhen', 'chongqing', 'chengdu', 'wuhan', 'tianjin', 'kunming',
        # 'hangzhou', 'suzhou', 'xian', 'changchun', 'qingdao', 'shijiazhuang', 'changsha', 'zhengzhou', 'wuxi', 'dalian',
        # 'shenyang', 'ningbo', 'nanchang', 'hefei', 'haerbin', 'nanning', 'foshan', 'fuzhou', 'dongguan', 'xiamen', 'guiyang'
    ]

    def start_requests(self):
        # 爬虫起点
        for cityName in self.cityList:
            url = 'http://www.dianping.com/' + cityName +'/ch70/g161'
        # 可以一口吃个胖子的形式横向所有城市然后纵向，也可以如下 一页一页遍历，如下。
        # for i in range(1, 30):
        #     url = 'http://www.dianping.com/'+'xian' + '/ch70/g27760' + str(i)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # follow跟踪会自动将链接拼接成绝对路径
        links = response.css('#J_boxList .shop-list li a.pic::attr(href)').re('.*www.dianping.com/shop.*')
        city = response.css('#logo-input a[class*="city"] span:nth-of-type(2)::text').extract_first()
        for link in links:
            yield response.follow(url=link, callback=self.detail_info, meta={'city': city})

        next_page = response.css('.Pages a.NextPage::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def detail_info(self, response):

        def hasValue(value):
            if value:
                if re.sub('\s', '', value):
                    return re.sub('\s', '', value)
                else:
                    return False
            else:
                return False
        city = hasValue(response.meta['city']) or ''

        item = PeoplespiderItem()
        item['pageLink'] = response.url

        if 'J_boxDetail' in response.text:

            item['city'] = city
            item['title'] = response.css('.shop-info .shop-title::text').extract_first() or ''

            # 正则匹配标题图片，如果存在，拼接绝对路径，否则空列表
            title_img = response.css('.mainpic img::attr(src)').re('.*?(.*.jpg|.*.png).*')
            if len(title_img) > 0:
                item['titleImg'] = [response.urljoin(title_img[0])]
                # 添加道image_urls列表中，准备下载
                item['image_urls'] = [response.urljoin(title_img[0])]
            else:
                item['titleImg'] = []
            item['star'] = response.css('.shop-info .comment-rst span[itemprop="rating"]::attr(title)').extract_first() or ''

            # 平均价格取数字，没有为 -
            if len(response.css('.shop-info .average::text').re('\d')) > 0:
                item['avprice'] = response.css('.shop-info .average::text').re('.*?(\d+).*')[0]
            else:
                item['avprice'] = ''
            item['address'] = response.css('.shop-info .shop-addr span::attr(title)').extract_first() or ''

            # 去除多个电话间的特殊符号
            phone = response.css('.shop-info .shopinfor span::text').extract_first()
            if phone:
                item['phone'] = re.split(r'\xa0\xa0', phone)
            else:
                item['phone'] = []
            item['nearLocation'] = response.css('.shop-info .gray-font::text').extract_first() or ''
            # 如果有俩信息，则正常赋值，否则payType为空列表

            item['payType'] = response.css('.shop-info .more-class p:contains("付款") span::text').extract()
            workTime = response.css('.shop-info .more-class p:contains("营业") span::text').extract_first()
            item['workTime'] = hasValue(workTime) or ''

            # 游玩须知 left key, right value,设施单独提取，因为为一个列表
            sheshi = response.css('.services-list .services-text::text').extract() or []
            purchaseKeys = [val for val in list(map(hasValue, response.xpath('//*[@class="purchase-notes"]/li[@class="notes-item"]/*[@class="list-tit"]//text()').extract())) if val] or []
            purchaseValues = [val for val in list(map(hasValue, response.xpath('//*[@class="purchase-notes"]/li[@class="notes-item"]/*[@class="list-item"]//text()').extract())) if val] or []
            purchaseValues.insert(0, sheshi)
            item['playNotice'] = dict(zip(purchaseKeys, purchaseValues))
            introduce = response.css('.J_showWarp span::text').extract_first()
            item['introduce'] = hasValue(introduce) or ''
            # 合并图片url 列表
            item['image_urls'] += response.css('.J_picDetailUl li img::attr(src)').re('.*?(.*.jpg|.*.png).*')

        else:
            item['city'] = city
            item['title'] = response.css('.shop-info .shop-title::text').extract_first() or ''
            # 标题图片
            title_img = response.css('.shop-info .thumb-wrapper img::attr(src)').re('.*?(.*.jpg|.*.png).*')
            if len(title_img) > 0:
                # 拼接绝对路径
                item['titleImg'] = [response.urljoin(title_img[0])]
                # 加入下载列表中
                item['image_urls'] = [response.urljoin(title_img[0])]
            else:
                item['titleImg'] = []
                item['image_urls'] = []
            item['star'] = response.css('.shop-info .comment-rst span[itemprop="rating"]::attr(title)').extract_first() or ''
            item['avprice'] = response.css('.shop-info dl dd::text').extract_first() or ''
            item['address'] = response.css('.shop-info .shopDeal-Info-address dd span[itemprop="street-address"]::text').extract_first() or ''
            item['phone'] = response.css('.shop-info #J-showPhoneNumber::attr(data-real)').extract()
            item['payType'] = []
            item['workTime'] = hasValue(response.css('.shop-detail-info .J_info-edit-wrap[data-info-type="bh"] .J_full-cont::text').extract_first()) or ''
            item['introduce'] = ''

            # 游玩须知
            purchaseKeys = [val for val in list(map(hasValue, response.css(
                '.shop-detail-info .desc-list dl dt::text').extract())) if val] or []
            purchaseValues = [val for val in list(map(hasValue, response.css(
                '.shop-detail-info .desc-list dl dd .J_full-cont::text').extract())) if val] or []

            item['playNotice'] = dict(zip(purchaseKeys, purchaseValues))
            item['nearLocation'] = ''
            # 加入下载列表中,去除图片无用尾椎
            item_images = response.css('.gallery-list li .thumb img::attr(src)').re('.*?(.*.jpg|.*.png).*')
            if len(item_images) > 0:
                item['image_urls'] += list(map(response.urljoin, item_images))

        # 根据地址请求高德逆地址编码接口，查找相应坐标
        # lng_lat_url = 'http://restapi.amap.com/v3/geocode/geo?key=''&address='+item["address"]+'&city=' + city
        # res = requests.get(url=lng_lat_url)
        # res_json = res.json()
        # if res_json['status'] == '1':
        #     item['businessLocation'] = res_json['geocodes'][0]
        # else:
        #     item['businessLocation'] = ''

        return item

