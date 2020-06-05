#!/usb/bin/python
# coding=utf-8
import sched
import time

from com_zxl_request.QsbkRequest import QsbkTxtRequest

s = sched.scheduler(time.time, time.sleep)


def start():
    s.enter(3600, 1, start_qsbk_hot_pic_spider, ())
    s.run()


def start_qsbk_hot_pic_spider():
    # request = QsbkTxtRequest()
    # request.start_task()
    start()


if __name__ == '__main__':
    start()
    # qsbkRequest = QsbkTxtRequest()
    # qsbkRequest.start_task()
