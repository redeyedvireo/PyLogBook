# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'search_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_searchDialog(object):
    def setupUi(self, searchDialog):
        if not searchDialog.objectName():
            searchDialog.setObjectName(u"searchDialog")
        searchDialog.resize(400, 300)
        self.verticalLayout_2 = QVBoxLayout(searchDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(searchDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.searchEdit = QLineEdit(searchDialog)
        self.searchEdit.setObjectName(u"searchEdit")

        self.horizontalLayout.addWidget(self.searchEdit)

        self.searchButton = QPushButton(searchDialog)
        self.searchButton.setObjectName(u"searchButton")
        self.searchButton.setEnabled(False)

        self.horizontalLayout.addWidget(self.searchButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.resultsListWidget = QListWidget(searchDialog)
        self.resultsListWidget.setObjectName(u"resultsListWidget")
        self.resultsListWidget.setStyleSheet(u"background-color: white;")

        self.horizontalLayout_2.addWidget(self.resultsListWidget)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.closeButton = QPushButton(searchDialog)
        self.closeButton.setObjectName(u"closeButton")

        self.verticalLayout.addWidget(self.closeButton)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.retranslateUi(searchDialog)

        QMetaObject.connectSlotsByName(searchDialog)
    # setupUi

    def retranslateUi(self, searchDialog):
        searchDialog.setWindowTitle(QCoreApplication.translate("searchDialog", u"Search", None))
        self.label.setText(QCoreApplication.translate("searchDialog", u"Search string", None))
        self.searchButton.setText(QCoreApplication.translate("searchDialog", u"Search", None))
        self.closeButton.setText(QCoreApplication.translate("searchDialog", u"Close", None))
    # retranslateUi

