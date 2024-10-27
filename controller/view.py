import logging
import time
from threading import Thread

import requests
import schedule
from PySide6 import QtWidgets
from PySide6.QtCore import Slot

from controller.db import get_db_settings, save_db_settings
from controller.support import show_message
from controller.worker import ConnectTestWorkThread, CategoryFetchWorkThread
from ui.ui_home import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    QT 应用主窗口事件槽
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.category_thread: CategoryFetchWorkThread = None
        self.proxy = None
        # self.proxy = {
        #     'server': 'http://as.x479.kdlfps.com:18866',
        #     'username': 'f2277811048',
        #     'password': 'cqclmjfn',
        # }
        # self.proxy = {
        #     'server': 'http://proxy.shenlongproxy.com:31212',
        #     'username': 'customer-cb8773a8ed6-country-US-session-250sahsop-time-3',
        #     'password': '26589497',
        # }
        # self.proxy = {
        #     'server': 'http://b4ade676d0deda12.fkz.as.ipidea.online:2336',
        #     'username': 'abcd003-zone-custom-session-123b1cmag-sessTime-3',
        #     'password': 'abcd003',
        # }
        thread = Thread(target=self.schedule_ip_status)
        thread.start()

    def schedule_ip_status(self):
        """
        定时刷新出口信息,并显示在状态栏
        """

        last_tip_message: str = None
        time_out_seconds: int = 30

        def refresh_ip():
            try:
                self.myStatusBar.showMessage('加载中...')
                if self.proxy:
                    proxies = {
                        "http": f"{self.proxy['server'][:7]}{self.proxy['username']}:{self.proxy['password']}@{self.proxy['server'][7:]}",
                        "https": f"{self.proxy['server'][:7]}{self.proxy['username']}:{self.proxy['password']}@{self.proxy['server'][7:]}",
                    }
                    response = requests.get('https://api.ip.cc/', proxies=proxies)
                else:
                    response = requests.get('https://api.ip.cc/')
                ipObj = response.json()
                self.myStatusBar.showMessage(
                    f'连接成功: {ipObj["ip"]}  {ipObj["country"]}  {ipObj["timezone"]}  {ipObj["asn_name"]}')
            except BaseException as e:
                self.myStatusBar.showMessage(f'连接失败: {repr(e)}')

        # 初始化先执行一次
        refresh_ip()
        # 每隔30秒执行一次任务
        schedule.every(30).seconds.do(refresh_ip)
        while True:
            schedule.run_pending()
            time.sleep(1)

    @Slot()
    def fetch_category(self, *args, **kwargs):

        @Slot(str)
        def response_handler(responseText):
            print('----->' + responseText)
            self.textBrowser.append(responseText)
            pass

        if not self.lineEdit.text():
            show_message('请输入要爬取的temu网站的具体某个商品列表页地址', warning=True)
            return

        self.textBrowser.clear()
        if self.category_thread:
            show_message('已经有一个相同的任务在运行了...', True)
            return

        self.category_thread = CategoryFetchWorkThread(self.proxy, self.lineEdit.text())
        self.category_thread.process.connect(response_handler)
        self.category_thread.start()
        self.btn1.setEnabled(False)
        self.btn2.setEnabled(True)

    @Slot()
    def stop_fetch_category(self, *args, **kwargs):
        if self.category_thread.isRunning():
            self.category_thread.stop()
        self.btn1.setEnabled(True)
        self.btn2.setEnabled(False)
        self.category_thread = None

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
