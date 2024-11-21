from PySide6.QtCore import QThread, Signal
from sqlalchemy import text

from controller.db import get_db_engine


# 测试连接
class ConnectTestThread(QThread):
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
