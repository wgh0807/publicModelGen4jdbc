#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# @Time : 2020/1/16 7:09 PM
# @Author : wanggh
# @FileName : __init__.py.py
# @Project : ModelGen

import pymysql


class SqlCursor():
    def __init__(self, host, port, user, password, db, charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.conn = pymysql.Connect(host=host, port=port, user=user, password=password, db=db, charset=charset)

    def getCursor(self):
        return self.conn.cursor()


valueTypeMap = {
    # String 类型
    "varchar": "String",
    "char": "String",
    "tinytext": "String",
    "text": "String",
    # 二进制类型
    "blob": "Byte[]",
    # 数值类型
    "integer": "Long",
    "int": "Integer",
    "tinyint": "Integer",
    "smallint": "Integer",
    "mediumint": "Integer",
    "bit": "Boolean",
    # "BIGINT", "BigInteger",
    "bigint": "Long",
    "float": "Float",
    "double": "Double",
    "decimal": "BigDecimal",
    # 布尔类型
    "boolean": "Boolean",
    # 时间类型
    "date": "Date",
    "time": "Date",
    "datetime": "Date",
    "timestamp": "Date",
    "year": "Date",

    # 未知
    "enum": "String",
    "longblob": "Byte[]",
    "longtext": "String",

}

valueMethodMap = {
    # String 类型
    "varchar": "getString",
    "char": "getString",
    "tinytext": "getString",
    "text": "getString",
    # 二进制类型
    "blob": "getBlob",
    # 数值类型
    "integer": "getLong",
    "int": "getInt",
    "tinyint": "getInt",
    "smallint": "getInt",
    "mediumint": "getInt",
    "bit": "getBoolean",
    "bigint": "getLong",
    "float": "getFloat",
    "double": "getDouble",
    "decimal": "getBigDecimal",
    # 布尔类型
    "boolean": "getBoolean",
    # 时间类型
    "date": "getTimestamp",
    "time": "rs.getTimestamp",
    "datetime": "getTimestamp",
    "timestamp": "getTimestamp",
    "year": "getTimestamp",
    # 其他
    "enum": "getString",
    "longblob": "getBlob",
    "longtext": "getString",
}
valueClassMap = {
    'BigDecimal':   ' java.math.BigDecimal;',
    'Date':         ' java.util.Date;',
}
