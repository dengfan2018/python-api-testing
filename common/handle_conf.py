# -*- coding: utf-8 -*-
# @Time    : 2021/8/29 9:24
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : handle_conf.py
import json
import os
import configparser
from string import Template

from ruamel.yaml import YAML

from common import handle_path as project


class HandleIni(configparser.ConfigParser):
    """用来操作.ini格式的配置文件
    """

    def __init__(self, filename="conf.ini", parent=project.conf_dir, interpolation=configparser.ExtendedInterpolation()):
        """
        继承 ConfigParser 类，并指定 self._interpolation 以支持
        :param filename:
        :param parent:
        :param interpolation:
        """
        super(HandleIni, self).__init__()
        self._interpolation = interpolation
        self.conf_path = parent.joinpath(filename)
        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("配置文件不存在！")

        self.read(self.conf_path, encoding="utf-8")

    def items_dict(self, section):
        """
        获取 section 下全部的值，返回字典形式"
        :param section: 
        :return: 
        """""
        return dict(self.items(section))

    def set_value(self, section, option, value):
        """设置配置文件中section下option的值"""
        self.set(section, option, value)
        with open(self.conf_path, "w", encoding="utf8") as f:
            self.write(f)

    def add_section(self, section):
        """在配置文件添加section"""
        self.add_section(section)
        with open(self.conf_path, "w", encoding="utf8") as f:
            self.write(f)


class HandleYaml:
    """用来操作 yaml 格式的配置文件/测试数据
    """

    @staticmethod
    def get_data(filename, parent=project.casedatas_dir):
        yaml = YAML(typ='safe')
        return yaml.load(parent.joinpath(filename))

    @staticmethod
    def replace_data(source_data: str or dict, replace_data: dict):
        if isinstance(source_data, dict):
            source_data = json.dumps(source_data)
        data = Template(source_data).safe_substitute(replace_data)
        return json.loads(data)


class GetYaml:
    """获取 yaml 文件中的数据
    通过类属性的方式调用
    """

    def __init__(self, filename, parent=project.casedatas_dir):
        self.filename = filename
        self.parent = parent
        self.yaml = YAML(typ='safe')
        self._data = None

    @property
    def data(self):
        if self._data is None:
            return self.yaml.load(self.parent.joinpath(self.filename))
        return self._data


if __name__ == '__main__':
    cases = HandleYaml.get_data("a-register.yaml")
    # print(cases)

    cases2 = GetYaml("a-register.yaml").data
    print(cases2)

    print(HandleIni("conf.ini").get("request_headers", "token"))
    print(HandleIni("conf.ini").get("request_headers", "authorization"))
    print(HandleIni("conf.ini").items("data"))


