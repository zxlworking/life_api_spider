#!/usr/bin/python
# coding=utf-8
from com_zxl_data.JokeDetailBean import JokeDetailBean
from com_zxl_db.BaseDB import BaseDB


class JokeDetailDB:

    TABLE_NAME = 'joke_detail'

    COLUME_ID = 'id'
    JOKE_ID = 'joke_id'
    COLUME_ARTICLE_ID = 'article_id'
    COLUME_STATS_TIME = 'stats_time'
    COLUME_CONTENT = 'content'
    COLUME_THUMB_IMG_URL = 'thumb_img_url'

    CREATE_TABLE_SQL = (
        "CREATE TABLE IF NOT EXISTS " + TABLE_NAME + " ("
        "  " + COLUME_ID + " bigint(20) NOT NULL AUTO_INCREMENT,"
        "  " + JOKE_ID + "  varchar(16),"
        "  " + COLUME_ARTICLE_ID + " text,"
        "  " + COLUME_STATS_TIME + " text,"
        "  " + COLUME_CONTENT + " text,"
        "  " + COLUME_THUMB_IMG_URL + " text,"
        "  PRIMARY KEY (" + COLUME_ID + ")"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")

    INSERT_JOKE_SQL = ("INSERT INTO " + TABLE_NAME + " ("
                                                     + JOKE_ID + ","
                                                     + COLUME_ARTICLE_ID + ","
                                                     + COLUME_STATS_TIME + ","
                                                     + COLUME_CONTENT + ","
                                                     + COLUME_THUMB_IMG_URL
                                                     + ") "
                                                     + "VALUES (%s, %s, %s, %s, %s)")

    DELETE_JOKE_SQL = ("DELETE FROM " + TABLE_NAME)

    DELETE_JOKE_SQL_BY_JOKE_ID = ("DELETE FROM " + TABLE_NAME + " WHERE " + JOKE_ID + " = '%s'")

    QUERY_JOKE_BY_ARTICLE_ID = ("SELECT "
                         + COLUME_ID + ","
                         + JOKE_ID + ","
                         + COLUME_ARTICLE_ID + ","
                         + COLUME_STATS_TIME + ","
                         + COLUME_CONTENT + ","
                         + COLUME_THUMB_IMG_URL
                         + " FROM " + TABLE_NAME
                         + " WHERE " + COLUME_ARTICLE_ID + " = '%s'")

    def __init__(self):
        global mDB
        mDB = BaseDB()
        mDB.create_table(self.CREATE_TABLE_SQL)
        print("JokeDetailDB::__init__")
        print(mDB)

    def create_insert_data(self, joke_detail_bean):
        return (
            joke_detail_bean['joke_id'],
            joke_detail_bean['article_id'],
            joke_detail_bean['stats_time'],
            joke_detail_bean['content'],
            joke_detail_bean['thumb_img_url'],
        )

    def insert_joke_detail(self, joke_detail_bean):
        mDB.insert(self.INSERT_JOKE_SQL, self.create_insert_data(joke_detail_bean))

    def delete_joke_detail(self):
        mDB.delete(self.DELETE_JOKE_SQL)

    def delete_joke_detail_by_joke_id(self, joke_id):
        mDB.delete(self.DELETE_JOKE_SQL_BY_JOKE_ID % (joke_id,))

    def query_by_article_id(self, article_id):
        cursor = mDB.query(self.QUERY_JOKE_BY_ARTICLE_ID % (article_id,))

        for (COLUME_ID,
             JOKE_ID,
             COLUME_ARTICLE_ID,
             COLUME_STATS_TIME,
             COLUME_CONTENT,
             COLUME_THUMB_IMG_URL) in cursor:
            jokeDetailBean = JokeDetailBean()
            return jokeDetailBean.create_joke_detail_bean(COLUME_ID,
                                                     JOKE_ID,
                                                     COLUME_ARTICLE_ID,
                                                     COLUME_STATS_TIME,
                                                     COLUME_CONTENT,
                                                     COLUME_THUMB_IMG_URL)
        return None
