#!/usr/bin/python
# coding=utf-8
from com_zxl_data.JokeCommentBean import JokeCommentBean
from com_zxl_db.BaseDB import BaseDB


class JokeCommentDB(BaseDB):
    TABLE_NAME = 'joke_comment'

    COLUME_ID = 'id'
    JOKE_ID = 'joke_id'
    COLUME_ARTICLE_ID = 'article_id'
    COLUME_COMMENT_USER_ID = 'comment_user_id'
    COLUME_COMMENT_USER_IMG = 'comment_user_img'
    COLUME_COMMENT_USER_NICK_NAME = 'comment_user_nick_name'
    COLUME_COMMENT_USER_GENDER = 'comment_user_gender'
    COLUME_COMMENT_USER_AGE = 'comment_user_age'
    COLUME_COMMENT_USER_CONTENT = 'comment_user_content'
    COLUME_COMMENT_TYPE = 'comment_type'

    CREATE_TABLE_SQL = (
        "CREATE TABLE IF NOT EXISTS " + TABLE_NAME + " ("
        "  " + COLUME_ID + " bigint(20) NOT NULL AUTO_INCREMENT,"
        "  " + JOKE_ID + "  varchar(16),"
        "  " + COLUME_ARTICLE_ID + " text,"
        "  " + COLUME_COMMENT_USER_ID + " text,"
        "  " + COLUME_COMMENT_USER_IMG + " text,"
        "  " + COLUME_COMMENT_USER_NICK_NAME + " text,"
        "  " + COLUME_COMMENT_USER_GENDER + " text,"
        "  " + COLUME_COMMENT_USER_AGE + " text,"
        "  " + COLUME_COMMENT_USER_CONTENT + " text,"
        "  " + COLUME_COMMENT_TYPE + " text,"
        "  PRIMARY KEY (" + COLUME_ID + ")"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")

    INSERT_JOKE_SQL = ("INSERT INTO " + TABLE_NAME + " ("
                                                     + JOKE_ID + ","
                                                     + COLUME_ARTICLE_ID + ","
                                                     + COLUME_COMMENT_USER_ID + ","
                                                     + COLUME_COMMENT_USER_IMG + ","
                                                     + COLUME_COMMENT_USER_NICK_NAME + ","
                                                     + COLUME_COMMENT_USER_GENDER + ","
                                                     + COLUME_COMMENT_USER_AGE + ","
                                                     + COLUME_COMMENT_USER_CONTENT + ","
                                                     + COLUME_COMMENT_TYPE
                                                     + ") "
                                                     + "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

    DELETE_JOKE_SQL = ("DELETE FROM " + TABLE_NAME)

    DELETE_JOKE_SQL_BY_JOKE_ID = ("DELETE FROM " + TABLE_NAME + " WHERE " + JOKE_ID + " = '%s'")

    QUERY_JOKE_BY_ARTICLE_ID = ("SELECT "
                                 + COLUME_ID + ","
                                 + JOKE_ID + ","
                                 + COLUME_ARTICLE_ID + ","
                                 + COLUME_COMMENT_USER_ID + ","
                                 + COLUME_COMMENT_USER_IMG + ","
                                 + COLUME_COMMENT_USER_NICK_NAME + ","
                                 + COLUME_COMMENT_USER_GENDER + ","
                                 + COLUME_COMMENT_USER_AGE + ","
                                 + COLUME_COMMENT_USER_CONTENT + ","
                                 + COLUME_COMMENT_TYPE
                                 + " FROM " + TABLE_NAME
                                 + " WHERE " + COLUME_ARTICLE_ID + " = '%s'")

    def create_insert_data(self, joke_comment_bean):
        return (
            joke_comment_bean['joke_id'],
            joke_comment_bean['article_id'],
            joke_comment_bean['comment_user_id'],
            joke_comment_bean['comment_user_img'],
            joke_comment_bean['comment_user_nick_name'],
            joke_comment_bean['comment_user_gender'],
            joke_comment_bean['comment_user_age'],
            joke_comment_bean['comment_user_content'],
            joke_comment_bean['comment_type'],
        )

    def insert_joke_comment(self, joke_comment_bean):
        self.insert(self.INSERT_JOKE_SQL, self.create_insert_data(joke_comment_bean))

    def delete_joke_comment(self):
        self.delete(self.DELETE_JOKE_SQL)

    def delete_joke_comment_by_joke_id(self, joke_id):
        self.delete(self.DELETE_JOKE_SQL_BY_JOKE_ID % (joke_id,))

    def query_by_article_id(self, article_id):
        cursor = self.query(self.QUERY_JOKE_BY_ARTICLE_ID % (article_id,))

        for (COLUME_ID,
             JOKE_ID,
             COLUME_ARTICLE_ID,
             COLUME_COMMENT_USER_ID,
             COLUME_COMMENT_USER_IMG,
             COLUME_COMMENT_USER_NICK_NAME,
             COLUME_COMMENT_USER_GENDER,
             COLUME_COMMENT_USER_AGE,
             COLUME_COMMENT_USER_CONTENT,
             COLUME_COMMENT_TYPE) in cursor:
            jokeCommentBean = JokeCommentBean()
            return jokeCommentBean.create_joke_detail_bean(COLUME_ID,
                                                             JOKE_ID,
                                                             COLUME_ARTICLE_ID,
                                                             COLUME_COMMENT_USER_ID,
                                                             COLUME_COMMENT_USER_IMG,
                                                             COLUME_COMMENT_USER_NICK_NAME,
                                                             COLUME_COMMENT_USER_GENDER,
                                                             COLUME_COMMENT_USER_AGE,
                                                             COLUME_COMMENT_USER_CONTENT,
                                                             COLUME_COMMENT_TYPE)
        return None

