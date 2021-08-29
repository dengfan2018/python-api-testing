# -*- coding: utf-8 -*-
# @Time    : 2021/8/29 11:36
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : utils_data.py


import re
import random

from common.handle_conf import HandleIni
from common.handle_log import log
from common.handle_mysql import HandleMysql


prefix = [130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 145, 147, 149, 150, 151, 152, 153, 155, 156, 157, 158, 159,
          166, 171, 172, 176, 177, 178, 180, 181, 185, 186, 189,
          182, 183, 184, 187, 188, 198
          ]


def __generator_phone():
    index = random.randint(0, len(prefix) - 1)
    # 前3位
    phone = str(prefix[index])
    for _ in range(0, 8):
        # 后8位拼接前3位，生成11位手机号码
        phone += str(random.randint(0, 9))
    return phone


def get_new_phone():
    db = HandleMysql()
    while True:
        # 1生成
        phone = __generator_phone()
        # 2校验，有
        count = db.query_one(f'select * from member where mobile_phone="{phone}"')
        # 如果手机号码没有在数据库查到。表示是未注册的号码。
        if count is None:
            return phone


def get_old_phone():
    """
    从配置文件获取指定的用户名和密码
    确保此帐号，在系统当中是注册了的。
    返回：用户名和密码。
    """
    from common.handle_conf import HandleIni
    conf = HandleIni()
    user = conf.get_value("general_user", "user")
    passwd = conf.get_value("general_user", "passwd")
    return user, passwd


def data_pre(data, token=HandleIni("conf.ini").get_value("request_headers", "token")):
    """
    如果 data 是字符串，则转换成字典对象。
    """
    if data is not None and isinstance(data, str):
        # 如果有null，则替换为None
        if data.find("null") != -1:
            data = data.replace("null", "None")
        # 使用eval转成字典.eval过程中，如果表达式有涉及计算，会自动计算。
        data = eval(data)

        # 如果是v3版本，需要加上sign和timestamp2个参数。
        if HandleIni("conf.ini").get_value("request_headers", "X-Lemonban-Media-Type") == "lemonban.v3" \
                and token:
            from utils.utils_encryption import generator_sign
            sign, timestamp = generator_sign(token)
            data["sign"] = sign
            data["timestamp"] = timestamp

    return data


class EnvData:
    """
    存储用例要使用到的数据。
    """
    pass


def clear_attrs():
    # 清理 EnvData里设置的属性
    values = dict(EnvData.__dict__.items())
    for k, v in values.items():
        if k.startswith("__"):
            pass
        else:
            delattr(EnvData, k)


def replace_case_by_regular(case):
    """
    对excel当中，读取出来的整条测试用例，做全部替换。
    包括url,request_data,expected,check_sql
    """
    for key, value in case.items():
        if value is not None and isinstance(value, str):
            case[key] = replace_by_regular(value)
    log.info("正则表达式替换完成之后的请求数据：\n{}".format(case))
    return case


def replace_by_regular(data):
    """
    将字符串当中，匹配 #(.*?)# 部分，替换换对应的真实数据。
    真实数据来源 2 个地方：
        1 是配置文件当中的 data 区域
        2 是 EvnData 的类属性。
    data: 字符串
    return: 返回的是替换之后的字符串
    """
    # 如果没有找到，返回的是空列表
    res = re.findall("#(.*?)#", data)

    if res:
        for item in res:
            # 得到标识符对应的值。
            try:
                value = HandleIni("conf.ini").get_value("data", item)
            except:
                try:
                    value = getattr(EnvData, item)
                except AttributeError:
                    continue
            # 替换原字符串
            data = data.replace("#{}#".format(item), value)
    return data


def replace_mark_with_data(case, mark, real_data):
    """
    遍历一个http请求用例涉及到的所有数据，如果说每一个数据有需要替换的，都会替换。
    case: excel当中读取出来一条数据。是个字典。
    mark: 数据当中的占位符。#值#
    real_data: 要替换mark的真实数据。
    """
    for k, v in case.items():
        if v is not None and isinstance(v, str):
            if v.find(mark) != -1:
                case[k] = v.replace(mark, real_data)
    return case


if __name__ == '__main__':
    case = {
        "method": "POST",
        "url": "http://api.lemonban.com/futureloan/#phone#/member/register",
        "request_data": '{"mobile_phone": "#phone#", "pwd": "123456789", "type": 1, "reg_name": "美丽可爱的小简"}'
    }
    if case["request_data"].find("#phone#") != -1:
        case = replace_mark_with_data(case, "#phone#", "123456789001")
    for key, value in case.items():
        print(key, value)
