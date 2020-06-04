#!/usr/bin/python
# coding=utf-8
import re

from com_zxl_request.QsbkDetailRequest import QsbkDetailRequest
from com_zxl_request.QsbkTxtRequest import *

if __name__ == "__main__":
    LogUtils.i("test_main"+"xxx")
    qsbkRequest = QsbkTxtRequest()
    qsbkRequest.start_task()

    # request = QsbkDetailRequest()
    # # request.parse("https://www.qiushibaike.com/article/122197536")
    # request.parse("41", "https://www.qiushibaike.com/article/123175612")
#     https://pic.qiushibaike.com/system/avtnew/3302/33028477/medium/20200501023523.jpg
#     https://pic.qiushibaike.com/system/avtnew/2841/28413052/medium/201610032055070.JPEG
