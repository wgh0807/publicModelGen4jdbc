#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# @Time : 2020/1/16 7:09 PM
# @Author : wanggh
# @FileName : test1.py
# @Project : ModelGen

from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, DateTime, String, Table, text, create_engine
from sqlalchemy.dialects.mysql import BIGINT, LONGTEXT, TINYINT
from sqlalchemy.ext.declarative import declarative_base
import sys

#####################参数区，根据实际情况修改#######################
# 是否需要Builder 类
needBuilder = True

db_user = 'test'
db_password = 'test'
db_host = 'localhost'
db_port = '3306'

# modelPackageName model包
model_package_name = 'com.test.model'
# dbPackageName DB包
db_package_name = 'com.test.dao.db'
# repositoryPackageName repository包名称
repository_package_name = 'com.test.dao'

# 导出路径 - 请提前建立目录(文件不需要)
outputFolder = 'gen/'
# 模版文件相对目录 - 若未移动则勿动
inputFolder = 'temp'

#####################常量区域，谨慎操作##################
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
    'BigDecimal':   ' java.math.BigDecimal',
    'Date':         ' java.util.Date',
}
#####################工作区，勿动#######################
db_db = 'information_schema'
env = Environment(
    loader=FileSystemLoader(inputFolder)
)
db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(db_user, db_password, db_host, db_port, db_db)
engine = create_engine(db_url)
session = sessionmaker(bind=engine)()
metadata = declarative_base().metadata


class ModelParam(object):
    def __init__(self):
        self.needBuilder = needBuilder
        # tableName 表名称-小写
        self.tableName = ''
        # tableAlias 表别名
        self.tableAlias = ''
        # className 类名称（驼峰｜替换`_`\|每部分首字母大写）
        self.className = ''
        # classNameHump类名称2（小驼峰｜替换`_`\|除了首部分外，每部分首字母大写）
        self.classNameHump = ''
        # classComment 类注释
        self.classComment = ''
        # keyType 主键类型
        self.keyType = ''
        # keyName 主键名称
        self.keyName = ''
        # classesNames 需要引入的包
        self.classesNames = []
        # modelPackageName model包
        self.modelPackageName = model_package_name
        # dbPackageName DB包
        self.dbPackageName = db_package_name
        # repositoryPackageName repository包名称
        self.repositoryPackageName = repository_package_name
        # properties 属性列表
        self.properties = []


class Prop():
    def __init__(self):
        # item.annotation 注释内容
        self.annotation = ''
        #  item.className 属性类型
        self.className = ''
        #  item.column 表列名
        self.column = ''
        #  item.upperColumn 大写列名名称
        self.upperColumn = ''
        #  item.name 属性名称
        self.name = ''
        #  item.humpName 大驼峰属性名称
        self.humpName = ''
        #  item.defaultValue 属性默认值
        self.defaultValue = ''
        #  item.valueMethod 获取属性方法
        self.valueMethod = ''


t_COLUMNS = Table(
    'COLUMNS', metadata,
    Column('TABLE_CATALOG', String(512), nullable=False, server_default=text("''")),
    Column('TABLE_SCHEMA', String(64), nullable=False, server_default=text("''")),
    Column('TABLE_NAME', String(64), nullable=False, server_default=text("''")),
    Column('COLUMN_NAME', String(64), nullable=False, server_default=text("''")),
    Column('ORDINAL_POSITION', BIGINT(21), nullable=False, server_default=text("'0'")),
    Column('COLUMN_DEFAULT', LONGTEXT),
    Column('IS_NULLABLE', String(3), nullable=False, server_default=text("''")),
    Column('DATA_TYPE', String(64), nullable=False, server_default=text("''")),
    Column('CHARACTER_MAXIMUM_LENGTH', BIGINT(21)),
    Column('CHARACTER_OCTET_LENGTH', BIGINT(21)),
    Column('NUMERIC_PRECISION', BIGINT(21)),
    Column('NUMERIC_SCALE', BIGINT(21)),
    Column('DATETIME_PRECISION', BIGINT(21)),
    Column('CHARACTER_SET_NAME', String(32)),
    Column('COLLATION_NAME', String(32)),
    Column('COLUMN_TYPE', LONGTEXT, nullable=False),
    Column('COLUMN_KEY', String(3), nullable=False, server_default=text("''")),
    Column('EXTRA', String(30), nullable=False, server_default=text("''")),
    Column('PRIVILEGES', String(80), nullable=False, server_default=text("''")),
    Column('COLUMN_COMMENT', String(1024), nullable=False, server_default=text("''")),
    Column('GENERATION_EXPRESSION', LONGTEXT, nullable=False)
)

t_TABLES = Table(
    'TABLES', metadata,
    Column('TABLE_CATALOG', String(512), nullable=False, server_default=text("''")),
    Column('TABLE_SCHEMA', String(64), nullable=False, server_default=text("''")),
    Column('TABLE_NAME', String(64), nullable=False, server_default=text("''")),
    Column('TABLE_TYPE', String(64), nullable=False, server_default=text("''")),
    Column('ENGINE', String(64)),
    Column('VERSION', BIGINT(21)),
    Column('ROW_FORMAT', String(10)),
    Column('TABLE_ROWS', BIGINT(21)),
    Column('AVG_ROW_LENGTH', BIGINT(21)),
    Column('DATA_LENGTH', BIGINT(21)),
    Column('MAX_DATA_LENGTH', BIGINT(21)),
    Column('INDEX_LENGTH', BIGINT(21)),
    Column('DATA_FREE', BIGINT(21)),
    Column('AUTO_INCREMENT', BIGINT(21)),
    Column('CREATE_TIME', DateTime),
    Column('UPDATE_TIME', DateTime),
    Column('CHECK_TIME', DateTime),
    Column('TABLE_COLLATION', String(32)),
    Column('CHECKSUM', BIGINT(21)),
    Column('CREATE_OPTIONS', String(255)),
    Column('TABLE_COMMENT', String(2048), nullable=False, server_default=text("''"))
)


def deal_table(schema, table, t_comment):
    cols = session.query(t_COLUMNS).filter(t_COLUMNS.c.TABLE_SCHEMA == schema,
                                           t_COLUMNS.c.TABLE_NAME == table).all()
    param = ModelParam()
    param.table_name = table
    param.classComment = t_comment
    tmp_table_names = table.split('_')
    for i in tmp_table_names:
        if i is None or len(i.strip()) == 0:
            continue
        i = i.strip()
        param.className += i[0].upper()
        param.tableAlias += i[0]
        if len(i) > 1:
            param.className += i[1:]
        pass
    param.classNameHump = param.className[0].lower()
    if len(param.className) > 1:
        param.classNameHump += param.className[1:]
    for col in cols:
        column_name = col[3]
        data_type = col[7]
        column_default = col[5]
        if column_default == 'CURRENT_TIMESTAMP':
            column_default = None
        column_key = col[16]
        column_comment = col[19]
        item = Prop()
        item.annotation = column_comment
        item.column = column_name
        item.upperColumn = str(column_name).upper()
        tmp_col_names = str(column_name).split('_')
        for i in tmp_col_names:
            if i is None or len(i.strip()) == 0:
                continue
            i = i.strip()
            item.humpName += i[0].upper()
            if len(i) > 1:
                item.humpName += i[1:]
            pass
        item.name = item.humpName[0].lower()
        if len(item.humpName) > 1:
            item.name += item.humpName[1:]
        item.defaultValue = column_default
        if data_type in valueTypeMap.keys():
            item.className = valueTypeMap.get(data_type)
            item.valueMethod = valueMethodMap.get(data_type)
            if column_key == 'PRI':
                param.keyType = item.className
                param.keyName = item.name
            if item.className in valueClassMap.keys():
                param.classesNames.append(valueClassMap.get(item.className))
        else:
            item.className = data_type
            item.valueMethod = data_type
            pass
        param.properties.append(item)
        pass
    param.classesNames = list(set(param.classesNames))
    model_template = env.get_template("model.java")
    res = model_template.render(param=param)
    saveToFile(file_name=param.className + ".java", res=res)
    db_template = env.get_template("db.java")
    res = db_template.render(param=param)
    saveToFile(file_name=param.className + "DB.java", res=res)
    repository_template = env.get_template("repository.java")
    res = repository_template.render(param=param)
    saveToFile(file_name=param.className + "Repository.java", res=res)


def saveToFile(file_name, res):
    model_file = open(outputFolder+file_name, mode="w+", encoding='utf-8')
    # print(res)
    model_file.write(res)
    model_file.flush()
    model_file.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("请输入传入参数！ 库名 [表名]")
        exit(1)
    tableName = None
    schema_name = sys.argv[1]
    if len(sys.argv) > 2:
        tableName = sys.argv[2]
    if tableName is None:
        table_list = session.query(t_TABLES).filter(t_TABLES.c.TABLE_SCHEMA == schema_name).all()
    else:
        table_list = session.query(t_TABLES).filter(t_TABLES.c.TABLE_SCHEMA == schema_name,
                                                    t_TABLES.c.TABLE_NAME == tableName).all()
    for table in table_list:
        tableName = str(table[2])
        table_comment = str(table[20])
        deal_table(schema=schema_name, table=tableName, t_comment=table_comment)

    print('完成')
