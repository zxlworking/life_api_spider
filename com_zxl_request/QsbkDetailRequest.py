#!/usr/bin/python
# coding=utf-8
import datetime
import json
import re

from selenium.common.exceptions import NoSuchElementException

from com_zxl_common import LogUtils
from com_zxl_data.JokeCommentBean import JokeCommentBean
from com_zxl_data.JokeDetailBean import JokeDetailBean
from com_zxl_db.JokeCommentDB import JokeCommentDB
from com_zxl_db.JokeDetailDB import JokeDetailDB
from com_zxl_db.JokeDetailErrorDB import JokeDetailErrorDB
from com_zxl_request.BaseRequest import BaseRequest


class QsbkDetailRequest(BaseRequest):

    def __init__(self):
        global jokeDB
        global jokeCommentDB
        global jokeDetailErrorDB
        jokeDB = JokeDetailDB()
        jokeCommentDB = JokeCommentDB()
        jokeDetailErrorDB = JokeDetailErrorDB()
        # jokeDB.delete_joke_detail()

    def parse(self, joke_id, url):
        LogUtils.i("parse::joke_id = " + joke_id)
        LogUtils.i("parse::url = " + url)

        article_id = -1
        find_article_id_result_array = re.findall(".*?(\d+).*?", url)
        if len(find_article_id_result_array) > 0:
            article_id = int(find_article_id_result_array[0])
        LogUtils.i("id = " + str(article_id))

        driver = self.get_web_content(url)

        page_source = driver.page_source
        LogUtils.i(page_source)

        try:
            stats_time_path = '//span[@class="stats-time"]'
            stats_time_object = driver.find_element_by_xpath(stats_time_path)
            stats_time = stats_time_object.text

            content_parent_path = '//div[@class="article block untagged noline"]'
            content_parent_object = driver.find_element_by_xpath(content_parent_path)

            content_object = content_parent_object.find_element_by_xpath('.//div[@class="content"]')
            content = content_object.text

            thumb_img_url = ''
            try:
                thumb_object = content_parent_object.find_element_by_xpath('.//div[@class="thumb"]')
                thumb_img_object = thumb_object.find_element_by_xpath('.//img')
                thumb_img_url = thumb_img_object.get_attribute('src')
            except NoSuchElementException as e:
                LogUtils.i(e.msg)

            LogUtils.i(article_id)
            LogUtils.i(stats_time)
            LogUtils.i(content)
            LogUtils.i(thumb_img_url)

            jokeDetailBean = JokeDetailBean()
            jokeDetailBean = jokeDetailBean.create_joke_detail_bean(
                "",
                joke_id,
                article_id,
                stats_time,
                content,
                thumb_img_url
            )

            jokeDB.delete_joke_detail_by_joke_id(joke_id)
            jokeDB.insert_joke_detail(jokeDetailBean)
            jokeDetailErrorDB.delete_joke_detail_by_joke_id(joke_id)

            jokeCommentDB.delete_joke_comment_by_joke_id(joke_id)
            self.parse_comment(joke_id, article_id, 0, 10)
        except NoSuchElementException as e:
            LogUtils.i(e.msg)

            jokeDetailBean = JokeDetailBean()
            jokeDetailBean = jokeDetailBean.create_joke_detail_bean(
                "",
                joke_id,
                article_id,
                '',
                '',
                ''
            )
            jokeDetailErrorDB.delete_joke_detail_by_joke_id(joke_id)
            jokeDetailErrorDB.insert_joke_detail(jokeDetailBean)

        driver.close()

    def parse_comment(self, joke_id, article_id, current_page, page_size):
        # https://www.qiushibaike.com/commentpage/122204240?page=1&count=10
        LogUtils.i("parse_comment::current_page = " + str(current_page) + "::page_size = " + str(page_size))
        # https://www.qiushibaike.com/commentpage/122204240?page=2&count=10
        url = "https://www.qiushibaike.com/commentpage/" + str(article_id) + "?page=" + str(current_page) + "&count=" + str(page_size)
        LogUtils.i("parse_comment::url = " + url)
        driver = self.get_web_content(url)

        total_count = 0

        try:
            page_source = driver.page_source
            LogUtils.i(page_source)

            comment_path = '//pre'
            comment_object = driver.find_element_by_xpath(comment_path)

            # "err": 0,
            # "comments": {
            #     "count": 10,
            #     "items": Array[9],
            #     "total": 58,
            #     "page": 0
            # }
            comment_json = json.loads(comment_object.text)
            error_code = comment_json['err']
            LogUtils.i("parse_comment::error_code = " + str(error_code))

            page_size = int(comment_json['comments']['count'])
            total_count = int(comment_json['comments']['total'])
            current_page = int(comment_json['comments']['page'])

            LogUtils.i("parse_comment::total_count = " + str(total_count))

            comment_items = comment_json['comments']['items']
            for comment_item in comment_items:
                # "status":"publish",
                # "uid":31265504,
                # "pos":0,
                # "avatar_file_name":"20160223143723.jpg",
                # "rank":108,
                # "anonymous":0,
                # "id":407134850,
                # "neg":0,
                # "age":23,
                # "role_id":0,
                # "content":"生活总是为难人",
                # "gender":"F",
                # "login":"╰亿.╭ァPing"
                comment_user_id = comment_item['uid']
                # https://pic.qiushibaike.com/system/avtnew/3126/31265504/medium/20160223143723.jpg
                comment_user_id_str = str(comment_user_id)
                str_length = len(comment_user_id_str) // 2
                comment_user_id_str = comment_user_id_str[0:str_length]
                comment_user_img = "https://pic.qiushibaike.com/system/avtnew/" + comment_user_id_str + "/" + str(comment_user_id) + "/medium/" + comment_item['avatar_file_name']
                comment_user_nick_name = comment_item['login']
                comment_user_gender = comment_item['gender']
                comment_user_age = comment_item['age']
                comment_user_content = comment_item['content']

                LogUtils.i("parse_comment::comment_user_id = " + str(comment_user_id))
                LogUtils.i("parse_comment::comment_user_img = " + comment_user_img)
                LogUtils.i("parse_comment::comment_user_nick_name = " + comment_user_nick_name)
                LogUtils.i("parse_comment::comment_user_gender = " + comment_user_gender)
                LogUtils.i("parse_comment::comment_user_age = " + str(comment_user_age))
                LogUtils.i("parse_comment::comment_user_content = " + comment_user_content)

                jokeCommentBean = JokeCommentBean()
                jokeCommentBean = jokeCommentBean.create_joke_comment_bean("",
                                                         joke_id,
                                                         article_id,
                                                         str(comment_user_id),
                                                         comment_user_img,
                                                         comment_user_nick_name,
                                                         comment_user_gender,
                                                         str(comment_user_age),
                                                         comment_user_content,
                                                         current_page)
                jokeCommentDB.insert_joke_comment(jokeCommentBean)
        except Exception as e:
            LogUtils.e(e)

        driver.close()

        LogUtils.i('\n')
        LogUtils.i('======================================parse_comment page end==========================================')
        LogUtils.i('\n')

        if page_size > 0:
            total_page = total_count // page_size
            if total_count % page_size != 0:
                total_page = total_page + 1
            LogUtils.i("parse_comment::total_page = " + str(total_page))

            if current_page < total_page:
                self.parse_comment(joke_id, article_id, current_page + 1, page_size)



    def get_detail(self, joke_id, url):
        LogUtils.i("start_task::" + 'Now Time::' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.parse(joke_id, url)


if __name__ == "__main__":
    request = QsbkDetailRequest()
    # request.parse("https://www.qiushibaike.com/article/122197536")
    request.parse("", "https://www.qiushibaike.com/article/122204240")
