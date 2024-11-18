# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'proxy.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QSpinBox, QWidget)

class Ui_Proxy(object):
    def setupUi(self, Proxy):
        if not Proxy.objectName():
            Proxy.setObjectName(u"Proxy")
        Proxy.resize(383, 221)
        self.gridLayout = QGridLayout(Proxy)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(Proxy)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        self.iPLabel = QLabel(Proxy)
        self.iPLabel.setObjectName(u"iPLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.iPLabel)

        self.iPLineEdit = QLineEdit(Proxy)
        self.iPLineEdit.setObjectName(u"iPLineEdit")
        self.iPLineEdit.setMinimumSize(QSize(200, 0))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.iPLineEdit)

        self.Label = QLabel(Proxy)
        self.Label.setObjectName(u"Label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.Label)

        self.SpinBox = QSpinBox(Proxy)
        self.SpinBox.setObjectName(u"SpinBox")
        self.SpinBox.setMinimumSize(QSize(100, 0))
        self.SpinBox.setMaximum(65535)
        self.SpinBox.setValue(8080)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.SpinBox)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)


        self.retranslateUi(Proxy)
        self.buttonBox.accepted.connect(Proxy.accept)
        self.buttonBox.rejected.connect(Proxy.reject)

        QMetaObject.connectSlotsByName(Proxy)
    # setupUi

    def retranslateUi(self, Proxy):
        Proxy.setWindowTitle(QCoreApplication.translate("Proxy", u"Dialog", None))
        self.iPLabel.setText(QCoreApplication.translate("Proxy", u"\u670d\u52a1\u5668:", None))
        self.iPLineEdit.setText(QCoreApplication.translate("Proxy", u"127.0.0.1", None))
        self.Label.setText(QCoreApplication.translate("Proxy", u"\u7aef\u53e3:", None))
    # retranslateUi

