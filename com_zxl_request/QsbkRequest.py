#!/usr/bin/python
# coding=utf-8
import datetime
import hashlib
import re

from selenium.common.exceptions import NoSuchElementException

from com_zxl_common import LogUtils
from com_zxl_data.JokeBean import JokeBean
from com_zxl_db.JokeDB import JokeDB
from com_zxl_db.JokeDetailDB import JokeDetailDB
from com_zxl_request.BaseRequest import BaseRequest
from com_zxl_request.QsbkDetailRequest import QsbkDetailRequest


class QsbkTxtRequest(BaseRequest):

    def __init__(self):
        global jokeDB
        jokeDB = JokeDB()
        # jokeDB.delete_joke()

    def parse(self, url_path):
        LogUtils.i("parse::url_path = " + url_path)

        driver = self.get_web_content("https://www.qiushibaike.com/" + url_path)
        page_source = driver.page_source
        LogUtils.i("parse::page_source::\n")
        LogUtils.i(page_source)

        text_joke_item_path = "//div[starts-with(@class,'article block untagged mb15')]"
        text_joke_items = driver.find_elements_by_xpath(text_joke_item_path)

        LogUtils.i('text_joke_items length = ' + str(len(text_joke_items)))

        for text_joke_item in text_joke_items:
            joke_id = text_joke_item.get_attribute('id')
            md5_object = hashlib.md5()
            md5_object.update(joke_id.encode('utf-8'))
            joke_md5_value = md5_object.hexdigest()

            author_object = text_joke_item.find_element_by_xpath('.//div[@class="author clearfix"]')
            author_nick_object = author_object.find_element_by_xpath('.//h2')
            author_nick_name = author_nick_object.text
            author_img_object = author_object.find_element_by_xpath('.//img')
            author_img_url = author_img_object.get_attribute('src')

            author_gender = ''
            author_age = -1
            try:
                author_gender_object = author_object.find_element_by_xpath(".//div[starts-with(@class,'articleGender')]")
                author_gender = author_gender_object.get_attribute('class')
                author_age = author_gender_object.text
            except NoSuchElementException as e:
                LogUtils.i(e.msg)

            content_object = text_joke_item.find_element_by_xpath('.//div[@class="content"]')
            content = content_object.text

            thumb_img_url = ''
            try:
                thumb_object = text_joke_item.find_element_by_xpath('.//div[@class="thumb"]')
                thumb_img_object = thumb_object.find_element_by_xpath('.//img')
                thumb_img_url = thumb_img_object.get_attribute('src')
            except NoSuchElementException as e:
                LogUtils.i(e.msg)

            stats_vote_content = ''
            stats_comment_content = ''
            stats_comment_detail_url = ''
            try:
                stats_object = text_joke_item.find_element_by_xpath('.//div[@class="stats"]')
                try:
                    stats_vote_object = stats_object.find_element_by_xpath('.//span[@class="stats-vote"]')
                    stats_vote_content = stats_vote_object.text
                except NoSuchElementException as e:
                    LogUtils.i(e.msg)
                try:
                    stats_comment_object = stats_object.find_element_by_xpath('.//span[@class="stats-comments"]')
                    stats_comment_content = stats_comment_object.find_element_by_xpath('.//a[@class="qiushi_comments"]').text
                    stats_comment_detail_url = stats_comment_object.find_element_by_xpath(
                        './/a[@class="qiushi_comments"]').get_attribute('href')
                except NoSuchElementException as e:
                    LogUtils.i(e.msg)
            except NoSuchElementException as e:
                LogUtils.i(e.msg)

            LogUtils.i(author_nick_name)
            LogUtils.i(author_gender)
            LogUtils.i(author_age)
            LogUtils.i(author_img_url)
            LogUtils.i(content)
            LogUtils.i(thumb_img_url)
            LogUtils.i(stats_vote_content)
            LogUtils.i(stats_comment_content)
            LogUtils.i(stats_comment_detail_url)
            LogUtils.i(joke_id)
            LogUtils.i(joke_md5_value)

            LogUtils.i('\n')
            LogUtils.i('======================================text_joke_item end==========================================')
            LogUtils.i('\n')

            joke_bean = JokeBean()
            joke_bean = joke_bean.create_joke_bean(
                "",
                author_nick_name.encode('utf-8'),
                author_gender,
                author_age,
                author_img_url,
                content.encode('utf-8'),
                thumb_img_url,
                stats_vote_content,
                stats_comment_content,
                stats_comment_detail_url,
                joke_md5_value)

            is_exist_joke_item = jokeDB.query_by_md5(joke_md5_value)
            LogUtils.i(is_exist_joke_item)
            if is_exist_joke_item is None:
                LogUtils.i("not ExistJokeItem")
                jokeDB.insert_joke(joke_bean)
            else:
                LogUtils.i("ExistJokeItem")
                driver.close()

            current_joke_item = jokeDB.query_by_md5(joke_md5_value)
            jokeDetailDB = JokeDetailDB()

            find_article_id_result_array = re.findall(".*?(\d+).*?", current_joke_item['stats_comment_detail_url'])
            if len(find_article_id_result_array) > 0:
                article_id = int(find_article_id_result_array[0])
                LogUtils.i("id = " + str(article_id))
                jokeDetailBean = jokeDetailDB.query_by_article_id(str(article_id))
                if jokeDetailBean is None:
                    qsbkDetailRequest = QsbkDetailRequest()
                    qsbkDetailRequest.get_detail(str(current_joke_item['id']), current_joke_item['stats_comment_detail_url'])

            if is_exist_joke_item is not None:
                return

        LogUtils.i("==============parse end=================")
        LogUtils.i("\n")

        driver.close()

    def close_db(self):
        if jokeDB is not None:
            jokeDB.close_db()

    def start_task(self):
        LogUtils.i("start_task::" + 'Now Time::' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.parse("text")
        self.parse("imgrank")
        self.close_db()


if __name__ == "__main__":
    request = QsbkTxtRequest()
    request.parse("text")

    request.close_db()
