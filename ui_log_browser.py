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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTextBrowser, QVBoxLayout, QWidget)
import PyLogBook_rc

class Ui_LogBrowserWidgetSimple(object):
    def setupUi(self, LogBrowserWidgetSimple):
        if not LogBrowserWidgetSimple.objectName():
            LogBrowserWidgetSimple.setObjectName(u"LogBrowserWidgetSimple")
        LogBrowserWidgetSimple.resize(511, 605)
        self.verticalLayout = QVBoxLayout(LogBrowserWidgetSimple)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.textBrowser = QTextBrowser(LogBrowserWidgetSimple)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(LogBrowserWidgetSimple)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.pageSpin = QSpinBox(LogBrowserWidgetSimple)
        self.pageSpin.setObjectName(u"pageSpin")
        self.pageSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.horizontalLayout.addWidget(self.pageSpin)

        self.numPagesLabel = QLabel(LogBrowserWidgetSimple)
        self.numPagesLabel.setObjectName(u"numPagesLabel")

        self.horizontalLayout.addWidget(self.numPagesLabel)

        self.horizontalSpacer_2 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.beginButton = QPushButton(LogBrowserWidgetSimple)
        self.beginButton.setObjectName(u"beginButton")
        icon = QIcon()
        icon.addFile(u":/PyLogBook/Resources/first-page.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.beginButton.setIcon(icon)

        self.horizontalLayout.addWidget(self.beginButton)

        self.previousButton = QPushButton(LogBrowserWidgetSimple)
        self.previousButton.setObjectName(u"previousButton")
        icon1 = QIcon()
        icon1.addFile(u":/PyLogBook/Resources/previous-page.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.previousButton.setIcon(icon1)

        self.horizontalLayout.addWidget(self.previousButton)

        self.nextButton = QPushButton(LogBrowserWidgetSimple)
        self.nextButton.setObjectName(u"nextButton")
        icon2 = QIcon()
        icon2.addFile(u":/PyLogBook/Resources/next-page.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.nextButton.setIcon(icon2)

        self.horizontalLayout.addWidget(self.nextButton)

        self.endButton = QPushButton(LogBrowserWidgetSimple)
        self.endButton.setObjectName(u"endButton")
        icon3 = QIcon()
        icon3.addFile(u":/PyLogBook/Resources/last-page.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.endButton.setIcon(icon3)

        self.horizontalLayout.addWidget(self.endButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(LogBrowserWidgetSimple)

        QMetaObject.connectSlotsByName(LogBrowserWidgetSimple)
    # setupUi

    def retranslateUi(self, LogBrowserWidgetSimple):
        LogBrowserWidgetSimple.setWindowTitle(QCoreApplication.translate("LogBrowserWidgetSimple", u"Form", None))
        self.label.setText(QCoreApplication.translate("LogBrowserWidgetSimple", u"Page:", None))
        self.numPagesLabel.setText(QCoreApplication.translate("LogBrowserWidgetSimple", u"%1 pages", None))
        self.beginButton.setText("")
        self.previousButton.setText("")
        self.nextButton.setText("")
        self.endButton.setText("")
    # retranslateUi

