# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDoubleSpinBox,
    QFormLayout, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QTableView, QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.WindowModality.WindowModal)
        MainWindow.resize(658, 480)
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        self.actiontools = QAction(MainWindow)
        self.actiontools.setObjectName(u"actiontools")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget_2 = QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget_2.setUsesScrollButtons(False)
        self.tabWidget_2.setDocumentMode(False)
        self.tabWidget_2.setMovable(False)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_3 = QGridLayout(self.tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.verticalLayout.setContentsMargins(0, -1, -1, 0)
        self.textBrowser = QTextBrowser(self.tab)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)

        self.line_2 = QFrame(self.tab)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(0, -1, 8, -1)
        self.lineEdit = QLineEdit(self.tab)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_3.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(80, 40))
        self.pushButton.setMaximumSize(QSize(80, 40))
        self.pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.line = QFrame(self.tab)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.line)

        self.btn1 = QPushButton(self.tab)
        self.btn1.setObjectName(u"btn1")
        self.btn1.setMinimumSize(QSize(80, 40))
        self.btn1.setMaximumSize(QSize(80, 40))
        self.btn1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn1.setFocusPolicy(Qt.FocusPolicy.TabFocus)

        self.horizontalLayout_3.addWidget(self.btn1)

        self.line_3 = QFrame(self.tab)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.line_3)

        self.btn2 = QPushButton(self.tab)
        self.btn2.setObjectName(u"btn2")
        self.btn2.setEnabled(False)
        self.btn2.setMinimumSize(QSize(80, 40))
        self.btn2.setMaximumSize(QSize(80, 40))

        self.horizontalLayout_3.addWidget(self.btn2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.gridLayout_3.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_2 = QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tableView = QTableView(self.tab_2)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setAutoScrollMargin(16)
        self.tableView.verticalHeader().setMinimumSectionSize(21)
        self.tableView.verticalHeader().setDefaultSectionSize(30)

        self.verticalLayout_3.addWidget(self.tableView)

        self.line_4 = QFrame(self.tab_2)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_4.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout_3.addWidget(self.line_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, 8, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_3 = QPushButton(self.tab_2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(self.tab_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_2.addWidget(self.pushButton_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_5 = QGridLayout(self.tab_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)
        self.formLayout_2.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)
        self.formLayout_2.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout_2.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Label_6 = QLabel(self.tab_3)
        self.Label_6.setObjectName(u"Label_6")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.Label_6)

        self.db_type_2 = QComboBox(self.tab_3)
        self.db_type_2.addItem("")
        self.db_type_2.addItem("")
        self.db_type_2.setObjectName(u"db_type_2")
        self.db_type_2.setMinimumSize(QSize(200, 0))

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.db_type_2)

        self.Label_7 = QLabel(self.tab_3)
        self.Label_7.setObjectName(u"Label_7")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.Label_7)

        self.host_2 = QLineEdit(self.tab_3)
        self.host_2.setObjectName(u"host_2")
        self.host_2.setMinimumSize(QSize(200, 0))

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.host_2)

        self.Label_8 = QLabel(self.tab_3)
        self.Label_8.setObjectName(u"Label_8")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.Label_8)

        self.port_2 = QDoubleSpinBox(self.tab_3)
        self.port_2.setObjectName(u"port_2")
        self.port_2.setMinimumSize(QSize(200, 0))
        self.port_2.setDecimals(0)
        self.port_2.setMaximum(65535.000000000000000)
        self.port_2.setStepType(QAbstractSpinBox.StepType.DefaultStepType)
        self.port_2.setValue(5432.000000000000000)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.port_2)

        self.Label_9 = QLabel(self.tab_3)
        self.Label_9.setObjectName(u"Label_9")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.Label_9)

        self.user_2 = QLineEdit(self.tab_3)
        self.user_2.setObjectName(u"user_2")
        self.user_2.setMinimumSize(QSize(200, 0))

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.user_2)

        self.Label_10 = QLabel(self.tab_3)
        self.Label_10.setObjectName(u"Label_10")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.Label_10)

        self.password_2 = QLineEdit(self.tab_3)
        self.password_2.setObjectName(u"password_2")
        self.password_2.setMinimumSize(QSize(200, 0))

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.password_2)

        self.Label = QLabel(self.tab_3)
        self.Label.setObjectName(u"Label")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.Label)

        self.database = QLineEdit(self.tab_3)
        self.database.setObjectName(u"database")
        self.database.setMinimumSize(QSize(200, 0))

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.database)

        self.pushButton_4 = QPushButton(self.tab_3)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(55, 35))
        self.pushButton_4.setMaximumSize(QSize(55, 35))
        self.pushButton_4.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.pushButton_4)

        self.pushButton_5 = QPushButton(self.tab_3)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setMinimumSize(QSize(55, 35))
        self.pushButton_5.setMaximumSize(QSize(55, 35))
        self.pushButton_5.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.pushButton_5)


        self.gridLayout_5.addLayout(self.formLayout_2, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_3, "")

        self.gridLayout.addWidget(self.tabWidget_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.myStatusBar = QStatusBar(MainWindow)
        self.myStatusBar.setObjectName(u"myStatusBar")
        MainWindow.setStatusBar(self.myStatusBar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 658, 33))
        self.menu = QMenu(self.menuBar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actiontools)

        self.retranslateUi(MainWindow)
        self.pushButton_4.clicked.connect(MainWindow.save_settings_info)
        self.pushButton_5.clicked.connect(MainWindow.test_connection)
        self.btn1.clicked.connect(MainWindow.fetch_category)
        self.btn2.clicked.connect(MainWindow.stop_fetch_category)
        self.tabWidget_2.currentChanged.connect(MainWindow.tab_changed)
        self.pushButton.clicked.connect(MainWindow.show_tree_dialog)
        self.menuBar.triggered.connect(MainWindow.menu_action)
        self.pushButton_3.clicked.connect(MainWindow.fetch_increment)
        self.pushButton_2.clicked.connect(MainWindow.stop_fetch_increment)

        self.tabWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Temu Spider", None))
        self.actiontools.setText(QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5\u4ee3\u7406", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"https://www.temu.com/us-zh-Hans/mens---o3-1699.html", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u5206\u7c7b", None))
        self.btn1.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u83b7\u53d6", None))
        self.btn2.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u83b7\u53d6\u5546\u54c1", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u65b0\u9500\u91cf", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u66f4\u65b0\u9500\u91cf", None))
        self.Label_6.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5e93\u7c7b\u578b", None))
        self.db_type_2.setItemText(0, QCoreApplication.translate("MainWindow", u"PostgreSQL", None))
        self.db_type_2.setItemText(1, QCoreApplication.translate("MainWindow", u"MySQL", None))

        self.Label_7.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5e93\u4e3b\u673a:", None))
        self.Label_8.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5e93\u7aef\u53e3:", None))
        self.Label_9.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5e93\u7528\u6237:", None))
        self.Label_10.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5e93\u5bc6\u7801:", None))
        self.Label.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5e93\u540d", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u4ea4", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u7cfb\u7edf\u914d\u7f6e", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u5de5\u5177", None))
    # retranslateUi

