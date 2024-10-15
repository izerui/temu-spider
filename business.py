import os.path
import uuid

from playwright.async_api import Response


async def save_goods(response: Response):
    try:
        # 获取响应的内容
        body = await response.json()
        # 将内容写入文件
        file_path = os.path.join('txt', f'{uuid.uuid4().hex}.json')
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(body)
    except Exception as e:
        print(f"Error handling response: {e}")
    pass
