# -*- coding: utf-8 -*-
# @Time    : 2021/8/29 9:21
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : handle_log.py

import os
import datetime

from loguru import logger


class LogHandler:
    """
    按日期创建日志文件
    info、error类型的日志分别写入不同的文件，info日志包含了error日志。
    """
    PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_PATH = os.path.join(PATH, "logs")
    today_now = f"{datetime.datetime.now().year}_{datetime.datetime.now().month}_{datetime.datetime.now().day}"
    logger.add(os.path.join(LOG_PATH, f'info_{today_now}.log'), rotation="00:01",
               format="{time:YYYY-MM-DD HH:mm:ss} {file} {line} {level} -> {message}",
               encoding="utf-8", level="INFO")
    logger.add(os.path.join(LOG_PATH, f"error_{today_now}.log"), rotation="00:01",
               format="{time:YYYY-MM-DD HH:mm:ss} {file} {line} {level} -> {message}",
               encoding="utf-8", level="ERROR")
    # logger.add(sys.stderr, format="{time:YYYY-MM-DD HH:mm:ss} {file} {line} {level} -> {message}")

    @staticmethod
    def log():
        return logger


log = LogHandler.log()


if __name__ == '__main__':
    log.info("就是这么简单，调用即可")
    log.warning("就是这么简单，调用即可")
    log.error("就是这么简单，调用即可")
    log.debug("就是这么简单，调用即可")

    # 函数可使用 @log.catch 装饰器或者  log.exception 输出错误日志，可以精确的知道是哪行代码出了问题

    # 捕捉函数运行过程中的错误，输出日志
    @log.catch
    def my_function(x, y, z):
        # 没有使用 try 不需要额外输出错误，只使用装饰器即可
        return 1 / (x + y + z)


    my_function(0, 0, 0)


    def mistake(a, b):
        # 如果使用了 try 就需要使用 log.exception 输出
        try:
            print(a / b)
        except ZeroDivisionError:
            # 将捕获到的错误输出
            log.exception("?")


    mistake(1, 0)
