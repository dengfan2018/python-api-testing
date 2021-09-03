# -*- coding: utf-8 -*-
# @Time    : 2021/8/29 9:49
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : handle_request.py


import allure
import requests

from common.handle_log import LogHandler
from common.handle_conf import HandleIni

logger = LogHandler.log()
conf = HandleIni()


class HandleHttp:

    @staticmethod
    def __pre_url(path):
        """
        拼接接口的url地址。
        """
        base_url = conf.get("pytest", "base_url")

        if path.startswith("/"):
            return base_url + path
        elif path.startswith("http://") or path.startswith("https://"):
            return path
        else:
            return base_url + "/" + path

    @staticmethod
    def __handle_header(headers):
        """
        添加配置文件中默认的请求头，和用例中的请求头合并

        :return: 处理之后 headers 字典
        """
        h = conf.items_dict("request_headers")
        [h.pop(k) for k, v in h.copy().items() if not v]
        if headers:
            h.update(eval(headers))
        return h

    def send(self, url, method='post', params=None, data=None, json=None, headers=None, **kwargs):

        headers = self.__handle_header(headers)
        url = self.__pre_url(url)
        from utils.utils_data import data_pre
        if data:
            data = data_pre(data, conf.get("request_headers", "token"))
        if json:
            json = data_pre(json, conf.get("request_headers", "token"))

        self.create_request_log(url, method, json if json else (params if params else data), headers, **kwargs)

        try:
            result = requests.request(method=method, url=url, params=params, data=data, json=json,
                                      headers=headers, **kwargs)

            logger.info("请求url为：{}".format(url))
            logger.info("请求头为：{}".format(headers))
            logger.info("请求参数为：{}".format(json if json else (params if params else data)))
            logger.info("实际结果为：{}".format(result.text))

            self.create_response_log(result.status_code, result.text)

            return result
        except Exception as e:
            logger.error(f"------{url} 请求失败------")
            logger.error(f"request_data： {json if json else (params if params else data)}")
            logger.error(f"request_headers： {headers}")
            logger.exception(e)

    # 设置一个 allure step，可以将请求信息输出在报告中
    @allure.step("请求")
    def create_request_log(self, url, method, body, header, **kwargs):
        ...

    # 设置一个 allure step，可以将响应信息输出在报告中
    @allure.step('响应')
    def create_response_log(self, status_code, body):
        ...


req = HandleHttp()
