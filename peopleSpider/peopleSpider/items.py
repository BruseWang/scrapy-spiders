# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def sub_br(val):
    return re.sub(r'\n', '', val)


def sub_phone(val):
    return re.split(r'\xa0\xa0', val)


def default_value(value):
    if value is None or value == '':
        return ''


class PeoplespiderItem(scrapy.Item):

    # 图片
    image_urls = scrapy.Field(

    )
    images = scrapy.Field(
    )

    city = scrapy.Field(
        # output_processor=TakeFirst()
    )
    pageLink = scrapy.Field()
    title = scrapy.Field(
        # output_processor=TakeFirst()
    )

    titleImg = scrapy.Field()

    star = scrapy.Field(
        # output_processor=TakeFirst()
    )
    avprice = scrapy.Field(
        # output_processor=TakeFirst()
    )

    address = scrapy.Field(
        # output_processor=TakeFirst()
    )

    # 游玩须知
    playNotice = scrapy.Field()
    # 附近
    nearLocation = scrapy.Field()

    # # 经纬度
    # lngLat = scrapy.Field(
    #     output_processor=TakeFirst()
    # )

    phone = scrapy.Field(
        input_processor=MapCompose(sub_phone)
    )

    payType = scrapy.Field(
        input_processor=MapCompose(sub_br)
    )

    workTime = scrapy.Field(
        input_processor=MapCompose(sub_br),
        # output_processor=TakeFirst()
    )

    introduce = scrapy.Field()

    businessLocation = scrapy.Field()