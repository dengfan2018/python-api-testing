# -*- coding: utf-8 -*-
# @Time    : 2021/8/29 11:25
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : test_register.py

import unittest

from ddt import ddt, data

from common.handle_request import req
from common import handle_excel
from common.handle_log import log
from common.handle_mysql import HandleMysql
from utils.utils_data import get_new_phone, replace_mark_with_data


cases = handle_excel.load_all_data_from_xls("api_cases.xlsx", "注册")

db = HandleMysql()


@unittest.skip
@ddt
class TestRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        log.info("======  注册模块用例 开始执行  ========")

    @classmethod
    def tearDownClass(cls) -> None:
        log.info("======  注册模块用例 执行结束  ========")

    @data(*cases)
    def test_register_ok(self, case):

        log.info("*********   执行用例{}：{}   *********".format(case["id"], case["title"]))

        # 替换 - 动态 -
        # 请求数据 #phone# 替换 new_phone
        # check_sql里的  #phone# 替换 new_phone
        if case["request_data"].find("#phone#") != -1:
            new_phone = get_new_phone()
            case = replace_mark_with_data(case, "#phone#", new_phone)

        # 步骤 测试数据 - 发起请求
        response = req.send(case["url"], case["method"], json=case["request_data"], headers=case['headers'])

        # 期望结果，从字符串转换成字典对象。
        expected = eval(case["expected"])

        self.assertEqual(response.json()["code"], expected["code"])
        self.assertEqual(response.json()["msg"], expected["msg"])
        # 如果check_sql有值，说明要做数据库校验。
        if case["check_sql"]:

            result = db.query_one(case["check_sql"])
            log.info(f"sql 为{case['check_sql']}")
            log.info(f"sql 结果为{result}")
            self.assertIsNotNone(result)

