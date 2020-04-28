## 这是一篇基于rasa中文的银行业务聊天机器人。本篇文章简单的实现了四个银行业务包括办卡、存钱、取钱和查询余额，同时调用第三方API实现了闲聊的功能。
## 首先安装支持该项目的包和依赖
- pip install -e .  # 下载setup.py中的需求
## 然后替换其中几个包的版本：
- pip install google-auth==1.10.1 
- prompt-toolkit==2.0.10 
- questionary==1.4.0 
- SQLAlchemy==1.3.12 
- urllib3==1.25.7
## 命令集都存储Makefile文件中
- 训练的命令:rasa train
- 初始化一个rasa框架:rasa init

