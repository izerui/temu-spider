import json
import logging
import random
import time
from urllib import parse

from PySide6.QtCore import QThread, Signal
from playwright.sync_api import Response, Frame, sync_playwright, Browser, Page, BrowserContext

from controller.db import add_temu_sku


# 爬取分类商品
class CategoryFetchWorkThread(QThread):
    process = Signal(str)

    def __init__(self, proxy, page_open_url):
        super().__init__()
        self.proxy = proxy
        self.page_open_url = page_open_url
        self.page_current_url = page_open_url
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self._is_running = True
        self.sku_links = []

    def run(self):

        def url_listener(frame: Frame):
            # self.fixed_page(frame.page)
            print(f"页面跳转: {frame.url}")

        def domcontentloaded_listener(page: Page):
            # self.fixed_page(page)
            pass

        def response_listener(response: Response):
            # print(f'url: {response.url}')
            # print(f' : {await response.text()}')
            if response.url.startswith('https://www.temu.com/us-zh-Hans/api/poppy/v1/opt'):
                # await save_goods(response)
                try:
                    response_text = response.text()
                    print(f'商品json内容 text : {response_text}')
                    json_result = json.loads(response_text)
                    if json_result['success']:
                        add_temu_sku(json_result)
                    else:
                        raise BaseException(json_result['message'])
                except BaseException as e:
                    self.process.emit(repr(e))
                    raise e
                # self.process.emit(response_text)
            pass

        # user_data_dir = '/Users/liuyuhua/Library/Application Support/Google/Chrome/Default'
        with sync_playwright() as playwright:
            # 通过命令: chrome://version/
            # 查看相关路径
            try:
                self.browser: BrowserContext = playwright.chromium.launch_persistent_context(
                    channel="chrome",
                    user_data_dir='',
                    headless=False,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                    ],
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                    proxy=self.proxy,
                )
                page = self.browser.new_page()
                page.on("framenavigated", url_listener)
                page.on("domcontentloaded", domcontentloaded_listener)
                page.on("response", response_listener)
                self.fixed_page(page)
                page.goto(self.page_open_url, wait_until='load')
                # page.wait_for_load_state('load')
                self.fetch(page)
            except BaseException as e:
                self.process.emit(repr(e))
                logging.exception(e)

    def fetch(self, page: Page):
        page_count = 0
        while self._is_running:
            self.process.emit("信息: 重置时长超过50ms的长任务数组记录。")
            self.clear_long_task_array(page)
            print(page.url)
            time.sleep(random.randint(1, 3))
            try:
                # 如果出现验证码，等待人工验证，直到出现查看更多按钮
                if page.url.startswith("https://www.temu.com/bgn_verification.html"):
                    try:
                        self.process.emit("警告: 出现验证码页面。")
                        page.wait_for_selector("div._2ugbvrpI._3E4sGl93._28_m8Owy.R8mNGZXv._2rMaxXAr", timeout=30000)
                        continue
                    except:
                        pass
                # 如果转到空白页，则按上一次的地址进行跳转
                elif page.url == 'about:blank':
                    try:
                        self.process.emit("错误: 跳转到空白页,请关闭后重试。")
                        page.goto(self.page_current_url, wait_until='load')
                    except:
                        pass
                    continue
                # 如果转到登录页，则后退，并刷新页面
                elif page.url.startswith('https://www.temu.com/login.html'):  # 防爬机制导致转到登录页的情况
                    try:
                        self.process.emit("错误: 跳转到登录页。")
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
                    self.process.emit("信息: 正常显示商品列表页。")
                    self.page_current_url = page.url
                    try:
                        # 查找 class 中包含 autoFitList 的 div 元素
                        divs = page.query_selector_all('div[class*="autoFitList"]')
                        for div in divs:
                            alist = div.query_selector_all('a')
                            for a in alist:
                                href = a.get_attribute('href')
                                href = parse.unquote(href)
                                link = f"https://temu.com/{href}"
                                self.sku_links.append(link)
                    except BaseException as e:
                        pass

                    # 如果翻页进行2~4次左右则新开一个商品详情页并关闭，然后刷新当前商品列表页面
                    if page_count > random.randint(2, 4):
                        self.process.emit("信息: 打开随机商品详情页并关闭。")
                        self.open_sku_and_close()
                        self.process.emit("信息: 刷新列表页，重置url链接参数。")
                        page.reload(wait_until='load')
                        page_count = 0
            except BaseException as e:
                self.process.emit(f'错误: {repr(e)}')
                logging.warning(repr(e))

            # 取模运算决定执行逻辑
            if (random.randint(1, 100) // 2) % 2 == 0:
                # 模拟按下空格键
                self.process.emit(f'信息: 模拟空格键按下。')
                page.keyboard.press("Space")
            else:
                # 模拟按下空格键
                self.process.emit(f'信息: 模拟空格键按下。')
                page.keyboard.press("Space")

            self.process.emit(f'信息: 模拟移动鼠标。')

            # 随机按三个位置移动鼠标
            page.mouse.move(random.randint(0, 1000), random.randint(0, 1000), steps=100)
            time.sleep(1)
            page.mouse.move(random.randint(0, 1000), random.randint(0, 1000), steps=100)
            time.sleep(1)
            page.mouse.move(random.randint(0, 1000), random.randint(0, 1000), steps=100)
            time.sleep(1)

            # 滚动指定的距离，例如向下滚动 1000 像素
            self.process.emit(f'信息: 向下滚动1000像素。')
            page.evaluate("window.scrollBy(0, 1000)")

            try:
                # 等待某个元素出现
                page.wait_for_selector("div._2ugbvrpI._3E4sGl93._28_m8Owy.R8mNGZXv._2rMaxXAr", timeout=3000)
                # 执行点击操作
                self.process.emit(f'信息: 点击更多按钮，显示更多商品。')
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
                    self.process.emit(f'信息: 点击重试按钮。')
                    page.click('//span[text()="重试"]', delay=random.randint(1000, 3000))
            except BaseException as e:
                logging.warning(repr(e))
            pass
            # page.bring_to_front()
        self.process.emit(f'信息: 关闭页面')
        self.context.close()
        self.browser.close()
        pass

    def clear_long_task_array(self, page: Page):
        page.evaluate("""() => {
            if (window.__tti && window.__tti.e) {
                window.__tti.e = [];
            }
        }""")

    def open_sku_and_close(self):
        try:
            if len(self.sku_links) > 0:
                last_sku_link = self.sku_links[-1]
                sku_page = self.browser.new_page()
                self.fixed_page(sku_page)
                sku_page.goto(last_sku_link, wait_until='load')
                self.process.emit("信息: 随机等待1~3秒后关闭详情页。")
                # 滚动指定的距离，例如向下滚动 1000 像素
                self.process.emit(f'信息: 详情页向下滚动1000像素。')
                sku_page.evaluate(f"window.scrollBy(0, {random.randint(200, 800)})")

                time.sleep(random.randint(1, 3))
                sku_page.close()
        except BaseException as e:
            logging.warning(repr(e))
            pass

    def fixed_page(self, page):
        self.process.emit(f'信息: 尝试注入反爬脚本。url: {page.url}')
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page.add_init_script("""
                            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                            """)
        page.add_init_script("""
                            Object.defineProperty(window, '__HEADER_USERAGENT__', {
                                value: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                                writable: false,
                                configurable: false
                            });
                            // 修改 navigator.userAgent 以避免被检测为爬虫
                            Object.defineProperty(navigator, 'userAgent', {
                                get: () => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                            });

                            // 修改 window.__ERROR_SAMPLE_RATE__ 以避免被检测为爬虫
                            Object.defineProperty(window, '__ERROR_SAMPLE_RATE__', {
                                value: 0.0,
                                writable: false,
                                configurable: false
                            });
                            """)
        # 执行 JavaScript 代码来移除带有 retain-in-offline="true" 属性的 <script> 标签
        page.evaluate('''
                    const scripts = document.querySelectorAll('script[retain-in-offline="true"]');
                    scripts.forEach(script => script.parentNode.removeChild(script));
                ''')
        # # 在页面加载前注入脚本以覆盖 document.addEventListener 方法
        # page.add_init_script("""
        #     (function() {
        #         const originalAddEventListener = document.addEventListener;
        #         document.addEventListener = function(type, listener, options) {
        #             if (type !== 'DOMContentLoaded') {
        #                 return originalAddEventListener.call(document, type, listener, options);
        #             }
        #         };
        #     })();
        #     """)

    def stop(self):
        self._is_running = False
        try:
            self.process.emit("警告: 关闭页面")
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
        except BaseException as e:
            pass
