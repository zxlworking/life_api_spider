#!/usr/bin/python
# coding=utf-8
import mysql.connector
from mysql.connector import errorcode

from com_zxl_common import LogUtils


class BaseDB:
    host = '127.0.0.1'
    port = '3306'
    # host = '103.46.128.49'
    # host = 'zxltest.zicp.vip'
    # port = '42278'
    urser_name = "root"
    pass_word = "root"
    db_name = 'life'

    CREATE_TABLE_SQL = ("")

    def __init__(self):
        global cnx
        global cursor
        try:
            cnx = mysql.connector.connect(user=self.urser_name, password=self.pass_word, host=self.host, port=self.port, database=self.db_name, charset="utf8mb4")
            cursor = cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                LogUtils.i("Something is wrong with your user name or password")
                exit(1)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                LogUtils.i("Database does not exist")
                cnx = mysql.connector.connect(user=self.urser_name, password=self.pass_word, host=self.host, port=self.port)
                cursor = cnx.cursor()
                self.__create_database()
                self.__create_table()
            else:
                LogUtils.i(err)
                exit(1)
        else:
            self.__create_table()
            LogUtils.i("DBUtil init finish")

    def __create_database(self):
        try:
            cursor.execute("CREATE DATABASE {} default character set utf8mb4 collate utf8mb4_unicode_ci".format(self.db_name))
            cnx.database = self.db_name
            LogUtils.i("Create database finish")
        except mysql.connector.Error as err:
            LogUtils.i("Failed creating database: {}".format(err))
            exit(1)

    def __create_table(self):
        # for name, ddl in CityDB.TABLES.iteritems():
        LogUtils.i("create table::" + self.CREATE_TABLE_SQL)
        try:
            LogUtils.i("Creating table {}: ".format(self.CREATE_TABLE_SQL),)
            cursor.execute(self.CREATE_TABLE_SQL)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                LogUtils.i("already exists.")
            else:
                LogUtils.i(err.msg)
                exit(1)
        else:
            print("OK")

    def query(self, sql_str):
        # LogUtils.i("query::", sql_str)
        cursor.execute(sql_str)
        return cursor

    def insert(self, sql_str, param):
        # LogUtils.i("insert::", sql_str)
        # LogUtils.i(param)
        cursor.execute(sql_str, param)
        cnx.commit()

    def update(self, sql_str):
        # LogUtils.i("update::", sql_str)
        cursor.execute(sql_str)
        cnx.commit()

    def delete(self, sql_str):
        # LogUtils.i("update::", sql_str)
        cursor.execute(sql_str)
        cnx.commit()

    def close_db(self):
        cursor.close()
        cnx.close()
