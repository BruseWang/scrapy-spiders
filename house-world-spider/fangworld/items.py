# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader


class FirstItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class FanghouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    # 来源url
    source_url = scrapy.Field(
    )
    # 标题
    title = scrapy.Field()
    # 封面
    image = scrapy.Field()
    # 轮播
    litImg = scrapy.Field()
    # 面积
    acreage = scrapy.Field()
    # 户型id
    house_type_id = scrapy.Field()
    # 户型名称
    house_type_name = scrapy.Field()
    # 厅数量
    liveroom_count = scrapy.Field()
    # 室数量
    bedroom_count = scrapy.Field()
    # 楼型id
    building_type_id = scrapy.Field()
    # 楼型名称
    building_type_name = scrapy.Field()
    # 装修id
    renovation_id = scrapy.Field()
    # 装修名称
    renovation_name = scrapy.Field()
    # 朝向id
    orientation_id = scrapy.Field()
    # 朝向名称
    orientation_name = scrapy.Field()
    # 楼层id
    floor_id = scrapy.Field()
    # 楼层名称（高中低等）
    floor_name = scrapy.Field()
    # 房号
    room_num = scrapy.Field()
    # 年代
    years = scrapy.Field()
    # 房屋详情
    house_info = scrapy.Field(
        # output_processor= MapCompose(print)
    )
    # 出租方式id
    rental_mode_id = scrapy.Field()
    # 出租方式名称
    rental_mode_name = scrapy.Field()
    # 小区
    village_id = scrapy.Field()
    # 小区名称
    village_name = scrapy.Field()
    # 楼栋
    building = scrapy.Field()
    # 单元
    unit = scrapy.Field()
    # 来源（1爬取，2用户添加，3管理员添加）
    source_type = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 显示价格
    show_price = scrapy.Field()
    # 省份id
    province_id = scrapy.Field()
    # 省份名称
    province_name = scrapy.Field()
    # 省份拼音
    province_pinyin = scrapy.Field()
    # 城市id
    city_id = scrapy.Field()
    # 城市名称
    city_name = scrapy.Field()
    # 城市拼音
    city_pinyin = scrapy.Field()
    # 县区id
    area_id = scrapy.Field()
    # 县区名称
    area_name = scrapy.Field()
    # 县区拼音
    area_pinyin = scrapy.Field()
    # 商圈id
    trade_area_id = scrapy.Field()
    # 商圈名称
    trade_area_name = scrapy.Field()
    # 地铁id 用, 分隔
    metro_id = scrapy.Field()
    # 地铁描述 用, 分隔
    metro_name = scrapy.Field()
    # 站点id
    metro_station_id = scrapy.Field()
    # 站点名称
    metro_station_name = scrapy.Field()
    # 详细地址
    address = scrapy.Field()
    # 上架时间
    shelve_date = scrapy.Field()
    # 下架时间
    off_shelve_date = scrapy.Field()
    # 状态（1上架，2下架）
    status = scrapy.Field()
    # 纬度
    lat = scrapy.Field()
    # 经度
    lng = scrapy.Field()
    # 浏览量
    see_count = scrapy.Field()
    # 预约数量
    bespeak_count = scrapy.Field()
    # 收藏数量
    favourite_count = scrapy.Field()
    # 认领数量
    broker_count = scrapy.Field()
    # 配套设施id 用, 分隔
    supporting_facilities_id = scrapy.Field()
    # 配套设施描述 用, 分割
    supporting_facilities_text = scrapy.Field()
    # 信息更新时间
    update_date = scrapy.Field()
    # 是否推荐（1否，2 是）
    is_recommend = scrapy.Field()
    # 1有效，2无效
    is_delete = scrapy.Field()
    # 创建人
    create_user = scrapy.Field()
    # 创建时间
    create_date = scrapy.Field()
    # 最后更新内容
    last_update_remark = scrapy.Field()
    # 房源类型（1出租房，2买房）
    house_source_type = scrapy.Field()
    # 1出租，2二手房，3新房
    second_hand_house = scrapy.Field()
    # 图片是否下载，2否，1是
    is_download_image = scrapy.Field()
    # 备用小区id
    village_id_bak = scrapy.Field()

    # 经纪人item
    # 名称
    broker_name = scrapy.Field()
    # 电话
    broker_mobile = scrapy.Field()
    # 公司
    broker_company_name = scrapy.Field()
    # # 报价
    public_price = scrapy.Field()
    # 上架时间
    shelve_date = scrapy.Field()