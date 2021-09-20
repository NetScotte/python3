# -*- coding: utf-8 -*-
"""
功能：测试mysql.connector的功能
设计：
备注： 在main函数中修改后执行
时间： 2018-07-21
"""
import pymysql


connect_info = {
    "host": "192.168.56.101",
    "user": "root",
    "password": "123lloi",
    "database": "easyflow"
}


def get_connection():
    return pymysql.connect(**connect_info)


if __name__ == "__main__":
    connection = pymysql.connect(**connect_info)
    cursor = connection.cursor()
    cursor.execute("show variables;")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    for row in result:
        print(row)

