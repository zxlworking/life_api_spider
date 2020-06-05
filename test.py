#!/usr/bin/python
# coding=utf-8
import re

from com_zxl_request.QsbkDetailRequest import QsbkDetailRequest
from com_zxl_request.QsbkRequest import *

if __name__ == "__main__":
    LogUtils.i("test_main"+"xxx")
    qsbkRequest = QsbkTxtRequest()
    qsbkRequest.start_task()

    # request = QsbkDetailRequest()
    # # request.parse("https://www.qiushibaike.com/article/122197536")
    # request.parse("41", "https://www.qiushibaike.com/article/123175612")

    # str1 = 'https://pic.qiushibaike.com/system/pictures/12318/123183192/medium/article/image/CEIKU4T1IY6SPYO1'
    # str2 = 'https://pic.qiushibaike.com/article/image/CEIKU4T1IY6SPYO1'
    #
    # if 'medium/article' in str1:
    #     pattern = re.compile('system/pictures/\\d+/\\d+/medium/')
    #     str1 = pattern.sub('', str1)
    #     print(str1)
