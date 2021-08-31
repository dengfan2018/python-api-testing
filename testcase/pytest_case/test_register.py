# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 16:30
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : test_register.py

import allure
import pytest
from common.handle_conf import HandleYaml
from common.handle_mysql import HandleMysql
from common.handle_request import req
from utils.utils_data import get_new_phone


cases = HandleYaml.get_data("a-register.yaml")
db = HandleMysql()


@pytest.mark.skip
@allure.feature("注册")
@pytest.mark.parametrize('case', cases['parameter'])
def test_login(case):
    allure.dynamic.title(case['title'])

    case = HandleYaml.replace_data(case, {"phone": get_new_phone()})
    result = req.send(cases['url'], cases['method'], json=case['request_data'])
    print(result.json())

    for k, v in case['expected'].items():
        assert result.json()[k] == v

    if case['check_sql']:
        assert db.query_one(case["check_sql"])
