#!/usr/bin/python
# coding=utf-8

# 获取logger实例，如果参数为空则返回root logger
import logging
import sys
import time
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()

# 指定logger输出格式
formatter = logging.Formatter('%(message)s')

# 定义一个logger并设置文件输出方法
#定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
file_handler = RotatingFileHandler('myapp_log.txt', maxBytes=10*1024*1024, backupCount=5)
# 设置改显示或者写入的等级。
file_handler.setLevel(logging.INFO)
# 最后进行绑定输出格式
file_handler.setFormatter(formatter)

# # 文件日志
# file_handler = logging.FileHandler("test.log")
# file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.INFO)

def i(msg):
    time_now = time.strftime("%Y-%m-%d %H:%M:%S: ", time.localtime())
    # logger.info(time_now)
    if msg is None:
        logger.info(time_now+"===msg none===")
    else:
        logger.info(time_now+str(msg))

def e(msg):
    time_now = time.strftime("%Y-%m-%d %H:%M:%S: ", time.localtime())
    # logger.info(time_now)
    if msg is None:
        logger.info(time_now+"===msg none===", exc_info=True)
    else:
        logger.info(time_now+str(msg), exc_info=True)