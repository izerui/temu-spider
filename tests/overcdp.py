import asyncio

from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        # 连接到已经启动的 Chrome 浏览器
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")

        browserContext = browser.contexts[0]
        # 创建一个新的标签页
        page = await browserContext.new_page()

        # 在新标签页中导航到一个网址
        await page.goto("https://www.google.com")
        title = await page.title()
        print(f"Page title: {title}")

        # 关闭浏览器连接（可选，根据需求决定是否关闭）
        # await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
