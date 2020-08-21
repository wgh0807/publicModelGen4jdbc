# jdbcmodel生成工具
> 见智 & 基础库专用工具   
若有模版变化，请联系wanggh修改模版

## 20200821 修改日志
1. model 默认增加 Builder构造器
2. DB修改，减少无用的class(使用匿名类替代)。
3. DB修改，若表中int/long类型数据存储为null，之前会自动获取为0，现会获取为null( Integer / Long 类型)
4. 请注意由3修改导致的空指针问题，避免频繁拆装箱。（若需要旧版DB，则使用`temp/db_old.java` 替代 `temp/db.java`文件）


## 包依赖
1. jinja2
2. sqlAlchemy
3. pymysql
```shell
pip install jinja2
pip install sqlalchemy
pip install pymysql
```

## 使用方式
1. 使用前请确认依赖已经安装完成
2. 使用前请打开文件修改相关属性（参数区），按需要修改。
3. 设置完成后，运行程序：
    1. 进入此文件所在目录下，命令行输入：
        ```shell
        python3 test1.py 库名 [表名]
        ```
        库名为必选项，表名为可选项。请合法输入
    2. 通过pycharm执行 
        - 点击运行，输出异常信息
        - `run` - `edit configurations` - 选择当前脚本 - `parameters` 输入 `库名 [表名]`
        - 再次运行

## 注意事项
1. 迁移时请保留temp中模版，修改输入/输出目录后应确保目录已经存在，且模版位于输入目录中
2. 暂时支持的数据类型请见constant.py（该文件没有用途，不使用可删除）
3. 新增/修改类型映射关系，请修改 `常量区域`代码
4. 意见建议欢迎随时联系wgh0807@qq.com

