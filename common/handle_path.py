# -*- coding: utf-8 -*-
# @Time    : 2021/8/29 9:14
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : handle_path.py

from pathlib import Path


base_dir = Path(__file__).resolve().parent.parent


# 测试数据路径
casedatas_dir = base_dir.joinpath("testcasedatas")

# 测试用例的路径
cases_dir_unittest = str(base_dir.joinpath("testcase", "unittest_case"))
cases_dir_pytest = str(base_dir.joinpath("testcase", "pytest_case"))

# 测试报告的路径
reports_dir_html = str(base_dir.joinpath("reports", "html"))
reports_dir_allure_temp = str(base_dir.joinpath("reports", "allure"))
reports_dir_allure_html = str(base_dir.joinpath("reports", "allure-html"))

# 日志的路径
logs_dir = base_dir.joinpath("logs")

# 配置文件路径
conf_dir = base_dir.joinpath("conf")
