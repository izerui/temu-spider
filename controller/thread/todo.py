from PySide6 import QtCore
from PySide6.QtCore import Signal

from controller.db import get_temu_sku_detail_todo_list

# 加载待更新销量goods_id列表
class TodoThread(QtCore.QThread):
    data_load = Signal(list)

    def __init__(self):
        super().__init__()

    def run(self):
        datas = get_temu_sku_detail_todo_list()
        self.data_load.emit(datas)
