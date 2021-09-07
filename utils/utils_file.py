# -*- coding: utf-8 -*-
# @Time    : 2021/9/7 16:46
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : utils_file.py

import hashlib
import math
import os

import requests


def get_md5(filename, chunk_size: int = 100, is_chunk=False):
    md5 = hashlib.md5()
    md5_chunks = []
    with open(filename, "rb") as f:
        while True:
            file_data = f.read(1024 * 1024 * chunk_size)
            if not file_data:
                break
            md5_chunks.append(hashlib.md5(file_data).hexdigest())
            md5.update(file_data)
    if is_chunk:
        return md5.hexdigest(), md5_chunks
    else:
        return md5.hexdigest()


def get_chunk_num(filename, chunk_size):
    """获取文件分段数量"""
    # 获取文件总大小(字节)
    file_total_size = os.path.getsize(filename)
    # 分段总数
    total_chunks_num = math.ceil(file_total_size / chunk_size)
    return total_chunks_num


def do_chunk_and_upload(file_path, chunk_size):
    """将文件分段处理，并上传"""
    total_chunks_num = get_chunk_num(file_path, chunk_size)

    # 遍历
    for index in range(total_chunks_num):
        if index + 1 == total_chunks_num:
            part_size = os.path.getsize(file_path) % chunk_size
        else:
            part_size = chunk_size

        # 文件偏移量
        offset = index * chunk_size

        # 生成分片id,从1开始
        chunk_id = index + 1

        print('开始准备上传文件')
        print("分片id:", chunk_id, "文件偏移量：", offset, ",当前分片大小:", part_size, )
        # 分段上传文件
        upload(offset, chunk_id, file_path, "file_md5", "filename", part_size, total_chunks_num)


def upload(offset, chunk_id, file_path, file_md5, filename, part_size, total):
    """分次上传文件--仅作示例，没有实际接口测试"""
    url = 'http://**/file/brust/upload'
    params = {'chunk': chunk_id,
              'fileMD5': file_md5,
              'fileName': filename,
              'partSize': part_size,
              'total': total
              }
    # 根据文件路径及偏移量，读取文件二进制数据
    current_file = open(file_path, 'rb')
    current_file.seek(offset)

    files = {'file': current_file.read(part_size)}
    resp = requests.post(url, params=params, files=files).text
    print(resp)


if __name__ == '__main__':
    a = get_md5("../main.py")

    print(a)
