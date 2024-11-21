import json
import logging

from PySide6.QtCore import QThread, Signal
from playwright.sync_api import Response, Frame, sync_playwright, Browser, Page, BrowserContext

from controller.db import get_temu_sku_detail_todo_list


# 爬取商品详细信息
class DetailFetchThread(QThread):
    detail_load = Signal(str)
    process = Signal(float)

    def __init__(self, proxy):
        super().__init__()
        self.proxy = proxy
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self._is_running = True
        self.todo_list = []
        self.next_goods_id = None

    def run(self):

        def handle_route(route, request):
            url = request.url
            # if url == 'https://static.kwcdn.com/m-assets/assets/js/biz_vendors_332837eb1c65430ffc0e.js':
            #     # 取消请求，阻止脚本加载
            #     # route.abort()
            #     route.continue_(headers={"Cache-Control": "no-cache"})
            # else:
            #     # 允许其他请求正常进行
            #     route.continue_(headers={"Cache-Control": "no-cache"})
            route.continue_()

        def url_listener(frame: Frame):
            # self.fixed_page(frame.page)
            print(f"页面跳转: {frame.url}")
            if frame.url.startswith('https://www.temu.com/bgn_verification.html'):
                self.pause = True
            else:
                self.pause = False

        def domcontentloaded_listener(page: Page):
            # self.fixed_page(page)
            pass

        def on_request(request):
            print(f"Request: {request.url}")

        def response_listener(response: Response):
            print(f'url: {response.url}')
            # print(f' : {await response.text()}')
            if response.url == 'https://www.temu.com/api/poppy/v1/search?scene=search':
                try:
                    response_text = response.text()
                    print(f'商品详细json内容 text : {response_text}')
                    json_result = json.loads(response_text)
                    if 'success' in json_result and json_result['success']:
                        pass
                        self.next_goods_id = self.todo_list.pop()['goods_id']
                    else:
                        if 'message' in json_result:
                            raise BaseException(json_result['message'])
                        elif 'error_msg' in json_result:
                            raise BaseException(json_result['error_msg'])
                except BaseException as e:
                    logging.exception(e)
                    raise e

        # user_data_dir = '/Users/liuyuhua/Library/Application Support/Google/Chrome/Default'
        with sync_playwright() as playwright:
            # 通过命令: chrome://version/
            # 查看相关路径
            try:
                self.browser: Browser = playwright.chromium.connect_over_cdp(
                    endpoint_url="http://localhost:9222",
                )
                self.context: BrowserContext = self.browser.contexts[0]
                self.todo_list = get_temu_sku_detail_todo_list()
                page = self.context.new_page()
                page.on("framenavigated", url_listener)
                page.on("domcontentloaded", domcontentloaded_listener)
                page.on("response", response_listener)
                page.on("request", on_request)
                # page.route('**/*', lambda route: route.continue_(headers={"Cache-Control": "no-cache"}))
                page.route('**/*', handle_route)
                page.goto(f'https://www.temu.com/search_result.html', wait_until='load')
                self.fixed_page(page)
                # page.keyboard.press('F12')

                self.next_goods_id = self.todo_list.pop()['goods_id']
                while self._is_running and len(self.todo_list) > 0:
                    if self.next_goods_id:
                        try:
                            input_element = page.wait_for_selector("//input[@id='searchInput']", timeout=3000)
                            input_element.fill(self.next_goods_id)
                            input_element.press('Enter')
                            self.next_goods_id = None
                        except BaseException as e:
                            logging.exception(e)
                    else:
                        continue
                page.close()
                # page.wait_for_load_state('load')
                # self.fetch(page)
                # self.context.close()
                # self.browser.close()
            except BaseException as e:
                self.process.emit(repr(e))
                logging.exception(e)

    def fixed_page(self, page):
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
