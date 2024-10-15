from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMessageBox

from support import Settings
from ui.ui_home import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    @Slot()
    def start_fetch_data(self, *args, **kwargs):
        msg: QMessageBox = QMessageBox()
        msg.setText('测试内容')
        msg.setWindowTitle('测试标题')
        msg.exec()
        pass

    @Slot()
    def tab_changed(self, index: int):
        print(index)
        if index == 1:
            settings = Settings.get_settings()
            self.db_type_2.setCurrentText(settings['db_type'])
            self.host_2.setText(settings['db_host'])
            self.port_2.setValue(settings['db_port'])
            self.user_2.setText(settings['db_user'])
            self.password_2.setText(settings['db_password'])
        pass

    @Slot()
    def save_settings_info(self, *args, **kwargs):
        settings = {
            'db_type': self.db_type_2.currentText(),
            'db_host': self.host_2.text(),
            'db_port': self.port_2.value(),
            'db_user': self.user_2.text(),
            'db_password': self.password_2.text(),
        }
        Settings.save_settings(settings)
        pass
