# -*- coding: utf-8 -*-
# @Time    : 2021/8/29 19:33
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : test_recharge.py


import unittest
import json
from jsonpath import jsonpath
from ddt import ddt, data

from common.handle_request import req
from common import handle_excel
from common import handle_path as project
from common.handle_log import log
from common.handle_conf import HandleIni
from common.handle_mysql import HandleMysql
from utils.utils_data import replace_case_by_regular, EnvData, clear_attrs, get_old_phone

cases = handle_excel.load_all_data_from_xls('api_cases.xlsx', "充值")

conf = HandleIni()
db = HandleMysql()


# @unittest.skip
@ddt
class TestRecharge(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # 清理 EnvData里设置的属性
        clear_attrs()

        # 得到登陆的用户名和密码
        user, passwd = get_old_phone()

        # 登陆
        resp = req.send("member/login", "POST", json={"mobile_phone": user, "pwd": passwd})

        # 获取登录的 token 和 member_id
        setattr(EnvData, "member_id", str(jsonpath(resp.json(), "$..id")[0]))
        setattr(EnvData, "token", jsonpath(resp.json(), "$..token")[0])
        conf.set_value("request_headers", "token", jsonpath(resp.json(), "$..token")[0])

    def tearDown(self) -> None:
        if hasattr(EnvData, "money"):
            delattr(EnvData, "money")

    @data(*cases)
    def test_recharge(self, case):
        # 替换的数据
        if case["request_data"].find("#member_id#") != -1:
            case = replace_case_by_regular(case)

        # 数据库 - 查询当前用户的余额 - 在充值之前
        if case["check_sql"]:
            user_money_before_recharge = db.query_one(case["check_sql"])[0]
            log.info("充值前的用户余额：{}".format(user_money_before_recharge))
            # 期望的用户余额。 充值之前的余额 + 充值的钱
            recharge_money = json.loads(case["request_data"])["amount"]
            log.info("充值的金额为：{}".format(recharge_money))
            expected_user_leave_amount = round(float(user_money_before_recharge) + recharge_money, 2)
            log.info("期望的充值之后的金额为：{}".format(expected_user_leave_amount))
            setattr(EnvData, "money", str(expected_user_leave_amount))
            # 更新期望的结果 - 将期望的用户余额更新到期望结果当中。
            case = replace_case_by_regular(case)

        # 发起请求 - 给用户充值
        response = req.send(case["url"], case["method"],  json=case["request_data"])

        # 将期望的结果转成字典对象，再去比对
        expected = json.loads(case["expected"])

        # 断言
        try:
            self.assertEqual(response.json()["code"], expected["code"])
            self.assertEqual(response.json()["msg"], expected["msg"])
            if case["check_sql"]:
                self.assertEqual(response.json()["data"]["id"], expected["data"]["id"])
                self.assertEqual(response.json()["data"]["leave_amount"], expected["data"]["leave_amount"])
                # 数据库 - 查询当前用户的余额
                user_money_after_recharge = db.query_one(case["check_sql"])[0]

                self.assertEqual("{:.2f}".format(expected["data"]["leave_amount"]),
                                 "{:.2f}".format(float(user_money_after_recharge)))
        except:
            log.error("断言失败！")
            raise
