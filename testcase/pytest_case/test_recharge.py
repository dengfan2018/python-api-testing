# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 18:01
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : test_recharge.py

import allure
import pytest
import json

from common.handle_conf import HandleYaml, HandleIni
from common.handle_mysql import HandleMysql
from common.handle_request import req
from common.handle_log import log


cases = HandleYaml.get_data("a-recharge.yaml")
db = HandleMysql()


# @pytest.mark.skip
@allure.feature("充值")
@pytest.mark.parametrize('case', cases['parameter'])
def test_recharge(case, login):
    member_id, token = login

    HandleIni().set_value("request_headers", "token", token)

    # 替换用例中的数据
    case = HandleYaml.replace_data(case, {"member_id": member_id})

    # 数据库 - 查询当前用户的余额 - 在充值之前
    if case["check_sql"]:
        user_money_before_recharge = db.query_one(case["check_sql"])[0]
        log.info("充值前的用户余额：{}".format(user_money_before_recharge))
        recharge_money = case["request_data"]["amount"]
        log.info("充值的金额为：{}".format(recharge_money))
        expected_user_leave_amount = round(float(user_money_before_recharge) + recharge_money, 2)
        log.info("期望的充值之后的金额为：{}".format(expected_user_leave_amount))
        # 更新期望的结果 - 将期望的用户余额更新到期望结果当中。
        case = HandleYaml.replace_data(case, {"money": expected_user_leave_amount})

    # 发起请求 - 给用户充值
    response = req.send(cases["url"], cases["method"], json=case["request_data"])

    assert response.json()["code"] == int(case["expected"]["code"])
    assert response.json()["msg"] == case["expected"]["msg"]
    if case["check_sql"]:
        assert response.json()["data"]["id"] == int(case["expected"]["data"]["id"])
        assert response.json()["data"]["leave_amount"] == case["expected"]["data"]["leave_amount"]
        # 数据库 - 查询当前用户的余额
        user_money_after_recharge = db.query_one(case["check_sql"])[0]

        assert "{:.2f}".format(case["expected"]["data"]["leave_amount"]) == \
               "{:.2f}".format(float(user_money_after_recharge))

