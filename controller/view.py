import json
import logging
import time
import webbrowser
from threading import Thread
from typing import Tuple

import requests
import schedule
from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QItemSelectionModel
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDialog, QTreeWidgetItem, QTableView

from controller.db import get_db_settings, save_db_settings
from controller.model.TaskModel import TaskModel
from controller.support import show_message
from controller.thread.category import CategoryFetchThread
from controller.thread.connection import ConnectTestThread
from controller.thread.detail import DetailFetchThread
from controller.thread.todo import TodoThread
from ui.ui_category import Ui_Dialog
from ui.ui_home import Ui_MainWindow
from ui.ui_proxy import Ui_Proxy


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    QT 应用主窗口事件槽
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.category_thread: CategoryFetchThread = None
        self.detail_thread: DetailFetchThread = None
        self.proxy = None
        self.dialog = None
        self.tableModel = TaskModel(None)
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
        """
        按分类批量抓取
        """

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

        self.category_thread = CategoryFetchThread(self.proxy, self.lineEdit.text())
        self.category_thread.process.connect(response_handler)
        self.category_thread.start()
        self.btn1.setEnabled(False)
        self.btn2.setEnabled(True)

    @Slot()
    def stop_fetch_category(self, *args, **kwargs):
        """
        停止按分类抓取
        """
        if self.category_thread.isRunning():
            self.category_thread.stop()
        self.btn1.setEnabled(True)
        self.btn2.setEnabled(False)
        self.category_thread = None

    @Slot()
    def fetch_increment(self, *args, **kwargs):
        """
        增量抓取
        """

        @Slot(dict)
        def detail_load(dict):
            print(dict)
            pass

        if self.tableModel.is_empty_data():
            show_message('没有待抓取的商品', warning=True)
            return
        self.detail_thread = DetailFetchThread(self.proxy)
        self.detail_thread.detail_load.connect(detail_load)
        self.detail_thread.start()
        pass

    @Slot()
    def stop_fetch_increment(self, *args, **kwargs):
        """
        停止增量抓取
        """
        if self.category_thread.isRunning():
            self.category_thread.stop()
        self.category_thread = None
        pass

    @Slot()
    def tab_changed(self, index: int):
        """
        切换tab页
        """

        @Slot(list)
        def todo_list_loaded(datas):
            self.tableModel = TaskModel(datas)
            self.tableView.setModel(self.tableModel)
            self.tableView.setSelectionModel(QItemSelectionModel(self.tableModel))
            # 设置列宽自适应内容
            # self.tableView.resizeColumnsToContents()

            # 设置单选模式
            self.tableView.setSelectionBehavior(QTableView.SelectRows)  # 选择行为：选择整行
            self.tableView.setSelectionMode(QTableView.SingleSelection)  # 选择模式：单选

            # 选项：设置表格最后一列扩展以填充剩余空间
            self.tableView.horizontalHeader().setStretchLastSection(True)

        try:
            if self.tabWidget_2.tabText(index) == '系统配置':
                settings = get_db_settings()
                self.db_type_2.setCurrentText(settings['db_type'])
                self.host_2.setText(settings['db_host'])
                self.port_2.setValue(float(settings['db_port']))
                self.user_2.setText(settings['db_user'])
                self.password_2.setText(settings['db_password'])
                self.database.setText(settings['db_database'])
            elif self.tabWidget_2.tabText(index) == '更新销量':

                todo_list_thread = TodoThread()
                todo_list_thread.data_load.connect(todo_list_loaded)
                todo_list_thread.start()
                pass
        except BaseException as e:
            logging.exception(e)
            show_message(str(e), True)

    @Slot()
    def save_settings_info(self, *args, **kwargs):
        """
        保存数据库连接
        """
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
        """
        测试连接
        """

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

        thread = ConnectTestThread(settings)
        thread.result.connect(result_handler)
        thread.start()

    @Slot()
    def show_tree_dialog(self, *args, **kwargs):
        """
        选择分类
        """
        if not self.dialog:
            self.dialog = CategoryDialog(self)
        self.dialog.show()
        if self.dialog.exec() == QDialog.Accepted:
            item = self.dialog.get_select_item()
            self.lineEdit.setText(f'https://www.temu.com{item["href"]}')

    @Slot()
    def menu_action(self, action: QAction):
        """
        菜单按钮触发
        """
        if action.text() == '测试代理':
            proxy_dialog = ProxyDialog(self)
            proxy_dialog.show()
            pass
        pass


class CategoryDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.treeWidget.clear()
        self.init_categories()

    def init_categories(self):
        with open('categories.json', 'r', encoding='utf-8') as f:
            categories = json.loads(f.read())
            for category in categories:
                node = self.create_tree_item(category, None)
                self.treeWidget.addTopLevelItem(node)

    def create_tree_item(self, data, parent=None):
        node = QTreeWidgetItem(parent, [data['text'], data['href']])
        if 'children' in data:
            for child in data['children']:
                child_node = self.create_tree_item(child, node)
                node.addChild(child_node)
        return node

    def get_select_item(self) -> Tuple:
        selItem = self.treeWidget.selectedItems()[0]
        return {
            'text': selItem.text(0),
            'href': selItem.text(1)
        }


class ProxyDialog(QtWidgets.QDialog, Ui_Proxy):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def accept(self):
        ip = self.iPLineEdit.text()
        port = self.SpinBox.value()
        url = f'https://tcp.ping.pe/{ip}:{port}'
        webbrowser.open(url)
        super().accept()

    def reject(self):
        super().reject()
