import logging

from PySide6 import QtWidgets
from PySide6.QtCore import Slot

from controller.db import get_db_settings, save_db_settings
from controller.support import show_message
from controller.worker import ConnectTestWorkThread, RecommendedFetchWorkThread
from ui.ui_home import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    QT 应用主窗口事件槽
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.recommended_thread: RecommendedFetchWorkThread = None

    @Slot()
    def fetch_recommended(self, *args, **kwargs):

        @Slot(str)
        def response_handler(str):
            print('----->' + str)
            pass

        if self.recommended_thread:
            show_message('已经有一个相同的任务在运行了...', True)
            return

        self.recommended_thread = RecommendedFetchWorkThread()
        self.recommended_thread.process.connect(response_handler)
        self.recommended_thread.start()
        self.btn1.setEnabled(False)
        self.btn2.setEnabled(True)

    @Slot()
    def stop_fetch_recommended(self, *args, **kwargs):
        if self.recommended_thread.isRunning():
            self.recommended_thread.stop()
        self.btn1.setEnabled(True)
        self.btn2.setEnabled(False)
        self.recommended_thread = None

    @Slot()
    def tab_changed(self, index: int):
        try:
            print(index)
            if index == 1:
                settings = get_db_settings()
                self.db_type_2.setCurrentText(settings['db_type'])
                self.host_2.setText(settings['db_host'])
                self.port_2.setValue(float(settings['db_port']))
                self.user_2.setText(settings['db_user'])
                self.password_2.setText(settings['db_password'])
                self.database.setText(settings['db_database'])
            pass
        except BaseException as e:
            logging.exception(e)
            show_message(str(e), True)

    @Slot()
    def save_settings_info(self, *args, **kwargs):
        try:
            settings = {
                'db_type': self.db_type_2.currentText(),
                'db_host': self.host_2.text(),
                'db_port': self.port_2.value(),
                'db_user': self.user_2.text(),
                'db_password': self.password_2.text(),
                'db_database': self.database.text(),
            }
            save_db_settings(settings)
            show_message('设置成功')
            pass
        except BaseException as e:
            logging.exception(e)
            show_message(str(e), True)

    @Slot()
    def test_connection(self, *args, **kwargs):

        @Slot(tuple)
        def result_handler(result):
            success, error = result
            if success:
                show_message('连接成功')
            else:
                show_message(error, True)

        settings = {
            'db_type': self.db_type_2.currentText(),
            'db_host': self.host_2.text(),
            'db_port': int(self.port_2.value()),
            'db_user': self.user_2.text(),
            'db_password': self.password_2.text(),
            'db_database': self.database.text(),
        }

        thread = ConnectTestWorkThread(settings)
        thread.result.connect(result_handler)
        thread.start()
