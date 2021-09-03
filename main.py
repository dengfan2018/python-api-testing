# -*- coding: utf-8 -*-
# @Time    : 2021/8/29 12:17
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : main.py

import os
import unittest

from BeautifulReport import BeautifulReport

from common.handle_path import reports_dir_html, cases_dir_unittest
from common.handle_path import *


test_type = "pytest"


if __name__ == '__main__':
    if test_type == "unittest":
        test_suite = unittest.defaultTestLoader.discover(cases_dir_unittest, pattern='test*.py')
        result = BeautifulReport(test_suite)
        result.report(filename='测试报告', description='测试deafult报告', log_path=reports_dir_html)
    elif test_type == "pytest":
        os.system(f"pytest -s -v --alluredir={reports_dir_allure_temp} --clean-alluredir")
        os.system(f"allure generate -c -o {reports_dir_allure_html} {reports_dir_allure_temp}")
