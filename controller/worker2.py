import logging
import random
import time
from urllib import parse

from PySide6.QtCore import QThread, Signal
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

    def __init__(self, page_open_url):
        super().__init__()
        self.page_open_url = page_open_url
        self.page_current_url = page_open_url
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self._is_running = True
        self.sku_links = []

    def run(self):

        def url_listener(frame: Frame):
            print(f"页面跳转: {frame.url}")

        def response_listener(response: Response):
            # print(f'url: {response.url}')
            # print(f' : {await response.text()}')
            if response.url.startswith('https://www.temu.com/api/alexa/homepage/goods_list'):
                # await save_goods(response)
                response_text = response.text()
                print(f'发现商品 url: {response.url}')
                print(f'商品内容 text : {response_text}')
                # self.process.emit(response_text)
            pass

        # user_data_dir = '/Users/liuyuhua/Library/Application Support/Google/Chrome/Default'
        with sync_playwright() as playwright:
            # 通过命令: chrome://version/
            # 查看相关路径
            try:
                self.browser: Browser = playwright.chromium.launch(
                    channel="chrome",
                    headless=False,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-infobars',
                        '--no-sandbox',
                        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    ],
                    ignore_default_args=[
                        '--enable-automation'
                    ],
                    proxy={
                        'server': 'socks5://127.0.0.1:1087',
                        # 'username': 'vyxbqrga',
                        # 'password': 'y5f9sg8m',
                    }
                )
                self.context = self.browser.new_context()
                # page = self.browser.new_page()
                page = self.context.new_page()
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
                page.goto(self.page_open_url, wait_until='load')
                # page.wait_for_load_state('load')
                self.fetch(page)
            except BaseException as e:
                self.process.emit(str(e))
                logging.exception(e)

    def fetch(self, page: Page):
        page_count = 0
        while self._is_running:
            print(page.url)
            time.sleep(random.randint(1, 3))
            # 如果出现验证码，等待人工验证，直到出现查看更多按钮
            if page.url.startswith("https://www.temu.com/bgn_verification.html"):
                try:
                    page.wait_for_selector("div._2ugbvrpI._3E4sGl93._28_m8Owy.R8mNGZXv._2rMaxXAr", timeout=3000)
                    continue
                except:
                    pass
            # 如果转到空白页，则按上一次的地址进行跳转
            elif page.url == 'about:blank':
                try:
                    page.goto(self.page_current_url, wait_until='load')
                except:
                    pass
                continue
            # 如果转到登录页，则后退，并刷新页面
            elif page.url.startswith('https://www.temu.com/login.html'):  # 防爬机制导致转到登录页的情况
                try:
                    last_url = page.url.replace('https://www.temu.com/login.html?from=', '')
                    last_url = parse.unquote(last_url)
                    self.page_current_url = last_url
                    self.open_sku_and_close()
                    page.goto(self.page_current_url, wait_until='load')
                except:
                    pass
                continue
            # 如果正常为当前商品列表页则执行抓取
            if page.url.startswith(self.page_open_url):
                self.page_current_url = page.url
                try:
                    # 查找 class 中包含 autoFitList 的 div 元素
                    divs = page.query_selector_all('div[class*="autoFitList"]')
                    for div in divs:
                        alist = div.query_selector_all('a')
                        for a in alist:
                            href = a.get_attribute('href')
                            link = f"https://temu.com/{href}"
                            self.sku_links.append(link)
                            self.process.emit(link)
                except BaseException as e:
                    pass

                # 如果翻页进行2~4次左右则新开一个商品详情页并关闭，然后刷新当前商品列表页面
                if page_count > random.randint(2, 4):
                    self.open_sku_and_close()
                    page.reload(wait_until='load')
                    page_count = 0

            # 滚动指定的距离，例如向下滚动 1000 像素
            page.evaluate("window.scrollBy(0, 1000)")
            try:
                # 等待某个元素出现
                page.wait_for_selector("div._2ugbvrpI._3E4sGl93._28_m8Owy.R8mNGZXv._2rMaxXAr", timeout=3000)
                # 执行点击操作
                page.click("div._2ugbvrpI._3E4sGl93._28_m8Owy.R8mNGZXv._2rMaxXAr", delay=random.randint(2000, 5000))
                page_count += 1
                continue
            except BaseException as e:
                logging.warning(str(e))

            # 出现重试
            try:
                if len(self.sku_links) > 0:
                    # 等待某个元素出现
                    page.wait_for_selector('//span[text()="重试"]', timeout=3000)
                    # 执行点击操作
                    page.click('//span[text()="重试"]', delay=random.randint(1000, 3000))
            except BaseException as e:
                logging.warning(str(e))

            # page.bring_to_front()

        self.context.close()
        self.browser.close()
        pass

    def open_sku_and_close(self):
        try:
            if len(self.sku_links) > 0:
                last_sku_link = self.sku_links[-1]
                sku_page = self.browser.new_page()
                sku_page.goto(last_sku_link, wait_until='load')
                sku_page.close()
        except BaseException as e:
            pass

    def stop(self):
        self._is_running = False
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
        except BaseException as e:
            pass
