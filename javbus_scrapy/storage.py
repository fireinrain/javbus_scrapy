#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Description: sqlite3 操作相关
@Author  : fireinrain
@Site    : https://github.com/fireinrain
@File    : storage.py
@Software: PyCharm
@Time    : 2022/7/14 2:31 AM
"""
import os
import sqlite3

from javbus_scrapy import settings

db_store_path = os.path.join(settings.DATA_STORE, "javbus.db")

db = sqlite3.connect(db_store_path)

db_cursor = db.cursor()

# create table for javbus actresses
# # 名字
# name
# # 个人主页地址
# star_page_url
# # 最新的一部作品url
# latest_movie_url
# # 最新作品简介
# latest_movie_intro -> latest_movie_code,latest_movie_publish_date,latest_movie_name
# # 大头贴地址
# head_photo_url
# # censored or uncensored
# # 有码 还是无码
# censored
create_actress_sql = 'create table if not exists actresses(' \
                     'id INTEGER PRIMARY KEY,' \
                     'star_info_id INTEGER,' \
                     'user_name TEXT, ' \
                     'start_page_url TEXT,' \
                     'latest_movie_url TEXT,' \
                     'latest_movie_code TEXT,' \
                     'latest_movie_publish_date TEXT,' \
                     'latest_movie_name TEXT,' \
                     'head_photo_url TEXT,' \
                     'censor_url TEXT)'

db.execute(create_actress_sql)

# create table for javbus movie item intro
# 名字
# star_name
# 作品url
# movie_url
# 作品封面图片地址
# movie_cover_url
# 作品名
# movie_title
# 是否是有码作品 默认是True 有码
# movie_censored
# 是否有磁力链接 默认为False
# movie_has_magnet
# 作品清晰度  默认为""
# movie_resolutions
# 作品是否有字幕下载的磁力 默认为False
# movie_has_subtitle
# 作品字幕标识 默认为""
# movie_subtitle_flag
# 作品番号
# movie_code
# 作品发行日期
# movie_publish_date
create_movie_intro_sql = 'create table if not exists movie_intro(' \
                         'id INTEGER PRIMARY KEY,' \
                         'actress_id INTEGER,' \
                         'star_name TEXT,' \
                         'movie_url TEXT,' \
                         'movie_cover_url TEXT,' \
                         'movie_title TEXT,' \
                         'movie_censored TEXT,' \
                         'movie_has_magnet TEXT,' \
                         'movie_resolutions TEXT,' \
                         'movie_has_subtitle TEXT,' \
                         'movie_subtitle_flag TEXT,' \
                         'movie_code TEXT,' \
                         'movie_publish_date TEXT' \
                         ')'
db_cursor.execute(create_movie_intro_sql)

# create table for movie star info
# 演员名
# star_name
# 大头贴url
# star_head_photo_url
# 所有作品数量
# all_item_counts
# 磁力作品数量
# magnet_item_counts
# 有码演员
# censored_star
# 生日
# birthday
# 年龄
# age
# 身高
# height
# 罩杯
# cup
# 胸围
# chest_circumference
# 腰围
# waistline
# 臀围
# hip_circumference
# 出生地
# birthplace
# 爱好
# habbits
create_star_info_sql = 'create table if not exists star_info(' \
                       'id INTEGER PRIMARY KEY,' \
                       'star_name TEXT,' \
                       'star_head_photo_url TEXT,' \
                       'all_item_counts INTEGER,' \
                       'magnet_item_counts INTEGER,' \
                       'censored_star TEXT,' \
                       'birthday TEXT,' \
                       'age TEXT,' \
                       'height TEXT,' \
                       'cup TEXT,' \
                       'chest_circumference TEXT,' \
                       'waistline TEXT,' \
                       'hip_circumference TEXT,' \
                       'birthplace TEXT,' \
                       'habbits TEXT' \
                       ')'

db_cursor.execute(create_star_info_sql)

# create table for movie detail
# 作品名
# movie_title
# 是否为有码作品
# movie_censored
# 作品链接
# movie_url
# 封面缩略图
# movie_cover_url
# 番号
# movie_code
# 发行日期
# movie_publish_date
# 作品时长
# movie_duration
# 导演
# movie_directors
# 制作商
# movie_maker
# 发行商
# movie_publisher
# 系列
# movie_series
# 类别
# movie_tags
# 演员列表
# movie_stars
# 样品图链接
# movie_sample_photo_urls

# create table for torrent info

# create table for toorent_info_detail

# create table for torrent detail


if __name__ == '__main__':
    pass
