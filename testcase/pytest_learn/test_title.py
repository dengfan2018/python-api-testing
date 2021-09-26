# -*- coding: utf-8 -*-
# @Time    : 2021/9/26 10:46
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : test_title.py
import allure
import pytest

params = [
    ("tom", "en name"),
    ("张三", "zh name")
]


# 可以读取参数化中的变量作为用例标题
@allure.title("{title}")
@pytest.mark.parametrize("name, title", params)
def test_title(name, title):
    print(f"{name} is testing {title}")
