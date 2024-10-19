import asyncio
import logging
from enum import Enum

from playwright.async_api import async_playwright, Browser, Page, Response
from playwright.sync_api import Browser, Frame

class PageStatus(Enum):
    home = '首页'
    bgn_verification = '验证码'
    skus = '商品列表'


current_status = PageStatus.home


def url_listener(frame: Frame):
    """
    监听页面地址变化
    :param frame:
    :return:
    """
    print(f"New URL: {frame.url}")
    if frame.url.startswith('https://www.temu.com/bgn_verification.html'):
        current_status = PageStatus.bgn_verification
    else:
        current_status = PageStatus.skus


async def response_listener(response: Response):
    # print(f'url: {response.url}')
    # print(f' : {await response.text()}')
    if response.url.startswith('https://www.temu.com/api/alexa/homepage/goods_list'):
        # await save_goods(response)
        print(f'发现商品 url: {response.url}')
        print(f'商品内容 text : {await response.text()}')
    pass


async def page_turning(page: Page):
    """
    首页翻页
    :param page:
    :return:
    """
    index = 0
    while True:
        # 滚动指定的距离，例如向下滚动 1000 像素
        await page.evaluate("window.scrollBy(0, 1000)")
        try:
            # 等待某个元素出现
            await page.wait_for_selector("div._2ugbvrpI._3E4sGl93._28_m8Owy.R8mNGZXv._2rMaxXAr")
            # 执行点击操作
            await page.click("div._2ugbvrpI._3E4sGl93._28_m8Owy.R8mNGZXv._2rMaxXAr")
            continue
        except BaseException as e:
            logging.exception(e)
        try:
            # 等待某个元素出现
            await page.wait_for_selector('//span[text()="重试"]')
            # 执行点击操作
            await page.click('//span[text()="重试"]')
            continue
        except BaseException as e:
            logging.exception(e)
    pass


async def main():
    # user_data_dir = '/Users/liuyuhua/Library/Application Support/Google/Chrome/Default'
    async with async_playwright() as p:
        browser: Browser = await p.chromium.launch_persistent_context(
            executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            user_data_dir='',
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        # browser: Browser = await p.chromium.launch(
        #     headless=False,
        #     args=["--disable-blink-features=AutomationControlled"],
        # )
        # context: BrowserContext = await browser.new_context()
        # page = await context.new_page()
        page = await browser.new_page()
        # 监听 framenavigated 事件
        page.on("framenavigated", url_listener)
        # 监听页面请求
        # page.on("request", request_listener)
        # 监听页面响应
        page.on("response", response_listener)
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        await page.add_init_script("""
                    Object.defineProperty(window, 'chrome', {
                        get: () => ({ runtime: {} })
                    });
                """)
        await page.add_init_script("""
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
        await page.goto("https://temu.com/")
        await page.screenshot(path="example.png")
        await page_turning(page)

        # 在这里进行自动化操作
        # await browser.close()
        while True:
            pass


if __name__ == '__main__':
    asyncio.run(main())
