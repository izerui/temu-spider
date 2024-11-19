import time
from typing import Union, Any

import PySide6.QtCore
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon


##
# 在PyQt中，模型可以针对不同的组件（或者组件的不同部分，比如存储数据、界面展示数据、按钮的提示等）提供不同的数据。例如，Qt.DisplayRole用于视图的文本显示。通常来说，模型中的数据项包含一系列不同的数据角色，数据角色定义在 Qt.ItemDataRole 枚举中，老猿掌握的包括下列枚举值：
# Qt.DisplayRole：文本表格中要渲染显示的数据，当存储的内部字典值要显示为可理解的文字含义数据时对应数据与实际存储数据会不一致
# Qt.EditRole：编辑器中正在编辑的数据，老猿认为这也应该是实际存储的数据
# Qt.ToolTipRole：数据项的工具提示的显示数据
# Qt.WhatsThisRole：项为"What’s This?"模式显示的数据
# Qt.DecorationRole：数据被渲染为图标等装饰(数据为QColor/ QIcon/ QPixmap类型)
# Qt.StatusTipRole：数据显示在状态栏中(数据为QString类型)
# Qt.SizeHintRole：数据项的大小提示，将会应用到视图(数据为QString类型)
# Qt.CheckStateRole：数据项前面的checkbox选择状态，当数据项构建时使用了setCheckable(True)时会发生作用
# Qt.TextAlignmentRole：数据项对齐方式，当设置了数据项的对齐格式时有效
##
class BaseModel(QtCore.QAbstractTableModel):

    def __init__(self, heads, datas):
        super().__init__()
        if datas == None:
            datas = []
        self.datas = datas
        self.originHeads = heads
        self.heads = list(filter(lambda x: 'hidden' not in x or not x['hidden'], heads))

    def headerData(self, section: int, orientation: PySide6.QtCore.Qt.Orientation, role: int = ...) -> Any:
        if role == QtCore.Qt.DisplayRole:
            if orientation == PySide6.QtCore.Qt.Orientation.Horizontal:
                return self.heads[section]['title']
            else:
                return str(section + 1)

    def data(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex],
             role: int = ...) -> Any:
        row = index.row()
        col = index.column()
        item = self.datas[row]
        key = self.heads[col]['code']
        if role == Qt.DisplayRole:
            if 'label_hidden' in self.heads[col] and self.heads[col]['label_hidden']:
                return None
            else:
                if 'label_format_fun' in self.heads[col]:
                    label_format_fun = self.heads[col]['label_format_fun']
                    return label_format_fun(key, item)
                else:
                    if isinstance(item[key], int):
                        return str(int(item[key]))
                    else:
                        return str(item[key])
        elif role == Qt.DecorationRole:
            if 'icon_fun' in self.heads[col]:
                icon_fun = self.heads[col]['icon_fun']
                return icon_fun(key, item)

    def columnCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self.heads)

    def rowCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self.datas)

    def icon_fun(self, key, item) -> QIcon:
        pass

    def date_time_fun(self, key, item) -> str:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item[key] / 1000)) if item[key] else None
