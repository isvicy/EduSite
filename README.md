### Django EduSite Demo

- 根据慕课网教程做成的教育类网站，基于Django1.11与python3.6.4，已完成基本功能，待后续改进。
- 已经部署到腾讯云: [EduSite](http://www.djangoflask.cn)

#### 使用方法：
1. `git clone https://github.com/bryceyang/EduSite.git`

2. 新建一个python3虚拟环境，然后安装依赖包。
```pip install -r requirement.txt```

3. 设置setting文件中用到的一些环境变量，比如数据库相关以及邮发送相关

4. 执行初始数据库迁移过程:
```python
python manage.py makemigrations
python manage.py migrate
```

5. 启动
```python
python manage.py runserver
```
