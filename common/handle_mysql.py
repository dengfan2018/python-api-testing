# -*- coding: utf-8 -*-
# @Time    : 2021/8/29 9:54
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : handle_mysql.py


import pymysql

from common.handle_conf import HandleIni


class HandleMysql:

    def __init__(self, db_config=HandleIni("conf.ini").items_dict("mysql")):
        db_config['port'] = int(db_config['port'])
        self.connection = pymysql.connect(**db_config)
        # self.connection.autocommit(True)
        self.cursor = self.connection.cursor()

    def query_all(self, sql):
        self.connection.commit()
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def query_one(self, sql):
        self.connection.commit()
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def query_many(self, sql, num):
        self.connection.commit()
        self.cursor.execute(sql)
        return self.cursor.fetchmany(num)

    def update_db(self, sql):
        self.connection.commit()
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()

    def __del__(self):
        """
        MysqlHandler 实例对象被释放时调用此方法,用于关闭 cursor 和 connection 连接
        """
        # print("close!!!")
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    # 初始化数据库对象
    from common.handle_conf import HandleIni

    db = HandleMysql()

    sql1 = 'select CAST(member.leave_amount AS CHAR) as leave_amount from member where id=123654130;'

    count = db.query_one(sql1)[0]
    print("获取到的结果为：", (count))
