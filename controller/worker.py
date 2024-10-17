import logging

from PySide6.QtCore import QThread, Signal
from playwright._impl._errors import TargetClosedError, TimeoutError
from playwright.sync_api import Response, Frame, sync_playwright, Browser, Page, BrowserContext
from sqlalchemy import text

from controller.db import get_db_engine


class ConnectTestWorkThread(QThread):
    result = Signal(tuple)

    def __init__(self, settings: dict):
        super().__init__()
        self.settings = settings

    def run(self):
        _result = True, ""
        engine = get_db_engine(self.settings)
        # 测试连接并执行查询
        try:
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                print("查询结果: ", result.fetchone())
                print("连接成功并执行查询成功!")
                _result = True, ""
        except Exception as e:
            print(f"连接失败: {e}")
            _result = False, f'连接失败: {str(e)}'

        self.result.emit(_result)


class RecommendedFetchWorkThread(QThread):
    process = Signal(str)

    def __init__(self):
        super().__init__()
        self.browser: Browser = None
        self.page: Page = None
        self._is_running = True

    def run(self):

        def url_listener(frame: Frame):
            print(f"New URL: {frame.url}")

        def response_listener(response: Response):
            # print(f'url: {response.url}')
            # print(f' : {await response.text()}')
            if response.url.startswith('https://www.temu.com/api/alexa/homepage/goods_list'):
                # await save_goods(response)
                response_text = response.text()
                print(f'发现商品 url: {response.url}')
                print(f'商品内容 text : {response_text}')
                self.process.emit(response_text)
            pass

        with sync_playwright() as playwright:
            # 通过命令: chrome://version/
            # 查看相关路径
            self.browser: BrowserContext = playwright.chromium.launch_persistent_context(
                executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                user_data_dir='/Users/liuyuhua/Library/Application Support/Google/Chrome/Default',
                headless=False,
                args=["--disable-blink-features=AutomationControlled"],
                # proxy={
                #     'server': 'http://127.0.0.1:7890',
                # }
            )
            page = self.browser.new_page()
            page.on("framenavigated", url_listener)
            page.on("response", response_listener)
            with open('stealth.min.js', 'r') as f:
                txt = f.read()
                page.add_init_script(txt)
            page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")
            page.add_init_script("""
                                        Object.defineProperty(window, 'chrome', {
                                            get: () => ({ runtime: {} })
                                        });
                                    """)
            page.add_init_script("""
                                        const getParameter = WebGLRenderingContext.prototype.getParameter;
                                        WebGLRenderingContext.prototype.getParameter = function(parameter) {
                                            if (parameter === 37445) {
                                                return 'Intel Open Source Technology Center';
                                            }
                                            if (parameter === 37446) {
                                                return 'Mesa DRI Intel(R) HD Graphics 620 (Kaby Lake GT2) ';
                                            }
                                            return getParameter(parameter);
                                        };
                                    """)
            page.goto("https://temu.com/")
            page.wait_for_load_state('load')
            while self._is_running:
                # 滚动指定的距离，例如向下滚动 1000 像素
                page.evaluate("window.scrollBy(0, 1000)")
                try:
                    # 等待某个元素出现
                    page.wait_for_selector("div._2ugbvrpI._3E4sGl93._28_m8Owy.R8mNGZXv._2rMaxXAr", timeout=3000)
                    # 执行点击操作
                    page.click("div._2ugbvrpI._3E4sGl93._28_m8Owy.R8mNGZXv._2rMaxXAr")
                    continue
                except BaseException as e:
                    logging.warning(str(e))
                try:
                    # 等待某个元素出现
                    page.wait_for_selector('//span[text()="重试"]', timeout=3000)
                    # 执行点击操作
                    page.click('//span[text()="重试"]')
                    continue
                except BaseException as e:
                    logging.warning(str(e))
            self.browser.close()
            pass

    def stop(self):
        self._is_running = False
        try:
            if self.browser:
                self.browser.close()
        except BaseException as e:
            pass