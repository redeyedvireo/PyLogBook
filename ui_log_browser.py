# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log_browser.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_LogBrowserWidgetSimple(object):
    def setupUi(self, LogBrowserWidgetSimple):
        if not LogBrowserWidgetSimple.objectName():
            LogBrowserWidgetSimple.setObjectName(u"LogBrowserWidgetSimple")
        LogBrowserWidgetSimple.resize(418, 605)
        self.verticalLayout = QVBoxLayout(LogBrowserWidgetSimple)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.textBrowser = QTextBrowser(LogBrowserWidgetSimple)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.beginButton = QPushButton(LogBrowserWidgetSimple)
        self.beginButton.setObjectName(u"beginButton")

        self.horizontalLayout.addWidget(self.beginButton)

        self.previousButton = QPushButton(LogBrowserWidgetSimple)
        self.previousButton.setObjectName(u"previousButton")

        self.horizontalLayout.addWidget(self.previousButton)

        self.horizontalSpacer = QSpacerItem(17, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(LogBrowserWidgetSimple)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.pageSpin = QSpinBox(LogBrowserWidgetSimple)
        self.pageSpin.setObjectName(u"pageSpin")

        self.horizontalLayout.addWidget(self.pageSpin)

        self.numPagesLabel = QLabel(LogBrowserWidgetSimple)
        self.numPagesLabel.setObjectName(u"numPagesLabel")

        self.horizontalLayout.addWidget(self.numPagesLabel)

        self.horizontalSpacer_2 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.nextButton = QPushButton(LogBrowserWidgetSimple)
        self.nextButton.setObjectName(u"nextButton")

        self.horizontalLayout.addWidget(self.nextButton)

        self.endButton = QPushButton(LogBrowserWidgetSimple)
        self.endButton.setObjectName(u"endButton")

        self.horizontalLayout.addWidget(self.endButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(LogBrowserWidgetSimple)

        QMetaObject.connectSlotsByName(LogBrowserWidgetSimple)
    # setupUi

    def retranslateUi(self, LogBrowserWidgetSimple):
        LogBrowserWidgetSimple.setWindowTitle(QCoreApplication.translate("LogBrowserWidgetSimple", u"Form", None))
        self.beginButton.setText(QCoreApplication.translate("LogBrowserWidgetSimple", u"Beginning", None))
        self.previousButton.setText(QCoreApplication.translate("LogBrowserWidgetSimple", u"Previous", None))
        self.label.setText(QCoreApplication.translate("LogBrowserWidgetSimple", u"Page:", None))
        self.numPagesLabel.setText(QCoreApplication.translate("LogBrowserWidgetSimple", u"/ %1 pages", None))
        self.nextButton.setText(QCoreApplication.translate("LogBrowserWidgetSimple", u"Next", None))
        self.endButton.setText(QCoreApplication.translate("LogBrowserWidgetSimple", u"End", None))
    # retranslateUi

