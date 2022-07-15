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
import time

from javbus_scrapy import settings, utils
from javbus_scrapy.settings import DATA_STORE, ACTRESSES_PATH_NAME, STARINFO_PATH_NAME, STARITEMINFO_PATH_NAME


class SqliteStorage:
    db_name = None

    def __init__(self, db_name):
        self.db_name = db_name

        self.db_store_path = os.path.join(settings.DATA_STORE, self.db_name)

        self.db = sqlite3.connect(self.db_store_path)

        self.db_cursor = self.db.cursor()

        self.default_column = [("create_datetime", "TEXT"), ("update_datetime", "TEXT")]

    def do_create_table_if_not_exists(self, create_table_sql, index_sql=None):
        try:
            self.db_cursor.execute(create_table_sql)
            if index_sql is not None:
                self.db_cursor.execute(index_sql)
            self.db.commit()
        except Exception as e:
            print(f"sql: {create_table_sql}|{index_sql}")
            print(f"cant create table dude to exception: {e}")
            self.db.rollback()

    def do_excute_sql_with_no_result(self, sql):
        try:
            self.db_cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(f"cant create table dude to exception: {e}")
            self.db.rollback()

    # create_table_actress
    def create_table_actresses(self):
        sql = 'create table if not exists actresses(' \
              'id INTEGER PRIMARY KEY,' \
              'star_info_id INTEGER,' \
              'user_name TEXT,' \
              'star_page_url TEXT,' \
              'latest_movie_url TEXT,' \
              'latest_movie_code TEXT,' \
              'latest_movie_publish_date TEXT,' \
              'latest_movie_name TEXT,' \
              'head_photo_url TEXT,' \
              'censored TEXT)'
        sql = self.sql_fillter_process(sql, self.default_column)
        index_sql = 'create index if not exists index_actresses_movie_code on actresses(latest_movie_code)'
        self.do_create_table_if_not_exists(sql, index_sql)

    # create table for javbus movie item intro
    def create_table_movie_intro(self):
        sql = 'create table if not exists movie_intro(' \
              'id INTEGER PRIMARY KEY,' \
              'star_name TEXT,' \
              'movie_url TEXT,' \
              'movie_cover_url TEXT,' \
              'movie_title TEXT,' \
              'movie_has_magnet TEXT,' \
              'movie_censored TEXT,' \
              'movie_resolutions TEXT,' \
              'movie_has_subtitle TEXT,' \
              'movie_subtitle_flag TEXT,' \
              'movie_code TEXT,' \
              'movie_publish_date TEXT' \
              ')'
        sql = self.sql_fillter_process(sql, self.default_column)
        index_sql = 'create index if not exists movie_intro_movie_code_index  on movie_intro(movie_code)'
        self.do_create_table_if_not_exists(sql, index_sql)

    def import_movie_intro_to_sqlite(self):
        sql = 'insert into movie_intro(' \
              'star_name,' \
              'movie_url,' \
              'movie_cover_url,' \
              'movie_title,' \
              'movie_has_magnet,' \
              'movie_censored,' \
              'movie_resolutions,' \
              'movie_has_subtitle,' \
              'movie_subtitle_flag,' \
              'movie_code,' \
              'movie_publish_date) values (?,?,?,?,?,?,?,?,?,?,?)'

        self.import_data_csv_to_sqlite(insert_sql=sql, data_store_abs_path=STARITEMINFO_PATH_NAME)

    # create table for star info
    def create_table_star_info(self):
        sql = 'create table if not exists star_info(' \
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
        sql = self.sql_fillter_process(sql, self.default_column)
        self.do_create_table_if_not_exists(sql)

    # create table for movie detail
    def create_table_movie_detail(self):
        sql = 'create table if not exists movie_detail(' \
              'id INTEGER PRIMARY KEY autoincrement,' \
              'movie_intro_id INTEGER,' \
              'movie_title TEXT,' \
              'movie_censored TEXT,' \
              'movie_url TEXT,' \
              'movie_cover_url TEXT,' \
              'movie_code TEXT,' \
              'movie_publish_date TEXT,' \
              'movie_duration TEXT,' \
              'movie_director_id INTEGER,' \
              'movie_maker_id INTEGER,' \
              'movie_publisher_id INTEGER,' \
              'movie_series_id INTEGER,' \
              'movie_tags_id INTEGER,' \
              'movie_stars_id INTEGER,' \
              'movie_sample_photo_urls TEXT)'
        sql = self.sql_fillter_process(sql, self.default_column)

        index_sql = 'create index if not exists movie_detail_movie_code_index  on movie_detail(movie_code)'
        self.do_create_table_if_not_exists(sql, index_sql)

    # create table for movie director
    def create_table_movie_director(self):
        sql = 'create table if not exists movie_director(' \
              'id INTEGER PRIMARY KEY autoincrement,' \
              'director_name TEXT)'
        sql = self.sql_fillter_process(sql, self.default_column)

        self.do_create_table_if_not_exists(sql)

    # create table for movie maker
    def create_table_movie_maker(self):
        sql = 'create table if not exists movie_maker(' \
              'id INTEGER PRIMARY KEY autoincrement,' \
              'movie_maker_name TEXT)'
        sql = self.sql_fillter_process(sql, self.default_column)

        self.do_create_table_if_not_exists(sql)

    # create table for movie publisher
    def create_table_movie_publisher(self):
        sql = 'create table if not exists movie_publisher(' \
              'id INTEGER PRIMARY KEY autoincrement,' \
              'movie_publisher_name TEXT)'
        sql = self.sql_fillter_process(sql, self.default_column)

        self.do_create_table_if_not_exists(sql)

    # create table for movie series
    def create_table_movie_series(self):
        sql = 'create table if not exists movie_series(' \
              'id INTEGER PRIMARY KEY autoincrement,' \
              'series_name TEXT)'
        sql = self.sql_fillter_process(sql, self.default_column)

        self.do_create_table_if_not_exists(sql)

    # create table for movie_detail_series
    def create_table_movie_detail_series(self):
        sql = 'create table if not exists movie_detail_series(' \
              'id INTEGER PRIMARY KEY autoincrement,' \
              'movie_detail_id INTEGER,' \
              'movie_series_id INTEGER)'
        sql = self.sql_fillter_process(sql, self.default_column)

        self.do_create_table_if_not_exists(sql)

    # create table for movie_tags
    def create_table_movie_tags(self):
        sql = 'create table if not exists movie_tags(' \
              'id INTEGER PRIMARY KEY autoincrement,' \
              'tags_name TEXT)'
        sql = self.sql_fillter_process(sql, self.default_column)

        self.do_create_table_if_not_exists(sql)

    # create table for movie_detail_tags
    def create_table_movie_detail_tags(self):
        sql = 'create table if not exists movie_detail_tags(' \
              'id INTEGER PRIMARY KEY autoincrement,' \
              'movie_detail_id INTEGER,' \
              'movie_tags_id INTEGER)'
        sql = self.sql_fillter_process(sql, self.default_column)

        self.do_create_table_if_not_exists(sql)

    # create table for movie detail stars info
    def create_table_movie_detail_star_info(self):
        sql = 'create table if not exists movie_detail_star_info(' \
              'id INTEGER PRIMARY KEY autoincrement,' \
              'movie_detail_id INTEGER,' \
              'star_info_id INTEGER)'
        sql = self.sql_fillter_process(sql, self.default_column)

        self.do_create_table_if_not_exists(sql)

    # create table for movie torrent
    def create_table_movie_torrent(self):
        sql = 'create table if not exists movie_torrent(' \
              'id INTEGER PRIMARY KEY autoincrement,' \
              'movie_code TEXT,' \
              'movie_url TEXT,' \
              'movie_torrent_detail_id INTEGER)'
        sql = self.sql_fillter_process(sql, self.default_column)

        index_sql = 'create index if not exists movie_torrent_movie_code_index on movie_torrent(movie_code)'
        self.do_create_table_if_not_exists(sql, index_sql)

    # create table for  torrent detail
    def create_table_torrent_detail(self):
        sql = 'create table if not exists torrent_detail(' \
              'id INTEGER PRIMARY KEY autoincrement,' \
              'movie_code TEXT,' \
              'torrent_name TEXT,' \
              'torrent_resolution TEXT,' \
              'torrent_subtitle TEXT,' \
              'torrent_movie_size TEXT,' \
              'torrent_share_date TEXT,' \
              'torrent_url TEXT)'
        sql = self.sql_fillter_process(sql, self.default_column)

        index_sql = 'create index if not exists torrent_detail_movie_code_index on torrent_detail(movie_code)'
        self.do_create_table_if_not_exists(sql, index_sql)

    # create table for movie detail torrent_detail
    def create_table_movie_torrent_detail(self):
        sql = 'create table if not exists movie_torrent_detail(' \
              'id INTEGER PRIMARY KEY autoincrement,' \
              'movie_toorent_id INTEGER,' \
              'torrent_detail_id INTEGER)'
        sql = self.sql_fillter_process(sql, self.default_column)

        self.do_create_table_if_not_exists(sql)

    # 给sql 添加一些指定的字段
    @staticmethod
    def sql_fillter_process(sql: str = None, colum_dict: [] = None):
        """
        给create sql 添加一些默认字段
        :param sql:
        :type sql:
        :param colum_dict:
        :type colum_dict:
        :return:
        :rtype:
        """
        if sql is None or colum_dict is None:
            return None
        temp_list = []
        for colum, type in colum_dict:
            temp_list.append(colum + " " + type)
        append_str = ",".join(temp_list)
        replace = sql.replace(")", "," + append_str + ")", 1)
        return replace

    def drop_table_by_table_name(self, table_name: str):
        """
        按照表名删除表
        :param table_name:
        :type table_name:
        :return:
        :rtype:
        """
        if table_name is None or table_name == "":
            return
        sql = f'drop table {table_name}'
        self.do_excute_sql_with_no_result(sql)

    def invoke_excute_method(self, method_name, *args):
        """
        反射调用创建表的方法
        :param method_name:
        :type method_name:
        :param args:
        :type args:
        :return:
        :rtype:
        """
        method_or_attribute = dir(self)
        if method_name not in method_or_attribute:
            print(f"cant invoke method on {self.__class__.__name__}")
            return
        method = getattr(self, method_name)
        method(*args)

    def init_db_tables(self):
        """
        初始化表结构
        :return:
        :rtype:
        """
        # 获取所有的表
        sql = 'select tbl_name from sqlite_master where type == "table"'
        execute = self.db_cursor.execute(sql)
        fetchall = execute.fetchall()
        exist_table = [i[0] for i in fetchall]
        print(f"start to init_db_tables......")
        method_or_attribute = dir(self)
        crate_table_methods = [i for i in method_or_attribute if i.startswith("create_table")]
        for m in crate_table_methods:
            table_name = m.replace('create_table_', '')
            if table_name in exist_table:
                continue
            self.invoke_excute_method(m)
            print(f"create table: {m.replace('create_table_', '')}")
        print(f"create tables success!")

    def drop_all_table_with_index(self):
        """
        删除表 包括表所创建的索引
        :return:
        :rtype:
        """
        print(f"start to drop all tables......")
        sql = 'select name,tbl_name from sqlite_master where type == "index"'
        self.db_cursor.execute(sql)
        fetchall = self.db_cursor.fetchall()
        if len(fetchall) == 0:
            print(f"there are no tables in local db file!")
            return
        for i, tab in fetchall:
            # print(i, tab)
            drop_index_sql = f'drop index if exists {tab}.{i}'
            self.do_excute_sql_with_no_result(drop_index_sql)
        method_or_attribute = dir(self)

        crate_table_methods = [i for i in method_or_attribute if i.startswith("create_table")]
        table_names = [i.replace("create_table_", "") for i in crate_table_methods]
        for table in table_names:
            self.drop_table_by_table_name(table)
        print(f"drop all tables success!")

    def import_actresses_to_sqlite(self):
        """
        导入actresses数据
        :return:
        :rtype:
        """
        sql = 'insert into actresses(' \
              'star_info_id,' \
              'user_name,' \
              'star_page_url,' \
              'latest_movie_url,' \
              'latest_movie_code,' \
              'latest_movie_publish_date,' \
              'latest_movie_name,' \
              'head_photo_url,' \
              'censored) values(?,?,?,?,?,?,?,?,?)'

        sql = self.add_default_column_in_insert_sql(sql, self.default_column)

        actresses_files = utils.latest_csv_pair_data_tuple_path(DATA_STORE, ACTRESSES_PATH_NAME)
        counts = 0
        for file in actresses_files:
            with open(file, 'r') as fi:
                batch_list = []
                while True:
                    readline = fi.readline()
                    if readline == "":
                        break
                    split = readline.split("|")
                    name = split[0].strip()
                    query_sql = f'select id from star_info where star_name="{name}"'
                    execute = self.db_cursor.execute(query_sql)
                    star_info_id = execute.fetchone()
                    # print(star_info_id)
                    if star_info_id is None:
                        star_info_id = -1
                    else:
                        star_info_id = star_info_id[0]
                    split.insert(0, star_info_id)
                    split.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
                    split.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
                    tuple_t = tuple(split)
                    batch_list.append(tuple_t)
                    try:
                        self.db_cursor.execute(sql, tuple_t)
                        self.db.commit()
                        counts += 1
                    except Exception as e:
                        self.db.rollback()
                        print(tuple_t)
                        print(f"insert exception: {e}")

                #     if len(batch_list) >= 10000:
                #         try:
                #             self.db_cursor.executemany(sql, batch_list)
                #             self.db.commit()
                #         except Exception as e:
                #             print(f"insert exception: {e}")
                #             self.db.rollback()
                #             batch_list = []
                #             counts += 10000
                #     else:
                #         continue
                # self.db_cursor.executemany(sql, batch_list)
                # self.db.commit()
                # counts += len(batch_list)
        print(f"插入actresses数据: {counts}条")

    def import_star_info_to_sqlite(self):
        """
        将star_info csv 文件导入到sqlite
        :return:
        :rtype:
        """
        sql = 'insert into star_info(' \
              'star_name,' \
              'star_head_photo_url,' \
              'all_item_counts,' \
              'magnet_item_counts,' \
              'censored_star,' \
              'birthday,' \
              'age,' \
              'height,' \
              'cup,' \
              'chest_circumference,' \
              'waistline,' \
              'hip_circumference,' \
              'birthplace,' \
              'habbits) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        self.import_data_csv_to_sqlite(insert_sql=sql, data_store_abs_path=STARINFO_PATH_NAME)

    # 给插入sql 设定默认行
    @staticmethod
    def add_default_column_in_insert_sql(sql: str = None, colum_dict: {} = None):
        if sql is None or colum_dict is None:
            return None

        keys = [i[0] for i in colum_dict]
        key_size = len(keys)
        append_str = ",".join(keys)
        index = sql.index(")")
        left_str = sql[:index]
        right_str = sql[index + 1:]
        left_str = left_str + "," + append_str + ")"

        end_str = ",".join(list(("?" * key_size)))
        right_str = right_str[:-1] + "," + end_str + ")"
        sql = left_str + right_str

        return sql

    def import_data_csv_to_sqlite(self, batch_count: int = 10000, insert_sql: str = None,
                                  data_store_abs_path: str = None):
        if insert_sql is None or data_store_abs_path is None:
            print("insert_sql or data_store_abs_path should not be None")
            return
        star_info_files = utils.latest_csv_pair_data_tuple_path(DATA_STORE, data_store_abs_path)
        insert_sql = self.add_default_column_in_insert_sql(insert_sql, self.default_column)
        table_name = insert_sql.replace("insert into", "").strip()
        index = table_name.index("(")
        table_name = table_name[:index]
        counts = 0
        for file in star_info_files:
            with open(file, 'r') as fi:
                batch_list = []
                while True:
                    readline = fi.readline()
                    if readline == "":
                        break
                    readline_split = readline.strip().split("|")
                    readline_split.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
                    readline_split.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
                    line_t = tuple(readline_split)
                    # try:
                    #     self.db_cursor.execute(insert_sql, line_t)
                    #     self.db.commit()
                    # except Exception as e:
                    #     print(line_t)
                    #     print(f"insert error: {e}")
                    #     self.db.rollback()

                    batch_list.append(tuple(readline_split))
                    if len(batch_list) >= batch_count:
                        try:
                            self.db_cursor.executemany(insert_sql, batch_list)
                            self.db.commit()
                        except Exception as e:
                            print(f"insert exception: {e}")
                            self.db.rollback()
                        batch_list = []
                        counts += batch_count
                    else:
                        continue
                self.db_cursor.executemany(insert_sql, batch_list)
                self.db.commit()
                counts += len(batch_list)

        print(f"成功插入{table_name}: {counts}条记录......")


if __name__ == '__main__':
    storage = SqliteStorage("javbus.db")
    # storage.init_db_tables()
    # storage.import_star_info_to_sqlite()

    # storage.import_actresses_to_sqlite()
    storage.import_movie_intro_to_sqlite()

    # storage.drop_all_table_with_index()
