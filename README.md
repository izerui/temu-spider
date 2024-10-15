# temu 网络爬虫

1. 初始化 python 虚拟环境: 
   * `python3 -m venv temu-spider/venv`
2. 并切换到当前环境, windows 下自行google。
   * `cd temu-spider && source ./venv/bin/activate`
3. 安装依赖
   * `pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple/`
   * `pip install fastapi`
   * `pip install pytest-playwright`
   * `pip install pyinstaller`
   * `pip install PySide6`
4. 启动应用: 
   * `uvicorn main:app --host 0.0.0.0 --timeout-keep-alive 60 --workers 1`



附:

依赖管理:
```
# 安装依赖
pip install -r requirements.txt
# 生成依赖描述文件
pip freeze > requirements.txt
```

附录:
https://playwright.dev/python/docs/api/class-page#events
https://playwright.nodejs.cn/docs/intro
