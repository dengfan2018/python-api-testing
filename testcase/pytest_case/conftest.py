# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 16:31
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : conftest.py
import jsonpath
import pytest

from common.handle_conf import HandleYaml
from common.handle_request import req


@pytest.fixture(scope="session")
def login():
    cases = HandleYaml.get_data("a-login.yaml")
    res = req.send(cases['url'], cases['method'], json=cases['parameter'][0]['request_data'])
    member_id = jsonpath.jsonpath(res.json(), "$..id")[0]
    token = jsonpath.jsonpath(res.json(), "$..token")[0]
    yield member_id, token
